# L29–L30 图表示与遍历：DFS 与 BFS

> 对应 spring2024 L29–L30：图模型与 Graph API、邻接表、DFS/BFS、连通性与跳数最短路径。阅读：CLRS 22.2–22.3；Lab9/Lab10；HW（WordLadder）。项目对应：projects/graph。

## 1. 核心概念

- **表示选型**：
  | 表示 | 空间 | 遍历 v 的邻居 | 判边存在 | 适用 |
  | --- | --- | --- | --- | --- |
  | 邻接表 `Map<V, List<Edge>>` | Θ(V+E) | Θ(deg) | Θ(deg) | 稀疏图（本课默认） |
  | 邻接矩阵 | Θ(V²) | Θ(V) | Θ(1) | 稠密/图算法代数（矩阵乘法闭包） |
  | 边列表 | Θ(E) | Θ(E) | Θ(E) | 仅 Kruskal 排序场景（L31） |
- **Graph API（Lab9 式）**：`V()`、`E()`、`adj(v)` 迭代器、`edges(v)`；有权边 `Edge { from, to, weight }`。把"图"与"图上算法"解耦，同 L08 接口哲学。
- **DFS（栈/递归）**：探到底再回头；用于连通分量、环检测、拓扑序（L31）、路径存在性。
  ```java
  void dfs(Graph g, int v) {
      visited[v] = true;
      for (int w : g.adj(v)) if (!visited[w]) { edgeTo[w] = v; dfs(g, w); }
  }
  ```
- **BFS（队列）**：一圈圈扩散；**无权图单源最短路**——第一次到达即最短（层级证明：dist 非降出队）。
  ```java
  Queue<Integer> q = new ArrayDeque<>(); q.add(s); dist[s] = 0;
  while (!q.isEmpty()) {
      int v = q.remove();
      for (int w : g.adj(v))
          if (dist[w] == -1) { dist[w] = dist[v] + 1; edgeTo[w] = v; q.add(w); }
  }
  ```
- `edgeTo[]` 是一棵以 s 为根的**最短路树/DFS 树**：路径回溯 `while (v != s) v = edgeTo[v]`。

## 2. 复杂度视角

| 算法 | 时间 | 空间 | 关键点 |
| --- | --- | --- | --- |
| DFS/BFS | Θ(V+E) | Θ(V) | 每边检查至多 2 次（无向）|
| 连通分量计数 | Θ(V+E) | | 外层对未访问点起 BFS |
| 无权最短路 | Θ(V+E) | Θ(V) | BFS 副产品 |
| 判环（无向） | Θ(V+E) | | 非树边指向已访问父以外的点 |
| 拓扑排序（DFS 逆后序 / Kahn 入度） | Θ(V+E) | Θ(V) | 仅 DAG；L31 前哨 |

## 3. 与前后讲联系

- 上承：L19 ArrayDeque 即 BFS 队列、L16 递归栈即 DFS；L20 HashMap 存 `dist`（顶点不连续编号时）。
- 下启：L31 MST 的 cut 性质用"已选边集是否连通"表述（并查集）；L32 Dijkstra = "带权重的 BFS + 优先级队列换掉普通队列"；L33 DP 在 DAG 上=拓扑序递推（Teleportation HW）。

## 4. 跨课程联系

- **CS61A**：61A 在 Scheme 里以"世界树 + memoization"写搜索，BFS/DFS 是 stream/树遍历语言；61B 把"遍历顺序"升格为图算法本体——两课同一棵树，61A 看值、61B 看形状。
- **6.006/CS170**：CLRS 三色标记（白灰黑）+ 递归树定理（DFS 分类树边/背边/叉边/前边）比本课细一层；CS170 以 BFS/DFS 为归约起点讲 reachability 下界。
- **CSAPP**：`visited[]` 布尔数组 = 位图/字节图，Θ(V) 位；超大图（web 级）用 Bloom filter 近似代替（省内存换假阳性）——数据结构换精度的一课。
- **DDCA**：DFS 递归深度失控 = 栈溢出（`StackOverflowError`），对应硬件栈帧；图遍历的显式栈改写是 OS 课程协程/纤夫(continuation)的动机之一。
- **OS**：内存分配器的空闲图可达性分析、文件 fsck 的 inode 遍历都直接是 DFS。

## 5. 开源项目应用

- **JDK**：无图库（java.util 只给组件）；Guava `graph`、JGraphT 提供 Lab9 式 API——JGraphT 的 `Algorithms` 包就是 Lab10/HW 的成品对照。
- **Git**：`git log --graph` = commit DAG 的 DFS 优先队列遍历（按提交时间作 tie-break）；`git gc` 可达性标记是经典 mark-sweep DFS；commit-graph 文件缓存 BFS 层级。
- **Lucene**：段合并调度对 segment 图做贪心遍历；查询改写图（synonym expansion）用 BFS 展开有限层。
- **Neo4j/TinkerPop**：Cypher/Gremlin 的 `MATCH (a)-[*1..3]->(b)` 就是带深度上限的 BFS；遍历策略层暴露 DFS/BFS/广度优先评分——工业级图 API 与 Lab9 抽象一致。
- **Linux**：内核模块依赖加载（modules.dep 图的 DFS 后序加载）；cgroup 树遍历。

## 6. 延伸阅读

- Hug 笔记 "Graphs" "Graph Traversals"；CLRS 22.1–22.4（含 BFS 正确性引理 22.2 与 DFS 括号定理）。
- Sedgewick《Algs4》4.1（同一 API 风格，61B 官方精神来源）；BFS 双向搜索优化见 CS188。
- "The GraphBLAS" 论文（图算法线性代数化——邻接矩阵路线的现代复兴）。
