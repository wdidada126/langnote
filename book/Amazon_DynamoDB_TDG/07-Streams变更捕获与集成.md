# 07 · Streams：变更捕获与无服务器集成（⚠️ 重构章题）

> 章定位：DynamoDB Streams 是这盘「托管 KV」与事件世界的接缝——CDC、物化视图、跨区域复制 v1 底层、审计流水都从这里走。取证锚：Streams.html ✅200（2026-09-27 实抓）；Streams.KinesisAdapter.html 302 版本跳转 ⚠️ 存目可引。

## 1. Streams 语义卡 ⚠️ 转述（✅ 主题页存目）

- 表级开关，四种视图粒度：KEYS_ONLY / NEW_IMAGE / OLD_IMAGE / NEW_AND_OLD_IMAGES——写前像/后像决定下游能算什么 diff ⚠️。
- 分区键相同的变更进入同一 stream shard ⇒ 顺序只保「同一 item」粒度 ⚠️。
- **保留窗口 24 小时** ⚠️（通识口径，未取静态页数字证）：迟到消费者丢数据须靠重放表/源重建兜底。
- 交付语义 at-least-once：消费端必须幂等 ⚠️（Lambda 事件映射的 batch 部分失败重试即在此语义下设计）。

## 2. 三种消费姿势

1. **Lambda 事件源映射**：托管轮询、按 shard 并行、批大小/出错重试/失败回收可配 ⚠️。
2. **Kinesis Data Streams 兼容适配器**（✅ 302 存目）：借 KCL 生态（增强型 fan-out、record 过期可配更久 ⚠️）解决原生 Streams 的 fan-out 与 24h 短板。
3. 自建 worker 轮询（GetShardIterator/GetRecords）：控制最细、运维最重 ⚠️。

## 3. 经典下游模式清单 ⚠️ 方法论转述

- 读模型物化：基表变更 → 写「另一套键」的投影条目（GSI 之外的第二轴，DDIA [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md) 物化视图视角）。
- 出站集成：搜索索引同步（对位盘上 Elasticsearch 册 [00](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)）、数仓落地（bigdata 目录 09 章域）、邮件/推送钩子。
- 跨区域复制 v1 的实现底座（08 章展开：v1 靠 Streams 回环复制，v2 改服务原生）。
- 审计与合规流水：OLD+NEW 双像出 diff 日志 ⚠️。
- 与 Kafka 谱系对照：Streams=「表自带的提交日志」，概念上与 CDC 工具（Debezium 类）同位 ⚠️。

## 4. 顺序与冲突：Streams 的三个坑 ⚠️

1. shard 分裂/合并引发迭代器失效——用 KCL/托管轮询而非手搓位点。
2. 同一 item 快速多次写：下游收到的「最新像」可能跳过中间态——业务需状态机幂等而非 delta 累加。
3. 跨区复制回环（v1 时代）：复制写再触发流——需哨兵属性或区域标记断环 ⚠️（08 章呼应）。

## 5. 概念类比（不算本册类比组，形状示意 🔧）

SQLite 触发器 `AFTER UPDATE ... INSERT INTO audit(old,new)` 可复现「NEW_IMAGE 视图 + 追加日志」的最小形状；与 DynamoDB 差异：触发器同步强一致、无 24h 窗口、无分片顺序契约。本册四组正式类比在 02/04/05/06 章（DDIA 通识：提交日志即「事件即数据」，[../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md) 的日志流复制模型是同一抽象）。

## 6. 与流式兄弟的谱系分工（盘上实链）

- [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)： Streams 之于 DynamoDB = 出站总线之于数据系统；该书日志/快照复制章给 Streams 定位提供理论骨架 ⚠️。
- [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)（同波/已盘按名册）——「物化读模型」的数据库化正是 Streams 下游模式的目标态。
- [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)：CDC 进湖仓的另一条路（表→changelog→lake），与「Streams→Lambda→S3」对照记账 ⚠️。

## 8. Streams vs Kafka 谱系能力对照（概念表 ⚠️ 转述）

| 维度 | DynamoDB Streams | Kafka/MSK 类 |
|---|---|---|
| 存在形态 | 表自带开关、零部署 ⚠️ | 独立集群/托管服务 |
| 分区映射 | 同 item → 同 shard（键即分片）⚠️ | topic-partition 自由路由 |
| 保留 | 固定短窗（24h ⚠️） | 按存期/容量配置 |
| 顺序契约 | 单 item 级 ⚠️ | 单 partition 级 |
| fan-out | 原生弱（适配层解 ✅ 存目） | consumer group 天生 |
| 语义 | at-least-once ⚠️ | at-least-once 默认 |
| 回放 | 过期即不可回（重放靠表本身）⚠️ | offset 重置 |
| 角色 | 表的提交日志 | 组织级事件总线 |

- 读法：Streams 是「这张数据库的 commit log」，不是「你的事件平台」——量级/保留/fan-out 任一越线就切适配层或 Kafka ⚠️。

## 9. 消费者运维剧本 ⚠️ 方法论

1. 幂等先行：以 (eventID, itemName) 去重表或条件写吞重复——at-least-once 的工程义务。
2. 部分失败：批内任一条异常=整批重投（Lambda 事件源映射语义 ⚠️）→ 把不可重试错误先落死信再抛。
3. 落后观察：shard iterator 年龄/最近处理时间差是 Streams 的 lag 替身 ⚠️。
4. 分裂应对：shard 图随基表吞吐变——消费组扩容非线性，提前按峰值配 ⚠️。
5. 回填策略：新消费者从 LATEST 起步=漏历史；TRIM_HORIZON 只剩窗口内 ⚠️——补历史走 Scan/导出（09 章管道）。
6. 断环：跨区复制类下游必须携带「来源区域哨兵」，见 §3-3 教训（v2 后此类手搓回环应退役，08 章）。

## 10. 本章自测（合卷作答）

1. 四种 stream view 各自能支撑什么下游计算？举 OLD_IMAGE 独有用例。
2. 为什么「同 item 顺序」不等于「全局顺序」？对计数器类下游意味着什么改造？
3. 24h 保留窗口如何反向决定你的重放架构？（提示：§9-5）
4. Kinesis 适配层解决了原生 Streams 哪三个短板？代价是什么 ⚠️。
5. Streams→ES 同步里，删除事件为何最容易丢？该用哪种 view 兜住？

## 11. 下游架构图（文字版）⚠️ 通式

```
基表写 → Streams(shard by PK)
   ├→ Lambda A：物化读模型（写另一键空间的投影条目，04/06 手法）
   ├→ Lambda B：出站同步（ES/S3/邮件，06 章「搜索是别人的活」）
   ├→ Lambda C：审计流水（OLD+NEW 双像 diff，09 章合规）
   └→ Kinesis 适配 → KCL 消费者组（大 fan-out/长保留，§8）
```
- 拓扑三戒律：每分支独立幂等（§9-1）；每分支自带死信（重试耗尽不阻塞 shard ⚠️）；分支间不共享状态（顺序契约只在 item 级，§4-2）。

## 12. 落地检查表（上 Streams 前过一遍 ⚠️）

- [ ] stream view 选择与下游需求对得上（KEYS_ONLY 够不够触发？）
- [ ] 消费起点策略：LATEST / TRIM_HORIZON / 时间戳，与新服务上线场景匹配
- [ ] 重放预案：24h 外丢数据如何用表本体+导出重建 ⚠️
- [ ] 死信队列（DLQ）配额与告警已配
- [ ] 消费延迟可观测（§9-3 的 lag 替身进看板）
- [ ] 跨区复制叠加时断环哨兵存在（§4-3，08 章）
- [ ] 压测覆盖 shard 分裂路径（KCL 自动扩缩验证 ⚠️）

## 13. 记忆卡补四行

- Streams 的默认假设：你会丢、会重、会迟到——幂等不是加分项是入场券 ⚠️。
- 24h 是窗口不是期限：把它当 Kafka 用的人，第一次故障就会懂 ⚠️。
- 官方最新趋势是「复制收回服务、事件留给用户」：v2 退役了回环玩法（08 章），Streams 更纯粹地回到下游集成本职 ⚠️✅。
- 视图粒度选错=下游全家的返工：KEYS_ONLY 省的钱会在 diff 需求出现那天加倍归还 ⚠️。

## 核心概念速览（中英对照）

1. **DynamoDB Streams** — 表自带变更日志：分片化 item 级事件流 ✅ 存目。
2. **视图类型** — stream view type：KEYS_ONLY/NEW_IMAGE/OLD_IMAGE/NEW_AND_OLD_IMAGES ⚠️。
3. **提交日志** — commit log：Streams 的 DDIA 抽象名（日志即事实源）。
4. **保留窗口** — 24h retention：过期即丢的消费时限 ⚠️。
5. **至少一次** — at-least-once：消费端幂等义务的来源 ⚠️。
6. **分片顺序** — shard-level ordering：同键变更的先后契约 ⚠️。
7. **事件源映射** — event source mapping：Lambda 托管消费机制 ⚠️。
8. **Kinesis 适配** — Kinesis adapter：Streams 的生态扩展接口 ⚠️（✅ 302 页存目）。
9. **读模型物化** — materialized read model：Streams 头号下游模式 ⚠️。
10. **复制回环** — replication loop：v1 跨区域时代的断环难题 ⚠️（08 章）。

## 最新演进与工业实践

- **取证（2026-09-27）**：Streams.html 200 ✅；Kinesis 适配页 302 版本化跳转（可引 ⚠️）。文档主题域十年稳定，无破坏性语义变更记录。
- **Kinesis 兼容层成熟后**，增强型 fan-out（多消费者各得完整流、独立过期窗口）是原生 Streams 短板的官方答案 ⚠️；社区「先原生、量级上来切适配」路径常见。
- **无服务器默认管道**：DynamoDB+Streams+Lambda 仍是 AWS 事件驱动教程第一形态（官方 first-time-users 资源页 ✅ aws.amazon.com/dynamodb/resources 200 佐证其叙事位）；PowerTools for Lambda（Idempotency 工具集）专门消化 at-least-once 的幂等负担 ⚠️。
- **对位本册 08 章**：Global Tables v2 用服务原生复制替代 Streams 回环——「把 CDC 从用户手里收回服务内部」的最新例证。
