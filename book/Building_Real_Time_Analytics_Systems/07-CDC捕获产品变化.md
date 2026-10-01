# 07 通过 CDC 获取产品变化（Getting Product Changes with CDC）

> 书目 #157 第 7 章 ｜ 主题：从业务数据库获取更改信息、CDC、将 CDC 应用于 AATD。
> 精读重构（目录 ✅，展开 ⚠️），非原书文本；Debezium 具体行为不实测，⚠️+官方文档。

## 本章任务

- 解决 03/05 章埋下的债：维表（product/store）的**持续正确供给**——不是双写，而是从业务库变更日志派生；
- 掌握 CDC 的机制地图：读 binlog/WAL 的日志挖掘式 vs 查询式轮询 vs 触发器/双写，以及为什么日志挖掘是工业默认；
- 把 AATD 的 `products` 表变更变成 Kafka topic，接入 Pinot 维表与 08 章流连接。

## 7.1 从业务数据库获取更改信息（Getting Changes from the OLTP Store）

- 需求本质：分析侧要的是"**变更事件**"而非"当前快照"——快照丢失了中间态（改价历史），全量拉取又打爆 OLTP；
- 三条路的批判：
  1. 定时全量/增量拉取（updated_at 轮询）：漏删除、中间态丢失、拉取尖峰伤害主库；
  2. 应用双写（dual-write）：业务事务与事件发送**不在同一提交点**——崩溃窗口必然漂移，一致性靠忏悔；
  3. **日志挖掘（log-based CDC）**：从数据库事务日志读"已提交变更流"，与业务解耦且保留全事件（含删除/回滚前态）；
- outbox 模式补刀：确需发"业务事件"（非行变更）时，把事件表写进同一本地事务，再由 CDC 抓 outbox 表——双写问题的事务化回收（⚠️ 书中是否展开 outbox 未实证，作为通识登记）。

## 7.2 CDC（Change Data Capture）

- 定义：捕获"数据变了"这一事实并转成事件流；输出语义常为 row 级 before/after 信封（op=c/u/d + ts_ms + source 元数据 ⚠️ 字段以 Debezium connector 文档为准 https://debezium.io/documentation/reference/stable/ ✅200）；
- 关键机制心智（⚠️ 均转述）：
  - MySQL binlog（ROW 格式）/PostgreSQL 逻辑复制槽（wal2json/pgoutput）为读取源；
  - 快照阶段（初始全量）+ 流阶段（增量日志）的两段式，及其一致性衔接；
  - 结构变更（DDL/schema evolution）时信封的演进策略；
  - 删除事件（tombstone）在下游 KV 表上的物理解除语义。
- 谱系对照：Debezium（Kafka Connect 插件形态）/ Maxwell / Canal（MySQL 中文圈）/ Flink CDC（把 CDC 直接接进流计算 ⚠️ 通识）；盘上无专册，本登记为缺口（兄弟义务：与波次总索引对位，此处不挂未验名链）。
- 理论锚：CDC 让"表=流的折叠态、变更日志=表的原因"在工程上闭环——[../Streaming_Systems/06-流和表.md](../Streaming_Systems/06-流和表.md) 的正题。

## 7.3 将 CDC 应用于 AATD（Applying CDC to AATD）

- 管线：`products` 表（MySQL ⚠️ 书所用水库以目录推断）→ Debezium connector → `inventory.products` 型 topic → 两路下游：
  1. Pinot 键控维表（upsert 语义收在 09 章讲透）；
  2. Kafka Streams 侧作为**表流**（KTable）供 08 章流连接；
- 本册的教科书一击：**维表不再是"导入的数据"，而是"另一条流"**——08 章的 join 因此从"流×静态表"升级为"流×表（changelog）"，语义完备；
- 工程护栏（通识）：连接器单 topic 分区数与下游并发对齐；初始快照在段模型里的重放幂等（依赖 09 章 upsert）；信封解码失败进死信队列。

## 🔧 概念对照（类比，非本书引擎行为）

DuckDB 1.5.5（**非 Debezium**）手工体验"变更流 vs 快照"的差别：把一表按批"最新快照覆盖"物化会丢中间态；改为 append 带 op 列的变更日志再折叠（`QUALIFY row_number() OVER (PARTITION BY key ORDER BY ts DESC)`）即可恢复时点任意状态——E4 的 append+dedup 分支（0.004s 与 upsert 状态等价）正是"CDC 日志折叠出当前表"的最小样本。数据：`D:\develops\tmp\dbwave_w8_brtas\results.txt`。

## 与其他册的关系

- 日志与 WAL 的数据库内核视角（CDC 读的东西到底是什么）：[../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)（盘上在盘目录 ✅ 已验名）。
- Kafka 作为总线的保留策略/压缩 topic（tombstone 依赖 log compaction ⚠️ 机制指认）：[../Kafka权威指南.md](../Kafka权威指南.md)；
- 湖仓侧的 CDC 入库（同一变更流的冷路径消费）：[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **变更数据捕获** — Change Data Capture (CDC)：把"数据变了"转成事件流的技术族。
- **日志挖掘** — Log Mining：从事务日志读已提交变更的 CDC 实现路线。
- **双写问题** — Dual-Write Problem：业务提交与事件发送跨提交点的固有漂移。
- **发件箱模式** — Outbox Pattern：事件与业务状态同事务落表再被 CDC 捞出。
- **信封** — Envelope：Debezium 型 before/after+op+元数据的消息结构（⚠️）。
- **快照阶段** — Snapshot Phase：CDC 初始全量与增量日志的衔接段（⚠️）。
- **墓碑消息** — Tombstone：删除事件在压缩日志中的物理清除记号（⚠️）。
- **表流** — Table Stream / Changelog Stream：以流形态供给的"表"。
- **结构演进** — Schema Evolution：DDL 变化下事件信封的兼容策略。
- **死信队列** — Dead Letter Queue：解码失败消息的隔离通道。
- **逻辑复制槽** — Replication Slot：PostgreSQL 侧 CDC 读取锚点（⚠️ 通识）。
- **日志压缩** — Log Compaction：按键保留最新值的 topic 清理语义（⚠️）。
- **维表流化** — Dimension as Stream：本册方法论：维不是导入物而是流。

## 最新演进与工业实践

- Debezium Server/Operator 化与 Outbox/Inbox 原生示例持续演进 ⚠️；官方 https://debezium.io/documentation/reference/stable/ ✅200（curl 实测）。
- Flink CDC 3.x 已成中文圈 CDC 事实标准之一（整库同步/ schema 演进自动化 ⚠️ 转述），与盘上 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md) 可接续；本册未用 Flink CDC。
- "零 ETL/CDC 直连仓"趋势（2024 后云侧兴起 ⚠️）：CDC 从"喂流"扩展为"喂仓"，与本册"喂维表+喂 join"同族——盘上镜像叙事见 [../Streaming_Databases/08-零ETL与近零ETL.md](../Streaming_Databases/08-零ETL与近零ETL.md)。
- MySQL 生态：binlog ROW+GTID 组合是 CDC 默认前置，Canal/Maxwell 长尾使用 ⚠️ 通识。
- DuckDB 无 CDC 源端（🔧 类比声明）：嵌入式场景以"增量 Parquet+主键折叠"手工替代（E4 方法），非引擎特性。
- 中译对应：机工版第 7 章《通过CDC获取产品变化》（✅ QQ 读书实抓）。
