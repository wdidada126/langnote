"""p09 最大流（Edmonds-Karp，衔接 6.046 L8-L9；本课 L09-L11 的 BFS/增广应用）。

残量网络 + BFS 选最短增广路（Edmonds-Karp 多项式界）；从最终残量图提取
S-T 最小割并验证容量 == 流量（最大流最小割定理的"割即证书"）。
归约应用：二分图最大匹配（源→L→R→汇，容量 1）。
"""
import random
from collections import deque
from itertools import combinations


class FlowNetwork:
    def __init__(self):
        self.cap = {}                      # (u, v) -> 残量（反向边以 0 起步）

    def add_edge(self, u, v, c):
        self.cap[(u, v)] = self.cap.get((u, v), 0) + c
        self.cap.setdefault((v, u), 0)

    def nodes(self):
        ns = set()
        for u, v in self.cap:
            ns.add(u); ns.add(v)
        return ns

    def _bfs_augment(self, s, t):
        parent = {s: None}
        q = deque([s])
        while q:
            u = q.popleft()
            for (a, b), c in self.cap.items():
                if a == u and c > 0 and b not in parent:
                    parent[b] = u
                    if b == t:
                        return parent
                    q.append(b)
        return None

    def max_flow(self, s, t):
        flow = 0
        while True:
            parent = self._bfs_augment(s, t)
            if parent is None:
                return flow
            bottleneck, v = float('inf'), t
            while v != s:
                u = parent[v]
                bottleneck = min(bottleneck, self.cap[(u, v)])
                v = u
            v = t
            while v != s:
                u = parent[v]
                self.cap[(u, v)] -= bottleneck
                self.cap[(v, u)] += bottleneck
                v = u
            flow += bottleneck

    def min_cut(self, s):
        """在最终残量图上从 s BFS 可达集 S；割 = {(u,v)∈E0原边: u∈S, v∉S}。
        注意：需在 max_flow 前备份原始边集。"""
        seen = {s}
        q = deque([s])
        while q:
            u = q.popleft()
            for (a, b), c in self.cap.items():
                if a == u and c > 0 and b not in seen:
                    seen.add(b); q.append(b)
        return seen


# ---------------- 暴力参考：枚举所有 s-t 割 ----------------
def brute_min_cut(edges, s, t):
    """edges: list[(u,v,c)]。返回最小割容量与割集。"""
    verts = set()
    for u, v, _ in edges:
        verts.add(u); verts.add(v)
    others = sorted(verts - {s, t})
    best = float('inf')
    best_cut = None
    for r in range(len(others) + 1):
        for subset in combinations(others, r):
            S = {s} | set(subset)
            cap = sum(c for u, v, c in edges if u in S and v not in S)
            if cap < best:
                best, best_cut = cap, S
    return best, best_cut


def make_net(edges):
    g = FlowNetwork()
    for u, v, c in edges:
        g.add_edge(u, v, c)
    return g


# ---------------- 二分图匹配归约 ----------------
def bipartite_matching(L, R, pairs):
    g = FlowNetwork()
    for u in L:
        g.add_edge('s', 'L' + str(u), 1)
    for v in R:
        g.add_edge('R' + str(v), 't', 1)
    for u, v in pairs:
        g.add_edge('L' + str(u), 'R' + str(v), 1)
    return g.max_flow('s', 't')


def matching_brute(pairs):
    Ls = sorted({u for u, _ in pairs}); Rs = sorted({v for _, v in pairs})
    best = 0
    for r in range(min(len(Ls), len(Rs)) + 1):
        for ls in combinations(Ls, r):
            for rs in combinations(Rs, r):
                for perm in permutations_local(rs):
                    if all((l, p) in pairs for l, p in zip(ls, perm)):
                        best = max(best, r)
        if best == min(len(Ls), len(Rs)):
            return best
    return best


def permutations_local(seq):
    if not seq:
        yield ()
        return
    import itertools
    yield from itertools.permutations(seq)


# ---------------- 自测与实验 ----------------
def self_test():
    # CLRS 图 26.1 经典例（v1..v4 记作 a..d）：最大流 23
    edges = [('s', 'a', 16), ('s', 'b', 13), ('a', 'b', 10), ('a', 'c', 12),
             ('b', 'a', 4), ('b', 'd', 14), ('c', 'b', 9), ('c', 't', 20),
             ('d', 'c', 7), ('d', 't', 4)]
    g = make_net(edges)
    f = g.max_flow('s', 't')
    assert f == 23, f
    S = g.min_cut('s')
    cut_cap = sum(c for u, v, c in edges if u in S and v not in S)
    assert cut_cap == f == 23, (S, cut_cap, f)   # 最小割 {a→c 12, d→c 7, d→t 4}
    print(f'CLRS 例: 最大流 {f} = 最小割容量 {cut_cap}, S={sorted(S)}（割即证书）。')

    rnd = random.Random(3)
    for _ in range(80):
        n = rnd.randint(3, 6)
        vs = [f'v{i}' for i in range(n)]
        edges = []
        for u, v in combinations(vs, 2):
            if rnd.random() < 0.55:
                edges.append((u, v, rnd.randint(1, 9)))
        s, t = vs[0], vs[-1]
        g = make_net(edges)
        f = g.max_flow(s, t)
        bc, _ = brute_min_cut(edges, s, t)
        assert f == bc, (edges, f, bc)
    print('随机网络自测通过：80 组 Edmonds-Karp 与暴力枚举最小割逐一相等。')

    pairs = {(0, 0), (0, 1), (1, 1), (2, 2), (3, 2), (3, 3)}
    m = bipartite_matching([0, 1, 2, 3], [0, 1, 2, 3], pairs)
    assert m == matching_brute(pairs) == 4, m
    print(f'二分图匹配（最大流归约）= {m}，与暴力一致。')


def experiment():
    rnd = random.Random(55)
    print('== 增广次数与网络结构（BFS 最短路增广: O(VE²) 上界很松） ==')
    print(f"{'V':>4} | {'E':>4} | {'最大流':>6} | {'增广次数':>8} | {'增广/|E|':>8}")
    for v_n in (8, 14, 20):
        for trial in range(3):
            vs = list(range(v_n))
            edges = []
            for u in vs:
                for w in vs:
                    if u < w and rnd.random() < 0.4:
                        edges.append((u, w, rnd.randint(1, 20)))
            g = make_net(edges)
            count = [0]
            orig_bfs = g._bfs_augment
            def bfs(s, t, _o=orig_bfs, _c=count):
                r = _o(s, t)
                if r is not None:
                    _c[0] += 1
                return r
            g._bfs_augment = bfs
            f = g.max_flow(0, v_n - 1)
            m = len(edges)
            print(f"{v_n:4d} | {m:4d} | {f:6d} | {count[0]:8d} | {count[0] / max(m, 1):8.2f}")
    print('（增广次数 ~ O(VE) 远小于 E² 界；每次增广的 BFS 本身 O(E)。）')


if __name__ == '__main__':
    self_test()
    experiment()
