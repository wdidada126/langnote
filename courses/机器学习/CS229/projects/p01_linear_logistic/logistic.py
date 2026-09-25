"""L03 逻辑回归：稳定 sigmoid、交叉熵梯度、GD/SGD 与 Newton/IRLS 的收敛对比。

知识点：从 MLE 导出交叉熵、梯度 (p−y)x 的简洁形式、Hessian 的加权 LS 结构、
log-sum-exp 数值稳定技巧（L03 陷阱 1）。唯一第三方依赖：numpy。运行：python logistic.py
"""
import numpy as np
from common import make_blobs_2d, add_bias, standardize, spark


def log_sigmoid(z):
    """−log(1+e^{−z}) 的稳定实现：z>0 用 −log1p(e^{−z})，z<0 用 z−log1p(e^{z})。"""
    return -np.logaddexp(0.0, -z)


def nll(X, y, theta):
    z = X @ theta
    # −[y·logσ + (1−y)·log(1−σ)] = log(1+e^z) − y z，全程 log 域
    return np.mean(np.logaddexp(0.0, z) - y * z)


def grad_nll(X, y, theta):
    p = 1.0 / (1.0 + np.exp(-np.clip(X @ theta, -50, 50)))
    return X.T @ (p - y) / X.shape[0]


def gd(X, y, alpha=0.5, iters=400):
    theta = np.zeros(X.shape[1])
    hist = []
    for _ in range(iters):
        theta -= alpha * grad_nll(X, y, theta)
        hist.append(nll(X, y, theta))
    return theta, np.array(hist)


def newton_irls(X, y, iters=50, tol=1e-10):
    """θ ← θ − H⁻¹g；H = X^T W X / m，W=diag(p(1−p))：每步是一次加权最小二乘（IRLS）。"""
    m, d = X.shape
    theta = np.zeros(d)
    hist = []
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(X @ theta, -50, 50)))
        g = X.T @ (p - y) / m
        W = p * (1 - p) + 1e-12           # 权重下限防奇异（L03 陷阱 4 的数值面）
        H = X.T @ (X * W[:, None]) / m
        step = np.linalg.solve(H, g)
        # 简单回溯线搜索防 overshoot
        t, f0 = 1.0, nll(X, y, theta)
        for _ in range(20):
            if nll(X, y, theta - t * step) <= f0 - 1e-4 * t * g @ step:
                break
            t *= 0.5
        theta -= t * step
        hist.append(nll(X, y, theta))
        if abs(hist[-1] - (hist[-2] if len(hist) > 1 else f0)) < tol:
            break
    return theta, np.array(hist)


def accuracy(X, y, theta):
    return np.mean((X @ theta >= 0).astype(int) == y.astype(int))


def main():
    print("实验 1：可分 blob（GDA 假设成立场景）——Newton 几步收敛，GD 慢得多")
    X, y = make_blobs_2d(400, seed=7)
    Xb = add_bias(X)
    Z, mu, sd = standardize(Xb[:, 1:])
    Xs = np.hstack([np.ones((X.shape[0], 1)), Z])
    th_gd, h_gd = gd(Xs, y)
    th_nt, h_nt = newton_irls(Xs, y)
    print(f"GD   iters={len(h_gd):4d}  loss={h_gd[-1]:.6f}  acc={accuracy(Xs,y,th_gd):.4f}")
    print(f"Newton iters={len(h_nt):4d}  loss={h_nt[-1]:.6f}  acc={accuracy(Xs,y,th_nt):.4f}")
    print(f"||θ_GD−θ_NT|| = {np.linalg.norm(th_gd - th_nt):.2e}")
    print(spark(np.concatenate([[h_gd[0]], h_gd[::10]]), title="GD loss (每10步)"))
    print("→ 两解重合：逻辑回归+交叉熵是凸问题（L03 §1.2）。p03 将验证该解=GDA 闭式解。")

    print("\n实验 2：类不平衡 1:50 且不做任何处理——acc 高得可疑")
    rng = np.random.default_rng(8)
    X, y = make_blobs_2d(500, seed=8)
    drop = rng.random(y.shape) < 0.98
    keep = ~drop | (y == 1)
    Xb = add_bias(X[keep]); yb = y[keep]
    th, _ = newton_irls(Xb, yb)
    pred = (Xb @ th >= 0).astype(int)
    print(f"全预测多数类 acc = {max(yb.mean(), 1-yb.mean()):.4f}; "
          f"模型 acc = {np.mean(pred==yb):.4f}; 正类召回 = "
          f"{np.mean(pred[yb==1]==1):.4f}")
    print("→ L03 陷阱 2：不平衡下阈值 0.5 与准确率都会骗人；看召回/PR。")

    print("\n实验 3：log_sigmoid 数值稳定性检查")
    z = np.array([-1000.0, -50.0, 0.0, 50.0, 1000.0])
    naive = np.log(1.0 / (1.0 + np.exp(-np.clip(z, -700, 700))))  # 直接写会 underflow
    print(f"稳定版 log σ(z) = {log_sigmoid(z)}")
    print(f"naive  版 log σ(z) = {naive}")
    print("→ 差在 −inf vs 有限值：交叉熵里一个样本就能把梯度炸没（L03 陷阱 1 / CSAPP 浮点）。")


if __name__ == "__main__":
    main()
