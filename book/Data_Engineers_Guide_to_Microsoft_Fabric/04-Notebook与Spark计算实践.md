# 04 Notebook 与 Spark 计算实践 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题域重构章（00 §5 口径）：对位书名中"数据工程师的主力算力"面。机制事实 ✅ 来自
> learn.microsoft.com data-engineering 域当日 200 页与 fabric-docs 文件清单实抓；产品性能数字
> 一律不抄死（⚠️ 当日页为准）。本章无独立 🔧 组（算力类比复用他章：会话冷启动↔🔧E5 的
> ATTACH 首连开销形态、并行度↔E3 碎片并行读），满足全册 🔧≥4 组红线（00 §6 共 7 组）。

## 4.1 笔记本在 Fabric 里的真实身份

✅ 转述 `https://learn.microsoft.com/en-us/fabric/data-engineering/author-execute-notebook`：
Fabric 笔记本 = Synapse 式内核 + 多语言单元（PySpark/SparkSQL/Scala/KQL/T-SQL/Rich Text），
运行在**Spark 池**上；`%%pyspark`、`%%spark` magic 与 `df.display()` 类工具面在
`notebook-utilities`、`spark-utilities` 等专页（✅ 文件名清单实抓）。要点三条（⚠️ 重构强调）：

1. 笔记本是**开发面**，不是生产面的默认形态——生产化路径是作业定义与环境（4.4 节）。
2. 单元语言混排使"探查→验证→编排"能在一个文件里完成，这是它取代部分 Airflow 开发场景的原因
   （引擎无关语境对照：[../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)）。
3. 笔记本产出注册进湖表即回到 `03` 章生命周期——计算与存储的责任分界清晰。

## 4.2 Spark 池：懒启动、可配置、被计费

✅ 转述 `https://learn.microsoft.com/en-us/fabric/data-engineering/create-custom-spark-pools` 与
`spark-compute`（当日 200）：工作区可配**自定义池**（节点尺寸/数量/自动扩缩/超时回收），
未配置时落**懒启动池**（按工作负载即时起会话 ⚠️ 概念名转述）。工程师该记住的三件事 ⚠️：

- **冷启动在池层**：会话拉起是固定成本，微批负载应调小并发、拉长批间隔来摊销（形态类比：
  🔧E5 中 ATTACH+物化的 50/43 ms 两段式——"建连接"与"干活"是两张账单）。
- **executor 规格先于代码优化**：Shuffle 大户先加节点、UDF 大户先改 pandas API（通用原则在
  [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md) 与
  [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)，⚠️ 平台数值不外推）。
- **池即配额边界**：容量 CU 在池粒度消耗与限制（`billing-capacity-management-for-spark` 在架 ✅；
  治理面回收于 10 章）。

## 4.3 运行时与库管理

✅ `python-notebook-runtime-lifecycle`、`spark-job-concurrency-and-queueing` 等专页实抓（文件名清单）：
环境（Environment item）把 `.yml` 依赖定义注入会话运行时；自定义池可预装库以避开每会话安装税
（⚠️ 推定的最佳实践方向，与"懒装库拖慢首单元"的社区共识一致）。库源面（wheel/PyPI/Conda）
`spark-pools-install-unmanaged-virtual-network` 等页名显示受控网络下装库有专章流程 ✅。

## 4.4 从"跑笔记本"到"跑作业"：生产化四步

⚠️ 重构的岗位流程（每步有 ✅ 页名对应）：

| 步 | 动作 | 官方件 |
|---|---|---|
| 1 | 参数化与触发 | `notebook-parameters-and-triggers`、`trigger-notebooks`（✅ 清单实抓） |
| 2 | 脱离笔记本形态 | `create-spark-job-definition`：以代码仓库工程组织 Spark 计算 ✅ |
| 3 | 编排挂链 | Data Pipeline 活动调笔记本/作业（`05` 章件）⚠️ |
| 4 | 观测闭环 | `spark-monitoring-overview`、`browse-spark-applications-monitoring-hub`、Spark 历史服务器 ✅ |

✅ `https://learn.microsoft.com/en-us/fabric/data-engineering/spark-monitoring-overview`：监控中心
（Monitoring Hub）汇总 Spark 作业运行、资源利用率与容量占用——"作业视角"而非"会话视角"，
与调度系统的 DAG 运行史同构（[../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)）。

## 4.5 JDBC/ODBC：把 Spark 结果端给全公司

✅ 转述 `https://learn.microsoft.com/en-us/fabric/data-engineering/spark-jdbc-driver` 与
`spark-odbc-driver`、`spark-sql-connector`：Spark 连接端点暴露 Thrift 面，BI 工具/Excel/自研服务
可直连湖表跑 Spark SQL（与 `08` 章 Warehouse 的 T-SQL 面、SQL 分析端点构成三条读路径）。
⚠️ 岗位提醒：交互式直连吃在线 CU，重查询要引导走物化/汇总表，别让"能连"变成"乱连"。

## 4.6 流式计算：与 07 章的分界线

✅ `structured-streaming-overview`、`structured-streaming-triggers-output-modes`、
`lakehouse-streaming-data`（清单实抓）：Fabric 的流处理即 Structured Streaming 语义 +
Lakehouse 增量写 + checkpoint 托管。分工建议（⚠️ 重构）：
**"数据在不在事件流里"决定归 04 还是 07**——Spark 流作业（本章）处理需要 DataFrame 全表达力
的流变换；Eventstream（`07` 章）处理"接入+轻变换+KQL 分析"的实时主干。语义学底座：
[../Streaming_Systems/02-数据处理的来龙去脉.md](../Streaming_Systems/02-数据处理的来龙去脉.md)；开放形态同款工程：
[../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)。

## 4.7 与 Synapse 的谱系接缝（波内兄弟登记位）

✅ `https://learn.microsoft.com/en-us/fabric/data-engineering/comparison-between-fabric-and-azure-synapse-spark`
（当日 200）给出两代 Spark 平台的逐项对照（池模型/目录/计费单位）。波9 兄弟 #217（Synapse 入门）/
#219（Synapse 食谱）在飞——**只登记不链**：迁移叙事（Synapse 池→Fabric 环境/作业）届时互为
前后台账，本行即挂点（00 §8）。

## 4.8 与盘上诸书的联系

- Spark 语义总源：[../Apache_Spark_2_Data_Processing/00-总览与阅读地图.md](../Apache_Spark_2_Data_Processing/00-总览与阅读地图.md)、
  [../Beginning_Apache_Spark_3/00-总览与阅读地图.md](../Beginning_Apache_Spark_3/00-总览与阅读地图.md)
  （盘上实名已验）；集群底座机制走 [../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md) 线。
- 姊妹章：[../Fundamentals_of_Microsoft_Fabric/02-核心组件与工作负载全景.md](../Fundamentals_of_Microsoft_Fabric/02-核心组件与工作负载全景.md)
  （工作负载地图位）。
- 分析工程视角的同一批计算：[../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)。
- 可观测纵深：[../Fundamentals_of_Data_Observability/00-总览与阅读地图.md](../Fundamentals_of_Data_Observability/00-总览与阅读地图.md)
  ——监控中心是平台内建件，其指标语义学在该册。

## 核心概念速览（中英对照）

- **Spark 池** — Spark Pool：会话算力容器；懒启动池 vs 自定义池的取舍=冷启动 vs 预配费 ✅。
- **环境 item** — Environment：.yml 依赖定义注入运行时，库安装的工程化出口 ✅。
- **Spark 作业定义** — Spark Job Definition：仓库形态的生产计算件，笔记本的"毕业"路径 ✅。
- **监控中心** — Monitoring Hub：Spark/Pipeline 运行观测统一入口（10 章治理回收）✅。
- **Thrift 直连** — JDBC/ODBC Endpoint：Spark SQL 对外交互面；在线 CU 消耗的主闸口 ⚠️✅。
- **冷启动摊销** — Startup Amortization：微批节奏设计的第一变量（🔧E5 两段式类比）⚠️。
- **队列与并发** — Concurrency & Queuing：池并发上限与排队语义，容量规划输入 ✅页名。
- **历史服务器** — Spark History Server：事后逐作业诊断件（✅ 清单实抓页名）⚠️。
- **流分界线** — Streaming Split（编者词）：Spark 流作业 vs Eventstream 主干，按表达力需求选边 ⚠️。
- **Synapse 谱系** — Synapse Lineage：Spark 池→Fabric 池的概念直系，兄弟册对位锚 ✅对照页。

## 最新演进与工业实践

2024→2026（URL/页名均 2026-10-02 实测或清单实抓 ✅；⚠️ 为推断）：

- **高并发与自动扩缩面成形**：`spark-job-concurrency-and-queueing`、`job-queueing-for-fabric-spark`、
  `autoscale-billing-for-spark-overview` 专页在架（✅ 清单）——Spark 计费从"会话粗账"走向
  "作业/池细账"，FinOps 侧的池右型化实践与云仓仓库右型化同构（可借
  [../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)
  的方法论迁移，⚠️ 跨平台类比）。
- **Copilot 进入笔记本**：`copilot-notebooks-*` 系列页名实抓（✅）——自然语言生成 PySpark 单元
  已是产品面；指南类书籍的"笔记本章"被迫加入 AI 协作小节 ⚠️。
- **VS Code 工作流**：`author-notebook-with-vs-code` 等页（✅）标志"仓库优先"的开发面扩张，
  与 02 章 Spark 作业定义同向——笔记本 item 不再是唯一入口。
- **工业实践画像** ⚠️（通识，非本书）：成熟租户常见配方=懒启动池做探索、按域自定义池跑生产、
  作业定义收编关键链路、监控中心接告警；四步全部有当日页支撑，属"文档可查的最佳实践骨架"。
- 本册纪律重申：Spark/Fabric 性能数字（节点数、CU 费率、超时阈值）一律不写死——2026 文档重组
  已让一批旧数字页 404（00 §9 禁引清单），引用当日重验是唯一可信姿势。
