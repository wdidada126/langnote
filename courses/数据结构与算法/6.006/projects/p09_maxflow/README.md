# p09 最大流（max flow）

- 对应讲次：6.006 表内 26 讲不含流，本项目为**衔接 6.046 L8–L9** 的延伸件；直接复用本课 L09–L11（BFS/增广/割的分层思想）。
- 知识点：残量网络、Edmonds-Karp（BFS 选最短增广路 → O(VE²) 多项式界）、最大流=最小割的"割即证书"（最终残量图可达集）、二分图最大匹配的流归约。
- 文件：`main.py`（FlowNetwork、暴力枚举全部 s-t 割的对拍器、CLRS 图 26.1 手算例、匹配归约、增广次数实验）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：CLRS 例流=23=割容量；80 组随机小网络与暴力最小割一致；匹配数=4；实验表显示增广次数 ≪ VE 界。
- 延伸：把 BFS 换成 DFS 即 Ford-Fulkerson——用"容量放大反例"观察其不终止/超慢（6.046 经典）。
