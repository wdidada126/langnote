# 01 流处理的兴起与 Flink 的定位

> ⚠️ **重构章声明**：原书（疑 Ben Stopford《Introduction to Apache Flink: Streaming at Scale》，O'Reilly 2022）
> 真实目录未取得（官方页 403，取证链见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第一节）。本文件是按
> 「短篇入门书开篇章」惯例**重构**的概念笔记，不冒充原书逐章对位。
> 本册三态口径：✅ 实证 / ⚠️ 转述推定 / 🔧 本机演示（**全部非 Flink 行为**）。

## 本章地图

1. 数据系统对「时间」的需求演化：批 → 微批 → 逐条流。
2. 「Streaming at Scale」难在哪：不稳定性、无序性、状态膨胀、故障恢复。
3. Flink 是什么、不是什么：逐条流优先、内置事件时间、真状态引擎。
4. 版图定位：与 Kafka（传输）、Spark（批/微批）、流式数据库（产品形态）的分工。

## 核心精讲

### 1. 批处理的时间观：「算的时候，世界已经定了」

批处理把数据当**有界集合**：数据到齐 → 全量扫描 → 出报表。它的正确性建立在两个隐含假设上：
（a）输入有限；（b）处理时刻 = 数据完整时刻。数仓 T+1 的「T」就是这个边界。
⚠️ 转述：这正是 [../Streaming_Systems/02-数据处理的来龙去脉.md](../Streaming_Systems/02-数据处理的来龙去脉.md)
梳理的「数据处理的来龙去脉」主线——批的一切语义都锚在「切角」（当数据来齐）这个动作上。

### 2. 微批是妥协：把流切碎装进批的盒子

Spark Streaming 式微批（DStream）以秒级小批模拟流：延迟下限被批间隔锁死，窗口聚合要跨批拼状态，
「逐条」只是幻觉。⚠️ 转述谱系登记见 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)
与 [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)（盘上已有，本册不重复展开）。

### 3. 逐条流（native streaming）的四座大山

- **乱序**：消息以事件时间看永远不「到齐」——分布式生产者没有全局时钟。
- **状态**：逐条累积的聚合值、join 缓存、CEP 模式，规模可以到 TB 级且必须可查。
- **故障**：逐条处理一旦崩溃，要么丢要么重；「恰好一次」需要快照+回滚+幂等三件套合谋。
- **升级**：作业是 7×24 长驻进程，改并行度/改逻辑 = 给飞行中的飞机换引擎（savepoint）。
✅ 以上四条正是 Flink 官方 "Stateful Stream Processing" 概念篇的组织方式：
`https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/`（实测 200）。

### 4. Flink 的答案卡片（本章只给「是什么」，机制留给 02/03/04）

| 难题 | Flink 的回答 | 本册深读处 | 姊妹册工程处 |
| --- | --- | --- | --- |
| 乱序/时间 | 事件时间 + watermark + 允许迟到 | [02-时间四要素：事件时间乱序水位线与窗口.md](02-时间四要素：事件时间乱序水位线与窗口.md) | [../Stream_Processing_with_Apache_Flink/06-时间与窗口算子.md](../Stream_Processing_with_Apache_Flink/06-时间与窗口算子.md) |
| 状态 | keyed state + RocksDB 状态后端 | [03-状态容错与恰好一次语义.md](03-状态容错与恰好一次语义.md) | [../Stream_Processing_with_Apache_Flink/07-有状态函数与状态管理.md](../Stream_Processing_with_Apache_Flink/07-有状态函数与状态管理.md) |
| 故障 | 分布式快照 checkpoint + savepoint | 03 | [../Stream_Processing_with_Apache_Flink/12-补编-检查点机制与分布式快照.md](../Stream_Processing_with_Apache_Flink/12-补编-检查点机制与分布式快照.md) |
| 抽象层 | DataStream → Table/SQL | [04-API分层：DataStream与Table与SQL.md](04-API分层：DataStream与Table与SQL.md) | [../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md](../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md) |

### 5. 版图：Flink 不吃谁的位置

- **Kafka 是神经，Flink 是大脑**：传输系统只保证送达，不定义时间语义（✅ 官方连接器文档
  `https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/` 实测 200）。
  盘上横向视角：[../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)。
- **湖仓是归宿**：流式结果要落表格式才能被批读——见 [../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md](../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md)。
- **流式数据库是竞争形态**：把 Flink 的问题域装进数据库产品，见
  [../Streaming_Databases/02-流处理平台版图.md](../Streaming_Databases/02-流处理平台版图.md)。

## 🔧 类比实测：增量维护 vs 全量重算（DuckDB/SQLite，非 Flink 行为）

流处理的本质卖点之一是「来一条更新一条」的增量性。它在小数据上**不占优**——这正是要用数字破除的迷思。
本机 Python 3.13.2 + sqlite3 3.45.3（`D:\develops\tmp\dbwave_w4_flink\demo.py`，seed=155）：

- 50,000 条事件、49 个 key：逐条「读-改-写」UPSERT 维护计数状态耗时 **125 ms**；
  先全部落表、事后一次 `GROUP BY` 重算仅 **32 ms**（含插入），两者结果一致（基数 49、总数 50000 校验通过）。
- 结论 🔧：**有界小数据集上，重算比维护状态便宜**。状态型流处理的收益窗口出现在——
  历史无界（重算要扫全量）× 输出要求亚秒 × 计算局部性差（每条只碰少量 key）三条件同时成立处。
- 非 Flink 行为声明：单进程 SQLite，无并行、无网络 shuffle、无故障模型；仅类比「增量 vs 重算」的成本结构。

## 时间线速览（⚠️ 通说口径，未逐一取证原始公告）

| 年代 | 节点 | 与本书关系 |
| --- | --- | --- |
| 2000s | 批数仓黄金期（MapReduce 范式） | 「T+1 世界」的基线 |
| 2010–2013 | Twitter Storm（逐条但无状态语义）、MillWheel/Aurora（内部系统定语义） | 概念源头；登记线 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md) |
| 2014 | Flink 从柏林工大（原 Stratosphere 项目）进入 Apache 孵化 | 「内置事件时间」差异化起点 ⚠️ |
| 2015–2019 | Kafka 普及 + 流式湖仓雏形；Flink 1.x 补齐 SQL/状态后端 | 工程化阶段（姊妹册基线 1.7 在此段尾） |
| 2019 | 本书疑似作者 Ben Stopford《Streaming Analytics》出版 | ⚠️ 同一作者假设下的前作谱系（未核实） |
| 2022 | 本书成书（⚠️ 名册给定年份） | 概念向短篇：把「at scale」的四座大山讲透 |
| 2024–2026 | Flink 2.x 一体化流批、Materialized Table | 见 06 章演进正表 |

## 与它书/它章的联系

- 「什么场景不值得上流式」的第一性讨论在 [../Streaming_Systems/01-流式入门.md](../Streaming_Systems/01-流式入门.md)。
- Flink 架构（JobManager/TaskManager/slot 共享）概念图：✅ `https://flink.apache.org/what-is-flink/flink-architecture/`（实测 200），细节留给 [05-规模化部署与运维.md](05-规模化部署与运维.md)。
- 论文线（MillWheel/Aurora/Dataflow Model 谱系）登记在 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)；工程索引见 [../../db/db.md](../../db/db.md)。

## 常见误区

1. 「Flink = 更快的 Spark」：错。微批与逐条流的差别在**时间语义与状态原语**，不在吞吐数字。⚠️ 转述。
2. 「有了 Kafka 就不需要流引擎」：Kafka Streams 也是流引擎；传输 ≠ 计算。⚠️。
3. 「流处理总是更省」：见 🔧——历史有界且能容忍重算时，批更省、更简单、更好纠错。
4. 「低延迟 = 事件时间正确」：处理时间延迟再低也答错「按事件时间聚合」的题（见 02 章）。

## 核心概念速览（中英对照）

- **批处理** — batch processing：对有界数据的一次性全量计算，正确性锚在「数据已齐」假设。
- **微批** — micro-batching：以秒级小批模拟逐条流（Spark Streaming 路线），延迟下限受批间隔约束。⚠️
- **逐条流** — native/per-event streaming：Flink 路线，每条事件独立触发计算与状态更新。
- **有状态流处理** — stateful stream processing：计算依赖历史累积（计数/连接池/模式前缀），状态是引擎的一等公民。✅（官方概念页）
- **乱序** — out-of-order-ness：事件到达顺序 ≠ 事件时间顺序，分布式系统的常态。
- **恰好一次** — exactly-once（语义）：效果上每条事件对状态恰好贡献一次，容错与重放的黄金承诺（03 章机制化）。
- **流批一体** — stream-batch unification：同一语义/引擎同时服务流与批；Flink 2.x 的演进主线（见 06 章）。
- **数据立方需求** — always-on analytics：业务要求「随时问随时新」，是流处理的第一驱动力。⚠️ 转述
- **引擎 vs 总线** — engine vs bus：Kafka 传输送达、Flink 定义时间/状态/语义、表格式负责可见性提交。
- **长驻作业** — long-running job：流作业是服务不是任务，升级=热替换（savepoint 的动机）。

## 最新演进与工业实践

- **2022 基线 → 2026 现状**：本书成书于 Flink 1.14/1.15 时代（⚠️ 推定）；此后 Flink 1.18（2023 底，
  ✅ 官方文档版本根页 `https://nightlies.apache.org/flink/flink-docs-release-1.18/` 实测 200）引入
  Materialized Table 早期预览（⚠️ 社区通说）；**Flink 2.0**（2024，⚠️ 通说 5 月）把「流批一体化」从口号变成
  单一 Planner 与统一表语义（✅ 文档版本根页 `https://nightlies.apache.org/flink/flink-docs-release-2.0/` 实测 200）。
- **生态位变化**：Flink 已成为 CDC 入湖（Flink CDC → Paimon/Iceberg/Hudi）的事实标准写入引擎之一 ⚠️ 转述；
  盘上实证笔记：[../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md](../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md)、
  [../Use_Iceberg_with_Spark/06-维护过程与流式写入.md](../Use_Iceberg_with_Spark/06-维护过程与流式写入.md)（Spark 侧对照）。
- **工业采用**：LinkedIn（开源母体）、Netflix、Uber、阿里（双 11 实时大屏/计算平台）、字节/快手等大规模运行
  Flink——⚠️ 转述业界通说，本册未逐一取证公司名场面；可核锚点仅 ✅ `https://flink.apache.org/what-is-flink/flink-applications/`。
- **云托管形态**：Ververica Platform/阿里云实时计算 Flink 版等把「长驻作业运维」产品化 ⚠️ 转述；
  与 [../Streaming_Databases/10-部署模型.md](../Streaming_Databases/10-部署模型.md) 的托管趋势互证。
- **本册观点保持**：2026 年「值不值得上 Flink」的判据仍是第 1 节四座大山 + 🔧 增量/重算成本结构，
  引擎版本号换了也不变。
