# 第 3 章 Delta Lake 基本操作：事务、CRUD 与 schema

> 原书第 3 章「Essential Delta Lake Operations」。本文件把书中散布在 SQL/DataFrame 两种入口的操作，
> 按**机制优先**重排：事务日志布局 → 乐观并发控制（OCC）→ DML 的写放大 → schema 约束与演化 → 基础时间旅行。
> 所有 SQL/代码为**自拟教学示意，非书中原文，不参与构建**；机制口径参照 delta.io 与 Databricks 公开文档。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 `_delta_log` 长什么样 | commit JSON、checkpoint、协议/元数据条目 | 一张 Delta 表 = data files + 一个可重放的日志 |
| 3.2 一次提交的生命周期 | 读快照→写文件→CAS 式追加 commit | 对象存储上的「串行化点」 |
| 3.3 乐观并发控制 | 冲突判定矩阵、重试语义 | 冲突在读集不在写集 |
| 3.4 DML 全家桶 | INSERT/UPDATE/DELETE/MERGE 的文件语义 | 每条行级 DML 都是「重写受影响文件 + 记 add/remove」 |
| 3.5 MERGE 深入 | 匹配条件、多动作、写放大 | MERGE 是 UPDATE+DELETE+INSERT 的批量合成 |
| 3.6 schema enforcement/evolution | 契约 vs mergeSchema | 默认拒绝未知列，演化要显式 |
| 3.7 约束 | NOT NULL 为真、CHECK 后加 | Delta 的 CHECK 直到 OSS 3.0/DBR 9.1 才强制 |
| 3.8 基础时间旅行 | VERSION/TIMESTAMP AS OF | 读历史 = 按 commit 重放 |

## 核心精讲

### 3.1 `_delta_log` 的文件布局

```text
my_table/
├── _delta_log/
│   ├── 00000000000000000000.json   ← commit #0（建表）
│   ├── 00000000000000000001.json   ← commit #1
│   ├── ...
│   ├── 00000000000000000009.json
│   ├── 00000000000000000010.checkpoint.parquet  ← 每 10 个 commit 一个快照
│   ├── 00000000000000000010.uuid.checkpoint.parquet（sidecar/uuid 变体，🔧）
│   └── _last_checkpoint            ← 指向最新 checkpoint 的指针
├── part_col=x/ part-00000-....parquet  ← data files（默认 Parquet）
```

commit JSON 是**一行一条目的 NDJSON**，关键 action（教学示意）：

```json
{"commitInfo":{"timestamp":1735689600000,"operation":"WRITE","operationParameters":{"mode":"Append"},"readVersion":3,"isolationLevel":"Serializable","readOpMetrics":{},"writerId":"stream-1"}}
{"protocol":{"minReaderVersion":1,"minWriterVersion":2}}
{"metaData":{"id":"d1b2...","format":{"provider":"parquet"},"schemaString":"...","partitionColumns":["dt"],"configuration":{"delta.checkpointInterval":"10"}}}
{"add":{"path":"dt=2026-01-01/part-xxx.parquet","size":5242880,"modificationTime":...,"dataChange":true,"stats":"{\"numRecords\":100000,\"minValues\":{\"id\":1},\"maxValues\":{\"id\":999999},\"nullCount\":{\"id\":0}}"}}
{"remove":{"path":"dt=2025-12-31/part-yyy.parquet","deletionTimestamp":...,"dataChange":true}}
```

- **`add`/`remove` 构成快照**：当前版本 = 从日志头重放所有 add/remove（checkpoint 提供加速入口，
  读时只需从最近 checkpoint 往后重放若干 commit）。
- **`stats` 内嵌 per-file 列级 min/max/nullCount**（默认只统计前
  `delta.dataSkippingNumIndexedCols`=5 列）——这是 data skipping 的物理基础（第 10 章性能）。
- **checkpoint 间隔**：`delta.checkpointInterval` 默认 10；日志越长，元数据重建越慢，
  这就是「commit 风暴（高频小提交）拖慢读」的根因（第 7 章流式微批尤其相关）。
- 🔧 Delta 4.0 引入**统一元数据布局**（变长 struct/map 的 metadata action），
  为 UniForm/sidecar checkpoint 铺路；老 reader 通过 protocol 表特性隔离。

### 3.2 一次提交的生命周期（对象存储上如何做「原子」）

```text
① 事务开始：记录当前读到的 commit 版本 V_read
② 物理写：新 data files 全部写完（此时对任何读者不可见——没有 commit 引用它们）
③ 生成候选 commit：txn/add/remove/timestampCommitMarker...
④ 尝试写 _delta_log/{V_read+1}.json（一次不可见的 PUT / 条件写）
   ├─ 成功 → 提交完成，全库瞬间可见（原子发布点）
   └─ 已存在 → 有人抢先提交：进入 ⑤
⑤ 冲突判定（见 3.3）：可调和 → 基于新快照重新生成 commit 再试；不可调和 → 抛异常
```

- 「④ 的原子性」依赖对象存储语义：S3 的 List-after-PUT 一致性与「同一 key 只写一次」惯例；
  这正是 Delta 论文（VLDB 2020）讨论的一致性前提。
- **提交是元数据操作，写数据才是重活**——这个分层让「回滚/时间旅行/克隆」全都近乎零成本。

### 3.3 乐观并发控制（OCC）

- 与两阶段封锁相对：**写前不加锁**，提交时比对并发事务的读写集。
- 隔离级别默认 **Serializable**（`commitInfo.isolationLevel`）；Delta 的冲突判定核心是：

| 并发事务 A 做了什么 | 事务 B 提交时判 | 结果 |
| --- | --- | --- |
| A 只 append 了新文件（B 没读那些分区） | 读集不相交 | 双方都成功 |
| A 重写了 B 读过/删过的文件 | add 同名 / remove-remove 幂等可调和 | 多数可自动重试 |
| A 与 B 都 DELETE/UPDATE 同一行 | 写写冲突 | Serializable 下后提交者失败或重试后重算 |
| A 改了 schema/partition，B 写数据 | 协议冲突 | 一般直接失败 |

- **重试语义分场景**：
  - Batch DML（MERGE/UPDATE）：OSS 默认**不自动重试**，抛
    `io.delta.exceptions.ConcurrentTransaction` 等，需客户端重试整个作业；
  - Structured Streaming sink：由流引擎保证「同一表同一时刻单 writer」（`txn` action 幂等，见第 7 章），所以天然无冲突；
  - 🔧 Databricks 对部分 DML 提供自动重试（`spark.databricks.delta.retries.enabled` 等，口径以 Databricks 文档为准）。
- 对照教科书：Kung & Robinson 1981 的乐观方法；与 [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md) 的「验证阶段」概念一一对应。

### 3.4 DML 全家桶的文件语义（写放大视角）

> 关键心智模型：**Delta 的 UPDATE/DELETE 不是改行，是发布新快照。**

```sql
-- 教学示意，非书中原文
UPDATE events SET severity = 'HIGH' WHERE ts > '2026-01-01';
```

Copy-on-Write（默认）执行过程：

```text
① data skipping 圈定候选文件（min/max 粗筛 + 精确读）
② 对每个「含目标行」的 parquet 文件：读全文 → 内存改行 → 写出新文件
③ commit：add 新文件、remove 旧文件；未受影响文件原样保留
```

- **写放大** = 受影响文件数 × 文件大小：一行改动重写整个文件（parquet 行组级不可就地改）。
  高基数 UPDATE（频繁改少量行）在 CoW 下代价极高 → 解法是 Deletion Vectors（第 7 章文件）。
- `DELETE` 同构；`INSERT` 只 add 新文件、零重写。
- 分区裁剪：`WHERE dt='2026-01-01' AND ...` 让 ① 只扫一个目录——**分区是 DML 的第一桶金**（而非只服务查询）。

### 3.5 MERGE 深入

```sql
-- 教学示意，非书中原文：典型 upsert
MERGE INTO dim_customer AS t
USING stg_customer_$runId AS s ON t.id = s.id
WHEN MATCHED AND s.is_delete = 'Y' THEN DELETE
WHEN MATCHED THEN UPDATE SET email = s.email, updated_at = current_timestamp()
WHEN NOT MATCHED THEN INSERT (id, email, updated_at) VALUES (s.id, s.email, current_timestamp());
```

- 机制：一次扫源、一次扫目标，按 ON + 附加条件把目标文件分为
  「命中需改 / 命中需删 / 不命中」三类，输出 = 未受影响文件保留 + 受影响文件重写（含新行） + 纯新增文件。
- **条件化 MATCHED 顺序敏感**：`MATCHED AND delete` 要写在无条件 `MATCHED UPDATE` 之前（同 UPDATE SET 里用 CASE 也可）。
- **源去重是失败主因**：ON 键在源侧重复且多行同时命中 → `MERGE MATCHED cardinality violation`；
  先对源 `GROUP BY`/`ROW_NUMBER` 去重是标准做法。
- 写放大：源里一个分区 1 行变更 ⇒ 目标整文件重写。小文件多时先 `OPTIMIZE` 再 MERGE 往往更快（文件少但大）。
- 🔧 Databricks 支持 MERGE 内子查询/多动作限制逐步放开；OSS 能力子集略小，以 delta.io 语法页为准。

### 3.6 Schema enforcement 与 evolution

```sql
-- 教学示意
ALTER TABLE users ADD COLUMNS (trial BOOLEAN);
ALTER TABLE users CHANGE COLUMN name name STRING AFTER id;   -- 只改列名/位置，需 column mapping
-- DataFrame 侧：df.write.format("delta").option("mergeSchema", "true").mode("append").save(path)
```

- **Enforcement**：写入 schema 与表 schema 不一致（多列/类型不同）默认报错——防脏写。
- **Evolution**：`mergeSchema=true`（写入选项）或显式 `ALTER TABLE`。类型上只允许**安全拓宽**
  （int→bigint、decimal 加宽；🔧 OSS 3.x type widening 才开放更多隐式拓宽）。
- **列名/列序变更依赖 column mapping**（`delta.columnMapping.mode = name`）：
  开启后 parquet 物理列用内部 id 对应逻辑列名，重命名不再重写数据。writer feature，协议 v2。
- ⚠️ `partitionColumns` 建表后**不能 ALTER**；要换分区方案只能重建/克隆 + liquid clustering（第 9/10 章）。

### 3.7 约束

| 约束 | 生效情况 |
| --- | --- |
| NOT NULL | 真约束，建表即强制 |
| CHECK | 🔧 后到能力（DBR 9.1 / OSS 3.0 writer feature），写入时求值强制 |
| 主键/外键 | **仅是元数据声明（ENFORCED false），引擎不校验**——给 BI/血缘用的语义提示 |

「Delta 有 PRIMARY KEY 却不强制」是原书点名的经典误区，务必带进 3.7 的表格记忆。

### 3.8 基础时间旅行（详见 04 章文件）

```sql
-- 教学示意
SELECT * FROM events VERSION AS OF 42;
SELECT * FROM events TIMESTAMP AS OF '2026-01-01 00:00:00';
DESCRIBE HISTORY events LIMIT 10;
```

读历史 = 从目标版本向前重放日志得到该快照的文件集；受 `delta.logRetentionDuration`（默认 30 天）
与 VACUUM 保留期约束——**日志过期或文件被清，历史就不存在**。

## 版本演进

| 版本 | 本章相关变化 |
| --- | --- |
| Delta 1.0（2020） | add/remove/commitInfo 布局冻结，Serializable 语义确立 |
| Delta 2.x | 冲突信息结构化（conflict metadata）、commit 重试可见性改善 |
| Delta 3.0（2023） | writer feature 框架：CHECK、type widening、file_format 特性化；column mapping 成熟 |
| 🔧 Delta 4.0（2025） | 统一元数据、type widening 更广、DV 成 writer3/特性 |

## 文献与文档

- Armstrong et al., *Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores*, VLDB 2020 —— 事务日志与对象存储一致性前提的原典。
- Kung & Robinson, *On Optimistic Methods for Concurrency Control*, ACM Computing Surveys 13(2), 1981。
- delta.io「Delta Lake Data API / Transactions / Constraints」文档；Databricks docs「Delta Lake optimization / MERGE INTO」。
- Gray & Reuter, *Transaction Processing*, 1993 —— 可串行化验证阶段的一般理论。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「UPDATE 是就地改一行」 | CoW 语义下重写受影响文件；写放大以文件为粒度（DV 缓解，见 07） |
| 2 | 「主键/外键能保证引用完整」 | Delta 不强制 PK/FK，只有 NOT NULL/CHECK 是真约束 |
| 3 | 「MERGE 天然幂等」 | 源侧重复键会直接报错；重试前还要确认目标没被并发改写 |
| 4 | 「commit 越多越好（历史丰富）」 | 日志线性变长、元数据重放变慢；checkpoint 与合并提交是必要运维 |
| 5 | 「schema evolution 永远无损」 | 重命名依赖 column mapping；未开启时是「新列+旧列并存」的假重命名 |
| 6 | 🔧 「OSS 与 DBR 约束能力一致」 | CHECK/type widening 的 GA 时间线两边不同步 |

## 与其他章 / 其他书的联系

- ← `01`：两个必配 conf 是本章语法可用的前提。
- → `04`：时间旅行/RESTORE/CLONE 的完整版；→ `07`：DV 如何改写 3.4 的写放大结论。
- → `10`：commit 风暴、checkpoint、stats 都在性能章继续展开。
- → [../mysql/19-redo日志.md](../mysql/19-redo日志.md)：redo 是「页增量+循环覆盖」，Delta 日志是「文件清单+永久追加」——同为 WAL 思想、相反的生命周期。
- → [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md)：OCC 验证阶段的教科书定义。
- → [../../db/db.md](../../db/db.md)：事务索引条目。
