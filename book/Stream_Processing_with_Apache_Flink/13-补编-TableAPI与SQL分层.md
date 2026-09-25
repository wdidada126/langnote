# 13 补编：Table API / SQL 与 DataStream 的分层映射

> ⚠️ **性质声明**：《Stream Processing with Apache Flink》**没有** Table API/SQL 正文章节。
> 原书对它的唯一提及是第 11 章的「Table API 及 SQL」小节（已核实目录），只给定位与最小示例
> （见 [11 章](11-生态展望-DataSet_Table_CEP_Gelly.md)）。本文件按任务要求补足这条主线
> （DataStream → Table/SQL 两层 API 的映射），内容依据 Flink 官方 Table/SQL 文档整理，
> **凡涉及具体版本行为处均标 ⚠️，落生产前请对照所用版本文档**。核实说明见 [00 总览](00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **表环境** — TableEnvironment：Table/SQL 的入口对象，统一管理 catalog、配置与类型系统（批流合一后取代 `StreamTableEnvironment` ⚠️）。
- **关系** — relation / Table：对「会随时间变化的行集合」的声明，可翻译为 dataflow 图（03 章）。
- **模式 / schema** — schema：列名 + 类型 + 约束（主键）+ 元数据列 + 时间属性的声明。
- **时间属性** — time attribute：`PROCTIME()` 计算时间属性列；`ROWTIME`/带 watermark 的列为事件时间属性，是窗口与 join 能按时间推进的前提。
- **水位线声明** — watermark declaration：`WATERMARK FOR ts AS ts - INTERVAL '5' SECOND`，等价于 DataStream 侧的时间戳分配 + 水位线生成（06 章）。
- **主键 / upsert 键** — primary key / upsert key：决定结果表的变更形式能否被 sink 消化（回撤 vs 更新）。
- **追加流** — append-only stream：只有 `+I` 事件的结果，源本身不更新时最常见。
- **回撤流** — retract stream：结果带 `+I/-U/+U`（插入、撤回旧值、更新新值），流式聚合的默认形态。
- **更新插入** — upsert（`+I/+U/-D`）：有主键时以键为单位的变更形式，需要支持主键的 sink。
- ** changelog / 变更日志** — changelog stream：把表表达为「变更事件的流」，这是 Flink 统一批流的语义基础。
- **窗口子句 vs 窗口 TVF** — group window vs window table-valued function：老写法 `GROUP BY TUMBLE(ts, INTERVAL '1' MINUTE)`；
  新写法 `FROM TABLE(TUMBLE(TABLE t, DESCRIPTOR(ts), INTERVAL '1' MINUTE))` ⚠️（1.13 起推荐）。
- **_over window_** — over window：按时间/行的滑动累计（`SUM(cnt) OVER (PARTITION BY uid ORDER BY ts ROWS BETWEEN ...)`）。
- **正则匹配识别** — `MATCH_RECOGNIZE`：SQL 层的 CEP 表达 ⚠️（落地版本与完整度以官方文档为准，见 14 补编）。
- **连接器 DDL** — `CREATE TABLE ... WITH ('connector'='kafka', ...)`：把物理世界声明成表；格式与 upsert 材料化选项都在这里。
- **物化 / 材料化** — materialization：把带主键的变更流落到能覆盖写的外部系统（ES/JDBC/数据湖）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 13.1 | 分层与互转 | 表层最终编译成同一张 dataflow 图；转换点是 `fromDataStream`/`toChangelogStream` |
| 13.2 | 类型与 schema 映射 | DataStream 的类型 ↔ 表列；时间戳/水位线如何跨层传递 |
| 13.3 | 时间语义映射 | 06 章的三件套（时间戳、水位线、窗口）在 SQL 里的对应写法 |
| 13.4 | 变更形式 | 追加 / 回撤 / upsert 三种流形态决定 sink 选型，这是最陌生的部分 |
| 13.5 | 状态与容错 | 表层不改变容错语义：检查点、精确一次仍来自运行时（12 补编） |
| 13.6 | 何时下沉到 DataStream | 逐事件状态机、计时器、侧输出、CEP、异步 IO 仍是 DataStream 的地盘 |

## 核心精讲

### 13.1 一张映射表：同一语义的两种写法 ⚠️（API 名称随版本）

| 语义 | DataStream（本书主线） | Table / SQL |
| --- | --- | --- |
| 入口 | `StreamExecutionEnvironment` | `TableEnvironment`（内部持有 env） |
| 源 | `env.addSource(KafkaSource)` | `CREATE TABLE k (...) WITH ('connector'='kafka')` |
| 过滤 | `.filter(_ > 0)` | `WHERE v > 0` |
| 投影/改名 | `.map(...)` | `SELECT a, b+c AS d` |
| 按键分区 | `.keyBy(...)` | `GROUP BY` / `PARTITION BY` / join 的等值键 |
| 增量聚合 | `.aggregate(AggregateFunction)` | `SUM/COUNT/AVG` 聚合函数 |
| 窗口 | `.window(TumblingEventTimeWindows.of(...))` | `TUMBLE`/`HOP`/`SESSION`（子句或 TVF） |
| 水位线 | `WatermarkStrategy`/assigner | `WATERMARK FOR col AS col - INTERVAL ...` |
| 双流连接 | `intervalJoin`/`CoProcessFunction` | 时间限定 join、窗口 join、`MATCH_RECOGNIZE` ⚠️ |
| 侧输出 | `OutputTag` + `getSideOutput` | 无直接对应：常见做法是加一列标记再 `WHERE` 拆表 |
| 计时器 | `onTimer` | 无直接对应；`interval join` 或下沉到 DataStream |
| 状态 | `ValueState/MapState` | 由算子自动持有（聚合状态、join 状态），用户不显式声明 |
| 拓扑身份 | `uid()` | ⚠️ 表作业的算子 uid 生成有专门机制（`table.exec.state-processor` / 自动 uid 追踪，名称以版本为准） |

🔧 互转骨架（Scala/Java 混合示意）：

```java
// 🔧 表 → 流（追加）
Table result = tEnv.sqlQuery("SELECT uid, COUNT(*) c FROM clicks GROUP BY uid");
DataStream<Row> appended = tEnv.toAppendStream(result, Row.class);   // ⚠️ 老 API；新版为 toDataStream / toChangelogStream

// 🔧 流 → 表（带事件时间属性：时间戳与水位线必须在 DataStream 侧先分配好）
tEnv.createTemporaryView("clicks", keyedStream, Schema.newBuilder()
    .columnByExpression("wc", "WATERMARK FOR ts AS ts - INTERVAL '5' SECOND")   // ⚠️ DSL 形态以版本为准
    .build());
```

### 13.2 类型与 schema 映射的三条硬规则

1. **只有一等类型能上表**：POJO / case class / Tuple / `Row` / `RowData` 可自动推断；
   第三方类型进表要显式 `DataTypes` 声明（对应 05 章的类型信息一节）。
2. **raw 类型与结构化类型的取舍**：现代写法倾向「DataStream 用 POJO，表层用结构化类型」；
   `RAW` 类型在跨语言 UDF 与某些算子上受限 ⚠️。
3. **时间列必须是 `TIMESTAMP(3) / TIMESTAMP_LTZ(3)`** 且精度与连接器格式一致，
   否则 `WATERMARK FOR` 会在校验期报错（而不是运行期）。

### 13.3 时间语义在表层的等价写法 🔧

```sql
-- 🔧 对应 06 章「每 5 分钟滚动窗口按键计数」
CREATE TABLE clicks (
  uid STRING,
  ts  TIMESTAMP(3),
  WATERMARK FOR ts AS ts - INTERVAL '5' SECOND          -- = 分配时间戳 + 生成水位线
) WITH ('connector'='kafka', 'topic'='clicks', 'format'='json');

SELECT window_start, uid, COUNT(*) AS c
FROM TABLE(TUMBLE(TABLE clicks, DESCRIPTOR(ts), INTERVAL '5' MINUTE))   -- 窗口 TVF 写法 ⚠️
GROUP BY window_start, window_end, uid;
```

处理时间的对应：`pt AS PROCTIME()` 计算列 + 按 `pt` 开窗；
**注意**：`PROCTIME()` 在表层是按算子所在机器定义的，与 02 章「处理时间不可复现」的告诫完全一致。

### 13.4 变更形式：本章真正的新概念

| 查询形态 | 结果流类型 | 可用 sink |
| --- | --- | --- |
| 纯投影/过滤/无聚合 join | 追加（`+I`） | Kafka、文件、任何 append sink |
| `GROUP BY` 聚合（无主键声明） | 回撤（`-U/+U`） | 需回撤能力：Print/部分 sink；直接写 Kafka 会报错 ⚠️ |
| 聚合 + 声明主键 | upsert（`+I/+U/-D`） | 支持主键覆盖写的 sink（ES/JDBC/数据湖/Cassandra） |
| 带 `HAVING`/去重的更新流 | 回撤 | 同上 |

🔧 常见组合（示意）：

```sql
CREATE TABLE agg_out (
  uid STRING,
  c   BIGINT,
  PRIMARY KEY (uid) NOT ENFORCED          -- NOT ENFORCED：Flink 不做校验，只用于路由与 sink 语义 ⚠️
) WITH ('connector'='upsert-kafka', 'key.format'='json', 'value.format'='json');

INSERT INTO agg_out SELECT uid, COUNT(*) FROM clicks GROUP BY uid;   -- 回撤流被自动转成 upsert
```

三个坑（与 06 章的迟到对照着记）：

- **回撤流写只接受追加的 sink 会失败**，报错常发生在运行期而非校验期（版本差异 ⚠️）。
- **聚合状态不会自动过期**：`table.exec.state.ttl` 决定无更新键的状态何时清理，
  不设就是「无限增长的 MapState」（对应 07 章 7.6 的状态泄漏防线）。
- **late data 在表层由 watermark 决定窗口结束**：迟到事件默认丢弃，没有 `sideOutputLateData` 的显式出口 ⚠️。

### 13.5 表层不改变容错语义

记住三点即可（原理见 [12 补编](12-补编-检查点机制与分布式快照.md)）：

1. SQL 作业同样靠屏障 + 对齐 + 全局回滚，检查点参数（10 章 10.5）原样适用；
2. 精确一次仍要求**可重放源 + 支持事务的汇**；`exactly-once` 的 Kafka sink 需要事务 ID 前缀与合理的 `transactional.id.expiration.ms` 关系 ⚠️；
3. 保存点升级对 SQL 作业的痛点是**算子 uid 稳定性**：改写一条 SQL 可能改变生成的算子图，
   从而让旧状态无法映射（各版本提供了 uid 生成/追踪机制，名称与默认值 ⚠️ 以版本文档为准）。

### 13.6 什么时候必须回到 DataStream

| 需求 | 为什么表层不合适 |
| --- | --- |
| 精细的逐键状态机（多状态 + 交叉清理） | SQL 只有聚合/join 的隐式状态，表达不出「删除这个键的这条记录」 |
| 计时器驱动的告警/超时 | `MATCH_RECOGNIZE` ⚠️ 覆盖有限，`onTimer` 更直白 |
| 侧输出分流脏数据 | 需要 `OutputTag` |
| 异步 I/O 富化外部维表 | 需要 `AsyncFunction`（08 章 8.6）；表层的异步 lookup join ⚠️ 需版本与连接器支持 |
| 复杂图案 CEP | 见 14 补编 |
| 自定义窗口/触发器 | 需要 `WindowAssigner`/`Trigger`（06 章） |

## 版本与兼容性 ⚠️

- `StreamTableEnvironment` / `BatchTableEnvironment` → 统一 `TableEnvironment`（1.10 起）；
- `toAppendStream/toRetractStream` → `toDataStream/toChangelogStream` + `fromDataStream`（1.14+ 的 DataStream 集成重写）；
- 规划器：legacy → Blink（1.12 起默认）；旧文档中的 `blink` 开关现已无意义；
- SQL 客户端 `bin/sql-client.sh`、YAML 定义的 pipeline（`flink-sql-gateway`）均晚于本书；
- 窗口 TVF（`TUMBLE`/`HOP`/`SESSION` 作为表函数）1.13 引入；`GROUP WINDOW` 子句被弃用 ⚠️。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「SQL 是独立引擎，语义与 DataStream 不同」 | 同一运行时（03 章）；语义差别只在「结果表达为变更流」与「状态由算子自动持有」 |
| 「`COUNT(*)` 的结果就是每个键一行」 | 它是回撤流：同一键会不断发 `-U/+U`，落到 append sink 会变成历史堆积或报错 |
| 「主键声明了就有约束校验」 | `NOT ENFORCED` 意味着 Flink 不校验唯一性，只用它决定变更形式与分区路由 |
| 「设了 watermark 列就自动丢迟到」 | 窗口结束由 watermark 驱动，迟到事件是否影响结果取决于算子实现；默认表现为「不再更新已关闭的窗口」 |
| 「改一条 SQL 不影响状态」 | 生成拓扑与算子 uid 可能变，导致保存点里的状态无处安放（13.5） |
| 「表层的 `state.ttl` 就是检查点 TTL」 | 它是**算子状态过期**，与检查点保留策略、连接器提交周期无关 |
| 「SQL 作业不需要反压调优」 | 反压机制完全相同（02 章），表层多出的风险是聚合状态过大导致的对齐等待 |

## 与其他章 / 其他书的联系

- 13.1/13.2 的类型体系源头 → [05-DataStreamAPI.md](05-DataStreamAPI.md)。
- 13.3 的时间三件套在元素层的写法 → [06-时间与窗口算子.md](06-时间与窗口算子.md)。
- 13.4 的状态与 TTL 概念对应 → [07-有状态函数与状态管理.md](07-有状态函数与状态管理.md)。
- 13.5 的端到端一致性与事务 sink → [08-读写外部系统.md](08-读写外部系统.md)。
- 原书中 Table/SQL 的原始位置（仅一小节）→ [11-生态展望-DataSet_Table_CEP_Gelly.md](11-生态展望-DataSet_Table_CEP_Gelly.md)。
- 仓库互链：与表格式（Iceberg/Hudi）的流式写入结合 →
  [../Use_Iceberg_with_Spark/06-维护过程与流式写入.md](../Use_Iceberg_with_Spark/06-维护过程与流式写入.md)、
  [../Apache_Hudi_Definitive_Guide/](../Apache_Hudi_Definitive_Guide/)、
  [../湖仓架构大规模数据平台的设计和实现/](../湖仓架构大规模数据平台的设计和实现/)；
  Spark 侧的结构化数据层对照 → [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)；
  批流统一的历史叙述 → [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。
