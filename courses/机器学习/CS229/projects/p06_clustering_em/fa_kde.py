"""L17 扩展：因子分析 EM + L22 核密度估计带宽扫描（同文件两个小实验）。

知识点：FA 的 EM（E 步条件高斯矩 / M 步 Λ、Φ 闭式更新）、FA 与 PCA 子空间对比
（旋转不可辨识 ⟹ 比较列空间而非载荷）、KDE 的偏差-方差-带宽三角。
唯一第三方依赖：numpy。运行：python fa_kde.py
"""
import numpy as np


# ---------------- 因子分析 EM（Notes L17 §1.2 / Murphy §12.3） ----------------

def gen_factor_data(n=600, m=8, k=2, seed=0):
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 1, (n, k))
    Lam = rng.normal(0, 1, (k, m))
    psi = rng.uniform(0.2, 1.0, m)
    X = z @ Lam + rng.normal(0, 1, (n, m)) * np.sqrt(psi)
    return X, Lam, psi


def fa_em(X, k, iters=200, seed=0):
    m = X.shape[1]
    rng = np.random.default_rng(seed)
    mu = X.mean(0)
    Lam = rng.normal(0, 0.5, (k, m))
    psi = np.full(m, max(X.var(0).mean() / m, 1e-3))
    lls = []
    for _ in range(iters):
        S = Lam.T @ Lam + np.diag(psi)
        Sinv = np.linalg.inv(S + 1e-10 * np.eye(m))
        beta = Lam @ Sinv                       # E[z|x] = beta·(x−mu)
        Xc = X - mu
        Ez = Xc @ beta.T                        # (n,k)
        Covz = S - beta @ S @ beta.T            # Cov(z|x)，与样本无关
        Ezz = Ez.T @ Ez + len(X) * Covz         # Σ_i E[z z^T | x_i]
        Ezx = Ez.T @ Xc                         # Σ_i E[z x^T | x_i]（mu 已中心化）
        Lam = np.linalg.solve(Ezz + 1e-10 * np.eye(k), Ezx)
        R = Xc.T @ Xc / len(X)
        psi = np.maximum(np.diag(R) - np.einsum("ij,ji->j", Lam, Ezx / len(X)), 1e-6)
        S = Lam.T @ Lam + np.diag(psi)          # 用更新后的参数计算边际对数似然
        Sinv2 = np.linalg.inv(S + 1e-10 * np.eye(m))
        _, ld = np.linalg.slogdet(S)
        quad = np.einsum("ij,jk,ik->", Xc, Sinv2, Xc)
        lls.append(-0.5 * (quad + len(X) * (ld + m * np.log(2 * np.pi))))
    return Lam, psi, np.array(lls)


def orthonormal_basis(A):
    """A 的列空间正交基（SVD）。"""
    U, s, Vt = np.linalg.svd(A.T)              # A.T: m×k → U 的前几列
    r = int((s > 1e-10 * max(s[0], 1e-30)).sum())
    return U[:, :max(r, A.shape[0])]


def principal_angles(U1, U2):
    """两个同维子空间的主角度（度数）。"""
    s = np.linalg.svd(U1.T @ U2, compute_uv=False)
    return np.degrees(np.arccos(np.clip(s, -1, 1)))


def pca_subspace(X, k):
    C = np.cov((X - X.mean(0)).T)
    w, V = np.linalg.eigh(C)
    return V[:, ::-1][:, :k]                   # 正交基


# ---------------- 核密度估计 ----------------

def kde_eval(x, X, h):
    """高斯核（一维）：p̂(x) = (1/(m h)) Σ φ((x−x_i)/h)。"""
    return np.exp(-0.5 * ((x[:, None] - X[None]) / h) ** 2).sum(1) \
        / (len(X) * h * np.sqrt(2 * np.pi))


def kde_demo():
    rng = np.random.default_rng(0)
    truth = np.concatenate([rng.normal(-2, 0.6, 400), rng.normal(2, 1.0, 600)])
    grid = np.linspace(-5, 5, 401)
    p_true = (0.4 * np.exp(-0.5 * ((grid + 2) / 0.6) ** 2) / (0.6 * np.sqrt(2 * np.pi))
              + 0.6 * np.exp(-0.5 * ((grid - 2) / 1.0) ** 2) / (1.0 * np.sqrt(2 * np.pi)))
    print("KDE 带宽扫描（ISE = mean (p̂−p)² 网格近似）")
    for h in [0.05, 0.1, 0.2, 0.4, 0.8]:
        p = kde_eval(grid, truth, h)
        print(f"  h={h:<5} ISE={np.mean((p - p_true) ** 2):.5f}"
              "   （小 h 高方差锯齿 ↔ 大 h 高偏差过平滑）")
    print("m 趋势：h* ∝ m^{-1/5}（每 ×16 样本，最优 h 约减半）")
    for m in [100, 400, 1600, 6400]:
        samp = np.concatenate([rng.normal(-2, 0.6, m * 2 // 5),
                               rng.normal(2, 1.0, m * 3 // 5)])
        hs = [0.03, 0.05, 0.08, 0.12, 0.2, 0.3, 0.45, 0.7]
        scores = [np.mean((kde_eval(grid, samp, h) - p_true) ** 2) for h in hs]
        print(f"  m={m:>4}  argmin h = {hs[int(np.argmin(scores))]}")


def main():
    print("实验 1：FA-EM 恢复真实载荷（k=2, m=8）")
    X, Lam_true, psi_true = gen_factor_data(seed=1)
    Lam, psi, ll = fa_em(X, k=2)
    # 旋转不可辨识 ⟹ 比较列空间：对齐度 = 主角度
    ang = principal_angles(orthonormal_basis(Lam.T), orthonormal_basis(Lam_true.T))
    print(f"  FA 列空间 vs 真值列空间 主角度 = {np.round(ang, 2)}°（≈0° 即同一平面）")
    print(f"  Φ̂    = {np.round(psi, 3)}")
    print(f"  Φ_true = {np.round(psi_true, 3)}   （唯一性=私有方差：PCA 不建模的量）")

    print("\n实验 2：FA vs PCA——同一数据两张透镜")
    Vp = pca_subspace(X, 2)
    ang_pca = principal_angles(Vp, orthonormal_basis(Lam.T))
    print(f"  PCA 前 2 主轴 vs FA 列空间主角度 = {np.round(ang_pca, 2)}°")
    print("  → 有限样本+异方噪声下两子空间会分开；Φ→σ²I 极限时重合（L17 §1.1）。")

    print("\n实验 3：KDE")
    kde_demo()


if __name__ == "__main__":
    main()
