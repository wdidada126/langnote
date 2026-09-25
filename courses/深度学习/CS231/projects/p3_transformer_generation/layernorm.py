"""P3 · Layer Normalization（对应 L06 BN 的逐样本版 + L08 Transformer 标配）。

与 BN 的区别：BN 沿 batch 对每通道归一（train/eval 行为不同），
LN 沿特征维对每个样本自己归一（推断无状态切换）。
"""
import numpy as np


def layernorm_forward(x, gamma, beta, eps=1e-5):
    """x (N,T,D) 或 (N,D)。"""
    mu = x.mean(axis=-1, keepdims=True)
    xc = x - mu
    var = (xc ** 2).mean(axis=-1, keepdims=True)
    std = np.sqrt(var + eps)
    xh = xc / std
    out = gamma * xh + beta
    return out, (xc, std, gamma, eps)


def layernorm_backward(dout, cache):
    xc, std, gamma, eps = cache
    D = dout.shape[-1]
    dxh = dout * gamma
    dvar = (dxh * xc * (-0.5) / std ** 3).sum(axis=-1, keepdims=True)
    dmu = (-dxh / std).sum(axis=-1, keepdims=True) + dvar * (-2.0 * xc / D).sum(axis=-1, keepdims=True)
    dx = dxh / std + dvar * 2.0 * xc / D + dmu / D
    dgamma = np.sum(dout * xc / std, axis=tuple(range(dout.ndim - 1)))
    dbeta = np.sum(dout, axis=tuple(range(dout.ndim - 1)))
    return dx, dgamma, dbeta
