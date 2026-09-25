#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch4_router_sim —— 《自顶向下方法》Ch4/Ch5 配套：路由器数据/控制平面模拟器。

三合一（对应笔记第 13/14/16/17 讲）：
  A. 最长前缀匹配 FIB（§4.3）：前缀/长度表 -> 转发决策；二进制 trie 实现。
  B. 链路状态 + Dijkstra（§5.1）：6 节点拓扑算全源最短路，生成每节点 FIB 下一跳。
  C. 距离向量 + Bellman-Ford 异步迭代（§5.1）：含**计数到无穷**演示——
     断链后逐轮打印距离表，观察坏消息以 +2/轮 爬升，毒性逆转可抑制。
仅用标准库：heapq, copy, itertools, time。
"""

import heapq

# ---------------------------------------------------------------- A. LPM FIB

class FIB:
    """二进制 trie 最长前缀匹配。表项: (prefix_str, len) -> next_hop。"""

    def __init__(self):
        self.root = {"kids": [None, None], "nexthop": None}

    def add(self, prefix, plen, nexthop):
        node = self.root
        bits = self._to_bits(prefix)[:plen]
        for b in bits:
            nxt = node["kids"][b]
            if nxt is None:
                nxt = {"kids": [None, None], "nexthop": None}
                node["kids"][b] = nxt
            node = nxt
        node["nexthop"] = nexthop

    @staticmethod
    def _to_bits(dotted):
        out = []
        for octet in dotted.split("."):
            v = int(octet)
            out += [(v >> i) & 1 for i in range(7, -1, -1)]
        return out

    def lookup(self, dotted):
        bits = self._to_bits(dotted)
        node, best = self.root, self.root["nexthop"]
        for b in bits:
            node = node["kids"][b]
            if node is None:
                break
            if node["nexthop"] is not None:
                best = node["nexthop"]
        return best


def demo_fib():
    print("== A. 最长前缀匹配 FIB ==")
    fib = FIB()
    fib.add("192.168.1.0", 24, "eth0-direct")
    fib.add("192.168.0.0", 16, "to-core1")
    fib.add("192.168.1.128", 25, "vpn-tunnel")
    fib.add("0.0.0.0", 0, "default-gw")
    for ip in ("192.168.1.10", "192.168.1.200", "192.168.0.9", "10.0.0.1"):
        print("  {:<14} -> {}".format(ip, fib.lookup(ip)))
    print("  要点：/25 比 /24 长胜；/24 比 /16 长胜；都不匹配走默认。")


# ---------------------------------------------------------------- B. 链路状态

def dijkstra(nodes, edges):
    """edges: list of (u, v, cost)。返回 (dist, parent) 全源对每源一次。"""
    adj = {n: [] for n in nodes}
    for u, v, c in edges:
        adj[u].append((v, c))
        adj[v].append((u, c))
    def one(src):
        dist, parent = {n: float("inf") for n in nodes}, {}
        dist[src] = 0
        pq = [(0, src)]
        seen = set()
        while pq:
            d, u = heapq.heappop(pq)
            if u in seen:
                continue
            seen.add(u)
            for v, c in adj[u]:
                if dist[u] + c < dist[v]:
                    dist[v] = dist[u] + c
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        return dist, parent
    return {n: one(n) for n in nodes}, adj


def demo_ls():
    print("\n== B. 链路状态：教材 Fig.5.3 六节点网络 + Dijkstra ==")
    nodes = "u v x y w z"
    edges = [("u", "v", 2), ("u", "x", 1), ("u", "w", 5),
             ("v", "x", 2), ("v", "y", 1), ("x", "w", 3),
             ("x", "y", 1), ("y", "z", 2), ("w", "z", 1)]
    res, _ = dijkstra(nodes.split(), edges)
    for src in ("u", "w"):
        dist, parent = res[src]
        print("  源 {}  最短路树：".format(src))
        for dst in sorted(dist):
            if dst != src:
                # 回溯求第一跳
                p, first = dst, dst
                while parent.get(p, src) != src and p in parent:
                    p = parent[p]
                first = p
                print("    {} : cost={} via {}".format(dst, dist[dst], first if dist[dst] < float("inf") else "-"))
    print("  ECMP 提示：等代价下一跳应全部进入 FIB（自行扩展 parent 为 list）。")


# ---------------------------------------------------------------- C. 距离向量

class DVNode:
    def __init__(self, name):
        self.name = name
        self.dist = {name: 0}          # 目的 -> 距离
        self.via = {}                  # 目的 -> next hop
        self.links = {}                # 邻居 -> 直连代价

    def vector(self):
        return dict(self.dist)

    def vector_to(self, peer):
        """毒性逆转：对'我经由它到达'的目的，向该邻居宣告 inf。"""
        out = {}
        for dst, val in self.dist.items():
            out[dst] = float("inf") if self.via.get(dst) == peer else val
        return out

    def init_from_links(self):
        self.dist = {self.name: 0}
        self.via = {}
        for nb, c in self.links.items():
            self.dist[nb] = c
            self.via[nb] = nb


def dv_step(node, received):
    """一次 Bellman-Ford 松弛：received = {邻居: 其(可能经毒性逆转的)距离向量}。返回是否变化。"""
    changed = False
    for dst in set(list(node.dist.keys()) + [d for v in received.values() for d in v]):
        if dst == node.name:
            continue
        best = node.dist.get(dst, float("inf"))
        bestvia = node.via.get(dst)
        for nb, vec in received.items():
            if nb not in node.links:
                continue
            d = vec.get(dst, float("inf")) + node.links[nb]
            if d < best:
                best, bestvia = d, nb
        if best != node.dist.get(dst) or bestvia != node.via.get(dst):
            changed = True
        node.dist[dst] = best
        node.via[dst] = bestvia
    return changed


def demo_dv(break_link=("x", "y"), poison=False, rounds=12):
    label = "毒性逆转" if poison else "朴素 DV"
    print("\n== C. 距离向量异步迭代（{}）：断开 {}-{} 演示计数到无穷 ==".format(label, *break_link))
    names = "x y z w".split()
    nodes = {n: DVNode(n) for n in names}
    base = [("x", "y", 1), ("y", "z", 1), ("z", "w", 1), ("x", "w", 3)]
    for u, v, c in base:
        nodes[u].links[v] = c
        nodes[v].links[u] = c
    for n in nodes.values():
        n.init_from_links()
    # 先收敛
    for _ in range(8):
        for n in nodes.values():
            dv_step(n, {nb: nodes[nb].vector() for nb in n.links})

    def show(t):
        line = "  t={:<3}".format(t)
        for n in names:
            line += " {}->y={:<3} ".format(n, nodes[n].dist.get("y", float("inf")))
        print(line)
        line = "      "
        for n in names:
            line += " {}->x={:<3} ".format(n, nodes[n].dist.get("x", float("inf")))
        print(line)

    print("  收敛后：")
    show(0)
    # 断链：x-y 代价 -> inf。只作废"经由被断邻居"的路由（真实协议行为），
    # 其余陈旧估计保留——正是计数到无穷的舞台。
    for a, b in (("x", "y"), ("y", "x")):
        nodes[a].links.pop(b, None)
        for dst in list(nodes[a].dist):
            if dst == b or nodes[a].via.get(dst) == b:
                nodes[a].dist.pop(dst, None)
                nodes[a].via.pop(dst, None)
        nodes[a].dist[a] = 0
    print("  断链后逐轮（观察 x/y 互为备胎、距离每轮 +2 爬升）：")
    for t in range(1, rounds + 1):
        changed = False
        for n in names:
            node = nodes[n]
            if poison:
                recv = {nb: nodes[nb].vector_to(node.name) for nb in node.links}
            else:
                recv = {nb: nodes[nb].vector() for nb in node.links}
            changed |= dv_step(node, recv)
        show(t)
        if not changed:
            break
    print("  结论：{} —— {}".format(
        "环被毒性逆转消灭，x 快速用 x-w-z-y" if poison else "y 借 x、x 借 y，距离缓慢爬到正确值(3)或更高",
        "这就是计数到无穷；RIP 用 15 跳封顶缓解（§5.1/笔记第 17 讲）"))


def main():
    demo_fib()
    demo_ls()
    demo_dv(poison=False)
    demo_dv(poison=True)


if __name__ == "__main__":
    main()
