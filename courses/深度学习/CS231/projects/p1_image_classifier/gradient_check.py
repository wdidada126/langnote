"""P1 · 梯度检查（对应 L03："make it right"，中心差商）。

思路：任意"接受 W、返回标量损失"的对象都能被检查——
用闭包把模型在指定 W 上的损失/解析梯度取出来，逐元素比较数值梯度。
注意：hinge 损失不可微，恰在间隔边界上的点会产生抖动；
小批量+正则项使差商与解析值完全一致（本实现用全量数据检查）。
"""
import numpy as np


def eval_numerical_gradient(loss_at, W, h=1e-6, max_elems=20, seed=3):
    """抽样版数值梯度：返回 {multi_index: 数值梯度}。"""
    rng = np.random.default_rng(seed)
    D, K = W.shape
    out = {}
    for (i, j) in [(int(rng.integers(0, D)), int(rng.integers(0, K)))
                   for _ in range(max_elems)]:
        old = W[i, j]
        W[i, j] = old + h
        fp = loss_at(W)
        W[i, j] = old - h
        fm = loss_at(W)
        W[i, j] = old
        out[(i, j)] = (fp - fm) / (2.0 * h)
    return out


def gradient_check(model, X, y, sample=200, h=1e-6, label=""):
    """对带 .W 且实现 .loss_grad(X,y)->(loss,dW) 的模型做抽样检查。

    返回最大相对误差；softmax 应在 1e-6 以下，SVM 次梯度在
    远离间隔边界时同样成立，这里对两者都打印结果供对照。
    """
    Xc, yc = X[:sample], y[:sample]
    _, dW = model.loss_grad(Xc, yc)

    def loss_at(W):
        old = model.W
        model.W = W
        try:
            l, _ = model.loss_grad(Xc, yc)
        finally:
            model.W = old
        return l

    num = eval_numerical_gradient(loss_at, model.W, h=h, max_elems=20)
    worst = 0.0
    for (i, j), g in num.items():
        rel = abs(g - dW[i, j]) / max(1e-8, abs(g) + abs(dW[i, j]))
        worst = max(worst, rel)
    print(f"[grad-check] {label:26s} max rel err = {worst:.3e}  "
          f"{'OK' if worst < 1e-6 else 'CHECK'}")
    return worst
