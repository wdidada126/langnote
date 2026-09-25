"""L19 Gibbs 采样：(A) GMM 标签重采样 vs EM 责任度；(B) 2D Ising 模型磁化曲线。

知识点：全条件分布逐坐标更新、细致平衡⟹平稳分布=目标、burn-in、
样本自相关与有效样本数、"采样 vs 优化（EM）"两种处理隐变量的路线。
唯一第三方依赖：numpy。运行：python gibbs.py
"""
import numpy as np


# ---------------- A. GMM 标签 Gibbs ----------------

def gmm_loglik_component(x, mu, Sig, Q):
    d = x.shape[0]
    sign, ld = np.linalg.slogdet(Sig)
    q = (x - mu) @ np.linalg.solve(Sig, x - mu)
    return np.log(Q) - 0.5 * (d * np.log(2 * np.pi) + ld + q)


def gibbs_gmm(X, k, iters=3000, burn=500, seed=0, eps=1e-3):
    """对标签 z_i 做 Gibbs：p(z_i=j | x_i, z_{−i}) ∝ 经验先验·N(x_i; μ̂_j, Σ̂_j)，
    其中 μ̂/Σ̂/先验都由"去掉 i 后"的簇统计构成（共轭 Dirichlet-高斯的全条件）。"""
    rng = np.random.default_rng(seed)
    m, d = X.shape
    z = rng.integers(0, k, m)
    mus0 = np.array([X.mean(0) + rng.normal(0, 1, d) for _ in range(k)])
    chain_size = np.zeros((iters, k))
    for it in range(iters):
        for i in rng.permutation(m):                   # 随机坐标顺序
            lp = np.zeros(k)
            for j in range(k):
                mask = (z == j)
                mask[i] = False                        # z_{−i}
                n = int(mask.sum())
                prior = (n + 0.5) / (m - 1 + k * 0.5)
                if n > d + 2:
                    mu_j = X[mask].mean(0)
                    Sig_j = np.cov(X[mask].T) + eps * np.eye(d)
                else:                                  # 稀疏簇：宽先验兜底
                    mu_j, Sig_j = mus0[j], np.eye(d) * 4.0
                lp[j] = gmm_loglik_component(X[i], mu_j, Sig_j, prior)
            p = np.exp(lp - lp.max())
            z[i] = rng.choice(k, p=p / p.sum())
        chain_size[it] = [(z == j).sum() for j in range(k)]
    return z, chain_size


def autocorr(x, lag):
    x = x - x.mean()
    if np.allclose(x, 0):
        return 0.0
    return float(np.corrcoef(x[:-lag or None], x[lag:])[0, 1] if lag else 1.0)


def ess(x):
    """有效样本数粗估：ESS ≈ n/(1+2Σρ_k)，截断到 ρ_k<0.05。"""
    n = len(x)
    s = 0.0
    for k in range(1, min(n // 4, 100)):
        r = autocorr(x, k)
        if r < 0.05:
            break
        s += r
    return n / (1 + 2 * s)


# ---------------- B. Ising 模型 ----------------

def ising_gibbs(L=12, beta=0.4, iters=3000, burn=800, seed=0):
    rng = np.random.default_rng(seed)
    S = rng.choice([-1, 1], size=(L, L))
    mags = []
    for it in range(iters):
        for _ in range(L * L):                          # 一轮 = L² 次随机坐标更新
            i, j = rng.integers(L), rng.integers(L)
            neigh = S[(i - 1) % L, j] + S[(i + 1) % L, j] + S[i, (j - 1) % L] + S[i, (j + 1) % L]
            # 翻转能 ΔE = −2·β·s_ij·neigh ⟹ p(s=+1) = σ(4β·neigh)（细致平衡成立）
            p_plus = 1.0 / (1.0 + np.exp(-4 * beta * neigh))
            S[i, j] = 1 if rng.random() < p_plus else -1
        mags.append(S.mean())
    return np.array(mags[burn:]), mags


def main():
    print("A. GMM 标签 Gibbs vs EM（同一份混合数据，L16 的对偶路线）")
    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal([0, 0], 0.6, (120, 2)),
                   rng.normal([4, 4], 0.6, (120, 2))])
    z, chain_size = gibbs_gmm(X, k=2, iters=1500, burn=300, seed=1)
    truth = np.concatenate([np.zeros(120, int), np.ones(120, int)])
    agree = max(np.mean(z == truth), np.mean(z != truth))
    print(f"  采样后硬分配 vs 真标签一致率 = {agree:.3f}")
    print(f"  链尾簇配额均值 = {chain_size[-200:].mean(0).round(1)}（真值 [120 120]）")
    e = ess(chain_size[:, 0])
    print(f"  配额链 ESS ≈ {e:.0f}/{len(chain_size)}（标签互换模式=慢混合，对照 L19 陷阱 4）")

    print("\nB. Ising Gibbs：β 扫描下的磁化（铁磁相变的手感）")
    for beta in [0.1, 0.3, 0.44, 0.6]:
        mag, _ = ising_gibbs(beta=beta, iters=1200, burn=400, seed=2)
        print(f"  β={beta:<5} <|m|>={np.abs(mag).mean():.3f}  "
              f"样本自相关 ρ1={autocorr(mag, 1):.3f}  ESS={ess(mag):.0f}")
    print("  临界 β_c = ½ ln(1+√2) ≈ 0.4407：附近磁化剧烈波动且自相关飙升（临界慢化）。")
    print("→ Gibbs=坐标随机下降的概率版；'多链对照'（不同初始块）是最便宜的收敛诊断。")


if __name__ == "__main__":
    main()
