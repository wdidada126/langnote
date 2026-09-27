# 01 · Fabric 是什么与湖中心架构（⚠️ 推定章：原书 TOC 未实抓，主题重构见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节）

本章回答官方简介第一条承诺："Discover the core Microsoft Fabric components and understand key concepts for building a robust data platform"（✅ O'Reilly 简介原文，经 Amazon 产品页实抓，访问 2026-09-27），并解释全书总纲概念 **lake-centric architecture（湖中心架构，官方简介第三条原文用词 ✅）**。

## 1.1 一句话定义与"SQL Server 之后最大数据产品"叙事

微软官方文档对 Microsoft Fabric 的定义口径：**统一 SaaS 分析平台**——
把 Power BI、Azure Data Factory、Azure Synapse Analytics、Azure Databricks 式 Spark 体验等原本分散的服务，收敛为：

- 一个产品面（fabric.microsoft.com 门户 + 工作区），
- 一套计费（容量 CU），
- 一个数据湖（OneLake）。

（⚠️ 转述；来源锚 ✅ https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview ，访问 2026-09-27，下同。）

官方简介直接引用了 "Microsoft's biggest data product in history after SQL Server" 的媒体比喻（✅ 简介原文）。
这句话同时暴露了本书体裁：**面向被"选择过载"困扰的平台决策者**，不是面向内核工程师——
简介原话还点名 "The myriad of choices within Fabric can be overwhelming, with multiple ways to tackle tasks, not all of which are equally efficient"（✅），
"选型地图"正是全书的隐含目录。

## 1.2 SaaS 化：Fabric 与 Azure PaaS 数据服务的三个断裂点

⚠️ 转述 + ✅ 文档取证，三点差异均可在 Learn 页复核（访问 2026-09-27）：

1. **入口从云资源变为租户**：不再"开一个 Synapse 工作区资源"，而是组织级 Fabric 租户 + 工作区（workspace）；
   容量（capacity）只是挂在 Azure 订阅上的计费锚（✅ https://learn.microsoft.com/en-us/fabric/enterprise/buy-capacity ：F SKU 经 Azure 订阅或 CSP 购买）。
2. **多对一数据模型**：一个湖（OneLake）对多个计算项——Lakehouse、Warehouse、Eventhouse 都是"挂在同一份文件上的引擎视图"
   （03/04/05 章各接一环；✅ https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview ）。
3. **权限统一层**：工作区角色横跨所有 item，取代每服务各自 IAM（⚠️ 转述，三层塔细则见 09 章 9.1）。

## 1.3 湖中心架构：全书的"同一份数据"论点

官方术语表给出 lake-centric 含义：以 OneLake 为唯一落盘真相，其余组件都是其上引擎
（✅ https://learn.microsoft.com/en-us/fabric/fundamentals/fabric-terminology ，访问 2026-09-27）。
这对应副标题 "Designing End-to-End Analytics Solutions" 的设计公理：

- 数据只存一次（copy of one），引擎按需挂载——Spark 写 Delta 文件、T-SQL 端点读同一文件、Power BI 用 Direct Lake 直读（04/05/08 章）。
- 与开放湖仓通论的关系：中立视角版见 [../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md](../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md)；
  **Fabric 的差异点是把"表格式+目录+对象存储"三件套打包成微软专有问题域**（Delta Parquet + OneLake Catalog + ABFS 命名空间），而非 Iceberg 式多方开放（⚠️ 转述，取证见 04 章）。
- 与网格理论对照：湖中心 ≠ 联邦强制搬迁（数据可以物理在别处，靠 Shortcut 指进来，03 章），
  这正是 Data Mesh"平台层"主张的产品化样本（✅ 概念对照 [../Data_Mesh/04-自助数据平台原则.md](../Data_Mesh/04-自助数据平台原则.md)）。

## 1.4 与 Azure 数据家族的边界（本书大概率绘制的"地图"）

⚠️ 推定论述 + ✅ 现状锚：微软侧仍并存 Azure SQL Database、Cosmos DB、Synapse、Databricks-on-Azure；
Fabric 的定位是"分析平台层"而非"所有数据服务"。可复核的收编证据（访问 2026-09-27）：

- Learn 把数据库镜像（Mirroring）列入 Fabric 能力面（✅ https://learn.microsoft.com/en-us/fabric/mirroring/overview ）；
- Fabric Warehouse 文档域内含 Synapse 专用 SQL 池迁移页（✅ data-warehousing 枢纽 hrefs 实抓 migration-synapse-dedicated-sql-pool 条目）；
- 判断口径：**事务系统留在 Azure DB 产品线，分析收敛进 Fabric**；与 Databricks 的关系 2025 后转向互操作（09 章 UC 线）。

## 1.5 容量经济学第一课：为什么"全家桶"是设计核心

所有工作负载共享一池 CU，按用量扣减（✅ https://learn.microsoft.com/en-us/fabric/enterprise/buy-capacity 与
https://learn.microsoft.com/en-us/fabric/enterprise/scale-capacity ，访问 2026-09-27；"F64 需要 64 个可用 CU 配额"为该页原文示例）。
⚠️ 转述其后果：

- 优点：Spark、T-SQL、KQL、报表在同一账单下无跨服务出口费；治理对象从 N 个资源缩为 1 个容量。
- 代价：**邻居噪音**——批处理高峰可以吃掉报表交互延迟，必须靠工作区/容量分池与时间窗治理（挂 10 章运营、09 章 9.5）。
- 对比云仓分计价：BigQuery 按槽/扫描、Snowflake 按 credit（对照 [../Google_BigQuery_TDG/00-总览与阅读地图.md](../Google_BigQuery_TDG/00-总览与阅读地图.md)、[../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md)）；
  本书"统一容量降低认知成本"的立场应视为**厂商叙事** ⚠️。

## 1.6 端到端方案的"五件套"心智模型（本章骨架）

以官方枢纽页可枚举为证（✅ 各页 200 实测，2026-09-27）：

```
存 OneLake → 集 Data Factory（Dataflow/Pipelines/Mirroring）
           → 算 Lakehouse-Spark / Warehouse-T-SQL
           → 流 Real-Time Intelligence（Eventhouse/Eventstream）
           → 析 语义模型/Direct Lake/Power BI + Copilot
```

章文件 03–08 即按此链展开；每环一个"接缝"，接缝清单见 02 章 2.5。

## 1.7 常见误解速查（⚠️ 教学重构）

| 误解 | 校正 | 依据章 |
|---|---|---|
| Fabric=云版 SSMS 管 SQL Server | 它是租户级分析平台，仓只是六面之一 | 02/05 |
| 用 Fabric 必须先退掉 Synapse | 迁移是渐进剧本，文档给双轨工具 | 10.4 |
| OneLake 是个大桶 | 逻辑单树+物理分域+权限三面账 | 03 |
| 有 Fabric 就不需要数仓方法论 | 分层与口径纪律照旧（Inmon 没死） | 05/10 |
| Copilot 能替治理 | AI 上限≈语义模型质量 | 08/09 |

## 1.8 读者画像与前置（⚠️ 推定）

官方简介暗示三类读者：被选型困扰的数据负责人、从 Power BI 上行的分析师、从 Synapse/ADF 平移的工程师。
前置知识与盘上分册分工：

- SQL 基础与方言 → [../SQL系列·总索引.md](../SQL系列·总索引.md)；
- Spark 计算原理 → [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)；
- 数仓建模纪律 → [../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)。

## 1.9 本章反直觉收口

**Fabric 最难的不是任何单引擎，而是"太多了以至于必须做减法"**：
同一目标（比如把 SQL Server 表变报表）官方文档就给 DirectQuery、导入、Mirroring、Pipeline 复制、Shortcuts 至少五条路
（✅ 各条路文档页存在，2026-09-27 验），本书的价值主张=给出按场景裁剪的路线地图——
这正是 "Fundamentals" + "Designing End-to-End" 两个词根的组合义（⚠️ 推定全书立场）。

## 1.10 自测三题（合卷再答）

1. 说出"SaaS 化三断裂点"并各举一个你现组织里会被迫做的决策。
2. copy of one 与 Data Mesh 域主权哪里冲突、哪里和解？（提示：Shortcut）
3. 为什么邻居噪音在实时报表面比批管道面更致命？（提示：CU 共享+延迟 SLA 感知）

## 核心概念速览（中英对照）

- **SaaS 分析平台** — SaaS analytics platform：以租户为单位、免资源编排的整体分析产品，Fabric 之根本形态。
- **湖中心架构** — Lake-centric architecture：OneLake 为唯一真相存储、多引擎挂读的设计公理。
- **工作区** — Workspace：Fabric 的权限与协作容器，item 的宿主。
- **容量** — Capacity / CU：统一计费与算力池，F SKU 挂 Azure 订阅。
- **租户** — Tenant：组织级 Microsoft Entra 边界，所有工作区/容量的最大圈。
- **item（项）** — Item：Fabric 资源单位（Lakehouse/Warehouse/Notebook/Pipeline 等）。
- **copy of one** — 单一真相副本：数据只物化一份、其余皆为视图或指针。
- **邻居噪音** — Noisy neighbor：共享 CU 池下批负载挤占交互负载的固有风险。
- **收编叙事** — Consolidation narrative：微软把 Synapse/ADF 能力迁入 Fabric 文档域的产品动作。
- **选型地图** — Trade-off map：本书体裁——多路径方案的场景化裁剪指南。

## 最新演进与工业实践

- **文档枢纽即路线图**（✅ 访问 2026-09-27）：Learn 的 Fabric 首页已把 Real-Time Hub 与 Fabric IQ 列为一级枢纽
  （https://learn.microsoft.com/en-us/fabric/real-time-hub/real-time-hub-overview 、
  https://learn.microsoft.com/en-us/fabric/iq/overview ，均实测 200），
  说明 2025–2026 重心已从"补引擎"转向"事件中枢+语义/本体层"。
- **容量口径 2026-08**（✅ buy-capacity 页标注更新日期 2026-08-27，访问 2026-09-27）：
  F SKU（Azure）+ P SKU（M365/Power BI Premium）并存、CSP 代购路径、租户级试用容量、自定义 RBAC 四动作建模。
- **认证与培训产业化**：DP-600 Fabric Analytics Engineer 课程页 ✅（https://learn.microsoft.com/en-us/training/courses/dp-600t00 ，2026-09-27 实测 200）；
  本书配套电子书在 O'Reilly 平台（⚠️ 403 未核，见 00 第二节缺口登记）。
- **工业实践观察**：微软把 Fabric 深度捆绑进 M365 上探路径，选型讨论中常见"Power BI 存量组织顺手接收全家桶"的落地动机（⚠️ 社区共识级陈述）；
  反面视角必读 Data Mesh 的厂商中立论证 [../Data_Mesh/06-拐点与旧架构的尽头.md](../Data_Mesh/06-拐点与旧架构的尽头.md) 与开放栈册 [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。
- **对本册的启示**：2025-08 印刷版不可能覆盖 IQ/Real-Time Hub 全部现状，09/10 章演进节以 learn.microsoft.com 当日页纠偏，凡引用带访问日期。
