# L31 最小生成树与并查集（Prim、Kruskal、Union-Find）

> 对应 spring2024 L31：cut 性质、lazy/eager Prim、Kruskal、并查集。阅读：CLRS 21（disjoint-set）、23（MST）。作业：Lab（Union-Find）、HW（Asteroids）。项目对应：projects/unionfind、projects/graph。

## 1. 核心概念

- **MST 定义与 cut 性质**：跨越任意割的最轻边必属于某 MST——Prim/Kruskal 的共同正确性引擎。
- **Kruskal**：边按权重排序，依次加入不形成环者；"判环"交给并查集：
  ```java
  Arrays.sort(edges, Comparator.comparingDouble(e -> e.weight));
  for (Edge e : edges)
      if (uf.find(e.v) != uf.find(e.w)) { mst.add(e); uf.union(e.v, e.w); }
  // Θ(E log E)
  ```
- **Prim lazy**：优先队列装"所有穿越树界的边"，弹出连接未访问点者；陈旧边留着等弹（队列可到 Θ(E)）。
  **Prim eager**：PQ 只装顶点，键 = `edgeTo[v].weight`，发现更优边 `decreaseKey`。
- **并查集（Union-Find / Disjoint Set）**：动态连通性——只支持 `union` 与 `connected`：
  ```java
  int find(int p) { while (p != parent[p]) { parent[p] = parent[parent[p]]; // 路径压缩
                                            p = parent[p]; } return p; }
  void union(int a, int b) { int ra = find(a), rb = find(b);
                             if (size[ra] < size[rb]) { int t=ra; ra=rb; rb=t; }
                             parent[rb] = ra; size[ra] += size[rb]; } // 按大小加权
  ```
- 演进四级：quick-find Θ(n)/union → quick-union（树）→ 加权 union → **加权 + 路径压缩 ⇒ 摊还 Θ(α(n)) ≈ 常数**（Tarjan；61B 只要求会用+给直觉证明）。

## 2. 复杂度视角

| 算法 | 时间 | 空间 | 备注 |
| --- | --- | --- | --- |
| Kruskal | Θ(E log E)=Θ(E log V) | Θ(V+E) | 边排序主导；稀疏图友好 |
| Prim lazy | Θ(E log E) | Θ(E) PQ | 每边最多入队一次 |
| Prim eager | Θ(E log V) | Θ(V) PQ | decreaseKey 需索引堆（L28 扩展） |
| Prim + Fibonacci 堆 | Θ(E + V log V) | | 理论最优，工程少见 |
| UF 加权+压缩 m 次操作 | 摊还 Θ(m·α(n)) | Θ(n) | Kruskal 的 connected 检查 |

## 3. 与前后讲联系

- 上承：L28 堆（两种 Prim 的 PQ）、L30 连通性概念升级成"带权最小连通"；L24 Comparator 驱动 Kruskal 排序。
- 下启：L32 Dijkstra 是"Prim-eager 框架只改键语义（distSum 替代 edgeTo.weight）"——61B 官方反复强调的同构；Lab 的 Asteroids（同屏连通块数）= 网格图 + UF 模板。

## 4. 跨课程联系

- **CS61A**：无对应；UF 是 61B 独有的"动态连通"武器，61A 只处理树/表的静态世界。
- **6.006/CS170/6.046**：6.046 给 Kruskal/Prim 的正确性 cut 证明与 Borůvka；CS170 把 α(n) 作为"摊还+阿克曼逆"招牌结果（Fredman-Saks 下界证明它最优）。
- **CSAPP**：`parent[]` 数组版 UF 的 find 是指针追逐（每跳一次 cache miss）——大 n 时"按大小 union"同时是缓存与深度双优化；GPU/TPU 上的 connected-components 用 pointer jumping 并行化。
- **OS/体系结构（DDCA）**：Linux cgroup/scheduler group 合并、链接器符号解析（把"同一符号的多次定义"union 成一个）本质都是 UF。
- **15-445/分布式**：Crash Recovery 中事务等价类、Chandy-Lamport 快照分组、网络分区的连通视图都复用 UF；Pregel/Giraph 的 CC 是 BFS 版对偶。

## 5. 开源项目应用

- **JDK**：无内置 UF（`java.util` 缺口，手写常考）；Apache Commons 有 `UnionFind`。
- **Lucene**：段编号映射 `ReaderAndUpdates` 的 liveDocs 分组、`Docvalues` 更新合并用 UF 式重映射。
- **Git**：`pack-objects` 把 delta 链基对象归组、`commit-graph` 的 chunk 合并；multi-pack-index 中包分组。
- **图形/图像（Photoshop 魔棒、连通域）**：经典 two-pass 连通标记 = 本讲 UF 的最出名工业应用（Halcon/OpenCV `connectedComponents` 文档直接引用加权 UF）。
- **分布式**：Kafka 控制器做分区 leader 均衡时的机架分组、Spark Shuffle 块合并。

## 6. 延伸阅读

- Hug 笔记 "Minimum Spanning Trees" "Union Find"；CLRS 21.3（带引理链的 α(n) 证明梗概）。
- Tarjan & van Leeuwen "Union-Find Algorithms with Path Compression"(1979)；Fredman & Saks 下界(1989)。
- Sedgewick & Wayne algs4 1.5（UF 实验对比表，本课 Lab 的母题）。
