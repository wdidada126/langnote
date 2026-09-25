"""P3 · 迷你 ViT（对应 L08：patch 化 + Transformer 块 + 分类头；复用 L02 的 softmax 头）。

结构（post-LN 原版 Transformer）：
    tokens = patchify(X)·E + pos          （L08 1.4：图像→token）
    y1 = x + MHA(LN1(x))                  （残差：L06 思想）
    y2 = y1 + FFN(LN2(y1))                （FFN: D→4D→D，1×1 卷积的 token 版）
    scores = W_head · y2[cls] + b
反向逐段手工链式（L04 的形状对偶律），与 autograd 等价。
"""
import numpy as np

from attention import MultiHeadAttention
from layernorm import layernorm_forward, layernorm_backward
from mlp import affine_forward, affine_backward, relu_forward, relu_backward, softmax_loss_forward


def patchify(X, P=2):
    """(N,H,W) → (N, (H/P)(W/P), P·P)。要求整除。"""
    N, H, W = X.shape
    assert H % P == 0 and W % P == 0
    nH, nW = H // P, W // P
    t = X.reshape(N, nH, P, nW, P).transpose(0, 1, 3, 2, 4)
    return t.reshape(N, nH * nW, P * P)


class TinyViT:
    def __init__(self, D_in=4, Dm=24, nH=3, K=4, T=4, rng=None):
        rng = rng or np.random.default_rng(0)
        self.D_in, self.Dm, self.nH, self.K = D_in, Dm, nH, K
        self.E = rng.standard_normal((D_in, Dm)) * np.sqrt(2.0 / D_in)
        self.bE = np.zeros(Dm)
        self.cls = rng.standard_normal(Dm) * 0.02
        self.pos = rng.standard_normal((T + 1, Dm)) * 0.02     # 学习式位置嵌入（L08 1.3）
        self.mha = MultiHeadAttention(Dm, nH, rng)
        self.ln1 = {"g": np.ones(Dm), "b": np.zeros(Dm)}
        self.ln2 = {"g": np.ones(Dm), "b": np.zeros(Dm)}
        self.fw1 = rng.standard_normal((Dm, 4 * Dm)) * np.sqrt(2.0 / Dm)
        self.fb1 = np.zeros(4 * Dm)
        self.fw2 = rng.standard_normal((4 * Dm, Dm)) * np.sqrt(2.0 / (4 * Dm))
        self.fb2 = np.zeros(Dm)
        self.hw = rng.standard_normal((Dm, K)) * 0.01
        self.hb = np.zeros(K)

    # ---------------- 前向 ----------------
    def forward(self, X, y=None):
        N = X.shape[0]
        tok = patchify(X, 2) if X.ndim == 3 else X
        T = tok.shape[1]
        M = N * (T + 1)
        x0 = (tok.reshape(-1, self.D_in) @ self.E + self.bE).reshape(N, T, self.Dm)
        x0 = np.concatenate([np.tile(self.cls, (N, 1, 1)), x0], axis=1) + self.pos[None]
        h1, c1 = layernorm_forward(x0, self.ln1["g"], self.ln1["b"])
        a, ca = self.mha.forward(h1)
        y1 = x0 + a
        h2, c2 = layernorm_forward(y1, self.ln2["g"], self.ln2["b"])
        z1, cf1 = affine_forward(h2.reshape(M, -1), self.fw1, self.fb1)
        r1, cr1 = relu_forward(z1)
        f, cf2 = affine_forward(r1, self.fw2, self.fb2)
        y2 = y1 + f.reshape(N, T + 1, -1)
        cls_out = y2[:, 0]
        scores, ch = affine_forward(cls_out, self.hw, self.hb)
        self.cache = (tok, x0, c1, ca, h1, y1, c2, cf1, cr1, cf2, ch, cls_out, N, T, M)
        if y is None:
            return scores
        loss, dS = softmax_loss_forward(scores, y)
        self.dS = dS
        return loss

    # ---------------- 反向（残差分支的梯度在这里合并）----------------
    def backward(self):
        tok, x0, c1, ca, h1, y1, c2, cf1, cr1, cf2, ch, cls_out, N, T, M = self.cache
        g = {}
        # 头 + cls 散射
        d_cls, g["hw"], g["hb"] = affine_backward(self.dS, ch)
        d_y2 = np.zeros((N, T + 1, self.Dm))
        d_y2[:, 0] = d_cls
        # FFN 分支：f = y2 - y1 贡献 d_y2；y1 直通分量后加
        d_f = d_y2.reshape(M, -1)
        dr1, g["fw2"], g["fb2"] = affine_backward(d_f, cf2)
        dh2 = relu_backward(dr1, cr1)
        dz, g["fw1"], g["fb1"] = affine_backward(dh2, cf1)
        dh2 = dz.reshape(N, T + 1, self.Dm)
        # LN2 → y1 合并
        dy1_ln2, g["ln2g"], g["ln2b"] = layernorm_backward(dh2, c2)
        d_y1 = d_y2 + dy1_ln2
        # MHA 分支（d_a = d_y1）与 LN1 → x0 合并
        dh1, dmha = self.mha.backward(d_y1, ca)
        for k, v in dmha.items():
            g["mha_" + k] = v
        dx0_ln1, g["ln1g"], g["ln1b"] = layernorm_backward(dh1, c1)
        d_x0 = d_y1 + dx0_ln1
        # patch 嵌入与位置
        g["pos"] = d_x0.sum(axis=0)
        g["cls"] = d_x0[:, 0].sum(axis=0)
        d_tok = d_x0[:, 1:].reshape(-1, self.Dm)
        g["bE"] = d_tok.sum(axis=0)
        g["E"] = tok.reshape(-1, self.D_in).T @ d_tok
        self.grads = g

    # ---------------- 一步 SGD+momentum（L03） ----------------
    def step(self, lr=0.05, momentum=0.9):
        if not hasattr(self, "vel"):
            self.vel = {}
        def upd(obj, name, grad, key):
            target = obj[name] if isinstance(obj, dict) else getattr(obj, name)
            v = self.vel.setdefault(key, np.zeros_like(target))
            v *= momentum
            v -= lr * grad
            target += v
        for name in ("E", "bE", "cls", "pos"):
            upd(self.__dict__, name, self.grads[name], name)
        for nm in ("ln1", "ln2"):
            upd(self.__dict__[nm], "g", self.grads[nm + "g"], nm + "g")
            upd(self.__dict__[nm], "b", self.grads[nm + "b"], nm + "b")
        for k in ("Wq", "Wk", "Wv", "Wo"):
            upd(self.mha.__dict__, k, self.grads["mha_" + k], "mha" + k)
        for nm in ("fw1", "fb1", "fw2", "fb2", "hw", "hb"):
            upd(self.__dict__, nm, self.grads[nm], nm)

    def accuracy(self, X, y):
        s = self.forward(X)
        return float(np.mean(np.argmax(s, axis=1) == y))
