# 07 · 监控：pgAdmin 与 Grafana（原书第 7 章）

> 对应原书章：**Ch.7 PostgreSQL Monitoring Using PgAdmin and Grafana**（✅ Crossref DOI `..._7`）。
> 官方摘要原句（✅）："Monitoring is one of the essential requirements for maintaining the stability,
> performance, and reliability of a PostgreSQL database. Along with the OS-level commands and database
> SQL statements, using PostgreSQL's built…"
> 口径声明：章题与摘要 ✅ 实抓；PG 正文为官方文档口径精读重构 ⚠️ 转述（本机无 PG，面板截图未实截）；
> 🔧 节为 DuckDB 内省视图实跑，**仅类比"SQL 即监控面"的设计模式，非 PG 数字**。

## 本章地图

| 主题 | 你能做到 | 关键对象/参数/命令 |
| --- | --- | --- |
| 统计视图族 | 分清"累计器"与"当前态"两类视图 | pg_stat_activity（当前态）vs pg_stat_database/用户表（累计）⚠️ |
| 等待事件 | 把"慢"定位到 IO/锁/CPU 面 | pg_stat_activity.wait_event_type/wait_event、wait_events.md 语义 ⚠️ |
| TOP SQL | 建立语句级排行 | pg_stat_statements（total_exec_time/mean/rows）、EXPLAIN 联动 ⚠️ |
| 日志面 | 从日志里榨出诊断信号 | log_min_duration_statement、csvlog、pgBadger 报表 ⚠️ |
| 面板化 | 部署 exporter+Grafana 告警 | postgres_exporter、Grafana dashboard、阈值表 ⚠️ |
| OS 层 | 不只看库：机器指标对表 | vmstat/iostat/内存水位、与库指标互为佐证 ⚠️ |

## 核心精讲（⚠️ 文档转述重构）

### 1. 两类视图，两种读法

- **当前态**：`pg_stat_activity`（谁在跑、state、wait_event、backend_type、leader_pid 并行树）、
  `pg_locks`（等待图）。判读公式：`state='active'` × wait_event_type 二维表——
  Lock/IO/Client 各走各的排查树（锁等→pg_locks 找 blocker；IO→03/06 章存储账）。⚠️
- **累计器**：`pg_stat_*` 全族是**自上次统计重置以来的流水**（`pg_stat_reset()` 会清零，崩溃也会丢），
  所以一切告警都建立在**差分**上：监控代理每 N 秒采快照、面板上画速率。这是所有 PG 监控工具
  （postgres_exporter/pgwatch2 类）共同的第一原理 ⚠️。
- PG16 起新增 `pg_stat_io`（按 backend type × context × object 的 IO 计数）与 `pg_stat_checkpoints`
  （检查点节奏画像），本册 01/05 章的判读表都挂在这两视图上 ⚠️ 转述。

### 2. 语句排行：pg_stat_statements

```sql
SELECT round(total_exec_time::numeric,1) tot_ms, calls,
       round(mean_exec_time::numeric,2) mean_ms, substring(query,1,60) q
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;
```

装机即 `shared_preload_libraries='pg_stat_statements'`（02 章预载清单）；关心 jitter 看
`stddev_exec_time`（1.10+ 列族 ⚠️），Top-N 之外用 `pg_stat_statements_reset(qid,userid,dbid)`
做语句级清零实验（06 章 A/B 工作流）。判读纪律：**total 排行找优化对象，mean 排行找受害者**。

### 3. 日志与离线分析

`logging_collector=on` + `log_destination='csvlog'`（或 stderr）+ `log_min_duration_statement=500ms`
起步；`log_checkpoints/log_lock_wait/log_autovacuum_min_duration` 运维事件面全开。
CSV 日志 → **pgBadger** 出火焰式日报（✅ https://github.com/darold/pgbadger 实抓 200；与 08 章
Ora2Pg 同作者 darold 系工具，口径同源）。日志是事后取证，实时面板管当下——两轨都要有 ⚠️。

### 4. pgAdmin 与 Grafana 两条面板路

- **pgAdmin4**（✅ https://github.com/postgres/pgadmin4 实抓 200）：自带 Dashboard 页拉实时事务/TPS/
  封锁树，适合"单库人工巡检 + 结构浏览"；作为浏览器形态不适合 7×24 告警。
- **Prometheus + postgres_exporter + Grafana**（exporter ✅
  https://github.com/prometheus-community/postgres_exporter 实抓 200）：exporter 以
  `pg_stat_*` 查询采集器（内建 + `queries.yaml` 自定义）暴露指标 → Prometheus 存储/告警 →
  Grafana 面板（✅ 社区经典面板 dashboards/9628 "PostgreSQL Database" 实抓 200；
  Percona 面板合集 ✅ https://github.com/percona/grafana-dashboards 实抓 200）。
- 最小告警集（本册自洽清单 ⚠️）：连接水位（max_connections−超用）、复制延迟（pg_wal_lsn_diff）、
  归档失败数（pg_stat_archiver.failed_count）、冻结水位 age、长事务时长、dead_tup 斜率、
  检查点频率（30min 内 timed 与 requested 的比例）。
- 巡检 SQL 素材库：pgx_scripts（✅ https://github.com/pgexperts/pgx_scripts 实抓 200）——膨胀、
  重复索引、无效索引等即取即用。

### 5. 🔧 本机概念演示：SQL 即内省面（DuckDB，非 PG 结论）

方法：**DuckDB 1.5.5**（Python API，本机实测）。建两张表后用系统表函数直接 SQL 查询元数据统计：

```
SELECT database_name, table_name, estimated_size, column_count FROM duckdb_tables();
→ [('pgd_ch7', 'ev', 100000, 2), ('pgd_ch7', 'dim', 10, 2)]     # ev=10 万行事件表, dim=10 行维表
```

**可迁移概念**（✅ 方法论）："引擎把自身状态做成可 SELECT 的视图"这一设计在三家开源引擎同构——
PG 的 `pg_stat_*`、MySQL 的 `information_schema`/`performance_schema`（对照
[../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)）、
DuckDB 的 `duckdb_*()` 表函数。DBA 的通用肌肉是：**先问 SQL，再问日志，最后才扒文件**
（03 章 pageinspect 是"扒文件"档的正规通道）。DuckDB 的 estimated_size 语义 ≠ PG 的 n_tup_*，勿互抄。

## 常见坑与判读

| 现象 | 第一判读 | 取证动作（⚠️ 转述） |
| --- | --- | --- |
| Grafana TPS 突然掉底再拉满 | 统计被重置（重启/pg_stat_reset）非业务真零 | 面板一律 rate() 差分 + 重置事件标注 |
| pg_stat_activity 里看不到自己的慢查询 | 采样窗口/权限（非超级用户只见部分列） | 用 pg_stat_activity 视图列权限或监控账号 ⚠️ |
| exporter 采爆高基数库 | 每库每查询展开成时序标签 | 裁剪 pg_stat_statements 上限/白名单查询集 |
| 告警"连接数 90%"但无人登录 | 连接池打满或应用泄漏 | 按 application_name/usename 分组找大户（01 章池化） |
| 复制延迟显示为负/0 | 采样时差或只算了写侧 | 用 confirmed_flush_lsn 与 replay_lsn 成对采 |
| 日志开全后 IO 翻倍 | log 级别过贪（log_statement=all） | 降到 duration+错误面，或 csvlog+异步盘 |

## 与其他章 / 其他笔记的联系

- 本册：01 章（backend_type 列即进程族画像）；03 章（relfilenode→文件名映射供磁盘告警）；
  05 章（归档/槽指标）；06 章（维护三水位：dead_tup/age/长事务）；10 章（PG17 监控面增量）。
- [../PostgreSQL_16_Administration_Cookbook/04-监控诊断与日常维护.md](../PostgreSQL_16_Administration_Cookbook/04-监控诊断与日常维护.md)：
  监控食谱版（等待事件判读、日报模板）。
- [../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md)：
  监控驱动性能法（USE 方法/指标树）的 MySQL 侧原著，方法论强互文。
- [../数据库高效优化.md](../数据库高效优化.md)：跨引擎指标体系对照。
- [../设计数据密集型应用.md](../设计数据密集型应用.md)：为什么"部分不可用"也要盯（面板背后的理论）。

## 核心概念速览（中英对照）

1. **活动视图** — pg_stat_activity：每 backend 一行的当前态全景。
2. **等待事件** — wait_event (type)：把慢归类的坐标系（Lock/LWLock/IO/Client…）。
3. **累计统计视图** — cumulative stats system (pg_stat_*)：差分监控的数据源，重启即清。
4. **语句统计** — pg_stat_statements：TOP SQL 排行的官方扩展。
5. **IO 统计** — pg_stat_io（PG16+）：backend 类型 × 上下文粒度的 IO 计数。
6. **检查点统计** — pg_stat_checkpoints（PG16+）：检查点节奏画像。
7. **CSV 日志** — csvlog + pgBadger：离线报表通道。
8. **导出器** — postgres_exporter：Prometheus 生态的 PG 指标翻译器。
9. **面板** — Grafana dashboard：速率化/告警化的展示层。
10. **基数爆炸** — cardinality explosion：语句级标签把时序库打穿的运维事故。
11. **水位告警** — threshold set：连接/延迟/冻结/归档四类必配线。
12. **统计重置** — pg_stat_reset()：一切差分读法的前置假设。

## 最新演进与工业实践

- **PG16/17 监控面**：pg_stat_io/pg_stat_checkpoints 已如上述 ⚠️；PG17 的 WAL/io 计数继续细化，
  入口 ✅ https://www.postgresql.org/docs/release/17.0/（实抓 200）。
- **生态**：pgwatch 系列在 2024 年分裂为 pgwatch3 维护线（原作者停更公告社区周知 ⚠️ 转述，
  URL 未验证不附）；pgmetrics（一次性巡检打包器）与 pgx_scripts 是"无代理取证"补充 ✅ 后者实抓 200。
- **eBPF/OS 面**：磁盘/网络画像经 BPF 工具直采内核事件的实践增多，与库内视图互为佐证 ⚠️ 转述。
- **AIO 影响预告**：PG18 异步 I/O 改变 IO 等待事件的形态（IO 提交与完成分离），
  等待事件字典与面板口径届时需重校 ⚠️ 转述（✅ release-18 页实抓 200）。
- **缺口诚实登记 ⚠️**：原书面板搭建用的具体 dashboard ID/版本（Grafana 8 还是 10、pgAdmin 截图
  版本）未获样章，本文件以当前主流口径重建。
