# 11 — Kafka 与 Spark 结构化流（Apache Kafka and Spark Structured Streaming）

> 《Modern Data Engineering with Apache Spark》第 11 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_11` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 Spark SS-Kafka 官方集成文档主题域反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

流式管道的「进」与「出」都接上真实世界：Kafka 作为 Spark SS 的源与汇。本书架构叙事的合拢点——10 章的查询生命周期在此获得生产级消息底座；「可重放源」（10 章容错前提）由 Kafka 的分区日志兑现。mission-critical 的另一半（端到端语义）也在此章摊开。

## 2. 源侧：readStream.fromKafka 的决策点（⚠️ 按章题域重构，官方文档校核）

- **订阅模式**：`subscribe(topics)` 自动分区再均衡 vs `assign(partitions=...)` 固定分片——前者弹性、后者可预期；SS 微批语境下社区常推荐 assign 系显式控制（⚠️ 立场以文档为准）。
- **起点语义** `startingOffsets`：`earliest/latest/具体 offset JSON/per-topic 指定`——**仅在首次无 checkpoint 时生效**，恢复永远读 checkpoint 里的 offset（本页第一铁律，✅ 集成文档明载 https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html）。
- **消费参数面**：`kafka.*` 透传（group.id 语义在 SS 下的弱化——offset 提交归 Spark，⚠️ 需强调）。
- **值解析**：`from_json(value_col, schema)` + `to_json`；`key/value/topic/partition/offset/timestamp` 元数据列全家。
- **手动提交** `commitOffsetByVersion`：仅 assign 模式可用——SS 先算后交的窗口期语义（→ §5 类比）。

## 3. 汇侧：writeStream.toKafka 的形状

- Kafka sink 是「普通批写出 + 键值映射」：每微批把 DataFrame 行发成消息——**无事务聚合语义**，消息级 at-least-once；重放产生重复消息需下游幂等（🔧 与 10 章实验三同一处方）。
- `keyBy` 决定分区路由与下游顺序域：无键则轮转、有键则同键同分区——顺序保证的边界在此划定。
- 转发管道（Kafka→Kafka enrichment）是本章典型终点形态（⚠️ 推定书中给此类样例）。

## 4. 端到端语义账本（本章的「mission-critical」清单，⚠️ 重构）

| 段 | 保证 | 失效模式 |
|----|------|----------|
| Kafka 读 | Spark offset in checkpoint，重放精确续读 | checkpoint 丢= earliest 重放或 latest 丢数 |
| SS 计算 | 微批至少一次 + WAL 恢复 | 查询定义不兼容需迁移预案 |
| Kafka 写 | 消息级 at-least-once | 重启重发重复消息 |
| 下游消费 | 各自为政 | 键控幂等表/去重窗设计 |

- 结论口径（与官方一致 ⚠️ 转述）：**Spark SS + Kafka 全链没有开箱 exactly-once**，file/表格式 sink 才有；Kafka sink 场景靠「键+版本化 upsert」逼近效果——第 3/10 章幂等线在本章闭合。
- 对位：[../Kafka权威指南.md](../Kafka权威指南.md)（消费组/事务的一般语义）、✅ https://kafka.apache.org/documentation/#semantics（交付语义节，2026-10 实测 200）。

## 5. 🔧 类比·「先算后交」的窗口期（SQLite 日志模型，非 Spark 行为）

模拟 SS-Kafka 的 offset 提交窗口：处理成功但提交前崩溃，会发生什么？

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE log(k TEXT PRIMARY KEY, v INT, ver INT)")     # 下游幂等表
db.execute("CREATE TABLE ckpt(topic TEXT, part INT, off INT)")          # 类 checkpoint
def handle(recs, commit=True):
    for k, v, ver in recs:
        db.execute("""INSERT INTO log VALUES(?,?,?) ON CONFLICT(k) DO UPDATE
                      SET v=excluded.v, ver=excluded.ver WHERE log.ver < excluded.ver""", (k,v,ver))
    if commit: db.execute("INSERT OR REPLACE INTO ckpt VALUES('t',0,100)")
# 场景1 正常: 处理+提交
handle([("a",1,1)]); 
# 场景2 崩溃模拟: 处理了但不提交 checkpoint → 重启后从旧 offset 重放同一批
handle([("b",2,2)], commit=False)
handle([("b",2,2),("b",2,2)])   # 重放两次同键旧值/新值混合
print(db.execute("SELECT * FROM log ORDER BY k").fetchall())
```

- 读数：重放的消息被 `ver` 比较条件吸收（`WHERE log.ver < excluded.ver`）——**版本化 upsert 使 at-least-once 在效果上等价 exactly-once**（与实验三同构，此处叠加「提交窗口」维度）。
- 类比边界：真实 Kafka 的重放粒度是分区 offset、事务生产者另有 idempotent producer 机制；SQLite 仅演示语义组合（🔧）。

## 6. 与 repo 谱系对位

- Spark 侧 Kafka 语义权威：[../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md)。
- Kafka 作为「数据库」的视角：[../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)、[../ApachePulsar原理解析与应用.md](../ApachePulsar原理解析与应用.md)（替代消息层语境，盘上存在）。
- 中文早期同题：[../分布式实时处理系统.md](../分布式实时处理系统.md)。
- Pulsar/Kafka 选型对读时注意：本书 Kafka-only，2026 工业语境多一层「流存储与表格式合流」议题（[../Apache_Paimon_Streaming_Lakehouse/01-导论流式湖仓与Paimon的崛起.md](../Apache_Paimon_Streaming_Lakehouse/01-导论流式湖仓与Paimon的崛起.md)）。

## 7. 校读清单

- 本书样例主题/分区数怎么设？——单分区样例掩盖了再均衡/顺序讨论（hands-on 册通病，⚠️）。
- 是否演示 `startingOffsets` 与 checkpoint 的相互作用实验？——好教材的试金石。
- Kafka 版本假设（2.8/3.0 前夜）——影响 ZK 集群搭建步骤的可用性（→ 演进节）。

## 8. 「先算后交」窗口期实验设计（⚠️ 需 Kafka+Spark 环境，本目录仅给方案）

> 本机无 Kafka/Spark（波6 实证延续，本波沿用），以下为**可复制实验剧本**转述设计，执行结果一律留 ⚠️ 待补。

1. 起 3 分区主题，灌 1 万条键值 JSON；SS 查询 `assign` 固定三分区、`startingOffsets=earliest`。
2. run A：正常跑到 offset≈5000，kill driver；同 checkpointLocation 重启——验证续读 5000 而非 earliest 重放（§2 铁律实证）。
3. run B：在 sink 写出成功、offset 提交前注入崩溃（`foreachBatch` 内先写后抛）——重启后观察重复行；再给 sink 表加 `ver` 守卫列重跑，重复被吸收（🔧 §5 的集群版）。
4. run C：扩主题到 6 分区（subscribe 模式）——再均衡对进行中微批的影响记录。
5. 产出物：三种 run 的行级对账表 + 「哪一段保证断了」的语义账本回填 §4。

## 9. 本章实验卡（轻量版，⚠️ 非原书代码）

1. 单分区小主题通读：`from_json` 解值 + 元数据列全展示——信封与载荷分离的体感。
2. `latest` vs 具体 offset JSON 两种首启语义对照（清 checkpoint 重跑观察差异）。
3. Kafka→Kafka 转发加一列富化：观察键不变、分区路由延续（§3 顺序域设计实证）。
4. 双消费组读同主题：SS 组（offset 在 checkpoint）与传统组（offset 在 broker）互不干扰的监控截图（Kafka 权威指南语义的 Spark 侧印证）。
5. 注入毒丸消息（非法 JSON）：`from_json` 的 `_corrupt_record` + 死信主题分流——生产级容错的最小闭环。

## 10. 校读问答（五问五答）

- **Q：SS 里 Kafka 的 group.id 还有意义吗？** A：弱化了——偏移主权归 Spark checkpoint；group 主要剩监控用途（⚠️ 表述以集成文档为终裁，§2 已给 URL）。
- **Q：多主题多订阅一个查询？** A：支持，`subscribeTopicPattern` 线；分主题水位需分别设计（13 章超时态的输入）。
- **Q：Kafka Streams/Flink 同题怎么做？** A：逐事件 commit 模型不同、但「提交窗口+幂等 sink」公分母不变——[../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md) 对位。
- **Q：本章会讲 Kafka 集群搭建吗？** A：hands-on 册大概率给 docker-compose 版（⚠️ 推定）；按演进节 KRaft 重校准再照抄。
- **Q：和 5 章 JDBC 合读法？** A：同一张业务表的两条入湖路：轮询快照 vs 变更流；键控 upsert 是共同终点（§4 账本合订）。

## 核心概念速览（中英对照）

- **from_kafka/subscribe** — Kafka Source：SS 的 Kafka 读入口，订阅或 assign 两式。
- **startingOffsets** — Starting Offsets：仅首启生效的位置语义；恢复读 checkpoint。
- **offset 版本化提交** — commitOffsetByVersion：assign 模式先算后交的手动闸。
- **元数据列** — Kafka Metadata Columns：key/value/topic/partition/offset/timestamp。
- **to_kafka sink** — Kafka Sink：消息级 at-least-once 写出，无事务聚合。
- **键控分区路由** — Key-Based Partitioning：同键同分区的顺序域设计。
- **重放** — Replay：checkpoint+日志使微批可整体重跑——Kafka 的日志本质红利。
- **端到端语义账本** — E2E Semantics：逐段保证与断点的清单化思维（本章精髓）。
- **幂等 producer** — Idempotent Producer：Kafka 侧去重（与 Spark 侧正交，→演进）。
- **转发管道** — Passthrough/Enrichment Pipeline：Kafka→Spark→Kafka 的近线形态。

## 最新演进与工业实践

- **Kafka 3.x→4.x：KRaft 独占**：ZooKeeper 模式移除（KIP-866/974 线），本书若含 ZK 搭建步骤已过时——部署以官方为准 ✅ https://kafka.apache.org/documentation/（2026-10 实测 200）。
- **消费者组协议 V2（KIP-848）**：新一代轻量再均衡改变运维形态；SS 的 assign 模式与其正交（⚠️ 转述，细节以 KIP/官方文档为终裁）。
- **Spark 侧**：0-10 集成文档线长期稳定（✅ https://spark.apache.org/docs/latest/streaming-kafka-0-10-integration.html 与 SS 版 https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html 均实测 200）；Kafka 作为 sink 的 exactly-once 仍未进入官方承诺（现状与本书一致，⚠️ 校核口径）。
- **CDC 入流主路径**：Debezium/Connect → Kafka topic（键=主键、值=变更信封）→ 本管道，替代 5 章批量 JDBC 轮询；下游直接落 Paimon/Delta 主键表成为 2024–2026 默认架构（[../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md](../Apache_Paimon_Streaming_Lakehouse/11-Flink集成与CDC入湖实践.md)）。
- **Schema Registry 普及**：信封+注册表使 `from_json` 前多一层契约校验，本书裸 JSON 教学需升级认知（⚠️ 观察性陈述）。
