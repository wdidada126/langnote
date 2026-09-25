"""P2 · 梯度与等价性检查（对应 L05/L06：卷积与 BN 的"make it right"）。"""
import numpy as np
import layers as L


def rel_err(a, b):
    return float(np.abs(a - b).max() / (np.abs(a).max() + np.abs(b).max() + 1e-12))


def check_conv_equivalence(N=4, C=3, H=8, W=8, F=5, seed=0):
    """naive 与 fast 的前向输出、两条反向梯度必须一致。"""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((N, C, H, W))
    w = rng.standard_normal((F, C, 3, 3)) * 0.1
    b = rng.standard_normal(F) * 0.1
    dout = rng.standard_normal((N, F, H - 2, W - 2))      # stride=1,pad=1
    cp = {"stride": 1, "pad": 1}
    o1, c1 = L.conv_forward_naive(x, w, b, cp)
    o2, c2 = L.conv_forward_fast(x, w, b, cp)
    dx1, dw1, db1 = L.conv_backward_naive(dout, c1)
    dx2, dw2, db2 = L.conv_backward_fast(dout, c2)
    return {
        "fwd": rel_err(o1, o2),
        "dx": rel_err(dx1, dx2),
        "dw": rel_err(dw1, dw2),
        "db": rel_err(db1, db2),
    }


def numeric_grad(loss_fn, x, h=1e-6, max_elems=8, seed=3):
    rng = np.random.default_rng(seed)
    out = {}
    shape = x.shape
    for _ in range(max_elems):
        ix = tuple(int(rng.integers(0, s)) for s in shape)
        old = x[ix]
        x[ix] = old + h
        fp = loss_fn(x)
        x[ix] = old - h
        fm = loss_fn(x)
        x[ix] = old
        out[ix] = (fp - fm) / (2.0 * h)
    return out


def grad_check_model(model, X, y, sample_params=("w1", "b1", "w2", "g1"),
                     n=4, seed=5):
    """端到端：模型总损失对少量参数元素的数值检查（A2 同款流程）。"""
    rng = np.random.default_rng(seed)
    model.mode = "train"
    worst_all = 0.0
    for name in sample_params:
        p = model.params[name]
        idxs = [tuple(rng.integers(0, s) for s in p.shape) for _ in range(n)]
        model.forward(X, y)
        model.backward()
        worst = 0.0
        for ix in idxs:
            old = p[ix]
            p[ix] = old + 1e-5
            lp = model.forward(X, y)
            p[ix] = old - 1e-5
            lm = model.forward(X, y)
            p[ix] = old
            num = (lp - lm) / 2e-5
            rel = abs(num - model.grads[name][ix]) / max(1e-8, abs(num) + abs(model.grads[name][ix]))
            worst = max(worst, rel)
        worst_all = max(worst_all, worst)
        print(f"[model-grad] {name:6s} max rel err = {worst:.2e}  "
              f"{'OK ' if worst < 1e-4 else 'FAIL'}")
    return worst_all
