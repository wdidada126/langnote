# 05 数据集成三岔路：Dataflow、Pipeline 与 Copy Job — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题域重构章（00 §5 口径）：对位书名中"把数据弄进来"面——数据工程师日常占比最高的决策。
> 官方把这道选择题做成了**决策指南页**（✅ 见 5.1），本章以其为骨架重构；🔧E4 为本机类比。
> 与波内 #220（Fabric Data Factory Playbook，在飞）**只登记不链**：选型三岔路是本章主场、
> 彼册是食谱纵深（00 §8 挂点）。

## 5.1 官方决策指南：三分法与各自的物种起源

✅ 转述两条当日 200 页：

- `https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-pipeline-dataflow-spark`
  ——Pipeline vs Dataflow Gen2 vs Spark 的选型文（本章 5.2 表即其重构）。
- `https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-overview` ——Data Factory
  工作负载总览：**Azure Data Factory 的谱系落进 Fabric**，以 Dataflow Gen2 / Pipelines /
  Copy job / Mirroring（`06` 章）四件套呈现；连接器矩阵见
  `https://learn.microsoft.com/en-us/fabric/data-factory/connector-overview` ✅。

物种起源 ⚠️（谱系登记，机制各页可查）：

| 件 | 前世 | 物种 |
|---|---|---|
| Dataflow Gen2 | Power BI Dataflows（Power Query 引擎） | 低代码转换为主，可写多目标 |
| Pipeline | ADF/Synapse 管道（活动编排 DAG） | 编排+控制流，搬运交给 Copy/Mirroring/笔记本 |
| Copy job | ADF Copy 的 SaaS 化极简壳 | 纯"源→目标"批量复制，零编排 |
| Mirroring | ADF/Synapse 链接服务的实时化 | 持续近实时副本（`06` 章） |

## 5.2 三岔路选择表（⚠️ 重构自 ✅ 决策指南 + 工程师口味）

| 你的处境 | 走哪条 | 理由（✅ 页支撑） |
|---|---|---|
| SaaS/API 全对象镜像进湖，团队没有调度平台 | Pipeline + Copy job 起步 | `what-is-copy-job`：托管定时/全量或增量，界面最薄 ✅ |
| 清洗逻辑是给业务 analysts 维护的 | Dataflow Gen2 | Power Query 血缘与自治维护面（`dataflows-gen2-overview`）✅ |
| 转换逻辑重、要版本控制与代码评审 | Spark/笔记本（`04` 章） | 决策指南明列"代码优先团队"侧 ✅ |
| 已有 ADF 资产要搬家 | Pipeline 升级路径 | `how-to-upgrade-your-azure-data-factory-pipelines-to-fabric-data-factory` ✅ |
| 混合：外部源进湖+湖内转换+对外发布 | 三件接力（Pipeline 编排全程） | `pipeline-overview` 活动面 ✅ |

⚠️ 推定的本书式提醒：**别用工具数量思维选"最强"的那条**——集成层的失败模式几乎总是运维性的
（没人接手、断点不可重放、水位丢失），选型即选"谁来值守"。

## 5.3 增量刷新工程：水位线、窗口与幂等

✅ 转述 `https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh`：
Dataflow Gen2 的增量刷新以**水位列**（时间戳/自增键）定义"上次到哪"，平台管窗口重叠
（增量+近回溯窗口）；同思想在 Copy job 增量配置（`incremental-copy-job` ✅ 页名）与教程
`tutorial-setup-incremental-refresh-with-dataflows-gen2`（✅ 清单实抓）中复用。工程师的三条铁律
（⚠️ 编者归纳，机制有据）：

1. **水位列必须有索引/分区支撑**，否则"增量查询"退化为全表扫（源侧成本）。
2. **软删除到不了**：水位增量看不见 DELETE——删除语义靠 CDC/镜像补（`06` 章）或周期性全量对账。
3. **幂等写**：目标端 MERGE/主键 upsert（`03` 章装载菜单）是重放安全的前提。

## 5.4 🔧 实验 E4：水位线增量的最小模型（非 Fabric 行为）

本机 SQLite 3.45.3（脚本 `exp.py`，2026-10-02 实测）：10 万行源表+检查点表 `ck(low_watermark)`，
两刷对照——

```text
[E4] full-refresh#1 loaded rows=100000 427.78 ms; incremental#2 after 2 new source rows
     loaded=2 rows 13.16 ms (only delta moved; watermark now 2024-06-16 08:00:00)
```

- 首刷搬 100,000 行（427.78 ms）；源端新增 2 行后二刷**只搬 2 行**（13.16 ms），水位从
  2024-05 推进到 2024-06-16——"增量"的收益是行数比，不是常数。
- 边界演示（同一 run 的语义设计）：水位比较用 `>` 严格大于，同时间戳多行会被截断——生产上
  需要"重叠窗口"或复合水位（时间戳+主键），这正是 ✅ 官方页里回溯窗参数的存在理由。
- 类比缺口登记：本机无调度、无并发刷、无源端连接池——真实 Dataflow 的失败模式（半成功批次、
  重试语义）不在本模型内 ⚠️。

## 5.5 数据移动的质量闸门

⚠️ 重构观点+✅ 页名支撑：Dataflow Gen2 带数据视觉与类型推断（`dataflow-gen2-data-visuals` 在架），
Copy job 有审核列（`audit-columns-copy-job` ✅ 页名：自动加来源/时间审计列）——集成件内置
"最小元数据卫生"。接盘上的质量框架：
[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)（数据质量学科位）。审计列
+行数断言（🔧E4 的重放语义）+水位表，三件套齐了才算一条可值守的管道（⚠️ 编者语）。

## 5.6 dbt 与第三方转换层的接缝

✅ 意外之喜：官方在 data-factory 域内置 `dbt-job-overview`（当日 200）——dbt 作业可作为 Fabric
集成面板的一等对象被调度。与盘上两册的分工（已验名实链）：
[../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)、
[../Unlocking_dbt/00-总览与阅读地图.md](../Unlocking_dbt/00-总览与阅读地图.md)：
"湖内转换用 Spark/SQL 端点"与"语义层转换用 dbt"不是零和——本册立场：入湖三岔路归本章，
出湖分析层可让位 dbt ⚠️。

## 5.7 与盘上诸书的联系

- 姊妹章（平台地图位）：[../Fundamentals_of_Microsoft_Fabric/06-数据集成三件套.md](../Fundamentals_of_Microsoft_Fabric/06-数据集成三件套.md)。
- 引擎无关的管道通识：[../Modern_Data_Engineering_with_Spark/07-数据管道与结构化应用.md](../Modern_Data_Engineering_with_Spark/07-数据管道与结构化应用.md)、
  编排对照 [../Modern_Data_Engineering_with_Spark/08-Airflow工作流编排.md](../Modern_Data_Engineering_with_Spark/08-Airflow工作流编排.md)
  ——Pipeline item 之于 Fabric ≈ Airflow DAG 之于开源栈（活动/依赖/重试语义同构 ⚠️）。
- 摄取侧 SQL 手艺：[../SQL反模式.md](../SQL反模式.md)、[../SQL编程思想.md](../SQL编程思想.md)（盘上实名已验）。
- 波内登记：#220 食谱册（挂点=本章 5.2/5.3）、#218 入门册（挂点=5.1 物种表）。

## 核心概念速览（中英对照）

- **三岔路** — Pipeline/Dataflow Gen2/Copy Job：编排、低代码转换、极简复制三物种，选型即选值守人 ✅⚠️。
- **ADF 谱系** — ADF Lineage：四件套的前世；升级向导页是迁移正路 ✅。
- **水位线** — Watermark Column：增量刷新的记忆体；重叠窗口补偿时钟毛刺 ✅🔧E4。
- **回溯窗口** — Backlog/Overlap Window：官方增量参数存在的理由（防同刻截断）✅⚠️。
- **审核列** — Audit Columns：Copy job 自动来源/时间元数据，最小卫生件 ✅。
- **删除盲区** — Delete Blind Spot：水位增量看不见 DELETE，靠 CDC/镜像/对账补 ⚠️✅。
- **重放安全** — Replay Safety：目标端 MERGE 幂等是断点续传前提（03 章装载菜单）⚠️。
- **连接器矩阵** — Connector Overview：源支持面以当日页为准（版本敏感信息禁抄）✅。
- **dbt 接缝** — dbt Job in Fabric：官方在架件，湖内/湖外转换层的边界协商点 ✅。
- **升级路径** — Upgrade Pipelines：ADF→Fabric 资产搬家专页线 ✅。

## 最新演进与工业实践

2024→2026（URL/页名 2026-10-02 实测 ✅；⚠️ 为推断）：

- **Copy job 独立成物种**：`what-is-copy-job`/`create-copy-job`/`copy-job-connectors` 专页族在架 ✅
  （2024 出版时点该件尚在预览）——"零编排纯复制"被产品化为最低门槛入口，指南书的集成章因此
  从两岔变三岔 ⚠️。
- **编排面现代化**：`pipeline-run-conditions`、`how-to-debug-pipelines-in-microsoft-fabric`、
  `operations-agent-for-pipelines`（✅ 页名实抓）——条件路由、调试器与运维代理进驻，向成熟
  调度器语义补课；AI 运维代理是 2025+ 新增面 ⚠️。
- **映射数据流迁移线**：`dataflow-gen2-mapping-data-flows-transforms*` 系列页名实抓 ✅——
  ADF 映射数据流用户在 Fabric 侧获得对应物，谱系兼容策略清晰。
- **工业实践画像** ⚠️（通识）：数据代理商（Databricks/ADF 存量）迁 Fabric 的常见分层=
  Copy job 收 API/SaaS、Mirroring 收事务库、Spark 收重转换，Pipeline 总编排；与本章 5.2 表
  几乎一一对应，说明"选型文档即实践总结"。
- 本册与 #220 兄弟分工再登记：食谱册深入连接器参数与活动配方，本章止于"选路与增量语义"；
  波尾主代理闭环时以两册 00 §8 挂点为准（只登记不链红线）。
