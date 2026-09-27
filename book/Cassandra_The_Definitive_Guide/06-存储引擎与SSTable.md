# 06 存储引擎与 SSTable（原书第 6 章"架构·存储层"域 ✅ 锚点，小节 ⚠️ 推定）

> 精读重构（非原书文本）。本章讲 Cassandra 的磁盘/内存引擎：LSM 树在 2.x 的实现形态。
> 未实测 ⚠️；管理员向同题：#89 册 [05-Cassandra架构](../Expert_Apache_Cassandra_Administration/05-Cassandra架构.md)。

## 6.1 题纲

1. 四大件：CommitLog / Memtable / SSTable / Key Cache(+Row Cache)
2. 写路径：commitlog 追加 → memtable（跳表）→ 阈值 flush → SSTable 不可变段
3. 读路径：key cache→bloom filter→分区摘要→SSTable 索引→（memtable 合并）
4. 墓碑与影子：删除语义、超卖读取、tombstone_warn_threshold 一族
5. 压实家族：STCS/LCS/TWCS 的行为差异与选型决策树（书内判词 ⚠️）
6. 缓存家族：key cache（分区索引常驻内存）、row cache（2.1 后不推荐 ⚠️）、counter cache
7. 压缩与加密：SSTable 块压缩（lz4/deflate/snappy）、静态加密
8. 2.x 格式考古：large text/legacy entry、索引文件（_index/_summary/_Statistics）

## 6.2 写路径：一切从"顺序追加"开始

```
Client(CQL) → Coordinator 节点
  1) 按分区键哈希定位副本集合（07 章放置）
  2) 本地：写 commitlog（fsync 策略 periodic/group ⚠️）→ 写 memtable（跳表，分区内存树）
  3) 远程副本：异步写其 commitlog+memtable，按 CL 等待应答（08 章）
memtable 满（默认 ~内存 1/3 量级 ⚠️）→ 冻结 → flush 成新 SSTable（按 key 有序、不可变）
```

关键推论（书内反复出现的心智）：**写 Cassandra 永远是在写日志，读才需要拼装**。
所以 INSERT 快、UPDATE 快（=再插一条带时间戳的新版本）、DELETE 也快（=立墓碑）、
而"最后一条记录"类查询可能很慢（跨 SSTable 归并）。与 #89 册的分工：它从"压实风暴/限流
参数"切入，本章从"为什么会产生风暴"切入。

概念源对照：LSM 通论（levelized vs size-tiered、读放大三角）在
[../数据库系统概念6/00-总览与阅读地图.md](../数据库系统概念6/00-总览与阅读地图.md) 的存储章谱系与
[../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)；
本册的独有贡献是"2.x 参数名与文件族"的忠实转述。

## 6.3 SSTable 解剖（2.x ⚠️）

一个 SSTable = 一组文件（`nb-big-Data.db` 等后缀族）：

- **Data.db**：按分区键排序的记录序列，内部是"聚簇列有序的最小堆式布局"（large entry 格式）。
- **Index.db**：稀疏索引（每 N 采样一个键→Data 偏移），二分查找的入口。
- **Filter.db**：**布隆过滤器**，按分区键回答"这表里可能有没有它"——省掉绝大多数随机盘读，
  fp 率与内存占用的权衡（`bloom_filter_fp_chance`）是书内调优第一课。
- **Statistics/Summary/CompressionInfo**：表统计、分区摘要、压缩块映射 ⚠️ 文件名族按版本变。

读一个分区的漏斗：key cache（Index.db 采样热区常驻）→ bloom → summary → 分区内跳索引 →
Data.db 顺序读解压块。**每一层都是"以内存换盘 IO"的连续赌注**，参数在 10 章。

## 6.4 压实三兄弟与选型（书内决策树 ⚠️）

| 策略 | 行为 | 书中场景判词 |
|---|---|---|
| STCS | 相似大小段分组归并（min/max threshold） | 通用默认；写放大约 log(数据量)，空间放大高 |
| LCS | level 内小段、级间归并 | 读优化、空间敏感；2.1 起支持窗口 ⚠️，盘 IO 尖峰 |
| TWCS | 按时间窗分段，窗内 STCS、跨窗不归并 | 时序/TTL 数据（05 章搭档）；避免"老数据被反复重压" |

压实=把"写的便宜"分期偿还：吞吐（throughput）限流参数、并行数、`compaction_history`
统计都归运维侧（#89 册 09/11 章的深水区）。2026 判词见文末（UCS 让这页决策树整体退役 ✅）。

## 6.5 墓碑、修复窗口与 GC

- DELETE 与 TTL 过期值都以墓碑/过期标记存在于 SSTable，压实只是"在 gc_grace_seconds
  之后才允许丢弃"。
- gc_grace 的设计动机（书内叙事 ⚠️）：给反熵修复留出"还能看到删除"的窗口——**把
  gc_grace 调小去腾空间=制造"复活死数据"事故**，这是本章给读者的最强警告。
- 读放大告警族：`tombstone_warn_threshold`/`abort_threshold`（2.1+ ⚠️）在查询返回过多
  墓碑时抛错——把"性能病"变成"显式异常"的里程碑设计。
- 概念回环：反熵（merkle tree 修复）与读修复的机制位置在 07/08 章，理论端在
  [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)（#89 册 05 章含 🔧 merkle 类比演示，可越册参读）。

## 6.6 缓存家族与内存图景

- **Key cache**：分区索引采样常驻（`keys_cache_size_in_mb`，默认取堆的一档 ⚠️）——
  对"按分区点查"收益最大；重启可从 saved_caches 预热（02 章目录挂点）。
- **Row cache**：整行常驻，2.x 中被官方口径劝退（命中率低+堆压力+大分区毒害 ⚠️），
  3.x 后整体移除 ⚠️——本章保留它是为了读懂书内旧参数。
- **Counter cache/Commitlog 内存**：计数器合并的临时账本、group commit 缓冲 ⚠️。
- 堆内 vs 堆外：2.x 的 mmap 片段（`mmap` 读 SSTable/Index Summary）与 5.0 trie 结构
  的堆外化趋势，见演进节。

## 6.7 本章在全目录中的挂点

- 参数落点 → [10-配置与集群运维](10-配置与集群运维.md)；排障指标 → [11-监控排障与性能调优](11-监控排障与性能调优.md)
- 集群侧的"谁持有哪个分区" → [07-集群架构与Gossip](07-集群架构与Gossip.md)
- 读路径的一致性动作（digest/修复）→ [08-一致性与读写路径](08-一致性与读写路径.md)
- 运维纵深 → [../Expert_Apache_Cassandra_Administration/11-性能调优.md](../Expert_Apache_Cassandra_Administration/11-性能调优.md)

## 核心概念速览（中英对照）

- **CommitLog** — Commit log：全集群级顺序预写日志，group commit，重放恢复的根据。
- **Memtable** — Memtable：跳表内存结构，按分区组织、冻结后 flush 成 SSTable。
- **SSTable** — Sorted String Table：不可变、按键有序的段文件族，LSM 的磁盘单元。
- **Bloom filter** — Bloom filter：分区键存在性预检，fp_chance 调内存/误判权衡。
- **Key cache** — Key cache：Index.db 采样热区常驻内存，加速分区定位。
- **Row cache** — Row cache：行级缓存，2.x 起不鼓励、后被移除 ⚠️。
- **Flush** — Flush：memtable 冻结落盘动作，触发压实压力的源头节拍。
- **Compaction** — Compaction：段归并，回收墓碑/过期、降读放大、还写债。
- **STCS/LCS/TWCS** — 压实三策略：size-tiered / leveled / time-window 各自偿还曲线。
- **Tombstone** — Tombstone：删除的时间戳遮蔽标记，GC 受 gc_grace_seconds 支配。
- **gc_grace_seconds** — GC grace：墓碑可丢弃前的修复宽限期，短=数据复活风险。
- **Write amplification** — Write amp：一逻辑写引发的多轮压实字节，LSM 的隐账单。
- **Chunk compression** — 块压缩：SSTable 内 lz4/deflate/snappy 块，读侧解压换空间。
- **sstabletools** — SSTable 工具族：`sstableverify/sstablescrub` 等离线检查器。

## 最新演进与工业实践

（均本会话实抓 ✅，注明者除外；引擎不实测纪律不变）

- **Memtable/SSTable 结构换代**：5.0 **Trie memtable（CEP-19）+ Trie 索引 SSTable（CEP-25）**
  替换跳表+稀疏索引，堆外化+读路径更稳（源：
  https://cassandra.apache.org/doc/latest/cassandra/new/index.html 与页内 CEP 链接）。
- **压实退役决策树**：5.0 **Unified Compaction Strategy（UCP/UCS，CEP-26）GA**——三选一
  变成"声明目标+自动调参"，本章 6.4 表转为历史语义 ⚠️（对 4.x 存量仍适用）。
- **行缓存终局**：3.x 移除 row cache 的口径延续；key cache 被 trie 结构吸收其职能 ⚠️。
- **SSTable 格式对升级的暴政**：2.x→3.x→4.x 格式逐级迁移（旧格式不可被新版直读），
  书内"原地滚升 2.1→2.2"的流程在 2026 只适用于"4.x→5.0"的当代类比 ⚠️——升级演练请查
  官方 upgrade 文档与 #89 册 08 章工法。
- **工业实践**：磁盘栈 NVMe+多数据目录（JBOD）为标准形态；块压缩默认 lz4 延续；
  透明磁盘加密与云侧加密并存 ⚠️。度量与故障谱的当代版在 11 章演进节与 #89 册 10 章。
