# 01 · Couchbase 定位与文档键值模型

> 主题域：为什么「内存优先的键值 + JSON 文档 + 磁盘持久化」是一个独立物种。
> 章号/章名为 ⚠️ 精读重构（原书目录未取证，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节）。

## 1. 一句话说清它的形状

Couchbase Server = **一个带复制与再平衡的、可持久化的、按 key 取值的分布式哈希表**，其 value 可以是任意二进制块，也可以是 JSON 文档；一旦 value 用 JSON，它就顺带长出了文档数据库的能力（二级索引、查询语言、全文与向量检索）。

- 2014 基线（⚠️ 推定当时口径）：bucket → key → document；`_id`/`_rev` 风格的元数据由服务器托管；「先当 KV 用，需要查询时再补视图」是官方推荐的入门路径（与官方文案「先连上集群、再存取信息、然后学习数据在集群里的工作流」一致 ✅ 文案见 00 第一节）。
- 2026 口径（✅）：官方把这一层叫 **Data Service** + **Document Data Model**，桶里再分 **scope / collection**，键的唯一性范围从「桶内」收窄到「collection 内」。

## 2. 数据分层：桶、键、值、元数据

| 层 | 2014（基线 ⚠️） | 2026（✅ 官方文档） |
|---|---|---|
| 容器 | bucket（内存配额 + 副本数 + 驱逐策略） | bucket 仍在，但内部是 `bucket → scope → collection` 三层；每集群至多 **1000 个 collection**（[scopes-and-collections](https://docs.couchbase.com/server/current/learn/data/scopes-and-collections.html)） |
| 键 | 桶内唯一，≤250 字节（⚠️ 当时口径） | 「Each key is unique **within its collection**, and values can be either binary or JSON.」（[learn/data/data](https://docs.couchbase.com/server/current/learn/data/data.html)） |
| 值 | JSON 或二进制；无 schema | 同左，JSON 按 RFC 8259；元数据（CAS/expiry/seqno）与**扩展属性 XATTR**分离存放（[extended-attributes-fundamentals](https://docs.couchbase.com/server/current/learn/data/extended-attributes-fundamentals.html)） |
| 索引 | View（MapReduce）+ FTS | GSI 二级索引 + View（**7.0 起弃用**）+ Search + 向量索引 |

关键点：**键是应用命名的产物，不是数据库生成的**。键空间设计因此成为 Couchbase 应用开发的第一号工程问题（见 [06-数据建模与键空间设计.md](06-数据建模与键空间设计.md)）。

## 3. 混合持久化：内存是什么、磁盘是什么

- 概念骨架（✅ 官方）：桶持有内存配额（quota），元数据常驻内存；value 是否驻留由**驱逐策略**决定；磁盘侧由存储引擎负责——今天有两个：**Couchstore 与 Magma**（[storage-engines](https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/storage-engines.html)）。
- 2014 基线的说法（⚠️ 推定）：「memory-optimized / disk-focused 两类桶」的划分方式；**2026 该表述已退役**，取而代之的是「Couchbase 桶（持久）/ Ephemeral 桶（纯内存）」+ 驱逐策略 `value only / full eviction / no eviction`（[buckets](https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/buckets.html) ✅）。
- 8.0 变化（✅）：**Memcached 桶已从产品中移除**，升级到 8.0 前必须把它换成 Ephemeral 桶；新默认存储引擎是 **Magma + 128 vBucket**（最小内存配额 100MiB，对比 1024-vBucket Magma 桶的 1GiB）。

## 4. 它不是什么：四张对位表

| 对照 | 表面相似 | 实质分歧 | 盘上深读 |
|---|---|---|---|
| Memcached/Redis | 都是内存优先 | Couchbase 有副本 + 再平衡 + 磁盘 + 视图/索引；Redis 的数据结构在服务端，Couchbase 的结构在**文档里** | [../Learning_Redis/02-五大数据类型的语义.md](../Learning_Redis/02-五大数据类型的语义.md) |
| MongoDB | 都是 JSON 文档 | Mongo 以「文档 + 更新算子 + 聚合管道」为中心；Couchbase 以「key 取值 + CAS + 视图/索引」为中心，文档是 value 的形状 | [../MongoDB_The_Definitive_Guide_3e/01-概述与入门.md](../MongoDB_The_Definitive_Guide_3e/01-概述与入门.md) |
| Cassandra | 都是分布式 + 最终一致运维模型 | Cassandra 的分片是**去中心化**（gossip + token ring），Couchbase 是**集中式集群映射**（一张 VBMap 表） | [../Cassandra_The_Definitive_Guide/07-集群架构与Gossip.md](../Cassandra_The_Definitive_Guide/07-集群架构与Gossip.md) |
| 关系库 | 都能做 OLTP | 「文档 ≈ 行、属性 ≈ 列」只是入门类比；没有 schema/JOIN/2PC，跨键原子性要靠 Transactions API | [../设计数据密集型应用/02-数据模型与查询语言.md](../设计数据密集型应用/02-数据模型与查询语言.md) |

## 5. 🔧 类比实测（SQLite/DuckDB，非 Couchbase 行为）

实验脚本：`D:\develops\tmp\dbwave_w4_couch\exp.py`，原始输出 `results.txt`。本机未安装、未运行 Couchbase Server，以下数字**只用于建立概念直觉**。

**E5 · 「文档 = 一次 IO 拿到整棵聚合树」的代价**：SQLite 建两张表，`u_emb(id, doc)` 存内嵌 20 个子项的 JSON，`u_ref` + `o_ref` 走规范化 JOIN，各 5 万用户 / 100 万订单。

- 取单个聚合根：内嵌 **0.13ms** vs JOIN **0.06ms**。
- 结论与直觉相反的一面：**当文档不大、且 JOIN 命中索引时，规范化并不慢**；内嵌真正的收益在「跨网络/跨分片时把 N 次往返压成 1 次」，本机单文件里体现不出来——这正是本册反复强调的「🔧 只能类比语义，不能类比成本结构」。

**E5b/E5c · 为什么后来要长出 Analytics/Analytical Service**：同一份 100 万行数据，行存 SQLite 全表 `group by` **433ms**，列存 DuckDB **4.3ms**（≈102×）。把「操作型读取」和「分析型扫描」放同一个引擎，是 2014 那本书没解决、而 2026 用独立服务解决的问题。

## 6. 三种典型用法与反用法

1. **会话/缓存层**（✅ 官方 expiration 文档的场景举例）：短生命周期、可丢失、按 key 点查 → Ephemeral 桶 + `maxTTL`（maxTTL 是后来才有的桶/集合级设置 ✅）。
2. **用户画像/目录主记录**：一次读多属性、需按属性查 → 文档 + GSI/SQL++。
3. **实体-关系重的报表**：2014 年靠视图聚合，今天靠 Analytical Service 或导出到数仓 → 见 [04-视图与二级索引时代.md](04-视图与二级索引时代.md)、[10-从2014基线到2026演进手册.md](10-从2014基线到2026演进手册.md)。
4. 反用法（⚠️ 转述常见工程教训）：把 Couchbase 当消息队列（无队列语义）、当强一致账本（单键 CAS 之外需要 Transactions）、当搜索引擎（该用 Search Service 而不是 LIKE/视图前缀）。

## 7. 元数据与不变式（记在脑子里的四条）

- key 唯一性范围：collection（2014：bucket）。
- 一次操作只保证单键原子（✅ [learn/data/data](https://docs.couchbase.com/server/current/learn/data/data.html)）；跨键原子由 Transactions API 以「乐观锁 + CAS」实现（✅ [learn/data/transactions](https://docs.couchbase.com/server/current/learn/data/transactions.html)）。
- 值有大小上限（当时文档口径 ⚠️ 20MiB 量级），因此「文档必须能装进一次内存操作」是硬约束。
- 无 schema ⇒ 类型/字段的兼容性演化由应用负责 ⇒ 见 [06-数据建模与键空间设计.md](06-数据建模与键空间设计.md) 的演化段。

## 8. 与其他章的接缝

- 桶为什么不是分片单位 → [02-集群架构与vBucket映射.md](02-集群架构与vBucket映射.md)
- 取值时到底发生了什么（网络、拓扑、序列化）→ [05-客户端SDK与语言集成.md](05-客户端SDK与语言集成.md)
- 「键怎么选」的所有工程后果 → [06-数据建模与键空间设计.md](06-数据建模与键空间设计.md)
- 多活下的 value 收敛 → [07-跨数据中心复制与多活.md](07-跨数据中心复制与多活.md)

## 5b. 文档体积与访问模式的工程后果（⚠️ 转述 + 🔧 类比直觉）

- **小文档（<1KB）**：内嵌与引用差异可忽略，序列化/反序列化成本远低于网络往返；此时选内嵌的唯一理由是「减少键数量、简化键空间」。
- **中等文档（1–10KB）**：内嵌开始体现「一次 IO 拿全聚合」的收益，但驱逐后重新加载的代价也随体积线性增长（⚠️ 转述通用工程经验）。
- **大文档（>100KB）**：接近 20MiB 上限时，序列化成本与网络传输均成为瓶颈；子文档 API（`lookupIn/mutateIn`）的价值在此区间最大（✅ 见 [03-键值操作与并发控制.md](03-键值操作与并发控制.md) 第 6 节）。
- 🔧 类比（非 Couchbase 行为）：SQLite 中 `json_extract` 对 100KB JSON 文档的单次提取在本机约 0.1ms 量级，但对 1MB 文档则升至 1ms+——体积与访问成本的线性关系在两边同构。
- **反模式登记**：把「无 schema」理解为「不需要设计文档结构」是 2014 与 2026 共同的事故源（⚠️ 转述）；现代做法是在应用侧保留 `type` 字段 + 校验层，或用 collection 做类型/租户隔离（✅ [scopes-and-collections](https://docs.couchbase.com/server/current/learn/data/scopes-and-collections.html)）。

## 5c. 二进制值的使用场景与限制（✅ 概念 + ⚠️ 转述）

Couchbase 的 value 不仅可以是 JSON，也可以是**任意二进制块**（✅ [learn/data/data](https://docs.couchbase.com/server/current/learn/data/data.html)：「values can be either binary or JSON」）。

| 场景 | 值类型 | 注意事项 |
|---|---|---|
| 会话/缓存 | JSON 或序列化对象 | 最常见用法，expiration + Ephemeral 桶 |
| 图片/文件缩略图 | 二进制 | 受 20MiB 上限约束；大文件应存对象存储，Couchbase 只存元数据 |
| 计数器 | 二进制（64 位整数） | 用 `increment/decrement` 原子操作（见 03 章） |
| 序列化对象 | 语言特定格式（protobuf/MessagePack） | SDK transcoder 负责编解码（见 05 章） |

- 🔧 类比（非 Couchbase 行为）：SQLite 的 `BLOB` 列可存任意二进制，但与 Couchbase 的区别在于——SQLite 的 BLOB 无法被查询引擎理解，而 Couchbase 的 JSON value 可以被 GSI/Search/Analytics 消费。二进制值在 Couchbase 中是**不透明的**，不能索引、不能查询、不能子文档访问。
- ⚠️ 转述：混存 JSON 与二进制在同一桶中会让视图/索引/迁移三处都变复杂，工程上建议按值类型分 collection。

## 核心概念速览（中英对照）

- **键值模型** — Key-Value Model：以应用自造的 key 寻址一个不透明或半结构化 value 的数据模型，读路径 O(1)。
- **文档** — Document：value 取 JSON 时的形态，属性即字段，无强制 schema，「文档≈行、属性≈列」只是类比。
- **桶** — Bucket：内存配额、副本数、驱逐策略与存储引擎的承载单位，2026 是其下 scope/collection 的容器。
- **范围收集** — Scope / Collection：桶内的逻辑命名空间，key 唯一性以 collection 为界；集群级上限 1000 collection。
- **混合持久化** — Hybrid Persistence：元数据常驻内存、value 依策略决定驻留、磁盘由引擎托管的三层结构。
- **驱逐策略** — Ejection/Eviction Policy：`value only` / `full eviction` / `no eviction` 三档，决定内存压力下丢什么。
- **扩展属性** — Extended Attributes (XATTR)：与用户 JSON 正文分离、只有请求它的应用可见的元数据槽位。
- **聚合根** — Aggregate（ACP 里的 A）：把一致演化的一组子结构内嵌进同一文档，换取一次 IO 取全。
- **瞬时桶** — Ephemeral Bucket：不落盘的纯内存桶，取代早年的 Memcached 桶定位。
- **存储引擎** — Storage Engine（Couchstore / Magma）：磁盘侧组织方式；Magma 为 LSM 式引擎且视图不支持它。
- **数据服务** — Data Service：负责键值存取、副本与故障转移的服务器角色。
- **文档标识** — Document Key：由应用拼出的、同时承担前缀查询与租户路由职责的唯一串。
- **元数据 CAS** — Compare-And-Swap 版本：随每次写变化的令牌，是单键并发控制的唯一凭据（见 03 章）。
- **过期** — Expiration/TTL：逻辑到期与物理清理分离（见 03 章宽限期实测）。
- **无模式** — Schemaless：结构演化不需要同步 DDL，代价是把一致性责任推给应用。

## 最新演进与工业实践

1. **版本基线刷新**：本册所有 2026 事实以 **Couchbase Server 8.0**（文档 `current` 指向 8.0；维护版 **8.0.3 于 2026 年 9 月发布**）为准 → [Release Notes](https://docs.couchbase.com/server/current/release-notes/relnotes.html)、[What's New in 8.0](https://docs.couchbase.com/server/current/introduction/whats-new.html)。✅
2. **数据模型面**：官方《The Couchbase Data Model》明确「轻量灵活、可随应用渐进演化」的口径 → https://docs.couchbase.com/server/current/learn/data/document-data-model.html ✅
3. **桶的三代变迁**：Memcached 桶（2014 时代的「纯内存桶」选项）**在 8.0 被移除**；桶类型收敛为 Couchbase/Ephemeral 两种，桶内即 scope+collection 层级 → https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/buckets.html ✅
4. **引擎换代**：Couchstore → **Magma** 成为新桶默认（128 vBucket / 100MiB 起）；这意味着 2014 书里所有「按内存换页调 bucket」的直觉要按 LSM 重学 → https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/storage-engines.html ✅
5. **静态加密原生化**：8.0 EE 可对桶数据、日志、审计与配置在落盘时加密，并对接外部 KMS → https://docs.couchbase.com/server/current/rest-api/security/encryption-at-rest/encryption-at-rest.html ✅
6. **云服务接替「装一套」**：开发面默认假设是 **Couchbase Capella**（托管，控制台在 `https://cloud.couchbase.com/`）→ 产品页 https://www.couchbase.com/products/couchbase-cloud/ 与文档入口 https://docs.couchbase.com/home/cloud.html ✅（`https://www.couchbase.com/products/capella/` 亦 200）
7. **AI 化的数据模型**：文档里可直接放 embedding 数组并被向量索引消费（见 10 章），官方把这条线称 **AI Data Plane** → https://www.couchbase.com/products/ai-services/ ✅；概念页 https://docs.couchbase.com/server/current/vector-index/vectors-and-indexes-overview.html ✅
8. **工业实践提醒**：把「无模式」当免设计许可证是 2014 与 2026 共同的事故源；现代做法是在应用侧保留文档 `type` 字段 + 校验层，或直接用 collection 做类型/租户隔离（✅ scopes-and-collections 页把 collection 描述为可按内容类型划分的数据容器）。
9. **与盘上书籍的读序建议**：先 [../MongoDB_The_Definitive_Guide_3e/05-应用设计与模式.md](../MongoDB_The_Definitive_Guide_3e/05-应用设计与模式.md) 建立文档建模通用直觉，再读本册 06 章；原理层回 [../设计数据密集型应用/02-数据模型与查询语言.md](../设计数据密集型应用/02-数据模型与查询语言.md)；横向比较回 [../nosql精粹.md](../nosql精粹.md)。
