# CS170 参考文献与开源应用（骨架）

> 关联讲次对应 README/outline 的 L1–L22。与 6.046 有主题重叠，此处侧重"难解性、随机化、近似"三条线的源头论文。

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The Complexity of Theorem-Proving Procedures (S. A. Cook) | 1971 | 首个 NP 完全定理（SAT），难解性理论的起点 | L17 |
| Reducibility Among Combinatorial Problems (R. M. Karp) | 1972 | 21 个 NPC 问题，建立"归约网络"方法论 | L17–L18 |
| Sorting and Searching, TAOCP Vol.3 (D. E. Knuth) | 1973 | 决策树下界与排序分析的系统化整理 | L4 |
| Computers and Intractability: A Guide to the Theory of NP-Completeness (Garey & Johnson) | 1979 | 强/弱 NP 完全分类与数百个归约手册 | L18 |
| Exact Exponential Algorithms (Fomin & Grandoni 等的测量与分支系列) | 2006–2009 | "指数但要更快"：精确算法的分支/度规分析与空间权衡 | L12, L18 |
| A Dynamic Programming Approach to Sequencing Problems (Held & Karp) | 1962 | 位掩码 DP 求解 TSP，O(n²2ⁿ) 的教科书例 | L12 |
| Linear Programming and Extensions (G. B. Dantzig) | 1963 | 线性规划与单纯形方法的经典体系 | L13–L14 |
| Maximum Flow Through a Network (Ford & Fulkerson) | 1956 | 最大流最小割定理与增广路径方法 | L15 |
| Algorithm 64: Quicksort (Hoare, 1961) / Engineering a Sort Function (Bentley & McIlroy, 1993) | 1961/1993 | 快速排序的理论起点与工业级实现 | L5 |
| How Bad Is Selfish Routing? (Roughgarden & Tardos) | 2002 | 网络博弈中的 Price of Anarchy 分析方法 | L22 延伸 |
| Worst-Case Analysis of a New Heuristic for the Travelling Salesman Problem (N. Christofides) | 1976 | 度量 TSP 的 3/2 近似（MST + 最小完美匹配） | L19 |
| Tight Bounds on the Approximation of the Set Covering Problem (L. Lovász) | 1979 | 集合覆盖 ln n 近似与匹配下界 | L19 |
| Improved Approximation Algorithms for Maximum Cut and Satisfiability Problems Using Semidefinite Programming (Goemans & Williamson) | 1995 | SDP + 随机超平面舍入的 0.878 MAX-CUT 近似 | L19, L20 |
| Universal Classes of Hash Functions (Carter & Wegman) | 1979 | 通用哈希族定义，随机化数据结构分析基石 | L20 |
| Space/Time Trade-offs in Hash Coding with Allowable Errors (B. H. Bloom) | 1970 | Bloom Filter：以可控假阳率换空间 | L20 |
| Min-wise Sketching / Locality-Sensitive Hashing (Indyk & Motwani) | 1998 | 相似近似最近邻的 LSH 框架 | L20 |
| Probabilistic Algorithm for Testing Primality (M. O. Rabin) | 1980 | 素性测试与其错误概率界 | L21 |
| A Method for Obtaining Digital Signatures and Public-Key Cryptosystems (Rivest, Shamir & Adleman) | 1978 | RSA：把"破译"归约到"分解"的安全证明范式 | L21 |
| Algorithms for Quantum Computation: Shor (1994) / Grover (1996) | 1994/1996 | 量子周期查找与平方根加速搜索 | L22 |
| Smoothed Analysis of Algorithms: Why the Simplex Algorithm in Practice (Spielman & Teng) | 2004 | 解释单纯形等最坏界悲观算法为何实践中很快 | L13, L20 |

## 近 5 年文献（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Beyond the Worst-Case Analysis of Algorithms (Blum 编) [专著] | 2021 | 平均情形、平滑分析与学习增强算法的统一图景 | L4, L20 |
| Negative-Weight SSSP in Near-Linear Time (Bernstein, Nanongkai, Wulff-Nilsen) | 2022 | 负权单源最短路近线性，改写"最短路复杂度地图" | L7, L15 |
| 近线性时间最大流/最小割系列（Yang；Brand、Nanongkai 等） | 2021–2023 | 图算法基础问题的多项式因子级改进 | L15–L16 |
| Exact Densest Subgraph in Near-Linear Time (Bohlin et al.) | 2022 | 稠密子图从"只有近似"到近线性精确解，社区挖掘落地 | L19 |
| Matrix Multiplication Exponent < 2.371552（Duan, Wu, Zhou） | 2023 | 激光方法改进，L2/L4 类下界叙事的具体刷新 | L2 |
| AlphaTensor: Discovering Faster Matrix Multiplication Algorithms (Nature) | 2022 | 把算法发现变成可学习的搜索问题 | L1–L2, L19 |
| FunSearch: Mathematics via Program Search with LLMs (Nature) | 2024 | 自动发现组合优化启发式（装箱、Cap set） | L9, L18–L19 |
| AlphaEvolve: Agentic Algorithm/Evolution Discovery | 2025 | 智能体自动改写实现与算法结构，改进数学与系统常数 | L1–L5, L19 |
| Fine-Grained Complexity: SETH-based Conditional Lower Bounds 综述与新结果（Abboud、Bringmann、Hernich 等） | 2021–2025 | 用 SETH 给 O(n²⁻ε)、2^(n-o(n)) 类下界，解释"为什么算法无法更快" | L4, L12, L18 |
| Unique Games 假设下的最优近似壁垒系列（Khot、Miners、Sawin 等） | 2021–2025 | 在 UG 假设下确认若干问题的最优近似比阈值 | L19 |
| Learned/Robust Combinatorial Optimization（ML-guided branch & bound 系列） | 2021–2025 | 机器学习加速求解器分支决策，保留正确性 | L16, L18 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 下界与决策树 (L4) | SQLite/PostgreSQL 查询优化器 | 排序/连接的下界决定算子选择策略 |
| 随机化算法与集中界 (L5, L20) | Redis HyperLogLog、ClickHouse、Spark approximate count-distinct | 概率计数与误差界直接来自 Chernoff 型论证 |
| 图遍历/BFS-DFS (L6) | NetworkX、igraph、Neo4j 遍历引擎 | 遍历骨架、拓扑排序用于依赖与影响分析 |
| Dijkstra/A* (L7) | OSRM、Valhalla、Recast/Detour（游戏寻路） | 分层预处理 + 启发式把最短路做到毫秒级 |
| 并查集 (L8) | Kruskal 实现、图像连通域（OpenCV）、网络可达性分析 | α(n) 级合并是大规模连通性基础 |
| 贪心与拟阵 (L9) | Hive/Spark 的调度贪心、编译器寄存器分配（图着色贪心） | 交换论证支撑调度策略合理性说明 |
| 动态规划 (L10–L12) | edlib/Needleman-Wunsch 比对、Stan/PyMC 的 Viterbi、diff 工具 | 编辑距离/序列 DP 是生物与文本工具内核 |
| 位掩码与精确指数算法 (L12, L18) | OR-Tools CP-SAT、Z3、Concorde TSP 求解器 | 指数算法优化常数与剪枝，解决真实规模实例 |
| LP 与对偶 (L13–L14) | HiGHS、GLPK、OR-Tools GLOP（MIP 求解器的 LP 松弛与对偶单纯形） | 对偶给界、影子价格用于容量/成本敏感性分析 |
| 网络流与匹配 (L15–L16) | LEMON、NetworkX 二部匹配、OR-Tools、图像分割 maxflow 库 | 匹配/分割/资源分派归约为最大流 |
| NP 完全与求解器 (L17–L18) | CaDiCaL、Kissat、MiniSat 生态；GCP/编码问题归约 | 编码成 CNF 是现代"难问题通用解法" |
| 近似算法 (L19) | METIS/KaHIP、k-means++、Flink/Spark 负载均衡 | 有保证的近似比是系统划分与聚类的依据 |
| 哈希与 Bloom Filter、LSH (L20) | RocksDB/Cassandra/ScyllaDB、HNSWlib/Faiss 的 LSH/ANN | 假阳率与相似检索的参数化设计 |
| 数论与密码 (L21) | OpenSSL/BoringSSL、libsodium、GnuPG、Let's Encrypt 栈 | 素性测试、模逆、RSA/ECC 参数生成 |
| 量子与并行 (L22) | Qiskit、Cilk/TBB、GPU 图算法（cuGraph） | work-span 分析指导并行化可行性判断 |
