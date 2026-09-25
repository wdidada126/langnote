# 第 5 章 表维护：时间旅行、VACUUM 与克隆恢复

> 原书第 5 章「Maintaining your Delta Lake」。本文件围绕三条运维主线：
> **看历史（DESCRIBE HISTORY）→ 回历史（时间旅行/RESTORE）→ 清历史（VACUUM/日志保留）**，
> 外加 CLONE/convert、表属性、OPTIMIZE 入门。所有 SQL 为**自拟教学示意，非书中原文**。
> 机制口径参照 delta.io「Table maintenance / Vacuum / Time travel」与 Databricks 同名文档。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 历史即数据 | commit 序列就是可查询的时间轴 | DESCRIBE HISTORY 是第一诊断工具 |
| 5.2 时间旅行 | VERSION/TIMESTAMP AS OF、生成列作版本 | 读旧快照 = 重放旧日志 |
| 5.3 VACUUM 机制 | 保留期、日志窗口、两阶段清理 | VACUUM 是**不可逆**的物理删除 |
| 5.4 RESTORE 与 CLONE | 回滚、浅克隆/深克隆、增量复制 | CLONE 只拷元数据+引用，代价极低 |
| 5.5 convertToDelta | 裸 parquet 目录原地升表 | 存量入湖的低成本入口 |
| 5.6 OPTIMIZE 入门 | 小文件合并 | 详细调优在第 10 章 |
| 5.7 表属性与配置 | TBLPROPERTIES 清单 | Delta 的行为大多可调 |

## 核心精讲

### 5.1 DESCRIBE HISTORY：先会看再敢动

```sql
-- 教学示意
DESCRIBE HISTORY events;          -- 全列
DESCRIBE HISTORY events
  SELECT operation, version, timestamp, readVersion, isManaged,
         operationMetrics.numUpdatedRows, operationMetrics.numRemovedFiles
  LIMIT 20;
```

- 每行 = 一个 commit。关键列：`version`、`readVersion`（本事务基于哪个快照，OCC 证据）、
  `operation`/`operationMetrics`（行数、文件数、字节数——审计与成本归因都在这里）。
- 过滤历史窗口用 `WHERE timestamp >= ...`；**历史行数受 `delta.logRetentionDuration` 控制**
  （默认 30 天）：日志被回收后，30 天前的版本连「看见」都做不到，更别说恢复。

### 5.2 时间旅行

```sql
-- 教学示意
SELECT * FROM events VERSION AS OF 42;
SELECT * FROM events TIMESTAMP AS OF '2026-01-01 09:00:00';
-- DataFrame / 生成列写法
df = spark.read.format("delta").option("versionAsOf", 42).load(path)
```

- 实现：读引擎定位目标版本 commit（checkpoint 加速重放），得到当时的文件集，正常扫 parquet。
- **前提校验**：目标版本必须 ≥ VACUUM 水位且其日志未过期——
  时间旅行不是备份，只是「旧元数据 + 未被删除的文件」。
- 经典事故：报表任务误用 `INSERT OVERWRITE` 覆盖全年数据 → 用
  `RESTORE ... VERSION AS OF <昨天>` 一键回滚（见 5.4）；再补一条 CHECK 约束防复发。

### 5.3 VACUUM：把「逻辑删除」变成「物理删除」

```sql
-- 教学示意
VACUUM events RETAIN 168 HOURS;              -- 默认保留 7 天
VACUUM events DRY RUN;                        -- 先列清单再动手
VACUUM catalog.db.events RETAIN 720 HOURS;   -- 按 UC 表名
```

机制（必考）：

```text
① 确定安全水位：max(当前时间 - retention, 最早保留的日志窗口)
② 重建「仍被任何 ≥ 水位的快照引用」的文件集（in-use set）
③ LIST 表目录下全部对象，取差集 = 可删文件
④ 分批批量 DELETE；日志中记 vacuum 事件
```

- **保留期默认 7 天**（`delta.deletedFileRetentionDuration`，SQL 侧下限默认 7 天，
  放宽需 `spark.databricks.delta.retentionDurationCheck.enabled=false`——生产禁用此开关是红线）。
- 为什么是 7 天：给「还在跑的长查询/长流作业」留读旧快照的窗口；
  **VACUUM 后 RESTORE 到更早版本 = 数据真没了**。
- VACUUM 不清 `_delta_log` 本体（日志归 logRetention 管），也不清未提交的孤儿文件之外的…
  准确说：孤儿文件（写成功但从未 commit 的）会被 LIST 差集清掉，这正是 VACUUM 慢的原因之一——**全目录 LIST**。
- 🔧 **Incremental VACUUM**（Delta 4.0/Databricks 14.x+）：按「上次 VACUUM 版本」只扫新增区间，
  大表 LIST 成本大幅下降；另有并行 VACUUM（分桶并发）。
- 多引擎旁路注意：**其他引擎的读者若长期持有旧快照（如慢 BI），7 天不够**——retention 是容量与安全的权衡。

### 5.4 RESTORE 与 CLONE

```sql
-- 教学示意：回滚到 3 天前
RESTORE TABLE events TO VERSION AS OF 1180;
-- 浅克隆：只拷元数据，共享文件（引用计数式）
CREATE TABLE gold_snapshot SHALLOW CLONE events VERSION AS OF 1180;
-- 深克隆：物化一份独立副本
CREATE TABLE dev_events DEEP CLONE prod.events;
-- 增量复制（持续同步用）
CLONE prod.events INTO dev_events REPLACE;   -- 只拷自上次 clone 以来的新文件
```

- RESTORE 本质是新 commit：add 旧快照仍在的文件、remove 新快照多出的文件——
  **回滚不重写数据，秒级提交**（除非数据文件已被 VACUUM）。
- SHALLOW CLONE：几乎零拷贝，适合「冻结快照给审计/回测」；但**与源表生死与共**——
  源表 VACUUM 前需把 retention 对齐，否则克隆表读到被删文件即损坏。
- DEEP CLONE/增量 CLONE：跨存储/跨云的物化与同步通道，是低成本灾备与「prod→dev 刷数」的标准件。
- `CLONE ... AS OF` + `REPLACE` 组合 = 手动 delta 同步协议；Delta 3.x 起增量克隆记录
  `delta.clones` 元数据，能只复制新文件。

### 5.5 convertToDelta：存量 parquet 目录升表

```sql
-- 教学示意：裸目录按分区推断挂载
 CONVERT TO DELTA.`parquet`.`/mnt/warehouse/orders` PARTITION BY (dt);
```

零数据重写：只生成首个 commit 把现有文件登记为 add。限制：无法恢复转换前的历史、
嵌套列需要完整 schema 声明——**先备份再 convert** 是老工程师的条件反射。

### 5.6 OPTIMIZE 入门

```sql
OPTIMIZE events;                       -- 小文件合并（bin-pack）
OPTIMIZE events ZORDER BY (user_id);   -- 合并 + 聚簇，见第 10 章
```

小文件危害链：LIST/元数据开销 → 任务碎片化 → data skipping 失效（每文件 min/max 覆盖全值域）。
OPTIMIZE 的完整策略（partition filter、schedule、与 DV 的交互）在 `09-性能调优.md`。

### 5.7 常用表属性速查（TBLPROPERTIES / SQLConf 前缀 `delta.`）

| 属性 | 默认 | 作用 |
| --- | --- | --- |
| delta.appendOnly | false | 禁止 UPDATE/DELETE（合规留存表用） |
| delta.dataSkippingNumIndexedCols | 5 | 统计前 N 列 |
| delta.checkpointInterval | 10 | 日志快照频率 |
| delta.logRetentionDuration | 30 天 | 历史可见窗口 |
| delta.deletedFileRetentionDuration | 7 天 | VACUUM 保留期 |
| delta.enableChangeDataFeed | false | CDF 开关（第 7 章文件） |
| delta.columnMapping.mode | none | 重命名支持 |
| 🔧 delta.enableDeletionVectors | false（DBR 10.4+ 新表默认方向） | DML 免重写文件 |

## 版本演进

| 版本 | 相关变化 |
| --- | --- |
| Delta 0.x–1.0 | 时间旅行、VACUUM、clone 语法成形 |
| Delta 2.0 | 增量 CLONE（只拷新文件） |
| Delta 3.x | 并行 VACUUM（社区）、RESTORE 完善；DV 改变 UPDATE 的删除物语义 |
| 🔧 Delta 4.0 / DBR 15+ | Incremental VACUUM（记 last vacuum 版本）、sidecar/uuid checkpoint 抗大日志 |

## 文献与文档

- delta.io：*Vacuum a table*、*Time travel*、*Clone (Shallow and Deep)*、*Convert to Delta*。
- Databricks docs：*Delta Lake table maintenance*（含 retention 安全阀说明）。
- VLDB 2020 Delta 论文 §日志回收/一致性窗口。
- 对照阅读：[../mysql/20-undo日志.md](../mysql/20-undo日志.md)——undo purge 与 VACUUM 同为「历史垃圾回收受最老活跃读者限制」的同构问题。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「时间旅行 = 备份」 | 依赖旧文件未被 VACUUM 且日志未过期；真灾备走 DEEP CLONE/对象存储版本控制 |
| 2 | 「VACUUM 只是清孤儿」 | 它同时清「remove 过的历史文件」，误配 retention 直接毁 RESTORE 能力 |
| 3 | 「retention 调成 0 省存储」 | 正在跑的读者立刻可见损坏；retentionDurationCheck 存在就是为了拦这个 |
| 4 | 「SHALLOW CLONE 是快照，绝对安全」 | 与源共享文件，源 VACUUM 会击穿克隆——要么提高 retention 要么 DEEP |
| 5 | 「RESTORE 很慢（要重写数据）」 | 是元数据提交；慢的只是「旧文件已被物理删除需回灌」的情况 |
| 6 | 🔧 「VACUUM 必然全目录 LIST」 | 增量 VACUUM（4.0+）只扫上次水位之后的增量区间 |

## 与其他章 / 其他书的联系

- ← `02`：add/remove 与 commit 结构是本章一切机制的地基。
- → `07`：DV 表里 DELETE 产生 `_deletion_vector_*.bin`，VACUUM 同样负责回收它们；OPTIMIZE 才物化压缩。
- → `09`：OPTIMIZE 深水区、liquid 重聚簇。
- → [../mysql/19-redo日志.md](../mysql/19-redo日志.md)、[../mysql/20-undo日志.md](../mysql/20-undo日志.md)：日志生命周期对照。
- → [../数据库系统概念6/16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)：ARIES 用日志「向前重做」，Delta 用日志「向后跳转」。
