"""公共工具：合成数据与 ASCII 绘图（无 matplotlib，依赖仅 numpy）。

CS229 L01-L03 配套。唯一第三方依赖：numpy。
"""
import numpy as np


def make_regression(n=200, d=3, seed=0, ill_conditioned=False):
    """y = X w* + N(0, 0.1)。ill_conditioned=True 时特征尺度指数衰减，
    用于演示条件数对 GD 收敛速度的影响（L02）。"""
    rng = np.random.default_rng(seed)
    X = rng.normal(0.0, 1.0, size=(n, d))
    w = rng.normal(0.0, 1.0, size=d)
    if ill_conditioned:
        scales = np.logspace(0, -3, d)          # 特征方差跨 3 个数量级
        X = X * scales
        w = w / scales                          # 保持目标值量级
    y = X @ w + rng.normal(0.0, 0.1, size=n)
    return X, y


def make_blobs_2d(n=200, seed=0, anisotropic=False):
    """两类二维高斯 blob，返回带偏置列的 X 与 y∈{0,1}。
    anisotropic=True 时协方差旋转/拉长——GDA 假设被破坏的实验组（L05/p03 也用类似思路）。"""
    rng = np.random.default_rng(seed)
    mu0, mu1 = np.array([-1.5, -1.0]), np.array([1.5, 1.0])
    if anisotropic:
        ang = np.pi / 4
        R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        cov0 = R @ np.diag([1.0, 0.05]) @ R.T
        cov1 = R @ np.diag([0.05, 1.0]) @ R.T
    else:
        cov0 = cov1 = np.eye(2)
    X0 = rng.multivariate_normal(mu0, cov0, n // 2)
    X1 = rng.multivariate_normal(mu1, cov1, n // 2)
    X = np.vstack([X0, X1])
    y = np.concatenate([np.zeros(n // 2, int), np.ones(n // 2, int)])
    perm = rng.permutation(n)
    return X[perm], y[perm]


def add_bias(X):
    """L01 的 x0=1 技巧。"""
    return np.hstack([np.ones((X.shape[0], 1)), X])


def standardize(X, mean=None, std=None):
    if mean is None:
        mean, std = X.mean(0), X.std(0) + 1e-12
    return (X - mean) / std, mean, std


def spark(values, width=60, title=""):
    """ASCII 折线：把一维序列缩放到 width 列高 9 行，用于在终端看收敛曲线。"""
    v = np.asarray(values, float)
    if v.size == 1:
        v = np.repeat(v, 2)
    lo, hi = v.min(), v.max()
    if hi - lo < 1e-15:
        hi = lo + 1e-15
    h = 9
    grid = np.full((h, width), " ", dtype="<U1")
    xs = np.linspace(0, width - 1, v.size).round().astype(int)
    ys = ((v - lo) / (hi - lo) * (h - 1)).round().astype(int)
    for x, y in zip(xs, ys):
        grid[h - 1 - y, x] = "*"
    lines = [f"{title}  [{lo:.3e} .. {hi:.3e}]"]
    lines += ["".join(row) for row in grid]
    return "\n".join(lines)


def table(rows, header):
    out = ["  ".join(f"{c:>12}" for c in header)]
    out += ["  ".join(f"{str(c):>12}" for c in r) for r in rows]
    return "\n".join(out)
