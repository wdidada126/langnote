"""L20 玩具网格世界 MDP + 值迭代/策略迭代（自建环境，不依赖 Gymnasium，纯 numpy）。

知识点：(S,A,P,R,γ) 五元组与转移张量、Bellman 备份、
值迭代（压缩映射收敛）与策略迭代（评估-改进交替）、策略提取。
唯一第三方依赖：numpy。运行：python gridworld.py
"""
import numpy as np

GRID = [
    ["1", "1", "1", "G+"],
    ["1", "#", "1", "#"],
    ["G-", "1", "1", "1"],
]                     # 4x5 双出口网格（+1 宝藏 / −1 陷阱 / 墙）
MOVES = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}   # 上下左右
SLIP = 0.2            # 10% 概率滑向左手侧、10% 右手侧


class GridMDP:
    def __init__(self, slip=SLIP, gamma=0.95):
        self.h, self.w = len(GRID), len(GRID[0])
        self.slip, self.gamma = slip, gamma
        self.cells = [(r, c) for r in range(self.h) for c in range(self.w)
                      if GRID[r][c] != "#"]
        self.terminals = {(r, c): 1.0 if GRID[r][c] == "G+" else -1.0
                          for r in range(self.h) for c in range(self.w)
                          if GRID[r][c].startswith("G")}
        self.S, self.A = len(self.cells), 4
        self.idx = {c: i for i, c in enumerate(self.cells)}
        self.P = np.zeros((self.S, self.A, self.S))
        self.R = np.zeros((self.S, self.A, self.S))     # 到达即得奖励
        self._build()

    def _nxt(self, cell, a):
        r, c = cell[0] + MOVES[a][0], cell[1] + MOVES[a][1]
        if not (0 <= r < self.h and 0 <= c < self.w) or GRID[r][c] == "#":
            return cell
        return (r, c)

    def _build(self):
        for cell in self.cells:
            i = self.idx[cell]
            if cell in self.terminals:
                self.P[i, :, i] = 1.0                   # 吸收态
                continue
            for a in range(4):
                outs = [self._nxt(cell, a), self._nxt(cell, (a - 1) % 4),
                        self._nxt(cell, (a + 1) % 4)]
                probs = [1 - self.slip, self.slip / 2, self.slip / 2]
                for o, p in zip(outs, probs):
                    j = self.idx[o]
                    self.P[i, a, j] += p
                    self.R[i, a, j] += self.terminals.get(o, 0.0)

    def sample(self, cell, a, rng):
        if cell in self.terminals:
            return cell, 0.0, True
        i = self.idx[cell]
        p = self.P[i, a].copy()
        j = rng.choice(self.S, p=p / p.sum())
        nxt = self.cells[j]
        return nxt, self.R[i, a, j], nxt in self.terminals


def q_from_v(env, V):
    """Q(s,a) = Σ P(R + γV)：V→Q 的 Bellman 期望备份。"""
    return np.einsum("sij,j->si", env.P, env.R + env.gamma * V[None, None, :])


def value_iteration(env, iters=200, tol=1e-10):
    V = np.zeros(env.S)
    deltas = []
    for _ in range(iters):
        Q = q_from_v(env, V)
        Vn = Q.max(1)
        d = np.abs(Vn - V).max()
        deltas.append(d)
        V = Vn
        if d < tol:
            break
    policy = q_from_v(env, V).argmax(1)
    return V, policy, len(deltas)


def policy_evaluation(env, pi, tol=1e-12):
    """解线性方程组 V = r^π + γP^π V（(I−γP^π)V=r^π，L20 §1.2）。"""
    Ppi = env.P[np.arange(env.S), pi]                   # (S,S)：P^π[s,s']
    Rpi = env.R[np.arange(env.S), pi]                   # (S,S)：R^π[s,s']
    rpi = np.einsum("sj,sj->s", Ppi, Rpi)               # Σ_{s'} P^π R^π
    return np.linalg.solve(np.eye(env.S) - env.gamma * Ppi, rpi)


def policy_iteration(env, max_iter=50):
    pi = np.zeros(env.S, int)
    for it in range(max_iter):
        V = policy_evaluation(env, pi)
        newpi = q_from_v(env, V).argmax(1)
        if np.all(newpi == pi):
            return V, pi, it + 1
        pi = newpi
    return policy_evaluation(env, pi), pi, max_iter


def render(pi, env, title):
    arrows = {0: "^", 1: "v", 2: "<", 3: ">"}
    print(title)
    for r in range(env.h):
        line = ""
        for c in range(env.w):
            cell = (r, c)
            if GRID[r][c] == "#":
                line += " ██ "
            elif cell in env.terminals:
                line += "  " + ("+1 " if env.terminals[cell] > 0 else "-1 ")
            else:
                line += f"  {arrows[pi[env.idx[cell]]]}  "
        print(line)


def main():
    env = GridMDP()
    print("MDP 规模：|S|=%d, |A|=4, γ=%.2f, 打滑=%.0f%%"
          % (env.S, env.gamma, 100 * env.slip))
    V_vi, pi_vi, k_vi = value_iteration(env)
    V_pi, pi_pi, k_pi = policy_iteration(env)
    print(f"值迭代   ：{k_vi} 轮收敛，‖V*‖∞={np.abs(V_vi).max():.4f}")
    print(f"策略迭代 ：{k_pi} 轮收敛，评估用线性求解；‖V_vi−V_pi‖∞="
          f"{np.abs(V_vi - V_pi).max():.2e}（两法同解，L20 §1.3）")
    # 一致性验证：策略迭代中途任意 π 的 V^π ≤ V*（策略改进定理数值版）
    random_pi = np.random.default_rng(0).integers(0, 4, env.S)
    V_rand = policy_evaluation(env, random_pi)
    print(f"随机策略 V^π：max={V_rand.max():+.3f} min={V_rand.min():+.3f} "
          f"≤ V* 逐点成立：{np.all(V_rand <= V_vi + 1e-9)}")
    render(pi_vi, env, "最优策略（值迭代提取）：")
    print("→ 注意：远离终点处动作近乎无差别（折扣后收益≈0），"
          "贴近 ±1 出口才出现方向性；打滑使最优路径绕开墙与陷阱夹缝。")


if __name__ == "__main__":
    main()
