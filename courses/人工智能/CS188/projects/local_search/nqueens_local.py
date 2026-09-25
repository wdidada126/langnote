# -*- coding: utf-8 -*-
"""L04 局部搜索项目：n-皇后 随机重启爬山 与 模拟退火（纯标准库）

运行:  python nqueens_local.py
对应 notes/L04-局部搜索-爬山与模拟退火.md

设计:
  state[i] = 第 i 列皇后所在行 (每列恰一皇后 => 无列冲突, 行/对角冲突计入值);
  值 = -冲突数(爬山取大), 等价于冲突数最小化.
  增量评估: 移动 col 列皇后只有 (col, j) 对变化 => O(n) 更新 (6.006 增量视角).
  HC : 最陡爬山(枚举全部 n*(n-1) 邻居) + 随机重启;
  SA : Metropolis 准则 P = exp(-delta/T), 几何冷却 T *= alpha.
"""
import math
import random


def col_conflicts(state, col):
    """涉及 col 列的冲突数(行相同 或 对角 |dr|==|dc|)."""
    n = len(state)
    total = 0
    r = state[col]
    for j in range(n):
        if j == col:
            continue
        if state[j] == r or abs(state[j] - r) == abs(j - col):
            total += 1
    return total


def conflicts(state):
    return sum(col_conflicts(state, c) for c in range(len(state))) // 2


def random_state(n, rng):
    return [rng.randrange(n) for _ in range(n)]


def hill_climb(n, rng, max_steps=5000):
    """最陡爬山. 返回 (state, 步数)."""
    state = random_state(n, rng)
    steps = 0
    while steps < max_steps:
        cur = conflicts(state)
        if cur == 0:
            return state, steps
        best = None
        for col in range(n):
            base = cur - col_conflicts(state, col)
            old = state[col]
            for row in range(n):
                if row == old:
                    continue
                state[col] = row
                c = base + col_conflicts(state, col)
                if c < cur and (best is None or c < best[0]):
                    best = (c, col, row)
                state[col] = old
        if best is None:
            return state, steps              # 局部极小
        _, col, row = best
        state[col] = row
        steps += 1
    return state, steps


def random_restart_hc(n, restarts, rng):
    """SIDA: 随机重启爬山. 返回 (成功率, 成功时平均步数)."""
    ok, step_sum = 0, 0
    for _ in range(restarts):
        state, steps = hill_climb(n, rng)
        if conflicts(state) == 0:
            ok += 1
            step_sum += steps
    return ok / restarts, (step_sum / ok if ok else float("nan"))


def simulated_annealing(n, rng, max_steps=100000):
    """SA 冲突最小化: t0 随 n 缩放, 几何冷却. 返回 (best_state, 步数)."""
    state = random_state(n, rng)
    cur = conflicts(state)
    best, best_c = list(state), cur
    T, t_end, alpha = max(4.0, n / 2.0), 0.02, 0.997
    steps = 0
    while steps < max_steps and T > t_end:
        col = rng.randrange(n)
        row = rng.randrange(n)
        if row == state[col]:
            T *= alpha
            continue
        old = state[col]
        old_c = col_conflicts(state, col)
        state[col] = row
        delta = col_conflicts(state, col) - old_c   # 总冲突增量 = 该列冲突增量
        if delta < 0 or rng.random() < math.exp(-max(delta, 0) / T):
            cur += delta
            if cur < best_c:
                best, best_c = list(state), cur
            if best_c == 0:
                return best, steps + 1
        else:
            state[col] = old                     # 拒绝: 撤销移动
        T *= alpha
        steps += 1
    return best, steps


def show(state):
    n = len(state)
    return "\n".join(
        "".join("Q" if state[c] == r else "." for c in range(n))
        for r in range(n)
    )


def main():
    rng = random.Random(188)
    print("=" * 60)
    print("n-皇后: 随机重启爬山(HC) vs 模拟退火(SA)   值=冲突数")
    print(f"{'n':<6}{'HC成功率':<12}{'HC均步数':<12}{'SA成功率':<12}{'SA均步数':<12}")
    for n in (8, 12, 20):
        tr = 20 if n <= 12 else 10
        hc_rate, hc_avg = random_restart_hc(n, tr, rng)
        sa_ok, sa_steps_sum = 0, 0
        for _ in range(tr):
            best, steps = simulated_annealing(n, rng)
            if conflicts(best) == 0:
                sa_ok += 1
                sa_steps_sum += steps
        sa_rate = sa_ok / tr
        sa_avg = sa_steps_sum / sa_ok if sa_ok else float("nan")
        print(f"{n:<6}{hc_rate:<12.1%}{hc_avg:<12.0f}{sa_rate:<12.1%}{sa_avg:<12.0f}")

    print("\n示例: 20-皇后 SA 求得的解:")
    best, steps = simulated_annealing(20, random.Random(42))
    print(f"步数={steps}, 最终冲突={conflicts(best)}")
    print(show(best))
    print("观察: n 增大 HC 成功率骤降(局部极小), SA 靠温度接受劣移动逃离 (笔记 L04).")


if __name__ == "__main__":
    main()
