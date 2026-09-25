# 11 Flink 集成与 CDC 入湖实践：流式湖仓的工程主场

> 《Apache Paimon 官方文档与源码精读》第 11 章。主源：文档 "Engine Flink"（SQL Jars / Action /
> Query / Write）与 "CDC Ingestion"（MySQL / Kafka / Pulsar / 整库同步）板块。Paimon 的 Flink
> 集成不是"有个 connector"，而是格式围绕 Flink 协议设计——本章把这些绑定落到可抄的管线上。

## 核心概念速览（中英对照）

- **入湖 Action** — Flink Action Job：`paimon-flink-action`  fat-jar 提交的专用作业（mysql 同步表/库、compact、rollback 等）。
- **整库同步** — Database Ingestion：一个作业把上游 MySQL 库的 N 张表同步为 N 张 Paimon 表，含 schema 自动跟随 🔧。
- **Pipeline YAML** — Flink CDC 3.x 管道定义：source/sink/pipeline 三段式 YAML 声明入湖链路 🔧。
- **schema 演进动作** — Schema Evolution Actions：对上游加列/改类型的处理策略（加列跟随/忽略/报错）。
- **启动模式** — Startup Mode：initial（全量+增量）、latest-full、from-snapshot/timestamp、compact-offsets 等 CDC 起点语义。
- **全量增量无感切换** — Lock-free 全量读取：CDC source 无锁一致性快照后接 binlog，Paimon 侧同一 sink 承接。
- **日志复制入湖** — Log Duplicating：Kafka 原文双写湖表供回溯/共享，湖不替代秒级总线（01.3）。
- **级联作业** — Chained Jobs：以 Paimon 表为中间层的 Flink 作业链，替代 Kafka 中间 topic。
- **计算引擎下推** — 源侧过滤/并行读取：入湖链路的裁剪与分片（分片大小、server-id 隔离）。
- **部分更新入湖** — 多库多表合表：不同分库分表 → 同一下游主键表的汇聚写模式。
- **两阶段落地** — 提交随检查点：入湖作业的可见性节拍=Flink checkpoint（第 05 章）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 11.1 | Flink 侧部署形态：jar/catalog/SQL | 一切从 bootstrap 包与 catalog 开始 |
| 11.2 | 单表同步 mysql-sync-table | 入门链路，理解 startup/撤回/桶 |
| 11.3 | 整库同步与 schema 演进 | 生产主力：YAML/Action 双形态 |
| 11.4 | 级联作业：湖表当流中间层 | 省 state、可回溯、可重放 |
| 11.5 | 端到端参考架构与参数表 | ODS→DWD→OLAP 一表多吃 |

## 精讲

### 11.1 部署三件套

🔧 官方快速开始口径：

```bash
# 1) 依赖：paimon-flink-<版本> 与 paimon-flink-action fat-jar 放入 Flink lib 或用 -jar 指定
# 2) catalog 注册（SQL 侧）
CREATE CATALOG my_paimon WITH (
  'type' = 'paimon',
  'metastore' = 'hive',              -- 或 filesystem/jdbc/REST（第 12 章）
  'warehouse' = 'hdfs:///warehouse',
  'hive.metastore.uris' = 'thrift://:9083'
);
USE CATALOG my_paimon;
# 3) Action 作业
bin/flink run -c org.apache.paimon.flink.action.MySqlSyncTableAction \
  paimon-flink-action.jar ...
```

SQL 操作面覆盖：CTAS、`INSERT INTO/OVERWRITE`、UPDATE/DELETE（主键表）、`CALL sys.*` 过程族
（tag/branch/rollback/rewrite 等）、system-table 查询（04.5）。1.x 起 SQL 能力面与 Spark 大体对齐，
差异以文档 Engine 页为准 🔧。

### 11.2 单表：mysql-sync-table 解剖

链路：`MySQL 表 →(CDC source：全量快照→binlog 增量)→ Paimon 主键表`。

- **主键**：默认取上游 PK；上游无 PK 则必须显式 `--primary-keys`；
- **分桶**：`--bucket` 显式指定（固定桶是默认推荐；省略时的行为与并行度关系以文档为准，按 2.3 决策）🔧；
- **changelog**：CDC 输入天然完整 → `--changelog-producer input` 或干脆表侧配 input（07.3 的"白送午餐"）；
- **启动模式**：`--startup-mode initial`（默认，先全量后 binlog）/ `latest-full` / `specific-offset`（timestamp）等；
- **一致性**：全量阶段无锁分片读（读一致性由 Flink CDC 的快照机制保证），与增量衔接处按
  binlog offset 回放收敛——**同键重复/旧覆盖新由 Paimon 主键 + sequence 兜底**（第 02/06 章）。

### 11.3 整库同步与 schema 演进

两种形态（同一能力面，🔧 版本以文档为准）：

```yaml
# Flink CDC 3.x Pipeline YAML → Paimon sink（新版推荐）
source:
  type: mysql
  tables: app_db.\.*          # 正则多表/整库
  server-id: 5400-5404
sink:
  type: paimon
  catalog.properties.metastore: hive
  catalog.properties.warehouse: hdfs:///warehouse
pipeline:
  name: MySQL to Paimon Pipeline
  parallelism: 2
```

- 自动建表：每张上游表映射一张 Paimon 主键表（库.表 → catalog.db.table）；
- schema 跟随：加列/加表（新表自动出现？取决于版本与 `include` 策略）可配 `schema_evolution` 动作；
  **类型收窄/删列等危险变更**按第 04 章的 schema 规则拒绝或告警；
- 旧形态 Action：`MySQLSyncDatabaseAction`（分库分表合并同步、`--assigners` 等）仍在维护窗口 🔧；
- 运维红线：分库分表**合表**时确认分片键不冲突（全局主键）；server-id 范围与其他 CDC 作业互斥；
  表数多时单作业并行度与 checkpoint 时长同步膨胀——大库拆分批是常见解法。

### 11.4 级联作业：中间层落湖的三重红利

传统：`A 作业 → Kafka 中间 topic → B 作业`。Paimon 版：`A → Paimon 表 →（流读）B`。

1. **状态瘦身**：B 不再为"中间结果"维护巨大 join/agg state——A 已把变更物化进湖，B 的 state
   只剩自身算子所需（维表侧更是直接 lookup join，8.5）；
2. **可回溯可重放**：中间层带快照历史 + consumer-id，B 出问题可指定位点重放（Kafka topic 的保留期
   换成湖的 tag/快照策略，第 10 章）；
3. **一写多读**：同一中间层再挂批读/OLAP/新流消费者，无需像 Kafka 那样按消费组复制存储。

代价：每一跳多出"检查点节拍 + compaction 节拍"两级延迟；**全链路新鲜度预算要逐跳累加**——
这正是 01.5 边界表里"秒级链路留 Kafka"的量化理由。

### 11.5 端到端参考架构

```text
业务 MySQL ─CDC(YAML 整库)→ Paimon ODS(主键表, changelog=input)
   │                              │ 流读 changelog
   │                              ▼
Kafka 日志 ──追加表 ODS────→ Flink 清洗/打宽 → Paimon DWD(主键表, partial-update, lookup)
                                                  │ 流读/ro 读
                                                  ▼
                              Paimon DWS(aggregation) → StarRocks/Doris 直读(第 12 章)
```

- ODS：input producer（白送）、固定桶按压测、daily tag 锚批；
- DWD：partial-update 打宽替代双流 join；lookup changelog 喂 DWS；
- DWS：aggregation 引擎预聚合 + deletion vectors 供交互查询免合并；
- 每张表都有：consumer-id 命名规范 + `$snapshots/$files` lag 巡检脚本（第 04/09 章处方）。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "CDC 入湖 = 表结构复制 + 数据搬运" | 关键在语义对齐：撤回流、startup 衔接、schema 演进策略、桶/producer 表设计——搬运只是 20% |
| "整库同步一劳永逸" | 上游加表/删表/改类型时策略差异巨大（自动跟随 vs 忽略 vs 中断），要按变更矩阵演练 🔧 |
| "级联作业延迟和 Kafka 链路一样" | 多了检查点+合并两拍；对延迟敏感的跳保留 Kafka（11.4 代价条）|
| "Flink 版绑定不会变" | Paimon 对 Flink 大版本（1.16/1.18/1.20/2.x）兼容随版本发布，升级要同时看两边矩阵（🔧 以 Releases 页为准）|
| "CDC 作业挂了重启会丢 binlog" | 位点在 checkpoint 里；真正常见的是**state 兼容失败**导致要从 initial 重放——整库同步作业尽量单表/小批分组部署以降低爆炸半径 |

## 与其他章 / 其他笔记的联系

- 提交/两阶段 → [05-写入路径与提交协议.md](05-写入路径与提交协议.md)；changelog 模式选择 → 07；
  维表连接 → 08.5；表设计三参数（桶/序列/producer）→ 02/06/07。
- Flink checkpoint 与撤回流基线 → [../基于Apache_Flink的流处理.md](../基于Apache_Flink的流处理.md)、
  [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)；
  Kafka/Debezium 接入基线 → [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)、
  [../Kafka权威指南.md](../Kafka权威指南.md)。
- Hudi Streamer 同类问题（摄取框架）对照 → [../Apache_Hudi_Definitive_Guide/08-基于HudiStreamer构建数据湖仓.md](../Apache_Hudi_Definitive_Guide/08-基于HudiStreamer构建数据湖仓.md)；
  CDC 模式读对照 → [../Apache_Hudi_Definitive_Guide/04-从Hudi读.md](../Apache_Hudi_Definitive_Guide/04-从Hudi读.md)；
  Delta Structured Streaming 源/汇对照 → [../Delta_Lake_Definitive_Guide/06-流处理-Structured-Streaming.md](../Delta_Lake_Definitive_Guide/06-流处理-Structured-Streaming.md)；
  Iceberg 的 Flink 实战 → [../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md](../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md)。
- 增量管线工程化 → [../Engineering_Lakehouses_with_Open_Table_Formats/10-增量管线与CDC.md](../Engineering_Lakehouses_with_Open_Table_Formats/10-增量管线与CDC.md)。

## 本章记忆桩

```text
三层绑定：协议层（checkpoint 即提交）、语义层（producer=input 接 CDC）、工程层（级联作业替 topic）。
入湖选型一问：下游要 -U 吗？ 要 → 建表时 producer 与 merge engine 就定了（06.5 矩阵）。
新鲜度预算：端到端 = Σ(检查点节拍 + 合并节拍 + 传输)——逐跳记账，别拿 Kafka 期望套湖。
```
