"""p06 动态规划（L08）：编辑距离 / 矩阵链乘法 / 0-1 背包 + Fibonacci 四写法。

统一模板：状态 → 转移 → 边界/顺序 → 计数（状态数 × 转移成本）；
小实例全部与暴力枚举对拍，验证"DP 保留所有子问题解"的正确性。
"""
import functools
import itertools
import random


# ---------------- Fibonacci 四种写法（调用计数版） ----------------
def fib_naive(n, stats):
    stats[0] += 1
    if n < 2:
        return n
    return fib_naive(n - 1, stats) + fib_naive(n - 2, stats)


def fib_memo(n, stats):
    @functools.lru_cache(maxsize=None)
    def f(i):
        stats[0] += 1
        return i if i < 2 else f(i - 1) + f(i - 2)
    return f(n)


def fib_tab(n, stats):
    stats[0] = n + 1
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ---------------- 编辑距离（含回溯） ----------------
def edit_distance(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # 删
                                   dp[i][j - 1],      # 插
                                   dp[i - 1][j - 1])  # 改
    # 回溯一条最优操作序列
    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s[i - 1] == t[j - 1]:
            ops.append('match'); i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f'delete {s[i - 1]}'); i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            ops.append(f'insert {t[j - 1]}'); j -= 1
        else:
            ops.append(f'replace {s[i - 1]}->{t[j - 1]}'); i -= 1; j -= 1
    return dp[m][n], list(reversed(ops))


def edit_distance_brute(s, t):
    """自顶向下 memo 递归参考实现（与自底向上表法互相印证）。"""
    @functools.lru_cache(maxsize=None)
    def rec(a, b):
        if not a:
            return len(b)
        if not b:
            return len(a)
        if a[-1] == b[-1]:
            return rec(a[:-1], b[:-1])
        return 1 + min(rec(a[:-1], b), rec(a, b[:-1]), rec(a[:-1], b[:-1]))
    ans = rec(s, t)
    rec.cache_clear()
    return ans


# ---------------- 矩阵链乘法 ----------------
def matrix_chain(dims):
    """dims = [p0, p1, ..., pn]，矩阵 A_i 维数 dims[i-1]×dims[i]（1-index 习惯）。"""
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):            # 区间 DP：按链长递增填表
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k
    def parenthesize(i, j):
        if i == j:
            return f'A{i}'
        k = s[i][j]
        return f'({parenthesize(i, k)}·{parenthesize(k + 1, j)})'
    return m[1][n], parenthesize(1, n)


def matrix_chain_brute(dims):
    n = len(dims) - 1
    memo = {}
    def rec(i, j):
        if i == j:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        best = min(rec(i, k) + rec(k + 1, j)
                   + dims[i - 1] * dims[k] * dims[j] for k in range(i, j))
        memo[(i, j)] = best
        return best
    return rec(1, n)


# ---------------- 0-1 背包 ----------------
def knapsack01(weights, values, cap):
    n = len(weights)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = weights[i - 1], values[i - 1]
        for c in range(cap + 1):
            dp[i][c] = dp[i - 1][c]
            if wi <= c and dp[i - 1][c - wi] + vi > dp[i][c]:
                dp[i][c] = dp[i - 1][c - wi] + vi
    # 重构方案
    take, c = [], cap
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            take.append(i - 1)
            c -= weights[i - 1]
    return dp[n][cap], sorted(take, reverse=True)


def knapsack_brute(weights, values, cap):
    best = 0
    for r in range(len(weights) + 1):
        for comb in itertools.combinations(range(len(weights)), r):
            w = sum(weights[i] for i in comb)
            if w <= cap:
                best = max(best, sum(values[i] for i in comb))
    return best


# ---------------- 自测与实验 ----------------
def self_test():
    assert edit_distance('kitten', 'sitting')[0] == 3
    dist, ops = edit_distance('abc', 'yabd')
    assert dist == 2, dist
    rnd = random.Random(11)
    for _ in range(60):
        a = ''.join(rnd.choice('abcd') for _ in range(rnd.randint(0, 8)))
        b = ''.join(rnd.choice('abcd') for _ in range(rnd.randint(0, 8)))
        d, ops = edit_distance(a, b)
        assert d == edit_distance_brute(a, b), (a, b)
        assert sum(1 for o in ops if o != 'match') == d, (a, b, ops)
    print('编辑距离自测通过：60 组随机串与 memo 递归参考一致、操作数=距离。')

    rnd = random.Random(12)
    for _ in range(40):
        n = rnd.randint(1, 7)
        dims = [rnd.randint(2, 40) for _ in range(n + 1)]
        v, scheme = matrix_chain(dims)
        assert v == matrix_chain_brute(dims), dims
    print('矩阵链自测通过：40 组随机维数与暴力 memo 一致；示例方案:',
          matrix_chain([10, 20, 30, 40, 30])[1])

    rnd = random.Random(13)
    for _ in range(60):
        n = rnd.randint(1, 12)
        weights = [rnd.randint(1, 20) for _ in range(n)]
        values = [rnd.randint(1, 100) for _ in range(n)]
        cap = rnd.randint(1, 60)
        best, take = knapsack01(weights, values, cap)
        assert best == knapsack_brute(weights, values, cap), (weights, cap)
        assert sum(weights[i] for i in take) <= cap
        assert sum(values[i] for i in take) == best
    print('背包自测通过：60 组随机实例与子集暴力一致，方案重构合法。')


def experiment():
    print('== Fibonacci 调用次数：指数 vs 线性（L08 核心对照） ==')
    print(f"{'n':>5} | {'裸递归调用数':>14} | {'memo 调用数':>12} | 比值")
    for n in (10, 15, 20, 24, 28):
        s1 = [0]; r1 = fib_naive(n, s1)
        s2 = [0]; r2 = fib_memo(n, s2)
        assert r1 == r2 == fib_tab(n, [0])
        print(f"{n:5d} | {s1[0]:14d} | {s2[0]:12d} | {s1[0] / max(s2[0], 1):10.1f}")
    print('（memo 版只计"未命中缓存"的调用 = 状态数 n+1，Θ(n)；裸递归 ≈ 2·fib(n+1)−1 指数。）')
    print()
    print('== DP 表的复杂度实测：编辑距离 Θ(mn) ==')
    for n in (200, 400, 800):
        a = 'x' * n; b = 'y' * n
        import time
        t0 = time.perf_counter()
        d, _ = edit_distance(a, b)
        dt = time.perf_counter() - t0
        print(f"n={n:4d}: 单元格 {n * n:8d}, 耗时 {dt * 1000:7.2f} ms, ms/百万格 {dt * 1e9 / (n * n):7.1f}")


if __name__ == '__main__':
    self_test()
    experiment()
