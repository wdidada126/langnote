# 07 · 实时分析：Eventhouse 与事件流（⚠️ 推定章：原书 TOC 未实抓，主题重构见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节）

Real-Time Intelligence 是 Fabric 六工作负载里最年轻的一面
（✅ https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview ，访问 2026-09-27）。
本章：事件流 → Eventhouse/KQL → 与湖仓的联动 → 流处理谱系定位。

## 7.1 产品拼图：Eventhouse、KQL Database、Eventstream

✅（访问 2026-09-27）：

- **Eventhouse**：实时分析容器 item（https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse ）；
- **KQL Database**：其内表载体，Kusto 查询语言血统（real-time-intelligence/create-database 文档在链路上，✅ overview 页 hrefs 实抓）；
- **Eventstream**：事件接入与路由（real-time-intelligence/event-streams/overview ✅）。

⚠️ 转述谱系：这套引擎直接承袭 Azure Data Explorer/Kusto（微软日志分析平台老兵），
Fabric 将其 SaaS 化并接入统一容量——**Kusto 用户是全栈迁移成本最低的群体**。

## 7.2 Eventstream：无代码的"轻量接入与路由"位

✅ event-streams/overview + create-manage-an-eventstream（hrefs 实抓，2026-09-27）：
源支持 Event Hubs/IoT Hub 及 Fabric 平台事件（工作区 item 事件、OneLake 事件、Job 事件）——
后者是 2025→2026 的 **Real-Time Hub 扩张线**
（✅ https://learn.microsoft.com/en-us/fabric/real-time-hub/real-time-hub-overview ，访问 2026-09-27；
其 hrefs 列出的源含 Azure Cosmos DB CDC、PostgreSQL CDC、Azure SQL CDC——**事件化与镜像化的边界正在模糊** ⚠️）。

⚠️ 评审口径：Eventstream 是"路由+轻转换（UDP）"，不是流计算引擎——
开窗聚合的严肃形态不在这里；把有状态流处理需求错放进 Eventstream 是常见架构事故。
盘上严肃流处理理论：

- [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)；
- [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)；
- Flink 工程线 [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)（波 4 已在盘，写前已验名）。

## 7.3 KQL Database：为"高基数日志式数据"优化的表

⚠️ 转述 + ✅（real-time-intelligence/create-database、eventhouse 页）：
KQL 表天然面向追加写、模式灵活、全文/时序算子丰富；
与 Delta 表的差异 = **为查询热路径与半结构日志而生，不为 BI 星型与事务而生**。

🔧 类比锚（本机 DuckDB 1.5.5，非 Fabric）：
借 05 章 EXP-4 量纲自测"日志表扫描"直觉——100 万行全扫聚合列存 2.59 ms/行存 138.3 ms（2026-09-27）。
KQL 引擎在同等单机上的定位介于两者之间偏列存侧（⚠️ 无权威可比数字，仅给方向，勿引作结论）。

## 7.4 事件入湖：Real-Time Hub → OneLake 的"事件变表"路径

✅（2026-09-27）real-time-hub 文档域存在 create-streams-fabric-onelake-events 等条目（hub-overview 页 hrefs 实抓）：
平台自身事件可发布进租户事件面被订阅。
⚠️ 转述架构意图：事件与湖仓表的双向流动（事件→KQL 留存查询；事件/镜像→Delta 长周期加工）
=把"流"纳入湖中心叙事，对应官方简介第五条管理面的可观测需求（10 章运营回收）。
盘上开放对照系（流式湖仓格式）：[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。

## 7.5 Eventhouse 与消息中间件谱系的关系（读者定位表）

| 你的旧栈 | Fabric 对位 | 提醒 |
|---|---|---|
| Kafka + Flink | Eventstream +（重计算仍在外部） | Fabric 无开源 Flink 语义 ⚠️ |
| ADX/Kusto | Eventhouse/KQL DB | 直系血亲，迁移成本最低 ✅ 谱系 |
| ELK/日志栈 | KQL 生态+Copilot 辅助 | 检索模型差异需重训 ⚠️ |
| CDC→数仓 | Mirroring/Hub 事件源 | 6.4 判据（06 章）仍适用 |

消息中间件通识对位 [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)（✅ 盘上在册）。

## 7.6 延迟预算与容量共享的现实

⚠️ 转述：所有 RTI 负载同样吃容量 CU（01 章 1.5 邻居噪音在实时面最疼）；
官方未见毫秒级端到端 SLA 承诺——**用"秒级可见、分钟级新鲜"作默认预算**，压线场景要在自己租户实测。
（Fabric 不可本机实测，本段标 ⚠️；截至 2026-09-27 未锚到官方延迟 SLA 页，诚实登记缺口。）

## 7.7 本章收口：三问定实时架构

1. 是"看事件"还是"算事件"？→ KQL 看 / 外部流算；
2. 数据要进湖仓血缘吗？→ Mirroring/Hub vs 自建管道的账；
3. 留存曲线？→ KQL 热层 + Delta 冷层的两段式（⚠️ 教学重构，非原书用语）。

## 7.8 案例重构：把"告警疲劳"搬进 Eventhouse（⚠️ 教学构造，非原书案例）

背景：运维团队每天 4000 条告警，无人再看。
Fabric 侧最小方案走查（零件均已 ✅ 锚定，拓扑综合 ⚠️）：

1. 接入：现有 Event Hubs topic → Eventstream（7.2），UDP 里做降噪过滤；
2. 热层：KQL Database 留 14 天，告警聚类用时序算子（7.3）；
3. 冷层：全量经事件入湖路径落 Delta，季度复盘重算（7.4）；
4. 前台：KQL 报表 + Copilot 自然语言查询值班新人的"为什么"（8.5）；
5. 预算：全部动作吃同一池 CU——上线前先做 7.6 的邻居噪音评估。

对照 06 章判据本案例零"搬运"：告警从不进仓，只进湖——**流的归宿由消费方式决定，不由数据形态决定**。

## 7.9 自测两题（⚠️ 教学构造）

1. Eventstream 与 Mirroring 都能"进湖"，什么信号该选前者？（提示：7.2 分界句）
2. 为何把有状态开窗聚合放在 Eventstream 是事故？外部计算放哪、延迟预算谁签？（提示：7.6）

## 核心概念速览（中英对照）

- **实时智能** — Real-Time Intelligence：Fabric 事件与分析工作负载面。
- **事件屋** — Eventhouse：KQL 数据库的容器 item。
- **KQL 数据库** — KQL Database：Kusto 血统的追加写/灵活模式分析载体。
- **事件流** — Eventstream：事件接入、轻转换（UDP）与路由层。
- **实时中枢** — Real-Time Hub：事件产品统一门户，含平台事件发布订阅。
- **统一数据管线** — UDP（unified data pipeline）：Eventstream 内路由配置对象。
- **CDC 事件源** — CDC event source：数据库变更以事件形态进 Hub（✅ 2026 文档域条目）。
- **热冷两段** — Hot/cold tiering：KQL 短留存高并发 + Delta 长留存加工。
- **无流计算内核** — No open stream-processor：Fabric 不承载 Flink/Storm 语义 ⚠️。
- **平台事件** — Platform events：工作区 item/OneLake/作业自身产生的可订阅事件。
- **降噪过滤** — Noise filtering：UDP 层对告警流的白名单/聚合预处理（⚠️ 案例用语）。
- **值班新人口音** — Natural-language front door：Copilot 承接非 KQL 用户的查询通道（8.5 挂点）。

## 最新演进与工业实践

- **Real-Time Hub 升为一级文档枢纽**（✅ real-time-hub-overview 实测 200，访问 2026-09-27）：
  2025 年 GA 叙事后的 2026 结构证据；其源清单（Cosmos DB CDC、PostgreSQL CDC、Azure SQL CDC、ADLS 事件…）
  逐条在 hub 页 hrefs 可见 ✅——**"镜像 vs 事件"成为 2026 微软自家分岔**，06 章判据要按当日源清单更新。
- **工作负载开发线**（⚠️ 转述 2024 InfoWorld "workload development kit" 报道，未逐条 curl 原文，登记为方向性证据）：
  第三方应用以自定义 item 进事件生态的路径在建设中。
- **流式谱系盘上全景**：本册 07 章是"厂商产品切面"，与理论册 [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)、
  开源引擎册 [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)（均在盘验名）合读，才是 2026 完整流处理决策视野。
- **工业实践**：日志/可观测场景借 KQL+Copilot 自然语言查询是微软主打卖点
  （✅ copilot 总览页当日含实时面描述 ⚠️ 细节未逐条核）；
  数据可观测性作为独立学科与波 5 兄弟册 #226 交叉（00 第十节登记，在飞不链）。
- 复习口令（⚠️ 教学构造）：**"看用 KQL、算在外部、冷进湖、热留屋"**——实时面十六字诀。
