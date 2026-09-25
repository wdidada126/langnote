"""P3 · 通用 MLP 积木（对应 L02-L04；供 attention/vit/gan/vae 共用）。"""
import numpy as np


def affine_forward(x, w, b):
    """x (N,D) @ w (D,K) + b。"""
    return x @ w + b, (x, w, b)


def affine_backward(dout, cache):
    x, w, b = cache
    return dout @ w.T, x.T @ dout, dout.sum(axis=0)


def relu_forward(x):
    return np.maximum(0, x), x


def relu_backward(dout, cache):
    return dout * (cache > 0)


def softmax_forward(scores):
    s = scores - scores.max(axis=1, keepdims=True)
    P = np.exp(s)
    P /= P.sum(axis=1, keepdims=True)
    return P


def softmax_loss_forward(scores, y):
    """(loss, dscores)——L02 的"预测-真值"。"""
    N = scores.shape[0]
    P = softmax_forward(scores)
    loss = -np.log(P[np.arange(N), y] + 1e-12).mean()
    dS = P.copy()
    dS[np.arange(N), y] -= 1.0
    return loss, dS / N


def mse_loss_forward(pred, target):
    diff = pred - target
    loss = 0.5 * np.mean(diff ** 2)
    return loss, diff / diff.shape[0]


def he_init(shape, rng):
    return rng.standard_normal(shape) * np.sqrt(2.0 / shape[0])


class MLP:
    """[affine → relu]×depth → affine。forward 返回 (out, cache)，backward 返回 (dx, params)。"""

    def __init__(self, dims, rng):
        self.params = []
        for i in range(len(dims) - 1):
            self.params.append({"w": he_init((dims[i], dims[i + 1]), rng),
                                "b": np.zeros(dims[i + 1])})

    def forward(self, x):
        cache = []
        for i, p in enumerate(self.params):
            x, c = affine_forward(x, p["w"], p["b"])
            cache.append([c])
            if i < len(self.params) - 1:
                x, r = relu_forward(x)
                cache[-1].append(r)
        return x, cache

    def backward(self, dout, cache):
        grads = []
        for i in reversed(range(len(self.params))):
            c = cache[i][0]
            r = cache[i][1] if len(cache[i]) > 1 else None
            if r is not None:
                dout = relu_backward(dout, r)
            dx, dw, db = affine_backward(dout, c)
            grads.append((dw, db))
            dout = dx
        return dout, grads[::-1]

    def update(self, grads, lr, momentum=0.9, vel=None):
        """vel 由调用方持有（动量缓冲跨步复用），key 用 (层号, 参数名)。"""
        if vel is None:
            vel = {}
            self._vel = vel
        for li, (p, (dw, db)) in enumerate(zip(self.params, grads)):
            for k, g in (("w", dw), ("b", db)):
                v = vel.setdefault((li, k), np.zeros_like(p[k]))
                v *= momentum
                v -= lr * g
                p[k] += v
