# LSMT

今天来聊聊lsm tree，它的全称是log structured merge tree ，简单来说，lsm tree可以认为是针对传统b树在磁盘写入上低劣表现的一种优化，其核心思想的核心就是放弃部分读能力，换取写入的最大化能力。

https://www.cnblogs.com/shenzhaohai1989/p/3893123.html

在我们介绍LSMT的原理之前，我们先来介绍一下它的子结构SSTable。

第一次看到这个单词的时候觉得一头雾水是正常的，SSTable的全称是Sorted String Table，本质就是一个KV结构顺序排列的文件。我们来看下下图：

[分布式——吞吐量巨强、Hbase的承载者 LSMT](https://mp.weixin.qq.com/s?__biz=MzUyMTM5OTM2NA==&mid=2247484853&idx=1&sn=99fa9bf9cc6a31d1f248a87c25966858&chksm=f9daf89ecead71885c7fb7cabc2ba719500aea4a8af277cd0744536dedd9b3dbead5f9253898&scene=21#wechat_redirect)

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

非常好的问题！您对LSM树的理解已经触及了现代数据库存储引擎的核心。我们来详细拆解一下。

核心答案

是的，您的理解基本正确。LSM树是一种数据存储的格式和结构，但它并不直接存储我们熟悉的“表数据”（如一行行的用户信息），而是存储构成数据库的最基础单元——键值对（Key-Value Pair）。

许多现代数据库（如 Google LevelDB/RocksDB、Apache Cassandra、HBase 等）的存储引擎正是基于LSM树构建的。即使是您熟悉的 MySQL，其流行存储引擎 MyRocks（由Facebook开发）也使用LSM树来替代传统的B+树。

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