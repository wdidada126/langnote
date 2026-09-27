# 第 12 章精读重构——优化 MySQL 8

> 原书章题：Optimizing MySQL 8（✅ 英题由代码包文件名实证：`B08055_Ch_12_Optimizing MySQL 8_Queries.sql`）；
> 中题 ✅ 社区译本。本文件为**精读重构**；调优语义以 8.0 手册主题域转述（⚠️），镜像 ✅ 200 核验：
> https://mysql.net.cn/doc/refman/8.0/en/performance-schema.html 、 .../explain.html 、 .../optimizer-hints.html 、
> .../resource-groups.html 、 .../slow-query-log.html 。

## 12.1 本章定位

书内调优章的体裁：**参数表 + 观测器 + 一条"看计划"方法论**，深度刻意停在"入门"——
北极星世界观（性能=查询响应时间）在 #45 已成体系，本章提供的是 MySQL 8 侧的仪表盘读法与旋钮清单。
读法：把每条建议都当作"先在 8.0 上验证统计口径，再谈调"。

## 12.2 观测三件套（⚠️ 转述）

1. **慢查询日志**：`long_query_time`（0.5–1s 起步）、`log_queries_not_using_indexes` 慎用（噪声）；
   `mysqldumpslow`/`pt-query-digest` 聚合出"总耗时 TopN"——digest 思想与 #45 第 1 章同源。
2. **performance_schema**：语句/等待/锁/复制四类 instrument 矩阵；`events_statements_summary_by_digest`
   是"哪类 SQL 吃掉了这个实例"的第一张表；sys schema 是其人类可读视图。
3. **状态计数器**：`SHOW GLOBAL STATUS` 差分（每秒化）：`Innodb_buffer_pool_reads` vs `read_requests`（命中率）、
   `Innodb_row_lock_*`、`Threads_running`（并发真实热度）——对读
   [../Efficient_MySQL_Performance/06-服务器指标与InnoDB.md](../Efficient_MySQL_Performance/06-服务器指标与InnoDB.md) 的光谱法。

## 12.3 优化器与执行计划（⚠️ 转述，✅ explain 页）

- `EXPLAIN` 列语义（type/key/rows/filtered/Extra）+ `EXPLAIN FORMAT=TREE`（8.0.18+）+ `EXPLAIN ANALYZE`
  （真执行、逐节点耗时/行数——8.0 调优最大增量）；机制纵深链到
  [../mysql/15-EXPLAIN详解.md](../mysql/15-EXPLAIN详解.md)、[../mysql/12-基于成本的优化.md](../mysql/12-基于成本的优化.md)、
  [../mysql/13-统计数据.md](../mysql/13-统计数据.md)、[../mysql/16-optimizer-trace.md](../mysql/16-optimizer-trace.md)。
- **直方图**：`ANALYZE TABLE t UPDATE HISTOGRAM ON col WITH 32 BUCKETS`（等高/TopN），补非索引列与相关性的统计盲区；
  与持久化统计（innodb_table_stats）双轨，`innodb_stats_transient_persistent` 口径别混（⚠️）。
- **优化器提示**：`/*+ INDEX(t idx) NO_BNL() JOIN_ORDER() */`——应急止痛药，入仓须带注释与退出计划（✅ optimizer-hints 页存在，用法 ⚠️）。
- 8.0 移除清单生效：查询缓存消失、`query_cache_*` 变死变量；所有"qc hit ratio"旧报表下线。

## 12.4 资源与参数主线（书内旋钮的 2026 复核）

| 旋钮 | 作用域 | 现状备注 |
| --- | --- | --- |
| innodb_buffer_pool_size(/instances/chunk) | 热数据驻留 | 仍是第一旋钮；云实例内存比例论不变 |
| innodb_redo_log_capacity（8.0.30+） | 写峰值缓冲/恢复时长 | 取代 log_file_size×组；书内旧口径要做翻译（⚠️） |
| innodb_io_capacity(_max) | 刷脏节奏 | 按实测 SSD 校准，别抄"1000/2000" |
| innodb_flush_log_at_trx_commit + sync_binlog | 持久化/性能交换 | "双 1"锚点，08 章已展开 |
| max_connections + thread handling | 连接风暴 | 线程池属企业版/Percona 线（社区默认一连接一线程 ⚠️） |
| replica_parallel_workers(+_type) | 回放吞吐 | WRITESET 依赖追踪解锁并行（08 章演进） |
| resource groups（CAP_SYS_NICE） | CPU 亲和/优先级 | 给批任务钉核，防"吵闹邻居"（✅ resource-groups 页；14 章联动） |

## 12.5 🔧 类比边界声明

- 本册 🔧 义务已由 04/05/07/08/09/11 章超额兑现（≥4 组，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第六节）；
  本章主题（buffer pool/统计信息/等待事件）在 SQLite/DuckDB 上**无诚实对位物**（无共享缓冲池、无成本统计面板），
  如实 ⚠️；唯一可借的直觉是 07 章"索引是优化器的建议不是命令"实验——它正是本章 12.3 方法论的跨引擎注脚。

## 12.6 与 repo 的分工与互链

- 性能观（先读）：[../Efficient_MySQL_Performance/01-查询响应时间.md](../Efficient_MySQL_Performance/01-查询响应时间.md)；
  索引决策：[../Efficient_MySQL_Performance/02-索引与索引编制.md](../Efficient_MySQL_Performance/02-索引与索引编制.md)。
- 机制底图：[../mysql/12-基于成本的优化.md](../mysql/12-基于成本的优化.md)、[../mysql/13-统计数据.md](../mysql/13-统计数据.md)、
  [../mysql/16-optimizer-trace.md](../mysql/16-optimizer-trace.md)、[../mysql/17-调节磁盘和CPU的矛盾.md](../mysql/17-调节磁盘和CPU的矛盾.md)。
- 中文调优谱系：[../MySQL8查询性能优化.md](../MySQL8查询性能优化.md)（Krogh，同 8.0 语境最接近本章）、
  [../千金良方_MySQL性能优化金字塔法则.md](../千金良方_MySQL性能优化金字塔法则.md)、[../数据库高效优化.md](../数据库高效优化.md)。
- 跨引擎指标法：[../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)
  （wait stats ↔ events_waits 的镜像读法，#45 00 已示范该互链句式）；Oracle 等待事件谱系
  [../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)（✅ 盘上登记）。
- 论文线：成本模型经典文献登记 [../../db/db.md](../../db/db.md)。

## 12.7 本章任务清单（自测）

1. 用 digest 表写出"本实例过去 7 天 Top10 总耗时"查询的伪 SQL 结构（列名以手册 ⚠️）；
2. 给"rows 估计严重偏小导致错走索引"的病例开三张处方（ANALYZE/直方图/hint）与各自副作用；
3. 说明 EXPLAIN ANALYZE 与 EXPLAIN 的成本差异（真执行=真写压力，生产慎用场景清单）；
4. 为混部实例设计 resource group 方案：批任务降权+OLTP 钉核（联动 14 章基线）。

## 核心概念速览（中英对照）

- **慢日志聚合** — slow log digest：按参数化指纹归并 SQL，找"总耗时冠军"而非"最慢个案"。
- **performance_schema** — 实例内仪器矩阵：语句/等待/阶段/锁/复制五大表族（✅ performance-schema 页）。
- **sys schema** — 人类视图层：p_s 的报表化封装，巡检 SQL 起手式。
- **EXPLAIN ANALYZE** — 8.0.18+ 真实执行画像：逐节点 actual time/rows/loops。
- **直方图** — histogram：列值分布桶（等高/TopN），非索引列选择率的官方补丁。
- **优化器提示** — optimizer hints：块级注释干预计划，应急属性，须配退出计划。
- **buffer pool 命中率** — read_requests vs disk reads：第一健康指标，但"低命中≠有病"要看工作集（⚠️ 判据）。
- **redo 容量** — innodb_redo_log_capacity：写洪峰缓冲与恢复时长的调节器（8.0.30+ 口径）。
- **threads_running** — 活跃线程数：并发风暴的领先指标，比 threads_connected 诚实。
- **resource group** — 资源组：线程绑核/优先级（CAP_SYS_NICE），吵闹邻居的内治法。
- **自适应哈希 AHI** — 等值热页加速：命中率低时关持有收益的争议旋钮（⚠️）。
- **查询缓存遗产** — query cache legacy：8.0 整层移除，一切旧经验的第一条作废项。

## 最新演进与工业实践

- **观测栈位移**（⚠️ 转述）：p_s + digest 的"实例内自观测"仍是地基，但工业界主面板普遍上移到
  PMM/自研 TSDB+Grafana（metrics 拉取→聚合→告警），书内"SHOW GLOBAL STATUS 差分"流程已是脚本素材而非工作台。
- **8.4 调优面**（⚠️）：innodb_redo_log_capacity 全量接管、`innodb_dedicated_server` 自适应内存/日志规模成默认推荐；
  9.x Innovation 的增量在并行读/向量化表达式的预告线上——**书内参数表在 2026 需要按 8.4 手册重刷一遍**。
- **EXPLAIN ANALYZE 的常态化**：从"应急工具"变成变更评审标配（上线前逐条真跑小样本）——8.0 调优方法论的最大代际差（⚠️ 实践口径）。
- **AI 辅助调参**（⚠️ 趋势转述）：自动 knob tuning 与异常检测进入商业 DB 服务层，开源 MySQL 侧仍以
  规则+人肉基线为主；本仓判断：书内"旋钮→指标→机制"三段论恰是人机分工里不变的骨架。
- **取证留痕**：✅ 五个镜像页 200（performance-schema/explain/optimizer-hints/resource-groups/slow-query-log，2026-09-27 实查）。
