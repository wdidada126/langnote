# 01 数据工程师的 Fabric 工作区导论 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题域重构章（00 §5 口径）：对位书名中"Guide 的第 0 页——平台心智与岗位坐标系"。
> 本章全册证据密度最高：平台结构、岗位认证、许可模型三处均有当日 200 官方页 ✅；
> "本书会怎么组织读者心智"为 ⚠️ 推定。Fabric 为云 SaaS，不可本机实测，凡行为描述均转述标注。

## 1.1 Fabric 的一句话解剖与其 SaaS 性格

✅ 转述 `https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview`（当日 200；
注意旧路径 `/fabric/get-started/...` 已 301 迁移，00 §9 清单）：Microsoft Fabric 是
**统一 SaaS 分析平台**——把数据工程、数据仓库、实时分析、数据科学、BI 等工作负载装进同一
租户、同一 OneLake 存储、同一安全/治理/许可平面。给数据工程师的三个推论（⚠️ 重构论点）：

1. **没有"装 Hadoop"这一步**：计算与存储全部平台托管，工程师的供给决策从节点/集群降级为
   item/容量两级——这是与开源自建栈（盘上正主：
   [../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md)）最根本的世界观差异。
2. **接缝即架构**：工作负载之间以"同一湖内对象"互相消费（Lakehouse 表被 Warehouse 查、
   Eventhouse 数据落湖），平台卖点是接缝免维护，风险是接缝黑盒——本册 02/03/06/07 章都在
   这些接缝上铺 ⚠️ 转述+✅ 页。
3. **SaaS 的更新节奏**：功能按月发布、文档域 2026 年大重组（✅ 00 §9 的 404 化石群实证），
   任何书（含本书）的机制描述都有保质——本册对策：结构讲原理、数字回当日页。

## 1.2 数据工程师岗位面：DP-700 的官方定义

✅ `https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/`
与其学习指南页 `/credentials/certifications/resources/study-guides/dp-700`（双 200 实抓）：
DP-700（Fabric 数据工程师助理认证）界定的岗位技能域=规划与实现数据摄取/转换、实施湖仓与
分布式计算、治理与安全运维——与本册章序（02 存→03 表→04 算→05/06 进→07 流→08 仓→09 管道→10 治）
几乎一一对应，可作为"重构章序"的独立旁证 ⚠️ 推断。数据工程工作负载官方枢纽 ✅
`/fabric/data-engineering/data-engineering-overview`（当日 200）列出该角色的对象菜单：
Lakehouse、Warehouse、Notebook、Spark job definition、Data Pipeline、Dataflow Gen2、Mirroring、
Eventstream（后四件分别在 05/06/07 章展开）。

## 1.3 平台对象词表：item、workspace、capacity、tenant

⚠️ 重构的四个名词卡（机制均 ✅ 有据：`fundamentals/create-workspaces`、`admin/capacity-settings`、
`governance/governance-compliance-overview` 等页名实抓 + 波5 #221 同款口径
[../Fundamentals_of_Microsoft_Fabric/01-Fabric是什么与湖中心架构.md](../Fundamentals_of_Microsoft_Fabric/01-Fabric是什么与湖中心架构.md)）：

| 词 | 是什么 | 工程师为什么在乎 |
|---|---|---|
| item | 最小功能对象（表/笔记本/管道…各型） | 权限、Git、监控、计费全部挂在 item 粒度 |
| workspace | item 的容器与团队边界 | 域团队制的落点；mesh 的"域"在此对齐 ⚠️ |
| capacity | 计费与限流单元（CU） | 一切性能讨论的分母（04/10 章回收） |
| tenant | 组织级根（安全/策略/目录顶层） | 治理红线设这里（10 章） |

## 1.4 许可与容量的心智模型（不抄数字）

✅ 转述 `https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview` 的许可段
与 `admin` 域页族：Fabric 按容量（CU 单位）计费，试用/开发者档存在；**具体档位价格与 CU 配额
属当日易变项**——本册一律不写（00 阅读纪律："数字回当日页"）。⚠️ 推定的本书岗位建议：
开工前先答三问——谁的容量池、超支谁被叫、探索负载如何与生产隔离——三问的治理机制在 10 章，
但**心智从第 1 章建立**。类比锚（🔧 有账面的方式理解计费）：🔧E5 中"ATTACH 57.68 ms + 物化
43.24 ms"的两段式成本结构与 Fabric "连接/计算/存储三段账"同型（⚠️ 纯结构类比，非平台行为）。

## 1.5 与家族成员划界：ADF / Synapse / Power BI

⚠️ 转述+✅ 页名支撑的谱系卡（各对象详细分工在各功能章）：

- **Azure Data Factory**：托管数据集成服务，其对象已入 Fabric 成为 Data Factory 工作负载
  （✅ `data-factory/data-factory-overview` 200）；外部 ADF 资产有官方升级路径（05 章）。
- **Azure Synapse Analytics**：上一代融合分析服务；Spark 池→Fabric Spark 的对照有专页
  （✅ `data-engineering/comparison-between-fabric-and-azure-synapse-spark` 200，4.7 节主锚）;
  波内兄弟 #217/#219 负责 Synapse 侧纵深（只登记不链）。
- **Power BI**：BI 工作负载在 Fabric 内（语义模型/Direct Lake 归 #221 通论册 08 章主场，
  本册只在 08 章选型处点到）——同产品不同岗位视角，互链不重讲 ✅。

## 1.6 一个端到端脚本（全册目录的预演）

⚠️ 重构的"如果本书有一章序，它大概长这样"演练——以官方端到端教程线为骨
（✅ `https://learn.microsoft.com/en-us/fabric/fundamentals/end-to-end-tutorials` 当日 200，
其 lakehouse 教程链含建湖→装载→转换→报表步骤；✅ `data-engineering/tutorial-*` 文件族清单实抓）：

1. 建工作区、选定容量（本章）→ 2. 建 Lakehouse、挂 Shortcut 引外部源（02/03）→
3. 笔记本/作业做bronze→silver 转换（04/09）→ 4. Pipeline 编排+增量水位（05）→
5. 事务库走 Mirroring（06）、事件走 Eventstream（07）→ 6. 聚合层落 Warehouse 或湖表 SQL 端点（08）→
7. Git 集成+部署管道+监控收尾（10）。每步的"为什么"都在对应章，本册不重复官方 step-by-step ⚠️。

## 1.7 常见误区纠偏（⚠️ 编者归纳）

1. **"Fabric=云版 DataWorks/自建栈换皮"**——错在治理面：SaaS 统一平面意味着租户级策略
   压倒工作区级自由（10 章），迁移成本主要在组织不在代码 ⚠️。
2. **"先选型后学习"**——岗位认证（1.2）与官方教程线（1.6）已经把学-选路径铺好，先用 DP-700
   技能域自检，再决定读哪本姊妹册（#221 通论/#218 入门/本册纵深）。
3. **"平台托管=不需要工程纪律"**——托管消灭的是运维体力活，medallion/契约/回滚等工程纪律
   反而更值钱（09/10 章回收）。

## 1.8 与盘上诸书的联系

- 通论锚（同产品地图位）：[../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)；
  波内登记（不链）：#218 Learn 册（入门动线）、#220 Playbook（集成食谱）、#217/#219 Synapse 双册（前世）。
- 撞名辨析：Data Fabric（编织架构模式）四册——
  [../Data_Fabric_Architectures/00-总览与阅读地图.md](../Data_Fabric_Architectures/00-总览与阅读地图.md)、
  [../Principles_of_Data_Fabric/00-总览与阅读地图.md](../Principles_of_Data_Fabric/00-总览与阅读地图.md)、
  [../Data_Fabric_and_Data_Mesh_with_AI/00-总览与阅读地图.md](../Data_Fabric_and_Data_Mesh_with_AI/00-总览与阅读地图.md)、
  [../Data_Fabric_as_Modern_Data_Architecture/00-总览与阅读地图.md](../Data_Fabric_as_Modern_Data_Architecture/00-总览与阅读地图.md)
  ——产品 ≠ 模式，词面同族易混（00 §3 已登记，本章再钉一颗钉子）。
- 岗位通识正主：[../Modern_Data_Engineering_with_Spark/01-现代数据工程导论.md](../Modern_Data_Engineering_with_Spark/01-现代数据工程导论.md)
  与 [../bigdata/Spark大数据实时计算.md](../bigdata/Spark大数据实时计算.md)（盘上单文件册：
  开源 Spark 栈岗位视角，与本册 Fabric 岗位视角是同一角色在两大栈的镜像——00 §10 数据工程纵深三角）。
- 方法论上游：[../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)、
  湖仓理论：[../Practical_Lakehouse_Architecture/01-湖仓架构简介.md](../Practical_Lakehouse_Architecture/01-湖仓架构简介.md)。

## 核心概念速览（中英对照）

- **统一 SaaS 分析平台** — Unified SaaS Analytics：租户/湖/安全/许可四平面合一 ✅。
- **接缝即架构** — Seams-as-Architecture：负载间靠同湖对象互消费，卖点与黑盒同体 ⚠️✅。
- **DP-700 技能域** — Fabric Data Engineer Associate：岗位坐标系，与本册章序互为旁证 ✅。
- **item 粒度** — Item-level Everything：权限/Git/监控/计费的统一挂载粒度 ✅⚠️。
- **容量 CU** — Capacity Units：性能与账单共同的分母；数字回当日页 ✅⚠️。
- **谱系三邻** — ADF/Synapse/Power BI：前世与同产品关系卡（1.5）✅。
- **文档保质期** — Docs Half-life：2026 重组化石群实证；机制引页、数字不抄 ✅(00 §9)。
- **端到端脚本** — End-to-end Tutorial Spine：官方教程线=全册目录预演 ✅。
- **组织迁移成本** — Org-side Migration Cost：治理面压倒技术面的迁移真相 ⚠️。
- **重构章声明** — Reconstructed Chapter：本目录全部章为 ⚠️ 主题重构（00 §5 铁律）。

## 最新演进与工业实践

2024→2026（URL 均 2026-10-02 实测 200；⚠️ 为转述/推断）：

- **岗位线扩张**：DP-700 学习指南页当日在架并持续更新（✅ study-guides/dp-700）；微软另设
  DP-600 分析工程师线（本册不展开，#221 册 08 章语境）——认证即教材目录，重构章序借此自检。
- **文档域大重组实证**：overview 主页从 get-started 迁至 fundamentals（✅ 301 实验，00 §9）；
  2024 年出版的指南类图书引用路径大面积失效——工业实践要求"引用当日重验"成纪律。
- **real-time hub 独立成域**：`/fabric/real-time-hub/real-time-hub-overview` ✅ 当日 200——
  实时接入面从特性升格为枢纽（07 章主锚）；平台边界仍在快速生长，"书后附录=功能发布清单"
  型内容一律 ⚠️ 化处理 ⚠️。
- **工业实践画像** ⚠️（通识，非本书内容）：企业导入 Fabric 的常见次序=BI 团队先行（Power BI
  存量）→ 数据工程师接湖仓 → 治理/容量后置；本书式"工程师第一课"恰在最容易被跳过的第二步，
  岗位心智（1.2/1.4）先于工具操作是本册的排序主张。
- 本册三态回顾：✅=当日实验（URL/文件清单/🔧），⚠️=转述与重构，🔧=本机类比且明示非 Fabric——
  后续各章不再重复此声明全文，只回链 00 序。
