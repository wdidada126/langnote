# 05 湖仓一体与 Delta Lake — Data Lake, Lake House, and Delta Lake 下半（原书第 3 章 B 段，章级 ✅）

> 章题 ✅ 把 Lake House 与 Delta Lake 并立（DOI `_3`，pp.95–160）；B 段边界线 ⚠️ 推定。
> 机制 = 官方文档转述 ⚠️ + ✅ URL（docs.delta.io / learn.microsoft Databricks 域 / iceberg.apache.org，
> 2026-10-02 验 200）；云上 Delta 事务行为不可本机实测——🔧G3/G4 是 DuckDB/SQLite 概念类比，
> **非 Databricks/Delta/两云平台行为**。

## 5.1 湖仓=把仓库合同签回湖里（⚠️ 转述 + ✅ 概念锚）

一句话定义：在对象存储底座（04 章）上补齐**事务、schema 治理、时间旅行、并发读写**四份合同，
使同一份数据同时服务 BI 与 ML。三块官方锚：
- Databricks 起源叙事与 medallion（✅ https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion，Azure Databricks 域）；
- Delta Lake 开放发行版特性页（✅ https://docs.delta.io/latest/index.html）；
- 表格式中立对照（✅ https://iceberg.apache.org/docs/latest/）。

盘上母题深读分工：架构总论 [../The_Data_Lakehouse/00-总览与阅读地图.md](../The_Data_Lakehouse/00-总览与阅读地图.md)、
工程落地 [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)、
Bill Inmon 理论与表格式互证 [../The_Data_Lakehouse/12-对照章-Inmon理论与开放表格式实现.md](../The_Data_Lakehouse/12-对照章-Inmon理论与开放表格式实现.md)——本册只取「多云装配」角度。

## 5.2 Delta Lake 四机制与其多云落点（⚠️ 转述，URL 对位）

| 机制 | Delta 语义（⚠️ OS1 口径） | Azure 落点 | AWS 落点 |
|---|---|---|---|
| 事务日志 ACID | 写=new commit 入日志，读=快照隔离 | Databricks on Azure；Synapse⇄Delta 互读（⚠️） | Databricks on AWS；Athena/Redshift 外表读（⚠️） |
| 时间旅行 | 按版本/时间戳查旧快照 | 同左 | 同左 |
| schema 演进/强制 | 写入契约校验+受控加列 | 同左 | 同左 |
| OPTIMIZE/Z-ORDER | 小文件合并+布局聚簇 | 同左 | 同左 |

多云 twist：**同一 Delta 表在两云可各自挂载**，但两云各自「读同一份还是各存一份」是组织题——
本册推定书答案：跨云共享表数据（单副本+双目录登记）优于双写复制（一致性噩梦），
前提把 D3 出云费算进读频（04 章 🔧G1 的税形同样适用跨云读）。

## 5.3 🔧 实测 E-G3：medallion 三层的漏斗账本（DuckDB 1.5.5，非平台行为）

脚本 demo2.py：20 万行原始 CSV 混 5% 空值+1 万条重复行。

| 层 | 动作 | 行数 | 用时 |
|---|---|---|---|
| bronze | `read_csv` 原样落表 | 210,000 | 185ms |
| silver | DISTINCT 去重+TRY_CAST 剔空 | **200,043**（剔除 9,957） | 119ms |
| gold | 按城市聚合 | 3 | 5ms |

方向性结论 ⚠️：bronze→silver 的**剔除量应作为监控指标**（本例 4.7%）——medallion 官方语义里
数据质量门就设在这一刀（✅AZ10 域）；gold 行数坍缩到维度级=报表读放大保护。
Databricks 真平台上另有期望值管理/自动优化作业，数字模型远复杂于此，**不可换算** 📐。

## 5.4 🔧 实测 E-G4：时间旅行的最简实现（版本目录+清单，非 Delta 行为）

脚本 demo3.py：silver 表导出两个不可变快照目录 `tbl/v1`（前 8 万行）与 `tbl/v2`（偶数 id 100,054 行）：

| 版本 | 行数 | 金额和 | 读取用时 |
|---|---|---|---|
| v1 快照 | 80,000 | 3,837,407 | 2.3ms |
| v2 快照 | 100,054 | 4,795,100 | 1.6ms |

两版本**同库并存、各自可查、互不覆写**——这就是 Delta「按版本读旧」的可移植语义核心；
真 Delta 用事务日志把版本挂到每行文件引用上（⚠️ OS1 转述），本实现用目录+清单文件模拟。
工业用例（⚠️ 推定书中场景）：错误装载回滚、合规留痕、A/B 特征基线冻结。

## 5.5 中位架构 vs 存算原生：湖仓的两种性格（⚠️ 对照 03 章形态）

- **性格A 仓库血统**（Synapse/Redshift 为主干，湖做前厅）：合同在引擎里，湖仓化=外表+零ETL 缝合；
- **性格B 湖血统**（Databricks/表格式为主干，仓做出口）：合同在文件层，BI 靠物化视图/直查。

本册多云蓝图允许**两云各取一性格**（例：Azure 走 A 承接 T-SQL 资产、AWS 走 B 承接 ML 特征栈），
但 medallion 分层命名与质量门必须全局统一——否则 10 章治理的「目录一致性」退化为「人肉对账」。
对位表联动：布局经济学细节在 [../Tuning_the_Snowflake_Data_Cloud/04-微分区.md](../Tuning_the_Snowflake_Data_Cloud/04-微分区.md)（托管引擎一侧）与
[../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md](../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md)（仓库一侧），本章不重复。

## 5.6 本章学习检查点（⚠️ 推定）

1. 说出四份「湖仓合同」各对应哪条 Delta 机制与哪个 🔧 实验；
2. 用 🔧G3 的 4.7% 剔除率定义一条生产告警（阈值、归属层、动作）；
3. 性格A/性格B 各举一类不适配负载（A 不适配高频 ML 特征回写；B 不适配高并发语义报表——⚠️ 推定口径）。

## 5.7 开放表格式三选一速查（⚠️ 通说 + ✅OS1/OS2 锚）

| 维度 | Delta Lake | Iceberg | Hudi |
|---|---|---|---|
| 合同载体 | 事务日志（OS1） | 引擎无关元数据层（OS2） | 日志+时间线 |
| 两云姿态 | Databricks 生态第一方（⚠️AZ6/AWS2 域） | 两云原生支持扩张中（⚠️ 各家现行口径） | 托管件内嵌（⚠️） |
| 多引擎互读 | 引擎族内最佳 | 中立牌最强 | 面偏窄 |
| 本册裁定 | 性格B 已沉域继续用 | 新域默认候选（09 章演进条三同向） | 存量才议 |

选型题不是「谁最好」，而是「哪个合同的双方引擎都认」（5.5 两性格都要过，⚠️ 推定书立场）。

## 5.8 读后回环三问（自测用 ⚠️）

1. 四份湖仓合同（5.1）分别由哪个机制兑现、哪个 🔧 实验侧写？（事务/时间旅行/schema/并发 ↔ G4/G3）；
2. 「双目录单副本」在什么负载下应反转为「单目录双副本」？（答：读多写少+驻留强制域，5.2 twist）；
3. 你司 bronze→silver 剔除率现在是多少？写不出数字，10.7 的 L3 就是空话。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 湖仓一体 | Lakehouse | 湖底座+仓合同：事务/schema/时间旅行/并发四件套 |
| Delta Lake | Delta Lake | 对象存储上的事务表格式（⚠️ OS1 口径），书题点名主角 |
| 事务日志 | Transaction Log | 版本与文件引用的真相账本 |
| 时间旅行 | Time Travel | 按版本/时点读旧快照（🔧G4 模拟） |
| 中位分层 | Medallion Architecture | bronze/silver/gold 三级质量流水线（✅AZ10） |
| schema 强制/演进 | Schema Enforcement/Evolution | 写入契约校验与受控加列 |
| OPTIMIZE / Z-ORDER | File compaction / layout clustering | 小文件合并+布局聚簇（对位微分区/聚簇键） |
| 开放表格式 | Open Table Format | Delta/Iceberg/Hudi 一族的跨引擎合同层（✅OS2） |
| 双目录单副本 | Single-copy Dual-catalog | 跨云共享表的推荐装配（5.2 twist） |
| 性格A/性格B | Warehouse-heritage / Lake-heritage | 湖仓两种血统（5.5） |

## 最新演进与工业实践

- **Iceberg 升为两云「最大公约数」**（2024–2026，⚠️ 转述；✅ https://iceberg.apache.org/docs/latest/ 与
  https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html 现行口径）：Delta 独家语义让位于
  「表格式多引擎互读」——Redshift/Synapse/Athena/Glue 的 Iceberg 支持面扩张快于本章书快照；
  盘上互证：[../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md](../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md)、
  [../The_Data_Lakehouse/12-对照章-Inmon理论与开放表格式实现.md](../The_Data_Lakehouse/12-对照章-Inmon理论与开放表格式实现.md)。
- **Databricks 在两云同为「第一方」**（⚠️；✅ https://learn.microsoft.com/en-us/azure/databricks/getting-started/overview）：
  Azure Databricks 与 AWS 原生嵌入的部署形态趋同——5.5「两云各取性格」的现实成本已低于本书成书时点。
- **托管时间旅行与保留策略计费化**（⚠️ 转述）：旧版本文件占存储费，「回看 7 天 vs 77 天」进入
  FinOps 谈判桌——🔧G4 的目录并存模型直观可算这笔账（版本数×快照大小）。
- **仓侧缝合加强**（⚠️；盘上对位 [../Amazon_Redshift_TDG/04-数据转换策略.md](../Amazon_Redshift_TDG/04-数据转换策略.md)）：
  性格A 路线的「外表即湖仓」在 2025 后普遍获得写回与合并能力，两性格边界继续变糊——
  选型结论（5.5）从「择一」软化为「按数据域择一」。
