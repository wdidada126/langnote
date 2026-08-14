# OceanBase

COMPRESSION
REPLICA_NUM
BLOCK_SIZE
TABLET_SIZE
PCTFREE
LOB_INROW_THRESHOLD
LOCAL

# 逐个解释：这些全是 OceanBase 私有表参数（MySQL8 完全不支持）
你原来的 SQL 是 OceanBase 分布式数据库 语法，不是原生 MySQL，我给你大白话+原理+为什么 MySQL 要删掉全部讲清楚。

## 1. COMPRESSION = 'zstd_1.3.8'
表级压缩算法
- OceanBase 专属：指定数据块压缩算法（zstd 高速压缩）
- 作用：磁盘压缩、节省空间、提升IO性能
- MySQL8：没有这个参数；MySQL 压缩是页压缩/行压缩，语法完全不一样
- 处理：直接删掉

## 2. REPLICA_NUM = 3
副本数量（分布式多副本）
- OceanBase 分布式：数据存3个节点副本，高可用、容灾
- 作用：集群副本数，自动主从同步、故障切换
- MySQL8：原生没有表级副本；MySQL副本是实例级主从复制，不是表级
- 处理：直接删掉

## 3. BLOCK_SIZE = 16384
数据块大小（页大小），单位字节
- OceanBase：每个存储块大小 16KB
- 作用：底层存储IO、索引、数据读写最小单元
- MySQL8：页大小固定默认 16KB，全局配置，不能单表指定
- 处理：直接删掉（MySQL默认刚好也是16K，不用改）

## 4. TABLET_SIZE = 134217728
Tablet 分片大小（OceanBase 分布式分片）
- OceanBase 专属：一张表切成多个 Tablet 分片，每个分片最大 128MB
- 作用：分布式水平分片、均衡负载、并行存储
- MySQL8：没有 Tablet 分片概念；MySQL分区表语法完全不同
- 处理：直接删掉

## 5. PCTFREE = 0
页预留空闲空间百分比
- OceanBase/Oracle：数据页预留空闲比例，0=不留空间、满页存储
- 作用：更新、插入预留空间，减少页分裂
- MySQL8 InnoDB：默认有pctfree逻辑，但不支持手动指定这个参数
- 处理：直接删掉

## 6. LOB_INROW_THRESHOLD=4096
LOB大字段行内存储阈值
- OceanBase：varchar/blob/text大于4096字节，才存到单独LOB页；小于4K存在行内
- 作用：优化大字段读写性能
- MySQL8：InnoDB LOB存储逻辑内置，不支持手动配置该参数
- 处理：直接删掉

## 7. KEY ... BLOCK_SIZE ... LOCAL
LOCAL索引 + 索引块大小
- LOCAL：OceanBase 本地分区索引（不跨分片、本地生效）
- BLOCK_SIZE：索引单独块大小
- MySQL8：没有LOCAL分区索引语法；索引块继承表块大小，不能单独指定
- 处理：删掉 BLOCK_SIZE LOCAL，只保留普通 KEY 索引

# 一句话总结（面试/迁移必背）
| 参数 | 所属数据库 | 含义 | MySQL8 是否支持 | 迁移处理 |
|---|---|---|---|---|
| COMPRESSION | OceanBase | 表压缩算法 | 不支持 | 删除 |
| REPLICA_NUM | OceanBase | 分布式副本数 | 不支持 | 删除 |
| BLOCK_SIZE | OceanBase | 数据块大小 | 不支持（全局固定） | 删除 |
| TABLET_SIZE | OceanBase | 分布式分片大小 | 不支持 | 删除 |
| PCTFREE | OceanBase/Oracle | 页预留空闲 | 不支持手动配置 | 删除 |
| LOB_INROW_THRESHOLD | OceanBase | 大字段行内阈值 | 不支持 | 删除 |
| LOCAL | OceanBase | 本地分区索引 | 不支持 | 删除 |

# 为什么你之前执行报错？
因为 MySQL8 不认识上面任何一个关键字，必须全部删掉，只保留标准字段、主键、普通索引、InnoDB、utf8mb4，就是我给你的版本。

需要我把你之前所有OceanBase表，统一整理成一份完整MySQL8迁移规范文档吗？


https://www.oceanbase.com/zh

## 版本
v3.1.0_CE_BP1
on Jun 22, 2021

v3.1.5_CE
 on Apr 17, 2023

v4.0.0_CE
on Nov 1, 2022

v4.1.0_CE
on Apr 3, 2023

v4.2.0_CE
on Aug 30, 2023

发布日期	2025-08-20
版本号	V4.3.5_CE_BP2_HF4

5.7.25-OceanBase-v4.2.1.10

缺陷修复
修复插入或查询时间相关生成列或函数索引时，使用的Timezone和创建表时使用的地区定义的Timezone不一致，引起的内存泄漏问题。
修复备份恢复访问S3协议的对象存储时，必须指定s3_region的问题。
优化PL并发编译慢的问题，增加PLSQL_OPTIMIZE_LEVEL系统变量支持调整编译优化级别和并发数。
优化部分OLTP场景下的性能。


2024 OceanBase开发者大会
上海市闵行区 3199 号宝龙艾美酒店
2024年4月20日

2023 OceanBase开发者大会在京召开，国泰产险资深数据库专家舒明分享了《国泰产险的OceanBase上云实践》的主题演讲

OcenBase 4.3打造PB级实时分析数据库，可实现秒级实时分析。

https://www.oceanbase.com/docs/community-tutorials-cn-10000000000012249

https://github.com/oceanbase/oceanbase

据说在某个客户那里，出现了数据不一致 问题

OceanBase | 试用版安装初体验
https://blog.csdn.net/daiyejava/article/details/109379738

ob docker centos 7
https://www.oceanbase.com/docs/oceanbase-database-trial/oceanbase-database-trial/V2.2.50/fbgwds

https://www.zhihu.com/question/19841579/answer/131853733

为什么OceanBase架构特别适合双十一
感谢所有同学的共同努力，OceanBase分布式关系数据库渡过了一个成功的双十一：支持了支付宝核心的交易、支付、会员和账务等，并且创造了新的纪录：交易创建17.5万笔/秒、交易支付12万笔/秒、全天累计支付10.5亿笔！
其实，虽然不是刻意设计的，但OceanBase确实比传统数据库更适合像双十一、聚划算、秒杀以及银行国库券销售等短时间突发大流量的场景：·短时间内大量用户涌入·短时间内业务流量非常大，数据库系统压力非常大·一段时间（几秒钟、几分钟、或半个小时等）后业务流量迅速或明显回落
虽然2010年设计OceanBase架构时，其实并没有特别考虑到这个突发大流量的因素。让我们从OceanBase的架构说起。OceanBase是“基线数据（硬盘）”+“修改增量（内存）”的架构，如下图所示：

![ob_data](./imgs/ob_data.png)

即整个数据库以硬盘（通常是SSD）为载体，新近的增、删、改数据（“修改增量”）在内存，而基线数据在保存在硬盘上，因此OceanBase可以看成一个准内存数据库。这样的好处是：·写事务在内存（除事务日志必须落盘外），性能大大提升·没有随机写硬盘，硬盘随机读不受干扰，高峰期系统性能提升明显；对于传统数据库，业务高峰期通常也是大量随机写盘（刷脏页）的高峰期，大量随机写盘消耗了大量的IO，特别是考虑到SSD的写入放大，对于读写性能都有较大的影响·基线数据只读，缓存（cache）简单且效果提升·线上OceanBase的内存配置是支撑平常两天的修改增量（从OceanBase 1.0开始，每台OceanBase都可以写入，都承载着部分的修改增量），因此即使突发大流量为平日的10-20倍，也可支撑1~2个小时以上。
<img src="https://pic1.zhimg.com/v2-a9b596591401543db10953f18f4802c8_b.png" data-rawwidth="873" data-rawheight="257" class="origin_image zh-lightbox-thumb" width="873" data-original="https://pic1.zhimg.com/v2-a9b596591401543db10953f18f4802c8_r.jpg"/>
一个问题是：修改增量在内存，大概需要多大的内存？即使按双11全天的支付笔数10.5亿笔，假设每笔1KB，总共需要的内存大约是1TB，平均到10台服务器，100GB/台。另一个问题是：在类似双十一这种流量特别大的场景中，就像前面说到的，OceanBase内存能够支持峰值业务写入1~2个小时以上，之后OceanBase必须把内存中的增删改数据（“修改增量”）尽快整合到硬盘并释放内存，以便业务的持续写入。整合内存中的修改增量到硬盘，OceanBase称为每日合并，必然涉及到大量的硬盘读写（IO），因此可能对业务的吞吐量和事务响应时间（RT）产生影响。如何避免每日合并对业务的影响呢？OceanBase通过“轮转合并”解决了这个问题。众所周知，出于高可用的考虑，OceanBase是三机群（zone）部署：
<img src="https://pic4.zhimg.com/v2-739bc65497010958be4c5d81db78a42b_b.png" data-rawwidth="353" data-rawheight="302" class="content_image" width="353"/>
根据配置和部署的不同，业务高峰时可以一个机群（zone）、两个机群（zone）或者三个机群（zone）提供读写服务。OceanBase的轮转合并就是对每个机群（zone）轮转地进行每日合并，在对一个机群（zone）进行每日合并之前，先把该机群（zone）上的业务读写流量切换到另外的一个或两个机群（zone），然后对该机群（zone）进行全速的每日合并。因此在每日合并期间，合并进行中的机群（zone）没有业务流量，仅仅接收事务日志并且参与Paxos投票，业务访问OceanBase的事务响应时间完全不受每日合并的影响，仅仅是OceanBase的总吞吐量有所下降：如果先前是三个机群（zone）都提供服务则总吞吐量下降1/3，如果先前只有一个或两个机群（zone）提供服务则总吞吐量没有变化。轮转合并使得OceanBase对SSD十分友好，避免了大量随机写盘对SSD寿命的影响，因此OceanBase可以使用相对廉价的“读密集型”SSD来代替传统数据库使用的相对昂贵的“读写型”SSD，而不影响性能。此外由于轮转合并对服务器的CPU使用、硬盘IO使用以及耗时长短都不敏感（高峰期的传统数据库在刷脏页的同时还要优先保证业务访问的吞吐量和事务响应时间，刷脏页的CPU及IO资源都非常受限），因此OceanBase在每日合并时可以采用更加高效的压缩或者编码算法（比如压缩或编码速度略慢，但压缩率较高、解压缩很快的算法），从而进一步降低存储成本并提升性能。

这里需要澄清的一点是OceanBase根本就不是什么nosql数据库。OB将会100%兼容MySQL，所以OB就是纯纯的关系型（SQL)数据库，而且是纯纯的分布式关系型(SQL)数据库。这里就不跟nosql数据库做对比了，直接对比MySQL吧。比MySQL强的几点
1. OB的redolog是使用分布式一致性算法paxos实现的。所以在CAP理论中，虽然OB使用的是强一致模型，但是OB能在一定网络分区的情况下做到高可用（通俗点讲就是多余半数机器还活着的时候就能干活）。官方的MySQL目前做不到这一点
2. OB的存储结构使用的是两级的LSM-tree。其中内存中的C0 Btree叶节点不需要和磁盘上的btree一样大小，所以能做得比较小，对cpu的cache比较友好，并且不会有写入放大的问题。使得OB的写性能有极大的提升。同时磁盘上的C1 tree不是一个传统意义上的btree（btree未经压缩可能浪费一半空间）。空间利用率大大提高。简单来说就是速度快，省成本。这里说的比较粗略，想详细理解自己去看LSM-tree的论文。
3. 数据库自动分片功能（支持hash/range，一级二级等等分片方式），提供独立的proxy路由写入查询等操作到对应的分片。这意味着数据量再大也不需要手动分库分表了。并且分片能在线的在各个server之间迁移，解决热点问题（资源分配不均的问题，做到弹性加机器和减机器）。每个分片（确切的说是被选为主的分片）都支持读写，做到多点写入（高吞吐量，性能可线性扩展）。
4. 数据库内部实现的无阻塞的两阶段提交（跨机事务）。参见论文Consensus on Transaction Commit 
5. 数据库原生的多租户支持。能直接隔离租户之间的cpu，mem，io等资源。
6. 基于代价的SQL查询优化和改写功能，对于复杂的分析型SQL做得比MySQL好（目前比Oracle差，正在努力追赶中）。支持各种类型的join算法（nestloop, merge, hash），优化器会自动选择最优的join类型。支持类似Oracle的SPM功能，用户能很轻松自如的管理查询计划。7. 自动化的集群管理，包括机器上下线，自动下故障盘等等。总之OB的设计理念就是只要是数据库需要解决的问题就不让用户操心。

https://blog.csdn.net/michaelyang_yz/article/details/50821721
Oracle SPM（SQL Plan Management）介绍及演示SQL

## OceanBase 综合笔记（截至 2026-08）

### 定位、版本与适用边界

OceanBase 是原生分布式关系型数据库，提供 MySQL 兼容模式和 Oracle 兼容模式。它的核心目标是把分片、多副本一致性、跨分片事务、故障恢复和租户资源隔离收进数据库内核，减少应用层手工分库分表与中间件路由的复杂度。它不是 NoSQL，也不是“把 MySQL 多实例拼起来”。

截至 2026-08-12，官方 V4.3.5 文档将该版本定位为面向分析处理（AP）的首个 LTS 版本；其在 V4.3.4 基础上强化了嵌套物化视图、全文/向量索引、ORC 外表、Parquet/ORC 导出和优化器能力。生产选择仍应遵循部署渠道的支持矩阵与补丁版本，不能只看大版本号；例如官方发布说明明确给出 V4.3.5 BP1 仅支持从 V4.3.x 升级，不能由 V4.2.x 或更早版本直接升级。

| 工作负载 | 适配性 | 设计重点 |
| --- | --- | --- |
| 高并发交易、账户、订单、支付状态 | 高 | 主键/分区设计、事务范围、热点行与跨 LS 事务比例。 |
| 多租户 SaaS、资源整合 | 高 | tenant、resource unit、resource pool、配额和隔离压测。 |
| 复杂 Oracle 存量系统迁移 | 可行但需评估 | 逐项验证 SQL、PL、对象、驱动和运维语义，不能承诺“100% 无改造”。 |
| 实时分析/HTAP | 中高 | 区分交易与分析资源；大扫描、宽表 Join 要单独压测。 |
| PB 级离线数仓或搜索召回主引擎 | 视场景而定 | OLAP、数据湖和搜索专用系统的成本/生态可能更合适。 |
| 跨数据库、消息、支付渠道的全局原子事务 | 不直接解决 | OceanBase 保证库内事务；外部系统仍需 outbox、幂等、对账与补偿。 |

官方入口：

- 数据库文档：https://www.oceanbase.com/docs
- V4.3.5 新特性：https://en.oceanbase.com/docs/common-oceanbase-database-10000000002013391
- V4.3.5 CE 发布说明：https://en.oceanbase.com/docs/common-oceanbase-database-10000000003450993
- 源码：https://github.com/oceanbase/oceanbase

### 从旧版“每日合并”到 V4 的核心对象

旧笔记中“基线数据 + 内存增量 + 合并”的描述说明了 OceanBase 的 LSM 存储思路：增量写入 MemTable，持久基线为 SSTable，redo/commit log 用于恢复和一致性。这个理解仍有价值，但不要把早期材料中的“每日合并”当成现代版本固定每天、全库执行一次的用户可见语义。实际运维应关注 major compaction、转储/合并任务、MemStore、水位、I/O 和热点，而不是照搬旧文章的时间表。

V4 的关键变化是以 **LS（Log Stream，日志流）** 而不是单个分区作为事务提交和复制的基本单元。Tablet 是表或索引数据的分片承载对象；一个 LS 可包含多个 Tablet，同时保存对应 redo log 和事务管理结构。单 LS 写事务由该 LS 内部原子提交；跨 LS 事务由优化的两阶段提交协调。LS 的副本通过 Paxos 同步日志，以多数派持久化来提供强一致和副本容灾。

```text
应用 / JDBC / MySQL Client / Oracle Client
                 |
                 v
           ODP / OBProxy（可选：连接复用、路由、故障切换）
                 |
                 v
    OceanBase Cluster: RootService + 多个 OBServer
                 |
        tenant -> unit -> LS -> tablet -> MemTable / SSTable
                 |              |
                 |              +-- Paxos 多副本日志复制
                 +-- CPU、内存、磁盘 I/O、连接等资源隔离
```

| 对象 | 主要职责 | 容易混淆之处 |
| --- | --- | --- |
| Cluster | 多个 OBServer 与管理服务组成的集群 | 不是一个业务库；可承载多个 tenant。 |
| Tenant | 对用户呈现的逻辑数据库实例和资源隔离边界 | tenant 不只是 schema，也有资源、副本和生命周期。 |
| Unit / Resource Pool | 将 CPU、内存等资源按 zone 分配给 tenant | 容量规划应先看 unit，不应只按库表数估算。 |
| LS | 日志复制和事务提交参与者 | V4 中比“分区就是提交单元”的旧心智模型更准确。 |
| Tablet | 表/索引的物理数据分片 | 不是 MySQL 的分区同义词；分区、Tablet、LS 处于不同层次。 |
| Zone / Locality / Primary Zone | 副本地理分布、优先服务位置 | 需要与机房故障域和读写延迟一起设计。 |

强一致 DML 和强一致读在 leader 上执行；leader 把 redo log 按 Paxos 发给 follower，多数副本持久化后提交。三副本跨三个故障域通常可容忍一个副本或一个 zone 故障，但前提是剩余多数可通信、容量足够且 locality 配置正确。不要把“有三台机器”直接等同于实现了异地容灾，也不要把“Paxos”误解为在网络分区下两边都能继续强一致写入。

官方参考：

- 总体架构：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001166402
- 副本与 LS：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001971061
- 数据分布：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001714585

### 多租户与容量规划

OceanBase 从 V4.0 起有三类 tenant：`sys` tenant 管理集群级公共任务，user tenant 承载业务，meta tenant 管理相应 user tenant 的私有元数据，如 location、replica、LS、备份恢复和 major compaction 状态。业务表和业务 SQL 应部署在 user tenant；不要把 `sys` tenant 当成普通业务库。

多租户的价值是可控隔离，而非“自动无限弹性”。tenant 的 locality、primary zone、resource pool、unit 数量决定了副本位置和计算资源。扩容、缩容、迁移或故障恢复还会触发副本迁移、LS 均衡及缓存预热。生产容量评估至少包含：

1. 峰值 TPS/QPS、P95/P99 延迟、连接数和事务平均/最大时长。
2. 行大小、索引倍数、复制倍数、LSM 写放大、日志、备份和临时空间。
3. 热点租户、热点主键、热点分区和跨 LS/跨 zone 事务的比例。
4. 正常和单 zone 故障时的 CPU、内存、磁盘、网络余量，不能只按三副本后平均除三。
5. 大查询、批处理、备份、schema 变更和 compaction 与在线交易并行时的资源上限。

租户隔离不替代连接池和 SQL 治理。应用仍需设置合理的连接池上限、超时、重试和熔断；DBA 仍需限制慢 SQL、超大事务和无界扫描。出现单租户高延迟时，先确认是 tenant 配额、排队、热点、跨分区访问还是全局资源不足，不能只增加机器。

### 事务、一致性与分布式代价

OceanBase 用 MVCC 提供多版本读，并通过 GTS（Global Timestamp Service）等机制协调全局时间与一致性快照。MySQL 模式支持 Read Committed 和 Repeatable Read，默认是 Read Committed；文档还说明启用 Serializable 需要先启用 GTS，且 `sys` tenant 不支持 Serializable。隔离级别、锁等待、死锁处理、自动重试和驱动行为必须在真实业务上验证，不能因为“兼容 MySQL”就假定与某个 MySQL 小版本完全一样。

```text
单 LS 事务：DML -> redo log -> Paxos 多数派持久化 -> 原子提交
跨 LS 事务：多个 LS 参与 -> 优化 2PC 协调 -> 全部提交或全部回滚
跨系统流程：OceanBase 提交 + MQ/HTTP/其他 DB -> 仍需业务幂等、outbox、对账、补偿
```

跨 LS 事务不是错误，但成本通常高于单 LS 事务：更多协调、日志与网络往返，更容易放大长事务、锁冲突和故障重试的影响。建模与访问应尽量让经常一起更新的数据按业务实体、租户或账户局部化；同时避免为了“零跨分片”制造严重热点。正确做法是量化真实比例、延迟和冲突，再取平衡。

| 现象 | 优先排查 | 常见处理 |
| --- | --- | --- |
| 提交延迟波动 | Paxos 副本网络、慢盘、跨 zone、日志盘、长事务 | 修复慢节点/网络，缩短事务，避免跨地域同步写。 |
| 死锁或锁等增多 | 热点行、更新顺序不一致、缺索引、批量事务 | 固定加锁顺序，缩小批次，给重试加入退避和幂等键。 |
| 读到旧数据 | 读一致性策略、读路由、事务快照 | 明确读己之写/强一致读需求，不能笼统配置“读副本”。 |
| 事务回滚很慢 | 超大事务、历史版本、长快照、跨 LS | 拆分业务批次，治理长事务，检查事务状态视图。 |

金融正确性不来自某个数据库产品名称，而是“库内原子性 + 唯一业务键 + 状态机 + 可重试接口 + 账务对账 + 人工/自动补偿”的完整链路。Paxos 解决副本共识和复制，不自动替应用解决重复扣款、消息重复投递或第三方超时不确定性。

官方参考：

- 事务结构：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001230830
- 隔离级别：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001974190
- 多版本读一致性：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001105868

### 兼容模式、建模和 SQL 性能

MySQL 模式和 Oracle 模式是 tenant 创建时的兼容模式选择，目标是降低迁移成本而不是抹平所有语义差异。迁移前应将功能分为 SQL 语法、数据类型/字符集/排序规则、事务与锁、索引/分区、存储过程/触发器/包、驱动与工具、运维脚本七类做自动化回归。旧的“完全不兼容”与“100% 完全兼容”都是不负责任的绝对表述，结论必须以目标版本、兼容模式和实际对象清单为准。

表与索引设计仍遵循关系数据库常识：

| 目标 | 建议 | 反模式 |
| --- | --- | --- |
| 点查与更新 | 用稳定且均匀的主键，热点业务引入可控打散或分区策略 | 单递增热点或把所有业务集中在少数 key。 |
| 时间数据 | 基于生命周期、查询范围和清理策略做 range 分区 | 只因“分布式”就大量细碎分区。 |
| 二级索引 | 从高频谓词、选择性、回表与写放大出发 | 迁移时照抄全部历史索引，导致写入/合并成本上升。 |
| 跨分区关联 | 用业务局部性降低跨 LS 访问，验证计划 | 假定数据库会自动让任意大表 Join 线性扩展。 |
| SQL 稳定性 | 收集统计信息，使用 `EXPLAIN` 和 SPM 管理关键计划 | 只看单次执行时间，忽略数据分布变化后的计划退化。 |

分区用于数据生命周期、裁剪和并行度，不等于把 MySQL 的手工分库分表原样搬进 OceanBase。应先定义数据访问路径和故障域，再决定 range/list/hash/key 分区、分区数和索引布局。过多小分区会增加元数据、调度和运维成本；分区过少又会限制并行性并形成热点。

旧笔记中所列 `COMPRESSION`、`REPLICA_NUM`、`BLOCK_SIZE`、`TABLET_SIZE`、`PCTFREE`、`LOB_INROW_THRESHOLD`、`LOCAL` 等是 OceanBase 建表/索引或特定兼容场景的扩展属性，不能原样投给原生 MySQL。迁移到 MySQL 时也不应机械“全部删除后即等价”：副本数、数据分布、压缩、LOB、分区索引和填充率背后的容量/性能目标需要分别映射到 MySQL 的实例拓扑、InnoDB、分区、备份和运维方案中。

### OLTP、HTAP 与 V4.3.5 的分析能力

OceanBase 的主战场是强一致分布式 OLTP，也提供面向 HTAP/AP 的能力。V4.3.5 将分析处理作为 LTS 重点，新增或增强嵌套物化视图、全文和向量索引、外表读取 ORC、`SELECT INTO OUTFILE` 输出 Parquet/ORC，以及 SPM、基数估算、递归 CTE 和范围提取的优化。这意味着可以将部分实时分析放在同一产品内，但不表示任何数仓/搜索工作负载都应迁入。

| 需求 | 可考虑的 OceanBase 能力 | 仍需验证 |
| --- | --- | --- |
| 实时汇总报表 | 物化视图、索引、分区裁剪 | 刷新开销、写入影响、查询改写和高并发。 |
| 湖/文件数据交换 | 外表、Parquet/ORC 导入导出 | 文件大小、小文件、对象存储吞吐与权限。 |
| 文本/语义检索 | 全文索引、向量索引 | 索引状态、召回/排序、更新成本和 Beta/版本限制。 |
| 复杂分析 | 优化器、并行执行、SPM | 宽表 Join、数据倾斜、内存、临时空间与多租户干扰。 |

分析负载和交易负载共集群时，要按 tenant/资源隔离，并在峰值交易期间压测备份、导入、物化视图刷新和 compaction。OLAP 专用数据库、数据湖引擎和搜索引擎在吞吐、生态或成本上可能更合适；选型应以 P95/P99、并发、数据规模、运维复杂度、RPO/RTO 和总成本比较，而非单一跑分。

### 高可用、备份、恢复与迁移

高可用分三个层次：副本多数派保证单 LS 可用性，zone/locality 处理机房故障域，备份与归档日志处理误删、逻辑损坏和多副本共同损坏。三副本复制不是备份，`DROP`、错误 `UPDATE`、权限误操作和应用 Bug 会被一致地复制到所有副本。

建议采用“日志归档 + 定期数据备份 + 恢复演练”。官方恢复要求目标 OceanBase 版本与备份源相同或更高；恢复时需要数据备份路径和日志归档路径。可将恢复的 tenant 先作为 standby，再显式激活为 primary。归档与备份可使用 NFS、OSS、COS 或 S3 等介质，具体认证、带宽、加密和保留策略要按部署版本验证。

```text
RPO/RTO 设计示例
在线多副本：应对少数节点/zone 故障，不替代备份
日志归档：缩短可恢复的数据时间窗口
数据备份：提供恢复基线
恢复演练：验证权限、对象存储、版本、耗时和业务校验
OMS/双写/灰度：用于迁移和切换，不自动证明数据正确
```

OMS（OceanBase Migration Service）用于异构/同构的数据迁移、实时同步和增量订阅，可覆盖 MySQL、Kafka 与 OceanBase 等组合。它能降低迁移风险，但不能替代迁移验收：必须核对 DDL 转换、初始全量与增量衔接点、无唯一非空键表、DDL 演进、双写冲突、延迟、水位、回切和业务对账。对于核心表，至少按行数、主键 checksum、金额/状态聚合、抽样明细和双向差异持续验证。

官方参考：

- 备份恢复：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001231356
- 创建备租户：https://en.oceanbase.com/docs/common-oceanbase-database-10000000001231004
- OMS：https://en.oceanbase.com/docs/oms-en

### 运维、POC 与面试要点

运维观测要覆盖集群、tenant、LS、SQL 和数据保护：OBServer/zone 存活与领导者分布、unit 资源、CPU/内存/磁盘/网络、Paxos 日志与副本延迟、事务与锁等待、慢 SQL/执行计划、compaction/转储、备份归档、OMS 水位和恢复任务。既要报警，也要建立容量趋势和变更后的基线对比。

POC 不应只运行单表 TPS。至少验证：

1. 单 LS 和跨 LS 的读写延迟、失败重试、死锁与热点主键。
2. 正常、单 OBServer 故障、单 zone 故障以及网络抖动下的可用性和数据正确性。
3. tenant 隔离下交易、批处理、备份/归档和 compaction 并发时的 P95/P99。
4. 真实 DDL、索引、存储过程/触发器、字符集、时间类型、事务隔离和 JDBC/ORM 行为。
5. 全量迁移、增量同步、灰度切换、回切，以及持续对账。
6. 从备份恢复到新 tenant 的真实 RTO 和恢复后业务校验，而非只看备份任务成功。

常见面试回答框架：

- **OceanBase 如何做到高可用？** 数据按 LS 多副本部署，redo log 经 Paxos 多数派提交；再以 zone/locality 规划故障域，备份/归档处理逻辑损坏。
- **为何跨分布式事务有代价？** 多 LS 需要协调和 2PC，增加网络、日志和故障处理成本；通过数据局部性降低比例，但不能因此制造热点。
- **tenant 与 schema 的区别？** schema 是逻辑命名空间；tenant 还是资源、副本、权限、备份和生命周期的隔离边界。
- **OceanBase 能取代 MySQL/Oracle 吗？** 取决于目标版本、兼容模式、对象与运行负载；先做兼容回归和 POC，而不是凭品牌或协议下结论。
- **Paxos 能否解决端到端一致性？** 只能解决副本共识/复制；消息、第三方支付和跨库流程还需幂等、outbox、对账和补偿。

学习顺序：先阅读 [数据库综合笔记](../db/db.md)、[Paxos](paxos.md) 和 [X-Engine](X-Engine.md) 建立事务与存储背景；再用 OBClient/ODP 建立三副本测试集群，创建 tenant、分区表和索引；接着观察 LS、事务、执行计划、备份恢复与 OMS；最后以一个订单或账务迁移案例完成建模、压测、故障演练和数据对账。能够写清“数据如何分布、事务如何提交、故障如何恢复、迁移如何验证”，才算掌握 OceanBase，而不是只记住参数名。
