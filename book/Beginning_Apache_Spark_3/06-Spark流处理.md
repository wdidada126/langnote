# 06 Spark Streaming（Spark 流处理）

> 原书 Ch6，pp.221–285（65 页）。章题沿用旧名「Spark Streaming」，内容实为**两代模型的过渡课**：DStream 快速考古 + Structured Streaming 正式登场（输入表/输出模式/触发器/windowed agg）。二级小节未实抓 ⚠️，依章题页幅与官方文档骨架推定；属**精读重构**。

## 6.1 DStream：先学是为了退役 ⚠️

- 模型（官方遗留文档口径，锚点 https://spark.apache.org/docs/latest/streaming-programming-guide.html ✅ curl 200）：输入流切成小 RDD 序列，`DStream` 上的算子=对每个小 RDD 重复应用；批间隔（batch interval）是用户的延迟-吞吐主旋钮；receiver 线（Kafka/Flume）与 direct 线（Kafka 偏移自主管理）两代接入 ⚠️ 本册给到什么深度存疑。
- 本册教学定位（重构）：约一章篇幅的前半 ⚠️——2021 年教材仍保留 DStream，多为读遗留代码服务；本目录建议：**半小时读完 6.1/6.2，重心放 6.3 之后**。
- 对照盘上：DStream 在中文教材里常是流处理的全部（杨力册第 10 章即 DStream 微批，见 [../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md) 头注对两书「2018 平台视角/2022 框架视角」的定性）；权威两代对比在 [../Spark_The_Definitive_Guide/09-结构化流处理.md](../Spark_The_Definitive_Guide/09-结构化流处理.md)。

## 6.2 从批到流：查询引擎的复用 ⚠️

- Structured Streaming 的核心论点（本册金句重构）：**流=无限增长的表（unbounded table）**；你对流写的查询和批查询是同一套 API，引擎负责「增量地跑同一个查询」。
- 三个抽象：Input Table（新到达行）→ Event(ing) Time/触发器驱动的增量查询 → Output Table（结果写出）。
- 与 DStream 的关系一句话：DStream 是「RDD 上的流」，SS 是「查询引擎上的流」——后者才有 schema、优化器与精确语义可谈。

## 6.3 输出模式与触发器：语义第一次成为第一课 ⚠️

- 输出三模式：Append（只追加新行，要求查询结果单调）、Update（增量变化，默认）、Complete（全量结果覆写，要求状态可容）——三选一的约束由聚合类型决定，这是很多人「跑通第一条流」撞墙处 ⚠️（转述官方语义）。
- 触发器：Processing Time（默认微批节拍）、AvailableNow（把「批 vs 流」压成同一个 API 的开关，2020 后新增 ⚠️ 本册是否收录存疑）、Once/连续模式（Continuous，实验性且后续被社区弱化 ⚠️）。
- 官方 SS 文档路径本次 curl **404** ⚠️（见 00 §五登记）——语义以 latest 文档主页 + TDG 权威章为补课源，本节全部标注为转述。

## 6.4 窗口聚合与事件时间入门 ⚠️

- `window(eventTime, "10 minutes", "5 minutes")`：窗口聚合=按 event time 分桶；watermark（Ch7 主角）在此预铺一句：**引擎需要一个「不再等待迟到数据」的承诺点**才能收敛输出。
- 概念辨析（重构自本册练习语境 ⚠️）：processing-time 窗口简单但语义脆弱（重放结果不一致）；event-time 窗口可重放、可纠正——入门者第一直觉「用处理时间」恰恰是要被纠正的。
- Flink 对照：事件时间/水位线的教学最完备形态在盘上 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md) 与 [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)——Spark 的 watermark 语义较 Flink 简并，跨引擎读者须知道这层差异 ⚠️。

## 6.5 🔧 实验 E3：微批 trigger 的两种算法（SQLite 3.45.3，**非本书 Spark 引擎行为**）

- 方法：SQLite 表 `ev(id,cat,amt)` 每 20,000 行模拟一个 trigger 批次（共 10 批）；A 案=每批**全表重算**聚合（Complete 风格），B 案=每批**只聚合新增段**再并入（Append/Update 风格）。
- 实测（毫秒，逐 trigger）：A 案 4.3→13.8→26.9→39.7→29.2→36.6→39.2→37.2→43.2→**48.9**（随表增长）；B 案 3.6/7.0/7.6/4.3/4.7/3.4/2.8/3.1/3.4/**2.8**（近似恒定）。
- 可迁移直觉：①「每 trigger 一个批查询」不是修辞——重算型查询的成本真的随历史线性涨；② Update/Append 模式的增量性来自**状态（或可界定增量）**，不是引擎魔法；③ windowed agg 的 state store 大小由 watermark 控制，不设承诺点则状态无限——这三条与 Spark SS 的微批实现同构 ⚠️（Spark 侧机制转述官方口径，未本机测）。
- 边界声明：本实验无乱序、无迟到、无 checkpoint，因此不涉及 Ch7 的更正语义；数字不可与任何 Spark trigger 指标对比。

## 6.6 本章练习视角（重构）⚠️

三连：① 把同一查询分别跑 Append 与 Complete，观察「Append 不支持非单调结果」报错现场；② socket source+update 模式体会微批节拍；③ 把 6.5 的 SQLite 脚本事件时间列打乱，思考「哪个 trigger 的结果之后会被改写」——这就是 watermark 问题。

## 6.7 两代模型对照卡（重构 ⚠️）

| 维度 | DStream（旧线） | Structured Streaming（新线） |
| --- | --- | --- |
| 抽象 | RDD 序列 | 无界表+增量查询 |
| schema | 无（类型靠代码） | 有（全 SQL 优化器可见） |
| 时间语义 | 处理时间为主 | 事件时间+watermark |
| 状态 | 算子内自带 | StateStore 统一托管 |
| 容错 | receiver/WAL | checkpoint(offsets+state) |
| 写出 | 手动 foreachRDD | 三种输出模式声明式 |
| 学习优先级 | 读懂遗留代码即可 | 主线 |

- 一句话版本：DStream 教你「流是一串批」，SS 教你「流是一张表」——后者的表达力与语义保证全面胜出，故本目录把 6.1 压缩为考古。

## 6.8 第一条流作业模板（重构 ⚠️ 语法示意非原书代码）

```
lines = spark.readStream.format("socket").option("host",...).option("port",...).load()
words = lines.select(explode(split(col("value"), " ")).alias("word"))
counts = words.groupBy("word").count()          # 无状态起点
q = counts.writeStream.outputMode("update") \
        .format("console").trigger(processingTime="10 seconds") \
        .start(); q.awaitTermination()
```

- 三处第一次埋雷：① `groupBy` 在无 watermark 时状态无限——console 跑无妨，落生产必炸；② Append 模式配不上 `count()`（结果会变，非单调）——报错文案即教学法；③ socket source 仅测试用途，生产换 kafka/file ⚠️。
- 建议动手顺序：file source（可重放，最适合观察 trigger 行为）→ socket → kafka（回 `07`）。

## 6.9 trigger 与延迟的算术题（重构 ⚠️）

- 微批模型的延迟下限 ≈ trigger 间隔 + 单批处理时长——「秒级」从来不是 Spark SS 的默认承诺；把 100ms 延迟需求交给本引擎，是选型第一课的反例。
- AvailableNow 的正确打开方式：历史回填（批模式跑同一段代码）→ 切回常态触发器上线——「批流同码」在本册语境里其实就这一个开关 ⚠️ 本册收录存疑，登记为演进补课项。
- 🔧 E3（6.5）的延伸算术：若每 trigger 重算全史，第 n 批成本 ∝ n；增量并入则 ∝ 1——把「批大小恒定、表无限增长」代入，就能理解为什么 Complete 模式只在状态有界（短窗口）时被推荐使用。

## 6.10 本章边界与补课路由

- 讲到了：微批模型、三输出模式、触发器、事件时间窗口入门、watermark 预铺、DStream 考古。
- 没讲到：乱序更正的完整语义、Kafka 生产接入、状态算子 API（全在 `07`）；流式 join/lookup（社区深水区 ⚠️）；连续处理模式细节（官方后续弱化，别投入）。
- 跨引擎补课：watermark 的最细教学在 Flink 线——盘上 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)；架构史（Lambda/Kappa 论战）在 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)；中文平台视角在 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)。

## 6.11 速自检（答案在上文）

1. DStream 的「流」在物理上是什么序列？
2. SS 世界观三抽象的名字？
3. 三种输出模式与单调性的关系一句话？
4. AvailableNow 把什么两个形态压成一个开关？
5. event-time 窗口为什么可重放而 processing-time 不可？
6. 🔧 E3 中 A 案成本的涨法与 B 案的稳法各说明什么？
7. watermark 预铺的那句「承诺点」承诺的是什么？
8. 连续模式（Continuous）今天还值得投入吗，一句读法？

## 6.12 流处理黑话小词典（语境卡 ⚠️）

- 微批（micro-batch）：把流切成小作业序列的执行形态——SS 的默认面。
- 增量查询（incremental query）：同一段查询逻辑只处理新到达部分的执行承诺。
- 状态爆炸：无 watermark 的窗口聚合把历史全留在 StateStore 的事故形态。
- 单调（monotonic）结果：旧行不再变——Append 模式的入场券。
- 重放（replay）：从源重新消费历史以纠正/重建结果——Kappa 的关键词。
- 事件时间 vs 处理时间：数据自己的钟 vs 引擎的钟，所有语义分歧的原点。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 离散化流 | DStream | 旧线：小 RDD 序列上的流抽象 |
| 批间隔 | Batch Interval | DStream 的延迟-吞吐主旋钮 |
| 无界表 | Unbounded Table | SS 的世界观：流=无限增长的表 |
| 增量查询 | Incremental Query | 同一查询语义的每 trigger 增量执行 |
| 触发器 | Trigger | Processing time/AvailableNow/Once 的节拍开关 |
| 输出模式 | Output Mode | Append/Update/Complete 三种写出语义 |
| 单调结果 | Monotonic Result | Append 模式的前提：旧行不再变 |
| 事件时间 | Event Time | 数据自带时间戳，可重放语义的根基 |
| 窗口聚合 | Windowed Aggregation | 按 event-time 桶划的分组聚合 |
| 水位线 | Watermark | 「不再等更迟到数据」的承诺点 |
| 处理时间 | Processing Time | 引擎时钟，语义脆弱但实现简单 |
| 连续模式 | Continuous Processing | 实验性低延迟线，社区热度已降 ⚠️ |

## 最新演进与工业实践

- **DStream 终局**：官方文档站仍托管遗留指南（✅ 链接见 6.1），但 2024–2026 的发行版与云产品教学已全面 SS 化；「入门书保留 DStream 半章」在 2021 合理、2026 是负资产——读法按本目录 6.1 建议执行 ⚠️。
- **Structured Streaming 的工业位**：Spark SS 的差异化在「批流同 API + 落地表格式」（Kafka→Delta/Iceberg 幂等写出），与 Flink 的「原生流+低延迟」形成清晰分工——两册对照盘上在盘实链（见 6.4）；流批四册（#150/#154/#193 等）为波8 兄弟，仅登记。
- **AvailableNow/流批一体教学化**：2022 后入门路径普遍改为「先 AvailableNow 批跑历史，再改 trigger 上线增量」——把本册 6.3 的触发器清单变成实操主线 ⚠️（社区教学共识，非单一官方文档）。
- **Kappa 语境**：Jay Reynolds 2014 年提出「流为主、批为快照」的 Kappa 架构（IEEE Internet Computing 2015 专栏文章 ⚠️ DOI 未本次校验，仅题目+出处+年份），本册 SS 的「无界表」论是其工程化回响之一；系统叙述盘上在 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)。
