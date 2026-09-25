# -*- coding: utf-8 -*-
"""L13-L14 强化学习项目：同一 4x4 网格世界上的无模型 Q-Learning + 迷你策略梯度

运行:  python q_learning.py
对应 notes/L13-*.md (Q-learning) 与 notes/L14-*.md (REINFORCE).
环境定义与 projects/mdp 完全一致(代码自带一份以保独立运行) --
"模型未知也能逼近 L12 的答案" 是本项目的验证目标.
"""
import math
import random
from collections import defaultdict

# ---------------- 环境 (与 mdp 项目同构, 但 agent 不可见 T/R) ----------------
ROWS = COLS = 4
WALLS = {(1, 1), (2, 2)}
TERMINALS = {(0, 3): 10.0, (1, 3): -10.0}
STEP = -0.04
GAMMA = 0.95
ACTIONS = ["N", "S", "E", "W"]
DELTA = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
SIDE = {"N": ("W", "E"), "S": ("E", "W"), "E": ("N", "S"), "W": ("S", "N")}
START = (3, 0)


def next_state(state, action):
    r, c = state
    dr, dc = DELTA[action]
    n = (r + dr, c + dc)
    if 0 <= n[0] < ROWS and 0 <= n[1] < COLS and n not in WALLS:
        return n
    return state


def sample_step(state, action, rng):
    """按 0.8/0.1/0.1 采样一个 (s', r) 样本 -- agent 只能看到样本, 看不到分布."""
    a = rng.choices([action, SIDE[action][0], SIDE[action][1]], weights=[0.8, 0.1, 0.1])[0]
    s2 = next_state(state, a)
    r = STEP + (TERMINALS[s2] if s2 in TERMINALS else 0.0)
    return s2, r


# ---------------- "老师": 值迭代给出最优 V*/pi* (供对照) ----------------
ALL_STATES = [(r, c) for r in range(ROWS) for c in range(COLS)
              if (r, c) not in WALLS and (r, c) not in TERMINALS]


def q_star(V, state, action):
    total = 0.0
    for a, p in zip([action, SIDE[action][0], SIDE[action][1]], [0.8, 0.1, 0.1]):
        s2 = next_state(state, a)
        v_next = 0.0 if s2 in TERMINALS else V[s2]
        r = STEP + (TERMINALS[s2] if s2 in TERMINALS else 0.0)
        total += p * (r + GAMMA * v_next)
    return total


def solve_optimal():
    V = {s: 0.0 for s in ALL_STATES}
    for _ in range(1000):
        newV = {s: max(q_star(V, s, a) for a in ACTIONS) for s in ALL_STATES}
        if max(abs(newV[s] - V[s]) for s in ALL_STATES) < 1e-6:
            V = newV
            break
        V = newV
    pi = {s: max(ACTIONS, key=lambda a: q_star(V, s, a)) for s in ALL_STATES}
    return pi


# ---------------- Q-Learning (L13) ----------------
def q_learning(episodes=8000, alpha=0.1, epsilon=0.2, seed=188, log_every=2000):
    rng = random.Random(seed)
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    curve = []
    for ep in range(episodes):
        s = START
        for _ in range(200):                      # 步数上限: 防早期乱走不终止
            if rng.random() < epsilon:
                a = rng.choice(ACTIONS)
            else:
                a = max(Q[s], key=lambda x: Q[s][x])
            s2, r = sample_step(s, a, rng)
            best_next = 0.0 if s2 in TERMINALS else max(Q[s2].values())
            td = r + GAMMA * best_next - Q[s][a]  # TD 误差: 自举残差
            Q[s][a] += alpha * td
            if s2 in TERMINALS:
                break
            s = s2
        if (ep + 1) % log_every == 0:
            curve.append((ep + 1, eval_greedy(Q, 200, rng)))
    return Q, curve


def greedy_policy(Q):
    return {s: max(Q[s], key=lambda a: Q[s][a]) for s in ALL_STATES}


def eval_greedy(Q, n_eps, rng):
    win = 0
    for _ in range(n_eps):
        s = START
        for _ in range(200):
            if s in TERMINALS:
                break
            a = max(Q[s], key=lambda x: Q[s][x])
            s, _ = sample_step(s, a, rng)
        if s == (0, 3):
            win += 1
    return win / n_eps


# ---------------- REINFORCE 迷你示范 (L14, 语境化赌博机) ----------------
# 真实最优 (agent 未知): state0 下动作 0 更好, state1 下动作 1 更好
BANDIT = {0: (0.9, 0.4), 1: (0.3, 0.8)}


def softmax(vals):
    m = max(vals)
    e = [math.exp(v - m) for v in vals]
    z = sum(e)
    return [x / z for x in e]


def reinforce(steps=30000, alpha=0.05, seed=7):
    rng = random.Random(seed)
    theta = {0: [0.0, 0.0], 1: [0.0, 0.0]}
    b = 0.5                                   # 移动平均 baseline (降方差)
    for _ in range(steps):
        s = rng.choice([0, 1])
        probs = softmax(theta[s])
        a = 0 if rng.random() < probs[0] else 1
        r = 1.0 if rng.random() < BANDIT[s][a] else 0.0
        adv = r - b
        b += 0.01 * (r - b)
        # softmax 参数化的单样本策略梯度:
        # dlog pi(a|s)/d theta_act = 1[act==a] - pi(act|s)
        for act in (0, 1):
            dlog = (1.0 if act == a else 0.0) - probs[act]
            theta[s][act] += alpha * adv * dlog
    return {s: softmax(theta[s]) for s in theta}


def main():
    pi_star = solve_optimal()
    print("=" * 60)
    print("Part 1  Q-Learning (模型未知) vs 值迭代最优策略 (L12/L13)")
    Q, curve = q_learning()
    pi_q = greedy_policy(Q)
    same = sum(1 for s in pi_star if pi_star[s] == pi_q[s])
    print(f"训练 8000 episodes (alpha=0.1, eps=0.2, gamma=0.95)")
    print(f"贪心策略与最优策略一致状态数: {same}/{len(pi_star)}")
    print(f"纯贪心评估胜率达 +10 概率: {eval_greedy(Q, 500, random.Random(1)):.1%}")
    for n, w in curve:
        print(f"  ep {n:>5}: 中期胜率 {w:.1%}")
    print("\nQ 表片段 (起点行):")
    for s in [(3, 0), (3, 1), (3, 2), (3, 3)]:
        qs = Q[s]
        print(f"  s={s}: " + "  ".join(f"Q[{a}]={qs[a]:+.2f}" for a in ACTIONS))

    print("\n" + "=" * 60)
    print("Part 2  REINFORCE 语境化赌博机 (L14: 策略梯度/基线)")
    probs = reinforce()
    print("learned pi(a=0|s):  s0 -> {:.2f} (最优 1.0)   s1 -> {:.2f} (最优 0.0)".format(
        probs[0][0], probs[1][0]))
    print("讨论: 无梯度可导的环境用采样回报乘 logπ 梯度; baseline 只降方差不改期望.")


if __name__ == "__main__":
    main()
