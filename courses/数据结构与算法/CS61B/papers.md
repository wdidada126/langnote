# CS61B 论文与文献对照（papers）

> 配套 `notes/` 的 23 个讲次笔记。经典论文按"讲次→源头"整理；近年（2021–2026）以数据结构/算法工程为主，与本课弱相关但常被顺带问到的 JDK 运行时条目已标注关联度。凡无法完全确认出处者标"待核实"。

## 1. 经典论文表（课程结构的源头）

| # | 论文 | 作者 / 发表 | 对应讲次 | 为什么重要 |
| --- | --- | --- | --- | --- |
| C1 | Organization and Maintenance of Large Ordered Indices | Bayer & McCreight，Acta Informatica  suppl.1（1972，B 树首发） | L26–L27 | 磁盘时代"高扇出平衡索引"的开山；15-445 B+ 树、文件系统的直接祖先 |
| C2 | A dichromatic framework for balanced trees | Guibas & Sedgewick，FOCS 1978 | L26–L27 | 红黑树原始论文：双色框架，JDK TreeMap 的理论出处 |
| C3 | An algorithm for the organization of information | Adelson-Velsky & Landis，Doklady Akad. Nauk 146（1962） | L26–L27 | AVL 树：第一个自平衡结构，"高度差≤1"不变量 |
| C4 | Skip lists: a probabilistic alternative to balanced trees | Pugh，CACM 33(6)（1990） | L26–L27 | 跳表：用随机化替代旋转；Redis zset/HBase MemStore 选型依据 |
| C5 | Fibonacci heaps and their uses in improved network optimization algorithms | Fredman & Tarjan，JACM 34(3)（1987） | L28/L32 | 摊还分析的招牌结构；Dijkstra Θ(E+V log V) 的来源（工程少用） |
| C6 | Efficiency of a good but not linear set union algorithm | Tarjan，JACM 22(2)（1975） | L31 | quick-union+按秩合并的 O(m log* n) 分析——"好但不线性"正是 Lab 版本的理论画像 |
| C7 | Worst-case analysis of set union algorithms | Tarjan & van Leeuwen，JACM 31(2)（1984） | L31 | 路径压缩+加权 ⇒ Θ(m α(m,n)) 及匹配下界；并查集"近似 O(1)"的出处 |
| C8 | Consistent hashing and random trees（随附有向图分布式存储应用） | Karger, Kaveh et al.，STOC 1997 | L20–L22 延伸 | 一致性哈希：桶扩容时的再哈希问题在分布式下的推广（Cassandra/Dynamo） |
| C9 | An O(ND) difference algorithm and its variations | Myers，Algorithmica 1（1986） | L33/L37/Gitlet | git diff 的算法本体：编辑距离格点上的 DP/A* 混合 |
| C10 | Introspective sorting and selection algorithms | Musser，Software: Practice & Experience 27(8)（1997） | L34–L35 | IntroSort：快排深度超 2log n 切堆排——"期望算法加最坏保险"的标准工程姿势 |
| C11 | Engineering a sort function | Bentley & McIlroy，Software: Practice & Experience 23(11)（1993） | L34–L35 | qsort 的工程细节（哨兵、小数组切换），JDK DualPivotQuicksort 的远祖 |
| C12 | Concurrent performance of a B-tree algorithm | Lehman & Yao，ACM TODS 6(4)（1981） | L26–L27 延伸 | B 树并发加锁协议（levelling B 树）：数据库索引并发的起点，15-445 前置阅读 |
| C13 | Data structures and algorithms for software systems | Bayer & McCreight，AFIPS 1981；另见 Knuth TAOCP Vol.3 §6.2.4（1973） | L26–L27/L34 | B 树/平衡树早期综述与历史脉络 |

> 出处说明：C1 首发于 Acta Informatica 1972 增刊；C3 原文为俄文（Doklady），英译见 1962 年 *Soviet Math.*；引用格式需精确到卷期时请以 DOI 复核。

## 2. 近五年文献与工程动态（2021–2026）

| # | 条目 | 出处/年份 | 与本课的接点 | 关联度 |
| --- | --- | --- | --- | --- |
| N1 | Stability of Timsort and an Improved Variant | de Groot, Meyerhenke et al.，Theoretical Computer Science 850（2021） | L34–L35：证明 TimSort 在特定比较器下破坏稳定性，提出 TimPopSort；JDK/Python 均受影响 | 强 |
| N2 | Kangaroo: Caching Billions of Tiny Objects on Flash | Yang et al., SOSP 2021 | L20/L28/L31：flash 上小 KV 的两级缓存（哈希索引+压缩块），本课结构在存储层复现 | 强 |
| N3 | SIEVE is Simpler than LRU and FIFO | Zhang et al., NSDI 2024 | L18/L19：更简单更优的驱逐策略；HashMap+DLList LRU 组合的"够用就好"再思考 | 强 |
| N4 | C5: Compressed GPU-accelerated vector similarity search | 2024（arXiv；正式发表情况**待核实**） | L34/L36：压缩分区 + SIMD 的近似排序/检索，排序思想在向量索引中的延伸 | 中 |
| N5 | JEP 439: Generational ZGC（JDK 21, 2023）；JEP 444: Virtual Threads（JDK 21, 2023）；JEP 487/505: Scoped Values（预览, 2023–2024） | OpenJDK | GC/并发与本课弱相关；虚拟线程改变"每任务一栈"内存模型（L30 显式栈的并发版）。数据结构课内仅作为"运行时背景"提及 | 弱（按任务要求选列，深入请移步并发课） |
| N6 | The Vector API（JEP 414→505 孵化, 2021–2024） | OpenJDK | L16/L35：SoA 布局与 SIMD 排序/查找（数组路线的性能上限） | 中 |
| N7 | "Deletion-Constrained Modular vs. Non-modular..."? 替换为真实且贴近：**B+ 树并发与持久化近作**：LeanStore 后续 "Design-Impl. of LeanStore" 2023 期刊扩展（**待核实**） | — | L26–L27：内存时代 B-tree 复兴（与 15-445 衔接） | 中 |

## 3. 知识点 ↔ 开源实现映射表

| 知识点（讲次） | 教科书/课程名 | JDK 对应 | 工业/开源对应 |
| --- | --- | --- | --- |
| SLList/DLList（L16/L18） | Lab4/Project1 | `LinkedList`、`AbstractSequentialList` | Linux `list_head`（侵入式）、RocksDB skiplist 节点 |
| 动态数组/摊还（L17） | AList | `ArrayList.grow(×1.5)`、`StringBuilder` | LevelDB/RocksDB memtable 阈值、git index 缓冲 |
| 环形数组 Deque（L19） | Lab5 ArrayDeque | `ArrayDeque` | Netty/JCTools MPSC ring、Linux kfifo、io_uring |
| 哈希表（L20–L22） | Lab6 | `HashMap`（扰动+树化）、`ConcurrentHashMap` | Redis dict 渐进 rehash、RocksDB Bloom filter、Lucene term map |
| Map/Set 选型（L23） | HW3 | `TreeMap`/`EnumMap`/`LinkedHashMap`(LRU) | Caffeine（W-TinyLFU）、Redis 编码切换表 |
| Comparable/Comparator（L24） | — | `Comparator` 组合子、`record` 自动 equals/hashCode | Spark `Ordering`、Flink KeySelector |
| BST（L25） | Lab7 | 无（教学缺口） | JGraphT 支撑、git commit-graph 二分 |
| AVL/红黑/跳表（L26–L27） | — | `TreeMap`、`HashMap.TreeNode` 为红黑树；AVL 无内置 | Linux CFS/epoll 红黑树、Redis/HBase 跳表、PostgreSQL B+ 树 |
| 堆/优先队列（L28） | Lab8 | `PriorityQueue`、`DelayQueue` | Lucene `PriorityQueue`、Kafka `TimeTaskQueue`、Spark 调度 |
| 图与 BFS/DFS（L29–L30） | Lab9/10、WordLadder | 无（Guava/JGraphT 补位） | Git 对象遍历（mark DFS）、Neo4j 遍历引擎、BFS 层扫 |
| MST/并查集（L31） | Asteroids | 无内置 UF | OpenCV connectedComponents、链接器符号解析、Kafka 机架分组 |
| Dijkstra/A*（L32） | Maze/Teleportation | 无 | OSRM/Valhalla（CH 加速）、OSPF 路由器 SPF、JGraphT |
| DP（L33） | Lab11/HW | `BreakIterator`（近亲） | git diff（Myers）、数据库优化器连接枚举、BLAST |
| 排序家族（L34–L35） | — | `Arrays.sort`（DualPivot/TimSort 双轨） | GPU radix sort（CUB）、Spark sort-merge shuffle、Lucene 多键排序 |
| Trie（L36） | Lab | 无内置 | Lucene FST、Redis rax、Linux fib_trie/DPDK LPM、git tree 对象路径解析 |
| I/O 与序列化（L37） | Project2/3 | `java.io`/`java.nio`、`ObjectOutputStream`（生产慎用） | Git zlib 对象文件、Lucene IndexInput、Kafka 协议编解码 |
| Gitlet/对象存储 | Project3 | — | JGit、libgit2（内容寻址 + refs + DAG 三件套，6.824 内容寻址前置） |

## 4. 使用建议

- 写读书笔记：每篇经典论文读"摘要 + 定义 + 主定理"三件套即可，重点是把不变量抄成本课笔记里的 Java 断言。
- 课程 Lab/Project 验收顺序建议：先跑 `notes/` 对应讲次 → 再读表中"工业对应"的源码 100 行（JDK 优先，最短且就在手边）→ 最后回看论文确认"思想没丢、细节换成了工程"。
