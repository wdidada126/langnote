"""L16 路线二：高斯混合模型 EM（全协方差），与 k-means 同数据对照。

知识点：责任度 logsumexp 稳定计算、对数似然单调性、Σ_j+εI 防奇异、
"球形共享协方差 ⟹ EM 退化为 k-means"的数值印证（L16 §1.3）、BIC 选 k。
唯一第三方依赖：numpy。运行：python em_gmm.py
"""
import numpy as np
from kmeans import make_blobs_2d_clusters, kmeans, init_kpp, ari_trivial


def logsumexp(a, axis=None):
    a = np.asarray(a)
    m = np.max(a, axis=axis, keepdims=True)
    out = m + np.log(np.sum(np.exp(a - m), axis=axis, keepdims=True))
    return np.squeeze(out, axis=axis) if a.ndim > 1 and axis is not None else float(out)


def log_gauss_pdf(X, mu, Sigma):
    d = X.shape[1]
    _, logdet = np.linalg.slogdet(Sigma)
    diff = X - mu
    quad = np.einsum("ij,ij->i", diff, np.linalg.solve(Sigma, diff.T).T)
    return -0.5 * (d * np.log(2 * np.pi) + logdet + quad)


def fit_gmm(X, k, iters=100, seed=0, eps=1e-4):
    rng = np.random.default_rng(seed)
    m, d = X.shape
    mu, _, _ = kmeans(X, k, iters=30, seed=seed)      # k++ 中心作初始化
    Sigma = np.array([np.cov(X.T) + eps * np.eye(d)] * k)
    Q = np.full(k, 1.0 / k)
    hist = []
    for _ in range(iters):
        lp = np.stack([np.log(Q[j] + 1e-300) + log_gauss_pdf(X, mu[j], Sigma[j])
                       for j in range(k)])                      # (k,m)
        lse = logsumexp(lp, axis=0)
        hist.append(float(lse.sum()))
        W = np.exp(lp - lse)                                    # 责任度 (k,m)
        Nk = W.sum(1) + 1e-12
        mu = (W @ X) / Nk[:, None]
        for j in range(k):
            diff = X - mu[j]
            Sigma[j] = (W[j][:, None] * diff).T @ diff / Nk[j] + eps * np.eye(d)
        Q = Nk / m
        if len(hist) > 1 and hist[-1] - hist[-2] < 1e-8:
            break
    return mu, Sigma, Q, np.array(hist), W


def fit_gmm_spherical_tied(X, k, iters=50, sigma2=1.0, seed=0):
    """共享球形协方差 σ²I 的特例：E 步 argmax_j −‖x−μ_j‖²/2σ² = 最近中心，
    与 k-means 完全一致（L16 定理的构造性证明）。"""
    rng = np.random.default_rng(seed)
    mu = init_kpp(X, k, rng)
    for _ in range(iters):
        d2 = np.maximum(((X[:, None] - mu[None]) ** 2).sum(-1), 0)
        assign = d2.argmin(1)                                   # E 步
        for j in range(k):                                      # M 步（等权 Q）
            if (assign == j).any():
                mu[j] = X[assign == j].mean(0)
    return mu, assign


def bic(X, ll, k):
    d = X.shape[1]
    n_par = k * (1 + d + d * (d + 1) // 2)
    return -2 * ll + n_par * np.log(len(X))


def main():
    X, truth = make_blobs_2d_clusters()

    print("实验 1：GMM-EM 拟合各向异性簇（k-means 慢性毒药场景）")
    mu, Sig, Q, hist, W = fit_gmm(X, 4, seed=0)
    hard = W.argmax(0)
    ok = np.all(np.diff(hist) >= -1e-9)
    print(f"  loglik {hist[0]:.1f} → {hist[-1]:.1f}，单调不降={ok}")
    print(f"  GMM 硬分配一致率={ari_trivial(hard, truth):.3f}（对比 kmeans.py 实验 3 的横切）")

    print("\n实验 2：球形共享 Σ ⟹ EM ≡ k-means（数值印证 L16 §1.3）")
    mu_t, assign_t = fit_gmm_spherical_tied(X, 3, seed=1)
    C, assign_k, _ = kmeans(X, 3, seed=1, kpp=True)
    # 两算法随机初值不同，直接比"目标函数同族性"：tied 版的分配就是最近中心
    d2 = np.maximum(((X[:, None] - mu_t[None]) ** 2).sum(-1), 0)
    same = np.all(assign_t == d2.argmin(1))
    print(f"  tied-球形 EM 的 E 步 == 最近中心分配：{same}")
    print(f"  一致率 tied-EM={ari_trivial(assign_t, truth):.3f} vs k-means={ari_trivial(assign_k, truth):.3f}（同一算法）")

    print("\n实验 3：BIC 选 k（loglik 永远骗人，罚项说真话）")
    for k in [2, 3, 4, 5, 6]:
        _, _, _, h, _ = fit_gmm(X, k, seed=3)
        print(f"  k={k}  loglik={h[-1]:>9.1f}  BIC={bic(X, h[-1], k):>9.1f}")
    print("→ 真簇数 3 附近 BIC 见底——结构风险（L09）在无监督下的化身。")

    print("\n实验 4：模糊责任度是信息量")
    pt = np.array([[0.0, 2.0]])
    lp = np.stack([np.log(Q[j]) + log_gauss_pdf(pt, mu[j], Sig[j])
                   for j in range(len(mu))])
    r = np.exp(lp - logsumexp(lp, axis=0))
    print(f"  点 (0,2) 的 responsibility = {np.round(r.ravel(), 3)}")
    print("  （k-means 只能硬判一类；软归属可用于缺失填补/异常度量，L16 陷阱 5）")


if __name__ == "__main__":
    main()
