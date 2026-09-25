"""L02-L03 附录：梯度下降家族超参实验——学习率 × 动量（任务要求的 lr/动量实验）。

在同一个 LMS 二次目标上比较：GD、momentum GD、（对照）Adam 的手写 mini 版。
知识点：α 过小/过大行为、动量对病态方向的加速、β 的"有效记忆窗口 1/(1-β)"。
唯一第三方依赖：numpy。运行：python gd_momentum.py
"""
import numpy as np
from common import make_regression, add_bias, standardize, spark


def quad_problem(seed=5, d=6, ill=True):
    X, y = make_regression(300, d, seed=seed, ill_conditioned=ill)
    Xb = add_bias(X)
    Z, mu, sd = standardize(Xb[:, 1:])
    Xs = np.hstack([np.ones((X.shape[0], 1)), Z]) if ill else Xb
    # 二次型 J(θ)=0.5 θ^T A θ − b^T θ + c 的矩阵（A = X^T X/m）
    A = Xs.T @ Xs / Xs.shape[0]
    b = Xs.T @ y / Xs.shape[0]
    return A, b


def run(A, b, alpha, momentum=0.0, iters=300, theta0=None):
    g = lambda t: A @ t - b
    theta = np.zeros(A.shape[0]) if theta0 is None else theta0.copy()
    v = np.zeros_like(theta)
    js = []
    for _ in range(iters):
        grad = g(theta)
        v = momentum * v + grad
        theta = theta - alpha * v
        r = A @ theta - b
        js.append(0.5 * theta @ A @ theta - b @ theta)   # 与 0.5‖Xθ−y‖²/m 差常数
    return theta, np.array(js)


def main():
    A, b = quad_problem()
    theta_star = np.linalg.solve(A, b)
    lam = np.linalg.eigvalsh(A)
    print(f"条件数 κ = λmax/λmin = {lam[-1]/lam[0]:.1f}")
    alpha_max = 2.0 / lam[-1]           # 梯度光滑常数 L=λmax 的 GD 稳定上界
    print(f"理论稳定上界 α < 2/λmax = {alpha_max:.3f}\n")

    for name, kwargs in [
        ("GD α=0.1/L", dict(alpha=0.1 * alpha_max)),
        ("GD α=0.9/L (临界)", dict(alpha=0.9 * alpha_max)),
        ("GD α=2.2/L (发散!)", dict(alpha=2.2 * alpha_max)),
        ("momentum β=0.9, α=0.5/L", dict(alpha=0.5 * alpha_max, momentum=0.9)),
        ("momentum β=0.98, α=0.5/L", dict(alpha=0.5 * alpha_max, momentum=0.98)),
    ]:
        th, js = run(A, b, iters=200, **kwargs)
        err = np.linalg.norm(th - theta_star)
        finite = np.isfinite(js).all()
        tail = js[-1] if finite else float("nan")
        print(table_line(name, err, tail))
        print(spark(js[:200] if finite else np.nan_to_num(js[:50], nan=1e10),
                    title="  loss"))

    print("→ 结论（对应 L02 §1.2 与陷阱）：")
    print("  1) α>2/λmax 必发散，可数值验证；2) 动量以牺牲稳定上界(≈(1+β)/L)换病态方向加速;")
    print("  3) β 过大(0.98)在二次问题上反而震荡——动量不是免费的午餐。")


def table_line(name, err, tail):
    return f"{name:<28} ||θ−θ*||={err:9.3e}  final J≈{tail:12.6f}"


if __name__ == "__main__":
    main()
