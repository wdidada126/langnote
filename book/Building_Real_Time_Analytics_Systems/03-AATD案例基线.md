# 03 AATD 案例基线（Introducing AATD: Real-Time Analytics for a Pizza Delivery Shop）

> 书目 #157 第 3 章 ｜ 主题：虚构比萨外卖店 AATD 的现有架构、数据、设置与实时分析应用分类的落地演练。
> 精读重构（目录 ✅，展开 ⚠️），非原书文本。

## 本章任务

- 吃透全书陪跑案例 AATD 的业务与数据形态（后续 4~10 章全部围绕它增建）；
- 学会从"现有批架构"出发做实时化的**需求盘点法**：先分类应用，再选架构；
- 建立"事件从哪来"的具体感：订单、订单行、餐厅、配送状态四族事件。

## 3.1 现有架构（The Existing Architecture）

- AATD 是一家（教学用）比萨外卖电商：下单→商家备餐→骑手配送的链路公司；
- 起始态：业务跑在关系库上，分析走 T+1 批管道（⚠️ 书中既有架构图的文字重构：业务库→定时抽取→批仓库→隔天报表）；
- 痛点画像：运营要"现在卖了什么"，商家要"我的单排到哪了"，用户要"骑手还有几分钟"——三类消费者被同一张 T+1 报表卡住；
- 本册方法论：**不动业务库，旁路加事件面**——以 CDC/埋点把事实送进 Kafka，再分层服务（这个决策在 7 章展开成 CDC 专章）。

## 3.2 设置（Setup）

- ⚠️ 书中给出可克隆的示例仓库与环境（Docker Compose 起 Kafka/应用栈的具体清单未实证，不虚构端口与镜像名）；
- 跟做心智清单：本机需要 JDK+Maven/Gradle（Kafka Streams 应用）、Docker（Kafka 单节点+Pinot standalone+可选 Debezium Connect）、Python（Streamlit 前端）；
- 盘上通识替代：Docker 起 Kafka 的通用步骤可参考 [../Kafka权威指南.md](../Kafka权威指南.md) 互链与官方 quickstart（https://kafka.apache.org/quickstart/ ⚠️ 本册未逐一验链，以 200 清单里的 documentation 页为准）。
- 诚实声明：本节"设置"细节本目录不做照抄式记录——它属于会随版本腐烂最快的部分。

## 3.3 检查数据（Inspecting the Data）

- 核心事件族（目录级确认+通识重构）：
  - `order` 流：订单创建/状态变更（含 order_id、store_id、金额、时间戳）；
  - `order line` 流：订单行（product_id、数量），与 order 一对多；
  - `product` 表：商品维度（名称、价格、品类）——7 章起由 CDC 持续供给；
  - 配送/骑手位置流：10 章地理空间查询的原料（⚠️ 字段名不转述）。
- 数据形态教训：事实流（append-only 事件）与维表（有状态实体）在实时栈里命运不同——前者直接进分析表，后者要么广播缓存、要么走 upsert（9 章）；
- 与批世界的映射：这四族恰好是星型模型的"事实+维"——实时分析没有发明建模学，只是把 ETL 的节奏从"天"压到"秒"。

## 3.4 实时分析的应用（Applying Real-Time Analytics）

把 01 章分类框架钉到 AATD：

| AATD 需求 | 类别（01 §1.6） | 新鲜度诉求 | 4~10 章对应 |
|---|---|---|---|
| 全站销量实时大盘 | A 追加型聚合 | 秒~分 | 04 直查可行 |
| 按品类/门店多维切片 | A+交互点查 | 秒+高并发 | 05 转 Pinot |
| 订单商品富化报表 | C 关联富化型 | 分 | 07+08 |
| 单张订单生命周期追踪 | B 状态更新型 | 秒 | 09 upsert |
| 骑手实时位置与时效 | D 交互点查+地理 | 亚秒 | 10 |
| 面向商家/用户门户嵌入分析 | D | 秒+高 QPS | 05/06/11 |

- 分类演练的结论：AATD 同时命中四类 → **纯 Kafka Streams 直查撑不住后半张表** → 引出服务层（05 章）；
- 这是本册最有教学价值的一击：不是"Pinot 好"，而是"需求分类先行，引擎选型随后"。

## 3.5 本章小结（重构）

- 案例基线 = 需求分类表 + 事件族清单 + 不动业务库的旁路原则；
- 后续每一章都是"给这张表补一个技术答案"。

## 与其他册的关系

- "事实流 vs 维表"的流表统一处理是 [../Streaming_Systems/06-流和表.md](../Streaming_Systems/06-流和表.md) 的教科书画像；
- 星型建模的批世界对应（事实/维、粒度声明）在系列内多册有专章，本目录守"存在才链"红线不在此挂未验名链接；
- 订单事件的可靠投递与事务：[../Kafka权威指南.md](../Kafka权威指南.md)（消息不丢的幂等/事务机制）。

## 核心概念速览（中英对照）

- **案例基线** — Baseline Case Study：全书共用的渐进式架构载体（AATD）。
- **旁路事件化** — Side-car Eventization：不改业务库，先给事实建流。
- **需求分类先行** — Classification-before-Selection：按新鲜度×查询形态选引擎。
- **事实流** — Fact Stream：业务事件的 append-only 序列。
- **维表供给** — Dimension Feed：有状态实体的持续更新流。
- **订单生命周期** — Order Lifecycle：一单从创建到送达的状态事件序列。
- **一对多流拆分** — Header/Line Streams：主事件与明细事件分流的建模决策。
- **T+1 卡点** — T+1 Bottleneck：隔天报表无法满足的三类消费者。
- **可克隆示例** — Cloneable Demo：教学栈随版本腐烂、笔记只记心智清单。
- **消费者分层** — Consumer Tiers：运营/商家/用户三类读者对新鲜度的不同定价。
- **埋点** — Instrumentation/Event Publishing：应用主动发事件的来源面。
- **业务库零改动原则** — Zero-change to OLTP：实时化项目的首要风险控制。

## 最新演进与工业实践

- "外卖/履约实时追踪"已是行业标配叙事：DoorDash/Uber Eats/美团均公开过实时数据平台实践（⚠️ 转述级，未逐条抓 URL；其共性架构与本册 AATD 演化路径一致：事件总线+OLAP 服务层+嵌入式分析）。
- 教学栈迁移：书中示例基于 Kafka/Pinot 旧版本；跟进用官方 quickstart 镜像为准（Pinot ⚠️ https://docs.pinot.apache.org/getting-started 未在本册验证清单——已验证的是 https://docs.pinot.apache.org/ ✅200）。
- 需求分类法的当代变体：现代"分析型产品（analytics as a feature）"选型问卷与 01 §1.6 表同构（⚠️ 通识转述）。
- DuckDB 对位（🔧 类比，非本书引擎）：A 类需求单机可用 DuckDB 增量管道起步（实验 E2 显示 2M 事件全量重算仅 5ms，中小盘直接"暴力重算"都够快——先测再上重型栈，见 [../DuckDB_in_Action/10-大数据集性能考量.md](../DuckDB_in_Action/10-大数据集性能考量.md)）。
- 中译对应：机工版第 3 章标题《介绍AATD：比萨外卖店的实时分析》（✅ QQ 读书实抓）。
