# 03 Lakehouse 与 Delta 表全生命周期 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题域重构章（00 §5 口径）：对位书名中"数据工程师的主表存储"面。机制事实 ✅ 来自
> learn.microsoft.com data-engineering/fundamentals 域当日 200 页；🔧 为本机类比（非 Fabric 行为）。

## 3.1 Lakehouse 是什么：一个 item，两套端点

✅ 转述 `https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview` 与
`.../create-lakehouse`：Lakehouse 是 Fabric 中**以 Delta Parquet 为底座的默认数据 item**——
Spark（笔记本/作业）写它，SQL 分析端点（T-SQL 只读连接串）读它，文件层经 OneLake 路径可见，
表/Schema 三级命名空间由平台托管（✅ `lakehouse-schemas` 在架，00 §2#17 文件清单）。

给工程师的三层解剖（⚠️ 推定的本书讲法，机制逐层有据）：

| 层 | Fabric 物件 | 你的操作面 |
|---|---|---|
| 文件层 | OneLake 内 Delta 目录（parquet+事务日志） | 原则上不直触；排障时经 Explorer 看 |
| 表语义层 | Table/Schema + SQL 端点 | `CREATE TABLE AS`、T-SQL 只读消费 ⚠️ |
| 计算层 | Spark 池 / 笔记本 / 作业定义 | 写路径主力（`04` 章） |

Delta 格式底座 ✅ 转述 `https://learn.microsoft.com/en-us/fabric/fundamentals/delta-lake-overview`：
ACID、时间旅行、模式演化等能力"由格式提供、由平台托管维护任务"——这句话是本章与全生命周期
主题的接缝。开放格式通感回链：
[../Delta_Lake_Definitive_Guide/02-基本操作-事务与CRUD.md](../Delta_Lake_Definitive_Guide/02-基本操作-事务与CRUD.md)。

## 3.2 写入模式工程学： append / overwrite / upsert / CDC

✅ `data-engineing/lakehouse-notebook-load-data` 与 `load-data-lakehouse`（当日 200，路径为
`.../data-engineering/load-data-lakehouse`）给出的装载菜单；⚠️ 编者按工程师决策树重排：

1. **批量落地**（`df.write mode=append/overwrite`）：最笨但最好排错；全量重刷只在维表尺度成立。
2. **MERGE/upsert**：Spark SQL `MERGE INTO`——键冲突语义显式化，替代"删了再插"的窗口裸奔期。
3. **CDC 入湖**：官方教程线含 change data capture 场景（✅ `lakehouse-and-delta-tables` 等页名实抓）；
   与 `06` 章 Mirroring 的分工：**Mirroring 搬"库的现值"，CDC 流搬"变更事件"**——前者面向分析库
   表全貌，后者面向事件语义（⚠️ 推定对比框架）。
4. **流式写**（Structured Streaming checkpoint）：见 `04/07` 章；Delta+流检查点= exactly-once 的
   Fabric 形态 ⚠️（机制语义的开放世界版在
   [../Delta_Lake_Definitive_Guide/06-流处理-Structured-Streaming.md](../Delta_Lake_Definitive_Guide/06-流处理-Structured-Streaming.md)，
   通用流语义在 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)）。

## 3.3 生命周期后半段：维护才是"指南"的含金量

✅ 转述 `https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance`
（当日页主题）：湖表三大慢性病与平台药方——

- **小文件病**：高频微批写→文件碎片→扫描规划开销上升。药方：平台侧自动优化（内部即
  OPTIMIZE/compaction 语义 ⚠️）+ 工程师侧"合理批尺寸"第一性责任。
- **快照垃圾病**：时间旅行保留期内的旧版本占存储；VACUUM/LAW（retention）语义 ⚠️ 与 Delta 开源
  一致但由平台托管触发（✅ `delta-lake-overview` 提及历史保留能力；参数策略需与合规窗口对齐——
  这是 `05` 章 #190 目录册语境的"治理决定物理"）。
- **统计信息病**：Z-order/聚簇类布局优化在托管面的自动化边界 ⚠️（当日页未展开处不脑补）。

⚠️ 推定的本书立场：数据工程师与平台运维的分界线正在被"托管维护"抹掉，但**成本账仍记在工作区
容量上**——维护是免费的错觉要破（省 CU 与占存储是同一枚硬币两面）。

## 3.4 🔧 实验 E2：提交与时间旅行的最小模型（非 Fabric 行为）

本机 DuckDB 1.5.5，manifest 指针模拟 Delta 事务日志（2026-10-02 实测，`exp_out.txt`）：

```text
[E2] commit(v2)=67.74 ms; as-of v1 rows=200000, as-of v2 rows=250000;
     old snapshot unchanged (immutable files = delta files appended)
```

- v1 快照 20 万行；提交 v2 = 写 5 万增量 + 重写快照文件 + manifest 追加一条 `{v:2}`，全程 67.74 ms。
- 关键行为复现：v2 提交**之后**读 v1 仍得 200,000 行——不可变文件+指针切换=时间旅行，
  与 Delta「快照隔离」同一机理（✅ 开源语义见 DDLG 04 章链接）。
- 与 Fabric 差异登记：真 Delta 的日志是 JSON 事务序列化、支持并发冲突重试与 ROW FILTER/列演化；
  本模型只有单写者语义——类比止于"为什么旧数据不用动"。

## 3.5 🔧 实验 E3：compaction 收益的量化直觉（非 Fabric 行为）

```text
[E3] scan-10-frags rows=200000 2.16 ms; OPTIMIZE-analog rewrite 47.44 ms;
     scan-merged rows=200000 1.21 ms; bytes 3.05MB -> 3.03MB; rowcount identical: True
```

- 10 碎片文件→单文件：扫描 2.16→1.21 ms（本机量级，**不外推**到分布式）；一次性整理费 47.44 ms。
- 两个工程结论：①收益随"读次数×碎片数"累积，读多写少者先受益；②`rowcount identical: True` 是
  维护作业的**验收断言**——compaction 必须行数不变（生产上再加校验和/抽样等值），这值得写进
  每个运维 runbook（⚠️ 编者语）。

## 3.6 Schema 演化与契约（⚠️ 推定小节，机制有据）

✅ `lakehouse-and-delta-tables`、`troubleshoot-spark-sql-schema-errors` 等页名实抓（文件清单）说明
平台把"模式漂移"当一等公民问题对待。⚠️ 重构观点：湖表是团队间契约，列的加入可以演化、类型
收窄与列删除应当走变更流程——契约工程通识见
[../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)
与 #190 目录册的 active metadata 语境。

## 3.7 与盘上诸书的联系

- Delta 机制正主（本册只取其产品化投影）：
  [../Delta_Lake_Definitive_Guide/04-表维护-时间旅行与VACUUM.md](../Delta_Lake_Definitive_Guide/04-表维护-时间旅行与VACUUM.md)、
  [../Delta_Lake_Up_and_Running/00-总览与阅读地图.md](../Delta_Lake_Up_and_Running/00-总览与阅读地图.md)。
- 中立湖仓存储论：[../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md](../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md)；
  开放格式工程面：[../Engineering_Lakehouses_with_Open_Table_Formats/00-总览与阅读地图.md](../Engineering_Lakehouses_with_Open_Table_Formats/00-总览与阅读地图.md)。
- 平台地图视角的姊妹章：[../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md](../Fundamentals_of_Microsoft_Fabric/04-Lakehouse与DeltaLake生态.md)。
- Spark 写路径内核：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。
- 波内只登记：#220（ADF 迁移食谱会复用本章装载菜单）、#219（Synapse 专用 SQL 池对照）。

## 核心概念速览（中英对照）

- **湖仓 item** — Lakehouse Item：Fabric 默认数据对象，Delta 底座+托管三级命名空间 ✅。
- **SQL 分析端点** — SQL Analytics Endpoint：湖表只读 T-SQL 消费面（写归 Spark）✅⚠️。
- **装载菜单** — Load Patterns：append/overwrite/merge/CDC/流式五档，决策树见 3.2 ⚠️。
- **托管维护** — Managed Table Maintenance：小文件/历史/统计三类自动作业面 ✅。
- **快照垃圾** — Snapshot Bloat：时间旅行保留期与存储账单的张力，合规窗口定生死 ⚠️。
- **验收断言** — Invariant Check（编者词）：维护前后行数/校验和必须一致 🔧E3。
- **不可变文件+指针** — Immutable Files + Log Pointer：时间旅行的机理底座 🔧E2 ✅。
- **模式演化** — Schema Evolution：可加列、慎删改；湖表=团队契约 ⚠️✅。
- **镜像 vs CDC** — Mirroring vs Change-Feed：库现值整体搬 vs 变更事件流，06 章分工线 ⚠️。
- **读放大** — Read Amplification：碎片×读次数的成本复利，批尺寸是第一性责任 🔧E3 ⚠️。

## 最新演进与工业实践

2024→2026（URL 均 2026-10-02 实测 200；⚠️ 为转述/推断）：

- **文档面的生命周期专页化**：`lakehouse-table-maintenance` 从 how-to 升级为独立概念页（✅ 域内
  文件清单实抓），标志"托管维护"从功能附录变成一等文档公民——指南类书籍的"维护章"因此有了
  官方骨架可挂靠 ⚠️。
- **故障排查面成体系**：`troubleshoot-lakehouse`、`troubleshoot-spark-storage-connectivity-errors` 等
  专页在架（✅ 文件清单）——工业实践上"湖表运维手册"条目化程度与这些页一一对应 ⚠️。
- **格式中立压力**：开放生态（Iceberg REST 化、Unity Catalog 扩散，盘上
  [../Apache_Polaris_TDG/00-总览与阅读地图.md](../Apache_Polaris_TDG/00-总览与阅读地图.md)、
  [../Data_Governance_with_Unity_Catalog/00-总览与阅读地图.md](../Data_Governance_with_Unity_Catalog/00-总览与阅读地图.md)）
  持续把"默认 Delta"厂商锚点变成议题；本册 02/03 章的选型评审应保留"如果迁出怎么办"一栏 ⚠️。
- **数字纪律重申**：🔧E2/E3 的 67.74 ms/47.44 ms/1.21 ms 均为本机单机量级，**不构成任何 Fabric
  容量规划输入**；平台行为一律以当日 learn 页与账户内实测为准（红线口径）。
- 书目侧：本章涉及的"原书是否真按此顺序讲"完全不可证（O'Reilly 403），全部为 ⚠️ 重构；
  若人工终裁取得原书 TOC，请优先勘正 3.2/3.3 的章内归并（00 §10 勘误回馈义务）。
