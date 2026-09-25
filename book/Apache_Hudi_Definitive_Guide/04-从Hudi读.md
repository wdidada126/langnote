# 第 4 章 从 Hudi 读

> 原书章题（译系列核实）：从 Hudi 读。小节地图：与查询引擎的集成（查询生命周期、数据目录）→ 探索查询类型（快照、时光回溯、增量 latest_state、增量 CDC 模式）→ 值得关注的读侧特性（流式读取、读时模式演进、Rust/Python 读取、生态集成）→ 总结。
> 机制口径以官方文档 Query Types / Tables 各页为准。

## 本章地图

> 一句话：**Hudi 的读 = 在 timeline 上选一个"版本视图"（snapshot/read-optimized/time-travel/incremental），再把视图翻译成 file slice 集合交给引擎扫描；CDC 只是把切片差分发成 changelog。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 查询生命周期 | 引擎下推 → Hudi 解析 instant → 规划文件切片 → 谓词/统计裁剪 → scan | 表格式是"读规划器"，不是存储格式 |
| 4.2 数据目录的角色 | Hive/Glue/JDBC 目录存表指针与 schema | 目录滞后 = 查不到新分区（第 9 章 sync） |
| 4.3 快照查询 | 当前 instant 的 latest slices | COW 无脑快；MOR 要现场 merge |
| 4.4 读优化查询 | 只读 base file | 换延迟不保新鲜度 |
| 4.5 时光回溯 | 按 instant / 按日期取历史快照 | 依赖 cleaner 保留窗口（第 6 章） |
| 4.6 增量查询 latest_state | (begin, end] 区间内每 key 最终态 | ETL 间微批搬运 |
| 4.7 增量查询 CDC 模式 | 输出 op/before/after 三件套 | 供下游流式重放（第 8/10 章） |
| 4.8 流式读取 | Flink/Spark structured streaming 消费 timeline | 拉模型：跟 instant 走 |
| 4.9 读时模式演进 / 多引擎 | 按查询 instant 还原 schema；Trino/Hive/Rust/Python | 异构生态统一读 |

## 核心精讲

> **教学示意，不参与构建。**

### 4.1 查询生命周期：读规划发生在哪

```text
SELECT ... WHERE dt='2026-09-25' AND age > 30
  ① 引擎（Spark/Trino/Flink）把表识别为 Hudi 关系，解析 query type 选项
  ② Hudi 读 timeline：确定目标 instant（当前/历史/区间）
  ③ 文件规划：
     - 从 commit 元数据 / metadata 表拿到候选 file slices
     - 分区裁剪（dt=...）
     - 列统计 data skipping（min/max/null count；第 5 章）
     - MOR：判断哪些 file group 带 log（需要 merge read）
  ④ 引擎扫描 Parquet（谓词下推到 row group/page index）
  ⑤ MOR snapshot 读：在扫描任务内把 log block merge 进 base
```

- 关键认知：**②③ 是 Hudi 独有的开销与价值**。裸表没有 ②，规划质量全靠目录分区；Hudi 把"哪些 slice 属于这个快照"变成确定性元数据查询。
- metadata 表加速 ③（files/column_stats partition）；元数据不全或过期时回退 .hoodie 元数据扫描（第 5 章）。

### 4.2 数据目录

- 表的"可发现形态"= catalog 里的 location + schema + 分区列表；Hudi 不自动维护它们，靠 **Hive Sync Tool / 自动同步**（第 9 章）。
- 直连 path 读（Spark `format("hudi").load(path)`）可完全绕开 catalog——调试时常用，生产要防止"查到一份没同步的旧 schema"。

### 4.3–4.4 快照 vs 读优化

```sql
-- 快照读（默认）：MOR 表 = base + log 合并后的最新态
SELECT count(*) FROM mor_orders;

-- 读优化（MOR 专属）：只扫 base file，等价"上次 compaction 时刻的快照"
SELECT * FROM orders /*+ OPTIONS('as.of.instant'='20260925090000000') */; -- 示意
-- Spark 官方开关：hoodie.datasource.query.type = snapshot | read_optimized
```

- COW 表两者退化为同一物（无 log）。
- 读优化是 BI 高并发场景的减压阀：新鲜度要求 ≤ compaction 周期的报表直接走 base。

### 4.5 时光回溯（Time Travel）

```sql
SELECT * FROM customers VERSION AS OF '20260924...';          -- Spark 语法
SELECT * FROM customers TIMESTAMP AS OF '2026-09-24 00:00:00';
-- Trino: FOR SYSTEM_VERSION AS OF / FOR SYSTEM_TIME AS OF
```

- 实现 = 把"目标 instant"塞进 4.1 的 ②，选 ≤ 该 instant 的 slices。
- **能回溯多远由 cleaner 决定**（`hoodie.clean.commits.retained` 默认 10、`hoodie.keep.min/max.commits` 与归档）；超窗口的请求会落到最近的可用快照或报错（第 6 章 cleaning，第 9 章 savepoint 可钉住版本）。

### 4.6 增量查询：latest_state 模式

```sql
CREATE OR REPLACE TEMP VIEW incr
USING hudi
OPTIONS (type='cow', path='...',
  hoodie.datasource.query.type='incremental',
  hoodie.datasource.read.begin.instanttime='20260925000000',   -- 必填
  hoodie.datasource.read.end.instanttime='20260925060000');    -- 选填（不填=到当前）
```

- 语义：区间内**每个 key 的最终态**（一 key 多次变更只输出最后一次）。
- 用途：Bronze → Silver 的链式微批——下游把自己的消费位点记成 begin instant（第 8 章 Hudi source 的机制）。
- 删除如何体现：latest_state 模式下删除记录默认也输出（带 delete 标记列），由下游决定落地。

### 4.7 增量查询 CDC 模式 🔧（1.x 重点）

- 开关：表属性 `hoodie.table.cdc.enabled=true`；查询选项 `hoodie.datasource.query.incremental.format = cdc`（增量读格式三选一：`latest_state` / `cdc` / `raw_convert`，官方口径）。
- 输出列：`_hoodie_operation`（i/u/d/b/r）、`_hoodie_before_image`（struct）、`_hoodie_after_image`。
- **实现要点**：
  - i/u/d 由 merge 阶段捕获（需要写侧付出一点序列化开销；`hoodie.table.cdc.supplemental.logging.mode` DATA_BEFORE / DATA_BEFORE_AFTER）。
  - **before image 从 base file 现算**：MOR 表的 log 里只有更新后的值，旧值要去 base 拿——这意味着 CDC 读 MOR 也吃 merge 成本。
  - 部分引擎（如 Flink 流读）把 Hudi CDC 直接映射为 changelog（+I/-U/+U/-D）。
- 与 Debezium 对照（第 8、10 章互见）：Debezium 在**源库 binlog 层**出 changelog；Hudi CDC 在**湖仓提交层**重放变更——后者让"湖内加工的每一跳都可被再订阅"。

### 4.8 流式读取

- **Flink**：source 以 streaming 模式跟踪 timeline，新 instant 到达即下发增量 splits；changelog 模式依赖 4.7。
- **Spark Structured Streaming**：`format("hudi").option("structure_streaming_source", true)`（官方口径：read streamed batches）+ `Trigger`；micro-batch 模式下每个 trigger 区间 = 一次增量查询。
- 流读把 Hudi 变成"带存储的 broker"：下游可以任意时刻重放（受保留窗口约束），对比 Kafka 的 offset 保留策略——这是湖仓版 CDC 的核心卖点（姊妹书《Kafka 权威指南》主题在本仓库有文字对照）。

### 4.9 读时模式演进与多引擎生态

- **Schema on read**：按目标 instant 还原当时 schema 读历史数据（新列补 null / 改名映射），保证"历史按历史的样子呈现"。
- 官方支持面（Query Engine 页）：Spark、Flink、Hive、Presto/Trino、Impala、Doris/StarRocks（第三方）、Kafka Connect sink。
- **hudi-rs / hudi-python** 🔧：Rust crate 与 Python 绑定提供 DataFrame 级只读（timeline 解析 + Parquet 读取），供 Ray/Daft 等无 JVM 栈读取湖仓——第 10 章"用 Ray 为 LLM 构建知识库"的技术底座。

## 版本演进

| 能力 | ≤0.12 | 1.x（本书基线） |
| --- | --- | --- |
| CDC 查询 | 无（只能靠 incremental 模拟） | 原生 op/before/after 列 🔧 |
| 增量读 MOR | 支持但 merge 成本不可见 | 与 compaction 解耦，可配 supplemental logging 档位 |
| 引擎面 | Spark/Flink/Hive 为主 | + Trino/Impala/Doris 成熟、hudi-rs Python 只读 🔧 |
| 读规划元数据 | 扫 .hoodie 文件 | metadata 表（files/column_stats）加速 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "read-optimized 是 Hudi 特有名词" | 本质是"读上次 compaction 的快照"——等价于把 freshness 换成 compaction lag |
| "增量查询会给出所有中间变更" | latest_state 只给终态；要中间变更（回撤序列）必须用 CDC 模式 |
| "time travel 无限回溯" | 受 cleaner 保留与归档窗口限制；长期审计需求要用 savepoint 钉住（第 9 章） |
| "catalog 和表是一回事" | catalog 只是指针与分区缓存；不 sync 时新分区在 Hive/Trino 里不可见，是新手第一大坑（第 9 章） |
| "CDC before image 存在事务元数据里" | 默认不存整行；读时从 base file 取旧值（supplemental logging 决定存不存） |

## 与其他章 / 其他笔记的联系

- 4.1 的列统计裁剪 → [05-索引与元数据表.md](05-索引与元数据表.md)；4.5 的保留窗口 → [06-维护与优化Hudi表.md](06-维护与优化Hudi表.md) cleaning。
- 4.6/4.7 是 [08-基于HudiStreamer构建数据湖仓.md](08-基于HudiStreamer构建数据湖仓.md) Hudi-as-source 的引擎侧前提，也是 [10-构建端到端的湖仓解决方案.md](10-构建端到端的湖仓解决方案.md) 分层链路的血液。
- OLTP 对照：4.5/4.3 = 数据库的 AS OF（Oracle Flashback / MySQL binlog 重放）在湖仓的廉价版——因为文件天然多版本（[../../db/db.md](../../db/db.md)）。
- 流语义背景：[../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)；查询引擎侧：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)、[../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。
