"""P1 · softmax 线性分类器（对应 L02：多类逻辑回归；L03：SGD+L2）。

梯度推导（务必手推一遍再读代码）：
    s = X·W        (N,K)   scores
    P = softmax(s) (N,K)
    L = mean_i(-log P[i, y_i]) + λ·reg(W)
    dL/ds_i = (P_i - onehot_i) / N        ← 预测减真值，全课最简洁梯度
"""
import numpy as np


def softmax_loss(scores, y, W=None, reg=0.0):
    """scores: (N,K)。返回 (loss, dScores)。数值稳定：先减行最大值。"""
    N = scores.shape[0]
    s = scores - scores.max(axis=1, keepdims=True)
    P = np.exp(s)
    P /= P.sum(axis=1, keepdims=True)
    loss = -np.log(P[np.arange(N), y] + 1e-12).mean()
    if W is not None:
        loss += reg * np.sum(W * W)
    dS = P.copy()
    dS[np.arange(N), y] -= 1.0
    dS /= N
    return loss, dS


def softmax_loss_only(W, X, y, l2=0.0):
    """纯函数版损失（梯度检查专用）：scores=X@W。"""
    N = X.shape[0]
    s = X @ W
    s = s - s.max(axis=1, keepdims=True)
    P = np.exp(s)
    P /= P.sum(axis=1, keepdims=True)
    return float(-np.log(P[np.arange(N), y] + 1e-12).mean() + l2 * np.sum(W * W))


class LinearSoftmax:
    def __init__(self, input_dim, num_classes, l2=1e-4):
        self.W = np.random.default_rng(0).standard_normal(
            (input_dim, num_classes)) * 1e-3
        self.l2 = l2

    def loss_grad(self, X, y):
        scores = X @ self.W
        loss, dS = softmax_loss(scores, y, self.W, self.l2)
        dW = X.T @ dS + 2.0 * self.l2 * self.W          # 链式：dS→dW
        return loss, dW

    def fit(self, X, y, lr=0.2, epochs=200, batch_size=64, momentum=0.9,
            val=None, verbose_every=50):
        N = X.shape[0]
        rng = np.random.default_rng(1)
        v = np.zeros_like(self.W)
        for it in range(epochs):
            idx = rng.integers(0, N, size=batch_size)   # 小批量 SGD（L03）
            _, g = self.loss_grad(X[idx], y[idx])
            v = momentum * v - lr * g
            self.W += v
            if verbose_every and (it + 1) % verbose_every == 0:
                msg = f"iter {it+1:4d} loss {self.loss_grad(X[:400], y[:400])[0]:.4f}"
                if val is not None:
                    msg += f" val acc {self.score(*val):.4f}"
                print(msg)

    def score(self, X, y):
        pred = np.argmax(X @ self.W, axis=1)
        return float(np.mean(pred == y))
