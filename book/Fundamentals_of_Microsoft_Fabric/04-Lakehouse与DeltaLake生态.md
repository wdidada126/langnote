# 04 · Lakehouse 与 Delta Lake 生态（⚠️ 推定章：原书 TOC 未实抓，主题重构见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节）

Lakehouse 是 Fabric 数据工程面的核心 item；官方把它定义为"OneLake 中由托管 Delta Parquet 组成的分析数据表示"
（✅ https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview ，访问 2026-09-27）。
本章四线：**表底座 → 双 API → 维护经济学 → 与开放表格式谱系辨析**。

## 4.1 Delta Lake：Fabric 的默认表格式立场

✅ https://learn.microsoft.com/en-us/fabric/fundamentals/delta-lake-overview （访问 2026-09-27）：
Fabric 的 Lakehouse 表即 Delta（Parquet 数据文件 + 事务日志），Spark 写入方托管。

⚠️ 与 Databricks 的关系陈述：Delta 是 Databricks 主推并开放化的表格式，
Fabric 采用它 = 接受对手格式作为自家湖底座（商业协调层面 ⚠️ 观点）。

谱系深读（盘上正典，均已验名）：

- Databricks 阵营专著：[../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md](../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md)
  （其 [02-基本操作-事务与CRUD.md](../Delta_Lake_Definitive_Guide/02-基本操作-事务与CRUD.md)、[04-表维护-时间旅行与VACUUM.md](../Delta_Lake_Definitive_Guide/04-表维护-时间旅行与VACUUM.md) 与本节对位）；
- 中立对比：[../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md](../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md)；
- 竞品格式：[../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)、[../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md)。

## 4.2 一张表两张脸：Spark API 与 SQL 分析端点

写路径：Notebook / Spark Job Definition（✅ https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse 演示门户与 Notebook 双入口，2026-09-27）。

读路径三张：

1. Spark（pyspark/Spark SQL）；
2. **SQL 分析端点**（T-SQL；⚠️ 其 DML 支持面演进快，以 https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint 当日页为准，页存在 ✅）；
3. 湖文件 REST/ABFS（03 章）。

端点定位辨析（✅ 同页）：它是"湖的 T-SQL 查询面"，**不是 Warehouse item**——
持久语义、权限模型都不同；选型由 5.3 决策指南处理。

## 4.3 小文件经济学与 🔧 EXP-2：为什么"写入便宜、扫描贵"

湖仓表按 Spark 分区/微批产出文件，高频小写入 → 文件数与元数据开销爆炸（⚠️ 通识；
Fabric 侧 OPTIMIZE/VACUUM 的当前文档页名本次未逐条实锚，**禁引旧链规则适用**，维护语义以当日 Lakehouse 文档为准）。

🔧 EXP-2 本机量化类比（非 Fabric 行为；DuckDB 1.5.5，1,000,000 行，2026-09-27）：

- 10 个碎片 Parquet 文件（合计 6.14 MB）全扫描聚合：**2.91 ms**；
- CTAS+COPY 压缩为单文件（6.24 MB）的一次性成本：**106 ms**；
- 压缩后同查询：**2.29 ms**；
- 前后结果一致：count 1,000,000、sum 714,214,285.7
  （逐位比较初报 false，复核为浮点求和次序 ULP 差，round 后完全一致——诚实登记）。

读数：本例"文件数 ÷10"换约 21% 扫描提速 + 一次性 106 ms 写放大；
数据量越大、查询越频繁，compaction 杠杆越接近数量级（方向性外推 ⚠️）。

## 4.4 🔧 EXP-3：时间旅行与快照的机制类比（非 Fabric 行为）

Delta 的 _delta_log = "表版本 → 文件清单"的提交链（✅ 概念对 [../Delta_Lake_Definitive_Guide/04-表维护-时间旅行与VACUUM.md](../Delta_Lake_Definitive_Guide/04-表维护-时间旅行与VACUUM.md)）。
本机用 manifest 文件指向"当前有效文件集"模拟提交：

- CTAS 建 v1 快照（1,000,000 行）：**11.2 ms**；
- 追加 delta_001.parquet（+50,000 行），manifest 升 v2；
- v2 读取：**1,050,000 行 / 1.36 ms**；v1 快照仍返回 **1,000,000 行**。

结论（类比层）：**快照隔离的本质是"读旧版本=换指针"，零拷贝**；
真实 Delta 额外提供模式演进、删除向量、CDF 等（⚠️ 转述，见 DLTG 其 07 章）。

## 4.5 Medallion 分层：Fabric 语境下的落点

bronze/silver/gold 是 Lakehouse 内（或多 Lakehouse 间）的表族组织法
（✅ 概念对 [../Delta_Lake_Definitive_Guide/08-湖仓架构-Medallion.md](../Delta_Lake_Definitive_Guide/08-湖仓架构-Medallion.md)）。
⚠️ 推定本书立场：443 页通论册大概率用"端到端方案"章把 Medallion 收作默认参考架构（本目录 10 章展开）。
盘上反方观点必读 [../Data_Mesh/06-拐点与旧架构的尽头.md](../Data_Mesh/06-拐点与旧架构的尽头.md)：
中心分层 vs 域内产品化之争，在 Fabric 里的实际调和是"一工作区一域、域内自分层"。

## 4.6 Spark 体验与开源谱系的落差清单（评审用）

⚠️ 转述 + ✅ 概念对照 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)、[../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)：

- 得到：凭据与 ADLS 一体、零集群运维、session/job 两级池化、Delta 托管写入、与工作区权限同构；
- 付出：引擎版本滞后、参数面收窄、部分开源生态库需自定义环境（⚠️ 能力面以当日页为准）；
- 给"从 Databricks 搬家"读者的判据：UC 语义映射到 OneLake Catalog（09 章互操作），notebook 参数化映射到 Pipeline 活动（06 章）。

## 4.7 湖仓表维护日历（⚠️ 教学重构，非官方模板）

| 周期 | 动作 | 类比锚 |
|---|---|---|
| 每次写入 | 分区设计审查（防碎片源头） | 4.3 |
| 每日 | compaction/整理窗口 | 🔧 EXP-2（106 ms/百万行量纲） |
| 每周 | 快照保留策略 vs 软删除联动 | 🔧 EXP-3 + 03 章 3.4 |
| 每月 | 孤儿文件回收/VACUUM 预算 | DLTG 04 章对位 |
| 每季 | 表格式能力复审（DV/CDF 等） | 4.1 ⚠️ |

## 4.8 本章收口三问

1. 该表需要高频事务 MERGE 吗？→ 多半该用 Warehouse（05 章）；
2. 有跨云消费者吗？→ Delta 开放文件 + Shortcut/镜像双解（03/06 章）；
3. 维护自动化了吗？→ 对照 4.3/4.7 建小文件预算。三问模板回收进 10 章评审清单。

## 4.9 一句话记忆桩（⚠️ 教学构造）

**"日志管版本、清单指文件、指针给时间"**——Delta 时间旅行三件套；湖仓一切维护动作都是在给"文件数×清单大小"这对乘积做减法。

## 核心概念速览（中英对照）

- **湖仓** — Lakehouse：OneLake 上由托管 Delta 表组成的分析数据表示。
- **Delta Lake** — Delta Lake：Parquet+事务日志的开放表格式，Fabric 默认底座。
- **事务日志** — Transaction log（_delta_log）：表版本与文件清单的提交链。
- **SQL 分析端点** — SQL analytics endpoint：湖表的 T-SQL 查询面（"湖上仓脸"）。
- **小文件问题** — Small file problem：高频小写入导致的扫描/元数据成本膨胀。
- **压缩整理** — Compaction/OPTIMIZE：碎片合并，写放大换扫描提速。
- **时间旅行** — Time travel：按版本读历史快照的表格式能力。
- **VACUUM** — VACUUM：过期版本文件回收，与软删除分层协同。
- **Medallion** — Medallion architecture：bronze/silver/gold 分层数据组织法。
- **Spark 作业项** — Spark Job Definition：无头 Spark 计算 item，供编排调用。
- **删除向量** — Deletion vectors：Delta 行级删除的新式编码（⚠️ 转述）。

## 最新演进与工业实践

- **2026 文档域迁移**（✅ 访问 2026-09-27）：Lakehouse 文档整体挪入 `data-engineering/*`
  （旧 `data-science/lakehouse-overview` 已 404，禁引；`data-engineering-overview` 枢纽 200 实测）。读旧博客前先 `curl -I`。
- **表格式政治**：Fabric 以 Delta 为默认；截至 2026-09-27 本次核查**未在 Learn 域定位到 Fabric 原生 Iceberg 表 item 的权威页**，
  二手传闻一律拒引，登记缺口。开放格式对决全貌读 [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md) 与 Delta/Hudi 双册。
- **维护自动化**：托管 compaction/孤儿清理类能力 2024–2026 从"手动 OPTIMIZE"走向平台自动化（⚠️ 未逐条锚定当前功能页，评审以当日维护文档为准）。
- **工业实践**：🔧 4.3/4.4 的"一次性 106 ms vs 每次省 0.6 ms"型权衡，正是生产"每日整理窗口"决策的原型；
  真实数据量下杠杆放大为数量级差（DuckDB 数字仅示方向，**非 Fabric/Delta 基准**）。
- **延伸对位**：流式湖仓（Flink 血统）路线 [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md) 与 Fabric 的"批湖+KQL 流"分工互为镜像。
