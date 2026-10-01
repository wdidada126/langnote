# 03 Azure Synapse Analytics 导论 — Introduction to Azure Synapse Analytics（原书第 3 章，pp.49–68）

> 章题与页区间 ✅ Crossref 存款记录实抓（DOI 后缀 `_3`，pp.49–68）；章内小节 ⚠️ 推定（无公开样章），
> 按章题语义与 learn.microsoft.com Synapse 概览文档域组织。Synapse 为云服务，不可本机实测，机制一律
> 「⚠️ 转述 + ✅ URL（2026-10-02 逐条验 200）」。

## 3.1 本章在全书中的位置

第 3 章首次点名产品：把 01 的概念、02 的架构张力收拢到「Azure Synapse Analytics 是什么、从哪来、
包含什么」。本章 20 页解决三件事：命名史与血统（避免与 Azure SQL Data Warehouse 混读）、组件清单
（工作区里有什么）、以及「为什么要把散件合并成一个服务」的产品逻辑。04 章起进入架构与组件纵深。

## 3.2 血统与命名史（⚠️ 转述 + ✅ 文档）

- 产品前史：并行数据仓库 APS/PDW（on-prem 一体机）→ **Azure SQL Data Warehouse**（2016 GA 的公有云
  MPP 数仓）→ 2019 Ignite 宣布更名/合并为 **Azure Synapse Analytics**（2021 本书出版时为统一分析服务
  口径）✅ `overview-faq`、`sql-data-warehouse/sql-data-warehouse-overview-what-is`。
- 内核谱系要点（详见 [00](00-总览与阅读地图.md) §5 对位表）：专用 SQL 池继承 SQL Server 分析代码线
  的列存/统计/计划缓存机理——盘上
  [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)、
  [../SQL_Server_2008_Internals/00-总览与阅读地图.md](../SQL_Server_2008_Internals/00-总览与阅读地图.md)
  为内核深读（在盘 ✅ 实名已验）。
- 「Analytics」后缀的营销史 ⚠️：改名同步发生在 BigQuery、Redshift 等厂，指向同一趋势——仓产品
  向「多负载平台」演化。

## 3.3 官方定义与组件清单

- 官方一句话 ⚠️ 转述：Synapse = **无缝的湖仓（unified lakehouse）分析服务**，集数据摄入、即席查询、
  企业数仓、ETL、实时分析于一体 ✅ `overview-what-is`。
- 工作区内五大件（04–09 章按此展开）：
  1. **专用 SQL 池**（原 ADS 仓，预置 MPP；05 章）✅ `sql-data-warehouse/sql-data-warehouse-overview-what-is`；
  2. **无服务器 SQL 池**（按需查询湖文件，按处理量计费；05 章并行小节）✅
     `sql/on-demand-workspace-overview`、`quickstart-serverless-sql-pool`；
  3. **Spark 池**（原生引擎集成+SynapseML；06 章）✅ `spark/apache-spark-overview`；
  4. **管道（Pipelines）**（ADF 血统集成服务；07 章）✅ `get-started-pipelines`；
  5. **Synapse Link**（零 ETL 近实时分析；09 章）✅ `synapse-link/sql-synapse-link-overview`。
- 外围粘合层：Power BI 数据集直连 ✅ `get-started-visualize-power-bi`；监控中心 ✅ `get-started-monitor`；
  安全/RBAC/网络（08 章）✅ `security/synapse-workspace-access-control-overview`。

## 3.4 「一个服务」解决了什么、没解决什么

- 解决：一套安全边界（工作区级 RBAC）、一份湖存储（ADLS Gen2 为默认账房 ⚠️）、一个监控面、
  跨引擎共享数据无需复制（引擎间语义差异仍在，04 章诚实清单）。
- 没解决：计费面仍是多套（DWU / 按处理量 / Spark 核心时 / 管道活动数 ⚠️ 转述），角色仍各有学习曲线；
  「统一」是存储与安全层面的统一，不是执行引擎的统一。

## 3.5 上手机动线（章尾工程视角 ⚠️ 推定组织）

- 建工作区 ✅ `get-started-create-workspace`、`quickstart-create-workspace`（需要订阅、RM 参与者权限、
  默认存储账户绑定）；
- 体验 Serverless 查湖 ✅ `quickstart-serverless-sql-pool`；
- 建专用池并装载 ✅ `quickstart-create-sql-pool-studio`、`quickstart-copy-activity-load-sql-pool`；
- 建 Spark 池与笔记本 ✅ `quickstart-create-apache-spark-pool-studio`、`quickstart-apache-spark-notebook`；
- 挂监控 ✅ `get-started-monitor`。
- 注：本目录所有 learn URL 为 2026-10-02 实测 200；部分 2021 代旧 slug 已 404（登记于
  [00](00-总览与阅读地图.md) §2 勘误）。

## 3.6 本章与兄弟书的坐标系

- 与 O'Reilly Fabric 教材（盘上 #221，
  [../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)
  在盘 ✅）的关系：2021 Synapse = 2023+ Fabric 的直接前身，组件级映射见 10 章「最新演进」；读法上
  本册给「为什么长成这样」的历史层，#221 给「现在该怎样用」的操作层。
- 与盘上云仓册的坐标系：Synapse 专用池=预置型 MPP，与 Redshift RS/RA3、Snowflake T 恤码同代概念，
  对照表见 05 章；BigQuery 槽位模式更接近 Serverless 一侧 ⚠️ 转述。

## 3.7 常见误区

1. **「Synapse=ADS 换皮」**——专用池只是其一把子组件；Spark/管道/Link 是新增血脉，混读会低估运维面。
2. **「Serverless 永远便宜」**——高并发重复查询下预置型或物化更快更省（账本框架在 02 章 §2.7）。
3. **「改名即换代」**——内核连续性强于产品叙事，SQL Server 系技能（T-SQL/索引/统计）平移价值高，
   这正是盘上两册 SQL Server 内部机制书仍必读的原因（[00](00-总览与阅读地图.md) §5）。
4. **「统一平台=一种引擎打天下」**——04 章将给出各引擎各自的最适负载。

## 3.8 Synapse↔旧术语对照速查（迁移时代「源端词典」⚠️ 组织，口径 ✅ `overview-terminology`）

| 你旧资产里的名字 | Synapse 里的对应物 | 继续演化后的 2026 名 |
| --- | --- | --- |
| Azure SQL Data Warehouse / ADS | Dedicated SQL Pool（专用池） | Fabric data warehouse |
| SQL DW 的 DWU 缩放 | 池容量参数（Gen1→Gen2 SKU） | Fabric 容量（CU） |
| PolyBase 外表装载 | 专用池外部表 + Serverless 引擎谱系 | 外表/视图+查询加速 |
| Azure Data Factory（独立服务） | 工作区内嵌 Pipelines | Fabric Data Factory |
| HDInsight Spark 集群 | Spark 池（会话/专有） | Fabric Spark |
| SSIS 包 + IR | Azure-SSIS IR（同 ADF） | 存 ADF/Synapse 侧为主 |
| ADLS Gen2 存储账户 | 工作区默认文件存储 | OneLake（shortcut 桥） |
| SSAS/Power BI 嵌入 | Power BI 数据集绑定 | Fabric 语义模型 |

- 读法：左列=2021 前遗产、中列=本册正文、右列=演进节反复指向的 2026 目标端；三列同物异名是
  读任何 Synapse 旧文档时最先要做的解码动作 ⚠️。
- 表内右列仅作**术语映射**，能力等价性逐条存疑（如 CU 与 DWU 非线性可比）——引用时以各 2026
  官方页为准（演进节 ✅ URL 面）。

## 核心概念速览（中英对照）

- **Azure Synapse Analytics** — 统一分析服务：摄入+ETL+仓+湖+实时+ML 的工作区级平台 ✅ overview-what-is。
- **专用 SQL 池** — Dedicated SQL Pool：预置 MPP 数仓形态，ADS 的直接延续 ✅。
- **无服务器 SQL 池** — Serverless/On-demand SQL Pool：按需扫描湖文件的 TDS 端点，按处理量计费 ✅。
- **Spark 池** — Apache Spark Pool：原生集成 Spark 的托管计算池（06 章）✅。
- **管道** — Synapse Pipelines：ADF 血统的数据集成服务（07 章）✅。
- **Synapse Link** — 零 ETL 近实时分析桥（09 章）✅。
- **工作区** — Synapse Workspace：捆绑存储/计算/安全/监控的 ARM 资源单元（08 章）✅。
- **血统链** — APS/PDW → Azure SQL DW → Synapse →（Fabric）：专用池的产品谱系 ⚠️ 转述+✅ 文档。
- **统一≠单一** — Unified Not Monolithic：一个安全/存储边界下的多执行引擎并存，本章核心论点。
- **改名营销史** — Rebranding Wave：仓产品向多负载平台演化的同代现象（Redshift/BigQuery 同潮）⚠️。

## 最新演进与工业实践

2021→2026（URL 均 2026-10-02 验证 ✅ 200；描述 ⚠️ 转述）：

- **官方入口现状**：https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is ✅
  仍在线维护；FAQ https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-faq ✅ 与术语页
  https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-terminology ✅ 构成 2026 年读
  本册 03 章的对照基准。
- **Synapse→Fabric 官方迁移线**：专用池→Fabric data warehouse 迁移助手 ✅
  https://learn.microsoft.com/en-us/fabric/data-warehouse/migration-assistant 与逐场景文档 ✅
  https://learn.microsoft.com/en-us/fabric/data-warehouse/migration-synapse-dedicated-sql-pool-warehouse；
  2026 年新项目立项口径普遍转向 Fabric ⚠️，本书概念仍是迁移的「源端词典」。
- **Azure 托管 Databricks 的分流**：https://learn.microsoft.com/en-us/azure/databricks/introduction/ ✅
  ——Spark 深度用户在 Synapse Spark 之外的官方替代面；与 06 章形成选型对照 ⚠️。
- **认证线演化**：DP-203（Synapse 数据工程师）已于 2024 退役、由 DP-700（Fabric 数据工程）承接 ⚠️
  转述；工业实践中「Synapse 存量运维 + Fabric 增量建设」双栈人才画像成为常态 ⚠️。
- **盘上三角登记**：本册 #217（Synapse 历史与概念层）↔ #221 Fabric 教材（操作层，实链见 §3.6）
  ↔ 波内 #218/#220/#191（登记不链，见 [00](00-总览与阅读地图.md) §4）。
