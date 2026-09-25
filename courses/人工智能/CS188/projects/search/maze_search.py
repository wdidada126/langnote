# -*- coding: utf-8 -*-
"""L02-L03 搜索项目：网格迷宫上的 BFS/DFS/UCS/Greedy/A*（Pacman 风格合成环境）

运行:  python maze_search.py   （或 ./run.sh / run.bat）
纯标准库。对应笔记 notes/L02-*.md、notes/L03-*.md。

内容:
  1) 单目标迷宫: 五种策略对比(扩展节点数/路径代价), 验证 A* 最优且扩展最少;
  2) 多豆问题(Pacman P1 味): 状态=(位置, 剩余豆子集合) bitmask 状态空间,
     对比 UCS / A*+最近豆启发式 / A*+MST 启发式(支配性)。
"""
import heapq
from collections import deque

DIRECTIONS = {"North": (-1, 0), "South": (1, 0), "West": (0, -1), "East": (0, 1)}


def parse_maze(lines):
    walls, foods = set(), set()
    start = goal = None
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "#":
                walls.add((r, c))
            elif ch == "P":
                start = (r, c)
            elif ch == "G":
                goal = (r, c)
            elif ch == "o":
                foods.add((r, c))
    return walls, foods, start, goal


class MazeProblem:
    """单目标: 状态 = 吃豆人位置."""

    def __init__(self, lines):
        self.lines = lines
        self.walls, self.foods, self.start, self.goal = parse_maze(lines)
        self.rows = len(lines)
        self.cols = max(len(r) for r in lines)

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.walls

    def successors(self, pos):
        r, c = pos
        for name, (dr, dc) in DIRECTIONS.items():
            n = (r + dr, c + dc)
            if self.in_bounds(n):
                yield name, n

    def step_cost(self, state, action, nstate):
        return 1

    def is_goal(self, state):
        return state == self.goal


class FoodProblem:
    """多豆: 状态 = (位置, frozenset(剩余豆)) -- 状态定义改变复杂度(笔记 L02 要点)."""

    def __init__(self, lines):
        self.lines = lines
        self.walls, self.foods, self.start, _ = parse_maze(lines)
        self.rows = len(lines)
        self.cols = max(len(r) for r in lines)

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.walls

    def successors(self, state):
        pos, remain = state
        r, c = pos
        for name, (dr, dc) in DIRECTIONS.items():
            n = (r + dr, c + dc)
            if self.in_bounds(n):
                yield name, (n, remain - {n} if n in remain else remain)

    def step_cost(self, state, action, nstate):
        return 1

    def is_goal(self, state):
        return len(state[1]) == 0


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def goal_heuristic(problem):
    return lambda state: manhattan(state, problem.goal)


def nearest_food_heuristic(problem):
    """可采纳(必须到达至少一颗豆), 但很弱."""

    def h(state):
        pos, remain = state
        if not remain:
            return 0
        return min(manhattan(pos, f) for f in remain)

    return h


def mst_heuristic(problem):
    """MST(当前位置+剩余豆) 全连接代价 -- 可采纳且支配 nearest_food."""

    def mst_cost(points):
        if len(points) <= 1:
            return 0
        intree = [points[0]]
        rest = list(points[1:])
        total = 0
        while rest:
            best_d, best_i = None, None
            for i, p in enumerate(rest):
                for q in intree:
                    d = manhattan(p, q)
                    if best_d is None or d < best_d:
                        best_d, best_i = d, i
            total += best_d
            intree.append(rest.pop(best_i))
        return total

    def h(state):
        pos, remain = state
        if not remain:
            return 0
        return mst_cost([pos] + list(remain))

    return h


def graph_search(problem, strategy, heuristic=None):
    """统一 frontier: bfs=queue, dfs=stack, ucs/greedy/astar=堆(键不同)."""
    start = Node(problem.start)
    explored = set()
    expanded = 0
    counter = 0

    if strategy in ("bfs", "dfs"):
        fringe = deque([start])
        push = fringe.append
        pop = fringe.popleft if strategy == "bfs" else fringe.pop
        heap = None
    else:
        heap = []
        key = (
            (lambda n: n.path_cost)
            if strategy == "ucs"
            else (lambda n: heuristic(n.state))
            if strategy == "greedy"
            else (lambda n: n.path_cost + heuristic(n.state))
        )
        heapq.heappush(heap, (key(start), 0, start))
        push = pop = None

    while True:
        if heap is not None:
            if not heap:
                break
            _, _, node = heapq.heappop(heap)
        else:
            if not fringe:
                break
            node = pop()
        if node.state in explored:
            continue
        explored.add(node.state)
        expanded += 1
        if problem.is_goal(node.state):
            return node, expanded
        for action, nstate in problem.successors(node.state):
            if nstate in explored:
                continue
            child = Node(nstate, node, action,
                         node.path_cost + problem.step_cost(node.state, action, nstate))
            if heap is not None:
                counter += 1
                heapq.heappush(heap, (key(child), counter, child))
            else:
                push(child)
    return None, expanded


def reconstruct(node):
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return list(reversed(actions))


def render(problem, node):
    """仅用于单目标 MazeProblem: 在地图上标出路径."""
    grid = [list(row) for row in problem.lines]
    cur = node
    while cur is not None:
        r, c = cur.state
        if grid[r][c] not in ("P", "G"):
            grid[r][c] = "*"
        cur = cur.parent
    return "\n".join("".join(row) for row in grid)


def run_single_goal():
    maze = [
        "###########",
        "#P#     #G#",
        "# # # # # #",
        "#   #   # #",
        "### # #   #",
        "#     #   #",
        "###########",
    ]
    print("=" * 60)
    print("Part 1  单目标迷宫 (L02-L03)")
    print("\n".join(maze))
    prob = MazeProblem(maze)
    h = goal_heuristic(prob)
    print(f"{'策略':<8}{'最优性':<8}{'扩展节点':<10}{'路径代价':<10}")
    results = {}
    for name, heur in [("bfs", None), ("dfs", None), ("ucs", None),
                       ("greedy", h), ("astar", h)]:
        node, exp = graph_search(prob, name, heur)
        cost = node.path_cost if node else float("inf")
        results[name] = (node, exp)
        optimal = "是*" if name in ("bfs", "ucs", "astar") else "否"
        print(f"{name:<10}{optimal:<10}{exp:<12}{cost:<10}")
    print("\nA* 解路径 (* 为路径):")
    print(render(prob, results["astar"][0]))
    print("动作序列:", "->".join(reconstruct(results["astar"][0])))
    print("注: bfs 单位代价下最优; dfs/greedy 无最优保证 (笔记 L02/L03 表格).")


def run_food():
    maze = [
        "#############",
        "#P   #   o  #",
        "# ## # ### ##",
        "#  o    o   #",
        "## # #### # #",
        "#  o #  o   #",
        "#############",
    ]
    print("\n" + "=" * 60)
    print("Part 2  多豆问题: 状态=(位置,剩余豆集合) (Pacman P1 味)")
    print("\n".join(maze))
    prob = FoodProblem(maze)
    print(f"豆子数: {len(prob.foods)}  状态空间规模 ~ {len(prob.foods) * 2 ** len(prob.foods)} * 格子数")
    print(f"{'策略':<18}{'扩展节点':<12}{'最优代价':<10}")
    rows = []
    node, exp = graph_search(prob, "ucs")
    rows.append(("UCS", exp, node.path_cost))
    optimal = node.path_cost
    for name, heur in [
        ("A*+最近豆", nearest_food_heuristic(prob)),
        ("A*+MST(支配)", mst_heuristic(prob)),
    ]:
        n2, e2 = graph_search(prob, "astar", heur)
        rows.append((name, e2, n2.path_cost))
        assert n2.path_cost == optimal, "可采纳启发式下 A* 必须最优"
    for gname, heur in [("Greedy+最近豆", nearest_food_heuristic(prob))]:
        n3, e3 = graph_search(prob, "greedy", heur)
        print(f"{gname:<16}{e3:<12}{n3.path_cost:<10}(贪心不保证最优)")
    for name, exp, cost in rows:
        print(f"{name:<18}{exp:<12}{cost:<10}")
    print("结论: 启发式越强(支配), A* 扩展越少; 一致启发式下 A* = UCS 的定向版.")


if __name__ == "__main__":
    run_single_goal()
    run_food()
