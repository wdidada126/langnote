# 第 11 章 成功设计模式：CDC、SCD 与幂等加载

> 原书第 11 章「Successful Design Patterns」。本章把前面所有机制组装成**可复用的工程模式**：
> CDC 入湖三路线、SCD1/SCD2 历史化、幂等加载与去重、审计/合规模式。
> SQL 为**自拟教学示意，非书中原文**；UPSERT 的一般理论见 [../../db/sql_UPSERT.md](../../db/sql_UPSERT.md)。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 11.1 入湖的三种真相 | 全量快照 / 增量 append / 变更捕获 | 模式选择 = 源系统能力选择 |
| 11.2 CDC 路线对比 | Debezium+MERGE vs Delta CDF vs Kafka Connect | 事件在哪一层产生 |
| 11.3 SCD 全家 | Type1 覆盖 / Type2 历史化 / Type3 桥 | MERGE 是 SCD 的执行原语 |
| 11.4 幂等加载 | 去重三要素：键、版本、水位 | 可重跑是管道的最低尊严 |
| 11.5 迟到与乱序 | 版本列仲裁 + 允许纠正 | 别信到达顺序 |
| 11.6 审计/合规模式 | appendOnly + CDF + 长保留 | 用格式特性替代自建日志 |

## 核心精讲

### 11.1 入湖三路线（先问源系统能给什么）

| 路线 | 源端要求 | 湖内形态 | 弱点 |
| --- | --- | --- | --- |
| 全量快照（每日 dump） | 无 | 每日一批新文件 | 无法捕获删除；体积大 |
| 增量 append（自增 id/时间戳） | 单调游标列 | 只追加 | 漏 UPDATE/DELETE |
| CDC（日志挖掘） | binlog/重做日志访问权 | 事件流 | 部署重；DDL 变更要跟 |

- Delta 的第一桶金：**前两种「残缺路线」在湖内也能被 MERGE 补齐成 upsert**；
  第三种自带语义时，Delta 提供 CDF 把「湖内变更」也变成一等公民。

### 11.2 CDC 的两层语义：源 CDC 与 Delta CDF

```text
路线 A（经典）：MySQL binlog → Debezium → Kafka → foreachBatch MERGE → silver
路线 B（湖内）：silver 开 CDF → 下游流读 TABLE(changes) 精确拿 pre/post image
路线 C（低代码）：Kafka → Delta Connect sink（内置 dedupe/MERGE 配置）
```

- A 与 B 不是竞品：**A 负责进湖，B 负责湖内广播**——一张 silver 表开 CDF，
  十个下游订阅变更，不必十个下游各自 diff。
- 判别口诀：下游需要「删了哪一行」的答案 → CDF；只需要当前态 → MERGE upsert 即可。
- 写放大对比：A 模式每批重写命中文件（无 DV 时严重）；开 DV 后 UPDATE 代价降为 bitmap 追加（第 7 章文件）。

### 11.3 SCD：用 MERGE 落地维度历史化

**SCD Type1（覆盖，不留历史）**——最常见的「修正型」维度：

```sql
-- 教学示意
MERGE INTO dim_customer t USING stg s ON t.customer_id = s.customer_id
WHEN MATCHED AND (t.email <> s.email OR t.city <> s.city)
  THEN UPDATE SET email = s.email, city = s.city, current_version = t.current_version + 1
WHEN NOT MATCHED THEN INSERT *;
```

**SCD Type2（历史化，版本链）**：

```sql
-- 教学示意：两步 MERGE（先关旧行，再插新行）
-- ① 关链：属性变化的现有行置失效
MERGE INTO dim_customer_zipper t USING stg_changed s
  ON t.customer_id = s.customer_id AND t.is_current = 'Y'
WHEN MATCHED THEN UPDATE SET t.is_current = 'N', t.end_date = s.effective_date;
-- ② 开链：变化行作为新版本插入
INSERT INTO dim_customer_zipper
SELECT s.*, s.effective_date AS start_date, '9999-12-31' AS end_date, 'Y' AS is_current
FROM stg s LEFT JOIN dim_customer_zipper c
  ON s.customer_id = c.customer_id AND c.is_current = 'Y'
WHERE c.customer_id IS NULL OR s.hash_diff <> c.hash_diff;
```

- 机制注意：两步之间**不是原子事务**——并发写或中途失败会留下「双 current」；
  防御：把两步合进一个 MERGE（WHEN MATCHED UPDATE + WHEN NOT MATCHED INSERT 单语句可完成大半），
  或按「同键同代次单 writer」纪律调度（第 6 章文件 7.1 的单 writer 原则）。
- 物理设计联动（第 9 章文件）：拉链表的 `is_current`/`effective_date` 是天然聚簇键
  （liquid `CLUSTER BY (customer_id)` 后「查当前态」几乎零扫描）；
  Z-ORDER 高基数键选择同理。
- Type3（加 previous_column 桥）：仅在业务只要「上一版」时用，Delta 时代更优解是
  **时间旅行代替 Type3**——`VERSION AS OF` 直接读历史快照，别再造列。
- 对照仓库既有笔记：SCD 的仓库语境见 [../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)；
  UPSERT 通用讨论见 [../../db/sql_UPSERT.md](../../db/sql_UPSERT.md)。

### 11.4 幂等加载：三要素模板

```sql
-- 教学示意：按业务键取最新版本后再 MERGE（批内去重）
WITH dedup AS (
  SELECT *, row_number() OVER (PARTITION BY order_id
            ORDER BY source_updated_at DESC, kafka_partition, kafka_offset DESC) rn
  FROM micro_batch)
MERGE INTO silver.orders t USING (SELECT * FROM dedup WHERE rn = 1) s
  ON t.order_id = s.order_id
WHEN MATCHED AND s.source_updated_at >= t.source_updated_at THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

- 三要素：**业务键（ON）+ 版本仲裁（WHERE 条件里的时间戳/offset）+ 重放保护（第 6 章文件 7.1 的 txn 幂等）**。
- 「`MATCHED AND newer`」条件是灵魂：不加它，重放旧批次会把新数据写回旧值（upsert 变 last-write-wins-by-arrival）。
- 删除语义：源侧硬删要么靠 CDC 事件（op=d），要么定期「全量对账 anti-join → DELETE」。

### 11.5 迟到与乱序

- 策略表：

| 场景 | 手段 |
| --- | --- |
| 迟到修正 UPDATE | 版本仲裁 MERGE（允许旧到达序、新业务时间戳） |
| 迟到 INSERT 且已过期聚合 | gold 增量重算窗口（按事件日期重刷分区） |
| 乱序窗口聚合 | 留给流引擎 state+watermark（湖外解决），或批模式全量重算 |
| 重复投递 | 幂等键去重（11.4 模板）+ txn 机制兜底 |

- 原则：**湖内表只认「业务版本」，不认「到达版本」**——到达序只用于同业务时间戳的 tie-break。

### 11.6 审计/合规模式（把特性当制度用）

- `delta.appendOnly=true` + 长 logRetention = 防篡改留痕；
- CDF = 变更审计日志（谁在何时改了哪些行，`_commit_version` 可关联 `DESCRIBE HISTORY` 的操作者）；
- 时间旅行 + SHALLOW CLONE 定期冻结 = 不可变发布快照（报表口径冻结用克隆，不用复制）；
- 与第 11 章文件（治理）的分工：Delta 提供**数据面**证据，UC 审计日志提供**访问面**证据。

## 版本演进

| 时期 | 模式演化 |
| --- | --- |
| 2019–2021 | 「MERGE 一把梭」时代：CDC/SCD 全靠手写 SQL |
| 2022–2023 | CDF 进 OSS：湖内变更流取代下游 diff 土法；DV 缓解 upsert 写放大 |
| 🔧 2024+ | declarative pipelines（DLT/Lakeflow）与 materialized views 把 11.2–11.4 变成托管能力；collation 根治维度键大小写分裂（第 7 章文件 8.6） |

## 文献与文档

- delta.io *Change Data Feed*、Databricks docs *Upsert (MERGE) / SCD with Delta*（CDC/SCD 模式官方样例的原口径）。
- Kimball & Ross, *The Data Warehouse Toolkit* —— SCD Type 1/2/3 的原始定义。
- Debezium 文档（源端 CDC）；databrickslabs/delta-connect（路线 C）。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「MERGE 了就是幂等」 | 无版本仲裁的 MERGE 重放旧批会回退数据；幂等 = 键 + 版本条件 |
| 2 | 「SCD2 要两条 SQL 才完整」 | 可单 MERGE 覆盖大半；两步则须保证原子性或单 writer 纪律 |
| 3 | 「Type3 保留旧值列很高级」 | Delta 有 time travel，Type3 多为多余复杂度 |
| 4 | 「CDF 与 Debezium 二选一」 | 层不同：Debezium 抓源库日志进湖，CDF 供湖内变更广播 |
| 5 | 「软删列（is_deleted）万能」 | 下游全要带谓词，忘一处即口径错；CDF/DV 硬删语义更干净 |
| 6 | 🔧 「模式只能手写」 | 托管物化视图/DLT expectations 已承接常见模式，手写前先查平台能力 |

## 与其他章 / 其他书的联系

- ← `02`：MERGE 语义与冲突；← `06`：foreachBatch 幂等；← `07`：CDF/DV 是本章两个模式的加速器。
- → `09`：优化把「按当前态过滤」的 SCD 表做到极致；→ `11`：模式产出的血缘与审计归口。
- → [../../db/sql_UPSERT.md](../../db/sql_UPSERT.md)、[../../db/sql2.md](../../db/sql2.md)：关系库视角的 UPSERT 对照。
- → [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)：Kafka/Debezium 上游生态。
- → [../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)：质量契约与模式库的互补。
