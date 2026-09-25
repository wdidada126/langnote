"""L02 线性回归：batch GD / SGD / 正规方程，及数值解法对照。

知识点：LMS 损失与梯度、批量 vs 随机 GD、学习率敏感性、
条件数与特征标准化、正规方程的 solve/lstsq/inv 数值对比、高斯噪声=平方损失的 MLE 解释。
唯一第三方依赖：numpy。运行：python linear.py
"""
import numpy as np
from common import make_regression, add_bias, standardize, spark, table


def loss(X, y, theta):
    r = X @ theta - y
    return 0.5 * np.mean(r * r)


def grad(X, y, theta):
    return X.T @ (X @ theta - y) / X.shape[0]


def batch_gd(X, y, alpha=0.1, iters=200, theta0=None):
    theta = np.zeros(X.shape[1]) if theta0 is None else theta0.copy()
    hist = [loss(X, y, theta)]
    for _ in range(iters):
        theta -= alpha * grad(X, y, theta)
        hist.append(loss(X, y, theta))
    return theta, np.array(hist)


def sgd(X, y, alpha0=0.1, b=50.0, epochs=30, seed=0):
    """衰减学习率 alpha(i)=a/(b+i)（L02 §1.3），每 epoch 洗牌。"""
    rng = np.random.default_rng(seed)
    m = X.shape[0]
    theta = np.zeros(X.shape[1])
    hist, i = [loss(X, y, theta)], 0
    for _ in range(epochs):
        for idx in rng.permutation(m):
            a = alpha0 / (b + i)
            theta -= a * X[idx] * (X[idx] @ theta - y[idx])
            i += 1
            if i % (m // 10) == 0:
                hist.append(loss(X, y, theta))
    return theta, np.array(hist)


def normal_equations(X, y):
    G = X.T @ X
    return np.linalg.solve(G, X.T @ y)     # 用 solve，绝不显式 inv


def demo():
    print("=" * 70)
    print("实验 1：良态数据（d=3，标准化）—— GD vs SGD vs 正规方程")
    X, y = make_regression(200, 3, seed=1)
    Xb = add_bias(X)
    Z, mu, sd = standardize(Xb[:, 1:])
    Xs = np.hstack([np.ones((X.shape[0], 1)), Z])
    th_gd, h_gd = batch_gd(Xs, y, alpha=0.1, iters=100)
    th_sgd, h_sgd = sgd(Xs, y)
    th_ne = normal_equations(Xs, y)
    th_ls = np.linalg.lstsq(Xs, y, rcond=None)[0]
    print(table(
        [["GD  ", loss(Xs, y, th_gd), np.linalg.norm(th_gd - th_ne)],
         ["SGD ", loss(Xs, y, th_sgd), np.linalg.norm(th_sgd - th_ne)],
         ["lstsq", loss(Xs, y, th_ls), np.linalg.norm(th_ls - th_ne)]],
        ["solver", "final J", "||θ-θ*||"]))
    print(spark(h_gd, title="batch GD loss"))

    print("=" * 70)
    print("实验 2：病态数据（特征尺度 1:1e-3）—— 同样的 α，GD 挣扎")
    X, y = make_regression(200, 3, seed=1, ill_conditioned=True)
    Xb = add_bias(X)
    print(f"cond(X^T X) ≈ {np.linalg.cond(Xb.T @ Xb):.1e}")
    _, h_raw = batch_gd(Xb, y, alpha=0.1, iters=100)
    Z, mu, sd = standardize(Xb[:, 1:])
    Xz = np.hstack([np.ones((X.shape[0], 1)), Z])
    _, h_std = batch_gd(Xz, y, alpha=0.1, iters=100)
    print(spark(h_raw, title="GD on raw scales"))
    print(spark(h_std, title="GD after standardize"))
    print("→ L02 陷阱 2：GD 慢常常不是 α 太小，而是数据没缩放。")

    print("=" * 70)
    print("实验 3：数值稳定性——inv vs solve vs lstsq 在 n≈m 时")
    rng = np.random.default_rng(2)
    X = rng.normal(size=(100, 95))
    yv = rng.normal(size=100)
    th_inv = np.linalg.inv(X.T @ X + 1e-12 * np.eye(96)) @ (X.T @ yv)
    th_sol = np.linalg.solve(X.T @ X + 1e-12 * np.eye(96), X.T @ yv)
    th_pinv = np.linalg.pinv(X) @ yv
    print(f"||inv−solve||={np.linalg.norm(th_inv-th_sol):.2e}  "
          f"||solve−pinv||={np.linalg.norm(th_sol-th_pinv):.2e}")
    print("→ cond(X^T X)=cond(X)^2：先对角加载 λI，再优先 solve/pinv（L02 陷阱 3）。")

    print("=" * 70)
    print("实验 4：概率解释——σ̂² 与残差方差、以及高斯 MLE=最小二乘的数值确认")
    X, y = make_regression(300, 3, seed=3)
    Xb = add_bias(X)
    th = normal_equations(Xb, y)
    resid = y - Xb @ th
    print(f"σ̂²(1/m 有偏)= {np.mean(resid**2):.4f}   "
          f"σ̂²(1/(m-d) 无偏)= {resid @ resid / (len(y)-Xb.shape[1]):.4f}")
    print("→ J(θ*)·m ≈ 高斯对数似然的负值（差常数）：平方损失 = 高斯噪声 MLE。")


if __name__ == "__main__":
    demo()
