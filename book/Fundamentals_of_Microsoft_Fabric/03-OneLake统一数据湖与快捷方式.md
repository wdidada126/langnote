# 03 · OneLake：统一数据湖与快捷方式（⚠️ 推定章：原书 TOC 未实抓，主题重构见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节）

OneLake 是全书 "lake-centric" 概念的物质载体（官方简介第三条）。
本章主线：**命名空间 → 快捷方式 → 复制语义与软删除 → 安全面 → 目录**，
全部锚定 ✅ 2026-09-27 实测 200 的 Learn 页。

## 3.1 统一命名空间：一个租户一棵"文件树"

官方口径：OneLake 为每个组织提供**单一、统一、可写**的分析数据湖，
逻辑结构 `OneLake/<租户>/<容量或短名>/<工作区>/<item>/…`，用户从任一工作区看到的都是同一棵树
（✅ https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview ，访问 2026-09-27）。

⚠️ 关键澄清（文档亦有说明）：逻辑统一 ≠ 物理单桶——数据按容量所在区域分布，跨地域落点有合规含义（09 章）。

对外 API 面（湖负责"文件脸"）：

- ABFS（HDFS 语义，Spark 原生友好）；
- Blob 兼容 REST（对象存储工具链可复用）；
- T-SQL（经湖仓 SQL 分析端点，04 章）；
- 目录/发现面（OneLake Catalog，3.6）。

## 3.2 Shortcuts：湖之间的"指针文件系统"

Shortcut = 把外部存储（S3、ADLS Gen2、GCS、另一湖的 Blob…）**挂载进 OneLake 命名空间而不复制**
（✅ https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts ，访问 2026-09-27）。
三点工程后果（⚠️ 推演 + ✅ 页面支持）：

1. 数据可以"留在原地"被全家桶消费——这是对"必须全量搬进微软云"质疑的官方答案，
   与 Data Mesh"数据主权在域"存在张力/兼容双面（✅ 概念对照 [../Data_Mesh/02-领域所有权原则.md](../Data_Mesh/02-领域所有权原则.md)）。
2. 治理边界随指针外移：Shortcut 指向的数据其生命周期由源系统负责，软删除/保留策略不覆盖（3.4）。
3. 性能与事务性受源限制：外部数据经由镜像/懒读路径消费，别按本地 Delta 预期做延迟预算（⚠️ 无官方延迟 SLA 数字可引）。

## 3.3 🔧 EXP-1：零拷贝指针 vs 复制导入（本机类比，非 Fabric 行为）

环境：DuckDB 1.5.5 / SQLite 3.45.3 / Python 3.13.2；数据 1,000,000 行事件表（Parquet 8.18 MB）；
方法脚本 D:\develops\tmp\dbwave_w5_fabric\exp.py，实测于 2026-09-27：

- 建 VIEW 指向外部 Parquet（≈Shortcut）：**1.2 ms**；随后查询 1,000,000 行：**0.9 ms**；
- COPY 建内表（≈导入复制）：**14.9 ms** + 磁盘多出一份 **8.18 MB**。

读数：**指针的创建成本与数据量无关；复制的创建成本与数据量线性相关**——这就是 Shortcut 卖点的量纲演示。
局限声明：DuckDB 视图没有跨云凭据委身/审计/目录登记语义，真实 Shortcut 还要过 3.5 的权限面（⚠️）。

## 3.4 复制语义、软删除与"湖的垃圾管理"

✅ https://learn.microsoft.com/en-us/fabric/onelake/soft-delete （访问 2026-09-27）：
OneLake 提供软删除保护。⚠️ 转述：可按范围启用、保留期内可恢复；**缺省开关与保留天数请以当日页为准**，本目录不背未验证的数字。

配套心智：**湖里的"误删恢复"从备份问题变成策略问题**。
与 Delta 表级时间旅行（04 章 EXP-3）互补成两层：

- 文件层软删除 → 管"整棵目录树"的误删；
- 表格式层快照 → 管"一张表的版本序列"。

## 3.5 OneLake 安全模型：三面账（为 09 章埋桩）

湖级安全三件套（✅ https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security ，访问 2026-09-27）：

1. 路径 ACL（类 POSIX 风格，作用于湖资源）；
2. item/工作区角色（09 章三层塔）；
3. 引擎侧权限（SQL 端点/仓侧，04/05 章）。

⚠️ 评审要点：同一张表被三种 API 面读取时，**必须三面对表**，
否则 REST 面成为 T-SQL DENY 的旁路——这是湖中心架构的固有审计题
（对照 [../Understanding_Data_Governance/08-合规与隐私.md](../Understanding_Data_Governance/08-合规与隐私.md)）。

## 3.6 OneLake Catalog：从"文件浏览器"升格为"联邦目录"

✅ https://learn.microsoft.com/en-us/fabric/governance/onelake-catalog-overview （访问 2026-09-27）：
跨工作区/租户的资产发现，支持联邦目录语义；与 Databricks Unity Catalog 的互操作专页见 09 章 9.4。
治理视角：目录是"治理的执行器不是治理本身"（✅ 同构论点见 [../Understanding_Data_Governance/05-元数据管理与数据目录.md](../Understanding_Data_Governance/05-元数据管理与数据目录.md)）。

## 3.7 湖到引擎的内部通道：SQL 端点读 OneLake 的权限耦合

Lakehouse 的 SQL 分析端点之所以能 T-SQL 查文件，靠 OneLake 把 Delta 文件登记进引擎元数据
（✅ https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint ，2026-09-27）；
跨面读的安全耦合面专页（✅ https://learn.microsoft.com/en-us/fabric/onelake/sql-analytics-endpoint-onelake-security ）。
⚠️ 评审要点：这种"湖表自动变 T-SQL 视图"的便利是 Fabric 相对裸 ADLS+Spark 的核心增值之一。

## 3.8 🔧 EXP-3 预告：快照直觉（详见 04 章 4.4）

用 manifest 文件指向"当前有效文件集"模拟提交链：CTAS 快照 11.2 ms、追加 delta 后 v2 读 1,050,000 行/1.36 ms、v1 快照不变。
OneLake 的软删除与该表级快照共同构成"两层后悔药"（非 Fabric 行为，2026-09-27 实测）。

## 3.9 本章收口：湖中心架构的三条守恒律

1. **指针不复制原则**：先 Shortcut 后 Copy（3.3 量纲）；
2. **一份数据多张脸原则**：写入方唯一（引擎选择见 04 章），读取方多元；
3. **删除要过两层原则**：文件软删除 + 表快照（3.4）。
三条在 10 章端到端模板里逐一回收（评审清单第 2/7 条）。

## 3.10 自测与讨论（⚠️ 教学构造）

1. 你的组织里哪张"想搬又搬不动"的大表最适合第一个 Shortcut 试点？为什么？（提示：3.2 三后果）
2. 软删除与 Delta 快照各自防什么事故、各花谁的钱？（提示：3.4 两层后悔药）
3. REST 面旁路 T-SQL DENY 的具体复现步骤是什么？写出你租户的三面账对表脚本思路。（提示：3.5）

## 核心概念速览（中英对照）

- **OneLake** — OneLake：组织级统一分析湖，逻辑单树、物理分域。
- **快捷方式** — Shortcut：把外部存储挂载进 OneLake 的零拷贝指针。
- **ABFS** — Azure Blob File System：HDFS 语义的湖文件 API 面。
- **软删除** — Soft delete：文件层可恢复删除保护，策略开关制。
- **路径 ACL** — Path-level ACL：湖资源上的类 POSIX 权限层。
- **OneLake Catalog** — OneLake Catalog：跨租户资产发现与联邦目录层。
- **命名空间树** — Namespace tree：租户/容量/工作区/item 四级路径约定。
- **零拷贝入湖** — Zero-copy ingest：经 Shortcut/镜像挂载而非搬运数据。
- **外部湖** — External lake：S3/ADLS/GCS 等被指针接进来的数据源域。
- **三面账** — Three-plane security：湖文件面、item 面、引擎面权限必须对表。

## 最新演进与工业实践

- **Unity Catalog 互操作落地中**（✅ 访问 2026-09-27）：专页 https://learn.microsoft.com/en-us/fabric/onelake/onelake-unity-catalog 实测 200
  （"Integrate Databricks Unity Catalog with OneLake"）；Databricks 侧对偶文档存在（✅ learn.microsoft.com/zh-cn/azure/databricks/partners/bi/fabric 搜索快照）。
  2025-12-31 Fabric 官方博客标题 "Databricks Unity Catalog tables available in Microsoft Fabric"（⚠️ 博客 403 未全文，仅题+日期）。
- **镜像生态扩张**（✅ https://learn.microsoft.com/en-us/fabric/mirroring/overview 实测 200，2026-09-27）：
  跨云"湖湖互指"已是 2026 平台竞争主战场（⚠️ 观点）；Snowflake 方向对位读 [../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md)。
- **概念类比书目**：湖上"开放格式+目录"中立实现的可跑版见 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md) 与
  [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)（"同一棵树谁来管"的 Iceberg 对照——Fabric 的树是微软家的）。
- **工业实践红线**（⚠️ 经验性条目，依据 3.5 结构推演，非官方清单原文）：
  生产租户评审三查——软删除开关核查、Shortcut 凭据轮换、湖路径 ACL 与引擎侧 DENY 的一致性抽查。
