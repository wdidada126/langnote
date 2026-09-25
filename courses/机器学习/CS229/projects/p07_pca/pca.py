"""L08/L18 PCA 实验台：eigh vs svd 双路径、解释方差、白化、与 k-means 的几何协作。

知识点：协方差特征分解 ⟺ SVD 右奇异向量；重构误差/投影方差互补；
白化与条件数；"PCA 前必须中心化"的数值证明；解释方差选 k。
唯一第三方依赖：numpy。运行：python pca.py
"""
import numpy as np
import sys
sys.path.insert(0, ".." + "/p06_clustering_em")
from kmeans import kmeans, ari_trivial           # noqa: E402


def pca_eigh(X, k):
    mu = X.mean(0)
    C = np.cov(X.T, ddof=1)
    w, V = np.linalg.eigh(C)                     # 升序
    idx = np.argsort(w)[::-1]
    return V[:, idx[:k]], w[idx[:k]], mu


def pca_svd(X, k):
    mu = X.mean(0)
    U, s, Vt = np.linalg.svd(X - mu, full_matrices=False)
    var = s ** 2 / (X.shape[0] - 1)
    return Vt.T[:, :k], var[:k], mu


def make_pig(seed=0):
    """经典"猪形"协方差：x 高方差、y 低方差、45° 旋转。"""
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 1, (500, 2)) @ np.array([[2.0, 1.2], [0.0, 0.3]])
    return z + np.array([3.0, -2.0])


def main():
    X = make_pig()
    print("实验 1：双路径一致性 + 解释方差")
    V1, w1, _ = pca_eigh(X, 2)
    V2, w2, _ = pca_svd(X, 2)
    print(f"  max|λ_eigh − λ_svd| = {np.abs(w1 - w2).max():.2e}")
    # k=2 为完整基：|det(V1ᵀV2)|=1 表示同一子空间（2D 全空间平凡成立，比方向逐个核对）
    ang = np.degrees(np.arccos(np.clip(np.abs(V1[:, 0] @ V2[:, 0]), -1, 1)))
    print(f"  两条路径第一主轴夹角 = {ang:.2e}°（eigh 与 svd 应完全一致）")
    evr1 = w1 / w1.sum()
    print(f"  解释方差比例 = {np.round(evr1, 4)}（k=1 保留 {evr1[0]*100:.1f}% 能量）")

    print("\n实验 2：中心化缺失的后果（不减均值 → 第一主成分被均值方向绑架）")
    Vc, _, mu = pca_eigh(X, 1)
    Vbad = np.linalg.svd(X.T @ X / len(X))       # 二阶矩（未中心化）的左/右奇异向量
    ang = np.degrees(np.arccos(min(1.0, abs(float(Vc[:, 0] @ Vbad[0][0])))))
    print(f"  中心化 PC1 vs 未中心化 PC1 夹角 = {ang:.2f}°（均值 {mu} 越大越离谱）")
    print("→ L08 陷阱 1：sklearn PCA 自带中心化，手写时别忘了。")

    print("\n实验 3：重构误差与投影方差互补（L08 §1.3 目标一等价式）")
    total = float(np.trace(np.cov(X.T, ddof=1)))
    for k in [1, 2]:
        V, w, mu_ = pca_eigh(X, k)
        proj = (X - mu_) @ V
        rec_err = float(np.mean(np.sum(((X - mu_) - proj @ V.T) ** 2, 1)))
        kept = w.sum()
        print(f"  k={k}: 保留方差={kept/total*100:5.1f}%  重构误差={rec_err:.4f} "
              f"（两者之和恒 = 总能量 {total:.3f}，逐样本平均后）")

    print("\n实验 4：白化与相关条件数（L16 ICA 前置 / GD 条件数回环 L02）")
    V, w, mu_ = pca_eigh(X, 2)
    Xw = ((X - mu_) @ V) / np.sqrt(w)
    Cw = np.cov(Xw.T, ddof=1)
    print(f"  原数据 cond(cov)={np.linalg.cond(np.cov(X.T, ddof=1)):.1f} → "
          f"白化后 cond={np.linalg.cond(Cw):.3f}")

    print("\n实验 5：PCA 降维对 k-means 的助产（2 维→1 维丢噪声方向）")
    rng = np.random.default_rng(0)
    core = np.vstack([rng.normal([0, 0], 0.5, (150, 2)), rng.normal([6, 0], 0.5, (150, 2))])
    Xn = np.hstack([core, rng.normal(0, 3, (300, 8))])   # 8 个纯噪声维度
    C1, a1, _ = kmeans(Xn, 2, seed=1)
    Vp, _, m2 = pca_eigh(Xn, 1)
    Z = ((Xn - m2) @ Vp[:, :1])
    C2, a2, _ = kmeans(Z, 2, seed=1)
    truth = (core[:, 0] > 3).astype(int)
    print(f"  10 维原始: 一致率={ari_trivial(a1, truth):.3f} | "
          f"PCA-1 维投影: 一致率={ari_trivial(a2, truth):.3f}")
    print("→ 维度灾难稀释欧氏距离；PCA 去噪后 k-means 找回信噪比（L08×L16 协同）。")


if __name__ == "__main__":
    main()
