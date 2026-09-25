"""P1 · 线性 SVM（hinge 多分类）（对应 L02/L03）。

    L_i = Σ_{j≠y_i} max(0, s_j - s_{y_i} + Δ) / N + λ·||W||²
不可微但有次梯度：违规类贡献 ±1，满足间隔的类贡献 0（稀疏梯度）。
"""
import numpy as np


class LinearSVM:
    def __init__(self, input_dim, num_classes, l2=1e-4, margin=1.0):
        rng = np.random.default_rng(0)
        self.W = rng.standard_normal((input_dim, num_classes)) * 1e-3
        self.l2 = l2
        self.margin = margin

    # ---- 循环版（"make it work"：先对，再快）----
    def loss_grad_loop(self, X, y):
        N = X.shape[0]
        S = X @ self.W
        dW = np.zeros_like(self.W)
        loss = 0.0
        for i in range(N):
            s = S[i]
            good = s[y[i]]
            mask = s - good[:, None] + self.margin      # (K,) 相对正确类的违规量
            mask[y[i]] = -np.inf
            bad = mask > 0
            loss += mask[bad].sum()
            ds = np.where(bad, 1.0, 0.0)
            ds[y[i]] = -ds.sum()
            dW += np.outer(X[i], ds)
        loss /= N
        loss += self.l2 * np.sum(self.W * self.W)
        return loss, dW / N + 2.0 * self.l2 * self.W

    # ---- 向量化版（"make it right+fast"：与循环版结果必须一致）----
    def loss_grad(self, X, y):
        N = X.shape[0]
        S = X @ self.W
        good = S[np.arange(N), y][:, None]
        delta = S - good + self.margin
        delta[np.arange(N), y] = -np.inf                 # 正确类不参与
        P = (delta > 0).astype(np.float64)               # 违规计数
        delta_pos = np.where(delta > 0, delta, 0.0)
        loss = delta_pos.sum() / N + self.l2 * np.sum(self.W * self.W)
        P[np.arange(N), y] = -P.sum(axis=1)              # 正确列吸收负梯度
        dW = X.T @ (P / N) + 2.0 * self.l2 * self.W
        return loss, dW

    def fit(self, X, y, lr=5e-3, epochs=200, batch_size=64, val=None,
            verbose_every=50):
        N = X.shape[0]
        rng = np.random.default_rng(1)
        for it in range(epochs):
            idx = rng.integers(0, N, size=batch_size)
            _, g = self.loss_grad(X[idx], y[idx])
            self.W -= lr * g
            if verbose_every and (it + 1) % verbose_every == 0:
                msg = f"iter {it+1:4d} loss {self.loss_grad(X[:400], y[:400])[0]:.4f}"
                if val is not None:
                    msg += f" val acc {self.score(*val):.4f}"
                print(msg)

    def score(self, X, y):
        return float(np.mean(np.argmax(X @ self.W, axis=1) == y))
