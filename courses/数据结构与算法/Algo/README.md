# Coursera: Algorithms I & II（Princeton / Sedgewick, algs4）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Algorithms, Part I & Part II（Princeton University on Coursera） |
| 学校 | Princeton University |
| 主讲 | Robert Sedgewick（与 Kevin Wayne 共同开发课程与教材） |
| 教材 | Algorithms, 4th Edition（algs4）开源课本：https://algs4.cs.princeton.edu/home/ |
| csdiy 路径 | https://csdiy.wiki/数据结构与算法/Algo/ （页面更新 2022-09-06） |
| 最新期次 | Coursera 全年滚动开课（内容自 2015 年起稳定）；algs4 网站持续更新 |
| 先修/语言/难度 | 先修 CS61A 或同等编程基础；语言 Java；难度 🌟🌟🌟；预计学时 60 小时 |
| 状态 | 骨架 |

## 为什么学

- Coursera 上评分最高的算法课；Sedgewick 有把极复杂算法讲得生动浅显的"魔力"（csdiy 作者自述 KMP 与网络流都是在此课茅塞顿开）。
- 课程设计精准对应掌握一个算法的三问：**为什么这么做（正确性推导）→ 如何实现它 → 用它解决实际问题**。
- 教材开源、代码开源，且 algs4 的实现**不是 demo 而是工业级**：注释、命名、模块化都极严谨，是学 Java 工程写法的高质量范本。
- 10 个 Project 有真实问题背景、丰富测试样例与自动评分（**代码风格也计分**），逼你写出可维护的实现。
- 与 CS61B/6.006 形成互补：CS61B 教你从零造结构，6.006 教你严格分析，本课教你**把算法用得漂亮、用得对**。

## 先修与知识联系

- 先修：CS61A（或等价的程序设计基础）；会写 Java 或愿意随课程的 Java 说明上手即可。
- 与前课：CS61B 的链表/哈希/BST/堆/图是本项目的前置语言；本课把每个结构的"工程实现"提到工业级。
- 与后续：6.006（同一主题的形式化分析与更多数据结构：摊还、vEB、字符串匹配证明）、6.046/CS170（算法设计与 NP 难解性证明）。
- 横向联系：1.5 并查集 → Kruskal/图像连通域 → 15-445 缓冲池；4.4 最短路 → CS144 路由；5.x 字符串 → 编译器与检索引擎；网络流 → 15-445 查询优化、OR 工具。
- 工具线：作业用 algs4.jar + standard intro 包，命令行/JUnit 式测试与必学工具 Git、Make 章节配合。

## 最新年份讲义章节目录（Part I 六周 + Part II 六周，对应 algs4 章节）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| **Part I** | 分析、排序、优先队列、符号表 | algs4 ch.1–3 |
| L1 | 算法分析：经验测定、增长阶、大 Θ 与 amortized 入门 | algs4 1.1–1.3（含 1.4 增长阶） |
| L2 | 基础排序：选择/插入/希尔排序与壳层递减 | algs4 2.1；Studio: Sorting |
| L3 | 归并与快排：分治、原地切分、三路切分与工程细节 | algs4 2.2；Project: Collinear Points |
| L4 | 优先队列与堆：二叉堆、下沉/上浮、堆排序、多阶段选择 | algs4 2.4；Lecture "Priority Queues" |
| L5 | 无序符号表：BST 的插入/删除/范围查询与退化风险 | algs4 3.1–3.2；Quiz: Symbol Tables |
| L6 | 平衡树：2-3 树 → 红黑树（左倾红黑 LLRB）与等价性 | algs4 3.3–3.4；Part I 期末测验 |
| **Part II** | 图算法、字符串与难解性 | algs4 ch.4–5（+ ch.6 延伸） |
| L7 | 无向图与 DFS：图模型、邻接表、连通分量、环与路径 | algs4 4.1；Project: WordNet 发布 |
| L8 | 有向图：可达性、拓扑排序、Kosaraju 强连通分量 | algs4 4.2；Project: Degrees of Separation |
| L9 | 最小生成树：Kruskal（并查集）、Prim（惰性/急切）、Cut 定理 | algs4 4.3 + 1.5；Project: Fat Trees |
| L10 | 最短路径：DAG 最短路、Dijkstra、Bellman-Ford 与归约技巧 | algs4 4.4；Quiz: Shortest Paths |
| L11 | 字符串：键索引计数、LSD/MSD 基数排序、三向字符串快排、Trie/符号表 | algs4 5.1–5.2；Project: KD-Trees |
| L12 | 子串搜索、正则与压缩：KMP、Boyer-Moore、Rabin-Karp、NFA、Huffman/LZW | algs4 5.3–5.5；Part II 期末测验 |
| 延伸 A | 线性规划与单纯形、对偶与博弈（algs4 ch.6.1–6.2 精读） | algs4 6.1–6.2（配合 6.046/CS170） |
| 延伸 B | 网络流：最大流最小割、增广路径、归约应用（棒球队淘汰、图像分割） | algs4 6.2/6.3 相关章节；Project: Soccer Teams / Baseball Elimination |
| 延伸 C | 难解性：P/NP、归约、近似与启发式（algs4 ch.6.1 背景） | algs4 ch.6.1 背景；对照 CS170 NP 部分 |

> 说明：Coursera 官方以"6 周 × 1 模块"组织 Part I/II，本目录把模块拆为 12 个讲次主题，并按 algs4 章节给出阅读定位；延伸 A–C 为教材中课程视频未展开、但 Project 会用到的内容。

## 课程资源（摘自 csdiy）

- 课程网站：Coursera「Algorithms, Part I」「Algorithms, Part II」
- 课程视频：详见课程网站（英文字幕，另有多语字幕）
- 课程教材：https://algs4.cs.princeton.edu/home/ （开源课本站内可直接阅读）
- 课程作业：10 个 Project（含自动评分，代码风格计分），具体要求见课程网站
- 社区资源汇总：PKUFlyingPig/Princeton-Algorithm
