# 01 · 认识 Microsoft Fabric 统一分析平台 —— Learn Microsoft Fabric（⚠️ 主题重构章）

> **降级声明**：原书目录未获任何渠道实证（取证负结果台账见 [00 · 总览与阅读地图](00-总览与阅读地图.md) §2），
> 本章为主题重构章：章题语义 = 「Learn X」式教学书的标准开篇位 + Fabric 官方文档信息架构第一层
> （✅ 枢纽 URL 均于 2026-10-02 以 `curl -I` 验 200，登记于 00 §5）。本章所有 Fabric 机制描述为官方
> 文档转述 ⚠️，绝不冒充原书正文；与盘上 O'Reilly 册 Fundamentals of Microsoft Fabric 的谱系辨析见
> [00 §3](00-总览与阅读地图.md)——**两册是不同出版社的不同书，引用勿混**。

## 1. 本章在学习路径中的位置

- 「Learn」系书的第一章惯例：不写代码、先立坐标系——回答四个问题：Fabric 是什么、为谁而造、
  解决了什么旧痛点、学完能做什么（⚠️ 推定本章覆盖面）。
- 对位兄弟册：[../Fundamentals_of_Microsoft_Fabric/01-Fabric是什么与湖中心架构.md](../Fundamentals_of_Microsoft_Fabric/01-Fabric是什么与湖中心架构.md)
  走「湖中心架构理念」切入；本册重构章按 Packt 教学体裁更偏「产品面 + 上手面」（⚠️ 推定）。

## 2. 核心叙事：分析平台的一体化收敛（⚠️ 转述 + ✅ 枢纽）

- Fabric 是微软的**分析 SaaS 总集**：把 Power BI（BI）、Azure Data Factory 血统的数据集成、
  Azure Synapse 血统的数据工程/数仓/ML、以及新造的实时分析栈收敛进**同一租户、同一数据湖、
  同一治理面**（⚠️ 转述；✅ <https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview>，2026-10-02 验 200）。
- 三个「统一」是理解一切的锚：
  1. **统一存储**：OneLake——租户级唯一逻辑数据湖，所有 item 的数据落同一命名空间（详见 [03 章](03-OneLake统一数据湖与快捷方式.md)）；
  2. **统一身份**：Entra ID + workspace/item 角色，一处授权处处生效（详见 [11 章](11-治理安全与租户管理.md)）；
  3. **统一计费**：容量（Capacity Units）池化付费，跨工作负载共享（详见 [02 章](02-许可容量与租户开通.md)）。
- SaaS 化是关键卖点：无需手工绑订阅、建存储账户、拼服务矩阵——门户开租户即可用（⚠️ 转述；
  ✅ <https://learn.microsoft.com/en-us/fabric/>）。
- 与 Azure 分析服务的关系（波内登记见 00 §4）：Synapse 系用户是官方点名的迁移人群；
  Fabric 不替代 Azure SQL/ Cosmos 等**事务型**数据库，只收敛**分析型**工作负载（⚠️ 转述）。

## 3. 工作负载家族速览（⚠️ 转述，章文件逐章展开）

| 工作负载 | 代表 item | 主要人群 | 本册章位 |
|---|---|---|---|
| Data Factory | 管道、数据流 Gen2、镜像 | 集成工程师 | [06](06-数据集成三岔路.md) |
| Data Engineering | Lakehouse、笔记本 | 数据工程师 | [04](04-Lakehouse与数据工程.md)/[08](08-Notebooks与Spark工作负载.md) |
| Data Warehouse | 仓库、SQL 数据库 | SQL 分析师 | [05](05-Warehouse数仓与SQL端点.md) |
| Data Science | 试验、模型 | ML 工程师 | [09](09-数据科学与机器学习.md) |
| Real-Time Intelligence | Eventhouse、事件流 | 实时分析者 | [07](07-实时智能与Eventhouse.md) |
| Power BI | 语义模型、报表 | BI 分析师 | [10](10-PowerBI语义模型与DirectLake.md) |

- 记忆法：**「存（OneLake）→ 进（集成）→ 算（工程/仓/实时）→ 用（BI/ML）」**四段，本册章序即按此排布。

## 4. 对象模型：租户 → 工作区 → 项（item）

- **租户（tenant）** = 组织的 Fabric 边界；**工作区（workspace）** = 项目组容器（借鉴 Power BI 概念）；
  **项（item）** = 一类工作负载的实体（表、笔记本、管道……各有专属图标与生命周期）（⚠️ 转述）。
- 「Shortcut 路径、报表嵌入、笔记本运行」等一切操作都发生在 item 粒度——这决定了权限、
  血缘、计费的观测粒度（⚠️ 推定延伸，与 11 章血缘节呼应）。
- 与姊妹概念辨析：item ≠ Azure 资源；Fabric 对象不走 ARM 模板部署（Git 集成与部署管道另述，见 12 章）（⚠️ 转述）。

## 5. 学习路径与认证对位（✅ 枢纽）

- 官方入口：Learn 平台的 Get started with Microsoft Fabric 学习路径（✅ <https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview>，2026-10-02 验 200）。
- 认证对位：DP-600（Fabric Analytics Engineer Associate）是本书体裁最匹配的考试；本册 12 章按
  「端到端项目 + 认证地图」收束（⚠️ 推定本书有此收尾章，DP-600 存在本身为 ✅ 公开事实）。
- 前置人群画像（⚠️ 推定）：SQL 分析师 / Power BI 报表开发者 / 传统 ETL 工程师转湖仓——三类人
  各取章：SQL 背景 → 05+06；PBI 背景 → 10+03；ETL 背景 → 06+07。

## 6. 常见误区（重构章的工程化提醒）

- 误区一：「Fabric = 换了皮的 Synapse」——错，Synapse 是 PaaS 服务拼装，Fabric 是 SaaS 收敛 +
  OneLake 底座，计费与治理模型都不同（⚠️ 转述）。
- 误区二：「OneLake 是新的存储产品，要把数据搬进去」——OneLake 是**逻辑统一层**，快捷方式与
  镜像让数据可以留在原处（🔧 类比见 03 章，零拷贝指针实测）。
- 误区三：「买了容量所有 item 自动高性能」——容量是共享池，item 级并发与缓存策略仍需设计
  （🔧 E6 并行弹性类比见 08 章；⚠️ 转述）。
- 误区四：把 **Data Fabric（架构风格）**当 Microsoft Fabric（产品）——盘上另有四册 Data Fabric
  理论书，对位辨析见 [../Data_Fabric_Architectures/00-总览与阅读地图.md](../Data_Fabric_Architectures/00-总览与阅读地图.md)（写前已验名）。

## 7. 本章在盘上目录版中的对位

- 概念纵深：湖仓通论见 [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)；
  「数据湖→湖仓」演化史见 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)。
- 厂商对照：Snowflake/Redshift/BigQuery 三云仓册的「平台总览」章可与本章互为镜像（登记于 00 §6）。
- 数仓方法论祖谱：传统自下而上/星型建模语境下的「平台是什么」完全不同——对照
  [../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md) 阅读可避免
  用「维度建模时代」的假设误读 Fabric 的表与物化视图策略（⚠️ 推定提醒）。
- 系列索引：[../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 8. 术语首次出现对照（读后续章的字典位）

| 首次出现 | 英文原名 | 本章段落 | 展开章 |
|---|---|---|---|
| 湖仓 | lakehouse | §2 | 04 |
| 单一数据湖 | OneLake | §2 | 03 |
| 快捷方式 | shortcut | §2 | 03 |
| 镜像 | mirroring / zero-ETP 风格复制 | §2 | 06 |
| 容量 | capacity | §2 | 02 |
| 语义模型 | semantic model | §3 | 10 |
| Eventhouse | eventhouse | §3 | 07 |
| 数据流 Gen2 | dataflow Gen2 | §3 | 06 |
| 管道 | pipeline | §3 | 06 |
| 试验 | experiment（ML） | §3 | 09 |

- 读法建议：本表按「章 1 遇到即查、到章再精读」使用；每个术语在 00 §7 阅读地图中另有跨章索引。
- 注：英文列均为产品面通用词（✅ 可在 00 §5 已验 200 的官方枢纽页中逐词核对），中文列为本目录译法，
  非官方定译（⚠️ 声明）。

## 9. 章末自测（重构题，⚠️ 非原书习题）

1. 说出 Fabric「三个统一」并解释各自降低的旧成本（§2）。
2. 一个租户内，工作区与容量是什么映射关系？给出一种生产/探索隔离方案（§4、02 章 §3）。
3. 为什么 OneLake 不需要你先「搬迁」数据？两个机制名是什么（§6，答：快捷方式与镜像）。
4. Data Fabric 与 Microsoft Fabric 的范畴差别？（§6 第四条 + 盘上 Data Fabric 四册登记）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 统一分析平台 | unified analytics SaaS | 多工作负载收敛于同一租户/存储/计费面 |
| 租户 | tenant | 组织的 Fabric 顶层边界（绑 Entra ID） |
| 工作区 | workspace | 项目组容器，权限与血缘的中间粒度 |
| 项 | item | 工作负载实体（表/笔记本/管道/报表…） |
| 快捷方式 | shortcut | OneLake 零拷贝逻辑指针（03 章展开） |
| 容量 | capacity / CU | 跨工作负载共享的计算计费池（02 章展开） |
| 镜像 | mirroring | 外部库零 ETL 复制入湖（06 章展开） |
| 工作负载 | workload | Data Factory/Engineering/Warehouse/Science/RTI/Power BI 六族 |

## 最新演进与工业实践

- 官方更新面：Fabric 月更节奏（Feature Summary 博客 + What's new 文档页，✅ 本页
  <https://learn.microsoft.com/en-us/fabric/get-started/whats-new>，2026-10-02 验 200）——学习
  任何「预览」标注的功能前先查当日页，本册所有快照日为 2026-10-02（⚠️ 纪律性提醒）。
- 平台演化叙事（⚠️ 社区通识转述，未逐条实证）：2023-05 Ignite 发布 → 2023 下半年至 2024 各工作
  负载渐次 GA → 2025 起补实时与 AI 面（Copilot 类功能、目录治理深化）→ 2026 文档域已两轮重组
  （旧链成片失效，波 5 册 00 §7 的 404 清单是化石证据）。
- 工业实践：评估顺序建议「先治理面后性能面」——租户设置、容量分区（F SKU）与权限模型是采购
  决策的三个真成本项（⚠️ 转述）；面试口径（DP-600 向）：能画「OneLake 居中、六负载环绕」的图
  并解释 item 与 workspace 关系是第一道门槛题（⚠️ 推定）。
