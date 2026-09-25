# 第 6 章 维护与优化 Hudi 表（表服务）

> 原书章题（译系列核实）：维护与优化 Hudi 表。小节地图：表服务概览（Inline/Async/Standalone 三种部署模式与选型）→ 压缩 Compaction（Schedule/Execute）→ 聚类 Clustering（Schedule/Execute、布局优化策略、Clustering vs Compaction）→ 清理 Cleaning（Schedule/Execute）→ 索引 Indexing → 总结。
> 机制口径以官方文档 Table Services / Configs 为准。本章回答的问题是：**写便宜了，读的钱谁付？**

## 本章地图

> 一句话：**Hudi 把"数据库后台"搬进湖仓：compaction 还 MOR 的 merge 债、clustering 还布局债、cleaning 还快照债、archival/indexing 还元数据债；每种服务都拆成 schedule（在 timeline 上登记一个 requested instant）与 execute（真正干活）两拍。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 表服务总览 | 四种服务 + 三态生命周期复用 timeline | 服务=特殊 action 的写事务 |
| 6.2 部署模式 | Inline / Async / Standalone | 延迟、资源隔离、正确性的三角 |
| 6.3 Compaction | MOR log → base；触发策略与调度 | 大 log 拖垮读；小 log 拖垮调度 |
| 6.4 Clustering | 小文件合并 + 排序布局优化 | 唯一能"改变数据邻近性"的服务 |
| 6.5 Cleaning | 快照保留策略 | 决定 time travel/增量读的窗口 |
| 6.6 Archival | timeline 文件归档到 .hoodie/archived | 元数据有界性的来源 |
| 6.7 Indexing 服务 | 表达式/记录索引的后台物化 | 索引不再只随写维护 🔧 |
| 6.8 Rollback/Savepoint/Restore | 事故修复与版本钉住 | 与运维章共用的表操作 |

## 核心精讲

> **教学示意，不参与构建。**

### 6.1 为什么需要"表服务"

```text
写侧的每笔"便宜"都在攒债：
  MOR 追加 log        → 读放大债     → compaction
  高频小批 upsert      → 小文件/布局债 → clustering
  每次 commit 新版本   → 存储与元数据债 → cleaning + archival
  表达式索引失效       → 索引债       → indexing 服务
表服务 = 以 timeline 事务形式偿还这些债（replacecommit/compaction/clean/indexing instant）。
```

### 6.2 三种部署模式（书中核心对比）

| 模式 | 机制 | 优点 | 代价 |
| --- | --- | --- | --- |
| Inline | 写入作业末尾同作业执行（如 `hoodie.compact.inline` + `hoodie.compact.inline.max.delta.commits`） | 零额外编排，强一致还债 | 写延迟毛刺、资源混抢 |
| Async（schedule+execute 分离） | 写作业只 schedule；独立异步作业/线程 execute（Spark 过程 `run_compaction` / `run_clustering` 等） | 写路径干净；资源隔离 | 新鲜度取决于调度频率 |
| Standalone | 专职服务持续循环（1.x 的 table service 守护作业：Spark 过程/CLI 的 table_service、Flink 专用作业） | 多表统一治理、最灵活 | 多一个运维对象 |

- 选型一句话（与书中"如何选型"一致）：**单作业小表用 inline；生产大表用 async/standalone 并纳入监控（第 9 章）**。
- 1.x 新增连续守护形态：table service 可作为独立进程持续监听多张表的 timeline 并轮转执行各类服务（参数与作业模板以官方文档为准，本目录只记模式不背名字）。🔧

### 6.3 Compaction：MOR 的读侧清算

```text
Schedule（写 <t>.compaction.requested）：
  选择策略挑出待压 file group（候选：带 log 的 slice）
Execute：
  读 base + log blocks 按 key merge → 重写新 base file → <t>.compaction (completed)
  旧 base 保留至 cleaning 窗口外（所以 compaction 后仍能增量读）
```

- 调度策略（官方 `hoodie.compaction.strategy`）：
  - `LogFileSizeBasedCompactionStrategy`（旧默认）：log 总大小/条数阈值。
  - `BoundedIOCompactionStrategy`：单轮 I/O 预算内尽量多压。
  - `UnBoundedCompactionStrategy`：全部候选都压。
  - 更细的策略族（含按 log 块大小/条数组合判断）以官方 Compaction 文档为准。
- 关键参数（教学口径）：`hoodie.compact.inline`、`hoodie.compact.inline.max.delta.commits`（N 个 deltacommit 后必压）、`hoodie.compaction.payload.class`（列投影裁剪 payload）。
- **资源账**：compaction 是重 I/O 重写作业；MOR 表吞吐 = min(写吞吐, compaction 吞吐)。第 10 章案例里"银层延迟劣化"的根因几乎都是 compaction 欠债。

### 6.4 Clustering：布局的再设计

```text
触发：schedule_clustering → pending_clustering instant；执行时把受影响分区整体
     重写为一组"新排布"的文件 → 一次 replacecommit 原子切换
能做两件事：
  ① binpack：小文件合并到目标大小（hoodie.clustering.plan.strategy.sortColumns 不填即纯 binpack）
  ② sort：按列排序/分区内分桶排序（lineal / greedy 策略）→ 直接提升 column_stats 跳过率（第 5 章）
参数族：hoodie.clustering.plan.strategy.*（sortColumns / 单文件目标大小 / 分区内分桶数等）、
        执行侧 hoodie.clustering.execution.strategy.class
```

- **Clustering vs Compaction（书中专门对比）**：
  - 对象：compaction 处理"带 log 的 file group"；clustering 处理"分区的文件布局"。
  - 结果：compaction 不改变 key→file 的归属；clustering 大改归属（所以必须 global index 或分区内全重建，且与 record index 有交互）。
  - 语义：clustering 走 `replacecommit`（旧文件集整体换新，原子切换），compaction 走 `compaction` instant。
- 布局优化策略（书中术语 "Layout Optimization Strategies"）：按查询热点列重排历史数据、对增量分区做渐进 clustering（小文件目标大小与 sort 列由 clustering plan strategy 参数族控制，口径以官方 Configs 页为准）。
- 小文件治理组合拳：写侧（03 章 partitioner 的 file sizing）+ 桶索引重算（5.4）+ clustering 三选一，**不要用 cleaning 兜小文件**。

### 6.5 Cleaning：快照保留的天平

```text
策略（hoodie.clean.policy；旧文档名 hoodie.cleaner.policy，版本间命名有迁移）：
  KEEP_LATEST_COMMITS（默认）：保留最近 N 个 commit 的可读快照
      保留数 = hoodie.clean.commits.retained（旧名 hoodie.cleaner.commits.retained，默认 10）
      → 增量/time travel 窗口 ≈ 10 个 commit
  KEEP_LATEST_FILE_VERSIONS：每个 file group 保留 M 个版本（默认 2）
另有时间维：hoodie.clean.hours.retained 与 hoodie.keep.min/max.commits 控制 timeline 长度
```

- cleaner 删的是"没有任何在保留窗口内快照引用的旧文件/log"。
- 窗口设置经验（书中口径同官方建议）：**长查询/慢消费者会读不到文件（FileNotFoundException）**——保留窗口必须覆盖最慢的合法读者；钉死关键版本用 savepoint。
- MOR 表若 compaction 不及时，cleaner 反而不能清理旧 base（还被引用）——三服务互相牵制。

### 6.6 Archival 与 timeline server

- 完成的 instant 文件超阈值后移入 `.hoodie/archived/`（`hoodie.keep.max.commits` 默认 30 等）；查询读窗口由元数据服务器（FileSystemView/timeline server）缓存加速（第 9 章性能调优）。

### 6.7 🔧 Indexing 表服务

- 表达式/函数索引、记录索引的重建等不再只能"写时顺带维护"：`schedule_indexing` / `run_indexing`（或 `indexing` 过程）异步物化 `functional_index` partition。
- 含义：**可以为"上线后才出现的查询"补建湖仓级索引**，这是本书标题强调 "self-managing tables" 的一部分。

### 6.8 同族操作：rollback / savepoint / restore

| 操作 | 语义 | instant |
| --- | --- | --- |
| Rollback | 清理失败的 inflight / 撤销一次坏提交 | `.rollback` |
| Savepoint | 给某 commit 打"不可清理"标记 | `.savepoint` |
| Restore | 把表回滚到某 savepoint/instant | `.restore` |

- 第 9 章表操作、第 10 章"数据韧性"直接复用。

## 版本演进

| 项 | 0.1x | 1.x |
| --- | --- | --- |
| 表服务形态 | inline 为主，手动 compaction 作业 | async + standalone（专职 table service 作业）成熟 🔧 |
| Clustering | 早期 schedule/execute 双文件 | 统一到 replacecommit + pending_clustering，布局优化策略扩展 |
| Indexing | 无独立服务 | functional index 异步维护 🔧 |
| 压缩策略 | 阈值型单一 | BoundedIO 等预算型策略 |

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "MOR 不 compaction 也能跑，只是慢一点" | log 无限堆积时 snapshot 读退化为"打开每个 file group 全部 block"，且元数据开销线性涨——是悬崖不是缓坡 |
| "clustering 等于 compaction" | 对象、instant、对索引的影响全不同（6.4 对比表） |
| "cleaning 是 GC，越大越好" | 保留窗口直接换算存储成本与 time travel 窗口；"顺手多留点"是湖仓账单失控的常见原因 |
| "inline 表服务最省心所以默认选它" | 生产上写延迟毛刺会传染上游 SLA；书与官方都倾向 async/standalone |
| "savepoint 能防误删数据" | savepoint 只防 cleaner 清理；文件被物理删（purge/外部 rm）救不回来 |

## 与其他章 / 其他笔记的联系

- 6.2/6.3 的资源隔离与 9 章监控指标联动 → [09-Hudi生产级部署与运维.md](09-Hudi生产级部署与运维.md)；6.4 的排序↔跳过 → [05-索引与元数据表.md](05-索引与元数据表.md) 5.7。
- 6.5 的保留窗口决定 4 章 time travel/incremental 边界 → [04-从Hudi读.md](04-从Hudi读.md)。
- compaction/clustering 是 Spark/Flink 批作业 → 执行层背景 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)；Flink 侧 compaction（TaskManager 内或独立作业）与 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md) 相关。
- OLTP 对照：cleaning ≈ vacuum/purge、archival ≈ binlog 截断、compaction ≈ LSM major compaction（[../../db/db.md](../../db/db.md)、《RocksDB/LSM 类》书目文字提及）。
