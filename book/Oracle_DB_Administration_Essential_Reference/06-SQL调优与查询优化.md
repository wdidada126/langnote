# 06 · SQL 调优与查询优化（⚠️ 主题重构章）

> 本章按出版社文案任务单元"performance tuning / query optimization"重构。小节划分本目录自拟（[00-总览与阅读地图.md](00-总览与阅读地图.md) §二）；Oracle 行为 ⚠️ 文档转述；🔧G5 为 SQLite/DuckDB 执行计划类比实验、**非本书引擎行为**。

## 6.1 本书时代的优化器双轨制（⚠️）

1999 年正处优化器路线切换阵痛期，本书速查必须两头都给：

| 轨 | 触发条件 | 决策依据 | DBA 抓手 |
|---|---|---|---|
| RBO 规则优化 | 无统计时的隐式默认（Oracle7 遗产） | 固定规则优先级表（ROWID>索引>…） | 背规则表=背 SQL 写法 |
| CBO 成本优化 | `OPTIMIZER_MODE=RULE/CHOOSE/COST`；CHOOSE 下**有统计才走 CBO** | 统计信息估算成本 | `ANALYZE` 的时机与范围 |

- `CHOOSE` 参数的半推半就是时代特产：一条表没统计就整条语句回 RBO——"ANALYZE 没跑全"是当时第一大成案；
- 本书的调优章因此一半篇幅在"ANALYZE TABLE/INDEX 的语法与后果速查"；
- 谱系注：CBO 的白盒解剖在盘上有 [../Cost_Based_Oracle_Fundamentals/01-成本究竟指什么.md](../Cost_Based_Oracle_Fundamentals/01-成本究竟指什么.md)（#23，Millsap，2006）——本书讲"何时该收集统计"，CBOF 讲"统计如何变成成本"，两册构成同一问题的前后两代答案。

## 6.2 执行计划获取三件套（⚠️）

```
1) EXPLAIN PLAN FOR <sql>;  SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);  -- 9i 后姿势；8.0 时代:
   @?/rdbms/admin/utlxplan.sql 建表 → EXPLAIN PLAN SET STATEMENT_ID='T1' FOR ...
   → SELECT ... FROM PLAN_TABLE WHERE statement_id='T1';（缩进读 Op/Name 列）
2) autotrace: SET AUTOTRACE TRACEONLY EXPLAIN;（SQL*Plus 侧车，08 章命令表）
3) SQL Trace + tkprof: ALTER SESSION SET SQL_TRACE=TRUE; → tkprof x.trc y.lst sort=(prsela,fchela)
```

读计划的本书口径（⚠️ 通说）：从最缩进行读起；`TABLE ACCESS FULL` 未必是错、`NESTED LOOPS` 配大行数才是事故；`SORT GROUP BY` vs `GROUP BY` 暴露有无索引可用；成本列在 RBO 下无意义——计划读法与 6.1 双轨制绑定。

## 6.3 索引决策速查（⚠️）

| 信号 | 动作 |
|---|---|
| 高选择性等值谓词、表大 | 建 B-tree 索引（`CREATE INDEX ... TABLESPACE idx_ts PARALLEL NOLOGGING` 后重建为 LOGGING——8i 快速建索引三板斧） |
| 谓词列被函数包裹 `WHERE v+0=123` | 索引失效——改写谓词或（8i 起）函数索引 |
| 低基数列（性别/状态） | 位图索引（数仓侧；OLTP 并发更新痛——对照 CBOF 位图章 [../Cost_Based_Oracle_Fundamentals/08-位图索引.md](../Cost_Based_Oracle_Fundamentals/08-位图索引.md)） |
| 覆盖查询 | 让索引含全部引用列免回表（🔧G5 实证此概念跨引擎通用） |
| 索引长胖 | `ALTER INDEX ... COALESCE` / `SHRINK SPACE`（后者 9i 起） |

## 6.4 等待与统计：实例级调优入口（⚠️）

本书时代的"性能体检单"（等待事件分析法定型于 8i，`V$SESSION_EVENT`/`V$SYSTEM_EVENT` 是本书能给的最现代面板）：

- `db file sequential read` 单块读——索引路径 IO 画像；`db file scattered read` 多块读——全表扫描画像；
- `buffer busy waits`/`free buffer waits`——DB 缓存压力（`db_block_buffers`，07 章参数）；
- `latch free`+`V$LATCH`——闩锁热点（专著纵深在 [../Oracle_Internals_An_Introduction/03-闩锁服务.md](../Oracle_Internals_An_Introduction/03-闩锁服务.md)，#74 册）；
- 比率法：`V$SYSSTAT` 的解析/执行比（软解析率）、命中率族（buffer/library/dictionary）——1999 年"命中率教"的原始素材，2026 视角：方法论已被 [../Oracle_Performance_Tuning_2e/02-等待事件与响应时间分析.md](../Oracle_Performance_Tuning_2e/02-等待事件与响应时间分析.md) 的响应时间模型取代，但"先看等待再看 SQL"的次序不变。

## 6.5 语句级调优工具箱（⚠️）

- 绑定变量 vs 字面量：硬解析风暴（共享池闩锁）的第一因——`WHERE empno=&n` 改 `:b1` 是速查书级别的忠告；
- HINT 语法卡：`/*+ FULL(t) INDEX(t ix) USE_NL(a b) LEADING(b a) FIRST_ROWS PARALLEL(t 4) */`——8.0 支持面与放置规则（紧跟 DML 关键字）；
- 改写模式：`IN (子查询)` vs `EXISTS`、`OR` 拆 `UNION ALL`、`ROWNUM` 分页三件套——RBO 时代"SQL 书法"的遗产，CBOF 时代多数被优化器自动变换接管；
- 排序与哈希：`sort_area_size`/`hash_area_size`（专有服务器 PGA 内限额，溢出进临时表空间——02 章 2.4 联动）。

## 6.6 调优工作流总卡（⚠️ 本目录自拟，复刻速查书决策树体裁）

```
慢的表象 → ①实例级还是语句级？(V$SYSTEM_EVENT 头部等待 vs 单 SQL 资源)
  ├─ 实例级：内存/IO/闩锁三问 → 07 章参数族调整 → 复测
  └─ 语句级：拿计划(6.2) → 计划合理吗？
       ├─ 不合理：统计过期？→ ANALYZE(6.1)；写法杀索引？→ 改写(6.5)；仍顽固→ hint 兜底
       └─ 合理但慢：数据量增长？→ 索引/分区(02 章存储联动)；资源饥饿？→ 回实例级
```

配套纪律（⚠️ 通说）：一次只改一个变量、改前留基线（tkprof 前后对照）、"慢"要有量化定义（响应时间/吞吐/资源三选一起誓）——这三条是速查书时代就定型、AWR 时代仍写在每一本调优手册扉页的元规则，与 [../Oracle_Performance_Tuning_2e/01-性能调优方法论总纲.md](../Oracle_Performance_Tuning_2e/01-性能调优方法论总纲.md) 的方法论总纲同构（已验名实链）。

## 6.7 🔧G5 实验：执行计划概念的跨引擎最小样本（非本书引擎行为）

同一查询形态在 SQLite（游标式）与 DuckDB（向量化）下的计划输出：

```
G5 sqlite plan (indexed):        SEARCH big USING COVERING INDEX ix_big (v=?)
G5 sqlite plan (non-indexed expr): SCAN big
G5 duckdb plan:  UNGROUPED_AGGREGATE → (filter i>0) ...（EXPLAIN 树状框图，节选）
```

（SQLite 3.45.3 / DuckDB 1.5.5，表 big 2 万行+索引 ix_big。）三点对照（均**非本书引擎行为**）：
1. `v=123` 走索引、`v+0=123` 退化为全表 `SCAN`——6.3 的"谓词列被函数包裹索引失效"在两个无关引擎上原样复现：**这是索引可用性判断的通用语法学，不是 Oracle 特性**；
2. `COVERING INDEX` 字样=6.3 第 4 行"覆盖免回表"——术语跨引擎稳定；
3. 差异登记：SQLite 计划无成本数字（规则式选路，恰似 Oracle RBO 气质）、DuckDB 计划无行号级缩进文本树（现代算子树）——读计划的能力=读**该引擎的方言**，本书 6.2 的 PLAN_TABLE 缩进法今天对应 `DBMS_XPLAN`，概念迁移零障碍、语法迁移必须重学。

## 6.8 章间连线

- 6.1 CHOOSE 参数 → 07 章参数速查；
- 6.2 autotrace/SQL*Plus → 08 章命令语法；
- 6.4 闩锁/等待 → #74 册 internals 纵深；
- 6.3/6.5 成本视角 → CBOF 02-13 章群；
- 现代诊断体系 → [../Oracle_Performance_Tuning_2e/06-优化器统计与SQL调优.md](../Oracle_Performance_Tuning_2e/06-优化器统计与SQL调优.md)、[../Oracle_Database_Problem_Solving/05-AWR分析优化.md](../Oracle_Database_Problem_Solving/05-AWR分析优化.md)。

## 6.9 章前自测与本章边界

- 自测三题：①CHOOSE 模式下为什么"半套统计"比"没统计"更危险？（有统计的表走 CBO、没有的走 RBO，混合计划不可预测）②`db file sequential read` 大量出现一定有问题吗？（不一定——索引路径的健康呼吸，看单次等待时长与总量）③hint 失效的三种常见原因？（拼写/对象别名不匹配/基线语法不被支持）。
- 本章边界：成本模型白盒归 CBOF（00 §4.2 谱系表）、等待事件微观机制归 #74 册、现代 AWR 工作流归 Problem_Solving 05 章；本章只管 1999 年面板上"看得见的手"。
- 🔧G5 的边界声明：实验只证"索引可用性判断与覆盖索引"两概念跨引擎成立，不证 Oracle 成本估算行为——后者永远 ⚠️。
- 证据锚点：RBO 于 9i 移除、`DBMS_XPLAN` 属 9i+ 两条 ⚠️ 断言以 00 §六的 23ai/11g 存档 URL 为回查路径；6.4 等待事件名在 11g 存档参考手册（e41084，实抓 200 ✅）中可逐条对账——这是"老速查书条目→现代文档验证"的标准动作，读者可复放。
- 一句话收束：本章的调优对象（计划、统计、等待）从未过时，过时的只是拿到它们的手势——把手势当方言、把方法论当语法，老书就读活了。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 规则/成本优化器 | RBO / CBO | 双轨时代的两种选路哲学 |
| 执行计划 | execution plan | 优化器选定的访问路径说明书 |
| 计划表 | PLAN_TABLE / DBMS_XPLAN | 拿计划的仓库与展示器（两代姿势） |
| 自动跟踪 | autotrace | SQL*Plus 侧车：计划+统计一次出 |
| 会话跟踪 | SQL Trace / tkprof | 事后放大镜，按资源列排序聚合 |
| 硬解析/软解析 | hard / soft parse | 字面量 SQL 的共享池杀手 |
| 提示 | hint | 注释形态的优化器指令，8.0 语法卡 |
| 等待事件 | wait event | 8i 起的性能问诊主诉单 |
| 命中率教 | hit ratio era | 比率指标的史前方法论（已被 RTM 取代） |
| 覆盖索引 | covering index | 免回表的索引列超集（🔧G5 跨引擎复现） |

## 最新演进与工业实践

- **优化器单轨化**（⚠️）：Oracle 9i 移除 RBO（仅 `ROW` 模式残影）、`CHOOSE` 语义并入 `ALL_ROWS`；统计侧 10g `DBMS_STATS`+自动收集作业+直方图体系——6.1 整节转为版本考古。直方图与选择度的现代白盒在 [../Cost_Based_Oracle_Fundamentals/07-直方图.md](../Cost_Based_Oracle_Fundamentals/07-直方图.md)。
- **计划稳定性工程**（⚠️）：绑定变量窥视（9i）、SQL Profile（10g）、SQL Plan Baselines（11g）/SPM——对付"升级后计划翻转"的制度化，对应本书"hint 保平安"的个体手艺；排错册的 GC 等待与 SPM 专章 [../Oracle_Database_Problem_Solving/02-GC缓冲区忙等待、自适应游标共享与SPM.md](../Oracle_Database_Problem_Solving/02-GC缓冲区忙等待、自适应游标共享与SPM.md) 是同一战场当代版。
- **诊断栈换代**（⚠️）：AWR/ASH/ADDM（10g）→ SQL*Monitor/SQL Tuning Advisor → 23ai 的自动索引（Auto-Indexing）与实时 SQL 监控；✅ 现行调优手册（实抓经重定向 200）：https://docs.oracle.com/en/database/oracle/oracle-database/23/tgdba/ （Performance Tuning Guide，/26/tgdba/）。
- **工业实践**（⚠️ 通说）：今天 SQL 性能事故的第一响应是"抓计划+看统计+比基线"，与 6.2 三件套同构；云托管（Autonomous DB）把 6.4 体检单变成自动巡检报告——速查书的角色从"人脑缓存"迁移为"平台的默认策略"，但策略内容仍是本章这些条目。
- **类比锚点**（🔧G5，非本书引擎行为）：函数包裹谓词杀索引、覆盖索引免回表两条经验在 SQLite/DuckDB 实测复现——调优知识里"引擎方言"与"存储引擎通用语法"的分界线，用异引擎实验切分最清楚。
