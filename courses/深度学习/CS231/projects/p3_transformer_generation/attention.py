"""P3 · 缩放点积注意力与多头注意力（对应 L08；A3/Transformer 手写练习的 numpy 版）。

形状约定：x (N,T,D)；头数 nH，dh = D/nH。
反向全部由 L04 链式法则 + softmax 的 (P - onehot) 结构推出：
    dP = dout @ Vᵀ
    dS = P ⊙ (dP - rowsum(dP ⊙ P)) · scale
    dQ = dS @ K ,  dK = dSᵀ @ Q ,  dV = Pᵀ @ dout
"""
import numpy as np


def softmax_rows(s):
    e = np.exp(s - s.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def attention_forward(q, k, v, mask=None):
    """q,k,v: (N,nH,T,dh)。返回 out (N,nH,T,dh), cache。"""
    scale = 1.0 / np.sqrt(q.shape[-1])
    s = np.einsum("nhtd,nhsd->nhts", q, k) * scale
    if mask is not None:
        s = s + mask * (-1e9)                     # 因果掩码：禁止看未来
    p = softmax_rows(s)
    out = np.einsum("nhts,nhsd->nhtd", p, v)
    return out, (q, k, v, p, scale)


def attention_backward(dout, cache):
    q, k, v, p, scale = cache
    dp = np.einsum("nhtd,nhsd->nhts", dout, v)
    # softmax 的反向：dS = P(dP - Σ P·dP)
    ds = p * (dp - (p * dp).sum(axis=-1, keepdims=True)) * scale
    dq = np.einsum("nhts,nhsd->nhtd", ds, k)
    dk = np.einsum("nhts,nhtd->nhsd", ds, q)
    dv = np.einsum("nhts,nhtd->nhsd", p, dout)
    return dq, dk, dv


class MultiHeadAttention:
    """x → Q,K,V 投影 → 多头注意力 → 输出投影（带残差的用法在 vit.py）。"""

    def __init__(self, D, nH, rng):
        self.D, self.nH, self.dh = D, nH, D // nH
        assert D % nH == 0
        self.Wq = rng.standard_normal((D, D)) * np.sqrt(2.0 / D)
        self.Wk = rng.standard_normal((D, D)) * np.sqrt(2.0 / D)
        self.Wv = rng.standard_normal((D, D)) * np.sqrt(2.0 / D)
        self.Wo = rng.standard_normal((D, D)) * np.sqrt(2.0 / D)

    def _heads(self, t):
        N, T, _ = t.shape
        return t.reshape(N, T, self.nH, self.dh).transpose(0, 2, 1, 3)

    def _merge(self, t):
        N, nH, T, dh = t.shape
        return t.transpose(0, 2, 1, 3).reshape(N, T, nH * dh)

    def forward(self, x, mask=None):
        N = x.shape[0]
        q = self._heads(x @ self.Wq)
        k = self._heads(x @ self.Wk)
        v = self._heads(x @ self.Wv)
        out, c = attention_forward(q, k, v, mask)
        o = self._merge(out) @ self.Wo
        return o, (x, q, k, v, c, out, o)

    def backward(self, dout, cache):
        x, q, k, v, c, out, o = cache
        dWo = self._merge(out).reshape(-1, self.D).T @ dout.reshape(-1, self.D)
        d_m = dout @ self.Wo.T
        d_out = d_m.reshape(x.shape[0], x.shape[1], self.nH, self.dh).transpose(0, 2, 1, 3)
        dq, dk, dv = attention_backward(d_out, (q, k, v) + c[3:])
        fx = x.reshape(-1, self.D)
        dWq = fx.T @ self._merge(dq).reshape(-1, self.D)
        dWk = fx.T @ self._merge(dk).reshape(-1, self.D)
        dWv = fx.T @ self._merge(dv).reshape(-1, self.D)
        dx = (self._merge(dq) @ self.Wq.T + self._merge(dk) @ self.Wk.T
              + self._merge(dv) @ self.Wv.T)
        return dx, dict(Wq=dWq, Wk=dWk, Wv=dWv, Wo=dWo)
