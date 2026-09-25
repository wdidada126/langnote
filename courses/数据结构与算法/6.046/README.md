# MIT 6.046: Design and Analysis of Algorithms 算法设计与分析

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | MIT 6.046J / 6.851J Design and Analysis of Algorithms |
| 学校 | Massachusetts Institute of Technology（与 6.046J 同为 EECS 课程） |
| 主讲 | Erik Demaine、Srini Devadas、Nancy Lynch（Spring 2015 版） |
| 教材 | Introduction to Algorithms（CLRS，4/E 优先）；课程自讲 notes 为主，参考 Kleinberg & Tardos《Algorithm Design》、Vazirani《Approximation Algorithms》、Motwani & Raghavan《Randomized Algorithms》 |
| csdiy 路径 | https://csdiy.wiki/数据结构与算法/6.046/ （页面更新 2023-01-18） |
| 最新期次 | csdiy 推荐 Spring 2015（OCW 全量：课件、视频、作业、考试） |
| 先修/语言/难度 | 先修 6.006 / CS61B / CS106B 或同等；板书与作业用 Python，但基本无编程作业；难度 🌟🌟🌟🌟🌟；预计学时 100h+ |
| 状态 | 骨架 |

## 为什么学

- 6.006 的后续课，重心从"现学现用"转向**举一反三地设计一套完备算法并证明它正确**，是算法能力的真正分水岭。
- 作业几乎全是设计 + 证明题：给出问题规格 → 你提算法 → 证正确性 → 分析复杂度 → 论证 tightness。这套训练直接对应研究、算法岗面试与竞赛。
- 覆盖 6.006 未展开的高级主题：最大流与归约、线性规划对偶、NP 完全性、近似算法、随机算法与概率分析、在线算法与竞争分析、博弈论与密码学算法（Nancy Lynch/Devadas 视角）。
- 学完基本覆盖"绝大多数考试与应聘"的算法题上限；再往上只需 6.854 高级算法。
- 三位图灵/院士级教师的讲法差异本身就是学习材料：Demaine 的构造性证明、Lynch 的下界与不可能性论证、Devadas 的随机化与密码学应用。

## 先修与知识联系

- 先修：6.006（数据结构与基础分析，见 ../6.006/README.md）、CS61B（实现经验）、6.042J / CS70（归纳证明、概率、图论基础）。
- 平行：CS170（同主题，Berkeley 版更偏理论与难解性，课程 notes 是极好补充）、Coursera Algorithms I&II（同主题的工程实现对照）。
- 向下：近似/随机分析支撑机器学习算法（CS229 的凸优化、随机梯度）、最大流与 LP 支撑数据库查询优化（15-445/CS186）、网络流与并行算法支撑 CS149/6.824、密码学部分衔接 6.858/CS161。
- 输出场景：算法设计与证明写作能力 → 论文/研究（与 17-803 实证研究方法互补：一边设计算法，一边评估算法的真实效果）。

## 最新年份讲义章节目录（Spring 2015，按课件主题整理为 22 讲）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论与设计范式：问题建模、分治与递推复习 | CLRS 2、4.1–4.5；lec1 notes |
| L2 | 贪心算法 I：区间调度、交换论证（exchange argument） | CLRS 16.1；KT 4 章 |
| L3 | 贪心算法 II：Huffman 编码、拟阵与贪心最优性刻画 | CLRS 16.2、16 章问题；拟阵补充阅读 |
| L4 | 生成树与图贪心：Kruskal/Prim、割性质与并查集 | CLRS 21、23 |
| L5 | 最短路综述与搜索启发式：Dijkstra/Bellman-Ford/A*、负权与负环 | CLRS 24.3–24.4 |
| L6 | 动态规划框架：最优子结构、状态设计与"DP=在 DAG 上最短路" | CLRS 15.1–15.3 |
| L7 | 动态规划应用：编辑距离/序列比对、背包、树形 DP、Viterbi | CLRS 15 章习题；KT 6 章 |
| L8 | 最大流 I：Ford-Fulkerson、残量网络、割与流的弱/强对偶、整数性 | CLRS 26.1–26.2 |
| L9 | 最大流 II：二分图匹配、带下界流、归约应用（项目选型、棒球淘汰） | CLRS 26.3；KT 7 章 |
| L10 | 线性规划与对偶：单纯形概览、LP 对偶定理、零和博弈等价 | CLRS 29；KT 7.5 |
| L11 | 计算难解性 I：问题归约、P/NP、Cook-Levin 定理 | CLRS 34.1–34.4 |
| L12 | 计算难解性 II：经典 NP 完全归约（团、独立集、顶点覆盖、哈密顿回路） | CLRS 34.5–34.6 |
| L13 | 计算难解性 III：数论与空间类（子集和、划分、PSPACE 概览） | CLRS 34.5、34.7 |
| L14 | 近似算法 I：装箱、顶点覆盖 2-近似、度量 TSP 与 Christofides | CLRS 35.1；Vazirani ch.1–3 |
| L15 | 近似算法 II：集合覆盖的 H_n 近似、LP 舍入与不可近似性 | Vazirani ch.5；CLRS 35.2 |
| L16 | 随机算法 I：概率空间、期望线性性、指示器变量、中位数选择 | CLRS 5、C.2–C.3；Motwani-Raghavan ch.1–3 |
| L17 | 随机算法 II：Markov/Chebyshev/Chernoff 界、加载问题、Skip List | CLRS C.2.2；MR ch.4–5 |
| L18 | 哈希与随机结构：通用哈希、Bloom Filter、随机化数据结构下界 | CLRS 11.3.3；lec notes |
| L19 | 在线算法与竞争分析：分页缓存、LRU 的竞争比、ski rental 下界 | CLRS 习题 18；Fiat-Werman ch.1–2 |
| L20 | 算法博弈论：纳什均衡、自私路由与 Price of Anarchy | KT 19 章；roughgarden 选读 |
| L21 | 密码学中的算法：数论、素性测试、RSA 与归约式安全证明 | CLRS 31； Katz-Lindell 选读 |
| L22 | 并行/量子视角与课程总结：work-span 模型、Brent 定理、难度谱系回顾 | CLRS 27（4/E）；客座讲稿 |

> 说明：6.046 每讲以"设计 + 证明"作业驱动，无编程作业；上表讲次划分依据 Spring 2015 OCW 课件主题顺序整理，不同学期合并/拆分略有差异（如 LP 与博弈可能并为一讲）。

## 课程资源（摘自 csdiy）

- 课程网站：MIT OCW 6.046 Design and Analysis of Algorithms, Spring 2015
- 课程视频：Spring 2015 全程录像（OCW）
- 课程教材：Introduction to Algorithms（CLRS）
- 课程作业：Spring 2015 的 problem set（以算法设计 + 正确性证明为主）
- 后续课程：6.854 Advanced Algorithms（进阶可选）
