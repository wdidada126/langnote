# -*- coding: utf-8 -*-
"""L12 MDP 项目：4x4 网格世界的值迭代与策略迭代（纯标准库）

运行:  python grid_mdp.py
对应 notes/L12-MDP-值迭代与策略迭代.md (官方 Pacman P2/P3 的合成环境版)

世界定义:
  16 格 4x4; 墙 (1,1),(2,2); 终点 (0,3)=+10, (1,3)=-10;
  动作 N/S/E/W: 0.8 按意图, 0.1/0.1 向左/右滑移(碰墙原地); 步代价 -0.04; gamma=0.95.
输出:
  值迭代收敛过程、V* 表、贪心提取的最优策略;
  策略迭代独立求解, 与 VI 策略比对一致性.
"""
import random

ROWS = COLS = 4
WALLS = {(1, 1), (2, 2)}
TERMINALS = {(0, 3): 10.0, (1, 3): -10.0}
STEP = -0.04
GAMMA = 0.95
ACTIONS = ["N", "S", "E", "W"]
DELTA = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
# 侧滑: 意图动作 -> (左, 右)
SIDE = {"N": ("W", "E"), "S": ("E", "W"), "E": ("N", "S"), "W": ("S", "N")}
PROBS = (0.8, 0.1, 0.1)


def all_states():
    return [(r, c) for r in range(ROWS) for c in range(COLS)
            if (r, c) not in WALLS and (r, c) not in TERMINALS]


def next_state(state, action):
    r, c = state
    dr, dc = DELTA[action]
    n = (r + dr, c + dc)
    if 0 <= n[0] < ROWS and 0 <= n[1] < COLS and n not in WALLS:
        return n
    return state


def transitions(state, action):
    """返回 [(s', prob)]: 意图 0.8 + 左右滑移各 0.1, 合并同终点概率(碰墙=原地)."""
    out = {}
    for p, act in zip(PROBS, (action, SIDE[action][0], SIDE[action][1])):
        s2 = next_state(state, act)
        out[s2] = out.get(s2, 0.0) + p
    return list(out.items())


def reward_for(s2):
    """进入 s' 的即时奖励: 步代价 + 终端值."""
    return STEP + (TERMINALS[s2] if s2 in TERMINALS else 0.0)


def q_value(V, state, action):
    total = 0.0
    for s2, p in transitions(state, action):
        v_next = 0.0 if s2 in TERMINALS else V[s2]
        total += p * (reward_for(s2) + GAMMA * v_next)
    return total


def best_action(V, state):
    return max(ACTIONS, key=lambda a: q_value(V, state, a))


def value_iteration():
    states = all_states()
    V = {s: 0.0 for s in states}
    deltas = []
    for it in range(1000):
        delta = 0.0
        newV = dict(V)
        for s in states:
            newV[s] = max(q_value(V, s, a) for a in ACTIONS)
            delta = max(delta, abs(newV[s] - V[s]))
        V = newV
        deltas.append(delta)
        if delta < 1e-6:
            break
    return V, it + 1


def policy_extraction(V):
    return {s: best_action(V, s) for s in all_states()}


def policy_evaluation(pi):
    states = all_states()
    V = {s: 0.0 for s in states}
    for _ in range(2000):
        delta = 0.0
        newV = dict(V)
        for s in states:
            a = pi[s]
            newV[s] = q_value(V, s, a)
            delta = max(delta, abs(newV[s] - V[s]))
        V = newV
        if delta < 1e-6:
            break
    return V


def policy_iteration():
    pi = {s: random.Random(7).choice(ACTIONS) for s in all_states()}
    for it in range(100):
        V = policy_evaluation(pi)
        stable = True
        for s in all_states():
            a2 = best_action(V, s)
            if a2 != pi[s]:
                pi[s] = a2
                stable = False
        if stable:
            return pi, it + 1
    return pi, 100


def grid_str(getter, width):
    lines = []
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            s = (r, c)
            if s in WALLS:
                t = "#####"
            elif s in TERMINALS:
                t = f"{TERMINALS[s]:+.0f}".center(5)
            else:
                t = str(getter(s)).center(width)
            cells.append(f"{t}|")
        lines.append("".join(cells))
    return "\n".join(lines)


def main():
    print("世界: P=起点建议(3,0); 墙=#####; 数字=终端")
    V, iters = value_iteration()
    print(f"\n[值迭代] 收敛于 {iters} 次迭代, 示例 V*(3,0)={V[(3, 0)]:.3f}")
    print("V* 表 (行=坐标 r, 列=c):")
    print(grid_str(lambda s: f"{V[s]:+.2f}", 5))
    pi = policy_extraction(V)
    print("\n最优策略 (VI 贪心提取):")
    print(grid_str(lambda s: pi[s], 1))

    pi2, it2 = policy_iteration()
    print(f"\n[策略迭代] 收敛于 {it2} 轮改进")
    print("策略迭代最优策略:")
    print(grid_str(lambda s: pi2[s], 1))
    same = sum(1 for s in pi if pi[s] == pi2[s])
    print(f"VI 与 PI 策略一致状态数: {same}/{len(pi)}")
    print("讨论: 滑移使边界格 '贴着陷阱' 动作被放弃 -- 风险规避来自模型本身(笔记 L12).")


if __name__ == "__main__":
    main()
