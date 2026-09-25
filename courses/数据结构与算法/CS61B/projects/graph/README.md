# 项目 6：图 — BFS / DFS / Dijkstra / Prim / Kruskal

> 对应讲次：L29（图表示）、L30（BFS/DFS）、L31（MST）、L32（Dijkstra）。
> 对应课程作业：Lab9/Lab10、WordLadder、Maze/Teleportation HW；工业对照：OSRM/JGraphT、Git 对象遍历。

## 知识点清单

| 文件/方法 | 知识点 | 复杂度 |
| --- | --- | --- |
| `Graph` | 邻接表 + Edge record；`addEdge` 存两条有向记录（无向图约定） | 空间 Θ(V+E) |
| `bfsHops` | ArrayDeque 队列、首次到达即最短（L19 复用） | Θ(V+E) |
| `dfsOrder`/`connectedComponents` | 递归标记 + 外层扫未访问 | Θ(V+E) |
| `dijkstra` | 松弛 + JDK PriorityQueue "懒惰插入"（弹出时跳过陈旧项），替代 decreaseKey | Θ((V+E) log V) |
| `kruskal` | 边排序 + 并查集判环（cut 性质，L31） | Θ(E log E) |
| `prim` | lazy 版：PQ 装穿越边界的边，陈旧边弹出即弃 | Θ(E log E) |
| `UnionFind` | 加权 + 路径压缩（与 projects/unionfind 同源） | 摊还 ~Θ(1) |

Main 内含一张 9 顶点测试图，**手工预算**了 BFS 跳数、Dijkstra 距离、MST 权重（=19），两套 MST 算法必须给出同一权重——这是"交叉验证"式测试设计（L13）。

## 编译与运行（JDK 17）

```bash
./build.sh        # 或 Windows: build.bat
javac -encoding UTF-8 -d build src/cs61b/graph/*.java
java -cp build cs61b.graph.Main
```

## 实验建议

1. Dijkstra 的 `double[]` 条目法每次松弛都插入新条目，队列规模可达 Θ(E)；改用"索引堆 + decreaseKey"（见 heap 项目实验 2）后重跑，比较 `pq.size()` 峰值。
2. 把测试图某条边权改为负数，观察 Dijkstra 输出错误（∞ 或次优）——这正是 Bellman-Ford 存在的理由（L32）。
3. 加 `dagShortestPath`：拓扑排序 + 一次松弛 ⇒ Θ(V+E)，对比同一图（去环后）上 Dijkstra 的结果一致性——L33 DP 的图视角。
