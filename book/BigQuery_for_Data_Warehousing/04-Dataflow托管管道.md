# 04 Dataflow 托管管道

> 对应原书 **Ch.7 Dataflow（pp.123–152）**（章题/页码：Crossref DOI _7，✅ 实抓）。
> 正文为精读重构；Dataflow/Beam 机制为官方文档转述（⚠️），✅ URL 经 `docs.cloud.google.cn` 镜像 2026-10 实测 200。

## 一句话主题

第 7 章是全书管道技术的核心章：当 Ch.5 批量与 Ch.6 流式都不够用（要清洗、要关联、要窗口聚合、要处理乱序），把「流批同一程序」的 Apache Beam 交给托管引擎 Dataflow 跑。作者的立场很清醒：**Dataflow 是重武器，用之前先回答「insertAll + 定时 SQL 为什么不行」**。

## 7.1 概念定位（⚠️ 转述）

- **Dataflow = Apache Beam 模型的 Google 托管运行时**：全托管、自动扩缩 worker、按 worker 资源-秒计费（2020 口径），无主节点概念；✅ 概览 https://docs.cloud.google.cn/dataflow/docs/overview（镜像 200）。
- **Beam 编程模型三件套**：`PCollection`（分布式不可变数据集）→ `Transform`（用户函数+引擎可优化的算子图）→ `Pipeline`（DAG，运行时翻译成执行图）。同一份代码换 runner 即换执行环境（DirectRunner 本地调试 / DataflowRunner 云端生产）——「写一次、批流两跑」。
- 与盘上谱系的关系：Beam 之于 Dataflow ≈ Spark SQL 之于托管集群；Flink 线的对位阅读在 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)、[../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)（波前在盘，写前已验名）；理论总账在 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)。

## 7.2 面向数仓的 IO 形状（重构自本章用例线）

- 读侧：`TextIO/GCSIO`（文件批量）、`PubsubIO`（流式事件）、`JdbcIO`（关系库轮询）、`BigQueryIO.read`（读回仓库做加工）；
- 写侧：`BigQueryIO.write` 的两种姿势——**批量写**（临时文件+load job，走 Ch.5 语义、无流式配额）vs **流式写**（Storage 通道直写分区表，走 Ch.6 语义）；写侧选姿直接决定账单结构，这是本章与 Ch.4 的暗线（见 [02-数据盘点与成本管控.md](02-数据盘点与成本管控.md)）；
- 典型管道形态（作者示例的抽象）：`PubSub 原始事件 → ParseFn(校验/标准化) → 侧输出坏记录 → 与 GCS 维表 join(用 View/Broadcast) → BigQuery 目标表`——坏记录侧输出落 GCS 供人工审，是「可对账」原则在管道层的实现；
- 模板（Templates）：Dataflow 提供文本/BigQuery/BQ-to-GCS 等预制模板，Console 一键起管道——作者提示：模板适合标准场景，**复杂清洗逻辑别硬塞模板参数，回归自定义 pipeline**。

## 7.3 流式语义深水区（本章技术含量最高处，⚠️ 转述）

- **窗口（Windowing）**：把无界流切成有界桶（固定/滑动/会话窗口）——聚合、join、去重都在窗口内谈；
- **Watermark 与乱序**：引擎以事件时间水位线判断「窗口还能不能再进迟到元素」；允许延迟（allowed lateness）+ 累计触发器（accumulating firing pattern）实现「先快值后修正值」的两段输出——对数仓的意义：**报表先出不准的，修正版幂等覆写同一分区**（与 Ch.6 装饰器覆写同构）；
- **Exactly-once 讨论**：Beam 的读取侧可重放 + 写入侧幂等键（Kafka offset/文件命名/insertId+MERGE）拼出 effectively-once；作者老实承认 BigQuery 表上没有主键约束，**去重终究是下游 SQL 的责任**（Ch.8/9 回收，见 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)）；
- 状态与键化：`GroupByKey` 与 per-key state 是会话化（sessionization）类需求的正解，但键基数失控会引爆 shuffle——Spark Structured Streaming 的对应机制（state store/checkpoint）在同波兄弟册 #150《Modern Data Engineering with Apache Spark》（目标目录 `Modern_Data_Engineering_with_Spark`）建档收束，按波8 兄弟规则**只登记不链**，登记见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 7.4 何时不用 Dataflow（作者清单的重构）

1. 纯搬运无变换：`bq load`/定时任务即可，管道引擎是杀鸡牛刀；
2. 变换能用一条 scheduled query 表达：用 Ch.10 调度 SQL，成本近零（见 [06-作业调度与无服务器函数.md](06-作业调度与无服务器函数.md)）；
3. 团队没有 Java/Python pipeline 工程力：维护成本 > 托管省下的运维成本；
4. 亚秒级响应需求：Dataflow 端到端是秒-分钟级，那不是仓库场景，该去流处理服务层。

## 实操演练建议（不可实测口径下的替代学习法）

- DirectRunner 本地跑通同一份 Beam 代码（pip 安装 apache-beam 本波属新装禁止，仅作为读者自学建议给出，⚠️ 非本波实测）；
- 本仓库实测纪律：BigQuery/Dataflow 均不可本机连测，机制全走 ⚠️ 转述 + ✅ 文档；概念类比组（🔧 E1/E2/E3/E4/E5 共 5 组）分布在 01/02/03/07 号文件，覆盖「扫描剪枝/分区裁剪/热冷分档/物化复用」，可代偿直觉。

## 附：Beam 配方卡与运维心法（自拟教学示意，⚠️ 非原书内容、非实测）

- **最小管道骨架**（Apache Beam Python 风格伪码，仅作形状记忆，不可直接运行——本波禁新装依赖）：

```python
with Pipeline(options) as p:
    raw = p | "read" >> PubsubIO.readStrings().fromTopic(topic)
    good, bad = (raw
        | "parse" >> Map(parse_and_validate)
        | "tee"    >> Partition(lambda kv, unused: 0 if kv.ok else 1))
    bad  | "quarantine" >> WriteToText(gcs_quarantine_dir)   # 坏记录隔离带
    (good
        | "window" >> Window.into(FixedWindows(300))
        | "agg"    >> CombinePerKey(sum_events)
        | "write"  >> BigQueryIO.write_rowcounts()
                        .to(table).withStreamWrites(True))
```

- **读写矩阵**（本章决策核心，重构）：

| 源→汇 | 批量姿势 | 流式姿势 | 账单落点 |
| --- | --- | --- | --- |
| GCS→BQ | TextIO+BigQueryIO 临时文件 | FileBasedStreamingSource | 装载免费/查询付费 |
| PubSub→BQ | 定时微批拉取 | 直写（withStreamWrites） | 流式配额+存储侵蚀 |
| JDBC→BQ | JdbcIO 读+批量写 | 轮询伪流（不推荐） | 源库压力审计 |

- **乱序三参数速记**：watermark（引擎的「现在」估计）、lateness（再等多久）、trigger（何时发射/是否累计）——三者组合=「先快后准」的产品语义；记法：**窗口定形状、水位定信任、触发器定节奏、迟到定悔棋**；
- 排障清单（依本章叙事重构）：worker 启动失败看 IAM/网络标签；shuffle 膨胀看键基数与热点（先 `count per key` 采样再上生产）；窗口不闭合看水位线是否被死源拖尾（`--max_num_workers` 与 idle hint 是止血带）；成本失控看 1 人 1 管的「管道僵尸」巡检——已停需求仍在跑的流式作业是最大的静默浪费；
- 模板作业心法：预制模板=「参数化的一次性脚本」，Flex 模板=「打包你自己的镜像」；作者的警告适用至今——**模板参数的排列组合不是编程模型**，超过三层 if 的逻辑请回到代码库；
- 思考题（5 道）：T1 Beam「写一次批流两跑」承诺在 IO 层（文件 vs 消息）兑现率如何，哪些算子破坏它？T2 为什么大维表 join 流要广播而不是 shuffle？T3 effectively-once 与 exactly-once 差在哪个组件？T4 水位线拖尾对数仓新鲜度 SLA 的传导路径？T5 本章 7.4「何时不用」四条与你团队现状对表，哪条先命中？

## 系列互链

- 同书纵向：上游摄入语义 [03-批量装载与流式摄入.md](03-批量装载与流式摄入.md)；下游表内加工与调度 [06-作业调度与无服务器函数.md](06-作业调度与无服务器函数.md)；管道产出的对账在 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)。
- 他书横向：Beam/流式理论 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)；Flink 对照 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)；湖仓写侧的同类问题 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)、[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)（盘上已验名）。

## 附二：误区速查与选型对照（重构，⚠️ 非原书内容）

- **十条误区**（社区高频，依本章叙事归拢）：
  1. 「有 Dataflow 就能实时」——端到端秒-分钟级，别承诺亚秒；
  2. 「Beam 代码与 runner 无关」——IO 连接器与状态后端的可用性按 runner 而定；
  3. 「窗口=业务时段」——固定窗口对齐时钟，会话窗口对齐行为，混用产出四不像指标；
  4. 「水位线会自动追上」——死源的 idle 处理要显式配置，否则窗口永不闭合；
  5. 「侧输出是可选卫生」——坏记录无隔离带=静默丢数+对账失败二连；
  6. 「流式写免配额」——写姿走 Storage 通道仍受行速率与配额约束（Ch.6 同款）；
  7. 「扩 worker 解决一切」——键倾斜下加机器只是把热点搬去更多机器；
  8. 「模板够用」——参数拼不出业务逻辑，三层 if 就该回代码库；
  9. 「测试可省 DirectRunner」——单元测试 PTransform 是 Beam 工程的第一纪律；
  10. 「管道活着=管道有用」——僵尸流式作业是账单里的长生不老药，季度盘点必须点名（Ch.8 卫生线的管道版）。
- **三平台管道概念对照**（帮助迁移已有心智，⚠️ 各家细节以其文档为准）：

| 概念 | Dataflow/Beam | Flink | Spark Structured Streaming |
| --- | --- | --- | --- |
| 最小单元 | PCollection | DataStream | DataFrame(append) |
| 窗口 | Window+Trigger | Watermark+Window | 事件时间窗口 |
| 迟到 | allowed lateness | allowed lateness | late join 容忍 |
| 状态 | per-key+state | keyed state | state store |
| 语义 | 读可重放+写幂等 | checkpoint 两阶段提交 | checkpoint+foreach 幂等 |

- 与盘上对照读物：Flink 纵深见 [../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md](../Stream_Processing_with_Apache_Flink/00-总览与阅读地图.md)；Spark 线头名册在 [00-总览与阅读地图.md](00-总览与阅读地图.md) 登记（同波册只登记不链）。

## 核心概念速览（中英对照）

- **Apache Beam** — Beam：统一批流编程模型的标准与 SDK，Dataflow 是其托管运行时。
- **PCollection** — PCollection：Beam 中分布式不可变数据集，可无界（流）可有界（批）。
- **Runner** — Pipeline Runner：同一图的执行后端；DirectRunner 调试、DataflowRunner 生产。
- **窗口化** — Windowing：按事件时间把无界流切成可聚合的有限桶。
- **水位线** — Watermark：引擎对「事件时间推进到哪」的估计，迟到判定的依据。
- **允许延迟** — Allowed Lateness：窗口关闭后仍接受迟到元素的附加时限。
- **触发器** — Trigger：定义窗口结果何时发射、是否累计修正的输出节奏。
- **侧输出** — Side Output：把坏记录/特殊元素分流到次级 PCollection 的机制。
- **BigQueryIO** — BigQueryIO：Beam 读写 BQ 的 IO 连接器，批量/流式两种写姿。
- **模板作业** — Flex Template/Job Template：参数化预制管道，免部署代码即可起跑。
- **会话化** — Sessionization：按活动间隔把事件流归并为会话的键化窗口计算。
- ** effectively-once** — Effectively-Once：可重放读取+幂等写入合成的实际不重不丢语义。

## 最新演进与工业实践

- **Dataflow Gen2 / 新版控制台（2024–2025）**：托管管道向「Gen2」演进，与 BigQuery 数据集/例证化作业绑定更深，面向数据工程师的低代码定位更明确（⚠️ 转述；canonical 文档页本环境镜像不可达，不给 ✅ 链）。经典 overview 仍 ✅：https://docs.cloud.google.cn/dataflow/docs/overview。
- **Beam 版本线**：Beam 2.x 长期主线的 2024–2026 发布（Java 21 运行时、Go SDK 成熟化、Python 性能路径改进）持续进行 ⚠️（beam.apache.org 本波未验证可达性，只题名不给 ✅）；Beam 的 Model API（LLM 推理内嵌管道，2025 起）是本波「流批+AI」交汇新点 ⚠️。
- **写侧统一**：Dataflow 流式写 BigQuery 的底层通道并入 Storage Write API 体系（✅ https://docs.cloud.google.cn/bigquery/docs/write-api 镜像 200），配额与监控口径与 Ch.6 一致收敛。
- **工业实践**：2024–2026 团队选型更常见的是「轻量场景交给托管 CDC/订阅推送、重变换才上 Dataflow」，作者 2020 年的「先问 insertAll 为什么不行」被制度化为管道选型评审单；与 dbt 的分工是「Dataflow 管摄入与清洗、dbt 管仓内建模」，见 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)。本册所在波次的 Spark 流批诸册（#150/#216 等）在盘后将补三角对读，现阶段按波8 规则只登记于 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
