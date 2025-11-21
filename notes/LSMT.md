# LSMT

rust lsm
https://github.com/edidada/mini-lsm
https://zhuanlan.zhihu.com/p/680608573
Mini-LSM：可能是史上最完整的 LSM-Tree 存储课程

## 概念
LSM树（Log-Structured Merge-Tree）
今天来聊聊lsm tree，它的全称是log structured merge tree ，简单来说，lsm tree可以认为是针对传统b树在磁盘写入上低劣表现的一种优化，其核心思想的核心就是放弃部分读能力，换取写入的最大化能力。

https://www.cnblogs.com/shenzhaohai1989/p/3893123.html

## 子结构SSTable/Sorted String Table(SSTable)
在我们介绍LSMT的原理之前，我们先来介绍一下它的子结构SSTable。
第一次看到这个单词的时候觉得一头雾水是正常的，SSTable的全称是Sorted String Table，本质就是一个KV结构顺序排列的文件。我们来看下下图：

[分布式——吞吐量巨强、Hbase的承载者LSMT](https://mp.weixin.qq.com/s?__biz=MzUyMTM5OTM2NA==&mid=2247484853&idx=1&sn=99fa9bf9cc6a31d1f248a87c25966858&chksm=f9daf89ecead71885c7fb7cabc2ba719500aea4a8af277cd0744536dedd9b3dbead5f9253898&scene=21#wechat_redirect)

首先，我们先从背景知识开始。我们之前介绍B+树的时候说过，B+树和B树最大的不同就是将所有的数据都放在了叶子节点。从而优化了我们批量插入以及批量查询的效率，而优化的核心逻辑就是因为无论是什么存储介质，顺序存储的效率一定要比随机存储更高，并且高的还不是一点半点。这个已经算是老生常谈了，如果我没记错的话，这已经是我第三次在文章当中提到这一点了。
我最近看到了一张图，很好地阐述了随机读取和顺序读取两者的效率差，我们来看下面这张图。其中绿色的部分表示硬盘顺序读取的最大速度，而红色表示随机读取时的速度。

![磁盘效率](imgs/save_disk.png)

我们看下纵坐标就知道，这两者差的不是一点半点，已经有数量级的差距了。而且还不止是一个数量级，至少相差了三个数量级，显然这是非常恐怖的。另外，这个差距并不只是在传统的机械硬盘上存在，即使是现在比较先进的SSD固态硬盘上，也一样存在。也就是说这个差距是介质无关的。

LSMT

SSTable开源实现

levelDb
Sorted String Table(SSTable)--是存储，处理和交换数据集的最流行的输出之一
https://www.cnblogs.com/Jack47/p/sstable-1.html

详解SSTable结构和LSMTree索引
https://blog.csdn.net/sdulibh/article/details/49719877

现代数据库存储引擎的核心。
核心答案
LSM树是一种数据存储的格式和结构，但它并不直接存储我们熟悉的“表数据”（如一行行的用户信息），而是存储构成数据库的最基础单元——键值对（Key-Value Pair）。

许多现代数据库（如 Google LevelDB/RocksDB、Apache Cassandra、HBase 等）的存储引擎正是基于LSM树构建的。即使是您熟悉的MySQL，其流行存储引擎 MyRocks（由Facebook开发）也使用LSM树来替代传统的B+树。
1. LSM树是什么？为什么会出现？
要理解LSM树，首先要明白传统数据库（如MySQL的InnoDB，使用B+树）在写入时面临的一个核心瓶颈：随机写磁盘速度极慢。
•   B+树的写入：当插入或更新一条数据时，数据库需要找到数据在B+树中的正确位置并进行修改。这个操作可能直接发生在磁盘上，导致大量的随机I/O。即使有缓冲池，在写入密集型场景（如日志记录、实时交易）下，随机I/O仍然是主要瓶颈。
LSM树（Log-Structured Merge Tree）的设计哲学完全不同，它源自一种叫做“日志结构”（Log-Structured）的文件系统思想。其核心目标是：将随机写入转换为顺序写入，从而极大提升写入吞吐量。
2. LSM树的工作原理（三步曲）
LSM树的工作流程可以概括为下图所示的三个核心阶段：
flowchart TD
    A[写入请求] --> B[“1. 写入内存（MemTable）”]
    B --> C[“2. 内存刷盘（Immutable MemTable -> SSTable）”]
    C --> D[“3. 后台合并（Compaction）”]
    D --> E[生成新SSTable<br>并清理旧文件]
    
    B --> B1[“WAL（Write-Ahead Log）<br>用于崩溃恢复”]
    C --> C1[“SSTable（磁盘文件）<br>只读且有序”]


步骤详解
第1步：写入内存（MemTable）
•   当有新的数据写入（PUT）时，它首先被追加到一个预写日志（Write-Ahead Log, WAL） 中。WAL是顺序写入的，速度很快，主要用于崩溃恢复。
•   随后，数据被插入到一个位于内存中的、排序好的数据结构里，这个结构称为 MemTable。因为是在内存中操作，所以速度极快。
第2步：内存刷盘（MemTable -> SSTable）
•   当MemTable的大小达到一定阈值后，它会被转换为一个只读的MemTable（Immutable MemTable），并随后顺序地刷写到磁盘上，形成一个名为 SSTable（Sorted String Table） 的文件。
•   关键点：这个刷盘过程是顺序写入，避免了B+树的随机I/O，速度非常快。每个SSTable文件内部都是按Key排序的。
第3步：后台合并（Compaction）
•   随着时间推移，磁盘上会有很多SSTable文件。同一个Key可能存在于多个SSTable中（有多个版本）。
•   LSM树有一个后台进程，负责将多个SSTable文件合并（Compaction） 成一个新的、更大的SSTable文件。在这个过程中，它会清除重复的、过时的Key（如被删除或更新的旧值），只保留最新的版本。
•   Compaction是LSM树的核心，也是其资源消耗的主要来源（会占用CPU和I/O）。
3. LSM树在数据库中的具体作用
1.  极高的写入吞吐量：这是LSM树最核心的优势。通过将随机写转换为顺序写，它非常适合写入密集型的应用场景，如物联网、日志采集、实时消息等。
2.  高效的存储：SSTable文件是不可变的，且是顺序存储的，这便于进行数据压缩，节省磁盘空间。
3.  读操作的权衡：
    ◦   缺点：读取操作可能变慢。因为一个Key可能存在于MemTable和多个不同层级的SSTable中，数据库需要检查这些可能的位置（这称为读放大），直到找到最新的值。为了加速读取，通常会使用布隆过滤器（Bloom Filter） 来快速判断一个Key是否不存在于某个SSTable中，避免不必要的磁盘查找。
    ◦   优点：范围查询（SCAN）在某些情况下可能比B+树更高效，因为SSTable内部是有序的，合并后的文件也是有序的。
4. 哪些数据库使用LSM树？
您可以将数据库的“存储格式”理解为它的“发动机”。不同的数据库选择了不同的发动机。
•   纯LSM树引擎的数据库：
    ◦   Google LevelDB / RocksDB：这是最著名的嵌入式LSM树库，是事实上的标准。RocksDB是LevelDB的强化版。
    ◦   Apache Cassandra：其存储引擎基于LSM树。
    ◦   HBase：其存储引擎（HFile）也基于LSM树思想。
•   支持LSM树引擎的传统关系型数据库：
    ◦   MySQL with MyRocks：MyRocks是一个使用RocksDB作为后端的存储引擎，可以作为InnoDB的替代品，在特定场景下（如高写入、需要节省存储空间）表现优异。
    ◦   MongoDB with WiredTiger：虽然WiredTiger主要使用B+树，但它也借鉴了LSM树的一些思想来管理其日志。
•   作为对比的传统引擎：
    ◦   MySQL InnoDB：使用B+树作为主要索引结构。Oracle, PostgreSQL, SQL Server 等传统数据库也主要使用B+树或其变种。
总结
特性 LSM树 B+树（传统）
核心优势 写入性能极高（顺序写） 读取性能稳定（特别是主键查询）
写入方式 追加、顺序写入 原地更新、随机写入
读取性能 可能较慢（需要查询多个来源） 非常快（通常O(logN)的复杂度）
存储空间 节省（高压缩率），但存在写放大 相对占用更多空间
典型应用 写入密集型：日志、IoT、消息队列 读多写少、需要事务：传统业务系统、银行交易
所以，您的说法“常见数据库把表数据按照LSM的格式存储”是基本正确的，但更精确的说法是：许多现代数据库的存储引擎使用LSM树的结构来管理底层的数据文件（这些文件以键值对的形式存储着表数据、索引等所有信息）。

这是一个很好的、兼具理论深度和实践价值的数据库主题。LSM树（Log-Structured Merge-Tree）是现代高性能KV存储和NoSQL数据库（如Cassandra、LevelDB、RocksDB、HBase等）的核心存储引擎结构。

对于LSM树的教学实现，可以从理论（本科）到实践（硕士/博士）分层次进行。
## 一、本科教学：理解核心概念与机制
本科阶段，重点在于理解LSM树的设计动机、基本结构和运行机制，以及它与传统B+树的性能权衡。

### 1. 核心概念
| 概念 | 描述 |
| :--- | :--- |
| 设计动机 | 优化写入操作。通过将随机写转化为顺序写（Append Only），充分利用SSD或HDD的顺序写入高性能特性。 |
| 基本结构 | 分为内存部分 (MemTable) 和磁盘部分 (SSTable/Level)。 |
| MemTable | 内存中的有序结构（如跳表 SkipList 或 AVL/红黑树），所有写入首先进入此处。 |
| SSTable | Sorted String Table，磁盘上的不可变、有序的键值对文件。 |
| 多层结构 (Levels) | 磁盘上的SSTable被组织成多个层级（L0, L1, L2...）。 |
| Compaction | 归并（合并）操作。将内存中的数据落盘，以及合并磁盘上不同层级的SSTable，是LSM树的核心维护机制。 |

### 2. 关键机制与权衡
* 写入 (Write/Insert/Update)： 顺序写入 MemTable $\rightarrow$ WAL (Write-Ahead Log)。写入性能极高。
* 读取 (Read)： 需要从 MemTable 开始，逐层向下查找 SSTable。由于数据冗余和多版本，读取性能相对B+树可能较差。
* 布隆过滤器 (Bloom Filter)： 用于加速读取。在每个SSTable中嵌入布隆过滤器，快速判断一个Key是否存在于该文件中，从而减少不必要的磁盘I/O。
* 性能权衡：
    * 高写吞吐量（通过顺序写实现）。
    * 写放大 (Write Amplification)： 由于Compaction操作，一个数据可能会被多次重写。
    * 读放大 (Read Amplification)： 读取一个Key可能需要检查多个SSTable。
    * 空间放大 (Space Amplification)： 旧版本的数据和已删除标记可能暂时共存，占用额外空间。

## 二、硕/博教学：深入实现与优化
研究生阶段应侧重于LSM树的实际工程实现、性能调优以及高级变种的研究。可以基于现有的开源项目进行二次开发或设计一个简化的原型。
### 1. 实现与原型设计
| 阶段 | 实践内容 | 涉及的关键技术 |
| :--- | :--- | :--- |
| Phase 1: 基础KV引擎 | 实现一个简化的、单层级的LSM-Tree原型（如基于LevelDB/RocksDB）。 | MemTable (SkipList) 实现；SSTable 文件的读写（需包含有序KV、索引块、布隆过滤器）；WAL 日志；Compaction 线程。 |
| Phase 2: 分层与Compaction | 引入多层结构（L0, L1, L2...）和分层 Compaction 策略。 | LevelDB/RocksDB 的 Level Compaction (size-tiered vs. leveled) 策略实现与对比；Compaction 调度和流控。 |
| Phase 3: 性能优化 | 针对放大问题进行优化。 | 布隆过滤器 实现与参数调优；读放大 优化（如Partitioning/Indexing）；写放大 优化（如tiered compaction）。 |
### 2. 重点研究方向（硕/博）
* Compaction 策略研究：
    * Size-Tiered Compaction (STCS): 写入性能好，空间放大高（常用于Cassandra）。
    * Leveled Compaction (LCS): 写入性能稍差，空间放大低（常用于LevelDB/RocksDB）。
    * Elastic Compaction/VTTree： 动态选择策略以适应不同负载。
* 读写分离与数据结构：
    * 引入Secondary Index（二级索引）在LSM树上的设计和维护。
    * Log-Structured B-Tree (LSB-Tree) 等混合结构的研究。
* 硬件优化：
    * LSM树在NVM/Optane等新型存储介质上的设计与实现。
    * 利用存储级内存 (SCM) 优化WAL和MemTable。
    * Compaction 卸载到FPGA/GPU 等加速硬件。
## 三、推荐教学资源与项目
| 类型 | 资源推荐 | 教学目的 |
| :--- | :--- | :--- |
| 理论书籍 | 《数据库系统实现》 (Database System Implementation)；相关数据库内核论文。 | 深入理解存储引擎设计。 |
| 开源项目 | LevelDB (Google/C++)；RocksDB (Facebook/C++)；BadgerDB (Dgraph/Go)。 | 学习工业级实现细节，作为原型参考或二次开发基础。 |
| 在线课程 | 著名大学（如 CMU）的数据库课程“15-721 Advanced Database Systems”，通常会深入讨论LSM-Tree。 | 学习前沿研究和工程挑战。 |

您希望我针对LSM树的具体Compaction 策略（如Leveled vs. Size-Tiered）进行更详细的比较和分析吗？
好的，既然您希望深入了解LSM树中两种主要的 Compaction 策略：Leveled Compaction (LCS) 和 Size-Tiered Compaction (STCS)，我将详细对比它们的机制、性能权衡以及各自适用的场景。

---

## ⚖️ Leveled vs. Size-Tiered Compaction 策略对比

Compaction 是 LSM 树的核心，它负责合并磁盘上的 SSTable，清理过期/删除数据，并维持数据有序性。选择不同的 Compaction 策略直接决定了存储引擎的读放大、写放大和空间放大。

| 特性 | Leveled Compaction (LCS) - 如 LevelDB, RocksDB | Size-Tiered Compaction (STCS) - 如 Cassandra, HBase |
| :--- | :--- | :--- |
| 基本思想 | 将数据严格分层，每层仅包含一个或少量大文件。下一层级的大小通常是前一层的 $T$ 倍（$T=10$）。| 将数据按大小分组（Tier），每组包含多个大小相近的文件。 |
| 层级数量| 层级数量较多 (e.g., L0, L1, ..., L6)。 | 层级数量较少，通常只有少数几个 Tier。|
| 触发机制| 当某一层 $L_i$ 的总大小超过阈值或与下一层 $L_{i+1}$ 有键范围重叠过多时，将 $L_i$ 中一个文件与 $L_{i+1}$ 中所有重叠文件合并。| 当一个 Tier 中累积到 $N$ 个文件时，将这 $N$ 个文件合并成一个更大的文件，并提升到下一个 Tier。 |
| 空间放大| 低 (Low)：因为每一层的数据键范围基本不重叠（L0 除外），重复数据和墓碑 (Tombstone) 可以很快被清理。通常接近 1.1x。| 高 (High)：一个 Tier 内的文件可能长期存在，旧版本数据和墓碑可能长时间保留，直到整个 Tier 被合并。可达 2.0x-5.0x。|
| 写放大 | 高 (High)：数据从 L0 到 Ln 需要经历多次小范围的合并，平均每个 KV 被重写 $O(\log N)$ 次。 | 低 (Low)：数据被合并的次数较少，合并时通常是 $N$ 个文件合一。平均每个 KV 被重写 $O(1)$ 或 $O(\log_{N} M)$ 次。 |
| 读放大 | 低 (Low)：一个 Key 只可能出现在 L0 的少数几个文件和 L1 以上的一个文件中。通常只需要检查 $O(\log N)$ 个文件。| 高 (High)：一个 Key 可能分布在每个 Tier 的所有文件中，查找时需要检查 $O(T \cdot \text{num\_tiers})$ 个文件。 |
| 写入吞吐| 相对稳定，但 Compaction 压力大时可能波动。| 极高，尤其是在 Compaction 尚未触发时，写入速度非常快。|
| 最适用场景| 读操作密集、需要严格控制空间占用、对延迟敏感的应用 (e.g., 核心存储、二级索引)。| 写操作密集、高吞吐量写入、可容忍高空间占用的应用 (e.g., 时序数据库、日志存储)。|

## 1. Size-Tiered Compaction (STCS) 详解
### 机制特点
1.  分组归并：数据按照文件大小被划分到不同的 Tier（层/组）。
2.  延迟合并：Compaction 不会频繁发生。只有当某个 Tier 中的文件数量达到预设阈值 $N$ 时，Tier 中的所有文件才会被一次性合并成一个更大的文件，然后进入下一个 Tier。
3.  高性能写入：由于 Compaction 被延迟，大部分写入只需将数据追加到 L0，因此写入延迟低，吞吐量高。

### 缺点分析
* 读放大：查找一个 Key 时，理论上必须检查所有 Tier 中的所有文件，直到找到数据。实际工程中会通过索引优化，但仍需检查 $O(\text{Num\_Tiers})$ 个文件，导致读性能波动大且慢。
* 空间放大：在某个 Tier 被合并之前，被删除的数据（墓碑）和旧版本数据会一直存在，导致空间占用较大。

## 2. Leveled Compaction (LCS) 详解
### 机制特点
1.  严格分层：数据被组织在 $L_0, L_1, L_2, ...$ 等层级中。从 $L_1$ 开始，每一层内的 SSTable 保证键范围互不重叠。
2.  增量归并：Compaction 是连续且小范围的。它通常选择 $L_i$ 中的一个文件与 $L_{i+1}$ 中所有键范围重叠的文件进行合并。
3.  快速清理：由于键范围不重叠，合并操作可以快速清理过期数据和墓碑。

### 缺点分析

* 写放大：为了将数据推入更高层级并保证键范围不重叠，一个 KV 对可能会被多次重写（每经过一个 $L_i$ 到 $L_{i+1}$ 的合并就会被重写一次）。
* Compaction 峰值：当写入速率持续高于 Compaction 速率时，系统必须投入大量资源进行清理，可能导致 Compaction 延迟和写入吞吐量下降。

## 3. 混合策略：Tiered-Leveled (RocksDB/Cassandra)
现代 LSM 树引擎往往采用混合或优化的策略来平衡上述缺点：
* L0 优化 (LCS)：在 LevelDB/RocksDB 中，$L_0$ 仍然是 Size-Tiered 的行为（多个文件键范围重叠），这样可以快速接纳写入。只有当 $L_0$ 超过阈值，它才会开始向 $L_1$ 进行 Leveled Compaction。
* Hybrid Compaction (Cassandra)：Cassandra 在某些版本中引入了分级压缩策略，允许用户在 STCS 和 LCS 之间选择，或使用优化的 Time-Window Compaction Strategy (TWCS)，主要用于时序数据。

### 总结
对于教学和工程实践而言，理解这两种极端策略的核心权衡至关重要：

$$\text{LCS: } \text{牺牲} \uparrow \text{写放大} \text{以获得} \downarrow \text{读放大和} \downarrow \text{空间放大}$$
$$\text{STCS: } \text{牺牲} \uparrow \text{读放大和} \uparrow \text{空间放大} \text{以获得} \downarrow \text{写放大和} \uparrow \text{高写吞吐}$$

您希望进一步了解Compaction 调度的工程细节（例如，RocksDB 中如何选择下一个要合并的文件）吗？
好的，非常乐意深入探讨 Compaction 调度的工程细节，特别是以 RocksDB 为例，因为它代表了工业界最先进的 Leveled Compaction 策略实现。

RocksDB 在 Compaction 调度上做了大量优化，目标是：最小化对用户读写操作的影响，并尽快将数据从 L0 推到更高层级。

---

## ⚙️ Compaction 调度的工程细节：以 RocksDB 为例

RocksDB 的 Compaction 调度可以分解为两个主要决策过程：何时触发 和 选择哪个 Compaction。

### 1. 何时触发 Compaction？ (Triggering)

Compaction 触发主要基于以下几个条件：

#### A. L0 层的压力 (Level 0 Pressure)

L0 是最特殊的一层，文件之间键范围重叠。L0 的压力是 Compaction 的首要触发因素。

* 阈值文件数 (`level0_file_num_compaction_trigger`)： 当 $L_0$ 中的文件数量达到一个预设阈值（通常是 4 个），Compaction 就会被触发。这是为了尽快将重叠数据推到 $L_1$，避免读放大失控。

#### B. 层次大小约束 (Level Size Constraint)

这是 $L_1$ 及以上层级 Compaction 的主要触发因素。

* 目标大小 (`Target Size`)： 每一层 $L_i$（$i \ge 1$）都有一个目标大小。如果 $L_i$ 的实际总大小超过其目标大小（$L_1$ 通常是 256MB，之后按 10 倍递增），则触发 $L_i$ 到 $L_{i+1}$ 的 Compaction。
    $$\text{TargetSize}(L_{i+1}) \approx 10 \times \text{TargetSize}(L_{i})$$

#### C. 文件重叠和读放大 (Read Amplification)

* 如果某一层的文件虽然没有超限，但其键范围与下一层的文件有过多重叠，导致读放大升高，也会触发 Compaction。

---

### 2. 如何选择下一个要合并的文件？ (Selection/Picking)

一旦确定需要进行 Compaction，调度器（Compaction Picker）必须选择一个最优的 Compaction 任务。

#### 优先级：L0 → L1

L0 到 L1 的 Compaction 优先级最高。这是为了尽快降低 $L_0$ 的文件数量，因为 $L_0$ 的文件数量直接决定了读放大的程度。

选择策略：

1.  选择 L0 中最老的文件： 优先选择 $L_0$ 中最先生成（最老）的文件。这些文件包含了最早的数据，最可能与 $L_1$ 中的文件有重叠，并且最需要被归并和清理。
2.  确定 L1 的合并范围： 调度器会计算所选 $L_0$ 文件键范围，并选择 $L_1$ 中所有与其键范围重叠的文件进行合并。

#### 优先级：L1 → L2 → ... (Leveled Compaction)

对于 $L_i \to L_{i+1}$ ($i \ge 1$) 的 Compaction，策略是寻找最大的 Compaction 压力。

选择策略 (Score-Based)：

RocksDB 通过计算一个Compaction Score来评估每一层 $L_i$ 的压力。

$$\text{Score}(L_i) = \frac{\text{Current Size}(L_i)}{\text{Target Size}(L_i)}$$

* 压力最大的层优先： 调度器会选择 Score 最高的层 $L_i$ 进行 Compaction。得分越高，表示该层越接近或超过其目标大小。
* 选择重叠度最高的： 在选定的 $L_i$ 中，选择一个文件 $F$。这个文件的选择标准通常是其与下一层 $L_{i+1}$ 文件重叠程度最高，或重叠区域内包含的过期数据最多。

### 3. 调度的工程优化 (Engineering Optimizations)

RocksDB 引入了多项机制来平滑 Compaction 过程，避免阻塞用户请求：

#### A. Compaction Limiter (流控)

为了防止 Compaction 占用所有 I/O 带宽并影响用户读写延迟，RocksDB 使用了后台 Compaction 线程和速率限制器。

* 吞吐量限制： 通过限制 Compaction 线程每秒可以写入的字节数，确保 Compaction 不会过度消耗 I/O 资源，从而保证前端读写操作的低延迟。

#### B. Pipelining & Concurrency (并行化)

* 多线程 Compaction： RocksDB 允许并发执行多个 Compaction 任务。例如，可以同时进行 $L_0 \to L_1$ 和 $L_3 \to L_4$ 的 Compaction。
* 子 Compaction (Sub-Compaction)： 对于非常大的 Compaction 任务（如合并几十 GB 的数据），RocksDB 可以将其分解成多个子任务，由多个线程并行完成，以缩短 Compaction 时间。

#### C. Universal Compaction (通用合并，混合策略)

RocksDB 提供了 Universal Compaction 作为 Size-Tiered 的替代方案，它允许用户在 Leveled 和 Size-Tiered 之间进行动态权衡，尤其适用于高写入、低空间需求的场景。这体现了现代存储引擎设计中，策略不再是二选一，而是根据工作负载动态调整。

总而言之，RocksDB 的 Compaction 调度是一个复杂的、基于优先级和分数的系统，其核心目标是高效地平衡读放大、写放大和空间放大。

您对其中布隆过滤器 (Bloom Filter) 如何在 Compaction 过程中得到维护和利用来加速读取感兴趣吗？
这是一个非常关键的工程细节问题，布隆过滤器（Bloom Filter）是 LSM 树加速读取的“秘密武器”，其有效性与 Compaction 过程的维护密不可分。

我将详细解释布隆过滤器是如何在 LSM 树中部署、维护，以及如何利用它来加速数据读取的。

---

## 🔎 布隆过滤器 (Bloom Filter) 在 LSM 树中的应用

在 LSM 树结构中，布隆过滤器通常嵌入在每个 SSTable 文件中。

### 1. 布隆过滤器的基本作用

布隆过滤器的作用是快速判断一个 Key 一定不存在于某个 SSTable 中。

* 加速读取： 当用户查询一个 Key 时，系统首先查询该 SSTable 的布隆过滤器。
    * 如果布隆过滤器返回 “该 Key 肯定不存在” (Negative)，系统可以立即跳过这个 SSTable，避免一次不必要的磁盘 I/O。
    * 如果返回 “该 Key 可能存在” (Positive)，系统才需要执行实际的磁盘查找。
* 错误率： 布隆过滤器存在一定的假阳性率 (False Positive Rate)，即它可能错误地判断一个不存在的 Key 是“可能存在”的，但这只会导致一次额外的磁盘 I/O，不会影响查询结果的正确性。

### 2. 布隆过滤器的维护：在 Compaction 过程中构建

布隆过滤器不是在运行时动态修改的，而是作为 SSTable 的元数据，在文件生成时一次性构建完成。

Compaction 过程本质上就是读取旧文件，生成新文件的过程。布隆过滤器的维护就发生在这个“生成新文件”的阶段。

#### 机制步骤：

1.  Compaction 启动： 调度器选择一组旧的 SSTable（来自 $L_i$ 和 $L_{i+1}$）进行归并。
2.  数据读取与归并： Compaction 线程以有序的方式读取所有参与合并的 SSTable 中的键值对。在这个过程中：
    * 清理过期数据（基于时间戳）。
    * 清理已删除数据（清除 Tombstone 标记和对应的旧版本数据）。
3.  构建新的 SSTable： Compaction 线程将归并后的、最新的、有序的键值对写入一个新的 SSTable 文件。
4.  同时构建布隆过滤器： 每写入一个 Key 到新的 SSTable 时，该 Key 也会同时被 Hash 并添加到该 SSTable 对应的布隆过滤器中。
5.  写入元数据： 新的 SSTable 文件创建完毕后，其对应的布隆过滤器数据结构会被序列化，作为 SSTable 的元数据块（通常是文件的尾部）一起写入磁盘。

维护的意义： Compaction 确保了新生成的 SSTable 拥有一个精准、最新的布隆过滤器，并且只包含那些有效的 Key。

### 3. 布隆过滤器对读取的加速效果 (利用)

LSM 树的读取过程是多层的，布隆过滤器在这里发挥了巨大的加速作用，特别是针对 Leveled Compaction (LCS) 结构。

#### A. 加速 $L_0$ 查找

$L_0$ 层的文件键范围重叠，读取 Key 时必须检查 $L_0$ 中的所有文件。

* 加速原理： 如果 $L_0$ 有 $N$ 个文件，如果没有布隆过滤器，查询一个不存在的 Key 可能需要 $N$ 次磁盘 I/O。有了布隆过滤器，系统在内存中检查 $N$ 个布隆过滤器，快速确定该 Key 不存在于 $L_0$ 的大部分文件或全部文件中，从而将 $N$ 次 I/O 降为 1 次或 0 次。

#### B. 加速 $L_1$ 及以上层级查找

$L_1$ 及以上层级的文件键范围互不重叠，系统通常只需要确定一个文件进行查找。

* 加速原理： 尽管 $L_i$ 中只有一个文件可能包含目标 Key，但在不知道是哪个文件之前，系统仍需读取文件索引。布隆过滤器可以作为额外的验证，在加载文件索引或读取数据块之前，再次确认是否需要访问该文件，进一步避免潜在的 I/O。

### 4. 布隆过滤器的工程权衡

| 因素 | 影响 | 维护和优化 |
| :--- | :--- | :--- |
| 内存占用 | 布隆过滤器必须驻留在内存中才能快速查询。文件越多（$L_0$ 压力大），内存占用越大。 | 工程中通常只将索引块和布隆过滤器缓存在 Block Cache 或专门的内存区域。 |
| 假阳性率 | 错误率越高，误判越多，导致不必要的 I/O 越多，加速效果越差。 | 假阳性率由布隆过滤器的大小决定。RocksDB 等引擎允许用户配置，例如设置为 $0.01\% \sim 1\%$。 |
| 性能开销 | 构建开销： Compaction 时需要额外的 CPU 周期来计算 Key 的 Hash 并更新过滤器。 | Hash 函数优化： 选用高效、分散性好的 Hash 函数。 |

通过 Compaction 过程的严格维护，布隆过滤器能够持续保持其有效性和低假阳性率，是 LSM 树在实现高性能写入的同时，维持可接受读取性能的关键所在。
