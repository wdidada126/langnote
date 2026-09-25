"""L06-L07 路线一：hinge 损失次梯度法（软间隔 SVM 的无约束等价形）。

min_θ  (λ/2)‖w‖² + (1/m)Σ max(0, 1 − y_i(w^T x_i + b))   （y∈{−1,+1}）
知识点：函数/几何间隔、hinge 与 SVM 约束式的关系、C=1/λ 视角、间隔分布统计。
唯一第三方依赖：numpy。运行：python hinge_sgd.py
"""
import numpy as np


def make_data(n=300, seed=0, overlap=False):
    rng = np.random.default_rng(seed)
    s = 1.0 if not overlap else 1.9
    X = np.vstack([rng.normal([-2, -2], s, (n // 2, 2)),
                   rng.normal([2, 2], s, (n // 2, 2))])
    y = np.concatenate([-np.ones(n // 2), np.ones(n // 2)])
    return X, y


def hinge_train(X, y, lam=0.05, iters=4000, lr=0.01, seed=0):
    rng = np.random.default_rng(seed)
    m, d = X.shape
    w = np.zeros(d); b = 0.0
    for t in range(iters):
        idx = rng.integers(m)
        xi, yi = X[idx], y[idx]
        margin = yi * (w @ xi + b)
        if margin < 1:                       # 违例：沿 hinge 次梯度
            w -= lr * (lam * w - yi * xi)
            b -= lr * (-yi)
        else:
            w -= lr * lam * w                # 仅权重衰减（正则项梯度）
    return w, b


def report(X, y, w, b, tag):
    margins = y * (X @ w + b)                # 函数间隔
    geo = margins / np.linalg.norm(w)        # 几何间隔
    viol = float(np.mean(margins < 1))
    geo_margin = float(np.min(margins) / np.linalg.norm(w))   # 最小几何间隔（训练集）
    acc = float(np.mean(np.sign(X @ w + b) == y))
    print(f"{tag:<28} acc={acc:.4f}  min几何间隔={geo_margin:.4f}  "
          f"违例比例={viol:.3f}  ‖w‖={np.linalg.norm(w):.3f}")
    return geo


def main():
    print("实验 1：λ（=1/C 风格）对间隔与违例的权衡（L06 软间隔）")
    Xtr, ytr = make_data(400, seed=1, overlap=True)
    mu, sd = Xtr.mean(0), Xtr.std(0)
    Xtr = (Xtr - mu) / sd                    # L06 陷阱 2：先标准化
    Xte, yte = make_data(2000, seed=2, overlap=True)
    Xte = (Xte - mu) / sd
    for lam in [1.0, 0.3, 0.1, 0.03, 0.01]:
        w, b = hinge_train(Xtr, ytr, lam=lam)
        # 测试集上报告 acc 与训练集最小几何间隔
        acc = float(np.mean(np.sign(Xte @ w + b) == yte))
        g = ytr * (Xtr @ w + b) / np.linalg.norm(w)
        print(f"  λ={lam:<5g} test acc={acc:.4f}  train min-geo-margin={g.min():.4f}  "
              f"#(margin<0)={int((g<0).sum())}")
    print("→ λ 小（C 大）：训练间隔名义变大但违例被严惩→对重叠区更激进；"
          "λ 大：‖w‖ 小、边界'宽厚'但训练违例多。")

    print("\n实验 2：可分数据上看最大间隔行为（λ→0 时逼近 OMC）")
    Xtr, ytr = make_data(300, seed=3, overlap=False)
    mu, sd = Xtr.mean(0), Xtr.std(0)
    Xtr = (Xtr - mu) / sd
    for lam in [0.1, 0.01, 0.001]:
        w, b = hinge_train(Xtr, ytr, lam=lam, iters=8000)
        margins = ytr * (Xtr @ w + b)
        nsv = int((margins < 1.01).sum())
        print(f"  λ={lam:<7g} 最小函数间隔={margins.min():.3f}  "
              f"边界附近点数(近似 #SV)={nsv}")
    print("→ hinge 约束被顶到 ≥1 的紧贴点 = 支持向量；λ→0 时解向最大间隔收敛。")

    print("\n实验 3：感知机对照（永远不分开的'无间隔'世界）")
    w = np.zeros(2); b = 0.0
    rng = np.random.default_rng(0)
    epochs = 0
    while True:
        order = rng.permutation(len(Xtr))
        changed = False
        for i in order:
            if ytr[i] * (w @ Xtr[i] + b) <= 0:
                w += 0.1 * ytr[i] * Xtr[i]; b += 0.1 * ytr[i]; changed = True
        epochs += 1
        if not changed or epochs > 500:
            break
    margins = ytr * (Xtr @ w + b) / np.linalg.norm(w)
    print(f"  感知机 {epochs} 轮收敛；其最小几何间隔={margins.min():.4f}（无最大化目标，随机初值敏感）")
    print("→ 对比 λ→0 的 hinge 解：'能分开'与'分得漂亮'的差距（L06 动机 / L08 感知机收敛定理）")


if __name__ == "__main__":
    main()
