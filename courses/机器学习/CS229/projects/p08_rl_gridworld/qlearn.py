"""L21 Q-learning：同一网格世界上"无模型"学习，与值迭代的 V* 对照。

知识点：TD 更新 Q←Q+α[r+γmaxQ'−Q]、ε-greedy 离策略探索、
Robbins-Monro 学习率条件、收敛度量（与 V* 的 L∞ 误差、胜率）。
唯一第三方依赖：numpy。运行：python qlearn.py
"""
import numpy as np
from gridworld import GridMDP, value_iteration, q_from_v, render


def q_learning(env, episodes=4000, alpha0=0.5, eps0=0.3, seed=0, decay=True):
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.S, env.A))
    steps = []
    for ep in range(episodes):
        # Robbins-Monro 风格衰减（可选）：α_ep, eps_ep
        a = alpha0 / (1.0 + 0.002 * ep) if decay else alpha0
        e = eps0 / (1.0 + 0.002 * ep) if decay else eps0
        non_term = [c for c in env.cells if c not in env.terminals]
        cell = non_term[rng.integers(len(non_term))]
        total = 0
        for t in range(200):
            i = env.idx[cell]
            if rng.random() < e:
                act = rng.integers(env.A)                 # 探索（离策略的核心）
            else:
                act = int(Q[i].argmax())
            nxt, r, done = env.sample(cell, act, rng)
            j = env.idx[nxt]
            Q[i, act] += a * (r + env.gamma * Q[j].max() - Q[i, act])
            cell, total = nxt, total + 1
            if done:
                break
        steps.append(total)
    return Q, np.array(steps)


def v_from_q(Q):
    return Q.max(1)


def win_rate(pi_or_Q, env, n=3000, seed=1):
    rng = np.random.default_rng(seed)
    wins = 0
    for _ in range(n):
        non_term = [c for c in env.cells if c not in env.terminals]
        cell = non_term[rng.integers(len(non_term))]
        for _ in range(100):
            if cell in env.terminals:
                break
            i = env.idx[cell]
            a = int(pi_or_Q[i].argmax())
            cell, _, done = env.sample(cell, a, rng)
            if done:
                break
        wins += cell in env.terminals and env.terminals[cell] > 0
    return wins / n


def main():
    env = GridMDP()
    V_star, pi_star, _ = value_iteration(env)

    print("实验 1：衰减 vs 固定超参（Robbins-Monro 条件的意义）")
    for tag, kw in [("α=0.5 衰减 ε→0", dict(decay=True)),
                    ("α=0.5 固定 ε=0.3", dict(decay=False))]:
        Q, steps = q_learning(env, episodes=4000, seed=2, **kw)
        Vq = v_from_q(Q)
        err = np.abs(Vq - V_star).max()
        wr = win_rate(Q, env)
        wr_star = win_rate(q_from_v(env, V_star), env)
        print(f"  {tag:<18} ‖V̂−V*‖∞={err:.4f}  学习胜率={wr:.3f} 最优胜率={wr_star:.3f}")
    print("→ 固定 α,ε 不收敛但仍有高胜率（'够用哲学'，对照 L02 SGD 抖动邻域）。")

    print("实验 2：探索预算的影响（ε0 扫描，均衰减）")
    for eps0 in [0.05, 0.1, 0.3, 0.8]:
        Q, _ = q_learning(env, episodes=3000, eps0=eps0, seed=3)
        err = np.abs(v_from_q(Q) - V_star).max()
        print(f"  ε0={eps0:<4} ‖V̂−V*‖∞={err:.4f}")
    print("→ ε0 太小：Q 的 (s,a) 覆盖不足，垃圾值残留（L21 陷阱 2 的'饿死'演示）。")

    print("实验 3：学习曲线（每 500 回合的 V 误差，看 1/√episodes 大致衰减）")
    for block in range(8):
        Q, _ = q_learning(env, episodes=500 * (block + 1), seed=4)
        print(f"  episodes={500 * (block + 1):>5}  err={np.abs(v_from_q(Q) - V_star).max():.4f}")

    print("\n实验 4：贪心策略 vs 值迭代策略（应几乎一致）")
    Q, _ = q_learning(env, episodes=6000, seed=5)
    pi_q = Q.argmax(1)
    agree = float(np.mean(pi_q == pi_star))
    print(f"  动作一致率 = {agree:.3f}（部分状态 V 相同 → 多个最优动作，允许不同）")
    render(Q.max(1).argmax(), env, "Q-learning 提取策略：")
    render(pi_star, env, "值迭代最优策略（对照）：")


if __name__ == "__main__":
    main()
