# 07 Advanced Spark Streaming（Spark 流处理进阶）

> 原书 Ch7，pp.287–329（43 页）。Structured Streaming 的生产三件套：状态与 watermark 精细语义、Kafka 接入、容错与落地（checkpoint/幂等/端到端 exactly-once）。二级小节未实抓 ⚠️，主题簇依章题页幅推定重构；属**精读重构**。

## 7.1 状态算子与 StateStore ⚠️

- 有状态查询（windowed/flatMapGroupsWithState/mapGroupsWithState）把「每 trigger 重算」变成「增量更新 keyed state」；state 按 (分组键, 窗口/时间片) 落 RocksDB/内存两实现可选 ⚠️（本册是否讲到 RocksDB 存疑，登记）。
- watermark 的三重作用（重构官方语义）：① 何时关闭旧窗口；② 何时清状态（`stateStore.timeout` 类约束）；③ 迟到数据是否还有资格**更正已输出结果**。
- `outputMode` 与更正语义的联动：Update 模式允许对「未过期窗口」的迟到行改写旧行；Complete 全量覆写天然兼容更正但写出量大——本册练习给的就是这对取舍 ⚠️。
- Flink 侧的对照（盘上权威）：[../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)——Flink 的 watermark 多源对齐/idleness、State TTL 表达比 Spark 更显式 ⚠️；工程上「复杂状态机选 Flink、批流同码选 Spark」是 2024–2026 常见分工。

## 7.2 Kafka 接入：从 socket 玩具到真实源 ⚠️

- 生产读法：`readStream.format("kafka")` + `subscribe/assign`、偏移语义（startingOffsets=latest/earliest/specific）；消费端偏移**不是** Kafka group 的事，而是随 checkpoint 走——这是 Spark SS 与「普通 Kafka 应用」心智的最大断点 ⚠️（官方文档转述）。
- 解析面：`value` 是 binary，真常态是 JSON 解码+schema 演进脏数据分流（from_json + `_corrupt_record`），本册给了入门版 ⚠️。
- 写回 Kafka：foreachBatch 里 `selectExpr("key","value")` 攒批发送；吞吐与微批节拍匹配是第一课 ⚠️。
- direct/receiver 考古一句带过（DStream 遗留），2026 读法见 `06`。

## 7.3 容错与端到端语义 ⚠️

- checkpoint 目录双账本：已读偏移（source offsets）+ 状态快照（state logs）——作业挂掉重启从「最后完成的 trigger」续跑，源端重放不重复计入。
- 三层幂等拼图（重构）：源可重放（Kafka）+ 引擎记录进度（checkpoint）+ **汇可去重**（幂等写出）——三者齐才谈 end-to-end exactly-once；本册给的工业样板：写出到支持事务/幂等的表格式（Delta 的 `MERGE INTO` 事务提交）⚠️。
- 对照盘上：[../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)（波2 权威叙事，exactly-once 的分布式语境）与 [../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md](../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md)。

## 7.4 流作业的日常运维 ⚠️

- 监控四元组（官方 metrics 口径转述）：trigger duration、batch 内 input rows/sec、source 端 lag（Kafka 积压）、state size——「输入慢不是问题，处理追不上才是」。
- 扩缩与背压：微批引擎的背压是隐性的（trigger 拉长→lag 增长），不像 Flink credit 模型显式 ⚠️；入门级处方面只有：加 executor、调 shuffle 分区、缩窗口状态。
- 架构叙事补课：本册未及的 Lambda→Kappa 论战线，盘上 [../分布式实时处理系统.md](../分布式实时处理系统.md) 单文件群与 [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)（波3 在盘）；Kappa 原始提出：Jay Reynolds《Stop Thinking About Batch》（IEEE Internet Computing, 2015）⚠️ DOI 未校验，只题录。

## 7.5 🔧 迟到与更正的单机标本（SQLite 复用 E3 底座，**非本书 Spark 引擎行为**）

- 方法：在 6.5 的 `ev` 表上追加两批「迟到段」（id 落在已结算批次区间内），分别演示：A 案（全表重算+覆写）自动「更正」历史窗口；B 案（增量并入）若不改状态则历史窗口**保持错误**。
- 观测：A 案每次覆写的代价 = 全量结果重写；B 案代价小但需要「窗口未过期才并入」的 watermark 纪律，否则要么漏更正要么状态无限。
- 迁移结论：watermark 的本质在任意引擎都一样——**用「多大历史保持可变更」换「输出能收敛」**；Spark 用 event-time 表达式实现，本标本用 SQL 重算实现，语义等价、成本面不同 ⚠️（Spark 具体边界值如 late-threshold 行为未在本书实测范围）。

## 7.6 本章练习视角（重构）⚠️

① 把 7.5 的迟到段比例从 1% 拉到 20%，观察 A 案重写成本与 B 案漏更正率——体感 watermark 的「宽容度」；② Kafka source 重启实验（本机无 Kafka → ⚠️ 只在文档层核对 checkpoint 目录内容结构）；③ 给流查询加 `foreachBatch` 打印每 trigger 的 metrics 表。

## 7.7 watermark 精细语义卡（重构 ⚠️ 转述官方口径）

- 定义式：watermark = max(已见事件时间) − 允许迟到时长；引擎以此断言「早于此水位的事件大概率不再来」。
- 三个判定点：
  1. 窗口何时关闭（事件时间 < 水位 − 窗口跨度 → 不再更新该窗口）；
  2. 迟到行是否被丢弃（`dropLate` 语义，窗口已结算则弃）；
  3. 状态何时清理（与输出模式联动：Update 保留未过期窗口状态）。
- 入门者误区三连：以为 watermark 是「数据年龄」（其实是事件时间承诺）、以为设得越大越安全（状态无限膨胀）、以为多源时各源独立推进（乱序源拖尾需要监控）。
- 🔧 与本目录标本的接缝：7.5 用「重算+覆写」回避了 watermark 的实现复杂度——这个回避本身说明：watermark 不是新发明，是任何增量系统都要回答的「收敛承诺」问题，Spark 只是给了声明式写法 ⚠️。

## 7.8 Kafka 接入检查单（重构 ⚠️）

- [ ] `startingOffsets`：首次用 earliest（全回填），之后由 checkpoint 接管——别改这个期待「重置消费」。
- [ ] key 的解码：`cast("string")` 还是二进制，schema 契约写进注释。
- [ ] 值格式：JSON→`from_json`+`_corrupt_record` 保留列，坏行旁路而非静默丢。
- [ ] topic 分区数 ≥ 期望并行度的整数倍——微批内并行受源分区钳制。
- [ ] 写出 Kafka 用 `foreachBatch`+外部 producer，事务/幂等 producer 配置在生产端 ⚠️。
- [ ] 积压告警接 lag 指标（7.4），阈值按「追平所需时间」定而非绝对值。

## 7.9 exactly-once 的三层论证（重构 ⚠️）

- 层一（源）：Kafka 偏移可重放——重读历史不改变「逻辑输入序列」。
- 层二（引擎）：checkpoint 的 offsets-log 决定每个 trigger 的处理区间，失败 trigger 重跑、成功 trigger 永不重计——这是「exactly-once processing」的实现面。
- 层三（汇）：写出必须幂等或事务——Delta/Iceberg 的 merge/commit 天然满足；普通文件系统 Append 不满足（重跑重复行）⚠️ 官方文档明确此边界。
- 一句话记忆：Spark 保证的是 processing 面，end-to-end 是「你+汇」的合同；本册给的 Delta 样板就是把合同签满的工业做法。
- 系统语境对照：事务/恢复的理论底座在盘上 [../../db/db.md](../../db/db.md) 论文线（ARIES/两阶段提交条目）与 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)；本册不给理论，这个缺口要诚实登记。

## 7.10 本章练习扩展（重构 ⚠️）

1. 用 7.5 标本给迟到段加「窗口已过期」判定列，模拟 `dropLate` 行为，比较丢与不丢的指标差。
2. 阅读 checkpoint 目录结构（offsets/logs 两子树；无集群环境 ⚠️ 以官方文档图为准）。
3. 写一段「Kafka→SS→Delta merge」的伪代码 pipeline，标出哪一步签了幂等合同。
4. 给同一流作业分别配 Update/Complete+短窗口，观察输出行数差异，验证 6.3 的模式约束。

## 7.11 速自检（答案在上文）

1. watermark 的三重作用各是什么？
2. 定义式一行：watermark = ____。
3. Update 模式下「未过期窗口」的状态为谁保留？
4. Spark SS 的消费偏移由谁记账（不是 Kafka group）？
5. checkpoint 目录的两本账各存什么？
6. 端到端 exactly-once 的三层合同分别签在哪些组件？
7. 微批背压的显形指标是什么？
8. 🔧 7.5 标本里 A/B 两案各对应哪种输出模式气质？
9. RocksDB state store 何时该考虑？（本册给没给 ⚠️ 诚实题）
10. 一句话说明「processing exactly-once ≠ end-to-end exactly-once」。

## 7.12 流式运维黑话小词典（语境卡 ⚠️）

- 追平（catch-up）：lag 清零的过程，扩容/缩窗的验收线。
- 拖尾源（straggler source）：多流中事件时间最不活跃的那个，压着全局水位。
- 空洞（hole）：水位已越过、迟到却落在其前的数据——dropLate 的弃子。
- 幂等键（idempotency key）：汇端去重的业务主键，merge 条件的灵魂。
- 小批饥饿：trigger 到点但输入为空，产出空 batch 的常态，不算故障。
- 作业僵尸：awaitTermination 挂着的无监控作业——入门到生产的第一只要杀的害虫。

## 7.13 微补：一个常被问的边界

- 「流查询能改 schema 吗」：SS 的查询 schema 固定，源侧 JSON 加列需重启作业并核对 checkpoint 兼容性——这是「流作业发布也要变更管理」的最早一课，本册未展开 ⚠️，登记为补课位。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| keyed 状态 | Keyed State | 按分组键+时间片维护的增量状态 |
| 状态存储 | StateStore | 状态的持久化载体（内存/RocksDB） |
| 迟到数据 | Late Data | event time 落在已结算窗口的数据 |
| 窗口更正 | Result Correction | 迟到行改写已输出窗口结果的能力 |
| 偏移跟踪 | Source Offsets Tracking | 随 checkpoint 记录的消费进度 |
| 断点目录 | Checkpoint Location | offsets+state logs 的落盘位置 |
| 幂等写出 | Idempotent Sink | 重放不产生重复效果的汇端 |
| 端到端精确一次 | End-to-End Exactly-Once | 源重放×引擎进度×汇幂等的合取 |
| 批处理钩子 | ForeachBatch | 每 trigger 对微批 DataFrame 执行任意写出 |
| 积压 | Lag | 生产与消费的速度差 |
| 隐性背压 | Implicit Backpressure | 微批引擎靠 trigger 拉长实现的反馈 |
| Kappa 架构 | Kappa Architecture | 流重放取代批的单一管线主张 |

## 最新演进与工业实践

- **表格式成为落盘默认（2021→2026）**：本册的 Delta MERGE 样板已成工业通用剧本：Kafka→Structured Streaming→Delta/Iceberg；Delta 文档 https://delta.io/（✅ 200）、https://docs.delta.io/latest/index.html（✅ 200）；Iceberg 对位盘上 [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md) 与 [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)（Paimon 线把「流式湖仓」做成原生主张，读 Spark SS 落库时可对照）。
- **SS 的延迟天花板未变**：微批语义使 <1s 场景仍归 Flink/原生流系统 ⚠️；Spark 4.x 的流处理演进集中在连接管理、V2 connector API 与表格式联动，而非延迟突破（官方 news 页 ✅ https://spark.apache.org/news/）。
- **监控工业化**：Spark MetricsReporter→Prometheus 系、云厂商托管作业画像替代裸 Web UI；「流作业可观测」话题盘上归 [../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)。
- 波8 兄弟分工登记（不链）：#150《Modern Data Engineering with Spark》副题即 Mission-Critical Streaming——本册 Ch6/7 的「生产化下一步」正落在它的问题域；#196 教学册同样覆盖 SS 但更浅。
