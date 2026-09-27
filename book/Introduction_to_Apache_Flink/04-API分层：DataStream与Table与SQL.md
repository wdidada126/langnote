# 04 API 分层：DataStream、Table API 与 SQL

> ⚠️ **重构章声明**：原书真实目录未取得（取证链见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 本章按「入门书必有的 API 地图章」重构。✅ 概念锚（实测 200）：
> `https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/concepts/overview/`、
> `https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/overview/`。
> **本册只画分层图与选型逻辑，不抄 API 细节**——写法一律转姊妹册
> [../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md](../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md)。

## 本章地图

1. 三层金字塔：ProcessFunction（原语）→ DataStream（算子库）→ Table/SQL（声明式）。
2. 流与表的二象性：同一数据的两种投影。
3. 回撤流/upsert 流：声明式层为什么需要「修正过去」的记录形态。
4. 选型：什么时候值得下沉一层。

## 核心精讲

### 1. 三层金字塔（自上而下 = 声明式 → 命令式）

| 层 | 抽象单位 | 时间/状态暴露 | 典型用户 |
| --- | --- | --- | --- |
| SQL | 表/列/查询 | 隐藏（watermark 由 DDL 声明） | 分析师、跨团队复用 |
| Table API | 关系代数算子 | 半隐藏（窗口 TVF） | 应用开发 |
| DataStream | 算子 + keyed state | 全暴露（timestamp/watermark/state 手动） | 平台/复杂语义 |
| ProcessFunction | 单事件回调 + Timer | 一切自己写 | 兜底原语 |

✅ 官方 DataStream→Table→SQL 的分层叙述见 table/concepts/overview 页。⚠️ 2022 书时代还常提 DataSet API（批），
1.18/2.x 演进后**批已并入 DataStream/Table 双模式**（见 06 章演进）。

### 2. 流 = 表的变更日志；表 = 流的物化

- 一条 SQL `GROUP BY` 在批里是「一次算完」，在流里是「每来一条修正一行输出」。
- 🔧 类比（SQLite 3.45.3，非 Flink 行为）：01 章 D3 的「逐条 UPSERT 维护 `state(uid,cnt)`」
  就是 `SELECT uid, COUNT(*) FROM clicks GROUP BY uid` 的**流式物化形态**——
  同一查询、两种执行哲学：重算（批，32 ms 一把梭）vs 维护（流，逐条 125 ms 摊到到达时刻）。
- 概念出处：[../Streaming_Systems/06-流和表.md](../Streaming_Systems/06-流和表.md)（duality 的正式论证）；
  产品化形态即物化视图/连续查询：[../Streaming_Databases/04-物化视图.md](../Streaming_Databases/04-物化视图.md)。

### 3. 记录形态的进化：append → retract → upsert

- append-only：只有 INSERT，聚合结果流「每个修正都是新行」——下游必须能处理回撤。
- **回撤流 retract stream**：`-U/+U` 成对出现，语义完备但下游难做。⚠️ 转述官方 changelog 表述。
- **upsert 流**：带主键的「以新覆盖旧」，工程上比回撤好落地，是 CDC/入湖的主流形态。
- 谱系对照：Paimon 的 changelog 生成机制就是「把 Flink 回撤流翻译成表格式可存储的形态」：
  [../Apache_Paimon_Streaming_Lakehouse/07-Changelog生成机制.md](../Apache_Paimon_Streaming_Lakehouse/07-Changelog生成机制.md)（盘上已验名）。

### 4. SQL 在 Flink 里的三重身份

1. **交互查询语言**（不是查询引擎！Flink SQL 无 ad-hoc 亚秒交互定位）⚠️ 与 Trino 类引擎的分工见
   [../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md](../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md)（盘上实名已验）。
2. **流作业的声明式接口**：DDL 里定义 watermark/主键/连接器——把 02/03 章概念「配置化」。
3. **流批统一入口**：同一查询在 streaming/batch 两种 runtime 下合法（2.x 单 planner 的方向，⚠️ 通说）。

### 5. 一张「能力 vs 抽象」对照表（选型前的最后半小时）

| 能力 | DataStream | Table/SQL | 备注 |
| --- | --- | --- | --- |
| 逐事件定时器/侧输出 | ✅ 原生 | ⚠️ 有限（SQL 无 ProcessFunction 等价物） | 02 章概念的直接落点 |
| 窗口聚合/Regular Join | ✅ 手写 | ✅ 声明式 | planner 优化空间在 SQL 侧 |
| Interval Join / CEP | ⚠️ 手写状态 | 部分 TVF/扩展库 | CEP 走独立库（姊妹册 14 补编） |
| 状态 TTL/清理策略 | ✅ 显式 | ⚠️ 由 planner 推导 | 排障时差异巨大 |
| UDF 体系 | 函数即代码 | 标量/聚合/表函数三类 | ✅ SQL 概览页 |
| 可治理性（血缘/审计） | ⚠️ 靠自觉 | ✅ 文本即资产 | §6 决策树的组织变量 |

### 6. 选型决策树（本册「概念向」的收敛点）

```
需要逐事件定制计时/乱序侧输出?  ─是→ ProcessFunction/DataStream
   │否
聚合/join/窗口可用关系语义表达? ─是→ Table API/SQL
   │否(模式匹配类)
→ CEP 库(姊妹册 14 补编) ── 或把状态推给外部系统(03 章 §1)
```

- 平台团队经验法则 ⚠️ 转述：SQL 是**资产**（可治理、可血缘、可复用），DataStream 是**代码**（能力强、负债也强）；
  组织内流作业规模化后，重心必然移向 SQL——这正是 Materialized Table 出现的需求土壤（06 章）。

### 7. 概念对位（谱系四角之「API 视角」）

| 主题 | 本章 | 互链（写前 ls/Glob 验名 ✅） |
| --- | --- | --- |
| DataStream 写法 | §1 | [../Stream_Processing_with_Apache_Flink/05-DataStreamAPI.md](../Stream_Processing_with_Apache_Flink/05-DataStreamAPI.md) |
| Table/SQL 分层细节 | §3 | [../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md](../Stream_Processing_with_Apache_Flink/13-补编-TableAPI与SQL分层.md) |
| 流表二象性语义 | §2 | [../Streaming_Systems/06-流和表.md](../Streaming_Systems/06-流和表.md)、[../Streaming_Systems/08-流式SQL.md](../Streaming_Systems/08-流式SQL.md) |
| 流式 SQL 产品语境 | §4 | [../Streaming_Databases/09-流式平面.md](../Streaming_Databases/09-流式平面.md) |

## 常见误区

1. 「Flink SQL = Spark SQL 换个皮」：changelog 语义（回撤/upsert）是 Flink SQL 类型系统的**一级公民**，
   ⚠️ 转述；批式 SQL 引擎普遍无此形态。
2. 「Table API 性能一定比 DataStream 好」：planner 优化的是关系算子链；不恰当中转 changelog 反而增加开销 ⚠️。
3. 「SQL 里不用管 watermark」：DDL 的 `WATERMARK FOR` 子句就是 watermark 声明处——不懂 02 章配不出来。
4. 「upsert 流 = 幂等写」：覆盖写幂等 ✅，但**聚合回撤的正确性**（-U 何时来）仍依赖 03 章的快照协议。
5. 「DataStream 是低级所以过时」：ProcessFunction 仍是所有侧写/定时器语义的兜底层 ✅ 官方分层图至今保留。

## 核心概念速览（中英对照）

- **分层 API** — layered API stack：ProcessFunction→DataStream→Table→SQL 逐级声明化。✅
- **流表二象性** — stream-table duality：流是未物化的表变更史，表是已物化的流快照。
- **变更日志** — changelog：+I/-U/+U/-D 四类记录的流形态，声明式层正确性的载体。⚠️
- **回撤流** — retract stream：携带「撤回旧值」的记录流，下游需支持删除。
- **upsert 流** — upsert stream：主键覆盖流；CDC/入湖的事实形态。
- **物化视图** — materialized view：连续查询的产品化名（04 章对位 Streaming_Databases）。
- **窗口 TVF** — window table-valued function：SQL 中 `TUMBLE(...)` 等以表函数表达窗口。✅（SQL 概览页）
- **连接器 DDL** — connector DDL：SQL 用元数据声明源/汇、watermark、主键。
- **规划器** — planner：Table/SQL 到算子图的翻译优化层；2.x 方向为流批单 planner ⚠️。
- **处理函数** — ProcessFunction：逐事件 + Timer 的最低层原语。
- **类型系统对齐** — type bridging：DataStream POJO 与 SQL 逻辑类型的互转，changelog 标记随类型流动 ⚠️。

## 最新演进与工业实践

- ✅ **Materialized Table（1.18 预览 → 2.x 文档成篇）**：`CREATE MATERIALIZED TABLE ... WITH (
  'refresh-mode'='continuous'|'full', 'freshness'='...' ) AS SELECT ...`——把「流作业 or 定时批重算」
  的选择交给**声明的保鲜度**，DDL 自动物化查询；官方文档：
  `https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/table/materialized-table/overview/`（实测 200；
  语句示例细节未从正文逐字核实，⚠️ 仅按可达页面+社区通说转述）。
- ⚠️ 通说：**Flink 2.0 统一 planner**、批模式回归 DataStream/Table 正统（DataSet API 退场），
  「流批一体」从营销词变成类型系统层事实；✅ 版本根页实测 200：flink-docs-release-2.0/。
- **生态现状**：Flink SQL Gateway / SQL Client 产品化、Catalog（Hive/Paimon/JDBC）打通元数据 ⚠️ 转述；
  盘上治理线对照：[../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md](../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md)（已验名）。
- **工业选型实践** ⚠️ 转述：国内大厂实时数仓分层（ODS/DWD/DWS 全部 Flink SQL + Paimon）已成主流范式，
  DataStream 只留给 CEP/自研连接器；对读 [../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md](../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md)。
- **兄弟书挂点（只登记不链）**：`Advanced_Analytics_with_Spark_2e/`（#195，未落盘）——Spark SQL 与 Flink SQL
  的 changelog 语义差是天然对照题，本册 §3/误区 1 已备好挂点。
