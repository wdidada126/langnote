# 项目 1：search —— 无信息与启发式搜索（`maze_search.py`）

## 对应讲次

- **L02 搜索 I**（BFS/DFS/UCS）、**L03 搜索 II**（Greedy/A*、可采纳/一致性/支配）。
- 对应官方 Pacman Project 1（Search）的合成环境简化版。

## 算法与内容

| 模块 | 说明 |
| --- | --- |
| `MazeProblem` | 单目标迷宫：状态=位置，五元组接口 `successors/is_goal/step_cost` |
| `FoodProblem` | 多豆问题：状态=(位置, 剩余豆 frozenset)——bitmask 状态空间，体会"状态定义改变复杂度" |
| `graph_search(problem, strategy, heuristic)` | 统一 frontier 框架：bfs=队列、dfs=栈、ucs=按 g、greedy=按 h、astar=按 g+h |
| `nearest_food_heuristic` / `mst_heuristic` | 最近豆下界 vs MST 下界，实测支配关系（A* 扩展数下降） |

运行后输出：各策略扩展节点数与路径代价对照表、A* 路径可视化、多豆问题 UCS/A* 最优性验证（`assert` 代价一致）。

## 运行方式

```bash
cd projects/search
python3 maze_search.py     # Windows: py -3 maze_search.py
# 或 ./run.sh / run.bat（内含 py_compile 自检：先编译检查再运行）
```

纯标准库（heapq/deque），无需安装任何包。

## 思考题（自测）

1. 把 UCS 的启发式换成 h=0 传给 astar，扩展数应与 UCS 一致——为什么？
2. DFS 在 Part 1 里找到的路径代价比 A* 大多少？frontier 为栈为何导致"先钻死路"？
3. 给 `FoodProblem` 再加一个"墙后有豆"的实例，比较 nearest 与 MST 启发式扩展数差距是否随豆数增大？

## 延伸阅读

- notes/L02-*.md、notes/L03-*.md；papers/papers.md 表一 Hart/Nilsson/Raphael 1968；NetworkX `astar` 对照实现。
