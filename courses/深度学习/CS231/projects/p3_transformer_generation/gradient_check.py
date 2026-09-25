"""P3 · 梯度检查（对应 L03/L08：注意力与 LayerNorm 的"make it right"）。

约定：f(x) 返回标量；g(x) 返回与 x 同形的解析梯度（两者必须对应同一线性泛函，
例如 f = Σ 0.01·out、g = dout=0.01·ones 反传——见 main.py 的闭包写法）。
"""
import numpy as np


def grad_check_callable(label, f, x, g, h=1e-6, n=10, tol=1e-5, seed=3):
    rng = np.random.default_rng(seed)
    ana = g(x.copy())
    worst = 0.0
    shape = x.shape
    for _ in range(n):
        ix = tuple(int(rng.integers(0, s)) for s in shape)
        old = x[ix]
        x[ix] = old + h
        fp = f(x.copy())
        x[ix] = old - h
        fm = f(x.copy())
        x[ix] = old
        num = (fp - fm) / (2.0 * h)
        rel = abs(num - ana[ix]) / max(1e-8, abs(num) + abs(ana[ix]))
        worst = max(worst, rel)
    print(f"[grad-check] {label:22s} max rel err = {worst:.2e}  "
          f"{'OK' if worst < tol else 'FAIL'}")
    return worst
