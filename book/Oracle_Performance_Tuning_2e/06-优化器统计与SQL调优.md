# 06 优化器统计与SQL调优 — Oracle Performance Tuning, 2e（精读重构）

> ⚠️ 主题重组口径（[00-总览与阅读地图.md](00-总览与阅读地图.md) §3/§8）。本章=CBO 时代的"喂料—读口供—纠偏"三板斧；
> Oracle 行为 ⚠️ 转述，🔧 为 SQLite/DuckDB 执行计划与统计机制类比（非 Oracle 行为）。

## 1. 优化器代际与模式（⚠️ 通说）

- 谱系：RBO（规则）→ CBO（代价，815/9i 成熟）→ 10g **系统统计**（CPU_IO_STATS：以 MHz/IO 时延标定成本单位）→ 11g 自适应/SQL Plan 管理线（本册未及，演进节记）。
- `optimizer_mode` 语义 ⚠️：ALL_ROWS（总成本最低）/ FIRST_ROWS_n（首行快）/ RULE（旧世界）；9i 默认 CHOOSE（有统计走 CBO）→ 10g 起默认 ALL_ROWS。
- 本章立场=结构派看优化器：**不解剖成本公式**（那是 Lewis《Cost-Based Oracle Fundamentals》的活，✅ 在盘 [../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)），只讲"给对料、读对计划、纠对偏"。

## 2. 统计：CBO 的粮食（⚠️ 通说；10g 代际重点）

| 层 | 内容 | 采集 | 病理 |
|---|---|---|---|
| 表 | 行数/块数/平均行宽 | `dbms_stats`/`analyze` | 陈旧→成本全歪 |
| 列 | NDV/空值/null | 直方图 | 倾斜无图→选择度骗局 |
| 索引 | 层级/叶块/聚簇因子 | 同上 | CF 虚高→弃用索引 |
| 系统 | CPU/IO 时延 | 10g workload/noworkload | noworkload 高估 IO |

- 9i→10g 工具迁移线 ⚠️：`ANALYZE`（列统计弱、CF 采样粗）→ **`DBMS_STATS`**（并行、可导出、可计划任务；10g 夜间维护窗自动收集）。
- 直方图纪律 ⚠️：`HEIGHT_BALANCED`（老）与 10g `FREQUENCY/TOP-N`；`METHOD_OPT` 按列定制；绑定变量 + 直方图的敏感期教训（peeking 演进留 `07`/演进节）。
- 深挖对位（✅ 在盘实证）：[../Cost_Based_Oracle_Fundamentals/07-直方图.md](../Cost_Based_Oracle_Fundamentals/07-直方图.md)、[../Cost_Based_Oracle_Fundamentals/05-聚簇因子.md](../Cost_Based_Oracle_Fundamentals/05-聚簇因子.md)、[../Troubleshooting_Oracle_Performance_2e/08-对象统计信息.md](../Troubleshooting_Oracle_Performance_2e/08-对象统计信息.md)。

## 3. 读执行计划：从"看图"到"算账"（⚠️ 通说）

- 取图四路 ⚠️：`EXPLAIN PLAN FOR`+`DBMS_XPLAN.DISPLAY`（9i 起）、`V$SQL_PLAN`（共享真身）、autotrace（速览）、10046+tkprof（执行实况）。
- 行操作词汇表 ⚠️：TABLE ACCESS FULL/BY INDEX ROWID、INDEX RANGE/UNIQUE/FULL SCAN、（PARTITION START/STOP 的组合拳=分区消除证据）、NESTED LOOPS/HASH/MERGE、SORT GROUP BY/SORT JOIN、INLIST/VIEW/MATERIALIZED 类。
- 两条纪律：**Est Rows ≠ Actual Rows 处即统计案发现场**；**从最深缩进往上读**（行源序）。与 TOP 2e 计划解读章共法（✅ [../Troubleshooting_Oracle_Performance_2e/10-执行计划.md](../Troubleshooting_Oracle_Performance_2e/10-执行计划.md)）。

### 🔧 类比 D1/D2：访问路径与"回表税"（SQLite 3.45.3，非 Oracle）

20 万行、`a` 列仅 20 个取值（每值 1 万行），`ix_big_a` 索引（`demo_out.txt`）：

- `SELECT id,a FROM big WHERE a=5` → 计划 `SEARCH big USING COVERING INDEX ix_big_a (a=?)`：**5.063 ms**（300 次均值）。
- `SELECT * FROM big WHERE a=5` → `SEARCH big USING INDEX ix_big_a (a=?)`：**22.096 ms**，≈4.4 倍。
- 对读 Oracle：覆盖索引=回表税清零（"by index rowid 次数"从账本消失）；这是 `02` 章 `db file sequential read`、`03` 章缓冲命中的三线合流点。CBO 的成本语言里它叫"聚簇因子 + 单块读成本 × 行数"（✅ [../Cost_Based_Oracle_Fundamentals/04-B树索引基础访问.md](../Cost_Based_Oracle_Fundamentals/04-B树索引基础访问.md)）。

### 🔧 类比 D5：连接算子选择（DuckDB 1.5.5，非 Oracle）

- 等值连接（100 万×50 万，`l.j=r.k`）→ EXPLAIN 仅见 **HASH_JOIN**；
- 不等式 theta 连接（2000×2000，防组合爆炸缩表）→ **PIECEWISE_MERGE_JOIN**。
- 对读 Oracle 三连接谱（NLJ/HJ/MJ，✅ 成本账在 [../Cost_Based_Oracle_Fundamentals/11-嵌套循环连接.md](../Cost_Based_Oracle_Fundamentals/11-嵌套循环连接.md)/[12](../Cost_Based_Oracle_Fundamentals/12-哈希连接.md)/[13](../Cost_Based_Oracle_Fundamentals/13-排序与归并连接.md)）：小结果集嵌套驱动选 NL、等值大批选 HJ、双方已排序省一层 sort 选 MJ——**算子谱系跨引擎同构，选择函数各引擎不同**（DuckDB 无"按成本挑 NL"的等值路径可复现，如实 ⚠️）。

### 🔧 类比 D3（负结果，如实报告）：统计翻案在 SQLite 不可复现

`ANALYZE` 前后对 `a BETWEEN 1 AND 10`（命中 50%）：计划**均为** `SEARCH big USING INDEX`，翻转未发生；`sqlite_stat1` 落地 `200000 10000`（总行×每键均值），计时 217.8 ms vs 234.8 ms 同量级。结论（诚实边界）：SQLite 的统计模型只有"表级键均值"，**无直方图、无范围选择度敏感性**——Oracle 式"统计更新→计划翻转"在此层无法类比复现，直方图故事只能 ⚠️ 转述（正主演示见 CBOF 07 章与 TOP 08 章的在盘实证）。这反过来说明 Oracle CBO 对统计的依赖深度是本册知识域里最难跨引擎平移的部分。

## 4. 纠偏工具箱（⚠️ 通说的三档烈度）

1. **Hint**（单语句、意图显式）：驱动序/连接法/访问路径/`LEADING`+`USE_NL` 族；纪律=最后手段 + 全注释。
2. **Profile/Outlines 前史** ⚠️：9i Stored Outlines（锁计划）——本册时代正解；10g SQL Profile（喂修正系数）与 11g SPM（演进节）接棒。
3. **SQL 改写**：谓词下推、连接化 IN、`OR-Expansion` 失败的手工分解——**先证明优化器没做，再动手**；改写手册的中文当代正典在盘：[../Oracle查询优化改写技巧与案例.md](../Oracle查询优化改写技巧与案例.md)（辨析：师庆栋/罗炳森原创，非译书，见 TOP 00 §5 同款结论）。

## 5. 绑定变量与解析经济学（⚠️ 通说；`03` 章共享池的应用面）

- 硬解析=语法+语义+生成+入池，软解析=句柄查找；**OLTP 头号 CPU 税**。
- 绑定三连 ⚠️：字面量 SQL → 版本爆炸/共享池风暴；`cursor_sharing=FORCE` 是止血带不是解药；**peeking 悖论**（10g 绑定+直方图 → 首值定计划 → 倾斜列上"绑定不如字面"回潮）——本册成书于该悖论爆发前夜（⚠️ 推定），其工程解（自适应游标/感知绑定）是 11g 以后的事，见演进节。
- TOP 2e 解析章给出 2014 视角全案（✅ [../Troubleshooting_Oracle_Performance_2e/12-解析.md](../Troubleshooting_Oracle_Performance_2e/12-解析.md)）；教材速览：[../Oracle12c数据库应用与开发/06-SQL执行计划与CBO.md](../Oracle12c数据库应用与开发/06-SQL执行计划与CBO.md)。

## 5.1 补充：一道"读口供"例题（文字重构 ⚠️，格式仿 DBMS_XPLAN）

```
| Id | Operation                    | Rows  | Cost |
|  0 | SELECT STATEMENT             |     1 |   45 |
|  1 |  NESTED LOOPS                |     1 |   45 |
|  2 |   TABLE ACCESS FULL ORDERS   | 48000 |   30 |   <-- 估算 48000 实际 3（案发地）
|* 3 |   INDEX RANGE SCAN CUST_IX   |     1 |    1 |
```

三层读法（⚠️ 通说）：①从缩进最深处起读=先扫 ORDERS 全表再逐行探索引；②ROWS 估算列在 Id2 与真实值差 4 个数量级 → ORDERS 侧谓词的列**缺统计或缺直方图**（`status` 列倾斜是经典元凶）；③驱动序倒置的代价被估算掩盖——修统计（喂料）优于加 hint（纠偏），两案皆不如"给 ORDERS 补复合索引"（改访问结构）。与 TOP 2e 计划章同法（✅ [../Troubleshooting_Oracle_Performance_2e/10-执行计划.md](../Troubleshooting_Oracle_Performance_2e/10-执行计划.md)），成本公式层面下钻见 CBOF（✅ 00 §6 表）。

## 5.2 统计采集节奏建议（⚠️ 时代运维配方）

| 对象 | 节奏 | 备注 |
|---|---|---|
| 全表扫描热点大表 | 夜间自动（10g job）+ 增量分区（11g 后 ⚠️） | 本册以全量为主 |
| 装载后即查的表 | 装载尾强制 `DBMS_STATS.GATHER_...` | "先查后集"次序纪律 |
| 稳定参考表 | 锁定统计 `LOCK_...` | 防误重收集翻案 |
| 倾斜列 | 直方图 + METHOD_OPT 定制 | 绑定敏感名单（`07`/演进） |
| 系统统计 | noworkload→workload 迁移一次定 | 10g 新件，改后全库成本基线位移 ⚠️ |

## 5.3 五条"翻案不翻车"守则（⚠️ 通说）

1. 每次只纠一案：同窗口改统计+加索引+改 SQL，归因即失效。
2. 纠偏要留痕：hint 必附"为什么+撤销条件"注释行。
3. 计划对比双证据：估算行数序列 + 10046 实际行数序列（`02` 章），单看图形像"更好"不算数。
4. 升级窗口预演：统计变更在等价副本先跑（本册时代=导出导入 `DBMS_STATS.IMPORT` ⚠️）。
5. 承认优化器：EstRows 合理而仍慢=可能不是计划病，回 `02` 账本再查等待构成。

## 5.4 一页记忆卡（⚠️ 自测）

1. 喂料三优先？——表/列统计新鲜度 > 直方图覆盖倾斜 > 系统统计标定；缺料时 hint 是止痛片。
2. EstRows 与 ActualRows 的来源各是？——`V$SQL_PLAN`（估算）vs 10046/tkprof 或 `GATHER_PLAN_STATISTICS`（实际）⚠️。
3. INDEX FULL SCAN 何时无罪？——小索引上取序（省 SORT ORDER BY）+ 仅需索引列（覆盖）——两条件对照 🔧D1 的"回表税"实验。
4. 绑定变量翻车的两个场景？——数据倾斜列（peeking 定死计划）与高度可变谓词组合（本册时代无 ACS 兜底 ⚠️）。
5. 何时该承认"不是 SQL 病"？——账本头部是闩/池/IO 类等待时，回 `02–05`；TOP SQL 榜只是"嫌疑人名单"。

## 核心概念速览（中英对照）

- **CBO/RBO** — Cost/Rule-Based Optimizer：代价寻优 vs 规则套模板。
- **选择度/基数** — Selectivity/Cardinality：谓词通过比例/结果行数，成本公式的两原语。
- **直方图** — Histogram：列值分布样本，倾斜数据的选择度救星。
- **聚簇因子** — Clustering Factor：索引序与物理序的背离度，决定回表税大小。
- **DBMS_STATS** — 统计包：并行采集/导出/锁定/自动收集的正主。
- **EXPLAIN PLAN / V$SQL_PLAN / DBMS_XPLAN** — 计划三口供：纸上/真身/格式化。
- **Hint** — 提示：语句级强制计划意图，最后手段纪律。
- **绑定变量** — Bind Variable：文本模板+值参，解析复用之源。
- **硬解析/软解析** — Hard/Soft Parse：全流水线 vs 句柄命中。
- **peeking** — Bind Peeking：10g 以首绑值定计划，直方图在场时高危 ⚠️。
- **Adaptive/SPM** — 自适应计划/SQL Plan 管理：11g+ 的运行时换路与计划金库（本册未及 ⚠️）。

## 最新演进与工业实践

- **文档锚 ✅（2026-09-28 curl 200）**：优化器与统计现行章节见 Tuning Guide（https://docs.oracle.com/en/database/oracle/oracle-database/26/tgdba/index.html ）；优化器参数百科在 Reference 手册 `optimizer_*` 参数族（仅引 guide 根 ⚠️）。19c 镜像 https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/index.html 。
- **代际补全** ⚠️：11g **自适应连接**（运行中 NL→HJ 换路）+ **ACS（自适应游标共享，计签换计划）**；12c **SQL Plan Management 自动化演进**、扩展统计（列组/表达式）；12.2 **partial index**（索引可见性试验田）与统计增量；19c 优化器行为补丁按 SQL 灰度（`_optimizer_...` 不再裸奔）。本册 2006 章面 = 这一切的"史前基线"。
- **AI/自动化的现在时** ⚠️：23ai/26ai 的 **Auto Index**（自治环境按 AWR 负载自动建删索引并 SPM 兜底）、SQL Tuning Advisor 并入 ADI；云控制台上"解释计划"升级为"建议+验证+回滚"闭环（✅ Autonomous 文档根 https://docs.oracle.com/en/cloud/paas/autonomous-database/index.html ；机制细节 ⚠️）。
- **跨引擎与学界线**：选择度/基数估计谱系（Selinger 1988、Leis 2015/2025 复审）论文链在盘已双证（[../Cost_Based_Oracle_Fundamentals/10-连接基数估算.md](../Cost_Based_Oracle_Fundamentals/10-连接基数估算.md)、[../../db/db.md](../../db/db.md)）；"统计不可信时怎么办"的现代解（学习型优化器/Lero 等）见 [../Database_Tuning/00-总览与阅读地图.md](../Database_Tuning/00-总览与阅读地图.md) 学习优化器线。
- **工业实践姿势**：OLTP 绑定变量 + 直方图白名单 + SPM 固化仍是 Oracle 调优三件套（⚠️ 通说）；临时诊断用 `DBMS_XPLAN.DISPLAY_CURSOR(GATHER_PLAN_STATISTICS)` 的"估算 vs 实际"双列对照——本册时代 autotrace 的现役替代。
