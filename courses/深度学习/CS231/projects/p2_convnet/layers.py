"""P2 · 神经网络层库（对应 L04-L06，对标 Assignment 2 的 fast_layers.py）。

命名约定：x (N,C,H,W)，w (F,C,HH,WW)。每个前向返回 (out, cache)，
反向接收上游梯度 dout 并返回 (dx, dw, db)。
朴素版（conv_*_naive）求正确，im2col 版（conv_*_fast）求速度，
main.py 会校验两者输出与梯度一致。
"""
import numpy as np


# ---------------- 全连接 / 激活 / 损失（来自 L02-L04） ----------------

def affine_forward(x, w, b):
    N = x.shape[0]
    out = x.reshape(N, -1) @ w + b
    return out, (x, w, b)


def affine_backward(dout, cache):
    x, w, b = cache
    N = x.shape[0]
    dx = (dout @ w.T).reshape(x.shape)
    dw = x.reshape(N, -1).T @ dout
    return dx, dw, np.sum(dout, axis=0)


def relu_forward(x):
    return np.maximum(0, x), x


def relu_backward(dout, cache):
    return dout * (cache > 0)


def softmax_loss_forward(scores, y):
    """数值稳定 softmax + 交叉熵；cache 直接存 dS（L02 的"预测-真值"）。"""
    N = scores.shape[0]
    s = scores - scores.max(axis=1, keepdims=True)
    P = np.exp(s)
    P /= P.sum(axis=1, keepdims=True)
    loss = -np.log(P[np.arange(N), y] + 1e-12).mean()
    dS = P.copy()
    dS[np.arange(N), y] -= 1.0
    dS /= N
    return loss, (dS,)


def softmax_loss_backward(dout, cache):
    return cache[0]          # dout 仅为接口统一；梯度已折算进 dS


# ---------------- Spatial Batch Normalization（L06） ----------------

def spatial_batchnorm_forward(x, gamma, beta, bn_params, running=None):
    """x (N,C,H,W)。训练用 batch 统计；running 传入 dict 时维护推理 EMA。"""
    N, C, H, W = x.shape
    eps = bn_params.get("eps", 1e-5)
    mu = x.mean(axis=(0, 2, 3))
    var = x.var(axis=(0, 2, 3))
    xc = x - mu[None, :, None, None]
    std = np.sqrt(var + eps)[None, :, None, None]
    xh = xc / std
    out = gamma[None, :, None, None] * xh + beta[None, :, None, None]
    if running is not None:
        m = bn_params.get("momentum", 0.9)
        running["mean"] = m * running.get("mean", mu) + (1 - m) * mu
        running["var"] = m * running.get("var", var) + (1 - m) * var
    return out, (xh, xc, std, gamma, eps)


def spatial_batchnorm_backward(dout, cache):
    """BN 使 batch 内同通道样本相互依赖（1/N 交叉项），是 A2/P2 手推难点。"""
    xh, xc, std, gamma, eps = cache
    N, C, H, W = dout.shape
    M = N * H * W
    dgamma = np.sum(dout * xh, axis=(0, 2, 3))
    dbeta = np.sum(dout, axis=(0, 2, 3))
    dxh = dout * gamma[None, :, None, None]
    std2 = std ** 2
    dvar = np.sum(dxh * xc, axis=(0, 2, 3)) * (-0.5) / (std2[0, :, 0, 0] ** 1.5)
    dmu = np.sum(-dxh / std, axis=(0, 2, 3)) + dvar * np.mean(-2.0 * xc, axis=(0, 2, 3))
    dx = dxh / std + dvar[None, :, None, None] * 2.0 * xc / M \
        + dmu[None, :, None, None] / M
    return dx, dgamma, dbeta


# ---------------- 朴素卷积（L05："make it work"） ----------------

def conv_forward_naive(x, w, b, conv_param):
    stride, pad = conv_param["stride"], conv_param["pad"]
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    xp = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)))
    H2 = (H + 2 * pad - HH) // stride + 1
    W2 = (W + 2 * pad - WW) // stride + 1
    out = np.zeros((N, F, H2, W2))
    for n in range(N):
        for f in range(F):
            for i in range(H2):
                for j in range(W2):
                    hs, ws = i * stride, j * stride
                    out[n, f, i, j] = np.sum(
                        xp[n, :, hs:hs + HH, ws:ws + WW] * w[f]) + b[f]
    return out, (x, w, b, conv_param)


def conv_backward_naive(dout, cache):
    x, w, b, conv_param = cache
    stride, pad = conv_param["stride"], conv_param["pad"]
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    _, _, H2, W2 = dout.shape
    xp = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)))
    dxp = np.zeros_like(xp)
    dw = np.zeros_like(w)
    db = dout.sum(axis=(0, 2, 3))
    for n in range(N):
        for f in range(F):
            for i in range(H2):
                for j in range(W2):
                    hs, ws = i * stride, j * stride
                    g = dout[n, f, i, j]
                    dw[f] += xp[n, :, hs:hs + HH, ws:ws + WW] * g
                    dxp[n, :, hs:hs + HH, ws:ws + WW] += w[f] * g
    dx = dxp[:, :, pad:pad + H, pad:pad + W]
    return dx, dw, db


# ---------------- im2col 快速卷积（L05："make it fast"） ----------------

def im2col_indices(x, HH, WW, stride=1, pad=0):
    """返回 cols (C·HH·WW, N·H2·W2)：每列是一个感受野拉平。

    用 stride_tricks 零拷贝开窗，再整理成 GEMM 友好的布局。
    """
    N, C, H, W = x.shape
    xp = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)))
    H2 = (H + 2 * pad - HH) // stride + 1
    W2 = (W + 2 * pad - WW) // stride + 1
    patches = np.lib.stride_tricks.as_strided(
        xp,
        shape=(N, C, H2, HH, W2, WW),
        strides=(xp.strides[0], xp.strides[1],
                 xp.strides[2] * stride, xp.strides[2],
                 xp.strides[3] * stride, xp.strides[3]),
        writeable=False)
    cols = patches.transpose(1, 3, 5, 0, 2, 4)               # (C,HH,WW,N,H2,W2)
    cols = cols.reshape(C * HH * WW, N * H2 * W2)
    meta = (N, C, H, W, H2, W2)
    return cols, meta


def conv_forward_fast(x, w, b, conv_param):
    """滑窗卷积 → 一次 GEMM：w_reshape @ cols (F,M)。"""
    cols, meta = im2col_indices(x, w.shape[2], w.shape[3],
                                conv_param["stride"], conv_param["pad"])
    N, C, H, W, H2, W2 = meta
    F = w.shape[0]
    out = w.reshape(F, -1) @ cols + b[:, None]               # (F, M)
    out = out.reshape(F, H2, W2, N).transpose(3, 0, 1, 2)    # (N,F,H2,W2)
    return out, (cols, w, meta, conv_param)


def conv_backward_fast(dout, cache):
    cols, w, meta, conv_param = cache
    N, C, H, W, H2, W2 = meta
    F, _, HH, WW = w.shape
    stride, pad = conv_param["stride"], conv_param["pad"]
    drows = dout.transpose(0, 2, 3, 1).reshape(N * H2 * W2, F)   # (M,F)
    dcols = drows.T                                             # (F,M)
    dw = (dcols @ cols.T).reshape(w.shape)
    db = dcols.sum(axis=1)
    dx_cols = w.reshape(F, -1).T @ dcols                        # (C·HH·WW, M)
    dxp = np.zeros((N, C, H + 2 * pad, W + 2 * pad))
    blocks = dx_cols.reshape(C, HH, WW, N, H2, W2)
    for i in range(H2):
        for j in range(W2):
            hs, ws = i * stride, j * stride
            # 散射回画布：感受野重叠处需要累加
            dxp[:, :, hs:hs + HH, ws:ws + WW] += \
                blocks[:, :, :, :, i, j].transpose(3, 0, 1, 2)
    dx = dxp[:, :, pad:pad + H, pad:pad + W]
    return dx, dw, db


# ---------------- 最大池化（L05，L04 的 max 门规则逐窗应用） ----------------

def max_pool_forward(x, pool_param):
    hh, ww, stride = (pool_param["pool_height"], pool_param["pool_width"],
                      pool_param["stride"])
    N, C, H, W = x.shape
    H2, W2 = (H - hh) // stride + 1, (W - ww) // stride + 1
    out = np.zeros((N, C, H2, W2))
    for n in range(N):
        for c in range(C):
            for i in range(H2):
                for j in range(W2):
                    win = x[n, c, i * stride:i * stride + hh,
                             j * stride:j * stride + ww]
                    out[n, c, i, j] = win.max()
    return out, (x, pool_param)


def max_pool_backward(dout, cache):
    x, pool_param = cache
    hh, ww, stride = (pool_param["pool_height"], pool_param["pool_width"],
                      pool_param["stride"])
    N, C, H, W = x.shape
    H2, W2 = (H - hh) // stride + 1, (W - ww) // stride + 1
    dx = np.zeros_like(x)
    for n in range(N):
        for c in range(C):
            for i in range(H2):
                for j in range(W2):
                    sl = (n, c, slice(i * stride, i * stride + hh),
                          slice(j * stride, j * stride + ww))
                    win = x[sl]
                    m = win.max()
                    mask = (win == m).astype(np.float64)
                    mask /= mask.sum()                      # 并列时平摊梯度
                    dx[sl] += mask * dout[n, c, i, j]
    return dx
