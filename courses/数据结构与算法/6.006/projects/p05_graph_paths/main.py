"""p05 图遍历与最短路（L09-L11）：BFS / DFS / 拓扑排序 / Dijkstra / Bellman-Ford。

图：邻接表 dict[str, list[(v, w)]]。网格图 + "路网"模拟（4/8 邻域随机权 + 少量长距捷径）。
实验：无权网格上 Dijkstra == BFS；非负路网上 Dijkstra == Bellman-Ford；负环检出。
"""
import heapq
import random
from collections import deque


class Graph:
    def __init__(self, directed=True):
        self.adj = {}
        self.directed = directed

    def add_edge(self, u, v, w=1.0):
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, [])
        if not self.directed:
            self.adj[v].append((u, w))

    def nodes(self):
        return list(self.adj)


# ---------------- 遍历 ----------------
def dfs_iter(g, s):
    order, seen, stack = [], set(), [s]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        for v, _ in reversed(g.adj[u]):
            if v not in seen:
                stack.append(v)
    return order


def bfs(g, s):
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v, _ in g.adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def connected_components(g):
    seen, comps = set(), []
    for s in g.nodes():
        if s in seen:
            continue
        comp = bfs(g, s)
        seen.update(comp)
        comps.append(sorted(comp))
    return comps


def topological_sort(g):
    indeg = {u: 0 for u in g.nodes()}
    for u in g.nodes():
        for v, _ in g.adj[u]:
            indeg[v] += 1
    q = deque(sorted(u for u, d in indeg.items() if d == 0))
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in g.adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(indeg):
        raise ValueError('graph has a cycle')
    return order


# ---------------- 最短路 ----------------
def dijkstra(g, s):
    dist = {s: 0.0}
    pq = [(0.0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float('inf')):
            continue                          # 惰性删除（L11）
        for v, w in g.adj[u]:
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def bellman_ford(g, s):
    dist = {u: float('inf') for u in g.nodes()}
    dist[s] = 0.0
    edges = [(u, v, w) for u in g.nodes() for (v, w) in g.adj[u]]
    n = len(dist)
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:                     # 第 n 轮还能松弛 ⇒ 负环可达
        if dist[u] + w < dist[v]:
            return None
    return dist


# ---------------- 合成数据 ----------------
def grid_graph(rows, cols, weights=None, rng=None, eight=False):
    g = Graph(directed=False)
    for r in range(rows):
        for c in range(cols):
            u = (r, c)
            nbrs = [(r + 1, c), (r, c + 1)]
            if eight:
                nbrs += [(r + 1, c + 1), (r + 1, c - 1)]
            for v in nbrs:
                if 0 <= v[0] < rows and 0 <= v[1] < cols:
                    w = 1.0 if weights is None else rng.choice(weights)
                    g.add_edge(u, v, w)
    return g


def road_network(rows, cols, seed=1):
    """网格 + 指数权 + 随机高速捷径：近似路网。"""
    rng = random.Random(seed)
    g = Graph(directed=False)
    base = grid_graph(rows, cols, weights=[1, 1, 2, 3, 5, 8], rng=rng, eight=True)
    g.adj = base.adj
    for _ in range((rows + cols) // 3):
        a = (rng.randrange(rows), rng.randrange(cols))
        b = (rng.randrange(rows), rng.randrange(cols))
        if a != b:
            g.add_edge(a, b, 1)               # 捷径: 跨距大但权小
    return g


# ---------------- 自测与实验 ----------------
def self_test():
    # 小图手算例
    g = Graph(directed=True)
    for u, v, w in [('a', 'b', 7), ('a', 'c', 9), ('c', 'f', 2), ('b', 'c', 10),
                    ('b', 'd', 15), ('d', 'f', 6), ('c', 'e', 11), ('e', 'f', 2)]:
        g.add_edge(u, v, w)
    d = dijkstra(g, 'a')
    # 手算: a=0, b=7, c=9, f=9+2=11, e=9+11=20, d=7+15=22
    assert d['f'] == 11 and d['e'] == 20 and d['c'] == 9 and d['d'] == 22, '经典 6 点例'
    assert bellman_ford(g, 'a') == d
    # 负环
    gn = Graph(directed=True)
    for u, v, w in [('x', 'y', 1), ('y', 'z', -2), ('z', 'x', 0.5)]:
        gn.add_edge(u, v, w)
    assert bellman_ford(gn, 'x') is None, '负环必须检出'
    # 拓扑
    t = Graph()
    for u, v in [('make', 'link'), ('link', 'bin'), ('hdrs', 'bin'), ('bin', 'install')]:
        t.add_edge(u, v, 1)
    order = topological_sort(t)
    assert order.index('make') < order.index('link') < order.index('bin') < order.index('install')
    try:
        cyc = Graph()
        cyc.add_edge('p', 'q'); cyc.add_edge('q', 'p')
        topological_sort(cyc)
        assert False
    except ValueError:
        pass
    # 无向网格: BFS(无权) == Dijkstra(全 1 权)
    gg = grid_graph(20, 25)
    bfsd = bfs(gg, (0, 0))
    dij = dijkstra(gg, (0, 0))
    assert {k: int(v) for k, v in dij.items()} == bfsd, 'BFS 是单位权 Dijkstra'
    print('自测通过：Dijkstra 手算例 / 负环检出 / 拓扑排序 / BFS==单位权 Dijkstra。')


def experiment():
    rng = random.Random(3)
    print('== 路网模拟 120x120（约 3.4 万结点） ==')
    g = road_network(120, 120, seed=7)
    n = len(g.nodes())
    src, dst = (0, 0), (119, 119)
    d1 = dijkstra(g, src)
    print(f"结点数 {n}, 无向边数 {sum(len(a) for a in g.adj.values()) // 2}")
    print(f"Dijkstra: dist({src}->{dst}) = {d1[dst]:.1f}")
    reach = len(bfs(g, src))
    print(f"BFS 可达结点 = {reach}（图应连通）；分量数 = {len(connected_components(g))}")
    # 在 40x40 子路上网跑 Bellman-Ford 对照（Θ(VE) 较慢, 用小图）
    gs = road_network(40, 40, seed=7)
    sub = Graph(directed=False)
    for u, lst in gs.adj.items():
        if u[0] < 40 and u[1] < 40:
            for v, w in lst:
                sub.add_edge(u, v, w)
    da = dijkstra(sub, (0, 0))
    db = bellman_ford(sub, (0, 0))
    same = all(abs(da[u] - db[u]) < 1e-9 for u in da)
    print(f"40x40 子网: Dijkstra 与 Bellman-Ford 距离逐一相等 = {same}")
    # 平均跳数示意
    sample = [(rng.randrange(120), rng.randrange(120)) for _ in range(20)]
    hops = []
    for t in sample:
        d = dijkstra(g, t)
        hops.append(d[dst])
    print(f"20 个随机源到 (119,119) 的距离: min={min(hops)}, med={sorted(hops)[len(hops) // 2]}, max={max(hops)}")


if __name__ == '__main__':
    self_test()
    experiment()
