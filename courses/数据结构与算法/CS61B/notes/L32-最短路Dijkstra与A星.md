# L32 单源最短路：Dijkstra 与 A* 启发式

> 对应 spring2024 L32：Dijkstra、优先级队列使用、A*（Maze/Teleportation HW）。阅读：CLRS 24.3。项目对应：projects/graph。

## 1. 核心概念

- **问题**：带非负权图，单源 s 到所有 v 的最短路径权 `distTo[v]`。
- **Dijkstra = Prim-eager 换键**：PQ 键从"连接到树的最轻边"换成"已确定的 s→v 距离"；弹出即冻结（贪心正确性依赖非负权）。
  ```java
  Arrays.fill(distTo, Double.POSITIVE_INFINITY); distTo[s] = 0;
  IndexMinPQ<Double> pq = new IndexMinPQ<>(V); pq.insert(s, 0.0);
  while (!pq.isEmpty()) {
      int v = pq.delMin();
      for (Edge e : g.adj(v))
          if (distTo[e.to] > distTo[v] + e.weight) {       // 松弛 relax
              distTo[e.to] = distTo[v] + e.weight;
              edgeTo[e.to] = e;
              if (pq.contains(e.to)) pq.decreaseKey(e.to, distTo[e.to]);
              else pq.insert(e.to, distTo[e.to]);
          }
  }
  ```
- **负权破坏 Dijkstra**（弹出后又被改短）→ Bellman-Ford Θ(VE)（CS61B 提及，6.006/CS170 主讲）；含负环则 SSSP 无定义。
- **A\***：把 PQ 键换成 `distTo[v] + h(v)`，h 为**可采纳启发式**（不高估真实剩余距离，如欧氏/曼哈顿距离）→ 弹出目标即最优；h=0 退化为 Dijkstra。
- **Teleportation HW 技巧**：加"传送边"后图含 0 权边——Dijkstra 仍正确（0 非负）；分层建图是通用模式。

## 2. 复杂度视角

| 实现 | 时间 | 说明 |
| --- | --- | --- |
| Dijkstra + 二叉堆 | Θ((V+E) log V) | 每边至多一次 decreaseKey（=删+插） |
| Dijkstra + Fibonacci 堆 | Θ(E + V log V) | 理论，几乎不用 |
| Dijkstra + 数组线性取 min | Θ(V²) | 稠密图反而最优 |
| DAG 最短路（拓扑序递推） | **Θ(V+E)** | 无环可免 PQ；L33 DP 的同一家族 |
| Bellman-Ford | Θ(VE) | 容忍负权/检负环 |
| BFS（无权特例） | Θ(V+E) | 全 1 权 = Dijkstra 用普通队列 |

## 3. 与前后讲联系

- 上承 L31（同一"PQ + 已确定集合"骨架）、L28（索引堆/IndexMinPQ 是 Lab 必写）、L30（无权最短路）。
- 下启 L33：DAG 上的 DP（背包图、编辑距离网格）即"按拓扑序跑一遍松弛"；排序无关，但 Project2 的迷宫/HW Maze 用 A*。

## 4. 跨课程联系

- **CS61A**：61A 的项目（Hagopian Taxi 等）用 Python 手写 Dijkstra 做地图 App——61A 视角它是"一个函数"，61B 视角它是"堆+图+贪心"三结构的合体；CS188 则把 A* 升格为搜索课程的主角（一致性/_admissible_ 证明更细）。
- **6.006/CS170**：6.006 给 Dijkstra 的循环不变量证明与 Bellman-Ford/负权全谱；CS170 讲 Johnson 全源（重新加权 + Dijkstra）。
- **CSAPP**：PQ 弹出随机访问 `items[]` 的下降 = 缓存不友好；稀疏图 CSR 邻接表连续存放可使松弛阶段带宽翻倍——图工程 = 内存布局工程。
- **OS/DDCA**：路由器 Dijkstra/SPF（OSPF 链路状态协议）是其最著名的工业部署；V 类数千级、每 30s 重算，Θ(V²) 数组版足够——"渐近最优 ≠ 工程最优"案例。
- **15-445/分布式**：Chandy-Rice 路由表更新即分布式 Bellman-Ford（距离向量，RIP）。

## 5. 开源项目应用

- **JDK**：无图库；Guava `ShortestPath.ssaDijkstra`、JGraphT `DijkstraShortestPath`/`AStarStar` 直接对应本讲。
- **OSRM/Valhalla/GraphHopper**（路由引擎）：分层收缩（Contraction Hierarchies）= Dijkstra 的预处理加速 1000×——"先付空间换查询时间"的算法工程化典范；A* + 地理启发式是其内核。
- **Lucene**：`MultiTermQuery` 的 top-k 检索用类似 PQ 的"候选集+提前终止"框架（WAND 与 Dijkstra 共享"上界剪枝"思想）。
- **Git**：`git blame`/revision walk 不做最短路，但 commit 距离（ahead/behind）用 BFS；JGit 的对象遍历按时间优先队列展开，结构同 Dijkstra 骨架。

## 6. 延伸阅读

- Hug 笔记 "Shortest Paths"；CLRS 24.3（Dijkstra 正确性：贪心交换论证）、24.1（松弛通用定理）。
- Hart-Nilsson-Raphael 1968（A* 原论文）；"A* Space-Optimal: IDA*" 简介。
- Geisberger 的 Contraction Hierarchies 论文（工业级最短路）。
