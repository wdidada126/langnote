# 03 数据读写与 MERGE INTO

> 章题为推断（见 [00 总览](00-总览与阅读地图.md) 声明段）。本章是 report 的实操心脏：
> DataFrame/SQL 两条路读写 + upsert 模式。语法核对自官方
> [Spark Writes](https://iceberg.apache.org/docs/latest/spark-writes/) 与
> [DDL](https://iceberg.apache.org/docs/latest/spark-ddl/) 文档。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 | 建表与基本读写 | `CREATE TABLE ... USING iceberg`；SQL 与 DataFrame 双轨 |
| 3.2 | V2 写 API | `df.writeTo(t).append()/.replace()/.create()` 是首选 |
| 3.3 | 行级变更 | UPDATE/DELETE 需要 v2 表；提交即新快照 |
| 3.4 | INSERT OVERWRITE 与动态分区覆盖 | 忘开 `partitionOverwriteMode=dynamic` 会清全表 |
| 3.5 | MERGE INTO 与 upsert 模式 | 一个语句完成 CDC 入湖；`WHEN NOT MATCHED BY SOURCE` 需 extensions |
| 3.6 | Copy-on-write vs merge-on-read | 写放大 vs 读放大的权衡，三档表属性 |

## 核心精讲

> 以下 SQL/代码均为**教学示意，不参与构建**；catalog 名 `wh` 假定已按 02 章配置。

### 3.1 建表与基本读写

```sql
-- 教学示意
CREATE TABLE wh.demo.orders (
  order_id  BIGINT,
  customer  STRING,
  amount    DECIMAL(12,2),
  ts        TIMESTAMP
) USING iceberg
PARTITIONED BY (days(ts))            -- 隐藏分区：分区表达式，不是列（05 章细讲）
TBLPROPERTIES ('format-version' = '2');

INSERT INTO wh.demo.orders VALUES (1, 'alice', 99.90, TIMESTAMP '2025-01-01 08:00:00');
SELECT count(*) FROM wh.demo.orders;
```

### 3.2 V2 写 API（DataFrame）

Spark DataSource V2 的 `TableWriter` API 是官方推荐姿势，语义自明且天然带原子提交：

```python
# 教学示意（PySpark）
df.writeTo("wh.demo.orders").append()               # 追加，一次作业一个快照
df.writeTo("wh.demo.orders").overwritePartitions()  # 动态分区覆盖（只碰 df 里出现的分区）
df.writeTo("wh.demo.orders").create(new_table)      # 建表并写入
df.writeTo("wh.demo.orders").replace(existing)      # 换 schema 重建数据，表名/权限保留（原地演化）
```

- 没有 `writeTo` 的旧代码（Spark <3）走 `df.write.format("iceberg").mode(...)`——能跑，但
  `overwrite` 语义受 `partitionOverwriteMode` 摆布，且拿不到 `overwritePartitions()` 的显式表达。
- `replace` 的杀手锏：**表身份不变**（catalog 里的登记、下游授权、历史快照血缘都在），
  这是 Hive 表 `DROP+CREATE` 永远做不到的。

### 3.3 行级变更

```sql
-- 教学示意
UPDATE wh.demo.orders SET amount = amount * 0.9 WHERE customer = 'alice';
DELETE FROM wh.demo.orders WHERE ts < TIMESTAMP '2024-01-01';
```

每条语句 = 一次快照提交：要么全成，要么无痕（读侧随时看到旧快照）。UPDATE/DELETE **要求 v2 表**；
v1 表上会报不支持。

### 3.4 INSERT OVERWRITE 与动态分区覆盖

```sql
-- 教学示意：先设会话开关，否则 OVERWRITE 是「静态分区覆盖」
SET spark.sql.sources.partitionOverwriteMode = dynamic;

INSERT OVERWRITE wh.demo.my_app_logs
SELECT * FROM staging.events_today;   -- 只重写结果集中出现的分区
```

`dynamic` 模式下等价于 `df.writeTo(...).overwritePartitions()`；漏设开关是数据湖经典事故：
下游补数任务把整张历史表覆盖成了当天增量。

### 3.5 MERGE INTO 与 upsert 模式

CDC 入湖的标准形态（官方文档示例语法）：

```sql
-- 教学示意：staged_updates 携带当批变更（含 insert/update/delete 标记）
MERGE INTO wh.demo.orders t
USING wh.staging.orders_changes s
ON t.order_id = s.order_id
WHEN MATCHED AND s.op = 'd' THEN DELETE
WHEN MATCHED THEN UPDATE SET t.customer = s.customer, t.amount = s.amount, t.ts = s.ts
WHEN NOT MATCHED THEN INSERT (order_id, customer, amount, ts)
                     VALUES (s.order_id, s.customer, s.amount, s.ts);
```

进阶（需要 02 章的 `IcebergSparkSessionExtensions`）：

```sql
-- 教学示意：全列更新免写列名；清理「源已删除但目标还在」的行
MERGE INTO wh.demo.orders t USING wh.staging.orders_full s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE THEN DELETE;    -- 扩展子句，原生 Spark SQL 没有
```

要点：

- `UPDATE SET *` / `INSERT *` 按**列名**匹配，配合 schema evolution 写变更集极省事（05 章）。
- 整个 MERGE 是**一个快照**：失败重试幂等（重试前无需手工清理半成品——本来就不存在半成品）。
- 典型事故：`ON` 条件不唯一（一对多匹配）时 Spark 默认报
  `MERGE_MATCHED_TOO_MANY_ROWS`，这是保护而非 bug——源端先 `ROW_NUMBER()` 去重。

### 3.6 Copy-on-write vs merge-on-read

行级改删有两种物化策略，按操作各配一档表属性：

| 属性（表 TBLPROPERTIES） | `copy-on-write`（默认） | `merge-on-read` |
| --- | --- | --- |
| `write.delete.mode` | 重写整份数据文件 | 追加 position delete 文件 |
| `write.update.mode` | 重写整份数据文件 | 追加 equality/position delete 文件 |
| `write.merge.mode` | 同上（作用于 MERGE） | 同上 |
| 代价落点 | **写放大**：改 1 行重写整个文件 | **读放大**：查询时合并删除文件 |
| 适合 | 读多写少、点状修正 | 高频批量 upsert、删除比例小 |

MoR 配套开关（示例）：

```sql
-- 教学示意
ALTER TABLE wh.demo.orders SET TBLPROPERTIES (
  'write.delete.mode' = 'merge-on-read',
  'write.update.mode' = 'merge-on-read',
  'write.distribution-mode' = 'hash'      -- 写时按分区键 shuffle，减少小删除文件碎片
);
SELECT * FROM wh.demo.orders VERSION AS OF 3;  -- 读侧默认自动合并 delete 文件，无需特殊语法
```

删除文件的堆积最终靠 06 章的 `rewrite_data_files` 消化——**MoR 不是「不整理」，是把整理推迟**。

## 版本与兼容性

- 原生 `MERGE INTO` Spark 3.2 起有；Iceberg extensions 补了 `BY SOURCE` 子句、通配集与
  多 `WHEN NOT MATCHED BY SOURCE` 分支（Iceberg ≥1.4 时代逐步稳定）。
- equality deletes 仅 v2 表；v3（Iceberg 1.8+ 实验推进中）扩展 deletion vector 等（以规范版本页为准，
  ⚠️ 本目录未逐条核实 v3 细节）。
- 旧式 `df.write().format("iceberg").mode("overwrite")` 在文档中已被 V2 API 取代叙述；
  行为差异主要体现在 `replaceWhere`（按条件覆盖，Iceberg 特有：`df.write.format("iceberg").option("replaceWhere", "ts >= '2025-01-01'")`）。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 不开 dynamic 就跑 `INSERT OVERWRITE` | 默认静态模式 = 全表覆盖；优先用 `writeTo().overwritePartitions()` 显式表达 |
| 「MERGE 失败会留下半更新」 | 快照原子性保证失败无痕；直接重跑即可 |
| MoR 上 `DELETE` 后磁盘文件立刻变小 | delete file 只是标记，物理合并等 compaction（06 章） |
| `ON t.id=s.id AND s.op='u'` 把过滤写进 ON | MERGE 的 `USING` 子查询/ON 语义与 JOIN 相同，但**放错位置会导致不匹配行意外保留**；过滤源集优先用子查询 |
| 以为 UPDATE 不锁表所以并发随便 | 并发冲突时提交做 serializable 校验，可能整体重试/报错；热点表建议批间串行或队列化 |
| DataFrame `.mode("overwrite")` 等同 `.replace()` | 前者覆盖（静态）数据，后者是「换内容保留表身份」的 catalog 操作 |

## 与其他章 / 其他书的联系

- 写入产生的快照 → 用时间旅行验证（[04-时间旅行与元数据表.md](04-时间旅行与元数据表.md)）。
- `PARTITIONED BY (days(ts))` 与 `UPDATE SET *` 的列名解析 → [05-演化与隐藏分区.md](05-演化与隐藏分区.md)。
- MoR 删除文件堆积的治理 → [06-维护过程与流式写入.md](06-维护过程与流式写入.md)。
- Spark JOIN/聚合的执行层背景 → [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)；
  写倾斜与 shuffle 调优 → [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)。
- 若后续建 `Delta_Lake_Definitive_Guide` 目录：Delta 的 `MERGE` 语法几乎同形，差异在
  事务日志冲突粒度与 `OPTIMIZE/ZORDER` 对照系（本目录 06 章）。
