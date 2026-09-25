"""p10 NP 完全体验（衔接 6.046/CS170；本课 L13 证明素养 + L08 DP + L09 图）。

3-SAT：暴力枚举 vs 回溯 DPLL（单元传播）——在随机 3-CNF 上观察
子句密度 α=m/n 跨过阈值 4.26 时的求解代价尖峰。
TSP：Held-Karp 位掩码 DP 精确解 vs 最近邻 vs MST-加倍 2-近似，
实测近似比始终 ≤ 2（经验上远小于）。
"""
import itertools
import math
import random


# ---------------- 3-SAT ----------------
def sat_brute(n_vars, clauses):
    for assign in itertools.product([False, True], repeat=n_vars):
        if all(any((assign[abs(l) - 1] if l > 0 else not assign[abs(l) - 1])
                   for l in cl) for cl in clauses):
            return assign
    return None


def sat_dpll(n_vars, clauses):
    """带回溯的 DPLL（单元传播 + 首子句分支），回溯节点数计入 sat_dpll.nodes。"""
    clauses = [tuple(c) for c in clauses]
    stats = [0]

    def value(lit, env):
        v = env.get(abs(lit))
        return None if v is None else (v if lit > 0 else not v)

    def simplify(cs, env):
        out = []
        for cl in cs:
            if any(value(l, env) is True for l in cl):
                continue                      # 已满足
            rest = tuple(l for l in cl if value(l, env) is None)
            if not rest:
                return None                   # 全假: 冲突
            out.append(rest)
        return out

    def solve(cs, env):
        stats[0] += 1
        cs = simplify(cs, env)
        if cs is None:
            return None
        while cs:                             # 单元传播到不动点
            units = [cl[0] for cl in cs if len(cl) == 1]
            if not units:
                break
            env = dict(env)
            for l in units:
                env[abs(l)] = l > 0
            cs = simplify(cs, env)
            if cs is None:
                return None
        if not cs:
            return env
        lit = cs[0][0]                        # 分支
        for val in (True, False):
            e2 = dict(env)
            e2[abs(lit)] = val if lit > 0 else not val
            r = solve(cs, e2)
            if r is not None:
                return r
        return None

    env = solve(clauses, {})
    sat_dpll.nodes = stats[0]
    if env is None:
        return None
    return tuple(env.get(i, False) for i in range(1, n_vars + 1))


def random_3cnf(n, m, rnd):
    clauses = []
    for _ in range(m):
        vs = rnd.sample(range(1, n + 1), 3)
        clauses.append(tuple(v if rnd.random() < 0.5 else -v for v in vs))
    return clauses


# ---------------- TSP ----------------
def tour_len(order, d):
    return sum(d[a][b] for a, b in zip(order, order[1:])) + d[order[-1]][order[0]]


def tsp_exact_dp(d):
    """Held-Karp: O(2^n n²)。返回 (最优长度, 环路)。"""
    n = len(d)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    par = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF or not (mask >> u) & 1:
                continue
            for v in range(n):
                if (mask >> v) & 1:
                    continue
                nmask = mask | (1 << v)
                nd = dp[mask][u] + d[u][v]
                if nd < dp[nmask][v]:
                    dp[nmask][v] = nd
                    par[nmask][v] = u
    full = (1 << n) - 1
    best, last = INF, -1
    for u in range(1, n):
        val = dp[full][u] + d[u][0]
        if val < best:
            best, last = val, u
    order, mask, u = [], full, last
    while u != -1:
        order.append(u)
        p = par[mask][u]
        mask ^= (1 << u)
        u = p
    return best, list(reversed(order))


def tsp_nearest_neighbor(d, start=0):
    n = len(d)
    unvisited = set(range(1, n))
    order, cur = [start], start
    while unvisited:
        nxt = min(unvisited, key=lambda v: d[cur][v])
        order.append(nxt); unvisited.discard(nxt); cur = nxt
    return order


def tsp_mst_double(d):
    """Prim MST + DFS 前序 + 短路：度量 TSP 的 2-近似。"""
    n = len(d)
    in_tree = [False] * n
    key = [float('inf')] * n
    parent = [-1] * n
    key[0] = 0
    adj = [[] for _ in range(n)]
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i]), key=lambda i: key[i])
        in_tree[u] = True
        if parent[u] != -1:
            adj[u].append(parent[u]); adj[parent[u]].append(u)
        for v in range(n):
            if not in_tree[v] and d[u][v] < key[v]:
                key[v] = d[u][v]
                parent[v] = u
    order, stack = [], [0]
    seen = {0}
    while stack:
        u = stack.pop()
        order.append(u)
        for v in sorted(adj[u], reverse=True):
            if v not in seen:
                seen.add(v); stack.append(v)
    return order


def euclid_dist_matrix(pts, rnd=None):
    n = len(pts)
    return [[math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
             for j in range(n)] for i in range(n)]


# ---------------- 自测与实验 ----------------
def self_test():
    rnd = random.Random(17)
    for _ in range(40):
        n = rnd.randint(2, 6)
        m = rnd.randint(1, 12)
        cls = random_3cnf(n, m, rnd)
        b = sat_brute(n, cls)
        g = sat_dpll(n, cls)
        assert (b is None) == (g is None), (cls, b, g)
        if g is not None:
            assert all(any((g[abs(l) - 1] if l > 0 else not g[abs(l) - 1]) for l in cl)
                       for cl in cls), 'DPLL 解校验失败'
    print('SAT 自测通过：40 组随机公式，暴力与 DPLL 可满足性判定一致、赋值合法。')

    rnd = random.Random(21)
    for _ in range(25):
        n = rnd.randint(4, 9)
        pts = [(rnd.uniform(0, 100), rnd.uniform(0, 100)) for _ in range(n)]
        d = euclid_dist_matrix(pts)
        opt, _ = tsp_exact_dp(d)
        nn = tour_len(tsp_nearest_neighbor(d), d)
        mst = tour_len(tsp_mst_double(d), d)
        assert nn >= opt - 1e-9 and mst >= opt - 1e-9
        assert mst <= 2 * opt + 1e-9, (mst, opt)   # 2-近似理论界实测成立
    print('TSP 自测通过：25 组随机欧氏点集，NN/MST 加倍均 ≥ 最优且 MST 加倍 ≤ 2×最优。')


def experiment_sat():
    print('== 随机 3-SAT 易/难相变（n=14，各密度 60 样本） ==')
    n = 14
    print(f"{'α=m/n':>6} | {'可满足率':>8} | {'DPLL 平均节点数':>14}")
    for alpha in (2.5, 3.5, 4.0, 4.25, 4.5, 5.0, 6.0):
        m = int(alpha * n)
        sat_rate, nodes = 0, []
        for t in range(60):
            rnd = random.Random(1000 + t)
            cls = random_3cnf(n, m, rnd)
            r = sat_dpll(n, cls)
            nodes.append(sat_dpll.nodes)
            sat_rate += r is not None
        print(f"{alpha:6.2f} | {sat_rate / 60:8.2f} | {sum(nodes) / len(nodes):14.1f}")
    print('（可满足率在 α≈4.26 处从 1 跌到 0，DPLL 代价在其附近达峰——硬件/调度求解器的痛点。）')


def experiment_tsp():
    print('== TSP 近似比实测（欧氏随机点, 每组 20 样本） ==')
    print(f"{'n':>4} | {'最优(HK)':>9} | {'NN/最优':>8} | {'MST2/最优':>9}")
    for n in (8, 10, 12):
        r1 = r2 = 0.0
        for t in range(20):
            rnd = random.Random(77 + t)
            pts = [(rnd.uniform(0, 100), rnd.uniform(0, 100)) for _ in range(n)]
            d = euclid_dist_matrix(pts)
            opt, _ = tsp_exact_dp(d)
            r1 += tour_len(tsp_nearest_neighbor(d), d) / opt
            r2 += tour_len(tsp_mst_double(d), d) / opt
        print(f"{n:4d} | {opt:9.2f} | {r1 / 20:8.3f} | {r2 / 20:9.3f}")
    print('（经验比 1.1–1.2，理论保证 NN 无界 / MST 加倍 ≤2 —— "经验好"≠"有保证"。）')


if __name__ == '__main__':
    self_test()
    experiment_sat()
    experiment_tsp()
