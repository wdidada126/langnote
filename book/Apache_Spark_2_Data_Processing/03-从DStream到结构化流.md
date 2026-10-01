# 03 从 DStream 到结构化流：微批、水位线与输出模式

> **取证态**：对应本书副题 *Real-Time Analytics* 的正主，主题「implementing streaming analytics with Spark Streaming」「scalable fault-tolerant streaming applications」与仓库 Module_2/Chapter 8 + 根数据 `newsCorpora.csv`（新闻语料流模拟源）✅ 目录级实抓；章名级 TOC 不可得 ⚠️（00 §3）。Spark 流式行为不可本机实测 → ⚠️ 转述 + 官方 [Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)（✅ 可达）与 [传统 DStream Guide](https://spark.apache.org/docs/latest/streaming-programming-guide.html)（✅ 可达，4.0.1 同路径亦在）双锚；🔧 E1/E2 为快照/重算模拟，**非本书 Spark 引擎行为**。语义正读：[../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)；头名册对位：[../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md)。

## 1. 2.x 的流式双轨：DStream 谢幕前的最后合订本

- **DStream（1.x 正统，2.x 仍在教）**：离散化为 RDD 微序列的 API——`socketTextStream`/Kafka Direct Stream，滑动窗口 `window()`，状态 `updateStateByKey()` ⚠️。语义是「RDD 之上的定时器」。
- **Structured Streaming（2.0 起核心）**：**「流 = 无界表，查询 = 对增量分区反复执行的查询」**——把 §02 的 DataFrame 世界观整体搬到流上，这是与 DStream 的根本代差 ⚠️。

```scala
// Structured Streaming 最小骨架（2.x 写法）
val lines = spark.readStream
  .format("socket")                    // 2.x 教学入门源
  .option("host", "localhost").option("port", 9999).load()
val words = lines.select(explode(split($"value", "\\s+")).as("word"))
val counts = words.groupBy("word").count()
counts.writeStream
  .outputMode("complete")              // append / update / complete
  .format("console")
  .option("checkpointLocation", "/tmp/ckpt")
  .start().awaitTermination()
```

```scala
// 同题 DStream 旧写法（本册时代已属「兼容轨」）
val ssc = new StreamingContext(sc, Seconds(1))
ssc.socketTextStream("localhost", 9999)
   .flatMap(_.split("\\s+")).map((_, 1))
   .reduceByKeyAndWindow((a: Int, b: Int) => a + b, Seconds(5), Seconds(1))
```

## 2. 微批语义与输出模式：🔧 E1 快照 diff 模拟

SQLite（3.45.3）建模：15 行事件按 5 行/拍进 3 个「微批」。**append 类比**=只发射本批增量聚合行；**update 类比**=维护累计状态表、每拍全量重发被改键。实测逐拍值：

| tick | append 发射（本批） | update 状态（累计） |
|---|---|---|
| 0 | g0(2,3.0) g1(2,5.0) g2(1,2.0) | 同左（首轮重合） |
| 1 | g0(2,15.0) g1(1,7.0) g2(2,13.0) | 递增累计 |
| 2 | g0(1,12.0) g1(2,23.0) g2(2,25.0) | g0(5,30.0) g1(5,35.0) g2(5,40.0) |

要点：append 与 update 对**同一数据流**给出完全不同下游形状——Spark 用「输出模式与聚合窗口的相容性」约束（complete 只能配窗口化下游等）⚠️ 转述；SQLite 双表 diff 演示的是语义而非引擎。**非 Spark 微批调度/检查点行为**。

## 3. 事件时间、水位线与迟到：🔧 E2 三遍快照对比

DuckDB（Python 1.5.5）按「到达时刻 ≤ 处理点」切三遍快照做 `date_trunc('minute')` 窗口聚合：

| 快照 | a@10:00 窗口和 | 语义类比 |
|---|---|---|
| 首发射（arrived≤10:01） | **1.0** | 窗口初步闭合发射 |
| lateness 内补发（arrived≤10:03:30） | **5.0** | 迟到行（10:03 到）改写了已发射窗口 → update 重发 |
| 含超迟到（arrived 10:05 行） | 8.0（仅全量重算可见） | 越过 watermark+allowedLateness → 引擎侧该行进丢弃/侧输出路径 ⚠️ |

对照官方口径：`withWatermark("eventTime", "10 minutes")` 决定「何时敢于发射、何时不再保留状态」，`trigger(processingTime/once/continuous)` 决定「何时尝试」——**水位线管正确性、触发器管延迟**，2.x 起即为此框架 ⚠️。流表二象性的完整语义学见 [../Streaming_Systems/06-流和表.md](../Streaming_Systems/06-流和表.md)，水位线专章见 [../Streaming_Systems/03-水位线.md](../Streaming_Systems/03-水位线.md)（两文件均 ✅ 在盘）。

## 4. 容错与端到端恰好一次（2.x 教义）

- **checkpointLocation 双职能** ⚠️：offset log（消费进度）+ 状态快照（HDFS 元数据式可靠性兜底）。
- **端到端 exactly-once** 配方：源端可重放（Kafka offset）+ 微批原子提交 + **幂等/事务 sink**（如支持事务的 Kafka 输出、`foreachBatch` 幂等写）⚠️；逐条 upsert 存储（HBase/Cassandra 线）在 2.x 手册中以「幂等重写」口径解释 ⚠️。互见 [../Streaming_Systems/05-精确一次与副作用.md](../Streaming_Systems/05-精确一次与副作用.md)。
- DStream 侧的 WAL 机制是另一代际方案 ⚠️，本册时代两者并陈——恰是流式容错教学史的标本。

## 5. 流式 join 与状态算子的边界（本册诚实面）

2.x 的 Structured Streaming 对**无界流 join** 约束严格（窗口化 join 方可行）⚠️；有状态算子的内存驻留与 `state` 算子升级语义随版本演进（2.3/2.4 有迭代但本册未逐章可考 ⚠️）——目录版把「连接语义」的正读让位于 [../Streaming_Systems/09-流式连接.md](../Streaming_Systems/09-流式连接.md) 与 [../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md)。

### E1b 第三种形状：complete 全量快照列

给 E1 的累计状态表加 `isCompleteSnapshot` 列并每拍全量重发——三模式在同一实验里对齐：append 只发增量行、update 只发改键、complete 重发全表。SQLite 侧一行 SQL 的事，Spark 侧对应「下游必须能吃重发」的契约差异 ⚠️（complete 只配窗口化聚合输出的相容性约束为 2.x 教义）。**非本书 Spark 引擎行为**。

## 2.5 流源与汇：2.x 教学三件套与生产面孔

| 端 | 关键参数 | 教学位/证据位 |
|---|---|---|
| socket 源 | host/port | §1 骨架的 hello-world 管 ⚠️ |
| 文件流源 | `path` + 目录结构约定 | 本仓库根 `newsCorpora.csv` 的模拟源正位 ✅ |
| Kafka | `subscribe/subscribePattern`、`startingOffsets`（2.x 默认 latest 代） | 生产迁移主面孔；DStream 侧 Direct 风格自管 offset ⚠️ |
| console/memory | 逐拍打印 | 教参默认观测口 |
| `foreach`/`foreachBatch`（后期） | 自定义函数 | 幂等 sink 的收纳口（§4 配方第三元）⚠️ |

- 水位线的两职能（敢发射承诺/清状态承诺）与「必须声明 eventTime 列」前置条件，2.x 定型至今未变（§3/E2 表为语义影子）⚠️；
- 聚合状态是**每键一行**的增量更新，非全量重算——这正是 update 模式贵得有道理的原因（E1 累计表列可见规模）。

## 4.5 时代差问答与自测（本章四问）

- **问：微批是不是「伪流式」？** 答：按延迟谱系它是批与流之间的采样点；2026 视角下 Spark 自己也向更低延迟的发起模型演进（演进表 PIP 行），但「秒级+吞吐+恰好一次」三角里微批仍是最稳的工程解（⚠️ 转述）。
- **问：DStream 代码见者即改？** 答：是——文档在位不等于推荐路径，4.0.1 的 guide 双存但教学主线唯一为 SS（演进表 ✅ 实测两 URL）。
- **问：水位线设多大？** 答：它是「迟到换延迟」的业务参数，不是技术默认值；E2 三遍快照展示的正是承诺兑现/不兑现的两副面孔（§3）。
- **问：checkpoint 删了会怎样？** 答：等价「从头重放」——offset 与状态双失忆；生产脚本以目录存在性当幂等锁是 2.x 民间智慧（⚠️ 转述，勿当官方承诺）。

自测四题：① 同一聚合在 append/update 下下游表形各长什么样（用 E1 三拍数据口述）；② 事件时间与到达时刻何时分叉、水位线管哪一头；③ 端到端 exactly-once 三要素各挡哪一层故障；④ continuous/once/processingTime 触发器与「正确性无关、与延迟有关」的论证。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
|---|---|---|
| 离散流 | DStream | 1.x 正统：以 RDD 微序列表达流的旧 API 轨 |
| 结构化流 | Structured Streaming | 2.0 起核心：流=无界表、查询=增量执行的引擎 |
| 微批 | Micro-batch | 把流切成小批次依次执行的运行模式（Spark 流式默认代名词） |
| 无界表 | Unbounded Table | 持续追加的行集合，SS 的表抽象本体 |
| 输出模式 | Output Mode | append/update/complete 三种再发射契约 |
| 事件时间 | Event Time | 数据自带的业务时间戳维度 |
| 水位线 | Watermark | 「不再等待更早数据」的进度承诺，管发射与状态清理 |
| 允许迟到 | Allowed Lateness | 已发射窗口仍可被迟到行改写并补发的宽限 |
| 触发器 | Trigger | 尝试执行的节奏承诺（processingTime/once/continuous） |
| 检查点 | Checkpoint Location | offset log + 状态快照的容错底座 |
| 端到端恰好一次 | End-to-End Exactly-Once | 可重放源+原子微批+幂等/事务 sink 的合成保证 |
| 侧输出 | Side Output(线) | 超水位迟到行走的旁路收纳（语义学正读在流式书目） |

## 最新演进与工业实践

| 本书（2.x） | 2026 现状 | 依据 |
|---|---|---|
| DStream/SS 双轨并存 | 新代码一律 SS；但官方 DStream 文档 4.0.1 仍在位（未宣判移除），教学叙事以 SS 为唯一主线 | ✅ 两 guide 本次均 200 可达（4.0.1 路径实测） |
| 微批=唯一成熟形态 | SS 向「计划启动执行（PIP）」低延迟形态演进；continuous 早期实验线让位 | ⚠️ 4.x 专页本次未逐字核对，仅给概念名目不编版本细节 |
| RocksDB 状态后端 | 3.x 起作为可选状态存储路线发展（外置依赖、实验→可用代际）| ⚠️ 具体 GA 状态本次不可达页面未证，登记待核 |
| Kafka 事务 sink | 工业标准件；湖仓 sink（表格式事务提交）成为新默认去处 | 盘上互见 [../Use_Iceberg_with_Spark/](../Use_Iceberg_with_Spark/)（目录实名登记 ✅） |
| Kafka Direct/Structured | Structured源 + 云托管流干线并用；Flink 在「真流式」语义席位持续（与 Spark 微批对照的史论见）| [../Stream_Processing_with_Apache_Flink/](../Stream_Processing_with_Apache_Flink/) 目录登记 ✅；论域正读 [../Streaming_Systems/10-大规模数据处理的演进.md](../Streaming_Systems/10-大规模数据处理的演进.md) |
| 版本坐标 | 流式 API 主干在 4.2.0/3.5.9 并行线持续修残 | ✅ [releases.html](https://spark.apache.org/releases.html) 实抓 |

**判语**：本册流式部分是 Learning Path 中「副题即书名」的核心单元——微批语义、水位线-触发器二分、输出模式相容性三件教义至今全部成立，是 2.x→4.x 落差最小的一章；落差在运行延迟与状态后端。
