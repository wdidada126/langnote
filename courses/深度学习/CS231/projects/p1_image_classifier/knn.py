"""P1 · kNN 基线（对应 L02：数据驱动决策、超参数只在验证集调）。"""
import numpy as np


def pairwise_l2(X, Y):
    """||x-y||^2 = ||x||^2 + ||y||^2 - 2x·y  的向量化展开（A1 名场面）。"""
    return np.maximum(
        np.sum(X ** 2, axis=1)[:, None]
        + np.sum(Y ** 2, axis=1)[None, :]
        - 2.0 * X @ Y.T, 0.0)


def pairwise_l1(X, Y):
    return np.abs(X[:, None, :] - Y[None, :, :]).sum(axis=2)


class KNearestNeighbor:
    """无训练、纯记忆；预测代价 O(N·D)。高维像素空间中语义距离失真——
    这正是引出线性分类器的动机。"""

    def __init__(self):
        self.X = None
        self.y = None

    def fit(self, X, y):
        self.X, self.y = X, y

    def predict(self, Xte, k=5, metric="l2"):
        D = pairwise_l2(Xte, self.X) if metric == "l2" else pairwise_l1(Xte, self.X)
        idx = np.argsort(D, axis=1)[:, :k]              # 每行最近的 k 个训练点
        lab = self.y[idx]
        # 多数投票：每类计数取 argmax
        votes = np.apply_along_axis(
            lambda r: np.bincount(r, minlength=int(self.y.max()) + 1).argmax(),
            axis=1, arr=lab)
        return votes

    def cross_validate(self, Xval, yval, k_range, metrics=("l2", "l1")):
        """小范围网格：在验证集上选 k 与距离度量（test 绝不上场）。"""
        results, best = {}, (-1, None)
        for m in metrics:
            for k in k_range:
                acc = float(np.mean(self.predict(Xval, k=k, metric=m) == yval))
                results[(m, k)] = acc
                if acc > best[0]:
                    best = (acc, (m, k))
        return best[1], best[0], results
