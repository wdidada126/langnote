# 6.006 参考文献：经典论文、近五年进展与开源映射

> 讲次编号对应本课程 README 的 L1–L26（Fall 2011）；pXX 指 projects/ 下配套项目。标题保留英文原名，说明为中文意译；正式引用前请核对出处卷期。

## 一、经典论文（按讲次/项目映射）

| 论文 | 年份 | 一句话贡献 | 关联 |
| --- | --- | --- | --- |
| A Note on Two Problems in Connexion with Graphs (R. W. Dijkstra) | 1959 | 单源最短路（Dijkstra）与最小生成树（Prim 之原形）两篇合一，图算法奠基短文 | L11, p05 |
| On the Shortest Spanning Subtree of a Graph (J. B. Kruskal) | 1956 | 贪心 MST；现代实现靠并查集判环 | L20, p05/p07 延伸 |
| A Programming Algorithm for Two Traveling Salesman Problems (M. Held & R. M. Karp) | 1962 | 子集 DP 解 TSP——"状态压缩 DP"开山 | L08, p06/p10 |
| An Algorithm for the Organization of Information (G. M. Adelson-Velskii & E. M. Landis) | 1962 | AVL 树：第一个自平衡 BST，旋转与高度界 | L15 |
| On a Routing Problem (R. Bellman) / Ford–Fulkerson 网络流系列 (L. R. Ford & D. R. Fulkerson, 1956) | 1956–1958 | 负权最短路（Bellman-Ford）与最大流增广路径/最小割定理 | p05, p09 |
| Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems (J. Edmonds & R. M. Karp) | 1972 | BFS 选最短路增广（Edmonds-Karp），首个多项式最大流 | p09 |
| A Special Program for Efficient Maximum Matching in Bipartite Graphs (J. E. Hopcroft & R. M. Karp) | 1973 | 二分图匹配 O(E√V)，分层增广（BFS 思想复用） | p09 延伸 |
| The Complexity of Theorem-Proving Procedures (S. A. Cook) | 1971 | 首证 SAT NP 完全（Cook-Levin 定理） | p10 |
| Reducibility Among Combinatorial Problems (R. M. Karp) | 1972 | 21 个 NP 完全问题与归约网络，NPC 理论成型 | p10 |
| Computers and Intractability: A Guide to the Theory of NP-Completeness (M. R. Garey & D. S. Johnson) [专著] | 1979 | NPC 归约手册与"强/弱 NP 完全"分类 | p10 |
| Organization and Maintenance of Large Ordered Indices (R. Bayer & E. McCreight) | 1972 | B 树原文：磁盘多路平衡索引 | L16 |
| Bloom Filters: Space/Time Trade-offs in Hash Coding with Allowable Errors (B. H. Bloom) | 1970 | 概率型成员查询，假阳性可量化——现代粗筛结构之父 | L17, p03 |
| Machine Solutions of the Prefix Problem (P. van Emde Boas, P. Kaijanpaa & M. Telenmaa) | 1977 | vEB 树：整数宇宙 O(log log u) 前缀/后继 | L23 |
| Efficient String Matching: An Aid to Bibliographic Search (A. V. Aho & M. J. Corasick) | 1975 | AC 自动机：多模式线性匹配 | L25 |
| Fast Pattern Matching in Strings (D. E. Knuth, J. H. Morris & V. R. Pratt) | 1977 | KMP：失败函数与不回退指针 | L24 |
| Efficient Pattern Matching Algorithms (M. O. Rabin) / "Randomized Pattern-Searching Algorithms" (R. M. Karp & M. O. Rabin, 1973/1987) | 1973/1987 | Rabin-Karp 滚动哈希：随机化进入字符串算法 | L24, L26 |
| Algorithm 614: Toward Optimal Organization of String Data for a Computer Concordance (A. J. Perkins; 推广为 Manber & Myers) | 1993 | 后缀数组 + 倍增排序（O(n log n)），信息检索基石 | L26 |
| Amortized Efficiency of List Update and Rearrangement (D. D. Sleator & R. E. Tarjan) | 1985 | 列表更新的摊还/竞争双重分析范式 | L19, L21, p11 |
| Self-Adjusting Binary Search Trees (D. D. Sleator & R. E. Tarjan) | 1985 | 伸展树：势函数 Φ=Σlog(size) 的摊还杰作 | L21 |
| Competitive Memory Allocation (Sleator & Tarjan, 1985) / Competitive Paging (A. Fiat et al., 1991) | 1985/1991 | 分页 k-竞争与随机分页 O(log k) 竞争——在线算法两场战役 | L22, p11 |
| An Optimal Algorithm for Approximate Nearest Neighbor (D. Eppstein et al.)/ y-fast 相关 (J. L. Bentley & A. C. Yao, 1976) | 1976–1983 | 前缀问题的分桶谱系，vEB 的近亲们 | L23 延伸 |
| A Formal Basis for the Heuristic Determination of Minimum Cost Paths (P. E. Hart, N. J. Nilsson & B. Raphael) | 1968 | A*：Dijkstra + 相容启发式；可采纳性定理 | L11/L12 延伸, p05 |
| Probabilistic Algorithm for Testing Primality (M. O. Rabin) | 1980 | 蒙特卡洛随机算法代表：错误概率可任意压小 | L26 延伸 |
| Randomized Algorithms (R. Motwani & P. Raghavan) [专著] | 1995 | 随机化算法系统化教材（集中不等式工具箱） | L26 |
| Consistent Hashing and Random Trees (D. Karger, E. Lehman, T. Leighton, R. Panigrahy, M. Levine & D. Lewin) | 1997 | 一致性哈希：负载均衡 + 动态成员，分布式哈希的算法内核 | L07/L17 延伸, 6.824 |
| Introduction to Algorithms (T. H. Cormen, C. E. Leiserson, R. L. Rivest & C. Stein, CLRS 3/E–4/E) [教材] | 1990–2022 | 本课正文教材；4/E 增 van Emde Boas 正文与在线章节 | 全课 |

## 二、近五年文献与工程里程碑（2021–2026）

| 条目 | 年份 | 一句话贡献 | 关联 |
| --- | --- | --- | --- |
| Maximum Flow by Augmenting Paths in Nearly-Linear Time (L. Chen, R. Kyng, Y. P. Liu, R. Peng, J. Gao & S. Mao, STOC 2022 最佳论文；同季 min-cost flow 近线性系列) | 2022 | 最大流/最小费用流进入近线性时代，Ford-Fulkerson 谱系的世纪级推进 | p09 |
| Beyond the Worst-Case Analysis of Algorithms (T. Roughgarden 编, Cambridge) [专著] | 2021 | 平滑分析、学习辅助、数据相关界等"后最坏情形"方法集结 | L21, L22, L26 |
| AlphaDev: Faster Sort Algorithms and the Impact on Computing (D. Mankowitz et al., Nature) | 2023 | 强化学习搜索排序网络：发现少于人工的交换网络，短序列超越人类最优 | L04, L05, p01 |
| FunSearch: Mathematical Discoveries from Program Search with LLMs (B. Romera-Paredes et al., Nature) | 2024 | LLM 生成候选程序 + 评估器回环，首次由 AI 发现新的组合算法构造（cap set 改进下界） | L26, p04 精神 |
| AlphaEvolve: A Coding Evolutionary Agent for Algorithm Discovery (DeepMind) | 2025 | 进化式代码智能体：4×4 复矩阵乘法 48 次标量乘（破 Strassen 1969 的 49），刷新 50+ 开放问题之一 | L04, L26 |
| A Refined Laser Method and Faster Matrix Multiplication (T. Duan, S. Wu, J. Zhou, Q. J. Liu 等) | 2023/2024 | ω < 2.371552：分治+组合构造（激光法）的最新推进，Strassen 思想的渐近极限 | L04 |
| Linux 6.6 EEVDF 调度器替换 CFS（Linux 内核社区，工程里程碑） | 2023 | 虚拟截止时间红黑树调度：L14/L18 结构 + 在线公平性思想的生产部署 | L14–L18, L21 |
| RocksDB/Flash 生态对自适应布隆与哈希索引的持续更新（如 Elastic 8.x/9.x 索引结构调优文档线） | 2021–2026 | Bloom/哈希粗筛 + 惰性重建的"教科书参数"在云存储成本模型下反复再平衡 | L17, L19 |

> 诚实注记：上表中 AlphaEvolve 的 48 次乘法结果（2025）是对 Strassen 家族的具体改进；FunSearch/AlphaEvolve 属"AI 辅助算法设计"新范式而非传统论文，引用时建议核对 Nature/DeepMind 官方版本页。

## 三、知识点 ↔ 开源项目映射速查

| 知识点（讲次） | 开源实现 | 备注 |
| --- | --- | --- |
| 二分与有序数组（L03/L14） | CPython `bisect` | 文档即复杂度承诺；`insort` 的 O(n) 搬移 |
| 堆与优先队列（L18） | CPython `heapq`；Go `container/heap` | `heapq.merge` = k 路归并（L04）；`nlargest` O(n log k) |
| 归并/Timsort（L04/L05） | CPython `list.sort`、Java `TimSort`、GNU coreutils `sort` | run 检测 + 二元插入 + galloping |
| 动态数组均摊（L19） | CPython `listobject.c`、Go `growslice` | 倍增/1.125× 策略源码注释含摊还论证 |
| 栈队列/双端（L06） | CPython `collections.deque`、`asyncio` 事件循环、LMAX RingBuffer | 块链 deque 兼顾 O(1) 两端与缓存 |
| 哈希表（L07/L17） | CPython `dict`、Go `map`、Java `HashMap`（树化桶）、Redis dict+渐进 rehash | 通用族/盐/惰性重建全谱系 |
| Bloom Filter（L17） | LevelDB/RocksDB `filter_block`、Cassandra、Chrome Safe Browsing | 1% 假阳、1.44 bit/元素 级 |
| 平衡树容器（L14–L16） | Linux 内核 `rbtree`（CFS/EEVDF）、Java `TreeMap`、C++ `std::map`、`sortedcontainers` | 最坏 O(log n) 的有序字典 |
| 并查集（L20） | NetworkX `union_find`、scipy `connected_components`、OpenCV CCL | Kruskal 内衬 |
| 图遍历/最短路（L09–L11） | NetworkX（BFS/DFS/Dijkstra/Johnson）、OSRM/Valhalla/GraphHopper、FRR OSPFd | 城市级路由 = Dijkstra + 分层剪枝 |
| 动态规划（L08） | git/`xdiff`（Myers）、Biopython（Smith-Waterman）、Kaldi 解码图 | 编辑距离/DAG 最短路 |
| 贪心/Huffman（L11/L18） | Zstandard/brotli 熵编码层、H.26x VLC | 前缀码工程 |
| 在线/缓存（L21/L22） | Redis LRU/LFU 近似、Caffeine TinyLFU、Linux `list_lru`/`mm` | 竞争分析的工程化身 |
| Trie/前缀（L25） | Linux FIB trie、eBPF LPM trie、pyahocorasick、Lucene FST | 路由与多模式匹配 |
| 后缀数组/字符串（L24/L26） | libdivsufsort、bwa/minimap2、ripgrep（fastsearch/twoway）、mummer | 检索与基因组 |
| 拓扑排序/调度（L10） | GNU Make、Airflow/BSP 超步、Gradle 依赖图 | DAG 即调度 |
| 随机化（L26） | CPython 哈希盐、ECMP 哈希选路、Redis 跳表/近似 LRU 采样 | 随机进算法，对手就哑 |
| vEB/位分层（L23） | Linux 位图 API + 两级 summary、RocksDB/BRIN 范围摘要 | 完整 vEB 罕见，思想遍地 |

## 四、阅读建议

1. 先读课程 notes（OCW L1–L26 板书）对应讲，再查 CLRS 章节，最后按需回到本文献表找"原始出处"。
2. 经典论文优先精读四篇短而完整：Dijkstra 1959（2 页）、Bloom 1970（3 页）、Kruskal 1956（1 页）、Aho-Corasick 1975（前 4 页）——都附 OCW/ACM 链接可查。
3. 近五年条目用于"讲完即聊"：L04 讲完读 AlphaDev/FunSearch 报道，L22 讲完读 Caffeine 设计文档，L15–L18 讲完读 EEVDF 提交邮件列表（Jonathan Corbet 三篇博客）。
