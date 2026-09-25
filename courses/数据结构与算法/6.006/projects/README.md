# MIT 6.006 配套项目集

- 语言：Python 3（仅标准库，不依赖 numpy/matplotlib；"绘图"以文本表格呈现）。
- 精神：对齐 6.006 经典 Problem Sets——每个项目 = 一个数据结构/算法族的**自写实现 + 合成数据实验 + 暴力对拍自测**。
- 约定：每个子目录含 `main.py`（完整自洽，直接运行即跑自测与实验并打印结果）、`README.md`（讲次/知识点/运行方式）、`run.sh` / `run.bat`（先 `python -m py_compile` 语法自检再运行）。
- 本轮只写不集中编译；各 `run.*` 脚本内即含编译自检，逐个运行即可验证。

## 项目总表

| 目录 | 主题 | 对应讲次 | 核心内容 | 运行 |
| --- | --- | --- | --- | --- |
| p01_sorting | 排序与渐近 | L03–L05, L18 | 插入/归并/堆排，比较次数计数与增长率文本表 | `cd p01_sorting && python main.py` |
| p02_search_trees | 搜索树 | L14–L16 | BST（删除/后继）+ 增广区间树 | `cd p02_search_trees && python main.py` |
| p03_hashing_bloom | 哈希与 Bloom | L07, L17, L19 | 线性探测哈希表（倍增惰性重建）+ Bloom filter 实测 FPR vs 理论 | `cd p03_hashing_bloom && python main.py` |
| p04_randomized | 随机化 | L26, L17 | 随机 quickselect 中位数（期望线性验证）+ ER 随机图与连通阈值 | `cd p04_randomized && python main.py` |
| p05_graph_paths | 图遍历与最短路 | L09–L11 | BFS/DFS/拓扑 + Dijkstra/Bellman-Ford，网格与路网模拟 | `cd p05_graph_paths && python main.py` |
| p06_dp | 动态规划 | L08 | 编辑距离（含回溯）/矩阵链/0-1 背包 + 暴力对拍 + fib 四写法调用数 | `cd p06_dp && python main.py` |
| p07_greedy | 贪心 | L11, L18 | 区间调度三策略对拍（反例搜索）+ Huffman（前缀性/Kraft/熵界） | `cd p07_greedy && python main.py` |
| p08_amortized | 摊还 | L19–L20 | 动态数组拷贝计费 + 并查集（按秩/压缩对照实验） | `cd p08_amortized && python main.py` |
| p09_maxflow | 最大流 | 6.046 衔接（L09–L11 延伸） | Edmonds-Karp + 最小割提取，随机图上枚举割暴力对拍；二分图匹配归约 | `cd p09_maxflow && python main.py` |
| p10_np_complete | NP 完全体验 | 6.046/CS170 衔接 | 随机 3-SAT 阈值现象（暴力+回溯）+ TSP（Held-Karp 精确 vs 最近邻/MST 加倍近似） | `cd p10_np_complete && python main.py` |
| p11_online | 在线算法 | L21–L22 | 分页 LRU/FIFO/OPT/Marked 竞争比实验 + ski rental（确定 vs 随机） | `cd p11_online && python main.py` |

## 合成数据原则

- 全部 `random.seed(...)` 固定种子，输出可复现；实验只报**计数/比值**，不依赖挂钟时间（fib 用调用次数代替计时）。
- 每个 `main.py` 的自测段：先 assert 正确性（对拍暴力/参考实现），后打印实验表格；任一 assert 失败即抛错退出。
