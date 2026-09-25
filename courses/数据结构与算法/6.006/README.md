# MIT 6.006: Introduction to Algorithms 算法导论（【CORE】）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | MIT 6.006: Introduction to Algorithms（MIT EECS 系） |
| 学校 | Massachusetts Institute of Technology |
| 主讲 | Erik Demaine、Srini Devadas（Fall 2011 版） |
| 教材 | Introduction to Algorithms（CLRS，Cormen/Leiserson/Rivest/Stein，3/E 或 4/E）；课程另有完整板书 notes 与 Python 代码 |
| csdiy 路径 | https://csdiy.wiki/数据结构与算法/6.006/ （页面更新 2024-04-14） |
| 最新期次 | csdiy 推荐 Fall 2011（OCW 全量公开：课件 + 视频 + 作业 + 考试）；OCW 亦存 Spring 2020 新版（Demaine & Justin Solomon），可作补充 |
| 先修/语言/难度 | 先修计算机导论（CS50/CS61A 或同等）；语言 Python；难度 🌟🌟🌟🌟🌟；预计学时 100h+ |
| 状态 | 全量（2026-09）：notes/ 26 讲中文笔记、papers/papers.md 论文与开源映射、projects/ 11 个配套项目均已完成 |

## 为什么学

- MIT-EECS 的瑰宝课，授课者之一是算法界奇才 Erik Demaine；讲解比 Stanford CS106B/X 更细，**弥补了纯数据结构课在算法侧的不足**。
- 以 Python 为语言，把"数据结构实现 + 复杂度分析 + 正确性论证"三者放进同一讲次，学完能同时具备写与证的能力。
- 覆盖 AVL 树、摊还分析、van Emde Boas 树、字符串匹配与后缀数组等**多数入门课略过的高价值主题**，对面试与科研都直接受益。
- 全资料开源（OCW），含 problem set、proficiency exercise、期中期末与回放视频，适合严格自学闭环。
- 公认难点：证明密度高、节奏快。csdiy 明示"出了名的难，需要做好心理准备"，因此本课程按全量标准逐讲做笔记。

## 先修与知识联系

| 方向 | 关联课程/知识 |
| --- | --- |
| 先修 | CS50 / CS61A（编程与递归基础）、CS61B（数据结构与 Java 实现经验）、CS70 / 6.042J（离散数学、归纳证明、概率） |
| 上游输入 | 6.042J 的渐近分析与递推关系直接用于本课程的 Θ 分析与主定理 |
| 直接后继 | 6.046（算法设计与分析，侧重"设计 + 证明"）、6.854（高级算法）、CS170（高效算法与难解问题） |
| 平级互补 | Stanford CS106B/X（C++ 数据结构实现）、Coursera Algorithms I&II（Sedgewick，工程实现与代码质量） |
| 向下支撑 | CSAPP/CS110：数组与链表、哈希、缓存局部性的机器级解释；15-445：B+ 树与索引、外部排序；CS186：join 与查询优化的算法基础 |
| 面向 AI 线 | 6.006 的概率方法、动态规划与图搜索 → CS188（搜索与规划）、机器学习算法分析 |

## 最新年份讲义全章节目录（Fall 2011，26 讲；按 OCW 讲授主题整理）

### Part A｜基础、Python 与渐近分析（L1–L7）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：算法与计算问题、Python 检索示例（DNA 序列匹配） | CLRS 1.1–1.2；course notes L1；Proficiency Exercise 1 发布 |
| L2 | Python 数据结构：list/tuple/dict/set、切片、位与字符串表示 | CLRS 附录 B；notes L2；PSet1 发布 |
| L3 | 渐近效率：O/Ω/Θ/O、增长阶、循环与递归的成本模型 | CLRS 3.1–3.2；notes L3 |
| L4 | 递归函数与归并排序：递归树、递推关系、主定理 | CLRS 2.3、4.1–4.4；notes L4；PSet1 截止 |
| L5 | 分治与排序 I：插入排序、正确性不变式、数组与链表实现对比 | CLRS 2.1；notes L5 |
| L6 | 栈、队列与双端队列（Deque）：接口设计与 O(1) 两端操作 | CLRS 10.1；notes L6；PSet2 发布 |
| L7 | 映射与哈希：dict 的实现、分离链与开放寻址 | CLRS 11.1–11.4；notes L7 |

### Part B｜动态规划与图搜索（L8–L13）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L8 | 除法与动态规划：Fibonacci 的四种写法、重叠子问题与 memoization | CLRS 15.1；notes L8 |
| L9 | 图遍历 I：深度优先搜索、递归栈、连通性与拓扑直觉 | CLRS 22.1、22.3；notes L9 |
| L10 | 图遍历 II：广度优先搜索与拓扑排序、分层图 | CLRS 22.2；notes L10；PSet2 截止 |
| L11 | 单源最短路：Dijkstra 与贪心正确性、优先级队列结合 | CLRS 24.3；notes L11 |
| L12 | 博弈搜索：Minimax 与 Alpha-Beta 剪枝（井字棋/国际象棋） | CLRS 补充阅读；AIMA 5 章（跨课程联系 CS188） |
| L13 | 习题课与期中复习：PSet3 讲解、复杂度证明常见错误 | PSet3；往年期中试题（OCW 公开） |

### Part C｜高级数据结构与摊还分析（L14–L23）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L14 | 二叉搜索树：结构性质、查找/插入/删除、有序遍历 | CLRS 12；notes L14；PSet3 发布 |
| L15 | 平衡二叉树：AVL 树与旋转、高度界证明 | CLRS 13.1（对照红黑）；notes L15 |
| L16 | 平衡树的工程实践：Java TreeMap/C++ std::map、B 树与外部存储 | CLRS 18.2；notes L16 |
| L17 | 通用哈希与惰性哈希、Bloom Filter | CLRS 11.3.3、附录 C 概率；notes L17 |
| L18 | 堆与优先队列：heapify 线性时间、堆排序 | CLRS 6；notes L18；PSet3 截止 |
| L19 | 摊还分析：聚合法、记账法与势函数法 | CLRS 17.1–17.4；notes L19 |
| L20 | 并查集（Disjoint Set Union）：按秩合并、路径压缩与逆 Ackermann 界 | CLRS 21；notes L20 |
| L21 | 在线算法与自组织表：Move-to-Front、Transpose、Splay 树 | CLRS 问题 12-1；notes L21；PSet4 发布 |
| L22 | 缓存与分页：LRU/LFU、竞争分析与缺页下界 | notes L22；Sleator-Tarjan 动态缓存论文 |
| L23 | van Emde Boas 树：整数宇宙上的 O(log log u) 前驱/后继 | CLRS 问题 20-2；notes L23 |

### Part D｜字符串、随机化与综合（L24–L26）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L24 | 字符串匹配：Rabin-Karp 滚动哈希、KMP 的前缀函数 | CLRS 32.1–32.2；notes L24；PSet4 截止 |
| L25 | 模式匹配与 Trie：多模式匹配、字典树压缩（Aho-Corasick 概览） | CLRS 32.4；notes L25 |
| L26 | 后缀数组与字符串排序（基数排序）、随机化算法与期末复习 | CLRS 8.3、33.4；notes L26；期末试题 |

> Fall 2011 为 2 次课/周 × 13 周共 26 讲，另含 2 次 proficiency exercise（Python/算法基础自测）、4 个 Problem Set、期中与期末（OCW 全部公开题目与解答）。个别讲次标题为中文意译，以 OCW 当期页面为准。

## 课程资源（摘自 csdiy）

- 课程网站：MIT OCW 6.006 Introduction to Algorithms, Fall 2011
- 课程视频：OCW Fall 2011 全程录像
- 课程教材：Introduction to Algorithms（CLRS）
- 课程作业：Fall 2011 的 Problem Sets、Proficiency Exercises、考试
- 学习建议：与 CS61B 对照学习"同一结构的两种语言实现"，再进 6.046 做设计与证明训练
