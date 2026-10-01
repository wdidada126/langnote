# 02 Spark运行原理（Ch2: How Spark Works）

> 章题取证 ✅（终版目录第 2 章）；节级结构参考 2e 草案第 2 章（✅ 实抓）：2.1 生态位 / 2.2 RDD 并行模型（惰性、持久化、不可变、类型、转换与行动、宽窄依赖）/ 2.3 作业调度 / 2.4 Job 剖析（DAG/Job/Stage/Task）/ 2.5 小结。⚠️ 终版或有增删，口径同 00。

## 0. 本章主线

调优的一切结论都要回落到这张执行模型地图上：

- **依赖关系决定 Stage 切分；**
- **Stage 决定任务边界；**
- **任务边界决定并行度与倾斜形态；**
- **内存模型决定"慢"会不会升级成"挂"。**

本章同时安置本册 🔧 E1 类比实验（内存阶梯与溢盘）。

## 2.1 Spark 在大数据生态中的位置（⚠️ 转述）

- 计算层（Spark）⇄ 存储层（HDFS/对象存储/湖仓表格式）⇄ 资源层（YARN/K8s/独立集群）。
- 本册视角的成本分摊：性能问题约 40% 出在**层间协议**（序列化、小文件、元数据），40% 出在**层内配置**，20% 出在**应用代码**——先定位在哪一层再动手。
- 湖仓侧的元数据优化不在此书射程，交给 ../Use_Iceberg_with_Spark/00-总览与阅读地图.md 那条线（隐藏分区/统计裁剪在引擎层之下的平行宇宙）。
- 中文生态位叙事：../bigdata/01-大数据技术全景.md。

## 2.2 RDD 并行计算模型（草案 2.2.1–2.2.6 ✅）

- **惰性求值 Lazy evaluation**：转换只记录 lineage，行动才执行。
  - 意义＝优化器获得全局视野（谓词/列裁剪跨算子合并的前提）；
  - 代价＝报错延迟（解析错误在第 8 个算子才爆）、重算放大（血缘越长恢复越贵）。⚠️＋ https://spark.apache.org/docs/latest/rdd-programming-guide.html ✅
- **内存持久化与内存管理**：cache/persist 与统一内存管理器。
  - executor 堆内分执行内存（shuffle/join/agg）与存储内存（cache blocks），共享一个池；
  - **存储侧可被执行侧挤出（eviction）**——"count 一样快、别人 OOM"的机制解释；
  - 参数族（spark.memory.fraction 等）以官方为准 ⚠️＋ https://spark.apache.org/docs/latest/configuration.html ✅
- **不可变性与 RDD 接口**：转换永远产新 RDD；lineage 是逻辑视图不是物化拷贝，"引用即视图"。
- **RDD 的类型**：映射类（窄）/逻辑聚合类（组合）/分区感知类（有 partitioner）——后续章"哪些操作免费、哪些收过路费"以此分类。
- **转换与行动**：只有 action 触发调度；同一 RDD 被多次 action＝潜在重复计算（07 章"重用 RDD"回收此伏笔）。
- **宽依赖与窄依赖**：窄＝父分区→子分区的固定函数（map/filter/union），宽＝按 key 重分布（groupBy/join/repartition）；**宽依赖是 shuffle 与 Stage 的唯一来源**。中文互证 ../bigdata/02-Spark核心与RDD模型.md。

## 2.3 作业调度（草案 2.3 ✅）

- 应用间资源分配：client/cluster 模式、动态分配（executor 随队列积压伸缩）、公平调度池。⚠️＋ https://spark.apache.org/docs/latest/job-scheduling.html ✅
- 应用解剖四层：Application → Job（每个 action 一个）→ Stage（每个 shuffle 边界一切）→ Task（每个分区一个）。
- 任务大小哲学：单任务 100ms–10min 经验区间——太小调度开销主导，太大倾斜风险高；这条经验值是 06 章并行度与 08 章分区器的公共前提。⚠️
- DAGScheduler 职责：把 RDD 图按 shuffle 切 Stage、拓扑排序提交 TaskSet；SchedulerBackend 管跨应用公平。⚠️ 转述口径。

## 2.4 Spark Job 剖析（草案 2.4.1–2.4.4 ✅；图示）

```
action(count)            action(show)
   │                        │
  Job-2                    Job-1
   ▼                        ▼
Stage-B(agg)  ←shuffle→ Stage-A(scan)     Stage-C 复用同谱系?
   每Stage内: Task×分区数                    (惰性=可能重复计算!)
```

- 读图三教训：
  1. shuffle 刀口数＝Stage 数−1＝分布式成本计数；
  2. 两个 action 可能把 Stage-A 算两遍（lineage 复用≠结果复用）；
  3. `spark.sql.shuffle.partitions`（默认 200）决定聚合后 Stage 形状，AQE 按运行时统计再合并。⚠️＋ https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅

## 2.5 🔧 E1 概念类比：限内存聚合与溢盘（非本书 Spark 引擎行为）

- 方法（可复现，脚本 `D:\develops\tmp\dbwave_w8_hps\exp.py`）：
  1. DuckDB 1.5.5，`SET threads=2; SET memory_limit='120MB'; SET temp_directory='.../duck_tmp.db'`；
  2. 造 1200 万行、800 万高基数分组，执行 `GROUP BY g SUM(r)`；
  3. 与放开到 4GB 的对照组比时。
- 实测（本机）：受限模式 **0.77s** 完成且结果正确、临时目录出现溢出文件；4GB 模式 0.89s——同数量级，该引擎溢盘路径很"便宜"。
- 映射到 Spark 的概念阶梯（⚠️ 转述）：缓存挤出 → 执行内存不足 → spill 排序文件 → 极端 OOM/重试放大 lineage 重算。
  - 差异提醒：Spark 的 spill 落在 JVM 序列化与多文件合并上，代价通常远高于单机引擎，且会叠加重试放大——**E1 数字只说明"溢盘阶梯存在且第一级几乎免费"这一概念，不外推**。
- 教学价值：内存参数讨论的正确抽象是"池＋优先级＋溢出阶梯"，不是背默认值。

## 2.6 常见误区

| 误区 | 正解（机理） |
|---|---|
| cache 后就不会重算 | 池被挤出即失效；长血缘该用 checkpoint（07 章） |
| 分区越多越并行 | 空任务调度税＋小文件输出（E1 阶梯的上游形态） |
| stage 多＝作业差 | shuffle 的写读合并才是账，Stage 数只是形状 |
| 动态分配总是省 | 冷启动税与 executor 抖动，短作业反而受伤 |

## 2.7 小结自检

1. 宽依赖三问：这个算子按什么分 key？切几个 Stage？shuffle 写出量多大？
2. cache 的块为什么会被执行内存挤掉？挤掉后再用会发生什么？
3. E1 里"溢盘几乎免费"的结论为什么不能直接搬到 Spark 集群？

## 2.8 互链

- 中文口径互证：../bigdata/02-Spark核心与RDD模型.md、../bigdata/03-Shuffle与宽依赖.md
- API/架构权威版：../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md
- 下文接棒：[07-高效转换算子](07-高效转换算子.md)（重用与内存）、[08-键值对数据与Shuffle](08-键值对数据与Shuffle.md)（分区器与倾斜）
- 部署运维视角：../bigdata/11-调度资源与运维.md

## 2.9 观测面小工具箱（接 10 章指标法）

- Stage 计数：宽依赖数＋1 是期望值——多出的 stage 都是不必要的 shuffle（2.4 Job 剖析的机制复现）。⚠️
- task 时长三件套 p50/p95/max：长尾分诊第一表；max/p50 超一个量级即按 08 章三查。⚠️
- shuffle 读写字节：map 端预聚合收益的直接可计量（对位 08 章 groupByKey 节）。⚠️
- GC 时间占比与 spill 记录数：内存阶梯的两只仪表——E1 的"120MB 挤出 spills、4GB 不挤"就是这双眼睛上的形状。🔧（**类比非 Spark**）
- Event Log 把以上全部变成可离线回放的证据链：忘开等于把事后调优退化成猜。⚠️＋ https://spark.apache.org/docs/latest/configuration.html ✅

## 2.10 执行形态三问（快速自检）

- 数据在动吗：跨节点 shuffle / 节点内序列化 / 落盘 spill——三种动法成本差一个量级。
- 时间在花在哪：计算 / 搬运 / 等待——等待段常被分区数与调度粒度藏起。
- 账单与直觉对上了吗：对不上处恰是本节学习入口。

## 核心概念速览（中英对照）

- **RDD** — Resilient Distributed Dataset：以 lineage 换容错的只读分区集合抽象，Spark 一切 API 的底座。
- **宽依赖/窄依赖** — Wide/narrow dependency：父→子分区映射是否跨节点重分布，决定 Stage 切分。
- **Shuffle** — Shuffle：宽依赖触发的全量重分布，写盘＋网络＋合并三大成本，性能分析第一现场。
- **统一内存管理器** — Unified memory manager：executor 堆内执行/存储共享池，带挤出与溢盘阶梯。
- **DAGScheduler** — DAG 调度器：把 RDD 依赖图按 shuffle 边界切成 Stage 并排序执行。
- **Task 粒度** — Task granularity：每分区一任务，100ms–10min 经验区间是并行度设计的锚。
- **动态分配** — Dynamic allocation：按队列积压伸缩 executor 的机制，共享集群友好但有冷启动税。
- **Lineage 重算** — Lineage recomputation：靠血缘重放丢失分区，容错便宜但链条长时放大灾难。
- **持久化级别** — StorageLevel：MEMORY_ONLY/DISK_ONLY 等权衡档位，OOM 与重算的兑换率。
- **shuffle.partitions** — SQL shuffle 并行度：默认 200，聚合 Stage 形状的第一旋钮，AQE 可再合并。
- **执行/存储内存** — Execution/Storage memory：共享池的两大租户，优先级与可驱逐性不同。

## 最新演进与工业实践

- **AQE 默认化（3.0+）**：合并多余 shuffle 分区、运行时改 Join 策略、倾斜分区拆分三件套，把本章"手工估并行度"的老功课大半自动化；官方条目 https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅（⚠️ 转述口径；Spark 4.2.0 文档为当前版，✅ 页头实抓）。
- **K8s 成为一等公民部署面**：https://spark.apache.org/docs/latest/running-on-kubernetes.html ✅；资源层口径从 YARN 队列转向 pod/executor 模板，"应用间资源分配"的现代形态。
- **工业实践共识**：排障顺序 UI→Stage 形状→shuffle 体量→内存阶梯，与本章地图一一对应；面试考点（宽窄依赖、Stage 划分、spill 机制）全部出自本章。
- **论文根基**：RDD 模型出自 HotCloud 2011《Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory MapReduce》（USENIX；⚠️ 无 DOI、原 legacy PDF 链接本轮 404，只给题＋会＋年）；可经 ../../db/db.md 书目线回溯。
- **内存模型演进**：堆外/堆内比例与 spill 策略随 3.x/4.x 多次再平衡，参数语义一律以 configuration 页 ✅ 当版为准，勿背他书旧值。
