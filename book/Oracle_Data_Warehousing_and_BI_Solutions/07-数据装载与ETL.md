# 07 数据装载与 ETL — Data Loading（原书第 7 章，pp.175–194）

> 章题/页区间/小节题名 ✅ 出版社目录扫描件（Contents）。本章把「数据怎么进仓库」拆成两级：
> **数据库内建装载件**（p.176 起五件套）与 **OWB 抽取转换装载平台**（p.181 起），最后给平衡裁决
> （p.192）。Oracle 机制 ⚠️ 文档转述（SQLLDR/Data Pump 有现行 ✅ URL；OWB/CDC 老产品据归档口径）；
> 🔧 数字来自本机 DuckDB/SQLite 类比（[00 §9](00-总览与阅读地图.md)），非 Oracle 行为。

## 7.1 Oracle 数据库的数据装载特性（p.176）

目录列出五件套（✅ p.176–181），按「离 SQL 越来越近」排序：

### 7.1.1 数据库内嵌 ETL（p.177）

- ⚠️ 转述：10g 语境的「Embedded ETL」= 用 SQL 本体做转换（INSERT SELECT、MERGE、DBMS Profiler
  等库内件）；思想在 2026 被「ELT 压倒 ETL」的产业走向完全验证——转换下推到数据所在之处
  （对照 [../Amazon_Redshift_Cookbook_2e/00-总览与阅读地图.md](../Amazon_Redshift_Cookbook_2e/00-总览与阅读地图.md) 的 SQL 管道、
  [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md) 的 dbt=纯 ELT 编排）。

### 7.1.2 SQL*L*oader（p.178）

- ⚠️ 转述 + ✅ https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-sql-loader.html ：
  外部文件逐行装载工具；三种模式（常规路径 vs **直接路径**绕过 buffer cache 批量写、外部表
  替代方案）；直接路径 + PARALLEL 是仓库大宗装载的经典组合 ⚠️。
- 🔧 装载经济学（**非 Oracle 行为**）：E4 用 51.4MB/2M 行 CSV 对比两种入口——批量 COPY
  **0.38s** vs 逐行 executemany（50k 行 37.7s，外推 2M ≈ **1500s**，≈**4000×** 差距）；
  另验证 MERGE 幂等重跑 10 万行结果不变。**「批量 vs 逐行」是装载章节里数量级最大的一条
  定律**，SQLLDR 直接路径、外部表、Data Pump 全是它的 Oracle 实现（00 §9 E4）。

### 7.1.3 变更数据捕获 CDC（p.179）

- ⚠️ 转述（归档口径 + 现行对位）：10g 的 Oracle CDC（物化视图日志驱动 ⚠️）捕获源表增量；
  现行文档对位为 XStream/逻辑解码族 ⚠️（11g 归档入口
  ✅ https://docs.oracle.com/cd/E11882_01/index.htm ，不编 10g 细节 URL）。
- 🔧 增量代价（**非 Oracle 行为**）：E5 在 200k 插入路径上挂「变更记录触发器」：
  0.19–0.20s → **0.68–0.72s（+254%）**，变更表同步 20 万行——CDC 不是免费午餐，
  **源侧写放大约 3.5×**；这条本机曲线正是 7.4「什么时候宁可全量重刷」裁决的算术依据（00 §9 E5）。

### 7.1.4 可传输表空间 TTS（p.180）

- ⚠️ 转述 + ✅ dwhsg 主题：把整块表空间文件「搬」进目标库（元数据导出+文件复制/恢复+插件），
  装载量级从行变成文件——大宗历史迁移的旁路通道；与 7.2 的 OWB 交换装载（exchange partition）
  同属「以搬代插」家族。
- 🔧 概念锚点：E2 的「直取年片 0.5ms vs 单大表 2.7ms」演示批量文件级切分的收益方向
  （**非 Oracle 行为**，真分区消除只有 Oracle 有，见 00 §9 E2）。

### 7.1.5 Data Pump（p.180）

- ⚠️ 转述 + ✅ https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-data-pump-overview.html ：
  expdp/impdp 的表空间/模式级高速导出入，PARALLEL 与直接路径语义内置；在仓库场景多用于
  环境间整体搬迁与暂存区灌数。

## 7.2 OWB：Oracle Warehouse Builder（p.181）

- ⚠️ 转述（归档口径）：OWB 是 10g/11g 时代的官方图形化 ETL 平台（设计器 + 生成物 +
  仓库内执行运行时）。目录细分五节：**打包**（Packaging，✅ p.181：设计资产如何版本化/晋升）、
  **典型步骤**（✅ p.182：映射定义→生成→部署→调度）、**ETL 设计**（✅ p.184：抽取/清洗/
  查找/聚合算子在映射图上的摆法）、**OWB 与维度模型**（✅ p.189：SCD 类型、星型装载的原生
  支持——与 [05](05-面向可用性的模型设计.md) 维度设计直接对接）、**流程编辑器**
  （Process Editor，✅ p.191：PL/SQL 级过程控制，弥补映射式 ETL 的表达力缺口）。
- ⚠️ 编者归纳：OWB 的「映射（declarative）+ 流程（procedural）」双层结构是本章产品级
  方法论核心：**能用映射的不用流程**，把可维护性留给生成物。
- 历史注脚：OWB 后被 ODI 收编、再后是 OCI Data Integration ⚠️；本章是中文读者理解
  「Oracle 系 ETL 三代同源」的祖本（→ 演进节）。

## 7.3 装载选择的平衡（p.192）

- ⚠️ 编者归纳（✅ p.192–194）：裁决轴——**增量 vs 全量**（E5 的 +254% 就是此轴的税单）、
  行级 vs 文件级（7.1.4 旁路）、库内 SQL vs 外部 ETL 工具（7.1.1 vs 7.2）、装载窗口时长
  （回链 [04 §4.6.1](04-平台选型与规模测算.md) 峰值输入）与**可恢复性**（断点重跑=幂等，
  🔧 E4 的 MERGE 验证）。

## 7.4 与 repo 其他书的联系

- 同题实施章：[../Oracle_Essentials_5e/08-仓库实施分区物化视图与装载.md](../Oracle_Essentials_5e/08-仓库实施分区物化视图与装载.md)
  （装载三件套的导游版）。
- 维度装载的建模前提：[../数据仓库工具箱.md](../数据仓库工具箱.md)（Kimball SCD 章节，本章 7.2
  p.189 的需求侧）。
- ELT 当代形态：[../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)、
  [../Amazon_Redshift_Cookbook_2e/00-总览与阅读地图.md](../Amazon_Redshift_Cookbook_2e/00-总览与阅读地图.md)、
  [../BigQuery_for_Data_Warehousing/00-总览与阅读地图.md](../BigQuery_for_Data_Warehousing/00-总览与阅读地图.md)。
- 流式增量对照：[../Building_Real_Time_Analytics_Systems/00-总览与阅读地图.md](../Building_Real_Time_Analytics_Systems/00-总览与阅读地图.md)
  （CDC 的下一代形态：变更流而非变更表）。
- 治理视角：[../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)。

- 三条保守经验（⚠️ 编者归纳）：幂等优先于巧滑；文件级优先于行级（量允许时）；
  增量优先于全量、但变更占比过高时反转为全量重刷——阈值就在 E5 的税单与窗口时长之间。
- 装载日志的双重身份（⚠️ 编者归纳）：既是 ch.8 的监控对象，也是 ch.12 度量的工时数据源。

## 核心概念速览（中英对照）

- **内嵌 ETL / ELT** — Embedded ETL：转换下推回 SQL 本体（✅ p.177）。
- **SQL*L*oader** — SQLLDR：外部文件装载；直接路径绕过 buffer cache（✅ p.178）。
- **直接路径** — Direct Path：批量旁路写，🔧 E4 4000× 差距的机制名。
- **CDC** — Change Data Capture：增量捕获；🔧 E5 源侧 +254% 写税（✅ p.179）。
- **TTS** — Transportable Tablespaces：以搬文件代替插行（✅ p.180）。
- **Data Pump** — expdp/impdp：高速整体搬迁（✅ p.180）。
- **OWB 映射** — OWB Mappings：声明式 ETL 算子图（✅ p.184）。
- **OWB 流程编辑器** — Process Editor：过程式补充层（✅ p.191）。
- **SCD 装载** — Slowly Changing Dimensions：OWB 对维度模型的原生支持（✅ p.189）。
- **幂等重跑** — Idempotent Reload：断点续跑的正确性前提（🔧 E4 MERGE 验证）。
- **增量 vs 全量裁决** — Incremental vs Full Balance：窗口时长与写税的权衡（✅ p.192）。

## 最新演进与工业实践

2007 → 2026 对位（⚠️ 转述 + ✅ URL）：

- **三代同源的 Oracle ETL**：OWB（本章）→ ODI（ Fusion Middleware 时代收编 ⚠️）→
  **OCI Data Integration**（托管管道，✅ https://www.oracle.com/database/technologies/ 为
  可验证入口；ODI/OCI DI 精确文档路径需版本号，本册登记为弃用不引，见 [00 §10](00-总览与阅读地图.md)）⚠️。
- **ELT 成为默认**：7.1.1 的「库内转换」预言了 dbt/各云仓 SQL 管道的主流化 ⚠️；
  SQLLDR/外部表/Data Pump 仍是 19c 现行件（✅ 上列两个 sutil URL），直接路径思想
  在云侧变成批量 COPY/LOAD 命令的同型物。
- **CDC 的形态迁移**：变更表模式（10g MV 日志）→ 逻辑解码/XStream → Kafka/Connect 与
  流批一体（对照 [../Building_Real_Time_Analytics_Systems/00-总览与阅读地图.md](../Building_Real_Time_Analytics_Systems/00-总览与阅读地图.md)、
  [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)）⚠️；
  🔧 E5 的写放大税单在每种形态都要重新算一遍——方向不变，只是记账位置移动。
- **TTS 的现代等价**：文件级搬迁变成快照/克隆库与开放表格式（Iceberg）的元数据切换
  （对照 [../Architecting_an_Apache_Iceberg_Lakehouse/00-总览与阅读地图.md](../Architecting_an_Apache_Iceberg_Lakehouse/00-总览与阅读地图.md)）⚠️。
- **装载可观测性**：本章 7.3 的「平衡」在 2026 有了岗位化表达——数据管道 SLA/新鲜度 SLO
  由可观测平台盯守（✅ 对照 [../Fundamentals_of_Data_Observability/00-总览与阅读地图.md](../Fundamentals_of_Data_Observability/00-总览与阅读地图.md)）⚠️。
- **本机教学** 🔧：E4/E5/E2 三件套（4000× 批量定律、+254% 增量税、文件片收益方向）覆盖
  本章全部定量论点；COPY/MERGE/触发器均为 SQLite/DuckDB 行为，**非 Oracle 行为**。
