# 02 · 集群架构与 vBucket 映射（VBMap）

> 主题域：Couchbase 的集中式集群映射——把「分片 + 迁移 + 故障转移」三件事统一成「改一张表」。
> 章号/章名 ⚠️ 精读重构；2026 事实全部 ✅ 到 docs.couchbase.com。

## 1. 为什么需要一个中间层

朴素做法（memcached 客户端分片）：`node = hash(key) % N`。节点数一变，**几乎所有键都要搬家**。

🔧 本机实测（E1，`exp.py`，SQLite + Python，**非 Couchbase 行为**）：

- 100 000 个键（`crc32(key) % 1024`），3 节点 → 4 节点：
  - 朴素对节点数取模：迁移 **74 772 键（74.77%）**。
  - 加一层 vBucket 间接映射 + 最小挪移：只需迁移 **256 / 1024 个 vBucket**，折算键迁移 **≈25.0%**。
- 这就是 VBMap 存在的全部理由：**数据移动的单位是 vBucket，而不是键**。

E1b：把 10 万条路由塞进 SQLite 表 `routes(key, vb, node)`，载入 0.21s；把一个 vBucket 改属主的 `UPDATE` 只花 **0.006s（影响 740 行）**——「改路由」是元数据级操作，真正的数据搬迁是后续、可限速、可中断的后台任务。

## 2. 官方口径（✅）

来源：https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/vbuckets.html

- 「Couchbase Server breaks the data in buckets into smaller units called **vBuckets** … Some people refer to vBuckets as shards.」
- 「When it creates the bucket, Couchbase Server breaks it into **a fixed number of vBuckets. Once created, the number of vBuckets in a bucket does not change.**」
- 数量取决于存储引擎：**Couchstore = 1024；Magma = 128 或 1024，且 8.0 EE 新桶默认 128**（https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/storage-engines.html ✅）。

🔧 E1 的另一半结论（128 vs 1024 的粒度代价，同脚本）：

| 配置 | 每 vBucket 平均键数 | 3 节点负载（10 万键） | 变异系数 |
|---|---|---|---|
| 1024 vBucket | 98 | 33279 / 33419 / 33302 | **0.002** |
| 128 vBucket | 781 | 33637 / 33707 / 32656 | **0.014** |

即：**桶数少 → 每次挪移的块大、均衡度粗**；官方给 Magma-128 的理由是内存配额（100MiB vs 1GiB），本实验给的是它在偏斜上的代价（约 7 倍变异系数）。

## 3. 集群映射的三种状态

概念上，一个 vBucket 在任意时刻处于：**active（某节点）/ replica（另一些节点）/ pending（再平衡中的新属主）**。

- 集群映射由**集群管理器（optervisor）**生成并下发给客户端；客户端因此知道「这个键该找谁」，不必让代理做全部转发。
- ✅ 页面：[Cluster Manager](https://docs.couchbase.com/server/current/learn/clusters-and-availability/cluster-manager.html)、[Connectivity](https://docs.couchbase.com/server/current/learn/clusters-and-availability/connectivity.html)（后者解释客户端如何拿到并使用映射）。
- 2014 基线（⚠️ 推定）：当时 `configChangeCallback` / `VbucketServerMap` 一类 API 直接暴露 VBMap 给 SDK；现代 SDK 把这层封成「请求路由器」，应用不再手写映射处理，但仍能从 `sdk-doctor` 之类的诊断里看到映射版本（✅ https://docs.couchbase.com/server/current/sdk/sdk-doctor.html）。

## 4. 副本、故障转移与再平衡

✅ [Replication architecture](https://docs.couchbase.com/server/current/learn/clusters-and-availability/replication-architecture.html)：桶可配 **最多 3 个副本**；节点不足时实际副本数会更少。

| 动作 | 语义 | 页面 |
|---|---|---|
| 再平衡 rebalance | 在集群仍在服务请求的前提下重分布数据/索引/事件/查询负载 | [rebalance](https://docs.couchbase.com/server/current/learn/clusters-and-availability/rebalance.html) ✅ |
| 计划内移除 | 先摘数据再下线 | [removal](https://docs.couchbase.com/server/current/learn/clusters-and-availability/removal.html) ✅ |
| 硬/优雅故障转移 | 节点已丢 vs 主动让节点退出并保数据 | [hard-failover](https://docs.couchbase.com/server/current/learn/clusters-and-availability/hard-failover.html) / [graceful-failover](https://docs.couchbase.com/server/current/learn/clusters-and-availability/graceful-failover.html) ✅ |
| 自动故障转移 | 按超时/容量阈值自动执行 | [automatic-failover](https://docs.couchbase.com/server/current/learn/clusters-and-availability/automatic-failover.html) ✅ |
| 副本恢复 | 短暂下线后的 delta 恢复 | [recovery](https://docs.couchbase.com/server/current/learn/clusters-and-availability/recovery.html) ✅ |
| 节点分组 | 机架/可用区感知（EE） | [groups](https://docs.couchbase.com/server/current/learn/clusters-and-availability/groups.html) ✅ |

8.0 新增（✅）：**非数据服务（index/n1ql/fts/cbas/eventing/backup）可在既有节点上动态增删并自动触发再平衡**；7.6 起再平衡支持**桶级优先级（Bucket Rank）**（见 rebalance 页 `Rebalance bucket rank` 段）。

## 5. 元数据、seqno 与「谁负责这个键」

- 每个 vBucket 有本地序号流（seqno），复制与 XDCR 都以它为进度凭据 → 观测口径见 ✅ [cbstats vbucket](https://docs.couchbase.com/server/current/cli/cbstats/cbstats-vbucket.html)、[cbstats-vbucket-details](https://docs.couchbase.com/server/current/cli/cbstats/cbstats-vbucket-details.html)。
- 元数据（键、CAS、seqno、expiry）常驻内存；条目被驱逐只丢 value，键仍在 → ✅ [metadata-management](https://docs.couchbase.com/server/current/learn/clusters-and-availability/metadata-management.html)。
- 🔧 类比（E2c，第 3 章展开）：SQLite 里 30000 键，逻辑过期判定 0.9ms，但**宽限期内的物理清理实删 0 行**——「逻辑不可见 ≠ 元数据消失」这一条在两边同构。

## 6. 与宽列/散列谱系的分野

| 维度 | Couchbase（VBMap） | Cassandra（token ring） | 依据 |
|---|---|---|---|
| 映射产生者 | 集中式集群管理器 | 去中心化 gossip + 一致性哈希 | ✅ [../Cassandra_The_Definitive_Guide/07-集群架构与Gossip.md](../Cassandra_The_Definitive_Guide/07-集群架构与Gossip.md) |
| 分片可数性 | 固定 128/1024，创建后不可变 | token 区间，虚拟节点数可调 | ✅ vbuckets 页 |
| 客户端角色 | 拿映射直连属主 | 协调节点可转发任意请求 | DDIA 分区章 |
| 迁移粒度 | 一个 vBucket（可排队/限速） | 一个 token range | — |

原理层对位：[../设计数据密集型应用/06-分区.md](../设计数据密集型应用/06-分区.md)（键范围 vs 散列分区，以及「再平衡不应停摆」的一般要求）；复制与故障检测的一般讨论在 [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)、[../设计数据密集型应用/08-分布式系统的麻烦.md](../设计数据密集型应用/08-分布式系统的麻烦.md)。Redis 侧的集中式槽位（16384 slot）是同一思想的另一实现，见 [../Learning_Redis/06-复制哨兵与集群.md](../Learning_Redis/06-复制哨兵与集群.md)。

## 7. 设计后果：键与桶的两条硬约束

1. **同桶同前缀的键会散到不同 vBucket** → 想「一批键一起迁走」是幻想；想「一次 range 扫描」得靠视图/索引而不是键序（见 [04-视图与二级索引时代.md](04-视图与二级索引时代.md)）。
2. **副本数决定可用性/写放大/持久性档位三角** → 与 03 章的 durability、07 章的 XDCR 串成一条线。
3. 🔧 E1 的推论：`hash(key) % 节点数` 这种客户端分片在扩缩容时的迁移比例是本机实测的 **74.77%**，任何「我们自己搓过一层 memcached 分片」的团队都该看一次这行数字。

## 8. 与其他章的接缝

- 键怎么命名会改变映射行为吗？——不会（散列打散），但会改变**索引与迁移的可运维性** → [06-数据建模与键空间设计.md](06-数据建模与键空间设计.md)
- 再平衡期间读写会不会脏？→ [03-键值操作与并发控制.md](03-键值操作与并发控制.md)
- 跨数据中心时的第二层映射 → [07-跨数据中心复制与多活.md](07-跨数据中心复制与多活.md)
- 桶配额与内存压力 → [09-管理接口内存与运维.md](09-管理接口内存与运维.md)

## 核心概念速览（中英对照）

- **vBucket** — virtual bucket：桶内固定数量的数据切片，是分布与复制的最小单位；Couchstore 1024、Magma 128/1024。
- **集群映射** — Cluster Map / VBMap：vBucket→节点（含副本、pending）的总表，由集群管理器下发。
- **属主/副本/pending** — active / replica / pending：同一 vBucket 的三种角色，再平衡期间三者并存。
- **再平衡** — Rebalance：把映射重算并把数据搬到新属主的过程，在线进行。
- **桶优先级** — Bucket Rank：7.6+ 再平衡时按桶排序处理迁移先后。
- **故障转移** — Failover（hard/graceful/auto）：把不可用节点上的副本提升为主。
- **Delta 恢复** — Delta Recovery：节点短时下线后只补差异的回队方式。
- **节点分组** — Server Groups：让副本跨机架/可用区摆放的 EE 特性。
- **seqno** — sequence number：vBucket 内的写序号，复制进度与故障恢复的时钟。
- **元数据驻留** — Metadata Residency：驱逐 value 仍保留键与元数据的机制。
- **写放大** — Write Amplification：副本数与持久化档位共同造成的额外写。
- **一致性哈希** — Consistent Hashing：Cassandra 路线，与 VBMap 相对照的去中心化方案。
- **爆炸半径** — Blast Radius：单节点/单桶故障波及的范围，由映射与副本共同决定。
- **拓扑感知客户端** — Topology-aware Client：直连属主节点、能处理映射变更的 SDK。
- **分片** — Shard：官方文档对 vBucket 的通俗别名。

## 最新演进与工业实践

1. **默认粒度变化是本次最大的坑**：8.0 EE 新桶默认 **Magma + 128 vBucket**（官方明确标注 "This is a default behavior change"，并要求升级前检查部署脚本）→ https://docs.couchbase.com/server/current/introduction/whats-new.html ✅
2. **vBucket 数不可变的约束仍在**（✅ vbuckets 页原句），所以「按数据量预估桶数」在 Magma 时代退化为「选 128 还是 1024」的二选一，权衡点=内存配额 vs 均衡粒度（🔧 E1 给了量化直觉）。
3. **Memcached 桶移除**：8.0 起集群里若仍有 Memcached 桶，升级会被卡住 → ✅ whats-new 页。
4. **服务角色可动态调整**：不再需要「为了加一个查询节点而换机器」→ ✅ whats-new 页（`index/n1ql/fts/cbas/eventing/backup` 可增删并自动再平衡）。
5. **可观测性升级**：从 2014 的 REST 统计页，到今天按服务分类的指标手册与 `cbstats` 的 vbucket/scope/collection 维度（✅ [metrics-reference](https://docs.couchbase.com/server/current/metrics-reference/metrics-reference.html)、✅ [cbstats-collections](https://docs.couchbase.com/server/current/cli/cbstats/cbstats-collections.html)）。
6. **云上的心智变化**：Capella 里集群即「Database」，扩缩容/再平衡是控制台动作（✅ https://docs.couchbase.com/cloud/clusters/create-database.html），2014 书里手搓 REST 调 `rebalance` 的代码今天只用于自建集群。
7. **工业实践**：把「再平衡窗口」写进发布纪律——在线再平衡期间 CAS 冲突率与延迟都会上升（原理见 ✅ [connectivity](https://docs.couchbase.com/server/current/learn/clusters-and-availability/connectivity.html) 的重路由语义）；对多租户 SaaS，用 collection 而不是多桶做租户切分是当下官方教程口径（✅ [tutorials/buckets-scopes-and-collections](https://docs.couchbase.com/server/current/tutorials/buckets-scopes-and-collections.html)）。
8. **谱系阅读**：宽列侧对照 [../Cassandra_The_Definitive_Guide/08-一致性与读写路径.md](../Cassandra_The_Definitive_Guide/08-一致性与读写路径.md)；论文线（分区/复制/共识）入口 [../../db/db.md](../../db/db.md)；同主题原理 ✅ 版见 [../设计数据密集型应用/06-分区.md](../设计数据密集型应用/06-分区.md)。
