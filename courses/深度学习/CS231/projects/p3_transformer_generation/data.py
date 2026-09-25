"""P3 · 合成数据（对应 L08/L13）。

1) 四象限斑点图：8x8 灰度图，光斑落在 4 个象限之一 → ViT 用注意力"看位置"。
2) 2D 三高斯混合：GAN/VAE 的玩具 p_data。
"""
import numpy as np


def make_quad_images(n_per_class=50, size=8, blur=0.9, seed=0):
    rng = np.random.default_rng(seed)
    X, y = [], []
    for c in range(4):
        for _ in range(n_per_class):
            img = np.zeros((size, size))
            # 类别 c 决定光斑中心所在象限，象限内再抖动
            cy = size / 4 if c % 2 == 0 else 3 * size / 4
            cx = size / 4 if c < 2 else 3 * size / 4
            cy += rng.uniform(-1, 1); cx += rng.uniform(-1, 1)
            yy, xx = np.mgrid[0:size, 0:size]
            d2 = (yy - cy) ** 2 + (xx - cx) ** 2
            img = np.exp(-d2 / (2 * blur ** 2))
            img += rng.normal(0, 0.05, img.shape)
            X.append(img)
            y.append(c)
    return np.stack(X)[:, None], np.array(y)


def make_two_d_data(n=400, mode="gauss", seed=0):
    rng = np.random.default_rng(seed)
    if mode == "gauss":
        centers = np.array([[2.0, 0.0], [-1.0, 1.7], [-1.0, -1.7]])
        k = rng.integers(0, 3, size=n)
        X = centers[k] + rng.normal(0, 0.4, size=(n, 2))
        return X.astype(np.float64), k
    raise ValueError(mode)


def split_data(X, y, ratios=(0.8, 0.2), seed=1):
    rng = np.random.default_rng(seed)
    p = rng.permutation(len(y))
    a = int(len(y) * ratios[0])
    return (X[p[:a]], y[p[:a]]), (X[p[a:]], y[p[a:]])
