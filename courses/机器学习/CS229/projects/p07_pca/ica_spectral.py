"""L18 ICA（FastICA 对称版）+ 谱聚类（归一化拉普拉斯）——同一特征分解工具的两次出手。

知识点：白化→负熵最大化坐标迭代（log cosh 非线性）、ICA 的符号/顺序不可辨识、
Ncut 松弛 ⟹ L_sym 前 k 小特征向量 + k-means。
唯一第三方依赖：numpy。运行：python ica_spectral.py
"""
import numpy as np
import sys
sys.path.insert(0, ".." + "/p06_clustering_em")
from kmeans import kmeans                        # noqa: E402
from pca import pca_eigh                         # noqa: E402


# ---------------- FastICA ----------------

def whiten(X):
    mu = X.mean(0)
    C = np.cov((X - mu).T, ddof=1)
    w, V = np.linalg.eigh(C)
    W = (V / np.sqrt(np.maximum(w, 1e-12))).T    # (d,d)：白化矩阵
    Z = (X - mu) @ W.T
    return Z, W


def fastica_sym(Z, iters=200, seed=0):
    """对称正交 FastICA：W ← E[Z g(WᵀZ)ᵀ] − E[g′]W，再对称正交化（Newton-Schulz）。"""
    rng = np.random.default_rng(seed)
    m, d = Z.shape
    A = rng.normal(0, 1, (d, d))

    def g(u):
        return np.tanh(u)                          # log cosh 的导数族代表

    def g_prime(u):
        return 1 - np.tanh(u) ** 2

    for _ in range(iters):
        UA = Z @ A.T                               # (m,d)：各行是一个分离方向的内积
        # 牛顿式分离矩阵更新：A_new = E[z g(Az)ᵀ] − diag(E[g'(Az)]) A（sklearn/FastICA 风格）
        A_new = (Z.T @ g(UA)) / m - g_prime(UA).mean(0)[:, None] * A
        # 对称正交化：A ← (A Aᵀ)^{-1/2} A
        u, s, _ = np.linalg.svd(A_new @ A_new.T)
        A = (u @ np.diag(s ** -0.5) @ u.T) @ A_new
    return A


def alignment_scores(S, Shat):
    """对齐评估：|corr(真源 j, 恢复源 i)| 矩阵（符号/排列不可辨识）。"""
    k = S.shape[1]
    corr = np.corrcoef(np.vstack([S.T, Shat.T]))
    return np.abs(corr[k:, :k])


def ica_demo():
    rng = np.random.default_rng(0)
    t = np.linspace(0, 8 * np.pi, 2000)
    s1 = np.sin(t) + 0.3 * rng.normal(0, 0.1, len(t))
    s2 = np.sign(np.sin(0.7 * t)) + 0.2 * rng.normal(0, 0.1, len(t))   # 方波（非高斯!）
    S = np.stack([s1, s2], 1)
    S = (S - S.mean(0)) / S.std(0)
    Amat = rng.normal(0, 1, (2, 2))
    X = S @ Amat.T
    Z, W = whiten(X)
    A = fastica_sym(Z)
    Shat = Z @ A.T
    corr = alignment_scores(S, Shat)
    print(f"  对齐相关矩阵 =\n{np.round(corr, 3)}")
    print(f"  双随机得分（≈1 表示完美恢复，允许符号/排列任意）= {(corr.max(1).mean() + corr.max(0).mean()) / 2:.4f}")
    kurt = lambda u: np.mean((u - u.mean()) ** 4) / np.var(u) ** 2 - 3
    print(f"  峰度检验：源1={kurt(Shat[:, 0]):+.2f} 源2={kurt(Shat[:, 1]):+.2f}"
          "（正弦≈−1.5 亚高斯，方波≈−1.8；高斯混合会=0）")
    print("  → ICA 找不到'高斯源'：两独立高斯的任何旋转仍独立（L18 §1.2 不可辨识定理）。")


# ---------------- 谱聚类 ----------------

def spectral_two_moons(n=240, seed=1, sigma=0.3, k=2):
    rng = np.random.default_rng(seed)
    t0 = rng.uniform(0, np.pi, n // 2)
    c0 = np.stack([np.cos(t0), np.sin(t0)], 1) + [-0.5, -0.3]
    t1 = rng.uniform(0, np.pi, n // 2)
    c1 = np.stack([1 - np.cos(t1), 1 - np.sin(t1)], 1) + [0.5, 0.3]
    X = np.vstack([c0, c1])
    truth = np.concatenate([np.zeros(n // 2, int), np.ones(n // 2, int)])
    sq = np.sum(X ** 2, 1)
    d2 = np.maximum(sq[:, None] + sq[None] - 2 * X @ X.T, 0)
    Wg = np.exp(-d2 / (2 * sigma ** 2))
    np.fill_diagonal(Wg, 0)
    deg = Wg.sum(1) + 1e-12
    Dm = np.diag(deg ** -0.5)
    Lsym = np.eye(n) - Dm @ Wg @ Dm              # I − D^{-1/2} W D^{-1/2}
    w, V = np.linalg.eigh(Lsym)                  # 升序：最小特征值=0（常数向量）
    Y = V[:, :k]
    Y = Y / (np.linalg.norm(Y, axis=1, keepdims=True) + 1e-12)   # 行归一化（Ng-Jordan-Weiss）
    _, assign, _ = kmeans(Y, k, seed=0)
    # Ncut = cut(A,B)/vol(A) + cut(A,B)/vol(B)，cut = 跨簇边权和
    cross = (assign[:, None] != assign[None, :])
    cut = float(Wg[cross].sum() / 2)
    vol0, vol1 = float(deg[assign == 0].sum()), float(deg[assign == 1].sum())
    ncut = cut / max(vol0, 1e-12) + cut / max(vol1, 1e-12)
    agree = float(np.mean(ari_match(assign, truth)))
    return X, truth, assign, w[:4], ncut, agree


def ari_match(pred, truth):
    """标签置乱下的逐点匹配：枚举 {恒等, 翻转}。"""
    return (pred == truth) if np.mean(pred[truth == 0]) < 0.5 else (pred != truth)


def spectral_demo():
    for sigma in [0.1, 0.3, 1.0]:
        X, truth, assign, w4, ncut, agree = spectral_two_moons(sigma=sigma)
        print(f"  σ={sigma:<4} Fiedler 值 λ2={w4[1]:.4f}  λ3={w4[2]:.4f}  "
              f"与真簇一致率={agree:.3f}  Ncut≈{ncut:.3f}")
    print("→ σ 过小图碎成沙（一致率崩），过大退化为完全图（≈k-means 行为）（L18 陷阱 2）。")


def main():
    print("实验 1：FastICA 鸡尾酒会（正弦 × 方波，2×2 混合）")
    ica_demo()
    print("\n实验 2：谱聚类切双半月（k-means 切不动的流形）")
    spectral_demo()
    print("→ 谱方法沿'窄桥'下刀：割最小 ⟹ Fiedler 向量符号几乎就是簇标签（L18 §1.3）。")


if __name__ == "__main__":
    main()
