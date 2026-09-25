# 第 2 章 Hudi 快速入门

> 原书章题（译系列核实）：Hudi 快速入门。小节地图：基础操作（建表/CRUD）→ 选择表类型（COW vs MOR、文件组与文件切片）→ 高级用法（CTAS、MERGE、非记录键更新、时间旅行、增量查询）→ 小结。
> 本章是全书物理布局与 timeline 概念的**唯一一次完整铺垫**，03/04/05/06 章全部依赖这里。

## 本章地图

> 一句话：**一张 Hudi 表 = 分区目录下的若干 file group；一次写入 = timeline 上一个 instant 从 requested 走到 completed；COW 在写时合并、MOR 在读时合并——其余全是这两句话的推论。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 建表 | 分区字段、记录键、preCombine 三元组 | 表属性决定后续一切布局 |
| 2.2 首次写入后的物理布局 | `.hoodie/` + 分区目录 + base file | commit 文件是"这一批的收据" |
| 2.3 Timeline：instant 三态 | requested → inflight → completed | 原子可见 = completed 文件出现 |
| 2.4 COW vs MOR | base file + log file；更新路径对比 | 读放大与写放大的交换比 |
| 2.5 File group 与 file slice | 同一 fileID 的多版本切片 | 时间旅行 = 选 slice 的算法 |
| 2.6 高级写入 | CTAS / MERGE INTO / 非记录键更新删除 | 非键更新靠索引反查（伏笔第 5 章） |
| 2.7 时间旅行与增量查询预览 | as-of version/timestamp；两 instant 之间 | 详细机制在第 4 章 |

## 核心精讲

> **教学示意，不参与构建。** 以下 SQL 基于 Spark 3.x + hudi-spark bundle，未在本地执行。

### 2.1 建表：三个属性定生死

```sql
-- 教学示意，不参与构建
CREATE TABLE retailmax.customers (
  id STRING,
  name STRING,
  ts TIMESTAMP,        -- preCombine 候选
  dt STRING            -- 分区字段
) USING hudi
TBLPROPERTIES (
  type = 'cow',                                  -- 或 mor
  primaryKey = 'id',
  preCombineField = 'ts'
)
PARTITIONED BY (dt)
LOCATION 's3://lake/hudi/retailmax/customers';
```

- **primaryKey**：记录级 upsert 的锚点；官方称 record key = (partitionPath, recordKey) 二元组。
- **preCombine**：同一批内出现重复 key 时谁胜出（第 3 章 merge mode 的批内部分）。
- **partition**：文件目录切分粒度；也是增量查询与 pruning 的第一层索引。分区值参与 record key 的全局唯一性判定——同 key 换分区 = 删旧插新（03 章 partition schema 的坑）。

### 2.2 首次写入后的物理布局

```text
s3://lake/hudi/retailmax/customers/
├── .hoodie/
│   ├── timeline/
│   │   └── 20260925101500000.commit            ← 完成态：一次 insert 的元数据(含受影响文件清单)
│   ├──hoodie.properties                          ← 表协议与不可变属性
│   └── metadata/                                 ← metadata table（第 5 章）
├── dt=2026-09-25/
│   └── a1b7-..._0-1-1_20260925101500000.parquet  ← base file
└── ...
```

- base file 命名（教学示意）：`<fileId>_<commit>_<task>_<version>`——同一 `fileId` 跨 commit 不变，这就是 file group 的身份。
- `.hoodie/<instant>.commit` 内容：该事务**新增/替换/删除了哪些文件、各文件记录数与字节数、schema、统计**。读取端靠它把"当前有效文件集合"算出来。

### 2.3 Timeline：instant 的三态生命周期

```text
一次 action 的生命：
  1) .commit.requested   （决定要做：分配 instant time）
  2) .commit.inflight    （正在做：数据文件已写、尚未发布）
  3) .commit             （完成：原子发布点，含额外元数据）
instant time：时间单调的字符串（001、002 递增，或 yyyyMMddHHmmssSSS）
```

- **可见性规则**：查询只看到 completed instant 组成的快照；requested/inflight 对读者不可见。
- **失败即回滚**：inflight 悬挂 → 下一次写事务开始前产生 `.rollback.inflight → .rollback`，清理半写文件（03 章"Start Commit 前先回收"）。
- **action 家族**：`commit`（COW 写）、`deltacommit`（MOR 写）、`compaction`、`clean`、`rollback`、`replacecommit`（clustering）、`savepoint`、`restore`、`indexing`、`bootstrap`。timeline 就是这些动作的全序日志——**它扮演的正是 MySQL redo/binlog 的角色，但记的是"文件清单版本"而非页改动**（对照 [../../db/db.md](../../db/db.md)）。

### 2.4 COW vs MOR：把合并成本放在写侧还是读侧

```text
COW 更新一条记录：
  找到含该 key 的 base file → 读整文件 + merge → 写新 base file（新 version）→ commit
MOR 更新一条记录：
  找到 file group → 往该 file group 追加一个 log block（parquet/avro block）→ deltacommit
MOR 读取（snapshot）：
  base file + 各 log block 现场 merge（读放大）
MOR 快照优化读（read-optimized）：
  只读 base file（旧值，零 merge）
```

| 维度 | COW | MOR |
| --- | --- | --- |
| 写放大 | 高（重写整文件） | 低（只追加 log） |
| 读放大 | 无 merge | snapshot 需 compaction/merge |
| 新鲜度 | 提交即可见 | read-optimized 滞后到 compaction |
| 适合 | 分析为主、更新比例低 | 高频 upsert、近实时 |
| 隐藏成本 | 大文件重写抖动 | compaction 调度与资源（第 6 章） |

官方口径补充：MOR 的 log 由若干 **log block**（hoodie parquet/avro block）顺序追加，读取时按 block 类型选择 merge 策略；COW 与 MOR 的"选哪个 file group / 何时滚动新文件"都依赖记录大小估算（具体小文件处理与参数在第 3 章、compaction 触发在第 6 章）。**选型一句话**：更新频率高选 MOR；否则 COW 少一套后台债务。

### 2.5 File group 与 file slice

- **file group**：同一分区内、同一 `fileId` 的所有 base/log 文件的逻辑集合——**并发控制与索引的裁决单位都是它**。
- **file slice**：file group 在某个 instant 时刻有效的一个版本（base + 尚未合并的 log）。
  快照查询 = 对每个 file group 取"≤ 当前 instant 的最大 slice"；增量查询 = 两 instant 之间"slice 变了的那些 file group 的差分"。
- **COW 也有 file slice**：每次重写 base file 就是新 slice，旧 slice 在 cleaner 保留窗口内仍供增量/CDC 读。

### 2.6 高级用法：写入 API 的形状

```sql
-- CTAS：从源表整表引导一张 Hudi 表（bulk 语义，文件按 sort 切）
CREATE TABLE hudi_customers USING hudi
TBLPROPERTIES (type='cow', primaryKey='id', preCombineField='ts')
AS SELECT /*+ BROADCAST */ * FROM src.customers;

-- MERGE INTO：部分列更新（matched update 只覆盖指定列）
MERGE INTO retailmax.customers t
USING stg.updates s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.name = s.name, t.ts = s.ts
WHEN NOT MATCHED THEN INSERT *;

-- 非记录键字段更新：WHERE 走全表扫描 + bloom/记录索引定位 file group
UPDATE retailmax.customers SET name='x' WHERE city='Shanghai';   -- 无 city 索引时很贵（第 5 章）
```

- 书中强调：**按非记录键更新/删除是可行但昂贵的操作**——定位"哪些文件含 city=Shanghai"依赖列统计/索引，这正是第 5 章 functional index、metadata 表 column stats 的动机。
- bulk insert（`operation=bulk_insert`）绕过索引与自动文件定尺，速度接近纯 Parquet（第 9 章也再提）。

### 2.7 时间旅行与增量查询（预览）

```sql
-- 时光回溯：按版本或按时间
SELECT * FROM customers VERSION AS OF '20260925101500000';
SELECT * FROM customers TIMESTAMP AS OF '2026-09-25 10:20:00';
-- 增量：某 instant 之后的所有变化（官方 Spark 读选项口径，第 4 章详解）
CREATE OR REPLACE TEMP VIEW customers_incr
USING hudi
OPTIONS (type = 'cow',
         path = 's3://lake/hudi/retailmax/customers',
         hoodie.datasource.query.type = 'incremental',
         hoodie.datasource.read.begin.instanttime = '20260925101500000');
SELECT * FROM customers_incr;
```

四种读法（snapshot / read-optimized / incremental / time-travel）的完整语义与 CDC 扩展在第 4 章。

## 版本演进

| 行为 | 0.1x | 1.x（本书基线） |
| --- | --- | --- |
| 默认索引 | BLOOM | 推荐 RECORD_INDEX（依赖 metadata table） |
| metadata table | 可选（0.9 引入，0.10 扩展） | 默认创建，承载 record index/column stats |
| MOR log 块格式 | 默认 Avro block | 推荐 `hoodie.log.record.reader.write.format=PARQUET` 混合格式 |
| CTAS/MERGE 语法 | 依赖 spark 扩展 | Spark Catalog API 支持 MERGE INTO / 存储过程 |
| hudi-rs 读 | 无 | 🔧 Rust/Python 可只读 Hudi 表（第 4 章展开） |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "MOR 表读到的永远是最新值" | snapshot 读才是最新值；read-optimized 只读 base file，故意旧 |
| "timeline 文件名时间戳=提交完成时间" | instant time 是**请求时刻**；完成时刻记录在 completed instant 的内部元数据里（archived 后亦然） |
| "COW 更新只是追加" | COW 每次 upsert 重写受影响 file group 的整个 base file，小文件反而被"顺带整理"，大文件则代价高（这是 clustering/写侧分桶存在的原因） |
| "分区改了没事" | record key 含分区路径：同一逻辑行换分区在 Hudi 里是"删+插"，破坏 upsert 幂等（03 章 partition schema 展开） |
| "rollback 需要人工触发" | 新写入会自动回收悬挂 inflight；人工 rollback 用于修复长时间失败留下的 inflight（第 9 章表操作） |

## 与其他章 / 其他笔记的联系

- 2.3 timeline 三态 → [07-Hudi中的并发控制.md](07-Hudi中的并发控制.md)（冲突检测就发生在 inflight→completed 之间）；[06-维护与优化Hudi表.md](06-维护与优化Hudi表.md)（表服务同样以 requested/inflight/completed 生命周期运行，"schedule vs execute"由此而来）。
- 2.5 file slice → [04-从Hudi读.md](04-从Hudi读.md)（增量/CDC 读 = slice 差分）。
- 2.1 preCombine / 2.6 merge → [03-写入Hudi.md](03-写入Hudi.md)。
- OLTP 视角对照：instant 三态 ≈ MySQL redo 的 mtr + checkpoint；"completed 文件出现即原子可见" ≈ binlog event 的原子组提交（[../../db/db.md](../../db/db.md)）。
- 文件格式基线：[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)；Spark SQL 扩展点：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。
