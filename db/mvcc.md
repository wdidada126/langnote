# mvcc

PostgreSQL MVCC 机制
核心：Heap Tuple Header + CID (Command ID) 与 Snapshot
PostgreSQL的策略更先进。它的多版本模型是数据库教科书的经典实现，可见性判断是确定性的逻辑运算，没有回溯链的复杂性和不确定性，对只读查询和复杂分析的支持是天生的优势。

MVCC 简介
MVCC（Multi-Version Concurrency Control，多版本并发控制）是一种在数据库系统中广泛使用的并发控制机制。它通过维护数据的多个版本来处理并发事务，从而提高数据库的并发性能和响应能力。MVCC 的主要优点包括提高并发性能、降低死锁风险等。
MVCC 的工作原理
1.当前读和快照读：
当前读：在 MySQL 中，当前读是一种读取数据的操作方式，它可以直接读取最新的数据版本，并在读取时保证其他并发事务不能修改当前记录。MySQL 提供了两种实现当前读的机制：一致性读和锁定读。
快照读：快照读是在读取数据时读取一个一致性视图中的数据。MySQL 使用 MVCC 机制来支持快照读，每个事务在开始时会创建一个一致性视图，该视图反映了事务开始时刻数据库的快照。
2.Undo 日志：
Undo 日志是 MVCC 能够得以实现的核心。它分为插入 Undo 日志和更新 Undo 日志，分别在插入和更新或删除操作中生成。Undo 日志用于事务回滚和 MVCC 实现。
3.版本链：
在 MVCC 中，每次更新操作，旧值会被保存到一条 undo 日志中，随着更新次数的增加，所有的版本会通过 roll_pointer 属性连接成一个链表，称之为版本链。
4.Read View：
一致性视图（Read View）是用来判断版本链中的哪个版本对当前事务是可见的。Read View 维护系统当前活跃事务的 ID，并根据这些 ID 来判断数据版本的可见性。
vMVCC 介绍
vMVCC 是一个基于 MVCC 的事务库，旨在减少编写并发应用程序代码的工作量。它使用 Go 语言实现，并使用 Perennial、Iris 和 Coq 进行验证。vMVCC 的主要特点包括：
提供高性能的事务处理能力。
通过机器检查证明其正确性，确保所有事务都能正确处理。
vMVCC 的设计和实现
1.数据结构：
vMVCC 使用 tuple 数据结构，包含多个版本、tslast 字段和用于同步访问的互斥锁。每个版本对应一个时间戳范围，表示其有效性。
2.事务处理：
vMVCC 通过为每个事务分配一个严格递增的时间戳来实现 MVCC。事务在提交时创建新版本，并通过互斥锁确保修改的原子性。
3.垃圾回收：
vMVCC 使用后台垃圾收集器来回收不再使用的版本，确保版本在不再被任何事务访问时被删除。
4.时间戳生成：
vMVCC 使用 CPU 时间戳计数器（如 x86 机器上的 RDTSC）生成严格递增的时间戳，避免了共享内存计数器的争用。
vMVCC 的验证
vMVCC 的验证使用了预言变量（prophecy variables），允许证明在事务的线性化点之前预测事务的行为，从而简化了对 MVCC 事务的验证。预言变量的使用使得 vMVCC 能够在事务提交时更新逻辑状态，即使事务体尚未执行。
vMVCC 的性能评估
vMVCC 在 YCSB 和 TPC-C 工作负载下的性能表现与 Silo（一种高性能事务数据库系统）进行了比较。结果显示，vMVCC 在某些工作负载下的性能接近 Silo，证明了其在并发事务处理中的有效性。
通过以上介绍，可以看出 MVCC 和 vMVCC 在数据库并发控制和事务处理中的重要性和优势。希望这些信息能帮助你更好地理解这些技术。


在 MySQL 中，Read View 是 MVCC（多版本并发控制）机制中的一个重要概念，用于处理快照读（Snapshot Read）。Read View 是在事务开始时创建的，用于确定事务可以看到哪些数据版本。以下是关于 MySQL 中 Read View 的一些关键点：
1.一致性视图（Consistent View）：
在可重复读（Repeatable Read）隔离级别下，MySQL 使用一致性视图来实现当前读。事务开始时，MySQL 会创建一个一致性视图，该视图反映了事务开始时刻数据库的快照。
2.Read View 的作用：
Read View 确保事务在执行期间看到的数据是一致的。在事务的整个生命周期内，无论其他事务如何修改数据，该事务始终使用一致性视图来读取数据。
3.Read View 的可见性规则：
Read View 会维护以下几个字段：
m_creator_trx_id：创建 Read View 的事务 ID。
m_up_limit_id：在创建 Read View 时，已提交事务的最大事务 ID。
m_low_limit_id：在创建 Read View 时，未提交事务的最小事务 ID。
m_ids：在创建 Read View 时，所有活跃事务的事务 ID 列表。
4.版本链的可见性判断：
当事务访问某个数据版本时，Read View 会根据以下规则判断该版本是否可见：
1.如果被访问版本的 DB_TRX_ID 属性值与 m_creator_trx_id 值相同，表示当前事务正在访问自己所修改的记录，因此该版本可以被当前事务访问。
2.如果被访问版本的 DB_TRX_ID 属性值小于 m_up_limit_id，说明生成该版本的事务在当前事务生成 Read View 之前已经提交，因此该版本可以被当前事务访问。
3.如果被访问版本的 DB_TRX_ID 属性值大于或等于 m_low_limit_id，说明生成该版本的事务在当前事务生成 Read View 之后才提交，因此该版本不能被当前事务访问。
4.如果被访问版本的 DB_TRX_ID 属性值位于 m_up_limit_id 和 m_low_limit_id 之间，则需要进一步检查 DB_TRX_ID 是否在 m_ids 列表中。如果在列表中，说明在创建 ReadView 时生成该版本的事务仍处于活跃状态，因此该版本不能被访问；如果不在列表中，说明在创建 Read View 时生成该版本的事务已经提交，因此该版本可以被访问。
5.Read View 的生成时机：
在可重复读（Repeatable Read）隔离级别下，每次 SELECT 数据前都生成一个 ReadView。
在读未提交（Read Uncommitted）隔离级别下，事务可以读取其他事务尚未提交的数据，因此不需要使用 Read View。
在串行化（Serializable）隔离级别下，事务具有最高的隔离性，通过锁机制保证事务之间的串行执行，因此也不需要使用 Read View。
通过以上规则，MySQL 的 MVCC 机制能够确保在高并发环境下，事务读取数据时的一致性和隔离性。

根据我查到的资料，MVCC是为了解决事务并发中的脏读和幻读问题。那么对于每种情况我们来具体分析下，
脏读，是在读未提交的隔离级别中，读取到的数据最终没有被提交，被回滚了。那么解决这个问题本来应该禁止读未提交的，因为这本身就是错的，或者说概率错，但是为了并发性能，数据库发明了一个版本控制的手段，让事务在不加锁的情况下依然能读。但是，这个读的数据是旧的，或者说依然是“可能假”，因为这要基于另一个操作这个数据的事务最终是否会提交，提交就是假数据，未提交回滚了那就是真数据。如果事务读到了最终假的数据，那么基于这个假数据所做的后续事务操作还有什么意义？？
幻读，是针对事务中重复读同一个数据结果不一致的问题，原因是在两次读之间被其他事务提交修改了。要解决这个问题，本来应该尽可能避免重复读或者加锁来保证读取一致性，但是出于并发性能的考虑，数据库试图利用MVCC解决这个问题。当重复读同一个数据的时候，会读到当前事务启动之前最新的数据版本。但是这个数据版本自然可能是未来假的，那就依然会有类似前面的问题，基于一个可能假的数据进行后续事务操作，有什么意义？
MVCC到底解决了什么问题？

作者：江小北
链接：https://www.zhihu.com/question/654676856/answer/3519235620

首先，我们得明确一点，MVCC确实是为了解决事务并发中的脏读和幻读问题而设计的。但我们需要更深入地理解这些问题以及MVCC是如何应对的。关于脏读，你提到的情况确实存在。在没有MVCC的情况下，如果一个事务读取了另一个未提交事务的修改，而这个修改最终被回滚了，那么读取到的数据就是“脏”的。MVCC通过保存数据的多个版本来解决这个问题。每个事务在开始时都会获得一个唯一的时间戳或事务ID，当事务尝试读取数据时，它会根据这个时间戳或事务ID来获取相应的数据版本。这样，即使其他事务对数据进行了修改但尚未提交，当前事务也只会读取到它开始之前的数据版本，从而避免了脏读。至于幻读问题，你提到的情况是在两次读取之间，数据被其他事务修改并提交，导致读取结果不一致。MVCC同样可以解决这个问题。通过保存数据的多个版本，并确保每个事务在读取时只能看到它开始之前的数据版本，MVCC保证了在同一个事务中的多次读取会看到一致的数据视图。这样，即使其他事务在此期间对数据进行了修改并提交，也不会影响到当前事务的读取结果。现在来回答你的问题：“MVCC到底解决了什么问题？”简单来说，MVCC解决了以下问题：脏读问题：通过确保每个事务只能读取到它开始之前的数据版本，避免了读取到其他未提交事务的修改。幻读问题：通过在同一事务中提供一致的数据视图，防止了在两次读取之间数据被其他事务修改导致的不一致性。提高了并发性能：由于MVCC允许多个事务同时读取和写入数据而不会相互阻塞（除非存在写冲突），因此它大大提高了数据库的并发性能。总的来说，MVCC通过保存数据的多个版本并为每个事务提供一致的数据视图，有效地解决了脏读和幻读问题，并提高了数据库的并发性能。虽然它可能增加了存储空间的开销和管理的复杂性，但在许多高并发场景下，这些开销是值得的。

Posgres的MVCC实现牛逼不，牛。serial snapshot isolation是很强。
是的,PostgreSQL的MVCC(Multiversion Concurrency Control,多版本并发控制)实现确实非常强大和出色。其中的串行快照隔离(Serial Snapshot Isolation)是PostgreSQL MVCC的核心机制之一,是它支持高并发读写的关键所在。
具体来说,PostgreSQL的MVCC及串行快照隔离机制有以下几个优点:
1. 高并发性能
   - MVCC允许多个事务并发读取同一数据,而不会相互阻塞。这大大提升了数据库的并发处理能力。
   - 串行快照隔离确保每个事务看到的数据都是一致的,不会出现脏读、不可重复读等问题。
2. 事务隔离性
   - 串行快照隔离是最高级别的隔离级别,可以避免幻读等隔离问题。
   - 即使事务之间存在并发,也能保证事务的原子性和隔离性。
3. 快照一致性
   - MVCC机制会为每个事务维护一个数据快照,确保事务内部看到的数据是一致的。
   - 即使数据在事务执行过程中发生变更,事务内部也能看到一致的快照数据。
4. 数据库恢复
   - MVCC的快照机制有利于数据库的恢复和审计,可以轻松地实现点in时间恢复。
5. 低锁开销
   - MVCC不需要对数据行加锁即可实现并发控制,大大降低了锁的开销。

总的来说,PostgreSQL的MVCC及串行快照隔离机制是其数据库引擎的核心优势之一,确实是非常出色的并发控制技术。这也是PostgreSQL广受欢迎的重要原因之一。

好的,让我来详细介绍一下串行快照隔离(Serializable Snapshot Isolation,SSI)的论文和代码实现。
论文方面:

- 串行快照隔离最初由Michael Cahill等人在2008年发表于SIGMOD会议上的论文《Serializable Isolation for Snapshot Databases》中提出。
- 论文中提出了一种基于依赖图的SSI算法,可以在不牺牲并发性的情况下实现可串行化的事务隔离。
- 论文详细阐述了SSI的原理和实现细节,包括如何检测和解决可串行化冲突。

代码实现方面:

- PostgreSQL就是最著名采用SSI机制的数据库系统之一。
- PostgreSQL的SSI实现主要集中在以下几个模块:
  1. 事务管理模块:维护事务的快照信息和依赖关系。
  2. 锁管理模块:检测可串行化冲突并加锁。
  3. 查询执行模块:根据事务快照提供一致的数据视图。
  4. 恢复模块:支持基于SSI的数据库恢复。
- PostgreSQL的SSI实现在9.1版本中引入,并在之后的版本中不断完善和优化。
- 除了PostgreSQL,Oracle数据库和某些NoSQL数据库如FaunaDB也采用了类似的SSI机制。

## 论文
好的，MVCC（多版本并发控制）是现代数据库管理系统的核心并发控制机制。它通过数据多版本化来高效处理读写冲突，极大提升了系统的并发性能。
以下是一些关于 MVCC 的开创性、奠基性以及具有深远影响的学术论文。阅读这些论文可以帮助你从根源上理解 MVCC 的设计哲学、权衡取舍和演进历程。
奠基性论文（理解 MVCC 的起源）
这些论文首次形式化或定义了 MVCC 的基本概念。

1. 《Concurrency Control in Distributed Database Systems》
• 作者： Phil Bernstein, Nathan Goodman (1981)
• 核心贡献： 虽然这篇论文不完全是关于 MVCC，但它系统地总结了并发控制的各种方法。在 MVCC 被明确定义之前，它是理解并发控制领域的必读文献，为后续 MVCC 的研究提供了理论基础。

2. 《Multiversion Concurrency Control - Theory and Algorithms》
• 作者： C. H. Papadimitriou (1982)
• 核心贡献： 这是一篇非常理论化的论文，首次形式化地描述了 MVCC 的理论模型和算法。它定义了多版本时间戳排序协议，并讨论了可串行化理论。适合希望深入理解 MVCC 形式化基础和正确性证明的读者。

系统实现的开山鼻祖（看理论如何落地）
这些论文描述了最早将 MVCC 成功应用于实际数据库系统的设计。

3. 《The Design of the Postgres Storage System》（以及系列论文）
• 作者： Michael Stonebraker 等 (1987)
• 核心贡献： Postgres 是第一个真正实现 MVCC 的主流关系型数据库系统。这篇论文描述了其存储系统的设计，包括如何通过元组级版本控制来处理并发。理解 Postgres 的 MVCC 实现是理解所有后续 MVCC 变种的基础。
• 关键思想： 将新版本的数据行直接追加到表中，通过指针将不同版本的行链接起来。这被称为 “仅追加”或“堆元组”的 MVCC 实现。

4. 《Aries: A Transaction Recovery Method Structured to Support a Fine-Granularity Locking and Partial Rollbacks》（1992）及相关的《ARIES/KVL: A Key-Value Locking Method for Concurrency Control》
• 作者： C. Mohan 等 (IBM)
• 核心贡献： ARIES 是 IBM DB2 的恢复和并发控制算法的基石，对整个行业产生了巨大影响。虽然 ARIES 本身是一个复杂的恢复协议，但它与一种称为“受索引锁”的并发控制方法紧密结合。它展示了如何在基于预写日志的系统中，将行级锁与版本控制思想结合，实现了高效的并发和可恢复性。许多现代数据库的 MVCC 实现都受到了 ARIES 思想的影响。
5. 《An Empirical Evaluation of In-Memory Multi-Version Concurrency Control》
• 作者： Yu Xia, 等 (CMU, 2017) - 来自 Andy Pavlo 的课题组
• 核心贡献： 这是一篇非常实用和现代的论文。它系统地对多种内存数据库的 MVCC 方案（如时间戳排序、乐观并发控制、两阶段锁等）进行了实证评估和比较。
• 为什么重要： 它不再讨论单个系统的设计，而是提炼出 MVCC 实现中的核心维度（如版本存储位置、垃圾回收机制、并发控制协议），并分析了不同设计选择对性能的影响。这篇论文是理解现代 OLTP 数据库（如 Hekaton, MemSQL, HyPer）中 MVCC 变种的绝佳材料。
现代发展与前沿趋势
这些论文代表了 MVCC 在分布式、新硬件等场景下的最新进展。
6. 《An Evaluation of Distributed Concurrency Control》（2017）
• 作者： Kyle Kingsbury (Jepsen 作者) 等
• 核心贡献： 将 MVCC 的讨论扩展到了分布式数据库领域。分析了在分布式环境下实现 MVCC 的挑战，例如如何分配全局单调递增的时间戳（如使用 TrueTime、HLC 混合逻辑时钟），以及如何协调跨分片的事务。
7. 《The Case for Deterministic Database Systems》（2010）及后续相关论文
• 作者： Philip A. Bernstein 等
• 核心贡献： 提出了一种颠覆性的思想：通过预先确定事务的执行顺序来避免运行时冲突，从而从根本上消除或简化了并发控制（包括 MVCC）的复杂度。H-Store/VoltDB 和 Calvin 是这一流派的代表。阅读这类论文可以帮助你理解 MVCC 的替代方案及其适用场景。
8. 与 索引 和 垃圾回收 相关的论文
MVCC 的成功离不开高效的索引和垃圾回收（版本回收）。
• 《Efficient Locking for Concurrent Operations on B-Trees》 (Lehman & Yao, 1981)： B-Link-Tree 的设计，允许在索引结构上的高并发，与 MVCC 配合极佳。
• 各大数据厂商（Oracle, SQL Server, MySQL/InnoDB）都有关于其 MVCC 垃圾回收机制的专利和内部技术报告，这些是理解工业级实现细节的关键。
如何查找和阅读这些论文？
1.  推荐网站：
    ◦ Google Scholar： 搜索论文标题。
    ◦ ACM Digital Library / IEEE Xplore： 计算机领域最重要的学术数据库。
    ◦ arXiv.org： 可以找到许多最新的预印本论文。
2.  搜索关键词：
    ◦ "multiversion concurrency control" paper
    ◦ "MVCC" survey (可以找到综述性论文，快速了解全貌)
    ◦ "Postgres MVCC"
    ◦ "in-memory database MVCC"
3.  阅读建议：
    ◦ 从现代论文开始： 比如先读 CMU 的那篇实证评估 (论文 5)，它提供了一个很好的框架，让你带着问题去读早期的论文。
    ◦ 结合源码： 在阅读 Postgres 或 MySQL InnoDB 相关的论文时，可以结合它们的源代码（如InnoDB的read view实现）来理解，效果更佳。

这些论文共同描绘了 MVCC 从理论提出、系统实现到不断优化和适应新场景的完整发展图景。希望这个列表对你有所帮助！

## MVCC 综合笔记（截至 2026-08）

### 正确的心智模型

MVCC（Multi-Version Concurrency Control，多版本并发控制）不是一个唯一算法，而是一类并发控制设计：同一逻辑数据可保留多个版本；读操作依据自己的 snapshot 选择可见版本；写操作创建或标记版本，再以锁、验证或提交协议处理写写冲突。目标是在明确隔离语义下减少读写阻塞，不是消灭所有锁、冲突、回滚和重试。

```text
逻辑行 account(id=1)

V1: balance=100, commit_ts=100  <- 已提交旧版本
V2: balance= 90, commit_ts=120  <- 已提交当前版本
V3: balance= 80, T30 未提交     <- 仅 T30 自己可见

snapshot(ts=110) 读取 V1
snapshot(ts=130) 读取 V2
```

因此，旧文中“快照读到的是可能最终回滚的假数据”的说法不准确。在常见的 RC、RR/Snapshot Isolation 实现中，普通一致性读不读取其他事务未提交的版本，只读快照边界前已提交的版本和当前事务自己的修改。它读到的是**可能较旧但已经提交**的数据；业务风险来自陈旧快照、写偏斜或读后写竞争，而不是把他人的未提交结果当成事实。

MVCC 也不单独决定隔离级别或幻读行为。是否防止幻读、写偏斜和序列化异常，取决于 snapshot 的创建时机、写冲突规则、谓词/范围锁、SSI 验证或串行执行等完整协议。InnoDB、PostgreSQL、TiDB、Oracle、SQL Server 的版本布局与冲突策略不同，不能把某一家的 Read View 当成 MVCC 定义。

| MVCC 常带来的收益 | 仍需要的机制 |
| --- | --- |
| 普通读可在不阻塞写的情况下读取一致快照。 | 写写冲突检测、行/范围锁、唯一约束和死锁/超时处理。 |
| 长查询可以看到稳定历史视图。 | undo/旧 tuple/时间戳的垃圾回收、保留策略与长事务治理。 |
| 可用快照实现更高并发。 | 对余额、库存等不变量使用锁、约束或可串行化隔离。 |
| 可将读路径与写路径解耦。 | WAL/redo、崩溃恢复、提交顺序和分布式提交协议。 |

官方参考：

- MySQL InnoDB 一致性读：https://dev.mysql.com/doc/refman/8.0/en/innodb-consistent-read.html
- MySQL 锁与事务模型：https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-transaction-model.html
- PostgreSQL MVCC：https://www.postgresql.org/docs/current/mvcc-intro.html
- PostgreSQL 隔离级别与 SSI：https://www.postgresql.org/docs/current/transaction-iso.html
- TiDB MVCC GC：https://docs.pingcap.com/tidb/stable/dev-guide-timeouts-in-tidb/

### 事务、版本与可见性

MVCC 的三个基本动作是：

1. **开始/读**：取得或复用 snapshot。snapshot 是“允许看到哪些提交”的逻辑边界，不是整库物理复制。
2. **写入**：产生新版本、写入 undo，或以时间戳写入新的 KV 版本；同时对同一逻辑记录的并发写进行等待、冲突检测或验证。
3. **提交/回滚与回收**：提交使版本对适当的未来 snapshot 可见；回滚丢弃或标记无效版本；GC 只能回收不再被活跃 snapshot、备份或复制需要的历史版本。

```text
visible(version, snapshot, reader_txn) =
  true   if version 是 reader_txn 自己写入且仍有效
  true   if 创建事务已提交，且其提交时间/事务 ID 在 snapshot 边界内
  false  if 版本来自其他未提交、已回滚或晚于 snapshot 的事务
```

实现会用事务 ID 集合、`xmin/xmax`、提交时间戳、TSO/HLC 或 undo 链表达该规则。删除通常不是立即擦除旧版本，而是创建删除标记或新版本；对旧 snapshot 而言该行仍可能可见。更新在逻辑上常可视为“旧版本失效 + 新版本创建”，但各引擎的物理布局不同。

### 隔离级别：稳定 snapshot 不等于可串行化

| 隔离级别/模型 | 通常能避免 | 仍可能发生 | 使用判断 |
| --- | --- | --- | --- |
| Read Uncommitted | 很少有保障 | 脏读及更多异常 | 不应用于正确性敏感业务。 |
| Read Committed（RC） | 脏读 | 不可重复读、幻读、写偏斜/序列化异常 | 单语句读取最新已提交数据的常用默认。 |
| Repeatable Read / Snapshot Isolation（SI） | 脏读、同一快照内的不可重复读 | 写偏斜、部分序列化异常 | 读多写少且可处理冲突重试的业务。 |
| Serializable / SSI | 已提交事务等价于某个串行顺序 | 序列化失败，需要整体重试 | 强业务不变量、复杂读后写决策。 |

**写偏斜（write skew）** 是 MVCC 最重要的实战陷阱。两个医生值班记录都为 `on_call=true`，规则是“至少一人值班”。T1、T2 在同一 snapshot 都读到两人值班；T1 把 A 改为 false，T2 把 B 改为 false。它们更新不同的行，行级写写冲突检测可能允许两者提交，最终无人值班。每次读都一致、没有脏读，也可能没有传统的同一行不可重复读，但业务不变量被破坏。

解决方案不是笼统地“开启 MVCC”，而是选择能表达冲突范围的方案：

- 使用 `SERIALIZABLE`/SSI，并把 `SQLSTATE 40001` 等序列化失败视为可重试错误。
- 对代表不变量的行/范围使用 `SELECT ... FOR UPDATE`、谓词/范围锁，显式串行化竞争。
- 将共享约束收敛为单条原子更新，例如 `UPDATE quota SET remaining=remaining-1 WHERE remaining>0`，并检查受影响行数。
- 使用唯一约束、排他约束、外键或原子 upsert，而不是“先 SELECT 判断不存在，再 INSERT”。

可串行化不等于所有请求单线程执行。PostgreSQL 的 Serializable Snapshot Isolation（SSI）仍用 snapshot 执行，但跟踪可能造成异常的读写依赖，发现危险结构时终止一个事务；应用必须重试整个事务。PostgreSQL 的 Repeatable Read 实际是 Snapshot Isolation，能提供稳定 snapshot 并避免幻读，却仍可能出现序列化异常。

### InnoDB：版本链、Read View 与锁协作

InnoDB 的聚簇索引记录通常含 `DB_TRX_ID` 和 `DB_ROLL_PTR` 等隐藏信息。更新后的当前记录指向 undo log 中的历史映像，形成版本链；一致性读从当前版本开始，若不可见则沿 undo 链重建可见旧版本。redo/WAL 用于崩溃恢复和持久性，undo 同时服务回滚和一致性读，两者不要混为一谈。

```text
聚簇索引当前记录 V3
  DB_TRX_ID = 300
  DB_ROLL_PTR ----> undo: V2 (trx 200) ----> undo: V1 (trx 100)

Read View 判断 V3 不可见 -> 依次回溯 V2/V1 -> 返回首个可见版本
```

Read View 可抽象为“低水位、下一可分配事务 ID、创建时活跃事务 ID 集合、创建者 ID”。对某版本的创建事务 ID：自己写入可见；快照前已提交可见；快照时仍活跃或快照后开始的事务产生的版本不可见。理解规则即可，不应依赖某个源码字段名或把高低水位术语死记硬背。

| InnoDB 读/写路径 | 语义 | 关键点 |
| --- | --- | --- |
| 普通 `SELECT`（consistent nonlocking read） | 读取 Read View 下可见版本 | RC 通常每个一致性读新建 snapshot；RR 通常复用首次一致性读建立的 snapshot。 |
| `SELECT ... FOR UPDATE` / `FOR SHARE` | 锁定读，读取并锁定当前可用版本 | 用于读后即将更新、队列领取等；可能等待、死锁或超时。 |
| `UPDATE` / `DELETE` / `INSERT` | 当前读 + 写锁/索引锁 | 写写冲突仍会等待或死锁，MVCC 不让两个事务盲目覆盖。 |
| RR 范围锁定读/写 | 记录锁之外可使用 next-key/gap lock | 阻止范围内插入，保障锁定读语义。 |

旧文“RR 下每次 SELECT 都创建 Read View”需要修正：普通一致性读在 InnoDB 的 RR 下使用事务中首次一致性读建立的 snapshot；RC 下每个一致性读可获得新 snapshot。`SELECT ... FOR UPDATE`、`UPDATE`、`DELETE` 属于锁定/当前读，不是简单复用普通快照读。混用普通 `SELECT` 与锁定 DML 时，前者可能看历史快照、后者基于当前记录加锁，业务代码必须明确需要的是“稳定历史”还是“最新且预留修改权”。

InnoDB 在 RR 中不是仅靠 MVCC 就处理所有幻读；针对锁定范围访问使用 next-key/gap locking。`SKIP LOCKED` 用于工作队列吞吐时会刻意跳过锁定行，官方明确其返回不一致视图，不适合需要完整事务视图的一般业务。

长事务会让旧 undo 版本不能 purge：历史链变长，读旧版本和二级索引回表成本上升，并可能造成 undo/history list 膨胀。监控最老活跃事务、`History list length`、purge 进度、锁等待与死锁；把 idle in transaction、大批量 DML 或跨网络 RPC 包在事务中都是高风险做法。

参考：[InnoDB 一致性读](https://dev.mysql.com/doc/refman/8.0/en/innodb-consistent-read.html)、[锁定读](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html)、[事务优化](https://dev.mysql.com/doc/refman/8.4/en/optimizing-innodb-transaction-management.html)、[死锁处理](https://dev.mysql.com/doc/refman/8.4/en/innodb-deadlocks.html)。

### PostgreSQL：tuple 版本、VACUUM 与 SSI

PostgreSQL 在 heap tuple 中保存版本相关系统列，例如 `xmin`（创建该 tuple 的事务）和 `xmax`（删除或更新它的事务），并用 snapshot 决定可见性。更新通常创建新 tuple 并让旧 tuple 的 `xmax` 生效；旧版本留在表中，直到所有可能需要它的事务结束后由 VACUUM 回收。因此它不是 InnoDB 那种“当前记录 + undo 回溯链”的物理布局。

| PostgreSQL 模式 | snapshot 行为 | 重点 |
| --- | --- | --- |
| Read Committed（默认） | 每条语句开始时 snapshot | 同一事务两次查询可能不同；更新会等待并在必要时重评估目标。 |
| Repeatable Read | 首个非事务控制语句建立事务 snapshot | 稳定 snapshot，写冲突可报 serialization failure 并要求整笔重试。 |
| Serializable | 在 SI 之上追踪读写依赖 | SSI 检测潜在序列化异常，报 `40001`，应用整体重试。 |

PostgreSQL “读不阻塞写、写不阻塞读”描述的是普通 MVCC 读写路径，不表示任意操作永不等待。行锁、表锁、DDL、唯一约束、热点更新和 I/O 仍会造成等待或失败。VACUUM/autovacuum 是正确性和容量治理的一部分：长期事务或遗留 replication slot 会阻止 dead tuple 回收，形成 table/index bloat，严重时还会威胁事务 ID wraparound 防护。

SSI 的 predicate lock（`SIReadLock`）主要用于记录读写依赖，并不按传统锁那样阻塞写；检测到无法串行化的依赖结构时让一个事务失败。使用 `SERIALIZABLE` 时，应在应用中统一实现有限次数、指数退避的整笔重试，避免事务内部已经对外发送不可撤销副作用后才发现提交失败。

### TiDB/分布式 MVCC：时间戳与 GC 安全点

分布式 MVCC 常将 key 设计为 `(user_key, commit_ts)` 或等价形式，读以 `start_ts` 找到不晚于该 snapshot 的最新已提交版本。TiDB 以事务时间戳管理 MVCC 版本，并通过周期性 GC 回收不再需要的数据；长事务、备份、CDC、follower read 或 safepoint 机制会影响历史版本保留窗口。与单机数据库相比，还需处理全局时间戳、跨分片提交、region/leader 路由、网络重试和锁解析。

```text
T1: start_ts=100, 读 k -> 找 commit_ts <= 100 的最新版本
T2: start_ts=110, 写 k，提交 commit_ts=120
T1: 仍读旧版本；T3 start_ts=130 才能读到 T2 的版本
GC safe point 前进后，早于 safe point 且不再需要的版本可回收
```

分布式时间戳不是“所有机器系统时钟相同”。系统借助集中式 TSO、混合逻辑时钟或等价服务建立全局顺序，并在提交阶段验证冲突。MVCC 负责读到对应 snapshot，但跨分片事务是否原子还取决于 2PC、Percolator 类协议、Raft/Paxos 副本提交和故障恢复。不要从“使用 MVCC”推出“跨服务 exactly-once”或“任意长事务安全”。

### 版本回收、长事务与可观测性

版本的回收条件是“没有读者可能再需要它”，不是“写事务已经提交”。常见阻塞者包括长事务、空闲未提交连接、长查询、慢副本、备份、逻辑复制/CDC、保留 snapshot 和异常客户端。GC 太激进会让仍运行的 snapshot 无法读取，GC 太保守会导致磁盘膨胀、放大写入和降低缓存命中。

| 引擎/形态 | 版本位置 | 回收关注点 |
| --- | --- | --- |
| InnoDB | 当前聚簇记录 + undo 版本链 | purge、history list、undo 表空间、长 Read View。 |
| PostgreSQL | heap 中旧/new tuple | autovacuum、dead tuple、冻结、replication slot、bloat。 |
| LSM/KV（如 TiKV） | 多个带时间戳的 KV 版本 | GC safe point、compaction、长事务/备份/CDC 保留。 |
| 内存 MVCC | 行内/旁挂版本数组或链 | epoch/时间戳、内存回收、读者公告与 ABA 风险。 |

排障顺序：先找最老活跃事务/snapshot 与持续时间，再看版本保留指标、磁盘增长和 GC/purge/vacuum lag；随后确认备份、复制或 CDC watermark 是否阻塞；最后才调整保留参数或扩容。直接强制清理历史版本可能让正在执行的查询失败或降低恢复能力。

### 实战建模、SQL 与面试要点

1. 事务保持短小：不要在事务中等待用户输入、调用远程服务、循环处理百万行或长时间持有连接。
2. 对库存、余额、配额和状态机转移，优先用条件更新、唯一约束或显式锁，把不变量放进数据库可原子判断的语句。
3. 遇到死锁、锁等待、序列化失败、乐观写冲突，按错误码整体重试，设置次数上限、退避、幂等 request ID 与可观测日志。
4. 分清“展示页可接受旧数据”和“扣款前必须最新且可修改”的读需求；前者可用普通 snapshot/stale read，后者需要 current/locking read 或更强隔离。
5. 设计索引以缩小锁定范围和更新扫描范围；无索引的 `UPDATE ... WHERE` 既慢又可能扩大锁冲突。
6. 上线前用并发脚本验证读后写、范围插入、唯一键竞争、超时重试、事务回滚和长事务 GC，而不是只验证单线程结果。

常见问题：

- **MVCC 是否完全不用锁？** 否。普通 snapshot 读通常不加读锁，但写写冲突、锁定读、唯一/外键、范围保护和 DDL 仍依赖锁或验证。
- **MVCC 能否保证可串行化？** 不能自动保证。Snapshot Isolation 仍可能写偏斜；需 SSI、严格 2PL、串行执行或业务级原子约束。
- **undo、redo、binlog/WAL 的关系？** undo 支持回滚和旧版本可见性；redo/WAL 支持崩溃恢复/持久化；binlog 是 MySQL Server 层复制与变更日志，职责不同。
- **为什么 RR 仍要 next-key lock？** 普通一致性读可用稳定 snapshot；需要基于最新数据做范围更新或锁定读时，必须阻止范围内并发插入破坏当前读语义。
- **为什么长事务伤害很大？** 它固定历史可见边界，阻止回收旧版本，并增加 undo/VACUUM/GC、I/O 和恢复压力。

学习顺序：先读 [InnoDB Read View](mysql/innodb_read_view.md) 和 [MySQL MVCC](mysql/mysql_mvcc.md)，用两个会话演示 RC/RR 的普通读与 `FOR UPDATE`；再读 PostgreSQL 的 [MVCC 文档](https://www.postgresql.org/docs/current/mvcc-intro.html) 与 SSI 示例，复现写偏斜和 `40001` 重试；最后结合 [MVCC/OCC](mvcc_occ.md)、[悲观并发控制](mvcc_pcc.md)、[TiDB TSO](tidb/中心化TSO.md) 比较单机与分布式设计。掌握 MVCC 的标准不是背出隐藏字段，而是能根据业务不变量选择 snapshot、锁、约束、重试与版本回收策略。

## Java MVCC 库：`mvcc-api-java`（test-java-mvcc 仓库）

> 本节对应本机仓库 [test-java-mvcc](https://github.com/ibqo/test-java-mvcc)（含 submodule `java-mvcc-api`），是上文中"内存 MVCC"形态的一个完整 Java 17 参考实现，语义对齐 Node.js 版 `mvcc-api`（vMVCC 算法），可嵌入 JVM 应用作为快照隔离事务层。

### 定位与来源

- 仓库结构：根仓库 `test-java-mvcc/`（`pom.xml` + 测试说明），实际库在 submodule `java-mvcc-api/`（远程 `github.com/edidada/java-mvcc-api`）。
- Maven 坐标：`io.github.mvccapi:mvcc-api-java:1.0.0-SNAPSHOT`，`release=17`；运行时仅依赖 `slf4j-api`，测试用 JUnit 5 + logback。
- 目标：把 vMVCC 的核心算法——事务局部缓冲、嵌套快照、全局版本链、first-committer-wins 写冲突——以"存储边界接口 + 事务引擎"分离的方式移植到 JVM，方便对接内存/文件/数据库等任意后端。
- 与综合笔记的关系：它演示了上表"内存 MVCC"行的落地：版本按事务与键维护、旧版本靠活跃读者保留、读者归零即回收，正是"版本回收、长事务与可观测性"一节的工程化对照。

### 版本模型与可见性

库维护两个层面的版本号：

| 层面 | 含义 |
| --- | --- |
| 全局版本（root） | 根事务每次提交分配一个新的单调递增全局版本（`RootState.version()`），已提交值按版本写入存储；全局版本链用追加数组实现摊销 O(1)，回收截点用二分定位。 |
| 局部版本（local） | 事务内每次 create/write/delete 使 `localVersion` 自增，作为本事务内修订号；有活跃后代时记录修订历史（按 revision 有序，读时二分）。 |

- 快照 = 事务创建瞬间捕获 `(snapshotVersion, snapshotLocalVersion)`：嵌套事务创建时记下父的局部版本作为截止点，因此**父之后提交的修改对已创建的子事务不可见**。
- 读取路径（`read`）：先查自己 `changes`（读己之写）→ 沿父链按局部截止点二分查历史 → 再到根按全局快照查存储（`RootState.readAt(key, version)`）。
- 提交合并：嵌套提交调用父 `merge(child)` 逐键校验并合并到父的变更集；根提交把整个变更集 `persist` 到存储边界并推进全局版本。
- 写冲突（first-committer-wins）：合并时若 `lastVersion(key) > child.snapshotVersion`（全局被更新）或父侧 `keyVersions(key) > child.snapshotLocalVersion`（局部被更新），判定冲突并返回 `TransactionConflict(key, parent, child)`，败方提交返回失败结果。
- 历史回收：`activeDescendants` 归零时立即清除已无用的局部历史；根提交时若仍有活跃后代则先归档历史再清空待定变更。

### API 一览（包 `io.github.mvccapi`）

| 类型 | 职责 |
| --- | --- |
| `MvccStrategy<K,V>` | 同步存储边界接口：`read/write/delete/exists` 四个方法；值必须非 null。 |
| `AsyncMvccStrategy<K,V>` | 异步存储边界：方法返回 `CompletionStage`。 |
| `MvccTransaction<K,V>` | 核心事务引擎（`AutoCloseable`），详见下节方法清单。 |
| `AsyncMvccTransaction<K,V>` | 异步门面：内部委托 `MvccTransaction` + 阻塞适配器，存储阶段只在 worker executor 上 join，绝不在调用线程阻塞；嵌套返回异步事务。 |
| `MvccOptions` | 配置 record：`cacheCapacity`（LRU 容量，默认 1000，须 ≥0）、`threadSafe`（默认 true）；默认构造 `(1000, true)`。 |
| `TransactionResult<K,V>` | commit/rollback 结果：`success/label/error/conflict/created/updated/deleted`，`isSuccess()` 便捷判断。 |
| `TransactionConflict<K,V>` | 冲突详情：`key`、`parent`（父侧值）、`child`（子侧值）。 |
| `TransactionEntry<K,V>` | 单条变更：`key` + `data`。 |
| `TransactionChanges<K,V>` | 提交前净变更集：`created/updated/deleted` 三个列表（均不可变拷贝）。 |
| `InMemoryMvccStrategy<K,V>` | 参考/测试用内存存储实现。 |
| `internal.RootState` / `LruCache` / `MvccTrace` / `TransactionLock` | 根状态（全局版本链、持久化、回收）、LRU 缓存（含负缓存）、版本追踪日志、事务级读写锁。 |

`MvccTransaction` 方法清单：

```text
CRUD      create(K,V) write(K,V) delete(K) read(K) exists(K)
          isWrote(K) isDeleted(K)
嵌套      createNested() isRoot() hasCommittedAncestor() activeDescendantCount()
结束      commit() commit(label) rollback() rollback(label) close() isFinished()
变更集    getResultEntries() createdEntries() updatedEntries() deletedEntries()
预检      static checkConflicts(Collection<MvccTransaction>)   // 静态预检冲突键
观测      snapshotVersion() transactionId() localVersion()
          retainedGlobalVersionCount() cacheSize()
```

### 事务语义要点

- 根事务可复用：`commit` 持久化后不清空自身，可继续发起新的嵌套事务；嵌套事务 commit/rollback 后即 `finished`。
- `close()`（try-with-resources）：仅对未结束的**非根**事务自动 `rollback`，根事务需显式处理。
- 语义约束：`create` 已存在键、`write`/`delete` 不存在键会抛 `IllegalStateException`，调用前可用 `exists`/`read` 检查；`checkConflicts` 可在提交前批量预检并提前处理冲突键。
- 一致性等级：**Snapshot Isolation（快照隔离）**，不是可串行化；写偏斜需按上文"隔离级别"一节由应用层用约束或 SSI 兜底。
- 并发：默认 `threadSafe=true`，内部用事务级读写锁；`threadSafe=false` 时要求外部串行化（性能对比用）。异步 API 的线程池/调度开销不计入核心算法对比。
- 可观测：`MvccTrace` 输出创建/缓冲/读取/合并/冲突/提交/回滚的完整事件流，配合 `docs/06-version-tracing.md` 可逐版本回放。

### 功能列表

1. 基础 CRUD：create/read/write/delete + commit 持久化 + 变更集验证（created/updated/deleted 分类准确）。
2. 快照隔离：父事务在子创建后的修改对子不可见。
3. 读己之写：事务内 create/write/delete 立即可见。
4. 嵌套事务提交：子提交 → 合并到父 → 根提交最终持久化。
5. 嵌套事务回滚：回滚后父不受影响，根不落盘。
6. try-with-resources：`close()` 自动回滚未完成嵌套事务。
7. 写写冲突：first-committer-wins，败者拿到 `TransactionConflict` 详情（键、双方值）。
8. 不同键并行：不相交写集合的并发事务全部成功。
9. 长读事务：跨根提交持久化，旧快照读取结果保持不变。
10. 创建后删除：同事务 create+delete 净结果为空。
11. 高并发同键：32 并发同键写仅 1 个成功、其余冲突（first-wins）。
12. 冲突预检：`checkConflicts` 静态返回可能冲突的键集合。
13. LRU 缓存：`cacheCapacity` 限制已提交值缓存 + 负缓存，`cacheSize()` 可观测。
14. 配置校验：`MvccOptions` 非法参数（负数容量）抛异常。
15. 异步事务：`AsyncMvccTransaction` CRUD + 嵌套提交，CompletionStage 链式。
16. 状态管理：`isFinished` 标记、根可复用、已提交祖先检测（`hasCommittedAncestor`）。
17. 版本追踪：`MvccTrace` 事件日志与 `docs/06-version-tracing.md` 分析。
18. 线程安全：默认跨线程安全，并有并发单测覆盖。
19. 版本回收优化：全局版本链追加 O(1)、回收截点二分、活跃后代归零即清历史。

（README 记录：全部 16 组共 77 项断言通过，覆盖上表 1–16。）

### 快速开始

```java
MvccStrategy<String, String> store = new InMemoryMvccStrategy<>();
MvccTransaction<String, String> root = new MvccTransaction<>(store, new MvccOptions());

root.create("k", "v1");

try (MvccTransaction<String, String> tx = root.createNested()) {
    String v = tx.read("k");                    // "v1"（读父快照，读己之写优先）
    tx.write("k", "v2");
    TransactionResult<String, String> r = tx.commit("update-k");
    if (!r.isSuccess()) {
        System.out.println("conflict on " + r.conflict().key()); // first-committer-wins
    }
}

root.commit();                                  // 根持久化到存储
System.out.println(root.read("k"));             // "v2"
```

异步版本只需把 `MvccStrategy` 换成 `AsyncMvccStrategy`、事务换成 `AsyncMvccTransaction`，方法返回 `CompletableFuture`。

### 性能实测（2026-08-10，本仓库）

环境：macOS 12.7.6 x86_64、GraalVM JDK 17.0.12、Node.js 24.14.0，与 Node.js 参考实现按等价负载独立进程对比（3 样本中位数）：

| case | Node ns/op | Java ns/op | Java 加速比 |
| --- | ---: | ---: | ---: |
| hot-read | 208.85 | 46.16 | 4.52x |
| nested-write-commit | 4,314.78 | 2,694.65 | 1.60x |
| long-snapshot-update | 301,725.39 | 7,201.91 | 41.90x |

`long-snapshot-update` 大幅领先得益于长快照路径的优化（版本链追加 O(1)、回收二分定位、历史即时清除）。微基准受 CPU 调频/JIT/GC 影响，仅代表核心状态机在等价负载上的对齐，不代表真实文件系统/数据库/网络 Strategy 的端到端吞吐。

### 限制与使用注意

- 仅快照隔离：写偏斜不在库层拦截，需应用层约束（唯一键、条件更新）或更强的隔离机制。
- 值必须非 null、键不可为 null；create 重复键、write/delete 缺失键抛 `IllegalStateException`，属"业务校验而非冲突"，与写写冲突（返回 `TransactionResult`）是两回事。
- 根事务不因 `close()` 自动回滚；提交失败的根事务仍处于打开状态，需自行决定重试或回滚。
- `threadSafe=false` 只适合外部已串行化的场景；并发安全依赖 `MvccOptions.threadSafe()`。

### 参考文档（仓库 docs/）

| 文件 | 内容 |
| --- | --- |
| `01-node-api.md` / `02-node-algorithm.md` | Node.js 参考实现的 API 与算法（语义对齐来源） |
| `03-java-high-level-design.md` / `04-java-detailed-design.md` | Java 版高层与详细设计 |
| `05-performance.md` | 与 Node 参考实现的性能对比方法与实测 |
| `06-version-tracing.md` | 版本追踪日志格式与回放分析 |

结合上文的 [MVCC/OCC](mvcc_occ.md)、[悲观并发控制](mvcc_pcc.md) 与 [InnoDB Read View](mysql/innodb_read_view.md)，可以把本库当作"内存 MVCC"的最小可运行标本：先看它的快照读取与冲突检测，再对照 InnoDB 的 undo 版本链与 Read View 理解生产级实现的差异（本库无持久化日志、无锁等待队列、无 DDL/索引交互，版本回收完全在内存进行）。
