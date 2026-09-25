"""P2 · 合成图像数据（对应 L05/L06：给卷积一个"有空间结构"的任务）。

在 16x16 画布上程序化绘制三种形状（圆/方块/十字），带位置、尺度、
亮度抖动与高斯噪声——全连接学它费劲，卷积学它轻松，对比即教学。
"""
import numpy as np


def _square(g, s):
    c = g.shape[0] // 2
    h = max(2, int(round(s * g.shape[0] / 4)))
    return g[c - h:c + h, c - h:c + h]


def _disk(g, s):
    yy, xx = np.mgrid[0:g.shape[0], 0:g.shape[1]]
    c = g.shape[0] / 2 - 0.5
    r = s * g.shape[0] / 4
    return (np.sqrt((yy - c) ** 2 + (xx - c) ** 2) <= r)


def _cross(g, s):
    n = g.shape[0]
    c = n // 2
    h = max(2, int(round(s * n / 4)))
    m = np.zeros((n, n), dtype=bool)
    m[c - h:c + h, :] = True
    m[:, c - h:c + h] = True
    return m


_SHAPES = (_disk, _square, _cross)


def _draw(shape_fn, rng, size=16):
    canvas = np.zeros((size, size), dtype=np.float64)
    mask = np.zeros((size, size), dtype=bool)
    s = rng.uniform(1.5, 3.0)                      # 尺度抖动
    m = shape_fn(canvas, s)
    oy = int(rng.integers(-2, 3))                  # 位置抖动（考验卷积平移性）
    ox = int(rng.integers(-2, 3))
    if m.ndim == 2:
        mask = np.roll(np.roll(m, oy, axis=0), ox, axis=1)
    intensity = rng.uniform(0.6, 1.0)              # 亮度抖动
    canvas[mask] = intensity
    canvas += rng.normal(0, 0.08, size=(size, size))
    return np.clip(canvas, 0, 1)


def make_shape_dataset(n_per_class=100, size=16, seed=0):
    """返回 X (N,1,size,size) float64 ∈ [0,1]，y (N,) ∈ {0,1,2}。"""
    rng = np.random.default_rng(seed)
    X, y = [], []
    for c, fn in enumerate(_SHAPES):
        for _ in range(n_per_class):
            X.append(_draw(fn, rng, size))
            y.append(c)
    X = (np.stack(X)[:, None] * 1.0)
    y = np.array(y)
    p = rng.permutation(len(y))
    return X[p], y[p]


def split_data(X, y, ratios=(0.7, 0.15, 0.15), seed=1):
    rng = np.random.default_rng(seed)
    n = len(y)
    p = rng.permutation(n)
    a = int(n * ratios[0]); b = a + int(n * ratios[1])
    return [(X[p[:a]], y[p[:a]]), (X[p[a:b]], y[p[a:b]]), (X[p[b:]], y[p[b:]])]
