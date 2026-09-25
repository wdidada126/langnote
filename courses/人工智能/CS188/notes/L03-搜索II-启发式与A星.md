# L03 搜索 II：启发式搜索与 A*

> 对应 AIMA Ch.3.4-3.6；Klein 讲义 "Informed Search"。承接 L02 的 frontier 统一视角。

## 1. 核心概念

- **启发式 h(n)**：对"从 n 到目标剩余代价"的估计；f = g + h。
- **Greedy Best-First**：只按 h 扩展——快但不最优（可能绕路）。
- **A***：按 f = g + h 扩展；**h=0 退化为 UCS，g 权重=0 退化为贪心**。
- **可采纳性（admissibility）**：h(n) ≤ h*(n)（不高估）。树搜索最优性条件。
- **一致性/单调性（consistency）**：h(a) ≤ c(a,b) + h(b)（三角不等式），且 h(goal)=0。
  - 一致 ⟹ 可采纳；图上搜索 A* 最优需要一致性（保证 f 沿路径单调不减，pop 即定案）。
- **支配（dominance）**：h2 ≥ h1 且均可采纳 ⟹ h2 扩展节点不多于 h1。

## 2. 关键定理与伪码

```
function A*-GRAPH(problem, h):
    frontier ← PQ keyed by g + h
    # 弹出时若 state 已 explored 则跳过（一致性下等价 Dijkstra）
    # 目标检验在 pop 时做（tree search 也可在 push 时提前终止）
```

- 构造一致启发式：最短路松弛（shortest path relaxation）、landmark 三角不等式取 max、模式数据库（pattern DB）。
- **relaxed problem** 下界：去掉约束（如 8-puzzle 允许任意方块移动）→ 曼哈顿距离 = "每块最少步数"之和。

## 3. 直觉例子

- Romania：直线欧氏距离（假设直线速度 ≥ 任何公路）可采纳且一致；到最近城市距离恒 0 也可采纳但很弱。
- Pacman P1：**closed-world heuristic**——剩余豆子最小生成树(MST, Prim) + 到最近未吃豆距离 = 可采纳的吃豆下界；"多豆包"（如每 10 豆包 1 点、共 3 包）用 `h = sum_i MST_i` 提升支配性。

## 4. 前后讲联系

- 前承 L02（frontier + 路径成本），后接 L04：h 不存在/内存爆炸时退局部搜索；L05 把 f 评估换成 minimax 估值；L07 GAC、L12 值迭代中 `h=V*` 是"完美启发式"——**值函数 = 最优启发式** 这一观点在 L13 Q-learning 处闭环。

## 5. 跨课程联系

- **6.006**：A* = Dijkstra + reweighting（势函数 φ=h 时边权 w' = w + h(v) − h(u) ≥ 0），一致性保证归约正确——与 Johnson 全源最短路同一技巧。
- **CS229/CS231n**：L14 的策略价值估计、AlphaZero 的价值网络输出的正是学习出来的 h。
- **MIT6.824**：地图路由（Chord）中的"到目标的比特前缀距离"是一种结构化启发式。
- **DDCA**：一致性条件类似时序电路的建立时间约束——f 单调 = 流水线不回退。

## 6. 开源项目应用

- **NetworkX**：`nx.astar(G, heuristic=...)`；`nx.dijkstra_path` 对照。
- **pyAIMA**：`search.py` 含 `recursive_best_first_search`、`hill_climbing`；8-puzzle/tile 问题带曼哈顿启发式。
- **游戏 AI 库（Recast/Detour、Godot AStar）**：导航网格寻路默认 A*+跳点搜索(JPS)；ROS Nav2 的 global planner = A*。
- **Fast Downward（L-规划项目）**：其 h_max 启发式正是"relaxed problem"思想的实现。

## 7. 延伸阅读

- AIMA 4e §3.5；CS188 Note "A* Correctness" 两个证明（树/图）。
- Hart, Nilsson, Raphael "A Formal Basis for the Heuristic Determination of Minimum Cost Paths" (1968)；Goldberg "A Ball-Pit Model…"(1997) 关于 reweighting。
- 项目实战：`projects/search`（本项目用 Python 标准库复现 BFS/DFS/UCS/Greedy/A* 并可视化节点扩展数）。
