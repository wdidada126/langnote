# UCB CS61B: Data Structures and Algorithms（【CORE】）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | UCB CS61B: Data Structures and Algorithms（伯克利 CS61 系列第二门） |
| 学校 | University of California, Berkeley |
| 主讲 | Josh Hug（该课开课教师，autograder 亦由其团队开源） |
| 教材 | csdiy 标注"无官方教材"；实际以 Josh Hug 课程笔记（datastructur.org/notes）+ 课件 slides 为主，可参读 Sedgewick & Wayne《Computer Science: An Interdisciplinary Approach》与 CLRS 作为工具书 |
| csdiy 路径 | https://csdiy.wiki/数据结构与算法/CS61B/ （页面更新 2025-08-30） |
| 最新期次 | spring2024（另有 fall2023、spring2023、spring2021、spring2018；sp2021 起对公众开放，Gradescope 邀请码如 MB7ZPY） |
| 先修/语言/难度 | 先修 CS61A；语言 Java；难度 🌟🌟🌟；预计学时 60 小时 |
| 状态 | 全量（2026-09）：notes/ 23 篇覆盖 L1–L38 全部目录项；papers.md 经典+近年文献与开源映射；projects/ 9 个 JDK17 Java 项目（自测 main + 构建脚本） |

## 为什么学

- 伯克利 CS61 系列第二门课，重心从"程序抽象"转向**数据结构与算法的设计与实现**，同时首次让学生读写上**千行级工程代码**，是 Java 软件工程思想的第一课。
- 作业质量极高：**14 个 Lab**（亲手实现课上讲过的绝大部分数据结构）+ **10 个 Homework**（用数据结构与算法解决实际问题）+ **3 个 Project**（真实多人协作式代码库）。
- 零基础友好：从 IntelliJ IDEA 配置讲起，Java 核心语法与特性"保姆级"覆盖；无 Java 经验也能跟上。
- 评测闭环公开：autograder 开源，可借 Gradescope 邀请码免费自评代码，适合自学。
- 后续铺路：Project 3（Gitlet）手写 Git，与必学工具的 Git 章节互相印证；图与排序部分直接为 6.006/CS170 打底。

## 先修与知识联系

| 方向 | 关联课程/知识 |
| --- | --- |
| 先修 | CS61A（程序结构与解释、Python 基础）；Missing Semester（Git/命令行） |
| 平行对照 | CS106B/CS106X（C++ 版数据结构，讲解侧重应用）、MIT 6.092（Java 语法速成） |
| 直接后继 | 6.006（算法与严格分析，Python）、6.046（算法设计与证明）、CS170（复杂度与难解性理论） |
| 向下支撑 | CSAPP：本课程的 ArrayList/HashMap/ArrayDeque 在 CSAPP 视角下对应"连续内存 vs 指针追踪"与缓存友好性 |
| 工程线 | 6.031：Lab 的 JUnit 测试、spec 与代码审查是其简化前奏；15-445 缓冲池/B+ 树复用本课程的数组/树/哈希结构 |
| 复用场景 | 15-213/CS110 的抽象、CS186 的索引结构（B+ 树/哈希索引）、CS144 的字节流与 I/O |

## 最新年份讲义全章节目录（spring2024，按讲授主题整理）

### Part A｜Java 语言与软件工程基础（L1–L15）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：JDK/IntelliJ IDEA 环境、编译与运行模型 | Hug 笔记 "Java Setup"；syllabus；Lab1 发布 |
| L2 | Java 语法基础：原始类型、表达式、整数溢出与 float 精度 | Hug 笔记 "Java Syntax"；HW1 |
| L3 | 控制流、作用域与"读代码"训练（Softwear 式反编译练习） | Hug 笔记 "Control Flow"；Lab1（Java 热身） |
| L4 | 对象、接口与封装：interface/implements、方法签名 | Hug 笔记 "Interfaces"；Lab2（IntLists） |
| L5 | 内部类与静态嵌套类、this 的作用域语义 | Hug 笔记 "Inner Classes" |
| L6 | 包、访问控制与信息隐藏（public/protected/private、API 设计） | Hug 笔记 "Packages & Access Control" |
| L7 | 继承与多态：extends/super/重写、Object 方法与 equals | Hug 笔记 "Inheritance"；Lab2 |
| L8 | 泛型接口 I：List 与实现层次（List ← ArrayList/LinkedList） | Hug 笔记 "Generic Interfaces: Lists" |
| L9 | 泛型接口 II：Set 与 Map 抽象（HashSet/HashMap/TreeMap） | Hug 笔记 "Generic Interfaces: Sets and Maps" |
| L10 | 泛型接口 III：Iterable 与 foreach 的展开语义 | Hug 笔记 "Generic Interfaces: Iterables" |
| L11 | 泛型方法与有界类型参数、类型擦除 | Hug 笔记 "Generic Methods" |
| L12 | 异常体系：受检/非受检异常、try-with-resources | Hug 笔记 "Exception" |
| L13 | 测试：JUnit 5、等价类/边界值、Mock 与覆盖率 | Hug 笔记 "Testing"；Lab3（TestArrayDeque） |
| L14 | 调试：IDEA debugger、断点/条件断点、性能剖析初阶 | Hug 笔记 "Debugging" |
| L15 | 渐近分析：Big-Θ、增长阶与"操作计数"式成本分析 | Hug 笔记 "Asymptotics"；CLRS Ch.3；HW2 |

### Part B｜数据结构设计与实现（L16–L28）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L16 | 数组基础、浅拷贝 vs 深拷贝；SLList（单链表）实现 | Hug 笔记 "Array Basis / Linked Lists"；Lab4 |
| L17 | 动态数组：ResizingArraySLList、几何扩容与摊还 O(1) | Hug 笔记 "Resizing Arrays"；CLRS 17.1 |
| L18 | 双向链表 DLList 与 List 接口设计总结（哨兵、prev/next） | Hug 笔记 "Doubly Linked Lists"；Project1a |
| L19 | Deque 抽象与 ArrayDeque：环形数组、head/tail 与取模 | Hug 笔记 "Deque"；Lab5（ArrayDeque） |
| L20 | 哈希 I：hash code 契约、分离链法（separate chaining） | Hug 笔记 "Hashing I"；CLRS 11.1–11.2 |
| L21 | 哈希 II：装填因子、倍增扩容与再哈希成本 | Hug 笔记 "Hashing II"；Lab6（HashMap） |
| L22 | 哈希 III：好哈希函数、通用哈希与字符串键处理 | Hug 笔记 "Hashing III"；CLRS 11.3.3 |
| L23 | Map/Set 工程对比：HashMap vs TreeMap 的实现与选型 | Hug 笔记 "Map Implementations"；HW3 |
| L24 | 比较接口：Comparable/Comparator、TreeMap 有序遍历 | Hug 笔记 "Comparison Interfaces" |
| L25 | 二叉搜索树：插入/查找/删除、中序遍历与性质维护 | Hug 笔记 "Binary Search Trees"；CLRS 12；Lab7 |
| L26 | 平衡树动机：2-3 树、旋转与高度界 | Hug 笔记 "Balanced Trees"；CLRS 13.1 |
| L27 | AVL/红黑树与跳表：工程中的取舍（Java TreeMap vs Redis zset） | Hug 笔记 "AVL Tree Rotations"；algs4 3.3 |
| L28 | 堆与优先队列：complete-tree 数组表示、offer/poll、heapify 线性构建 | Hug 笔记 "Heaps"；CLRS 6；Lab8 |

### Part C｜图算法与算法设计范式（L29–L38）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L29 | 图模型与 Graph API：V/edges、顶点迭代器、加权图 | Hug 笔记 "Graphs"；Lab9（Graph 抽象） |
| L30 | 图遍历：DFS 与 BFS、连通性、跳数最短路径（WordLadder） | Hug 笔记 "Graph Traversals"；CLRS 22.2–22.3；Lab10 |
| L31 | 最小生成树：Prim(lazy/eager)、Kruskal 与并查集（Union-Find） | Hug 笔记 "Minimum Spanning Trees / Union Find"；CLRS 21、23 |
| L32 | 单源最短路：Dijkstra、优先级队列使用与 A* 启发式（Maze/Teleportation） | Hug 笔记 "Shortest Paths"；CLRS 24.3 |
| L33 | 动态规划：重叠子问题、自顶向下 memo 与自底向上表（0-1 背包/LCS/编辑距离） | Hug 笔记 "Dynamic Programming"；CLRS 15；Lab11 |
| L34 | 排序 I：选择/插入排序、归并与快排（分治与递归树） | Hug 笔记 "Sorts"；CLRS 2、6.3、7 |
| L35 | 排序 II：稳定性、比较排序下界、基数排序与 Arrays.sort 的工程实现 | Hug 笔记 "Stability / Radix Sorts / Arrays Library"；algs4 5.1 |
| L36 | 字符串结构：Trie、前缀检索与拼写检查应用 | Hug 笔记 "Tries"；CLRS 32.2 |
| L37 | Java I/O：字节流/字符流、Buffered、序列化与文件处理 | Hug 笔记 "Java I/O"；Project2 |
| L38 | 课程总结与后续路线：并发概览、算法工程实践与 6.006/CS170 衔接 | Hug 笔记 "Conclusion & Next Steps"；HW10 |

### 作业与实践环节（spring2024，每年略有调整）

| 环节 | 内容 | 关联讲次 |
| --- | --- | --- |
| Lab（约 14 个） | Java 热身、IntLists、Deque、HashMap、BST、Heap、Graph、Union-Find、Trie 等**亲手实现数据结构** | L1–L36 |
| Homework（约 10 个） | 用数据结构与算法解决实际问题（含渐近分析、图建模、DP） | L15–L35 |
| Project 1（1a/1b） | 1a：2D 数组与游戏（Tetris 风格）；1b：二维数组工程 + Enigma 加密机模拟 | L4–L20 |
| Project 2 | 大型多人协作式代码库改造：文本编辑器/特征开关（feature enabler）与继承式扩展 | L18–L28、L37 |
| Project 3 | **Gitlet**：用 Java 重写一个功能子集 Git（提交、分支、合并），手写对象存储与版本图 | L20–L31 |
| 最终考核 | 期末笔试（数据结构设计 + 复杂度分析 + 图算法手写） | 全课 |

> 说明：本目录按 spring2024 官网（sp24.datastructur.org）讲授主题整理为 38 讲 + 实践环节；不同期次的讲次合并/拆分略有差异（如 fall2023 把部分泛型内容合并），以官网当期 schedule 为准。

## 课程资源（摘自 csdiy）

- 课程网站：spring2024 / fall2023 / spring2023 / spring2021 / spring2018（datastructur.org 系列站点）
- 课程视频：原版视频见课程网站；B 站有中文翻译搬运
- 课程作业：每年略有不同（18 春季为 14 Lab + 10 Homework + 3 Project）
- 社区资源汇总：PKUFlyingPig/CS61B、InsideEmpire/CS61B-PathwayToSuccess
- 预计投入：60 小时（🌟🌟🌟），Project 3 Gitlet 通常另需 15–20 小时

## 本目录学习材料（全量 2026-09）

| 目录/文件 | 内容 |
| --- | --- |
| `notes/`（23 篇） | L1–L38 合并为 23 个中文笔记（文件名标注讲次范围）：实现要点+Java 片段、复杂度表、前后讲联系、跨课程联系（CS61A/6.006/CSAPP/DDCA/15-445）、开源应用（JDK/Lucene/RocksDB/Git）、自测题 |
| `papers.md` | 经典论文 13 篇（红黑树/AVL/B 树/跳表/堆/并查集/一致性哈希/排序等）＋近五年（2021–2026）表＋知识点↔开源实现映射表 |
| `projects/`（9 项） | JDK17 零依赖 Java 项目：dllist、hashmap、bst(AVL)、heap(TopK)、trie、graph(BFS/DFS/Dijkstra/Prim/Kruskal)、unionfind、sorts、minigit(GITLET 骨架)；各含自测 main、README、build.bat/sh；总表见 `projects/README.md` |
