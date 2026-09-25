# p05 图遍历与最短路（graphs & shortest paths）

- 对应讲次：L09（DFS/递归栈）、L10（BFS/拓扑/连通分量）、L11（Dijkstra + 惰性堆；负权对照 Bellman-Ford）。
- 知识点：邻接表图；BFS 分层距离与 Dijkstra 在单位权下等价；Kahn 拓扑排序并检测环；Bellman-Ford 第 n 轮可松弛 ⇒ 负环；网格图/带捷径路网合成数据。
- 文件：`main.py`（Graph 类 + 五个算法 + 自测 + 120×120 路网实验）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：经典 6 点手算例断言通过；负环检出；BFS==单位权 Dijkstra；路网上 Dijkstra 与 Bellman-Ford 距离逐一相等，并打印随机源距离分布。
- 延伸：加 A*（曼哈顿启发式）对比扩点数（L11/L12 联系）；把路网换成带坐标的 Delaunay 图更接近真实道路。
