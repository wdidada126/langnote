# 07 实时分析 Eventstream 与 Eventhouse — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题域重构章（00 §5 口径）：对位书名中"实时数据"面。机制事实 ✅ 来自 learn.microsoft.com
> real-time-intelligence / real-time-hub 域当日 200 页；KQL/引擎内核类描述统一 ⚠️ 转述。
> 🔧E6 为本机类比（非 Fabric 行为）。Real-Time Hub 于 2024→2026 间独立成域（✅ 00 §9 演进注记）。

## 7.1 实时栈的三层解剖

✅ 转述 `https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview`（当日 200）与其
导航域：Fabric 实时面 = **Eventstream（接入与路由）→ Eventhouse（存储与查询，KQL）→
Real-Time Hub（跨面分发，落湖/触发下游）** 三层。数据工程师的对象清单（✅ 域内页名清单实抓）：

| 对象 | 职责 | 关键页（✅ 当日 200） |
|---|---|---|
| Eventstream | 事件源连接、拓扑、轻转换（KQL/Spark）、目标路由 | `real-time-intelligence/get-data-eventstream` |
| Eventhouse / KQL database | 高吞吐追加型存储+KQL 查询面 | `real-time-intelligence/eventhouse` |
| KQL queryset | 表集合的逻辑查询单元 | `git-kql-queryset`（域内清单） |
| Real-Time Hub | 组织级实时资产治理与分发（含 Fabric 平台自身事件流 ⚠️） | `real-time-hub/real-time-hub-overview` |

与 `04` 章 Spark 流的分工线（⚠️ 重构）：需要窗口聚合/join 全表达力的流计算回 Spark
Structured Streaming；"接入+留存+交互探查+告警"主干走本章栈——两栈共享事件语义但不同工。

## 7.2 Eventstream：把连接器搬进事件面

✅ `get-data-eventstream` 页列出的接入形态（转述级）：事件中枢类（Event Hub、IoT 平台、
Kafka 风格源）、SaaS/应用事件（⚠️ 连接器矩阵当日页为权威）、以及 Fabric 内部事件（Real-Time
Hub 线）。工程师心智 ⚠️：Eventstream 是**声明式管道**——源、拓扑（agent/函数）、目标三段；
它把 `05` 章"批的三岔路"镜像成"流的三岔路"：直存 Eventhouse、透传落湖（OneLake 表）、再加工
（交给 Spark/笔记本）。**同一条事件流的三种归宿，对应三种成本与延迟档位** ⚠️。

## 7.3 Eventhouse 与 KQL：日志形数据的家

⚠️ 转述（机制锚 ✅ `eventhouse` 页）：KQL 数据库为**追加为主、时间分区、高压缩**的形态优化；
KQL 查询语言强于时间窗过滤、模式推断（schema inference）、采样探查。数据工程师该守的三条 ⚠️：

1. **别把它当仓库**：更新/删除语义弱（与 `08` 章 Warehouse 的分界线的实时版）。
2. **留存策略先于容量**：热/冷分层与保留期设置是 KQL DB 的 first-class 配置（🔧E6 演示其账）。
3. **落湖通道常开**：Eventhouse 的价值上限取决于"金队分析能不能在湖里拿到同一份数据"
   （✅ 域内 `database-shortcut`、OneLake 线；02 章回收）。

## 7.4 🔧 实验 E6：追加日志+留存修剪的最小模型（非 Fabric 行为）

本机 SQLite 3.45.3（脚本 `exp.py`，2026-10-02 实测）：60,000 行事件表模拟"只追加"日志，
施加留存策略（`DELETE WHERE ts < 阈值`）并做尾窗查询——

```text
[E6] events ingested=60000; retention-delete 35.89 ms -> remaining=13545;
     2-day tail-window count=3870
```

- 留存清理 60,000→13,545 行、耗时 35.89 ms：事件面的"数据重力"要靠**策略**而非存储扩容来管 ⚠️。
- 尾窗查询（时间范围谓词）天然需要分区/索引支撑，本机全表扫也仅毫秒级——量级不外推，
  结构直觉保留：时间谓词是热路径，留存是冷路径，两条路互不抢道（🔧 本机形态）。
- 类比缺口登记：真实 Eventhouse 的压缩列存、缓存层、KQL 模式推断均不在本模型；
  "留存=DELETE"只是策略语义等价物，物理上 KQL 引擎按分区整体卸载 ⚠️。

## 7.5 事件工程三问：乱序、重复、迟到

⚠️ 通识重构（引擎无关面在盘上正主）：

- **乱序**：事件时间 vs 摄入时间双列原则（KQL 与湖表都适用）；机制理论见
  [../Streaming_Systems/02-数据处理的来龙去脉.md](../Streaming_Systems/02-数据处理的来龙去脉.md)。
- **重复**：至少一次投递是常态——消费侧幂等键（05 章水位铁律 3 的流版）。
- **迟到**：水位推进策略与回溯窗口（🔧E4 演示过批侧；流侧参数化在 Spark trigger 语义，
  ✅ 页名 `structured-streaming-triggers-output-modes`，04 章件）。

## 7.6 平台事件与自治运维（Real-Time Hub 的隐藏用途）

✅ 页名实抓：`real-time-hub/fabric-events-overview`、`explore-fabric-capacity-overview-events`、
`create-streams-fabric-capacity-overview-events`——**Fabric 自身把平台事件（容量用量、作业事件）
也作为流暴露**，团队可用同一栈监控自己平台（"吃自家狗粮"面）。⚠️ 重构的工程建议：容量告警、
成本周报应作为第一组 Eventstream 用例——治理数据与业务数据同栈，10 章运维闭环的伏笔在此埋下。

## 7.7 实时面的成本与降级纪律（⚠️ 编者清单）

1. **实时是买来的 SLA，不是默认值**：Eventstream/Eventhouse 常驻计算按容量计费（1.4 纪律），
   业务方说"要实时"时先问"分钟级是否致命"——多数答案是否，退批处理（05 章增量）省一个量级 ⚠️。
2. **KQL 库不是第二数仓**：热窗查询主场，历史沉淀走"KQL→湖表导出"单向阀（✅ 域内实抓
   `onelake-shortcuts`、`materialized-view`、`data-management` 页名族支撑导出/物化路径）
   ⚠️ 方向性以当日页为准。
3. **schema 漂移预案**：上游加列默认宽容（模式推断 ✅ 机制词），删列/改型必须有契约评审——
   否则下游 KQL 查询静默空结果，比报错更难发现（🔧E6 的尾窗计数是最低防线）。
4. **降级路径先写好**：事件断流时消费者看什么（湖侧 T-1 快照）要在建流那天定，不是故障当天 ⚠️。

## 7.8 与盘上诸书的联系

- 姊妹章（BI 视角的实时）：[../Fundamentals_of_Microsoft_Fabric/07-实时分析Eventhouse与事件流.md](../Fundamentals_of_Microsoft_Fabric/07-实时分析Eventhouse与事件流.md)。
- 流语义理论正主：[../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)
  （log/位置/回溯全套）；开源事件总线对照：[../ApachePulsar原理解析与应用.md](../ApachePulsar原理解析与应用.md)
  （盘上单文件册，实名已验——Eventstream 之于 Fabric ≈ Pulsar 之于自建栈的角色对照卡）。
- 日志数据库形态对照（引擎中立）：[../从Lucene到Elasticsearch.md](../从Lucene到Elasticsearch.md)
  （盘上单文件册——KQL/ES 同属"追加+时间窗探查"形态，分词与倒排是彼方主场，本册不展开 ⚠️）。
- 实时湖仓写入侧：[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)
  （"流数据入表格式"的开放答案，与本册"落湖通道"对读）。
- 波内登记：#218（入门动线含 RTI 章）、#220（事件连接器食谱）。

## 核心概念速览（中英对照）

- **三层解剖** — Eventstream/Eventhouse/Hub：接入路由、存储查询、跨面分发各司其职 ✅。
- **声明式事件管道** — Declarative Streams：源-拓扑-目标三段；三种归宿三档成本延迟 ⚠️✅。
- **追加型存储** — Append-first Store：KQL DB 形态本质；更新删除弱是设计不是缺陷 ⚠️✅。
- **留存策略** — Retention Policy：热冷分层+保留期=事件面第一配置（🔧E6 的账面）✅。
- **KQL queryset** — Queryset：表的逻辑查询组，Git 化对象之一（✅ 域内页名）。
- **双时间列** — Event vs Ingest Time：乱序世界的第一工程习惯 ⚠️。
- **幂等键** — Idempotency Key：至少一次投递下的消费侧防线（05 章铁律流版）⚠️。
- **平台事件自监控** — Self-observability via Hub：容量/作业事件同栈消费，10 章伏笔 ✅页名实抓。
- **落湖通道** — Sink-to-OneLake：实时面与湖面的接缝，数据重力归零处 ✅⚠️。
- **Spark 分界线** — Streaming Split：全表达力计算归 04，接入探查告警主干归 07 ⚠️。

## 最新演进与工业实践

2024→2026（URL/页名均 2026-10-02 实测 ✅；⚠️ 为转述）：

- **Real-Time Hub 升格**：独立域 + `fabric-events-overview` 等专页在架（✅）——平台事件、
  组织级共享事件湖成为一等公民；2024 版叙事里这还只是 Eventstream 的"目标端" ⚠️ 时代注脚。
- **实时面的 AI 化**：域内 `multivariate-anomaly-overview`（多元异常检测）、
  `vector-database-eventhouse`（KQL DB 向量检索）等页名实抓 ✅——Eventhouse 从日志库扩张为
  "实时+AI 探查"混合面；本册立场：这些属分析工程师纵深，数据工程师知道接缝存在即可 ⚠️。
- **旧链化石**：`/fabric/real-time-intelligence/event-streams`、`/fabric/real-time-hub/overview`
  实测 404（00 §9）——现行 `get-data-eventstream`/`real-time-hub-overview`；引用重验纪律再证。
- **工业实践画像** ⚠️（通识）：事件面的成本事故多源于"留存不设防+全量热存"；先定策略后接源的
  评审动作在 🔧E6 的 35.89 ms 账面前显得直觉正确——量级是玩具，**顺序是真理**。
- 与治理接缝：事件流同样带出"数据出境/域边界"问题（10 章 Purview/网络策略回收 ✅
  `security/security-overview` 200 页）。
