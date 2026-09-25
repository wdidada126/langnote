# UCB CS170: Efficient Algorithms and Intractable Problems 高效算法与难解问题

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | UCB CS170: Efficient Algorithms and Intractable Problems（伯克利算法设计与分析） |
| 学校 | University of California, Berkeley |
| 主讲 | Dan Klein、Sushant Sachdeva 等（历年授课组；csdiy 页面未固定指名） |
| 教材 | 课程自写 notes（https://www.cs170.org/ 的 Course Notes，公认"证明浅显易懂、可当工具书"）；参考 Kleinberg & Tardos《Algorithm Design》、CLRS、Dasgupta《Algorithms》 |
| csdiy 路径 | https://csdiy.wiki/数据结构与算法/CS170/ （页面更新 2022-09-06） |
| 最新期次 | cs170.org 常年更新，近期为 Fall 2024 / Spring 2025 版（notes 与 hw 全部公开） |
| 先修/语言/难度 | 先修 CS61B、CS70；作业用 LaTeX 撰写；难度 🌟🌟🌟；预计学时 60 小时 |
| 状态 | 骨架 |

## 为什么学

- 伯克利的算法设计课，**比工程向课程更强调理论基础与复杂度分析**：既讲"怎么设计高效算法"，也讲"为什么某些问题不存在高效算法"。
- 内容谱系完整：分治、图算法、最短路、生成树、贪心、动态规划、并查集、线性规划、网络流、NP 完全、随机算法、哈希算法（csdiy 摘要所列全覆盖）。
- 课程 notes 写得极好，证明浅显易懂，非常适合当**工具书**反复查阅；与 6.046 互为最佳替代教材。
- 只有 13 次书面作业且推荐用 LaTeX 编写：一举训练算法证明表达 + 学术排版能力（衔接必学工具 LaTeX 章节）。
- 难解性与近似部分（NP-hard、gap 归约、PTAS/FPTAS）是后续机器学习理论、组合优化、系统调度论文的共同语言。

## 先修与知识联系

- 先修：CS61B（数据结构与实现，见 ../CS61B/README.md）、CS70（离散数学、归纳与递归证明、概率、图论基础）。
- 平行：6.006（Python 向，数据结构与分析细节更多）、6.046（设计 + 证明强度最高）、Coursera Algorithms I&II（同主题工程实现）。
- 向上：CS170 的概率方法与哈希 → CS189/CS229 的机器学习理论；LP 与对偶 → 15-445/CS186 查询优化与凸优化（EE364A）；NP 完全 → CS278 计算复杂性。
- 密码学与量子部分与 CS161/6.858 安全课程直接呼应。
- 与其他课的写法差异：CS170 的 hw 需要"用 LaTeX 讲清证明"，与 17-803 的"用统计讲清结论"构成研究写作的两极训练。

## 最新年份讲义章节目录（按 cs170.org Course Notes 主题顺序整理为 22 讲）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论与增长阶：算法、模型、Asymptotic 记号与递归式 | CS170 Notes §Introduction；CLRS Ch.3–4；HW1 发布 |
| L2 | 分治 I：主定理、大整数乘法、Strassen 矩阵乘法 | Notes §Divide & Conquer |
| L3 | 分治 II：最近点对、平面扫描与递归树 | Notes §D&C Applications |
| L4 | 下界与决策树：比较模型、排序 Ω(n log n)、对抗论证 | Notes §Lower Bounds；CLRS Ch.9 |
| L5 | 随机化排序与选择：Quicksort 分析、Randomized Select、Linear-time 期望 | Notes §Randomization I；HW2 |
| L6 | 图模型与遍历：BFS/DFS、连通性、二分性、拓扑排序 | Notes §Graphs I；CLRS Ch.22 |
| L7 | 权重图与 Dijkstra：贪心正确性、堆实现、A* 与启发式 | Notes §Graphs II；CLRS Ch.24 |
| L8 | 最小生成树与并查集：割性质、Kruskal/Prim、Union-Find 分析与路径压缩 | Notes §MST/Union-Find；CLRS Ch.21, 23；HW3 |
| L9 | 贪心方法论：区间调度、拟阵、交换论证与"何时贪心不成立" | Notes §Greedy；KT Ch.4 |
| L10 | 动态规划 I：有向无环图上的最短路、递归+memo、状态设计 | Notes §Dynamic Programming |
| L11 | 动态规划 II：2D DP（编辑距离/LCS）、背包与伪多项式、FPTAS | Notes §DP Applications；HW4 |
| L12 | 高级 DP：树形 DP、位掩码 DP、DP 与矩阵幂（计数类问题） | Notes §Advanced DP |
| L13 | 线性规划：可行域、顶点、单纯形直觉与建模技巧 | Notes §Linear Programming；KT Ch.7 |
| L14 | LP 对偶与博弈：互补松弛、零和博弈、用对偶证近似界 | Notes §Duality；HW5 |
| L15 | 网络流 I：最大流最小割、Edmonds-Karp/Dinic、整数性 | Notes §Network Flow；CLRS Ch.26 |
| L16 | 网络流 II：二分图匹配、König 定理、带下界流与归约目录 | Notes §Matching；HW6 |
| L17 | 难解性 I：P vs NP、归约、Cook-Levin 与 SAT 家族 | Notes §NP-Completeness；CLRS Ch.34；HW7 |
| L18 | 难解性 II：图类/数值类 NPC、强 NPC 与"遇到 NP-hard 怎么办" | Notes §Reductions；KT Ch.8 |
| L19 | 近似算法：顶点覆盖、集合覆盖、TSP、LP 舍入、PTAS/FPTAS 与不可近似性 | Notes §Approximation；HW8 |
| L20 | 概率工具与哈希：期望线性性、Chernoff 界、通用哈希、Bloom Filter、LSH | Notes §Randomization II；CLRS App.C, Ch.11；HW9 |
| L21 | 数论与密码学：模运算、GCD、费马/欧拉、RSA、离散对数、素性测试 | Notes §Cryptography；CLRS Ch.31；HW10 |
| L22 | 量子计算与其他前沿：qubit、Shor/Grover 概览、并行 work-span、总结 | Notes §Quantum Computing；HW11–HW13（含综合复习） |

> 说明：CS170 各学期以"单元（Unit）+ 13 次书面 hw"组织，上表把 notes 主题拆为 22 讲方便逐章记笔记；个别讲次（如 streaming、error-correcting codes、game theory）在部分学期为客座讲座，可按需增补 L23+。

## 课程资源（摘自 csdiy）

- 课程网站：https://cs170.org/
- 课程视频：https://www.bilibili.com/video/BV1BU4y1b7RK（B 站搬运）
- 课程教材：详见课程网站 notes
- 课程作业：13 次书面作业，推荐用 LaTeX 编写（作业模板见课程网站 hw/）
- 社区资源汇总：PKUFlyingPig/UCB-CS170
