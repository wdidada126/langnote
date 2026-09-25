"""L16 路线一：k-means（含 k-means++ 初始化）与收敛性实验。

知识点：坐标下降两步、单调性检查、k++ 的 D² 采样、空簇处理、"球形等方差"假设违约演示。
唯一第三方依赖：numpy。运行：python kmeans.py
"""
import numpy as np


def make_blobs_2d_clusters(seed=0):
    """4 簇混合：其中一对是长条椭圆（k-means 的慢性毒药，L16 陷阱 3）。"""
    rng = np.random.default_rng(seed)
    a = rng.normal([0, 4], [0.5, 0.5], (80, 2))
    b = rng.normal([4, 0], [0.5, 0.5], (80, 2))
    ang = np.pi / 4
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    long_cov = R @ np.diag([1.2, 0.03]) @ R.T
    c = rng.multivariate_normal([-3, -3], long_cov, 90)
    d = rng.multivariate_normal([3, 3], long_cov, 90)
    X = np.vstack([a, b, c, d])
    truth = np.concatenate([np.zeros(80), np.ones(80), np.full(180, 2)])
    return X, truth


def init_random(X, k, rng):
    return X[rng.choice(len(X), k, replace=False)].copy()


def init_kpp(X, k, rng):
    """k-means++：按当前最近中心距离平方 D(x)² 概率采样下一中心。"""
    centers = [X[rng.integers(len(X))]]
    while len(centers) < k:
        C = np.array(centers)
        d2 = np.min(np.maximum(((X[:, None] - C[None]) ** 2).sum(-1), 0), 1)
        p = d2 / d2.sum()
        centers.append(X[rng.choice(len(X), p=p)])
    return np.array(centers)


def kmeans(X, k, iters=100, seed=0, kpp=True, tol=1e-9):
    rng = np.random.default_rng(seed)
    C = init_kpp(X, k, rng) if kpp else init_random(X, k, rng)
    hist = []
    for _ in range(iters):
        d2 = np.maximum(((X[:, None] - C[None]) ** 2).sum(-1), 0)
        assign = d2.argmin(1)
        inertia = float(d2.min(1).sum())
        hist.append(inertia)
        newC = np.zeros_like(C)
        for j in range(k):
            members = X[assign == j]
            newC[j] = members.mean(0) if len(members) else C[rng.integers(k)]  # 空簇重播种
        if abs(hist[-1] - (hist[-2] if len(hist) > 1 else hist[-1])) < tol:
            C = newC
            break
        C = newC
    return C, assign, np.array(hist)


def ari_trivial(pred, truth):
    """极简配对率（非正式 ARI，演示用途）：同对一致比例。"""
    idx = np.random.default_rng(0).choice(len(pred), 800)
    same_pred = pred[idx][:, None] == pred[idx][None, :]
    same_true = truth[idx][:, None] == truth[idx][None, :]
    return float(np.mean(same_pred == same_true))


def main():
    X, truth = make_blobs_2d_clusters()
    print("实验 1：k=3（真簇 3 个但形状违约）——k++ vs 随机初值的 J 分布")
    Js_kpp, Js_rand = [], []
    for s in range(10):
        _, _, h = kmeans(X, 3, seed=s, kpp=True)
        Js_kpp.append(h[-1])
        _, _, h = kmeans(X, 3, seed=s, kpp=False)
        Js_rand.append(h[-1])
    print(f"  k++:  best={min(Js_kpp):.1f} mean={np.mean(Js_kpp):.1f}")
    print(f"  rand: best={min(Js_rand):.1f} mean={np.mean(Js_rand):.1f}")
    print("→ k++ 抬高最差重启的下限（D² 采样避开坏中心），呼应 Arthur-Vassilvitskii。")

    print("\n实验 2：单调性核对——J 每步不增（坐标下降的证明练习数值版）")
    _, _, h = kmeans(X, 4, seed=1)
    diffs = np.diff(h)
    print(f"  最大正增量 = {diffs.max():.2e}（应为 ~0；>0 即实现 bug）")

    print("\n实验 3：假设违约——长条簇被横切")
    C, assign, _ = kmeans(X, 4, seed=2)
    print(f"  k=4 配对一致率={ari_trivial(assign, truth):.3f}（长条对半分切，一致率受损）")
    C, assign, _ = kmeans(X, 5, seed=2)
    print(f"  k=5 配对一致率={ari_trivial(assign, truth):.3f}（用额外簇'补'椭圆的策略）")
    print("→ 各向异性协方差下 k-means 的几何假设失败（EM/GMM 见 em_gmm.py，L16 §1.1）。")

    print("\n实验 4：肘部法（inertia vs k）")
    for k in range(1, 8):
        _, _, h = kmeans(X, k, seed=7)
        print(f"  k={k}  J={h[-1]:>8.1f}")


if __name__ == "__main__":
    main()
