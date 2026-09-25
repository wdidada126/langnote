# 第 8 章 基于 Hudi Streamer 构建数据湖仓

> 原书章题（译系列核实）：基于 Hudi Streamer 构建数据湖仓。小节地图：湖仓架构来救场（Alcubierre 的数据孤岛之痛、问题回顾、数据管理与本地化一致性、释放分析的力量、异构数据与模式演进）→ Hudi Streamer 入门（什么是 Streamer、设置、数据源总览）→ Hudi Streamer 实战（准备上游、从 S3/Kafka/RDBMS 摄取）→ 探索选项（General/Source/运维选项）→ 数据质量保障与去重 → 总结。
> 机制口径以官方文档 Hudi Streamer / Ingesting Data 各页为准。

## 本章地图

> 一句话：**Hudi Streamer = 把"读取源 → 微批转换 → upsert 入湖 → 记 checkpoint"固化为一个可断点续传的 Spark 作业模板；它不是新引擎，而是第 3 章写路径 + 第 4 章增量读的产品化封装。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 8.1 为什么要有 Streamer | 数据孤岛、重复造轮子的 ETL 工具 | 摄取是湖仓的"最后一公里"标准件 |
| 8.2 运行模型 | 微批循环 + source checkpoint | exactly-once 的边界要说清 |
| 8.3 数据源矩阵 | Kafka/S3/JDBC/Hudi(增量) 等官方 source | 每类 source 的位点语义不同 |
| 8.4 选项体系 | General/Source/Transform/Write/Hive Sync/运维 | 一张参数地图 |
| 8.5 多跳管线 | Bronze→Silver 用 HoodieIncrSource | 湖内增量搬运是杀手锏 |
| 8.6 Schema 与质量 | SchemaProvider、evolving、去重、preCombine、质量断言 | "脏数据进不来" |
| 8.7 其他写路 | Flink/Kafka Connect（书第 10 章案例） | Streamer 之外的互补选项 |

## 核心精讲

> **教学示意，不参与构建。**

### 8.1–8.2 运行模型

```text
spark-submit --class org.apache.hudi.utilities.deltastreamer.HoodieStreamerMain \
  hudi-utilities-bundle.jar \
  --source-class org.apache.hudi.utilities.sources.AvroKafkaSource \
  --source-ordering-field ts \
  --target-base-path s3://lake/hudi/bronze/orders \
  --target-table bronze_orders --op UPSERT \
  --scheduling-interval-seconds 60 \
  --continue-on-failure
```
（旧名 `HoodieDeltaStreamer` 仍可用；官方已更名 Hudi Streamer，书中同步。）

- 每个微批：`source.fetchNext(checkpoint)` → 可选 transform 链 → 第 3 章的 upsert 写入 → 成功后推进 checkpoint。
- **Checkpoint 存哪里**：默认写进目标表的 commit 元数据（`hoodie.deltastreamer.source.checkpoint...`），也可存 ZK——位点与事务同库 = "提交成功即位点前移"，天然接近 exactly-once；Kafka 位点若独立存储则存在"提交成功但位点未推进"的重复窗口，靠 upsert 幂等消化。
- 失败恢复：`--continue-on-failure` + 自动 rollback（03 章 ①）；毒丸记录有专门的跳过/报错行为选项（语义开关口径以官方 Streamer Configs 页为准，本目录不背名字）。
- Checkpoint 的形状（各 source 不同，机制同源）：

| Source | checkpoint 内容 | 恢复动作 |
| --- | --- | --- |
| Kafka | topic → 各分区 offset（JSON 汇总） | 从 offset 区间重放 |
| JdbcSource | 增量列水位（如 `max(id)` / `max(ts)`） | 从水位之后重查 |
| S3/文件类 | 已读文件清单 + 目录位点 | 跳过已读对象 |
| HoodieIncrSource | 已消费的 instant time | 从该 instant 之后增量读（04 章） |

- 一个常被忽略的点：**checkpoint 前移与表提交不是同一个原子**——Streamer 的设计是"提交成功后才记 checkpoint"（记在 commit 元数据里），崩溃重启会从上一个成功提交的位点重放；这正是 8.2 "接近 exactly-once"论断的实现细节。

### 8.3 数据源矩阵（官方支持面）

| Source | 位点语义 | 典型格式 | 备注 |
| --- | --- | --- | --- |
| JsonKafkaSource / AvroKafkaSource | Kafka offset 区间 | JSON/Avro + Confluent Schema Registry | CDC 流（Debezium envelope）常配 `--enable-hive-sync` 与 schema provider |
| s3TextBasedSource(S3/json/Avro) | 对象清单 + 增量目录扫描 | 落地文件再摄取 | 与"直写湖"二选一时看治理需求 |
| JdbcSource | 增量列（`--source-partition-lower/upper`） | 关系表快照+增量 | 大表回填 + 增量列追新 |
| **HoodieIncrSource** | **begin/end instant（第 4 章增量读）** | 读另一张 Hudi 表 | 多跳管线核心（8.5） |
| KafkaDvmSource 等 | Debezium Value 反序列化 | CDC 事件 | 版本支持面以文档为准 |
| 自定义 | Source interface | — | 实现 `fetchNext` + checkpoint |

- 书中表 "Hudi Streamer 支持的数据源（Table 8-1）" 与官方 Ingestion Sources 页一致；**写 Flink/Kafka Connect 路线见 8.7**。

### 8.4 选项体系（记族不记名）

| 族 | 代表选项 | 作用 |
| --- | --- | --- |
| General | `--source-class --target-table --op --source-limit`（单批上限） | 作业骨架 |
| 写入映射 | `--record-key-field --partition-path-field --source-ordering-field` | 对齐 03 章 key generator/merge mode |
| Schema | `--schema-provider`（Inferred/JsonFile/SqlDatabase/Evolving）、`--source-avro-schema-str` | 异构与演进 |
| Transform | `--transformer-class`（SQLTransformer、ChainedTransformer、AWSTransform/lambda 等） | 清洗/脱敏/类型化 |
| Hive Sync | `--hive-sync --hive-sync-url --hive-sync-table` | 目录可见（09 章） |
| 运维 | 连续模式、微批间隔、指标与重试选项族 | 生产化 |

### 8.5 多跳管线：湖吃湖（Hudi → Hudi）

```text
Kafka(Debezium) ──AvroKafkaSource──▶ Bronze(Hudi, MOR)
Bronze ──HoodieIncrSource(增量读: 上次 instant→)──▶ Silver(Hudi, 清洗/去重/维度化)
Silver ──批/流 SQL 聚合──▶ Gold(Hudi, 指标/宽表)
```

- 每一跳都是"上游表的增量查询下游化"：位点存在下游自己的 checkpoint 里（第 4 章 4.6 的 begin instant）。
- 关键收益：**任何一跳可独立重放、独立回滚（savepoint，第 9 章）**；对比"一条巨型 DAG 天天全量重刷"。
- 与第 10 章 RetailMax 案例的 Bronze/Silver/Gold 完全同构。

### 8.6 数据质量与去重（书中"数据质量保障与去重"）

- **去重三层**：record key 幂等（03 章 merge mode）→ Streamer checkpoint（批间不重读）→ 专门的批内去重策略（官方 dedup 策略参数族，含忽略错误/按记录数或时间取最新等模式，口径以文档为准）。
- **preCombine/ordering field 选错 = 数据倒退**（03 章 3.8 呼应）。
- **质量断言**：transform 阶段自定义过滤/打点（官方示例：NullFieldTestFilter 一类 transformer）；复杂规则放 SQLTransformer。
- **异构合并**：EvolvingSchemaProvider 把多 topic/多表 schema 合并成目标表宽 schema（书中 Alcubierre 案例核心痛点，3.9 schema evolution on write 的摄取侧应用）。

### 8.7 Streamer 之外：Flink 与 Kafka Connect（互补而非替代）

- **Flink Hudi connector**（书中第 10 章 airline 案例采用）：changelog 流写 MOR、事件时间对齐 checkpoint；适合 Flink 已深度使用的团队（对照 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)）。
- **Kafka Connect Hudi Sink**：托管式连接器的"无代码摄取"，位点走 Connect 框架（第 10 章 RetailMax 用 Debezium + Sink Connector）。
- 选型口诀：**要转换选 Streamer/Flink，纯搬运选 Connect**。

## 版本演进

| 项 | 旧版 | 1.x（本书基线） |
| --- | --- | --- |
| 名称 | DeltaStreamer（类名残留） | Hudi Streamer（文档与 CLI 统一） |
| Kafka Avro/JSON 反序列化 | 手动 registry 配置 | 原生 Schema Registry 集成 + 演进 provider |
| 增量多跳 | HoodieIncrSource 已可用 | 与 CDC 模式配合形成"湖内流" |
| 调度 | --once 外部 cron | `--continuous`、微批间隔 + 表服务守护合并 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "Streamer 保证 exactly-once 端到端" | 保证的是"位点随提交推进"的 at-least-once + 幂等写；端到端语义还取决于 source 可重放与 record key 幂等 |
| "upsert 会去重，随便重放" | 去重按 record key 判同；同 key 但 ordering field 不单调时，重放会把新值盖成旧值 |
| "Bronze 也要做成 COW 方便查询" | Bronze 的使命是便宜落地：MOR + 大分区是常态；分析在 Silver/Gold 做 |
| "schema 不匹配会失败才对" | 默认宽容（infer/evolve），失败反而要靠配置"严格模式"拦住脏 schema |
| "Streamer 是摄取唯一入口" | Flink/Connect/自写 DataSource 都在官方路线内；Streamer 的价值是把常见组合标准化 |

## 与其他章 / 其他笔记的联系

- 8.2 的"提交后推位点"依赖 [03-写入Hudi.md](03-写入Hudi.md) 3.5 与 [07-Hudi中的并发控制.md](07-Hudi中的并发控制.md)；8.5 的位点 = [04-从Hudi读.md](04-从Hudi读.md) 4.6。
- 8.6 与 [09-Hudi生产级部署与运维.md](09-Hudi生产级部署与运维.md) 的监控（读延迟/写失败）配套。
- Kafka/Debezium 背景：[../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)；姊妹书目《Kafka 权威指南》在本仓库有 .md 大纲（book/Kafka权威指南.md，文字对照）。
- 数据质量工程化：[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)。
