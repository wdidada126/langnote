# 04 · Spark 流处理配方（原书 Ch5 Spark Streaming）

> 精读重构笔记，非原书文本。目录取证：微信读书官方电子版目录快照（✅ 实抓）；Spark 侧行为 ⚠️ 转述；🔧 组为 SQLite/DuckDB **类比，非本书 Spark 引擎行为**。

## 1. 章域定位

Ch5 全书仅 4 个食谱（Introduction + Word count using Streaming + Streaming Twitter data + Streaming using Kafka），是 12 章中篇幅最小、**范式换代最彻底**的一章：DStream 抽象（离散化流，micro-batch 的原始形态）在 Spark 2.0 后被 Structured Streaming 取代、Twitter 数据源随 API 收紧消失、Kafka 0.8 简化消费者演进为 0.10+ 统一 reader。今天读章的正确姿势：把 4 个食谱当作「微批语义三要素——输入 DStream、窗口算子、输出算子」的最小标本，再用流批三角笔记迁移到当代心智。

## 2. 食谱地图

| # | 食谱（官方目录逐字） | 配方核心 | 2026 等价物 ⚠️ |
|---|---|---|---|
| 5.1 | Word count using Streaming | `StreamingContext(sc, Seconds(1))` + socketTextStream + reduceByKeyAndWindow | readSocket 已删；换 Kafka 源 |
| 5.2 | Streaming Twitter data | OAuth + receiver 拉推文流分词计数 | Twitter source 不存在；Kafka 桥接 |
| 5.3 | Streaming using Kafka | 0.8 时代 KafkaUtils.createStream（receiver DStream） | direct stream(2.x)/结构化 read |
| （章骨架） | checkpointing / window / slide 参数 | 状态与窗口靠 checkpoint 目录兜底 | 状态store WAL 化 |

## 3. 精读块一：DStream 的微批世界观（5.1）

**问题**：如何把「连续流」翻译进 RDD 批次语义。
**配方骨架**：固定 batch interval（如 1s），到达的数据切成小 RDD 序列；`window/slide` 两参数决定窗口滚动，跨窗口的聚合靠 `reduceByKeyAndWindow` 带逆函数（incr/decr）复用上一窗结果。
**评注 ⚠️**：batch interval 决定延迟下限、receiver 决定吞吐上限，二者都在 driver/executor 之间抢资源——这是微批架构的原罪，也是当年「Spark Streaming 到底算不算流」论战焦点。Structured Streaming 把连续性交给增量查询与触发器抽象，DStream 于 3.x 进入维护态（官方流指南仍并列两种 API ⚠️）。
**🔧 类比（DuckDB 1.5.5，非本书 Spark 引擎行为）**：以固定 uid 区间把 20,000 行表切成 5 个「批」，每批做 `GROUP BY user` 聚合写入 sink 表（每批 5 行 ×5 批，批式重放总耗时 1,600.9 ms）——「每批全表扫」的浪费显式暴露：微批系统的固定开销与状态复用（增量聚合）正是 5.1 逆函数技巧解决的问题，单机上把谓词改成增量区间即可复算两种成本差。

## 4. 精读块二：Receiver 与 Kafka 的两种耦合（5.2/5.3）

**问题**：外部消息系统进 DStream 的两条路——receiver 常驻拉取 vs 每批直读 offset。
**配方骨架**：Twitter 食谱示范 receiver（长连接、会丢）；Kafka 食谱用 `createStream` 按 zookeeper consumer group 提交——**at-least-once 靠 receiver 默认、WAL checkpoint 兜底状态类算子**。
**评注 ⚠️**：本书停在 0.8 receiver 形态，同年稍晚即出现 direct approach（1.3/0.10 connector），把 offset 管理交给 Spark 侧实现 exactly-once；食谱的价值是让你看清「谁持有 offset」这个流处理第一问题在 2015 年还没答案。
**与 repo 对照**：Kafka 侧机制详述见 [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)；流式架构叙事（Lambda/Kappa）见 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md) 与 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)。

## 5. 精读块三：窗口语义与状态边界（全章共性）

- **窗口三问**：窗口多大（window）、多久滚一次（slide）、迟到怎么办（本章几乎不谈 ⚠️）；
- **状态两坑**：checkpoint 目录复用错版本导致反序列化爆炸、`updateStateByKey` 全键遍历的延迟增长——食谱用固定参数演示，生产必须按 key 空间规模调 TTL；
- **输出三态**：print/save 每批落外部系统时**不幂等**，Kafka 消费端重放即重复计算——当年唯一解是幂等 sink 设计。
**当代迁移**：watermark/late arrival/state TTL 在 Structured Streaming 成为一等公民，其概念谱系可经 [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)（流数据库正统脉络）与 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)（连续流对照系）双向夹击理解。

## 6. 本章的系列学位置

食谱 5.1-5.3 组成的「socket→twitter→kafka」梯度即流接入教学法的标准三拍；与波 8 流批组（#156/#157/#199/#166，只登记不链）形成「操作手册 vs 架构叙事」互补——架构判断请去那四册，手改配方回这一章。

## 7. 互链清单

- 主参照：[../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md)（DStream → Structured Streaming 的当代答复）
- 底座：[../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)、[../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)、[../bigdata/Spark大数据实时计算.md](../bigdata/Spark大数据实时计算.md)
- 流三角：[../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)、[../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)、[../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)
- 前章/后章：[03-SparkSQL配方.md](03-SparkSQL配方.md) ｜ [05-MLlib基础与回归配方.md](05-MLlib基础与回归配方.md)

## 8. 配方骨架速查（考古重构，⚠️ 转述，语法按 1.x 惯例）

- **5.1**：`val ssc = new StreamingContext(sc, Seconds(1))` → `ssc.socketTextStream(host, port)` → `lines.flatMap(split).map((_, 1)).reduceByKeyAndWindow(Seconds(30), Seconds(10))` → `ssc.start(); ssc.await()` ⚠️。
- **5.2**：TwitterUtils.createStream(ssc, auth 四件套（consumer key 等）) → filter 语言 → 分词计数打印；receiver 线程常驻 ⚠️。
- **5.3**：KafkaUtils.createStream(ssc, zookeeperQuorum, consumerGroup, topicPartitions map) 得 (key, msg) 流；offset 由 zookeeper 侧 consumer 群提交 ⚠️（direct 路线同年代晚一步出现）。
- **容灾**：`ssc.checkpoint(<hdfsDir>)` 兜住状态算子；恢复即从目录重放图定义与 WAL ⚠️。

## 9. 自测卡（合卷作答，8 问）

1. batch interval 调小的两个后果？（调度开销放大、小批处理不完堆积）
2. window 与 slide 各控什么？不整除时的形态差？（窗口跨度/滚动步长；重叠批）
3. reduceByKeyAndWindow 的逆函数省掉了什么？（整窗重算，只算进出边界批）
4. receiver 丢数的条件是什么？WAL 为什么能兜住状态类？（长连接断/背压；日志重放补齐输入）
5. 5.3 当年为什么不是 exactly-once？（offset 在 zk 侧提交、与处理结果不同事务）
6. updateStateByKey 的延迟增长根因？（全键遍历）
7. E8 实验里「批」的切分键是什么？换成 ts 切会暴露什么问题？（uid 区间；迟到与乱序未建模）
8. DStream 与 Structured Streaming 在「状态存放」上各靠什么？（checkpoint 目录+WAL vs 状态 store+changelog ⚠️）

## 10. 小练习

1. 把 5.1-5.3 三食谱各改写为 Structured Streaming 的三行伪码（readStream/writeStream/trigger），标注语义缺口（如 watermark）。
2. 重放 E8（脚本 `D:\develops\tmp\dbwave_w8_scbkt\exp.py`）：把 5 批改 20 批，记录总耗时变化，用一句话说出「批大小-固定开销」曲线形状。
3. 为团队写半页「2015 微批 vs 2026 SS/Flink」选型备忘：延迟下限、状态规模、乱序容忍三格各填谁。

## 11. 易混点辟谣（快问快答）

- **误区：Spark Streaming 等于实时**——微批延迟下限=batch interval，毫秒级诉求本就不属于它的叙事 ⚠️。
- **误区：checkpoint 默认兜底一切**——不设目录时状态算子挂了就是全丢，DStream 图定义同样要落盘。
- **误区：5.3 用 Kafka 就 exactly-once**——offset 在 zk 侧提交、与处理结果不同事务，食谱形态是 at-least-once。
- **误区：Twitter 食谱已完全无用**——它示范的「外部服务 receiver」教学位由 datagen/Kafka 桥接续任，模式没死。
- **误区：DStream 与 Structured Streaming 可混用互补**——状态与语义两套体系，一个作业只应有一套 ⚠️。
- **误区：5.2 的教训已过时**——「第三方 API 作为流的输入端最脆弱」在 2026 的 SaaS webhook/轮询源上逐字重现。
- **误区：并行度拉高=流更好**——批变小后调度开销与算子固定成本占比反升。
- **误区：WAL 开了就 exactly-once**——它保输入重放不保输出幂等，端到端语义看整条链 ⚠️。
- **误区：流食谱可以照抄批食谱参数**——batch interval 与窗口参数的耦合是流侧独有约束。

## 12. 读后行动清单

1. 把 5.1 改写为 Structured Streaming 三行伪码（readStream/writeStream/trigger），标出 watermark 缺口。
2. 重放 E8（`exp.py`）：5 批改 20 批，记录总耗时，写一句「批大小-固定开销」曲线形状。
3. 制作术语卡四张：window/slide、WAL、offset 归属、watermark——每张一句 2015 与一句 2026。
4. 读 [../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md) 引言，列出本章三食谱各自的 SS 对应物。
5. 用一页纸回答「微批第一波（本章）→ 增量查询（SS）→ 连续流（Flink）」三段的延迟-状态-语义三角取舍，收尾回贴流三角互链。

### 本章一页纸总结

三要素：输入 DStream（socket/receiver/Kafka）→ 转换算子（窗口/状态族）→ 输出算子（print/存外）。
两旋钮：batch interval 定延迟下限，window/slide 定业务视野。
一条底线：输出不幂等则一切语义白谈——sink 设计先行。

## 核心概念速览（中英对照）

- **DStream** — discretized stream：连续流离散化为 RDD 序列的核心抽象，微批范式的本体。
- **batch interval** — 批间隔：微批系统的延迟下限旋钮，与窗口参数联动设计。
- **StreamingContext** — StreamingContext：流应用的调度入口，持有图与检查点配置。
- **receiver DStream** — receiver-based input：长连接拉取式输入，吞吐受限于 receiver 且可能丢数。
- **reduceByKeyAndWindow** — 窗口聚合：带增减逆函数的跨窗口复用技巧，避免整窗重算。
- **updateStateByKey** — 键状态更新：跨批维护每键状态的通用算子，全键遍历是其性能软肋。
- **checkpointing** — 检查点：把图定义与 WAL 状态落 HDFS 的容灾机制，版本错配是经典坑。
- **at-least-once** — 至少一次语义：1.x receiver 路线的默认交付保证，幂等 sink 兜底。
- **direct approach** — 直读 Kafka：Spark 侧持有 offset 实现精确一次的方向，本书成稿于其前夜 ⚠️。
- **watermark** — 水位线：迟到数据容忍边界，本章缺席、Structured Streaming 补上的关键概念。
- **socketTextStream** — socket 输入源：5.1 演示用假数据源，仅教学价值。

## 最新演进与工业实践

- **API 换代**：Structured Streaming（2.0 实验 → 2.2 生产可用 → 3.x 默认推荐）以增量查询 + 状态store + checkpoint 重构本章全部三题；官方指南 ✅ https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html （2026-10-01 curl -sI 200）。DStream 文档并列保留但不再加特性 ⚠️。
- **语义升级**：offset 管理进 checkpoint、输出端幂等写 + 4.x 的 replay 支持使「端到端 exactly-once」从技巧变成保证；Kafka connector 统一为 0-10 reader 后，0.8 时代的 zookeeper 参数全数作废——食谱 5.3 的配置文件形态已是考古材料。
- **Twitter 谱系**：receiver 型社交源随 API v1.1 收紧退役；演示型流数据改由 `readkafka`/datagen/云事件总线供给，教学三拍中的第二拍已重写。
- **人物与文献**：Spark 项目与 Structured Streaming 谱系由 Matei Zaharia、Tathagata Das 等在 Databricks/UCB 线推动；概念史对位可引流式书目三角（本目录上节）；本书成书时间（2015-07）恰在 Spark 1.4/1.5 窗口期、SS 论文（SIGMOD 2018 线 ⚠️ 未过 Crossref 校验，仅题录）之前，属「微批第一波」的一手记录。
- **工业现状**：2026 年新流负载里 Flink（连续流）与 Spark SS（微批）按延迟需求分治，Spark 侧增量迁移叙事可经 [../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md) 与 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md) 双向索引；Kappa 化（一切实为流）仍是争论中而非默认 ⚠️。
