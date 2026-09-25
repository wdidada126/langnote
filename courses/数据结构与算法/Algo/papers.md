# Algorithms I & II 参考文献与开源应用（骨架）

> 关联讲次对应 README/outline 的 L1–L12（延伸 A–C 为 algs4 ch.6 相关主题）。论文标题以英文原名为准，个别中文说明为意译；正式引用前请核对出处与 DOI。

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Shell Sort: Algorithms for Sorting Information Structured Data (D. L. Shell) | 1959 | 递减增量排序，第一个实践上显著优于 O(N²) 的排序 | L2 |
| Algorithm 64: Quicksort (C. A. R. Hoare) | 1961 | 提出快速排序，至今通用排序的骨架 | L3 |
| An Algorithm for the Organization of Information (Adelson-Velskii & Landis) | 1962 | AVL 树与旋转，首个自平衡二叉搜索树 | L6 |
| A Note on Two Problems in Connexion with Graphs (E. W. Dijkstra) | 1959 | 单源最短路（Dijkstra）与 MST 的贪心证明范式 | L9, L10 |
| On the Shortest Spanning Subtree of a Graph (J. B. Kruskal) | 1956 | MST 贪心算法与"避环"准则 | L9 |
| Shortest Connection Networks and Some Generalizations (R. C. Prim) | 1957 | 逐点扩张的 MST 算法（Prim） | L9 |
| Algorithm 232: Heapsort (J. W. J. Williams) / Algorithm 245: Treesort (R. W. Floyd) | 1964 | 堆结构与原地 O(N log N) 堆排序 | L4 |
| Trie Memory (E. Fredkin) | 1960 | 形式化前缀树，字符串检索结构的源头 | L11 |
| Organization and Maintenance of Large Ordered Indexes (Bayer & McCreight) | 1972 | B 树，磁盘索引与数据库的基石 | L6 |
| Fast Pattern Matching in Strings (Knuth, Morris & Pratt) | 1977 | 线性时间字符串匹配与前缀函数（KMP） | L12 |
| A Fast String Searching Algorithm (Boyer & Moore) | 1977 | 坏字符/好后缀启发式，实践亚线性搜索 | L12 |
| Efficient Randomized Pattern-Matching Algorithms (Karp & Rabin) | 1987 | 滚动哈希字符串匹配，多模式与查重基础 | L12 |
| Self-Adjusting Binary Search Trees (Sleator & Tarjan) | 1985 | 伸展树与摊还分析方法论 | L1, L6 |
| Fibonacci Heaps (Fredman & Tarjan) | 1987 | 摊还 O(1) 合并的优先队列，Dijkstra 达 O(E + V log V) | L4, L10 |
| Engineering a Sort Function (Bentley & McIlroy) | 1993 | 系统级 qsort 实现：三向切分、碎片处理、小数组策略 | L3, L11 |
| A Killer Adversary for Quicksort (M. D. McIlroy) | 1999 | 构造使朴素快排退化的输入，催生随机化/pdqsort | L3 |
| Efficiency of a Good but Not Linear Set Union Algorithm (Tarjan & Van Leeuwen) | 1975 | 加权快速合并 + 路径压缩的近线性（逆 Ackermann）界 | L9 |

## 近 5 年文献（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Algorithms with Predictions（Beyond the Worst-Case Analysis of Algorithms 章节） | 2021 | 学习增强算法：用 ML 预测打破最坏情况界（排序、缓存、匹配） | L1, L3 |
| pdqsort 进入 Rust 标准库排序实现 | 2021 | 模式破坏快排：随机化 + 部分有序检测，逼近工程排序上界 | L3 |
| Negative-Weight Single-Source Shortest Paths in Near-Linear Time (Bernstein, Nanongkai, Wulff-Nilsen) | 2022 | 负权 SSSP 近多项式/近线性突破，重写最短路可行性边界 | L10 |
| Discovering Faster Matrix Multiplication Algorithms with Reinforcement Learning (AlphaTensor, Nature) | 2022 | 自动搜索矩阵乘法算法，发现优于 Strassen 的方案 | L1, 延伸 A |
| A (Near-)Linear-Time Maximum Flow 系列（Yang 2020/2021；Brand 等 2022–2023） | 2021–2023 | 近最优最大流：把流问题推向"几乎读输入一遍" | 延伸 B |
| 矩阵乘法指数上界改进至 2.371552（Duan–Wu–Zhou） | 2023 | 改进激光方法，刷新矩阵乘法指数 ω 的上界 | 延伸 A |
| Mathematical Discoveries via Human-Aligned Program Search (FunSearch, Nature) | 2024 | LLM + 进化搜索自动发现装箱/组合结构新启发式 | L1, 延伸 C |
| AlphaEvolve: A Coding Agent for Scientific and Algorithmic Discovery | 2025 | 智能体演化代码改进矩阵乘法、数据结构与系统内核常数 | L1–L4, 延伸 C |
| Graph Algorithms on GPUs（cuGraph/最新基准研究） | 2021–2025 | BFS/SSSP/MST 在 GPU 上的并行实现与性能模型，验证"内存层次决定算法" | L7–L10 |
| Learned Index Structures 后续（RSMT/在线更新索引等） | 2021–2024 | 用模型替代 B 树/Trie 索引结构，重议"索引"的成本模型 | L5–L6, L11 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 动态数组与摊还分析 (L1) | CPython list、C++ vector、Rust Vec | 几何扩容与容量策略、`reserve`/`shrink_to_fit` API |
| 插入排序作小数组基例 (L2) | LLVM `llvm::sort`、pdqsort、Timsort(CPython/Java) | 混合排序：小分区切换插入排序、防退化模式检测 |
| 快排与三路切分 (L3) | Go `sort`、Rust std `sort_unstable`、RocksDB 内部排序 | 重复键处理与不稳定排序的性能取舍 |
| 堆与优先队列 (L4) | Linux 内核定时器/调度、Kafka 延迟队列、Tims Dataflow | 索引堆支持优先级更新，事件驱动调度 |
| BST / 红黑树 (L5–L6) | Java `TreeMap`、Linux CFS `rb_root_cached`、libstdc++ `std::map` | 有序映射与"取最小虚拟运行时间"的调度 |
| 并查集 (L9) | Boost.Graph、OpenCV 连通域、图分割/账户合并类实现 | 近线性连通性与 Kruskal 支撑结构 |
| Dijkstra / Bellman-Ford (L10) | OSRM、Valhalla、GraphHopper、PostGIS 路由 | 路网最短路 + A*/分层剪枝；负环检测用于依赖解析 |
| DFS / 拓扑排序 (L7–L8) | Bazel、Gradle、Spark DAGScheduler、pnpm 依赖解析 | 构建顺序、任务调度与环检测 |
| 强连通分量 (L8) | 编译器 CFG 循环识别、Julia 方法分派、包管理器求解器 | 缩点后在 DAG 上传播/排序 |
| 基数排序 / 三向字符串快排 (L11) | ClickHouse、PostgreSQL 排序算子、Lucene 段合并 | 字符串键线性排序与前缀压缩块 |
| Trie / 压缩 Trie (L11) | Lucene/ES 词典、FRR/BIRD 路由最长前缀匹配、输入法引擎 | 前缀检索、自动补全、路由表 |
| KMP / Boyer-Moore / Rabin-Karp (L12) | ripgrep、GNU grep、Suricata、Hyperscan | 单/多模式匹配与特征扫描 |
| 正则 NFA/DFA (L12) | RE2、Hyperscan、Flex/RE2C | 无回溯 NFA 保证线性时间（防 ReDoS） |
| Huffman / LZ 压缩 (L12) | zstd、LZ4、Brotli、RocksDB 块压缩、PNG/zlib | 变长前缀码与字典压缩的工程形态 |
| 网络流与最小割 (延伸 B) | OR-Tools、maxflow(Kolmogorov-Zabih)、图像分割、Bender 规划器 | 最大流最小割归约到匹配、分割与调度 |
