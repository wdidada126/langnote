"""L09 §1.2 偏差-方差分解的蒙特卡洛验证（把恒等式画成数）。

E_D[(h_D(x)−y)²] = σ² + Bias²(x) + Var(x)，
在固定测试点上用大量独立训练集估计三项，按 m 与 deg 扫描验证。
唯一第三方依赖：numpy。运行：python bv_decomp.py
"""
import numpy as np
from poly_ridge import true_f, gen, vander, ridge_fit

X_TE = np.linspace(-3, 3, 201)


def decompose(m, deg, n_rep=200, noise=0.3, lam=0.0):
    preds = np.zeros((n_rep, len(X_TE)))
    for r in range(n_rep):
        xtr, ytr = gen(m, seed=1000 + r, noise=noise)
        th = ridge_fit(vander(xtr, deg), ytr, lam)
        preds[r] = vander(X_TE, deg) @ th
    f = true_f(X_TE)
    mean_pred = preds.mean(0)
    bias2 = np.mean((mean_pred - f) ** 2)
    var = np.mean(preds.var(0))
    sigma2 = noise ** 2
    # 逐点期望恒等式核对：E_D E[(h−y)²] = σ² + (E h − f)² + Var(h)
    total = bias2 + var + sigma2
    return total, bias2, var, sigma2


def main():
    print("deg=1（线性，欠拟合）：Bias² 主导，Var 很小")
    for m in [20, 200]:
        t, b, v, s = decompose(m, 1)
        print(f"  m={m:>4}  total={t:.4f}  bias²={b:.4f}  var={v:.4f}  noise={s:.4f}")
    print("deg=12（高次，过拟合）：Var 随 m 缩小，Bias 几乎不变")
    for m in [10, 30, 100, 400]:
        t, b, v, s = decompose(m, 12)
        print(f"  m={m:>4}  total={t:.4f}  bias²={b:.4f}  var={v:.4f}  noise={s:.4f}")
    print("λ=1 正则化 deg=12（容量受限后 var 回落，bias 微升）")
    for lam in [0.0, 1e-3, 1.0, 100.0]:
        t, b, v, s = decompose(30, 12, lam=lam)
        print(f"  λ={lam:<6g} total={t:.4f}  bias²={b:.4f}  var={v:.4f}")
    print("→ 与 poly_ridge.py 的 holdout 曲线互证：train/val gap≈var 症状，双高≈bias。")


if __name__ == "__main__":
    main()
