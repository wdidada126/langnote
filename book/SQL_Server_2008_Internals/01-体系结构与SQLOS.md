# 01 体系结构与 SQLOS（原书 ch1 System Architecture + ch2 The SQLOS）

> 状态标注：⚠️ = SQL Server 引擎二手转述（本机不可实测）；✅ = Microsoft Learn 现行文档（写前 curl -sL 200）；🔧 = 本机 SQLite/DuckDB 类比，**非本书 SQL Server 引擎行为**。

## 一、本章地图

本章覆盖内幕卷的"世界观"层：SQL Server 进程如何被切成两大引擎、以及内嵌于进程内的操作系统抽象 SQLOS。后所有章（存储/日志/查询/锁）都运行在这套骨架上。

- 1A 关系引擎 vs 存储引擎的二分法
- 1B 查询处理管道：解析→绑定→优化→执行
- 1C SQLOS：内存管理、调度器、异常/IO 封装、等待统计
- 1D Worker、Scheduler、Ums 与协作式调度
- 1E Buffer Pool、Memory Node、外部资源与内存压力

## 二、核心精讲（⚠️ 转述）

### 2.1 关系引擎与存储引擎二分（⚠️）

SQL Server 进程（`sqlservr.exe`）在逻辑上分成两半：**关系引擎（Relational Engine / Query Processor）**负责"要做什么"——查询解析、查询编译、优化与执行计划生成；**存储引擎（Storage Engine）**负责"怎么存取"——数据在页/ extent 中的布局、事务日志写入、缓冲池管理、锁与恢复。两者通过一种称为 **ES（Engine-Storage）接口/调用协议** 的边界对话：关系引擎发出对某行/某索引的操作意图，存储引擎执行并返回数据流（⚠️ 依 Delaney 团队公开架构描述转述）。

这一"查询处理架构"的现代官方表述见 ✅ Learn：[Execution plans](https://learn.microsoft.com/en-us/sql/relational-databases/performance/execution-plans)（写前 200 验通，见文末链接清单）；算子级观测口径与执行计划概念同源。

### 2.2 SQLOS：进程内嵌的"迷你操作系统"（⚠️）

2005 版起，SQL Server 把一批 OS 原语在用户态自行实现，即 **SQLOS（SQL Server Operating System）**，目的是：跨 Windows 版本行为一致、细粒度资源调度、可观测的等待/诊断。四大子系统（⚠️）：

- **Memory Manager（内存管理器）**：把可用内存切成 **Buffer Pool（缓冲池）** 与 **Memory Clerks（内存 clerk）**；`max server memory`/`min server memory` 划定目标；NUMA 场景下按 **Memory Node** 分区。缓冲池缓存数据页，clerk 服务编译、锁、计划缓存等"非页"内存。
- **Scheduler / OS 调度层**：每个逻辑 CPU 对应一个 **Scheduler（调度器）**，其上有 **Worker（工作线程）** 执行请求；SQL Server 用**协作式（cooperative）调度**——worker 主动让出，而非抢占，减少上下文切换开销。
- **Exception Handling / Debug**：把访问违例、死锁等包装成可控异常，避免拖垮整进程。
- **IO Completion / 异步 IO**：封装数据文件/日志文件的读写完成端口，向存储引擎提供异步 IO。

### 2.3 等待统计与可观测性（⚠️）

SQLOS 把每次 worker 让出 CPU 都归因为一次"等待（wait）"，累计进 `sys.dm_os_wait_stats`——这是 2008 排错体系的基石，也是本波兄弟 #68《Advanced Troubleshooting》整册的主战场。✅ Learn：[sys.dm_os_wait_stats](https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-wait-stats-transact-sql)。

## 三、🔧 类比实验（非本书 SQL Server 引擎行为，仅通用机制演示）

SQL Server 的 SQLOS 无法本机复现（⚠️），但"缓冲/等待/调度"的通用直觉可用可跑的引擎类比：

- **🔧-A 缓冲池 ≈ SQLite page cache**：SQLite 的 `PRAGMA cache_size` 决定内存中缓存的页数，命中免 IO、未命中回读磁盘——与 SQL Server Buffer Pool 缓存 8KB 页同构（机制类比，非同一实现）。
- **🔧-B 内存 clerk ≈ DuckDB buffer manager**：DuckDB 用统一 buffer manager 在内存上限内换入换出数据块（可 spill 到临时目录）；`duckdb_settings()` 可观察 memory_limit 生效，类比 SQL Server 在 `max server memory` 下的内存再分配压力。
- **🔧-C 等待统计的"计数累加"范式**：SQLite 无 DMV，但 `EXPLAIN QUERY PLAN` 与 `PRAGMA` 计数器（如 `cache_hit`）体现了"可观测计数"的同类思想；DuckDB `PRAGMA enable_profiling` 给出算子级耗时，与 SQL Server 等待/算子统计的观测目标一致（仅类比，非 SQL Server DMV）。
- **🔧-D 协作式调度 ≈ 单线程事件循环**：SQLite 默认单写者、协作推进事务；DuckDB 并行执行用固定 worker 池、算子间协作拉取数据——两者都体现"少抢占、多让出"的调度哲学（类比，非 SQL Server scheduler）。

> 以上数字与行为均来自本机 SQLite 3.45.3 / DuckDB 1.5.5；SQL Server 的内存 clerk/scheduler 内部一律 ⚠️ 转述，不做实测伪装。

## 四、与其他章/笔记的联系

- SQLOS 内存/缓冲是 [02-数据库与数据库文件.md](02-数据库与数据库文件.md) 页与缓冲池、[04-表存储.md](04-表存储.md) 行存取的运行前提。
- 调度/等待→ [07-查询处理优化器与计划缓存.md](07-查询处理优化器与计划缓存.md) 的并行度与执行。
- 与同社 #36 [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md) 的体系结构章互旁证；#56 [../SQL_Server_2012_Internals/00-总览与阅读地图.md](../SQL_Server_2012_Internals/00-总览与阅读地图.md) 将本"体系结构"扩展为 2012 的配置与列存/内存 OLTP 前置。
- 通用内核理论对照 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)。

## 五、常见误区（⚠️）

- 把 SQLOS 当"完整 OS"：它是进程内用户态抽象，仍依赖 Windows 内核提供线程与 IO 完成端口（⚠️）。
- 把 `max server memory` 当硬上限：它约束缓冲池与 clerk 的目标，动态调整而非强制截断（⚠️）。
- 忽略协作式调度：一个长时间不释放 CPU 的 CLR/扩展过程会拖累同调度器上的其他 worker（⚠️）。

## 六、版本视角：2008 的边界

本章是"2008 版"内核描述：此时**没有**内存优化表（Hekaton）、列存储索引、`sys.dm_os_*` 中若干新 DMV，均 2012+ 才有，故本册凡涉列存/内存表一律 ⚠️ 前向引用 #56，不在 2008 章内臆造。

## 七、内存压力与换页（⚠️ 深入）

- **目标 vs 承诺 vs 可用**：SQLOS 维护"目标内存"（由 `min/max server memory` 与 OS 反馈共同决定）与"已承诺内存"，clerk 在压力下按可回收等级被要求释放；缓冲池因页可脏化/可回写，成为最灵活的压力缓冲垫（⚠️）。
- **写回与脏页**：被修改但未落盘的页称"脏页"，由检查点/lazy writer 异步回写（详见 [03-日志与恢复.md](03-日志与恢复.md)），保证内存吃紧时可安全丢弃干净页。
- **内存不足信号**：OS 内存压力事件触发 SQLOS 主动收缩，避免进入 Windows 交换文件（页面交换对数据库是性能毒药，⚠️）。

## 八、🔧 类比实验的命令级复现（非本书 SQL Server 引擎行为）

以下命令本机可跑，演示与上面 ⚠️ 段落同构的"通用机制"，但**不代表 SQL Server 实现**：

```sql
-- 🔧-A SQLite 缓冲池命中与页缓存（类比 Buffer Pool）
PRAGMA page_size = 4096;          -- 页为 IO/分配原子单位（SQL Server 固定 8KB，⚠️）
PRAGMA cache_size = -2000;        -- 负值=KB 预算：约 2000KB 内存缓存页
SELECT count(*) FROM big WHERE k > 1000;  -- 首次冷读、二次热读，感知"命中"差异

-- 🔧-B DuckDB 统一 buffer manager 与内存上限（类比 clerk 再分配）
SET memory_limit='256MB';
PRAGMA enable_profiling='query_tree';     -- 算子级耗时，类比等待/算子观测
SELECT cat, count(*) FROM t GROUP BY cat; -- 超限时向临时目录 spill

-- 🔧-C 观察 SQLite 页级占用（类比按对象记账）
PRAGMA page_count; PRAGMA freelist_count;  -- 页数/空闲页，近似"内存/空间账本"
```

> 数字见本册总览第八节 E1–E6 总表（`exp.py` 复现）。SQL Server 无 `PRAGMA`，其内存账本走 `sys.dm_os_memory_clerks`（⚠️），二者仅"可观测记账"思想同源。

## 九、常见问答（FAQ）

1. **问：SQLOS 是不是虚拟化层？** 答：不是。它是进程内用户态资源管理，仍跑在真实 OS/硬件之上（⚠️）。
2. **问：为什么协作式调度重要？** 答：worker 主动让出使调度开销低、上下文切换少，但代价是失控的长 CPU 操作会饿死同调度器其他 worker（⚠️）。
3. **问：2008 有列存/内存表吗？** 答：没有。它们分别是 2012 列存储索引与 2014 Hekaton，本册前向引用 #56/#71，2008 章内不写（⚠️ 硬边界）。
4. **问：能拿 SQLite 数字当 SQL Server 结论吗？** 答：绝对不能。🔧 只演示通用机制，页大小、分裂、等待范式皆"非本书 SQL Server 引擎行为"。

## 核心概念速览（中英对照）

- 关系引擎 — Relational Engine：查询解析/编译/优化的引擎侧，决定"要什么"。
- 存储引擎 — Storage Engine：页/日志/缓冲/锁的实现侧，决定"怎么存取"。
- SQLOS — SQL Server Operating System：进程内嵌的用户态 OS 抽象层。
- 缓冲池 — Buffer Pool：内存中缓存数据页的区域，命中免磁盘 IO。
- 内存 clerk — Memory Clerk：为编译/锁/计划等非页用途记账的内存消费者。
- 调度器 — Scheduler：与逻辑 CPU 一对一绑定的 worker 分发单元。
- 工作线程 — Worker：执行一条请求的单元，协作式让出 CPU。
- 等待统计 — Wait Statistics：worker 让出 CPU 的归因累计，排错基石。
- 内存节点 — Memory Node：NUMA 下按节点划分的内存分区。
- 执行计划 — Execution Plan：优化器产出的算子树，指导逐行/逐批取数。
- max server memory — max server memory：实例内存目标上限（动态非硬截）。
- 异步 IO — Asynchronous IO：SQLOS 封装的完成端口式读写。
- NUMA — Non-Uniform Memory Access：跨内存节点访问代价不均的硬件拓扑。

## 最新演进与工业实践

- 架构分层沿用至今：SQL Server 2022/2025 仍是"关系引擎 + 存储引擎 + SQLOS"三段式；SQLOS 在 Linux 版（SQL Server on Linux，2017 起）改由 PAL（Platform Abstraction Layer）承载，见 ✅ [SQL Server on Linux overview](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-overview)。
- 等待统计与 DMV 已成工业标准排错入口：现代工具（`sp_WhoIsActive` by Adam Machanic、`sp_Blitz*` by Brent Ozar 团队）封装 `sys.dm_os_wait_stats`/`sys.dm_exec_requests`，本波 #68 整册即此主题。
- 2012→2022 演进：内存 OLTP（Hekaton）、列存储、自动计划修正（Intelligent Query Processing）相继落地；体系结构内幕细节以 [../SQL_Server_2012_Internals/00-总览与阅读地图.md](../SQL_Server_2012_Internals/00-总览与阅读地图.md) 与 #71（2022 管理）为准。
- 参考与准绳（写前 curl -sL 200）：https://learn.microsoft.com/en-us/sql/relational-databases/performance/execution-plans；https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-os-wait-stats-transact-sql；https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexes-overview（后向引用列存）；https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/overview-and-usage-scenarios。404 候选 `performance/sql-server-memory-manager` 已弃用、不引。
- 工业口径：容量规划仍围绕 `max server memory` + 缓冲池命中 + 等待画像三件套；本页所有 SQL Server 数字结论为 ⚠️ 转述，非本机实测。
