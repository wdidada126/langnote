# 第 9–10 章：使用 AWR 分析优化数据库（一）（二）

> ⚠️ 文档转述（章题取自中译本逐字目录 ✅，章内小节自拟 ⚠️；AWR 行为为 11gR2–12cR1 口径转述，无 Oracle 实测）。本章 🔧 组为 SQLite ANALYZE/统计翻转类比，**非 Oracle 行为**。

## 本文件定位

第 9、10 章是同一主题的上半场/下半场（对应官方报告的两份输出）：第 9 章教你**读懂快照与负载摘要**，第 10 章教你**从段级/SQL 级明细里抓凶手**。这两章是全书的"仪表盘"，其余各章的症状几乎都能在这里找到量化入口。

## 第 9 章 使用AWR分析优化数据库(一)：快照与总览

### 9.1 采集面（⚠️ 转述）

- AWR=Statspack 换代：MMNL/SMMN 后台进程每小时抓 `v$active_session_history` 采样 + 一批 `v$` 视图快照落 `dba_hist_*`；保留默认 8 天（11g）/30 天（12c），许可面属 Diagnostics Pack——无许可时退 Statspack（社区反复强调的合规红线）。
- 快照卫生：RAC 下报告有全局/节点两级；快照间隔可按诊断期临时加密（`DBMS_WORKLOAD_REPOSITORY.MODIFY_SNAPSHOT_SETTINGS`），但 retention 与 MMON 刷写负担要一起想。

### 9.2 报告解读顺序（⚠️ 转述，本章方法论核心）

1. **Load Profile**：每事务/每执行口径先看，避免"绝对值幻觉"；redo per sec 与 db block changes 平衡判断写放大。
2. **Top 5/10 Timed Events**：DB Time 的构成即优先级——前台等待事件类（User I/O / Concurrency / Application / Administrative / Cluster）决定往哪一章跳：Cluster→第 3/11 章，Concurrency→第 16 章，User I/O→第 15/17 章。
3. **Instance %**：Buffer Hit/Library Hit 等旧指标在 2010s 社区口径里已被降级为"参考"（命中率不是目标，DB Time 才是）——本章是本书里少数被后续版本"纠偏"的章。
4. **OS/内存段**：vmstat/Paging、硬解析比例（parse cpu vs elapsed、`v$sysstat` 中 parse count (hard) per sec）。

## 第 10 章 使用AWR分析优化数据库(二)：明细钻取

### 10.1 钻取路径（⚠️ 转述）

- SQL 区四张表：`SQL ordered by Elapsed`（用户痛感）、`by Gets`（缓冲区凶手）、`by Reads`（IO 凶手）、`by Executions`（热点小查询）；每张表的候选都要回 `dba_hist_sqlstat` 比对同一 sql_id 在多快照里的**计划翻转**（CHG→与第 4/5 章 ACS/SPM 接口）。
- 段级：Segments by Cr/Buffer Busy Waits、by Direct Path Reads、by Logical/Physical Reads；热点段清单直接喂给第 3/6/7 章处置。
- ASH 补位：AWR 是 10 秒粒度平均值，瞬态问题用 `dba_hist_active_sess_history`（1 秒采样）按时间切片+等待事件+blocking_session 树查阻塞源；这是"不可复现问题"的主力证据（同 TOP2e 的事后分析章）。

### 10.2 时间轴对比法（⚠️ 转述）

- 好/坏基线快照对拉（`awrrpt.sql` 两段区间 → `AWRDIFF` 类脚本社区化）：负载画像不变而耗时变→找变更（统计/计划/参数/硬件）；负载画像变→找业务侧。
- 计划翻转定位：`dba_hist_sql_plan` 按 snap_id 分组看 plan_hash_value 时间线，配 `v$sql` 现状——"何时开始坏"比"现在多坏"更能指到根因。

## 🔧 实验 G3 · 统计采集让计划翻转（非 Oracle；Python 3.13 / SQLite 3.45.3）

稀有值查询在无列统计与有统计两种状态下计划翻转，模拟"统计刷新/嗅探后计划变脸"：

```text
### G3 stats baseline (AWR vs ANALYZE + sqlite_stat1)
before ANALYZE, plan for rare cat:
[(3, 0, 0, 'SEARCH t USING INDEX i_cat (cat=?)')]
sqlite_stat1 -> [('t', 'i_cat', '1000 500')]
after ANALYZE, plan for rare cat:
[(2, 0, 0, 'SCAN t')]
```

- 方法：1000 行、cat 二值（990 COMMON / 10 RARE）+索引；`ANALYZE` 生成 `sqlite_stat1` 后，同一查询的计划由走索引翻为全表扫描——因为统计揭示了"RARE 并不稀有到值得回表"的分布。
- 对照：Oracle 中同款翻转发生在统计收集/直方图变化/ACS 绑值切换时；AWR 的 `dba_hist_sqlstat` 正是把"翻转时刻"坐标化的账本（`plans_in_error` 类比物）。**排错动作也一样：先定位翻转时间点，再找该点上的变更**。

## 9.3 采集与保留的坑位细节（⚠️ 转述）

- MMON 刷写滞后：AWR 看"当下这一分钟"必然迟到，实时现场交给 ASH/`v$active_session_history`——第 9 章管"账本"，第 10 章管"明细"，现场另有窗口。
- 保留是环形账本不是历史：retention 缩短被覆盖的快照回不来；值得长期对比的区间要 BASELINE 固化（`DBMS_WORKLOAD_REPOSITORY.CREATE_BASELINE`）。
- RAC 报告口径：全局 `awrglobal.sql` 与单节点报告结构不同，把单节点 Load Profile 当全局是高频误读。
- 加密快照的代价：诊断期把 interval 调到 10 分钟会放大 AWR 自身写与字典负担，用完要还原——观测行为也在被观测系统里付费。

## 10.3 案例演练：月末批处理让 DB Time 翻倍（⚠️ 按章主题结构化）

1. 区间选取：好/坏 snap 边界对齐"批处理开始前"的最后一次快照，而非自然整点。
2. Load Profile 对比：redo per sec 与 db block changes 同涨→写入面变重（走第 6/7 章找执行计划变更）；User I/O 等待类涨→读取放大（走 10.1 段级排行）。
3. SQL 四榜交叉：elapsed 榜与 gets 榜的并集里，逐个查 `dba_hist_sqlstat` 的 plan_hash_value 时间线，把"计划变了"从"量大了"里剥出来。
4. ASH 切片：热点段的等待是连续带（批处理本态）还是尖峰（锁/驱逐类次生问题）。
5. 输出：结论按"负载变了 / 计划变了"二选一给动作项——前者容量与错峰，后者第 4/5 章止血。
6. 沉淀：演练用过的 snap 对命名进 BASELINE，下一批处理季有可比对象。

## 10.4 常见误区（⚠️ 社区口径）

- "retention 越大越安全"——字典与刷写负担同步涨；30 天默认值+定点 BASELINE 才是平衡解。
- "elapsed 榜首=凶手"——每执行口径与等待类结构比榜首头衔可靠。
- "实例百分比命中率高就健康"——命中率是旧货币，DB Time 才是（9.2 第 3 点）。
- "AWR 抓不到就说明没问题"——MMON 滞后+环形覆盖两种盲区，现场用 ASH、历史用 BASELINE（9.3）。
- "SQL 排行按绝对值排前十就行"——每执行/每事务归一化不做，会把"高频小妖"漏给"低频大妖"陪榜。
- "快照加密总无害"——AWR 自身的字典写在加密期同步放大，观测也要过成本审计（9.3 末条）。
- "ASH 能替 AWR 长期留存"——采样保留窗口远短于 AWR，长期账本仍归快照层。

## 症状 → 动作速查表

| 症状 | 第一动作 | 跳转 |
|---|---|---|
| DB Time 暴涨但 OS 正常 | Top Timed Events 找等待类分布 | 第 3/15/16 章 |
| 某 sql_id 耗时阶跃 | dba_hist_sqlstat 查 plan_hash_value 时间线 | 第 4/5 章 |
| redo/sec 与 block changes 失衡 | 查批量写/索引过多/触发器 | 第 6 章 |
| 段热点榜出现单对象 | ASH 看具体 SQL 与绑值分布 | 第 3/18 章 |
| 瞬时抖动 10s 平均看不见 | 切 ASH 时间切片+阻塞树 | 第 10 章 |
| 无 Diagnostics Pack | Statspack 兜底，口径降级声明 | 第 9 章 |

## 自测题

1. 为什么 Load Profile 要按每事务/每执行读？绝对值会骗人在哪里？
2. Top Timed Events 的等待类到本书章节的映射，说出 Cluster 与 Concurrency 两条。
3. AWR 与 ASH 的粒度差是什么？举一个"只有 ASH 能答"的问题。
4. 好/坏基线对拉能区分哪两种变化？各自下一步查什么？
5. `dba_hist_sql_plan` 在计划翻转案里的正确用法？
6. 🔧G3 中计划翻转的方向与 Oracle 直觉相反（有统计后弃索引），说明统计"揭示事实"与"索引必然优"哪个成立？
7. 加密快照为什么"用完要还原"？观测行为在哪一层还在付费？
8. RAC 全局报告与单节点报告混用的两种典型误读各是什么？

## 核心概念速览（中英对照）

- **AWR** — Automatic Workload Repository：快照式负载仓库，Diagnostics Pack 许可项 ⚠️
- **快照/基线** — Snapshot/Baseline：分析区间端点与可命名保留点 ⚠️
- **DB Time** — DB Time：前台会话忙碌总和，优先级货币 ⚠️
- **负载概况** — Load Profile：每秒/每事务归一化指标组 ⚠️
- **Top Timed Events** — 计时事件前 N：DB Time 的等待构成 ⚠️
- **等待类** — Wait Class：User I/O、Concurrency、Cluster 等分组路由 ⚠️
- **ASH** — Active Session History：1 秒活动会话采样，瞬态取证 ⚠️
- **SQL Ordered by …** — SQL 排行榜：Elapsed/Gets/Reads/Executions 四榜 ⚠️
- **计划翻转** — Plan Flip：同 sql_id 的 plan_hash_value 随时间变化 ⚠️
- **Statspack** — Statspack：无许可时的手工快照替代 ⚠️
- **硬解析率** — Hard Parse Rate：每秒硬解析次数，可伸缩性第一指标之一 ⚠️
- **统计翻转实验** — Stats-Driven Plan Flip：🔧 SQLite ANALYZE 前后的计划变化（非 Oracle）

## 最新演进与工业实践

- **口径迁移**：19c/23ai 的 AWR Plus/实时 ASH（23ai 默认免费档扩大）让"无许可降级 Statspack"的选择变宽（docs.oracle.com 23ai licensing 文档 ✅ 域名可达，细节 ⚠️ 未直读）。
- **从报告到异常检测**：Enterprise Manager Database Services 与 Oracle 云 Observability 直接把"好坏基线对拉"产品化为自动基线异常检测；DBA 的手工 awrrpt 流程转为复核角色 ⚠️ 转述。
- **SQL Monitor 补位**：单条 SQL 执行内并行从属/计划行级统计（`v$sql_monitor`）成为"SQL 区四榜之外"的第五视角，11g 起属 Tuning Pack 许可 ⚠️——本书时代其使用受许可限制，社区仍高频引用。
- **跨引擎镜像**：pg_stat_statements（PostgreSQL）与 performance_schema events_statements（MySQL）承担了与 AWR SQL 区同构的角色；"排行榜四问（时间/逻辑读/物理读/次数）"在三大引擎里都有对应物，🔧G3 说明统计维度在 SQLite 也有最简同型。
