# 01 从 Azure 数据工厂到 Fabric 数据工厂 — ADF to Fabric Data Factory（⚠️ 重构章，非原书 TOC）

> 本章为「谱系章」：全书一切讨论的地基。章题为 ⚠️ 推定重构（依据见 00 §2）；机制 =
> learn.microsoft.com 官方文档转述 ⚠️ + ✅ URL（2026-10-01 `curl -sI` 200 验真）；
> Fabric 平台本机不可实测，概念类比仅见 🔧 标注处（非 Fabric 平台行为）。

## 1.1 为什么先讲谱系（Playbook 的第 0 页剧本）

- 本书副题（✅ 封面 OCR）承诺的是「Design, orchestrate, and scale reliable data pipelines」——
  而 Fabric Data Factory（下称 FDF）的管道语法几乎逐词继承自 Azure Data Factory（ADF），
  不补 ADF 前史就无法理解 FDF 文档里大量「与 ADF 相比…」的省略句 ⚠️。
- 作者谱系一手证据 ✅：本书作者 Mark Kromer（Packt 封面署名）2022 年在 Apress 出版
  《Introduction to Azure Data Factory》（Crossref 实抓：ISBN 9781484286111/9781484286128，
  Apress，2022，作者姓寄存 Kromer）——同一作者把笔从 ADF 换到 FDF，本身就是产品迁移
  方向的行业信号 ⚠️ 编者评述。
- 阅读姿势建议：把本章当「词汇表」，02–11 章当「剧本库」；遇到任何 FDF 概念先问
  「它在 ADF 里叫什么」，答案决定你查哪套文档。

## 1.2 ADF 是什么（前身定位，⚠️ 转述）

权威页：`https://learn.microsoft.com/en-us/azure/data-factory/introduction` ✅ A1。要点 ⚠️：

- ADF = 微软云 ETL/ELT **编排服务**：管道（pipeline）+ 活动（activity）+ 连接器
  （connectors，400+ 口径以现行页为准）+ 集成运行时（Integration Runtime, IR）执行层。
- IR 是 ADF 的灵魂也是负担：Azure IR / Self-hosted IR / Azure-SSIS IR 三形态，用户要自己
  管节点、网络与扩展 ⚠️。
- 装载面：Copy Activity（✅ A2 copy-activity-overview）+ Mapping Data Flows / Wrangling Data
  Flows（✅ A4 wrangling-data-flow-overview）；控制流活动全家桶（✅ A3
  control-flow-execute-pipeline-activity 为其文档组织示例）。
- ADF 属 PaaS：按活动执行/核时计费，工作区概念弱，Git 集成走 ARM 模板/协作分支。

## 1.3 FDF 是什么（SaaS 化重定位，⚠️ 转述）

权威页：`https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-overview` ✅ F1、
`https://learn.microsoft.com/en-us/fabric/data-factory/compare-fabric-data-factory-and-azure-data-factory` ✅ F2。
要点 ⚠️（以 compare 页现行版为准）：

- FDF 把 ADF 的管道/活动/连接器/Copy 语义搬进 Fabric 工作区，成为一等 **item**（与
  Lakehouse/Notebook/Warehouse 同列），不再需要独立数据工厂资源。
- **执行层 serverless 化**：自助管理 IR 的运维面基本消失（自托管源接入形态以现行文档为准 ⚠️），
  算力从「核时」改记 **Fabric 容量单元 CU**。
- **存储归一**：数据默认在 OneLake（✅ 06 章 O1），湖仓/事件湖与管道同命名空间。
- **能力裁剪**：ADF 的 SSIS IR、映射数据流等能力在 FDF 的支持面与 ADF 不同——逐项差异
  只认 F2 compare 页现行表 ⚠️，本册不抄死（成书后口径漂移是这类对比页的常态）。
- **新增面**：Copilot 辅助管道创作（✅ F9 copilot-fabric-data-factory）、事件驱动编排与
  Fabric 告警生态（09 章）、Git 集成 + 部署管线（08 章 C1/C2/C3）。

## 1.4 差异速查表（⚠️ 编者按官方对比框架整理，引用请以 F2 现行页复核）

| 维度 | ADF（✅ A1–A4） | FDF（✅ F1/F2） | 迁移含义 |
| --- | --- | --- | --- |
| 资源形态 | 独立 Data Factory 资源（PaaS） | Fabric 工作区 item（SaaS） | 治理/权限并入角色体系 |
| 执行层 | IR 三形态自管 | serverless + CU 计量 | 省运维、换账单 |
| 存储 | ADLS/Blob 等外挂 | OneLake 原生 | 落地即湖仓（06 章） |
| SSIS | Azure-SSIS IR 原生托管 | 支持面收窄 ⚠️ | 包需重平台化（11 章） |
| 数据流 | Mapping DF + Wrangling DF | 支持面不同 ⚠️（F2 为准） | 04 章边界讨论 |
| CI/CD | 协作分支 + ARM 模板 | Git 集成 + 部署管线（✅ C1–C3） | 08 章剧本 |
| 监控 | ADF Monitor | 管道运行监视 + Fabric 告警（✅ F4） | 09 章剧本 |
| 前身关系 | —— | 「reimagined ADF」定位 ⚠️ | 语法同源、运维异源 |

## 1.5 三条产品承载史：ADF / Synapse Pipeline / FDF（波内登记 ⚠️）

- 同一套管道语法在微软分析栈有**三种承载**：ADF（独立 PaaS）、Synapse Pipeline（内嵌
  Synapse Studio）、FDF（内嵌 Fabric）。Synapse 双册 #217/#219 为本波兄弟，**只登记不链**
  （写检日盘上无目录）；挂点：本章 1.4 表与 11 章迁移决策树。
- 趋势判读 ⚠️ 编者评述：官方把迁移叙事从「ADF→Synapse」改口为「ADF→Fabric」（✅ F10
  migrate-planning-azure-data-factory 标题即证），FDF 是微软数据集成编排的**当前主推承载**；
  学习投资排序建议：FDF 语法 > ADF 特有运维（IR/SSIS）> Synapse 专属面。

## 1.6 「Playbook」体裁与本章的用法

- Playbook ≠ 教程：预设读者要产出**可复用的剧本**（pattern），而非跟做一次性 demo ⚠️ 编者读法。
- 本章产出的三个可带走判断：①看到管道 JSON 先认 ADF 血统（活动名基本同名）；②成本问题
  一律换算到 CU 语言（10 章）；③「FDF 缺什么」永远查 F2 compare 现行表，不查记忆。
- 反模式警告 ⚠️：把 ADF 的 IR 排障经验直接套 FDF（无对应运维面）、把 SSIS 包原样搬进
  FDF 计划（11 章迁移剧本第 2 幕处理）。

## 1.7 与 repo 其他书的联系

- Fabric 全景前置：[../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)
  之 01「Fabric 是什么」与 06「数据集成三件套」（ls 验名 ✅）——先读它建立组件地图，
  再回本章补「集成面为什么长成这样」的历史因果。
- 湖仓平台中立理论：[../Practical_Lakehouse_Architecture/02-传统架构与现代数据平台.md](../Practical_Lakehouse_Architecture/02-传统架构与现代数据平台.md)
  的「ETL 工具演化」叙事与本章 1.2–1.3 对位（写前 ls 验名 ✅）。
- 波内登记（不链）：#218 Learn Microsoft Fabric、#191 Data Engineer's Guide to MS Fabric、
  #217/#219 Synapse 双册；建议主代理波尾 Fabric 谱系总表把本章 1.4 表作为「集成面」切片。

## 1.8 本章自测（Playbook 风格，答案均在上文 ⚠️ 编者）

1. FDF 与 ADF 的「同语法、异运维」分别指什么？（1.3：管道 JSON 族 vs IR/CU）
2. 为什么「FDF 缺什么」不许凭记忆回答？（1.6：compare 现行表纪律，✅ F2）
3. SSIS 包在迁移评估里的正确处置路径？（1.6 反模式 → 11 章第 2 幕）
4. 「三承载同族」是哪三种？学习投资排序怎么给？（1.5）
5. 作者谱系证据链的两环是什么？各自取证等级？（1.1：封面署名 ✅ + Crossref ADF 册 ✅，
   同人判定 ⚠️）
6. 把 FDF 问题翻译成 ADF 语言的第一个动作？（1.1：先问「它在 ADF 里叫什么」）

- 记忆锚一句：**「语法认 ADF、差异认对比页、账单认 CU」**——1.4 表的三行压缩版。
## 核心概念速览（中英对照）

- **Azure 数据工厂** — Azure Data Factory (ADF)：微软云 ETL 编排 PaaS，FDF 的语法前身（✅ A1）。
- **Fabric 数据工厂** — Data Factory in Microsoft Fabric：ADF 的 SaaS 化重定位，工作区一等 item（✅ F1）。
- **集成运行时** — Integration Runtime (IR)：ADF 执行层三形态，FDF 中运维面基本消失 ⚠️。
- **容量单元** — Capacity Unit (CU)：Fabric 统一计费/计量单位，替代 ADF 核时口径 ⚠️。
- **对比页现行表** — compare doc：FDF 与 ADF 能力差异的唯一权威快照（✅ F2），引用勿凭记忆。
- **三承载同族** — ADF / Synapse Pipeline / Fabric DF：同管道语法的三种产品宿主 ⚠️。
- **管道即项** — Pipeline as Item：FDF 中管道与 Lakehouse/Notebook 同列可版本化对象（✅ C2 延伸）。
- **重平台化** — Re-platforming：SSIS/映射数据流等 ADF 资产迁入 FDF 时的改造动作（11 章）。
- **作者谱系证据** — 同一作者 Apress ADF 册→Packt FDF 册：产品迁移方向的一手行业信号 ✅。

## 最新演进与工业实践

- **文档口径演进**（URL 均 ✅ 200，机制 ⚠️ 转述）：F2 compare 页与 F10/F11 迁移双页在
  2025–2026 持续更新，官方迁移叙事已完全转向 Fabric 承载；本册刻意不抄差异表细节数值，
  防止成书后漂移——工业实践中应把 F2 链接钉进管道评审模板而非截图存档。
- **DP-700 认证线** ⚠️：微软数据工程师认证（DP-700）考纲覆盖 Fabric 集成面（learn 站内搜索
  命中 study guide 页，本册未逐条验其 URL，仅登记方向），FDF 剧本与考纲的交集在 02/03/07/09 章。
- **工业实践**：存量 ADF 工厂普遍采取「新管道写 FDF、存量 ADF 缓迁」双轨策略 ⚠️ 编者综合
  F10 迁移规划页要点的评述；双轨期的关键纪律是**同一活动名两套文档同名不同版本**，
  排障时先确认资源归属再查语法。
- **本机互鉴** 🔧：本章无实验；最小心智模型留给 03 章 E1——「copy = 一条带映射的 SELECT
  导出」，DuckDB 单机即可体会（**非 Fabric 平台行为**）。
