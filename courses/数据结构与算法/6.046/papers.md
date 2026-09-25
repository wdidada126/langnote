# 6.046 参考文献与开源应用（骨架）

> 关联讲次对应 README 的 L1–L22。标题用英文原名，说明为中文意译；正式引用前请核对出处。

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Maximum Flow Through a Network (L. R. Ford & D. R. Fulkerson) | 1956 | 最大流与增广路径、最小割定理的原始形式 | L8–L9 |
| Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems (Edmonds & Karp) | 1972 | BFS 增广得到多项式时间最大流 | L8 |
| The Complexity of Theorem-Proving Procedures (S. A. Cook) | 1971 | 首个 NP 完全结果（SAT），奠定难解性理论 | L11 |
| Reducibility Among Combinatorial Problems (R. M. Karp) | 1972 | 21 个 NP 完全问题与归约网络 | L11–L13 |
| Computers and Intractability (Garey & Johnson) [专著] | 1979 | 数百个 NPC 问题与归约手册，强/弱 NP 完全分类 | L13 |
| Programming in Linear Structures (G. B. Dantzig) | 1947 | 线性规划与单纯形方法 | L10 |
| Non-Cooperative Games (J. F. Nash) | 1950 | 纳什均衡存在性定理 | L20 |
| How Bad Is Selfish Routing? (Roughgarden & Tardos) | 2002 | 自私路由 PoA 上界与 Braess 现象的算法分析 | L20 |
| Near-Optimal Bin Packing Algorithms (D. S. Johnson) [博士论文/算法分析] | 1973 | 装箱近似比与下界的经典分析 | L14 |
| Worst-Case Analysis of a New Heuristic for the TSP (N. Christofides) | 1976 | 度量 TSP 的 3/2 近似（MST + 完美匹配） | L14 |
| Tight Bounds on the Approximation of the Set Covering Problem (L. Lovász) | 1979 | 集合覆盖贪心的 ln n 近似与匹配下界 | L15 |
| Improved Approximation Algorithms for MAX-CUT Using Randomization and Semidefinite Programming (Goemans & Williamson) | 1995 | SDP + 随机舍入的 0.878 近似，近似算法里程碑 | L15, L17 |
| Self-Adjusting Binary Search Trees (Sleator & Tarjan) | 1985 | 摊还分析与伸展树，动态最优性 | L19, L6 |
| Amortized Efficiency of List Update and Rearrangement (Sleator & Tarjan) / Competitive Paging (Sleator–Tarjan; Fiat et al.) | 1985–1991 | 竞争分析与分页 LRU 的紧界、概率方法下界 | L19 |
| Probabilistic Algorithm for Testing Primality (M. O. Rabin) | 1980 | 随机化素性测试及其错误概率界 | L16, L21 |
| A Method for Obtaining Digital Signatures and Public-Key Cryptosystems (Rivest, Shamir & Adleman) | 1978 | 公钥密码与"破译 ⇔ 分解"的归约式安全论证 | L21 |
| Smoothed Analysis of Algorithms: Why the Simplex Algorithm in Practice (Spielman & Teng) | 2004 | 平滑分析：解释单纯形等算法的实践高性能 | L10, L16 |
| Theoretical Foundations of Randomized Algorithms (Motwani & Raghavan) [专著] | 1995 | 随机算法系统化教材，集中不等式工具箱 | L16–L18 |

## 近 5 年文献（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Beyond the Worst-Case Analysis of Algorithms (Blum 编, Cambridge) [专著] | 2021 | 学习增强/平均分析等"后最坏情形"范式的系统总结 | L16–L20 |
| Negative-Weight Single-Source Shortest Paths in Near-Linear Time (Bernstein, Nanongkai, Wulff-Nilsen) | 2022 | 负权 SSSP 近线性，打破长期停滞的复杂度边界 | L5 |
| 近线性时间最大流新进展（Yang 2020–2021；Brand 等 2022–2023, FOCS/SODA） | 2021–2023 | 最大流逼近"读一遍输入"的成本，推动图算法统一框架 | L8–L10 |
| Densest Subgraph in Near-Linear Time (Bohlin et al., KDD) | 2022 | 精确稠密子图近线性算法，社区挖掘基础算子落地 | L9, L19 |
| Discovering Faster Matrix Multiplication with Reinforcement Learning (AlphaTensor) / 2.371552 上界改进（Duan–Wu–Zhou） | 2022–2023 | 自动搜索算法 + 手工理论突破双线上抬基线 | L1, L22 |
| FunSearch: Mathematical Discoveries via Program Search (Nature) | 2024 | LLM 驱动搜索组合优化启发式，自动"设计算法" | L2, L14, L16 |
| Proving Optimality Gaps: Fine-Grained Conditional Lower Bounds 综述系列（Abboud、Bringmann 等） | 2021–2024 | 用 SETH/OGV 等假设给出 O(n²)、3SUM 类问题的条件性 tight 下界 | L11–L13, L18 |
| AlphaEvolve: Agentic Algorithm Discovery (DeepMind) | 2025 | 智能体演化算法/数据结构，改进矩阵乘法与在线问题常数 | L2–L15 |
| Differential Privacy Composition 与在线决策新界（Rényi DP、RDP 系列后续） | 2021–2023 | 概率集中不等式在隐私保护算法中的组合界 | L17, L19 |
| 学习增强在线算法（Learning-Augmented Caching/Ski Rental 系列） | 2021–2024 | 用 ML 预测改善竞争比，同时保留最坏界保证 | L19 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 贪心 + 交换论证 (L2–L4) | Spark/Hive 调度器、Kubernetes 抢占策略 | 优先级抢占式调度的最优性直觉与代价证明 |
| 最短路/启发式 (L5) | OSRM、Valhalla、Valhalla 的 MLD 分层 | 分层预处理把 Dijkstra 变成毫秒级查询 |
| 动态规划 (L6–L7) | Stan/PyMC 的 HMM、edlib/SeqAlign（生物）、Diff/P4 编译 | 编辑距离与 Viterbi 是版本比对与基因比对内核 |
| 最大流与归约 (L8–L9) | OR-Tools CP-SAT/网络流、Booyuk/LEMON、maxflow(Kolmogorov-Zabih) | 图像去噪（min-cut）、匹配与资源分派 |
| 线性规划与对偶 (L10) | HiGHS、GLPK、OR-Tools GLOP、Gurobi 开源接口 | 影子价格与互补松弛用于容量规划分析 |
| NP 完全与求解器 (L11–L13) | CaDiCaL、Kissat、Z3、OR-Tools SAT | 归约工程：把问题编码成 CNF 交给现代求解器 |
| 近似算法 (L14–L15) | METIS/KaHIP 图分割、k-means++ 实现、Flink 负载均衡 | 大规模划分与聚类使用有保证的近似 |
| 随机化与集中不等式 (L16–L17) | HyperLogLog（Redis/ClickHouse/BigQuery）、MinHash/LSH（datasketch） | 基数估计与相似度检索的正确性来自概率界 |
| 通用哈希/Bloom Filter (L18) | RocksDB/Cassandra/ScyllaDB、Chrome Safe Browsing | SST 查找前的存在性过滤、假阳率参数化 |
| 在线算法与竞争分析 (L19) | Caffeine/SIEVE/ARC 缓存、Kafka/Redis 淘汰策略、CDN LRU | 竞争比是缓存策略评估的事实标准 |
| 算法博弈论与机制设计 (L20) | Ad Exchange/拍卖系统、Kubernetes 优先级调度、内容分发定价 | PoA 分析指导资源竞价与公平性设计 |
| 数论与密码算法 (L21) | OpenSSL、libsodium、BoringSSL、GnuPG | Miller-Rabin 密钥生成、RSA/ECC 参数校验 |
| work-span 与并行调度 (L22) | Cilk/Cilkplus、OpenMP、LLP (Legion)、Spark 调度 | 跨度决定加速比上界，work-stealing 实现 |
