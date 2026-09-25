"""L09 正则化与偏差-方差：多项式拟合 + 岭回归的三类经典曲线（终端表格版）。

知识点：假设空间容量（多项式阶数）与 λ 如何分别驱动 bias/variance、
训练/验证误差随样本量与正则强度的走势、正则不惩罚截距的惯例。
唯一第三方依赖：numpy。运行：python poly_ridge.py
"""
import numpy as np


def true_f(x):
    return np.sin(1.5 * x)


def gen(m, seed, noise=0.3, x_range=(-3.0, 3.0)):
    rng = np.random.default_rng(seed)
    x = rng.uniform(*x_range, m)
    y = true_f(x) + rng.normal(0, noise, m)
    return x, y


def vander(x, deg):
    return np.vander(x, N=deg + 1, increasing=True)   # 第0列=1：截距


def ridge_fit(Xtr, ytr, lam, fit_intercept_unpenalized=True):
    """min ‖Xθ−y‖² + lam‖θ_非截距‖²；lam=0 即最小二乘。"""
    d = Xtr.shape[1]
    P = np.eye(d) * lam
    if fit_intercept_unpenalized:
        P[0, 0] = 0.0                          # L02 陷阱 4：不惩罚 θ0
    return np.linalg.solve(Xtr.T @ Xtr + P, Xtr.T @ ytr)


def rmse(X, y, theta):
    return float(np.sqrt(np.mean((X @ theta - y) ** 2)))


def holdout(deg, m_tr=30, m_va=500, seed=10, lam=0.0):
    xtr, ytr = gen(m_tr, seed)
    xva, yva = gen(m_va, seed + 999)
    th = ridge_fit(vander(xtr, deg), ytr, lam)
    return rmse(vander(xtr, deg), ytr, th), rmse(vander(xva, deg), yva, th)


def exp_capacity():
    print("实验 1：容量扫描（固定 m_train=30，λ=0）——U 形验证曲线")
    rows = []
    for deg in range(1, 13):
        tr, va = holdout(deg)
        rows.append([deg, f"{tr:.4f}", f"{va:.4f}"])
    print("  deg   trainRMSE    valRMSE")
    for r in rows:
        print(f"  {r[0]:>3}   {r[1]:>9}    {r[2]:>9}")
    best = min(rows, key=lambda r: float(r[2]))
    print(f"→ 最优阶数 ≈ {best[0]}（低阶欠拟合=高 bias，高阶过拟合=高 variance）")


def exp_lambda(deg=12):
    print(f"\n实验 2：λ 扫描（固定 deg={deg}，等价于限制有效容量）")
    print("      λ       trainRMSE    valRMSE")
    for lam in [0, 1e-8, 1e-6, 1e-4, 1e-2, 1, 10, 100, 1e3]:
        tr, va = holdout(deg, lam=lam)
        print(f"  {lam:>8.0e}   {tr:>9.4f}    {va:>9.4f}")
    print("→ λ 是连续版'降阶数'：验证曲线仍是 U 形——bias-variance 的旋钮不唯一。")


def exp_learning_curve(deg_bad=12, deg_good=2):
    print("\n实验 3：学习曲线（train/val vs m）——诊断 bias 还是 variance")
    ms = [5, 10, 20, 40, 80, 160, 320]
    for deg, tag in [(deg_good, "欠拟合模型 deg=2"), (deg_bad, "过拟合模型 deg=12")]:
        print(f"  [{tag}]")
        print("     m      train      val     gap")
        for m in ms:
            xtr, ytr = gen(m, 42)
            xva, yva = gen(600, 43)
            th = ridge_fit(vander(xtr, deg), ytr, 0.0)
            tr, va = rmse(vander(xtr, deg), ytr, th), rmse(vander(xva, deg), yva, th)
            print(f"  {m:>5}  {tr:>8.4f} {va:>8.4f} {va-tr:>8.4f}")
    print("→ deg=2：gap 小但双双高位 → 加容量；deg=12：gap 随 m 收窄 → 加数据（L09 诊断流程）。")


def exp_resampling(deg=6):
    """λ 的选择必须由独立验证数据/K-fold 决定（L09 陷阱 2 的制度化）。"""
    print(f"\n实验 4：5-fold KFold 自动选 λ（deg={deg}，m=60）")
    x, y = gen(60, 7)
    X = vander(x, deg)
    rng = np.random.default_rng(0)
    folds = np.array_split(rng.permutation(len(x)), 5)
    best, best_lam = np.inf, None
    for lam in [1e-6, 1e-4, 1e-3, 1e-2, 0.1, 1, 10]:
        errs = []
        for k in range(5):
            te = folds[k]
            tr = np.concatenate([f for j, f in enumerate(folds) if j != k])
            th = ridge_fit(X[tr], y[tr], lam)
            errs.append(rmse(X[te], y[te], th))
        cv = float(np.mean(errs))
        flag = ""
        if cv < best:
            best, best_lam, flag = cv, lam, " *"
        print(f"  λ={lam:<8g} cvRMSE={cv:.4f}{flag}")
    print(f"→ CV 选出 λ={best_lam}（与实验 2 的'目测谷值'对照：手调易过拟合验证集）")


if __name__ == "__main__":
    exp_capacity()
    exp_lambda()
    exp_learning_curve()
    exp_resampling()
