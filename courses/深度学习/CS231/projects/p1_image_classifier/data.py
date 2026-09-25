"""P1 · 合成数据与预处理（对应 L01/L02：数据划分、零中心化、归一化）。

只用 numpy 与标准库。高斯团簇（blobs）模拟"图像像素空间中的类别簇"，
用于 kNN / 线性 SVM / softmax 分类器的完整管线实验。
"""
import numpy as np


def make_blobs(n_samples=1000, n_features=192, centers=4,
               cluster_std=1.2, seed=0):
    """生成高斯团簇数据。n_features 取 8*8*3=192，即 8x8x3 小图拉平。"""
    rng = np.random.default_rng(seed)
    per = n_samples // centers
    X = np.empty((per * centers, n_features), dtype=np.float64)
    y = np.empty(per * centers, dtype=np.int64)
    # 类别中心：在 [-4,4]^D 里撒点，簇间有重叠也有分离
    centroids = rng.uniform(-4.0, 4.0, size=(centers, n_features))
    for c in range(centers):
        idx = slice(c * per, (c + 1) * per)
        X[idx] = centroids[c] + rng.normal(0, cluster_std, size=(per, n_features))
        y[idx] = c
    perm = rng.permutation(len(y))
    return X[perm], y[perm]


def split_data(X, y, ratios=(0.6, 0.2, 0.2), seed=0):
    """train/val/test 三分（L02 纪律：超参数只看 val，test 只在最后报一次）。"""
    rng = np.random.default_rng(seed)
    n = len(y)
    p = rng.permutation(n)
    n_tr = int(n * ratios[0])
    n_va = int(n * ratios[1])
    return [(X[p[a:b]], y[p[a:b]])
            for a, b in [(0, n_tr), (n_tr, n_tr + n_va), (n_tr + n_va, n)]]


def preprocess(X_train, *others, scale=False):
    """按训练集零中心化（可选再归一化到单位方差），变换应用于所有数据集。"""
    mu = X_train.mean(axis=0)
    out = [X_train - mu] + [X - mu for X in others]
    if scale:
        sd = X_train.std(axis=0) + 1e-12
        out = [X / sd for X in out]
    return out


def add_bias_column(X):
    """L02 技巧：增广一列 1，把偏置 b 并入权重 W 一起训练。"""
    return np.hstack([X, np.ones((X.shape[0], 1))])


def accuracy(scores_or_pred, y, is_pred=False):
    pred = scores_or_pred if is_pred else np.argmax(scores_or_pred, axis=1)
    return float(np.mean(pred == y))
