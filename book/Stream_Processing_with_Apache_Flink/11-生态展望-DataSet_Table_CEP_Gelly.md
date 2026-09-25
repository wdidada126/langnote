# 11 生态展望：DataSet、Table API/SQL、FlinkCEP、Gelly（原书第 11 章）

> 对应原版第 11 章（中文版「还有什么？」，英文章名 ⚠️ 未从官方页逐字核实，常见写法为 "What Else Is There?"）。
> 小节范围按已核实中文目录：Flink 生态其他组成部分、DataSet API、Table API 及 SQL、FlinkCEP、Gelly、欢迎加入社区。
> **本章是全书的「指路章」**：它只给出各 API 的定位与最小示例，深入内容不在本书（第 1–10 章全部围绕 DataStream）。
> 正文逐字内容未获取，下文按该范围重写，并把后续版本的重大变化标 ⚠️
> （见 [00 总览](00-总览与阅读地图.md) 核实说明）。

## 核心概念速览（中英对照）

- **DataSet API** — DataSet API：Flink 的批处理 API（有界数据、可迭代、以算子链与物化为特征）；**已随 2.x 移除** ⚠️。
- **迭代** — iteration：`iterate`/`closeWith`（DataSet 与 DataStream 都有），面向图算法/收敛型计算。
- **Table API** — Table API：以关系表为抽象的声明式 API，可用 Scala/Java DSL 表达 select/filter/join/groupBy。
- **SQL** — Flink SQL：标准（Calcite 派生）语法层，DDL 定义源/汇表，DML 表达流式查询。
- **关系 / 表** — relation / table：「表 = 随时间变化的流；流 = 不断被更新的表」，这是 Flink 统一批流的语义核心。
- **时间属性** — time attribute：表里的 `proctime` / `rowtime` 列，让 SQL 层的窗口能按处理时间或事件时间推进。
- **目录** — catalog：表名 → 连接器/schema 的注册中心（`hive`、`default`）⚠️（原书是否展开未核实）。
- **回撤 / 更新结果** — retract / update result：流式聚合对外表现为一串「+/-」变更，是 SQL 层语义的关键差异点（13 补编）。
- **窗口 TVF** — window table-valued function：`TUMBLE/HOP/SESSION` 作为表函数写法 ⚠️（1.13+ 定型，晚于本书）。
- **FlinkCEP** — Complex Event Processing：在流上做「图案序列 + 时间约束 + 次数约束」匹配，内部用 NFA。
- **图案** — pattern：`Pattern.begin("a").where(...).next("b")...within(...)`，支持 `times`/`greedy`/`optional`/`until`。
- **非确定有限自动机** — NFA：CEP 图案的执行装置，把图案编译成状态机在每条事件上推进 ⚠️（实现细节以官方文档为准）。
- **Gelly** — Gelly API：图 API（`DataSet`/`DataStream` + 图算子、GS 迭代），与 Spark GraphX 同类。
- **FLIP** — Flink Improvement Proposal：社区设计提案机制，是理解「为什么 API 变了」的第一手来源。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 11.1 | 分层视图 | 运行时一套，API 多层：元素级（DataStream）、关系级（Table/SQL）、图级（Gelly）、图案级（CEP） |
| 11.2 | DataSet API | 批是「有界流」的特例；但两套 API 的语义差异（迭代、物化）当年仍在 |
| 11.3 | Table API / SQL | 声明式、可优化、跨批流统一；与 DataStream 可互相转换 |
| 11.4 | FlinkCEP | 补上 DataStream 不擅长的「有序多事件模式」 |
| 11.5 | Gelly | 图上迭代算法（PageRank 等），依赖 DataSet/迭代能力 |
| 11.6 | 社区 | 邮件列表、FLIP、`flink-connector-*` 独立仓库、贡献流程 |

## 核心精讲

### 11.1 一张分层图收尾全书

```
        ┌──────────── 应用 ────────────┐
        │ SQL │ Table API │ CEP │ Gelly │   ← 声明式 / 领域专用
        ├─────┴───────────┴──────┴──────┤
        │        DataStream API（本书主线）│   ← 元素级、最透明
        ├───────────────────────────────┤
        │  运行时：dataflow 图 / 任务并行 /  │
        │  事件时间 / 状态 / 检查点 / 反压   │   ← 语义都住在这里（02/03/12 章）
        ├───────────────────────────────┤
        │ 部署：standalone / YARN / K8s    │   ← 09/10 章
        └───────────────────────────────┘
```

判据（本目录反复使用的口径）：**越靠上层越省代码，越靠下层越可控**。
选型问三句：需要逐事件精细状态吗（DataStream）？能用关系代数表达吗（Table/SQL）？
需要事件序列模式吗（CEP）？

### 11.2 DataSet API：今天已是历史 ⚠️

书中定位：批处理 API，提供 `map/groupBy/join/iterate`、二次排序、哈希连接等批优化，
且与 Flink 运行时共享检查点与内存模型。示例骨架 🔧：

```java
// 🔧 旧 DataSet 写法（仅作历史对照，勿在新项目使用）
ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();   // 批的入口对象（已随 DataSet API 移除 ⚠️）
DataSet<Sale> sales = env.readTextFile("hdfs:///sales").map(SaleParser::new);
sales.groupBy("region").sum("amount").output(new DiscardingOutputFormat<>());
```

**现状**：批处理统一进 DataStream（有界流 + `checkpointing` 可选）与 Table/SQL，
DataSet API 在 1.18 标记废弃、**2.0 移除** ⚠️。今天读到这里请直接把「DataSet」当作「有界 DataStream」。

### 11.3 Table API / SQL：最小对照

```java
// 🔧 本书时代的 Table API（StreamTableEnvironment；现代为 TableEnvironment，13 补编详述）
StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);
Table clicks = tEnv.fromDataStream(clickStream);              // DataStream → 表
tEnv.registerFunction("parse", new ParseUdf());
clicks.filter("url LIKE '%/product%'")
      .groupBy("userId")
      .select("userId, cnt = count()")                         // ⚠️ 表达式 DSL 的写法跨版本变化较大
      .toAppendStream(Row.class);                              // 表 → DataStream
```

```sql
-- 🔧 SQL（DDL 在本书时代多为 registerTableSource/Sink；新版为 CREATE TABLE ... WITH (...)，见 13 补编）
SELECT userId, COUNT(*) AS cnt
FROM clicks
GROUP BY userId;
```

本章在原书里只到「能看懂、能互转」的深度；本目录把系统展开放在
[13-补编-TableAPI与SQL分层.md](13-补编-TableAPI与SQL分层.md)（⚠️ 明确标注为超出本书内容的备考补编）。

### 11.4 FlinkCEP：补上 DataStream 的短板

DataStream 擅长「一事件 ↔ 状态」，不擅长「事件序列 + 时间窗 + 次数」。CEP 的写法 🔧：

```java
// 🔧 图案：5 分钟内「登录失败 ×3 → 成功」则告警
Pattern<Login, ?> pattern = Pattern.<Login>begin("first")
    .where(e -> !e.success)
    .timesOrMore(3)
    .next("ok").where(Login::success)
    .within(Time.minutes(5));

PatternStream<Login> ps = CEP.pattern(loginStream.keyBy(e -> e.userId), pattern);
ps.process((Map<String, List<Login>> match, TimestampedCollector<Alert> out) ->
    out.collect(new Alert(match.get("ok").get(0).userId, "brute force")));
```

要点与坑（详见 [14-补编-CEP侧输出与广播状态.md](14-补编-CEP侧输出与广播状态.md)）：

- CEP 依赖事件时间水位线推进，**图案的 `within` 与作业的水位线延迟叠加**决定输出延迟；
- `times`/`optional`/`greedy`/`until` 与「跳过策略」（skip till next / after match skip）直接决定组合爆炸与否；
- 图案可通过广播流热更新（14 补编），无需重启作业。

### 11.5 Gelly 与迭代

Gelly = `Graph` 数据集 + 图算子（`runGellyWith`、PageRank、GIRCC、度量计算）。
它依赖迭代能力（批量收敛计算），因此在批侧与 DataSet 绑定更深 ⚠️（DataSet 移除后，
图相关的现代路径是把算法用迭代 DataStream 或 Table 表达 ⚠️ 未逐条核实官方结论）。

对本目录的实际意义：**第 6 章的「迭代」缺位是刻意的**——原书把迭代放在生态章，
主线（时间 + 状态）不需要它。

### 11.6 社区与演进机制

- **FLIP**（`cwiki.apache.org/confluence/flink/FLIP-*`）：每个大 API 变更都有提案，是版本差异的最权威解释来源；
- **连接器独立仓库**：`flink-connector-kafka`、`flink-connector-jdbc`、`flink-cdc` 与主仓库发版节奏不同；
- **版本策略**：1.x 长维护 + 2.x 破坏式清理（Scala API、DataSet、旧 Source/Sink）⚠️ 以官方版本公告为准。

## 版本与兼容性

| 本书内容 | 后续变化 ⚠️ |
| --- | --- |
| DataSet API | 1.18 废弃、2.0 移除；批并入有界流与 Table/SQL |
| `StreamTableEnvironment` / `registerTableSource` | 统一为 `TableEnvironment` + `CREATE TABLE ... WITH`（1.9/1.11 起渐进） |
| 窗口 SQL 用 `GROUP BY TUMBLE(...)` 时间窗口子句 | 1.13 起推荐窗口 TVF（`TABLE( TUMBLE(...))`），聚合可保留更新语义 |
| FlinkCEP | API 稳定，新增 `skipTillNextNonDuplicate`、`afterMatchSkipStrategy` 细化、SQL 层 `MATCH_RECOGNIZE` ⚠️（是否落地以版本文档为准） |
| Gelly | 更新缓慢，社区重心转移 ⚠️ |
| Scala API | 独立 Scala DataStream 层在 2.x 被削减 ⚠️ |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「Table/SQL 是另一套引擎，语义与 DataStream 不同」 | 语义（时间、状态、检查点）来自同一运行时；差别在**表达层次与优化器**，以及结果的变更形式（追加/回撤） |
| 「学了本书就能写生产 SQL 作业」 | 本书不含 SQL 正文；回撤流、upsert 主键、watermark 声明在表层都有新坑（13 补编） |
| 「CEP 就是复杂一点的 filter + 状态」 | 差别在「序列 + 时间 + 次数」的组合语义与 NFA 的状态管理；手写会退化成状态机维护地狱 |
| 「CEP 图案越复杂越智能」 | 图案组合数随 `times`/`optional` 指数增长，状态与 CPU 都会失控；先定跳过策略 |
| 「批处理需要单独的引擎」 | 在 Flink 里批 = 有界流；本书写作时才存在两套 API，今天已统一 ⚠️ |
| 「Gelly/ML 等库是运行时的一部分」 | 它们是**库**（跑在运行时上的 API），不参与运行时语义 |
| 「API 版本差异记不住就背类名」 | 更有效的是记「语义不变量」：水位线、键控状态、屏障、两阶段提交——它们跨版本都存在 |

## 与其他章 / 其他书的联系

- 11.1 的「元素级」那一层 → [05-DataStreamAPI.md](05-DataStreamAPI.md) 起全书主线。
- 11.3 的系统展开 → [13-补编-TableAPI与SQL分层.md](13-补编-TableAPI与SQL分层.md)。
- 11.4 的系统展开与广播规则 → [14-补编-CEP侧输出与广播状态.md](14-补编-CEP侧输出与广播状态.md)。
- 迭代/收敛计算与状态的关系 → [07-有状态函数与状态管理.md](07-有状态函数与状态管理.md)。
- 仓库互链：批流统一的另一种叙述见 [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)；
  表格式与流式写入的落点见 [../Use_Iceberg_with_Spark/06-维护过程与流式写入.md](../Use_Iceberg_with_Spark/06-维护过程与流式写入.md)、
  [../Apache_Hudi_Definitive_Guide/](../Apache_Hudi_Definitive_Guide/)；
  Kafka 作为 SQL 源/汇的语义见 [../深入理解Kafka与Pulsar.md](../深入理解Kafka与Pulsar.md)。
