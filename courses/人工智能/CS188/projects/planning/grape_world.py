# -*- coding: utf-8 -*-
"""规划项目（L02-L03 搜索视角 + AIMA Ch.10-11 补充）：GrapeWorld 简化版状态空间规划

运行:  python grape_world.py
经典 GRAPES 世界(Russell & Norvig 规划习题)的极简合成版:
  两个房间 A(有机械手 grip, 有杯子) / B(有一串葡萄 grape);
  机器人(起始在 A) 双手最多: grip / grape / juice;
  动作: Move(1) PickGrip(1) PickGrape(2, 需 grip 且在 B)
        Pour(3, 需在 A 且同时握 grip+grape, 消耗 grape 得 juice)
        Drink(1, 需握 juice) --> 目标: 已喝到葡萄汁(done).
规划 = 在状态空间 (位置, 手持集合, done) 上搜索, 对照 AIMA STRIPS 前置/效果表.
"""
from collections import deque
import heapq

ACTIONS_META = [
    # (名称, 代价, 前置条件描述, 效果描述)
    ("Move",        1, "总可执行(到另一房间)",     "位置翻转"),
    ("PickGrip",    1, "在A 且未握grip",           "+grip"),
    ("PickGrape",   2, "在B 且握grip 且未握grape", "+grape"),
    ("Pour",        3, "在A 且握grip 且握grape",   "-grape +juice"),
    ("Drink",       1, "握juice",                  "+done (目标)"),
]


def successors(state):
    pos, hands, done = state
    if done:
        return
    other = "B" if pos == "A" else "A"
    yield f"Move({pos}->{other})", 1, (other, hands, done)
    if pos == "A" and "grip" not in hands:
        yield "PickGrip", 1, (pos, hands | {"grip"}, done)
    if pos == "B" and "grip" in hands and "grape" not in hands:
        yield "PickGrape", 2, (pos, hands | {"grape"}, done)
    if pos == "A" and "grip" in hands and "grape" in hands:
        yield "Pour", 3, (pos, (hands - {"grape"}) | {"juice"}, done)
    if "juice" in hands:
        yield "Drink", 1, (pos, hands - {"juice"}, True)


def is_goal(state):
    return state[2]


def goal_flags(state):
    pos, hands, done = state
    return {"grip": "grip" in hands, "grape": "grape" in hands,
            "juice": "juice" in hands, "drunk": done}


def h_missing(state):
    """未完成子目标计数启发式(GBFS 用). 注意: Pour 消耗 grape, 该 h 在本域不严格可采纳,
    故只用于演示 GBFS 的行为, 最优解以 UCS 为准 -- 这正是'启发式设计要检查副作用'的活教材."""
    return sum(1 for v in goal_flags(state).values() if not v)


class PNode:
    def __init__(self, state, parent, action, cost):
        self.state, self.parent, self.action, self.cost = state, parent, action, cost


def plan_search(start, strategy, h=h_missing):
    """BFS / UCS / GBFS 三种规划器共用骨架 (L02 的 frontier 统一思想).

    BFS: 单位步数视角, push 时去重即可;
    UCS: 代价不等, 必须"弹出时定案"(Dijkstra 正确性, 见笔记 L02);
    GBFS: 启发式 h_missing, 最优性无保证.
    """
    start_node = PNode(start, None, None, 0)
    keyf = ((lambda n: n.cost) if strategy == "ucs"
            else (lambda n: h(n.state)))
    if strategy == "bfs":
        frontier = deque([start_node])
        seen = {start}
        while frontier:
            node = frontier.popleft()
            if is_goal(node.state):
                return node
            for name, cost, ns in successors(node.state):
                if ns not in seen:
                    seen.add(ns)
                    frontier.append(PNode(ns, node, name, node.cost + cost))
        return None
    counter = 0
    frontier = [(keyf(start_node), counter, start_node)]
    closed = set()
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node.state in closed:
            continue
        closed.add(node.state)
        if is_goal(node.state):
            return node
        for name, cost, ns in successors(node.state):
            if ns in closed:
                continue
            child = PNode(ns, node, name, node.cost + cost)
            counter += 1
            heapq.heappush(frontier, (keyf(child), counter, child))
    return None


def extract(node):
    acts, states = [], []
    while node.parent is not None:
        acts.append(node.action)
        states.append(node.state)
        node = node.parent
    return list(reversed(acts)), list(reversed(states))


def show_plan(title, node):
    acts, states = extract(node)
    print(f"\n-- {title}: {len(acts)} 步, 总代价 {node.cost}")
    s0 = ("A", frozenset(), False)
    print(f"   状态                          动作")
    print(f"   pos=A hands=∅                 (初始)")
    prev = s0
    for a, s in zip(acts, states):
        pos, hands, done = s
        print(f"   pos={pos} hands={{{','.join(sorted(hands))}}} done={done:<5} {a}")
        prev = s


def main():
    print("=" * 62)
    print("GrapeWorld 简化版: 前置条件状态搜索规划 (AIMA Ch.10-11 补充)")
    print("\nSTRIPS 风格动作表:")
    print(f"{'动作':<12}{'代价':<6}{'前置条件':<32}{'效果'}")
    for name, c, pre, eff in ACTIONS_META:
        print(f"{name:<12}{c:<6}{pre:<32}{eff}")
    print("\n状态空间: (位置∈{A,B}) x (手持子集) x done -- 枚举即知规模 ~ 2*8*2=32")

    start = ("A", frozenset(), False)
    for strategy, title in [("bfs", "BFS(最少步数, 忽略代价)"),
                            ("ucs", "UCS(最小代价=最优计划)"),
                            ("gbfs", "GBFS(未完成子目标启发, 不保证最优)")]:
        node = plan_search(start, strategy)
        if node is None:
            print(f"\n-- {title}: 未找到计划")
        else:
            show_plan(title, node)
    print("\n讨论: 规划=在'世界状态'上跑 L02-L03 的搜索算法; 状态变量越多组合越爆炸,")
    print("      真实规划器(Fast Downward)靠删除放松等启发式, 思路与 L03 一脉相承.")


if __name__ == "__main__":
    main()
