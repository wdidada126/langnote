# 01 Oracle 商业智能全景 — Oracle Business Intelligence（原书第 1 章，pp.3–25）

> 章题/页区间/以下全部小节题名 ✅ 来自出版社目录扫描件（Contents ix，见 [00 §4](00-总览与阅读地图.md)）。
> 小节内部论述不可获取：机制描述为 Oracle 文档与产品口径转述 ⚠️，凡本机演示一律 🔧 且**非 Oracle 行为**。
> 本书为 10gR2 时代（2007）方案书，作者团 Stackowiak/Rayman/Greenwald 均为 Oracle 内部人士，故本章的「版图」视角
> 强于「操作」视角——这是全书三篇十二章的入口章。

## 1.1 章定位：一张版图 + 两条路线（pp.3–4）

本章在 Part I「Oracle Business Intelligence Defined」里承担**定义与分类**职责：先把 BI 与事务应用
（transactional applications）放在同一张图上，再给出两条实现路线——

1. **用现成的**（1.2 节：E-Business Suite / PeopleSoft / Siebel 内建的分析件）；
2. **自建**（1.4 节：Oracle Database + OWB + BI EE/SE + Portal + 自建应用）。

⚠️ 编者归纳：这个二分法是全章骨架，也是 Part II（自研方案）与 Part III（治理与论证）的分界线；
读者若只为选型而来，读完 1.5 的组件表 + 第 4 章平台选型即可退出。

## 1.2 BI 与事务应用的关系（p.4）

- ⚠️ 转述（10g 口径）：事务应用负责**录入与流程**，BI 负责**读数与判断**；两者的耦合点在
  「同一套 Oracle Schema 里既有业务表又有分析对象」，这正是本书反复讨论的架构张力（第 3、5 章展开）。
- 目录给出的四个「应用内 BI」子件（✅ 小节题名）：
  - **Daily Business Intelligence**（p.5）：EBS 内建的日粒度分析包，随模块授权提供 ⚠️；
  - **Balanced Scorecard**（p.6）：战略指标卡（KPI + 目标 + 动作），与 1.2.2 同名件在 ch.2 深挖；
  - **Enterprise Planning and Budgeting**（p.8）：预算与规划（后来并入 Hyperion 线的口径 ⚠️）；
  - **Activity-Based Management**（p.9）：作业成本法分析，把成本按活动/资源分摊 ⚠️。
- 判读要点 ⚠️ 编者归纳：这四件是**功能型 BI**（有固定业务语义），与 ch.6 的**平台型 BI**（Discoverer /
  BI EE 这类通用工具）不同层，选型时不要拿前者去比后者的灵活性。

## 1.3 使能 BI 的 Oracle 集成组件（p.9）

目录列出四件（✅ 题名 + 页码）：**Data Hubs**（p.10）、**Business Activity Monitoring**（p.10）、
**BPEL Process Manager**（p.11）、**Enterprise Messaging Service**（p.11）。

- ⚠️ 转述：这一组的共同职责是**把散在应用里的事件与主数据汇成可分析的流**——Data Hub 提供行业化
  主题存储（客户/通信/金融等），BAM 提供事件侧的实时指标，BPEL 提供流程编排（分析结果回写流程），
  EMS 提供消息通道。
- 架构含义 ⚠️ 编者归纳：2007 年就把「集成层」当作 BI 的前置件，而不是事后 ETL，这在当时是相对
  超前的表述；它对应今天「ELT vs CDC 流式管道」的同一争论（本册 07 章 + 湖仓侧对位）。
- 🔧 概念类比（非 Oracle 行为）：用 SQLite 触发器把 20 万行写入镜像到变更表，实测 0.19–0.20s →
  0.68–0.72s（**+254%**，见 00 §9 E5）。这组数字说明「事件捕获」不是免费的：BAM/CDC 类组件的
  开销在写入侧，规划窗口时必须算进去。

## 1.4 定制数据仓库方案（p.12）

本节是 Part II 的预告，目录给出 8 个组件位（✅ 题名 + 页码）：

| 组件（✅） | 页 | 一句话职责（⚠️ 转述） | 本册深挖章 |
| --- | --- | --- | --- |
| The Role of the Oracle Database | 14 | 数据库本身就是仓库平台：分区/物化视图/并行/位图索引 | 05、09 |
| Oracle Warehouse Builder | 15 | 装载与元数据的图形化 ETL 工作台 | 07 |
| Oracle Business Intelligence Standard Edition | 16 | 授权受限的入门 BI 套件（Discoverer 等） | 06 |
| Oracle Business Intelligence Enterprise Edition | 18 | 企业级 BI 平台（分析/仪表盘/.dis 语义层） | 06 |
| BI (XML) Publisher | 20 | 模板驱动的高保真报表与分发 | 06 |
| Oracle Portal | 20 | 门户与 portlet 承载分析内容 | 06、08 |
| Spreadsheet Add-ins | 21 | 把 Excel/Hyperion Smart View 类前端接到仓库 | 06 |
| Building Custom Business Intelligence Applications | 23 | 用 JDeveloper/BI Beans 把分析嵌进应用 | 06 |

- ⚠️ 编者归纳：这张表的价值在于**同一厂商栈内的重叠授权面**——BI SE 与 BI EE、Discoverer 与 BI EE、
  Portal 与自建应用，两两之间都有替代关系。书中把「先定业务需求再选组件」写进 Part III，正是为了
  对抗「按组件清单买齐」的采购惯性（对照 11 章的六种坏部署症状）。

## 1.5 新兴趋势（p.24）

- ⚠️ 转述（2007 视角）：目录以 Emerging Trends 收尾，当年口径落在「分析进入流程、实时化、
  与门户/办公前端融合」这类方向上。
- 本册评注 ⚠️ 编者归纳：2026 年回看，这一节最准的预测是「BI 与流程耦合」，最不准的是「自建仓库
  仍是默认路线」——云数仓与托管 BI 把成本结构换掉了（各章末「最新演进」节逐条对位）。
- 「趋势」一节的读法 ⚠️ 编者归纳：把 p.24 的方向句当作**当时技术约束下的外推**而非预言清单——
  凡「实时化/融合化」类表述，先问它依赖的采集、消息与授权前提在 2026 是否仍成立，再决定继承度。
- 与本章组件表的关系：1.5 的趋势全部落在 1.3/1.4 已有组件上，说明作者的判断是
  **演化而非替代**——版图内没有新增物种，只有老物种换食性 ⚠️ 编者归纳。

## 1.6 与 repo 其他书的联系

- 导游册浅层：[../Oracle_Essentials_5e/09-高可用集群与Oracle产品版图.md](../Oracle_Essentials_5e/09-高可用集群与Oracle产品版图.md)
  （⚠️ 其章为题重构章，证据等级低于本册）与 [../Oracle_Essentials_5e/07-数据仓库基础与体系结构.md](../Oracle_Essentials_5e/07-数据仓库基础与体系结构.md)。
- 方法论对照：[../Building_the_Data_Warehouse/01-决策支持系统的演化.md](../Building_the_Data_Warehouse/01-决策支持系统的演化.md)
  （Inmon 的 DSS 演化叙事）与 [../数据仓库工具箱.md](../数据仓库工具箱.md)（Kimball 维度生命周期，与本册 10 章最近）。
- 治理线：[../Understanding_Data_Governance/00-总览与阅读地图.md](../Understanding_Data_Governance/00-总览与阅读地图.md)。
- 波内兄弟 #142/#143/#145/#168/#205/#206：**只登记不链**（见 [00 §8](00-总览与阅读地图.md)）。
- 名册 #204（Heaton，Packt 2012 BI 食谱）：同域不同书，三叉辨析见 [00 §5](00-总览与阅读地图.md)，挂点在本章
  1.4 的组件表（#204 的 recipe 多落在 BI EE/OWB 两行）。
- 理论根基：[../../db/db.md](../../db/db.md)；总索引：[../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 核心概念速览（中英对照）

- **应用内 BI** — Embedded/Transactional BI：随业务模块授权交付的分析件（DBI/记分卡/EPBF/ABM），语义固定 ⚠️。
- **功能型 vs 平台型 BI** — Functional vs Platform BI：前者给结论，后者给做结论的工具（1.2 与 1.4 的分层）⚠️ 编者归纳。
- **Data Hub** — 数据中枢：行业化主题存储，把应用主数据与事件汇成可分析层 ⚠️。
- **BAM** — Business Activity Monitoring：事件流上的实时指标与告警 ⚠️。
- **BPEL Process Manager** — 流程编排：让分析结论回写业务流程的引擎 ⚠️。
- **EMS** — Enterprise Messaging Service：消息通道，BI 事件传输底座 ⚠️。
- **OWB** — Oracle Warehouse Builder：图形化 ETL 与仓库元数据工作台（10g/11g 时代）⚠️。
- **BI SE / BI EE** — 标准版/企业版 BI：同一栈内两档授权，功能重叠需按需求裁剪 ⚠️。
- **BI (XML) Publisher** — 模板驱动高保真报表与分发 ⚠️。
- **Spreadsheet Add-ins** — 表格插件前端：把仓库指标接入 Excel 类客户端 ⚠️。
- **自建 BI 应用** — Custom BI Applications：用 JDeveloper/BI Beans 把分析嵌进自有应用 ⚠️。
- **组件重叠税** — Overlap Tax（⚠️ 编者归纳）：同厂商多组件互为替代，选型必须先业务后组件。

## 最新演进与工业实践

2007（10gR2）→ 2026 对位（⚠️ 转述 + ✅ URL，逐条状态见下）：

- **应用内 BI**：DBI/Balanced Scorecard/ABM 作为独立产品已退场，其位置由 **Oracle Fusion Analytics
  Warehouse（FAW）** 与行业数据模型承接——预置主题 + 预置管道，理念与本章 1.2 同构 ⚠️
  （✅ https://www.oracle.com/analytics/ ；FAW 文档为登录态路径，`/en/cloud/saas/fusion-analytics/` 404 已登记）。
- **集成组件**：Data Hub/BAM/EMS 谱系并入 **OCI Streaming / OCI Data Integration / GoldenGate（Veridata）**；
  BPEL 线仍在 **Oracle Integration / SOA Suite**（✅ https://docs.oracle.com/cd/E11882_01/index.htm 为归档入口）⚠️。
- **OWB**：官方停止特性演进，路线指向 **ODI → OCI Data Integration / FDI（Fuse Development Insights）** ⚠️
  （本册 07 章展开；ODI 精确版本文档链接 404 已登记，不编 URL）。
- **BI SE/EE → OAC**：BI EE 的后继为 **Oracle Analytics Cloud / Oracle Analytics Server**，语义层由
  `.dis` 迁移到 OAC 数据模型与目录 ⚠️（✅ https://www.oracle.com/analytics/）。
- **XML Publisher → BI Publisher（Fusion Middleware 内）**：模板报表仍是企业打印/发票场景主力 ⚠️。
- **自建 BI 应用**：JDeveloper BI Beans 退场，改由 **REST API + OAC 可视化嵌入 + 前端框架**承担 ⚠️。
- **数据库即仓库平台**：这条 2007 判断在 2026 更强——**Autonomous Data Warehouse** 把分区/物化视图/并行/
  In-Memory 变成托管默认项（✅ https://docs.oracle.com/en/cloud/paas/autonomous-database/ 、
  https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/ 、
  https://docs.oracle.com/en/database/oracle/oracle-database/19/inmem/ ）⚠️。
- **本机教学** 🔧：E5 的 CDC 触发器开销（+254%）与 E7 的低基数索引反例（77.3ms → 85.9ms）适合在课堂上
  一次讲清「集成层不是免费」与「为什么需要位图索引」；重申 SQLite/DuckDB **非 Oracle 引擎行为**。
