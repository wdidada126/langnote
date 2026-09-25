"""L19 HMM 精确推断：前向-后向（log 域）+ Viterbi + Baum-Welch（离散 EM）。

知识点：α/β log 域递推（防下溢，L19 §1.2 数值）、γ/ξ 责任度、
max-product 半环、Baum-Welch = EM 的序列实例（对接 p06 的 EM 循环）。
唯一第三方依赖：numpy。运行：python hmm.py
"""
import numpy as np

LOG0 = -1e30    # log(0) 的有限替身，避免 NaN 传播


def make_hmm(N=2, M=3, seed=0):
    rng = np.random.default_rng(seed)
    A = rng.dirichlet(np.ones(N) * 5, size=N)       # 转移
    B = rng.dirichlet(np.ones(M) * 5, size=N)       # 发射
    pi = rng.dirichlet(np.ones(N) * 5)
    return A, B, pi


def simulate(A, B, pi, T=60, seed=1):
    rng = np.random.default_rng(seed)
    s = rng.choice(A.shape[0], p=pi)
    states, obs = [], []
    for _ in range(T):
        states.append(s)
        obs.append(rng.choice(B.shape[1], p=B[s]))
        s = rng.choice(A.shape[0], p=A[s])
    return np.array(states), np.array(obs)


def lse(a):
    a = np.asarray(a, float)
    m = a.max()
    return m + np.log(np.exp(a - m).sum()) if np.isfinite(m) else m


def log_forward(A, B, pi, obs):
    T, N = len(obs), A.shape[0]
    la, lb, lpi = np.log(A + 1e-300), np.log(B + 1e-300), np.log(pi + 1e-300)
    alpha = np.full((T, N), LOG0)
    alpha[0] = lpi + lb[:, obs[0]]
    for t in range(1, T):
        for j in range(N):
            alpha[t, j] = lse(alpha[t - 1] + np.log(A[:, j] + 1e-300))
        alpha[t] += lb[:, obs[t]]
    return alpha, lse(alpha[-1])


def log_backward(A, B, obs):
    T, N = len(obs), A.shape[0]
    lb, lA = np.log(B + 1e-300), np.log(A + 1e-300)
    beta = np.full((T, N), LOG0)
    beta[-1] = 0.0
    for t in range(T - 2, -1, -1):
        for i in range(N):
            beta[t, i] = lse(lA[i] + lb[:, obs[t + 1]] + beta[t + 1])
    return beta


def forward_backward(A, B, pi, obs):
    """返回 log P(obs)、γ (T,N)、ξ (T−1,N,N)。"""
    T, N = len(obs), A.shape[0]
    alpha, ll = log_forward(A, B, pi, obs)
    beta = log_backward(A, B, obs)
    g = alpha + beta
    gamma = np.exp(g - g.max(1, keepdims=True))
    gamma /= gamma.sum(1, keepdims=True)
    xi = np.zeros((T - 1, N, N))
    lA, lb = np.log(A + 1e-300), np.log(B + 1e-300)
    for t in range(T - 1):
        M = alpha[t][:, None] + lA + lb[:, obs[t + 1]][None, :] + beta[t + 1][None, :]
        M -= M.max()
        xi[t] = np.exp(M)
        xi[t] /= xi[t].sum()
    return ll, gamma, xi


def viterbi(A, B, pi, obs):
    T, N = len(obs), A.shape[0]
    la, lb, lpi = np.log(A + 1e-300), np.log(B + 1e-300), np.log(pi + 1e-300)
    delta = lpi + lb[:, obs[0]]
    psi = np.zeros((T, N), int)
    for t in range(1, T):
        for j in range(N):
            psi[t, j] = (delta + la[:, j]).argmax()
        delta = np.array([delta[psi[t, j]] + la[psi[t, j], j] for j in range(N)]) \
            + lb[:, obs[t]]
    path = [int(delta.argmax())]
    for t in range(T - 1, 0, -1):
        path.append(int(psi[t, path[-1]]))
    return np.array(path[::-1]), float(delta.max())


def baum_welch(obs, N=2, M=3, iters=100, seed=0, tol=1e-8):
    rng = np.random.default_rng(seed)
    A = rng.dirichlet(np.ones(N), size=N)
    B = rng.dirichlet(np.ones(M), size=N)
    pi = rng.dirichlet(np.ones(N))
    prev = -np.inf
    curve = []
    for _ in range(iters):
        ll, gamma, xi = forward_backward(A, B, pi, obs)
        curve.append(ll)
        A = xi.sum(0)
        A /= A.sum(1, keepdims=True) + 1e-12
        for w in range(M):
            B[:, w] = gamma[obs == w].sum(0)          # Σ_t 1{o_t=w} γ_t(j)
        B /= B.sum(1, keepdims=True) + 1e-12
        pi = gamma[0] / gamma[0].sum()
        if ll - prev < tol:
            break
        prev = ll
    return A, B, pi, np.array(curve)


def main():
    A, B, pi = make_hmm(seed=0)
    states, obs = simulate(A, B, pi, T=60, seed=1)
    print(f"真 HMM：N=2, M=3, T=60；观测前 18 步：{obs[:18]}")

    ll, gamma, xi = forward_backward(A, B, pi, obs)
    print(f"前向递推 log P(obs) = {ll:.3f}")

    # 暴力枚举验证截断前缀（6 步）：Σ_{路径} π·Π A·B
    Tc = 6
    brute = 0.0

    def rec(t, s, p):
        nonlocal brute
        if t == Tc:
            brute += p
            return
        for j in range(A.shape[0]):
            rec(t + 1, j, p * A[s, j] * B[j, obs[t]])
    for s0 in range(A.shape[0]):
        rec(1, s0, pi[s0] * B[s0, obs[0]])
    ll_prefix = forward_trunc(A, B, pi, obs, Tc)
    print(f"截断 T={Tc}：暴力路径和={np.log(brute):.6f} vs 前向递推={ll_prefix:.6f}")

    vpath, vscore = viterbi(A, B, pi, obs)
    smooth = gamma.argmax(1)
    print(f"Viterbi vs 平滑 argmax 一致率 = {np.mean(vpath == smooth):.3f}")
    print(f"Viterbi vs 真状态序列 一致率 = {np.mean(vpath == states):.3f}（模型=真模型时参照上界）")

    A_e, B_e, pi_e, curve = baum_welch(obs, iters=120, seed=3)
    print(f"Baum-Welch（随机初值）：loglik {curve[0]:.1f} → {curve[-1]:.1f}（{len(curve)} 轮，"
          f"真模型 LL={ll:.1f}）")
    # 状态排列自由：挑更好的置换再比误差
    err_id = np.abs(A_e - A).max()
    err_sw = np.abs(A_e[::-1] - A).max()
    best_err = min(err_id, err_sw)
    print(f"排列对齐后转移矩阵误差 max|Â−A| = {best_err:.3f}")
    print("→ 学到的是'似然等价类'中的某个解（状态排列自由）；EM 单调不降（p06 同款曲线）。")


def forward_trunc(A, B, pi, obs, Tc):
    alpha, _ = log_forward(A, B, pi, obs[:Tc])
    return lse(alpha[-1])


if __name__ == "__main__":
    main()
