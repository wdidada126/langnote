# 第 7 章 流式进出 Delta Lake（Structured Streaming）

> 原书第 7 章「Streaming In and Out of Your Delta Lake」。Delta 把「同一张表既能当流 sink 又能当流 source」
> 变成核心卖点。本文件机制优先：**幂等提交 → 增量读 → 常见拓扑 → 监控与运维**。
> 所有代码为**自拟教学示意，非书中原文**；选项语义以 Databricks/delta.io 流式文档为准。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 sink 语义 | append 微批、txn action 幂等 | 流写 Delta = 一串可重放的 commit |
| 7.2 foreachBatch + MERGE | 官方推荐的 upsert 模式 | 每批一个事务，批内去重再 MERGE |
| 7.3 source 语义 | 增量读 commit、offset 即版本 | 从 VACUUM 水位之后才安全 |
| 7.4 高级选项 | availableNow、maxBytesPerTrigger、skipChangeCommits | 控制延迟、背压与脏数据 |
| 7.5 拓扑模式 | bronze→silver→gold 全是 Delta 表 | 表间流式依赖即「连续读旧表写新表」 |
| 7.6 监控运维 | 进度、积压、commit 风暴 | checkpoint 与告警指标清单 |

## 核心精讲

### 7.1 Delta 作为 sink：幂等是设计核心

```python
# 教学示意：Kafka → bronze 表，微批 append
(bronze_query = (spark.readStream
    .format("kafka").option("subscribe", "orders").option("startingOffsets", "latest")
    .load()
    .select(from_json(col("value").cast("string"), schema).alias("v"),
            col("topic"), col("partition"), col("offset"))
    .writeStream.format("delta")
    .option("checkpointLocation", "/_ckpt/bronze_orders")
    .outputMode("append")
    .table("bronze.orders")))
```

- **两阶段提交语义**：Structured Streaming 的 checkpoint 记「微批 → 来源 offset」映射；
  Delta commit 里的 **`txn` action** 记「transactionVersion → 已提交批次」。
  作业崩溃重启后，重复批次被 `txn` 识别跳过——**端到端 exactly-once 效果**（引擎侧术语：
  幂等写入；严格说是「effectively-once」，对照 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md) 的语义分层）。
- **约束**：同一 Delta 表同一时刻只应有一个 writer（多流并发写同表会触发第 2 章的并发冲突，
  `txn` 幂等只对「自己 checkpoint 重放」有效）。
- schema 演化：流表加列需 `mergeSchema=true` 或预先 ALTER；`columnType` 变更会直接失败。
- `partitionOverwriteMode` + `mode("overwrite")`：只覆盖本批出现的分区（动态分区覆盖），
  是「批式重跑某日数据」的正规姿势——默认 `static` 会清空全表，重大坑。

### 7.2 foreachBatch + MERGE：官方推荐 upsert

```python
# 教学示意：源含更新/删除的 CDC 流 → silver 表 upsert
def upsert(batch_df, batch_id):
    (batch_df.createOrReplaceTempView("micro_batch"))
    spark.sql(f"""
      MERGE INTO silver.orders t
      USING (SELECT * FROM (
               SELECT *, row_number() OVER (
                 PARTITION BY order_id ORDER BY source_ts DESC, kafka_offset DESC
               ) rn FROM micro_batch) WHERE rn = 1) s
      ON t.order_id = s.order_id
      WHEN MATCHED AND s.op = 'd' THEN DELETE
      WHEN MATCHED THEN UPDATE SET *
      WHEN NOT MATCHED THEN INSERT *
    """)

(stream.writeStream.format("delta")
   .foreachBatch(upsert)
   .option("checkpointLocation", "/_ckpt/silver_orders")
   .trigger(processingTime="1 minute")
   .start())
```

- **批内去重必须先行**（MERGE 的 ON 键重复会 cardinality violation，第 2 章 3.5）——
  按业务时间戳 + offset 取每键最新。
- foreachBatch 每批一个 Delta 事务；批失败则整批回滚（文件成为孤儿，等 VACUUM）。
- 想「一小时内只提交一次」以降 commit 频率：加大 trigger 或用
  `availableNow` + 攒批；反之高频 trigger 会把表变成「commit 风暴场」：
  日志暴涨、元数据重放变慢、下游流读压力大。

### 7.3 Delta 作为 source：增量读

```python
# 教学示意：bronze → silver 的表到表流
(silver_source = (spark.readStream.format("delta")
    .option("startingVersion", 42)          # 或 startingTimestamp；或默认从最新
    .table("bronze.orders")))               # offset 即 commit 版本区间 (start, end]
```

- **offset 模型**：微批 i 消费 commit 版本 `(start, end]`；新快照的 `add` 文件被增量读，
  被 DV 标记删除的行默认**不可见**；**remove 掉的行不会回放成 -1**。
  因此「读上游 Delta 流」拿到的是**净插入流**，不是变更日志——要变更日志请用 CDF（第 7 章文件/10）。
- 下游 checkpoint 决定安全位点：**上游 VACUUM 保留期必须 > 下游最大停摆时长**，
  否则下游重启时从旧版本增量读会报「文件缺失」。
- 🔧 `skipChangeCommits`（跳过含删除的 commit，保证不崩）、`ignoreDeletes`/`ignoreRescuedData`
  系列选项治理「上游 DML 打断下游流」——生产几乎必开一个。

### 7.4 高级选项速查

| 选项 | 用途 |
| --- | --- |
| `availableNow=true` | 把流当「有终点的批」跑完即停（回填/触发式管道，Databricks 12.2+） |
| `maxBytesPerTrigger` | 按数据量而非行数限批，背压友好（Bronze→Silver 吞吐控制） |
| `withSchemaEvolution`（DBR） | 上游加列自动跟随 |
| `skipChangeCommits` | 上游 DELETE/MERGE 产生的 commit 直接跳过而非报错 |
| `trigger(once=True)` / `availableNow` | 「流批一体」的语法糖：同一代码批模式跑 |
| `userMetadata` | 在 commitInfo 里塞业务标记，审计可读 |

### 7.5 medallion 拓扑的流式骨架（预告第 9 章）

```text
Kafka ──流写──> bronze（append，原始）
bronze ──流读+foreachBatch MERGE──> silver（清洗去重，CDC 语义）
silver ──流读+聚合──> gold（快照表：stateful agg / foreachBatch MERGE）
```

- gold 的「当前态表」两写法：无状态 `groupBy` 只能出**增量聚合**（append 累加事实）；
  要「每个客户最新汇总」得用 foreachBatch MERGE 或（DBR 13.3+ 的 materialized view/streaming table）。
- **stateful 聚合的 checkpoint 与表是两套状态**：清 checkpoint 丢窗口状态；VACUUM 过头丢输入历史——备份两侧都要管。

### 7.6 监控与运维清单

- `streaming.query.progress` 事件 → 每批 `commitVersion` 区间、输入行数、执行时长；
  接 MetricsReporter/自定义 listener 出图：**批时长 P95 > trigger 间隔 = 积压预警**。
- `DESCRIBE HISTORY` 里 operation=`STREAMING` 的连续 commit 即管道心跳；
  `operationMetrics.numInsertedRows` 可做数据量对账。
- 长停作业重启后一次性追大量 commit：考虑 `maxBytesPerTrigger` 限流，避免单批 OOM。
- 表侧配套：bronze/silver 定 OPTIMIZE 计划（流写必然产小文件，第 10 章）。

## 版本演进

| 版本 | 相关变化 |
| --- | --- |
| Delta 0.x/1.0 | readStream/writeStream 基础语义 + txn 幂等 |
| Delta 2.x | 多 outputMode 兼容、foreachBatch 成熟 |
| Delta 3.x | `skipChangeCommits`、`ignoreDeletes` 与 DV 交互；CDF 流读（第 7 章文件） |
| 🔧 DBR 13.3+ | materialized views / streaming tables（托管的增量物化，替代部分自搭管道） |

## 文献与文档

- delta.io *Delta Lake Unbounded (Streaming) Tables*；Databricks *Delta Live Tables / Streaming Tables* 文档。
- Spark Structured Streaming 指南（流式 sink 契约、`txn` 幂等的一般形式）。
- VLDB 2020 Delta 论文（流式写入的日志组织）。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「流读 Delta 能拿到 UPDATE/DELETE 事件」 | 默认净插入语义；变更事件流要开 CDF 或走第 10 章 CDC 模式 |
| 2 | 「exactly-once 是 Delta 给的」 | 是「checkpoint + txn action」的合成效果，双状态任一丢失即退化 at-least-once |
| 3 | 「trigger 越频越好」 | commit 风暴拖慢所有读者；间隔要与下游读延迟一起设计 |
| 4 | 「overwrite 模式只覆盖新分区」 | 默认 static 覆盖全表；必须显式 `partitionOverwriteMode=dynamic` |
| 5 | 「两个流可以随便写同一张表」 | 单 writer 原则；多 writer 靠 MERGE 冲突重试，不是好习惯 |
| 6 | 🔧 「ignoreDeletes 能治所有上游 DML」 | 语义细分（skipChangeCommits 等）按引擎版本核对 |

## 与其他章 / 其他书的联系

- ← `02`：txn/add/remove action 与 MERGE 语义。
- ← `04`：VACUUM 保留期决定流读安全性。
- → `08`：CDF 流读补上「变更事件」缺口；→ `10`：CDC/SCD 模式即本章 7.2 的展开。
- → `09`：gold 层聚合的完整 medallion 设计。
- → [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)：Flink/Kafka Streams 语义对照。
- → [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)：微批调优的 Spark 侧基础。
