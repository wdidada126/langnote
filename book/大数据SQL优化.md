# 大数据SQL优化：原理与实践 陈鹤 杨国栋 : 陈鹤

作者: 陈鹤 杨国栋 / 杨国栋
出版社: 机械工业出版社
出品方: Powerdata社区
副标题: 陈鹤
页数: 384
丛书: 数据之力技术丛书
ISBN: 9787111767039

## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2023-09
> 《高性能高可用 MySQL》和《SQL 优化》两部分有重合，对《SQL 优化》整理出来了一个合适的观看顺序，目录如下
> 《高性能高可用 MySQL》和《SQL 优化》两部分有重合，对《SQL 优化》整理出来了一个合适的观看顺序，目录如下
> 《SQL 优化》视频中的 3~25


## 精读补写（系统整理，2026-09-23）

### 版本与 ISBN
- 《大数据 SQL 优化：原理与实践》，陈鹤、杨国栋 著，机械工业出版社（数据之力技术丛书 / Powerdata 社区出品），**ISBN `978-7-111-76703-9`**（384 页）。
- 笔记中提到的《高性能高可用 MySQL》《SQL 优化》视频与该书内容有重合，可相互印证；建议按"执行引擎 → 计划生成 → 代价估计 → Join 与倾斜 → 存储与格式"的顺序阅读（笔记 2023-09 已整理过观看顺序）。

### 主线脉络
**SQL 执行流程**：解析 → 语法/语义校验 → **逻辑计划**（关系代数）→ **优化**（RBO 规则优化：谓词下推、列裁剪、常量折叠、分区裁剪；随后 CBO 代价优化）→ **物理计划**（算子选择、Join 顺序与算法、并行度）→ **执行**（流水线、算子下推、向量化）。
**核心议题**：统计信息与**基数估计**、代价模型、Join 算法（nested loop / hash join / sort-merge join；分布式下 broadcast vs shuffle/repartition）、**数据倾斜**识别与治理（salting、两阶段聚合、广播小表）、分区与分桶、物化视图与预聚合、列式存储与压缩编码（字典/RLE/Delta）、资源与并行度调优。

### 经典论文与原始文献根基
- **Selinger 等《Access Path Selection in a Relational Database Management System》**(SIGMOD 1979)——**System R 优化器**，代价基优化（CBO）与选择率的奠基之作，今天所有代价模型的祖先。
- **Graefe & McKenna《The Volcano Optimizer Generator》**(ICDE 1993)；**Graefe《The Cascades Framework for Query Optimization》**(IEEE Data Eng. Bull. 1995)——**Volcano/Cascades** 是可扩展优化器（Calcite、Orca、SQL Server、Spark SQL）的共同范式。
- **列存与向量化**：Stonebraker 等《C-Store: A Column-oriented DBMS》(VLDB 2005)；Boncz 等《MonetDB/X100: Hyper-Pipelining Query Execution》(CIDR 2005)——**向量化执行**的源头。
- **分布式 Join**：Blanas 等《A Comparison of Join Algorithms for Log Processing in MapReduce》(SIGMOD 2010)；Afrati & Ullman 关于 map-reduce join 的理论分析。
- **现代优化器实现**：**Apache Calcite**(2014 起)；**Orca**(Soliman 等, SIGMOD 2014, Greenplum/HAWQ)；**Spark SQL**(Armbrust 等, SIGMOD 2015)；**Velox**(Meta, 2021 起，统一执行引擎库)。

### 最新研究与产业进展
- **学习化查询优化（Learned QO）**：Kraska 等《Learned Cardinality Estimation》(CIDR 2019 / 及其 "Learned Index" 系列)；**Bao**(Marcus 等, SIGMOD 2021) 用强化学习选择 hint 集合；**Neo**(Marcus 等, VLDB 2019) 从历史执行中学习代价模型。这是 2019 年以来数据库研究最活跃的方向之一。
- **基数估计的误差本质**：Ioannidis & Christodoulakis (1991) 指出多谓词独立性假设会导致误差**指数级放大**——这解释了为什么"整体代价模型一定准"是错觉，也是学习化估计的动机。
- **自适应执行**：Spark 3.0+ **AQE**（运行时合并 shuffle 分区、切换 Join 策略、倾斜处理）、动态分区裁剪；Flink SQL、Trino 的动态过滤。
- **湖仓一体与开放格式**：Delta Lake / Apache Iceberg / Hudi + Trino / StarRocks / Databricks Photon；**Arrow/Parquet** 与向量化执行成为标配；**Substrait** 试图统一跨引擎的查询计划表示。
- 与 MySQL/OLTP 的分野：列存场景通常**没有传统索引**，靠 zone map/min-max 索引、排序键、物化视图与分区裁剪；把 MySQL 的索引调优经验直接搬到大数仓会失效（笔记中《SQL 优化》与《高性能 MySQL》两部分重合处正是易混点）。

### 常见误区 / 纠错
- **"先加索引"在大数据引擎上不成立**：Hive/Spark/ClickHouse 等列存引擎靠分区裁剪、排序键、稀疏索引与向量化，索引概念与 OLTP 不同；优化重点应是数据布局、Join 策略与倾斜治理。
- **"CBO 一定比 RBO 好"有前提**：CBO 的精度取决于统计信息新鲜度与基数估计质量；统计信息缺失或倾斜严重时，CBO 可能选出更差计划（这也是 AQE 与 hint 存在的意义）。
- **数据倾斜不是"加资源"能解决的**：热点 key 会让单个 task 拖垮整个 stage，正确做法是 salting（加盐打散）、map-side 聚合、广播 join 或两阶段聚合。
- **shuffle 是主要成本中心**：网络与磁盘 IO 往往主导查询耗时，减少 shuffle（colocate join、bucket join、广播小表）通常比微调 SQL 更有效。
