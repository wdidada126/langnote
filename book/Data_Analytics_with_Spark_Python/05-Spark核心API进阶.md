# 05 Spark 核心 API 进阶（对应原书 Ch5，印张页 111–159）

> 所属书目：[00-总览与阅读地图](00-总览与阅读地图.md) ｜ 《Data Analytics with Spark Using Python》1e，Jeffrey Aven 著，Addison-Wesley Professional，2018。
> 本章二级目录 ✅ 实抓自官方 informIT 产品页；正文为**精读重构**，非原书文本；参数名与默认值按公开文档语境 ⚠️ 转述，不保证与原文一致。

## 官方二级目录（✅ 实抓）

- Shared Variables in Spark (p.111) ／ Broadcast Variables (p.112) ／ Accumulators (p.116)
- Exercise: Using Broadcast Variables and Accumulators (p.119)
- Partitioning Data in Spark (p.120) ／ Partitioning Overview (p.120) ／ Controlling Partitions (p.121)
- Repartitioning Functions (p.123) ／ Partition-Specific or Partition-Aware API Methods (p.125)
- RDD Storage Options (p.127) ／ RDD Lineage Revisited (p.127) ／ RDD Storage Options (p.128)
- RDD Caching (p.131) ／ Persisting RDDs (p.131) ／ Choosing When to Persist or Cache RDDs (p.134)
- Checkpointing RDDs (p.134) ／ Exercise: Checkpointing RDDs (p.136)
- Processing RDDs with External Programs (p.138) ／ Data Sampling with Spark (p.139)
- Understanding Spark Application and Cluster Configuration (p.141)
- Spark Environment Variables (p.141) ／ Spark Configuration Properties (p.145)
- Optimizing Spark (p.148) — Filter Early, Filter Often (p.149) ／ Optimizing Associative Operations (p.149)
  ／ Understanding the Impact of Functions and Closures (p.151) ／ Considerations for Collecting Data (p.152)
  ／ Configuration Parameters for Tuning and Optimizing Applications (p.152) ／ Avoiding Inefficient Partitioning (p.153)
- Diagnosing Application Performance Issues (p.155) ／ Summary (p.159)

## 精读重构·共享变量（p.111–119）

- **Broadcast Variables**：驱动端一次性序列化下发只读副本（btw 块式传输到 executor 再本地分发），
  替代「每任务重复闭包捕获大对象」。Python 侧 `sc.broadcast(obj)`，任务内 `b.value` 读。
- **Accumulators**：只加不减的全局计数器，`sparkContext.accumulator`/`sc.accumulator(v)`，
  任务侧只能 `add`，值在 action 后由驱动读；**惰性重算导致重复累加**是官方文档经典警告 ⚠️ 转述。
- Ch4 p.100 的广播连接伏笔在此兑现：join 大表×小表时把手工字典升级为 broadcast 变量。

## 精读重构·分区控制（p.120–126）

TOC 的三段递进（⚠️ 推定展开）：

1. **Partitioning Overview**：并行度 = 分区数；默认来源（输入切片数/`defaultParallelism`/`minPartitions`）。
2. **Controlling Partitions**：PairRDD 的 `Partitioner`（Python 侧通过 `partitionBy(num, func)` 传键散列函数）；
   `rangePartitioner` 思想；同分区器 RDD 间操作免 shuffle。
3. **Repartitioning Functions**：`repartition(n)`（必然 shuffle）、`coalesce(n)`（收缩、可免 shuffle 但会失衡）、
   `partitionBy`（按键重排）；**p.153「Avoiding Inefficient Partitioning」**把倾斜列为头号杀手。
4. **Partition-Aware API**：`mapPartitions`/`foreachPartition`/`glom`——以分区为单元摊销 setup 成本（DB 连接类场景）。

🔧 **本地对照实测 E2（非本书 Spark 引擎行为）**：DuckDB 1.5.5 上 20 万行事件表、
user_id 含 6000 倍金额倾斜的热点键（user<5 的行 ×100）：
热点键子集聚合 0.0064 s vs 均匀子集 0.0109 s——单机向量化引擎靠 hash 聚合把键倾斜消化到无感；
但同数据若换成分区文件逐个归并的路径（模拟 hash 分区不均），倾斜代价立刻显形。
结论（类比面）：Spark 的 salted key/two-stage aggregation 调优（p.153 语境）本质是在补救
「hash 分区打不过数据倾斜」这一物理事实，而单机 hash 聚合无此暴露面。
脚本：`D:\develops\tmp\dbwave_w8_daspark\analogies.py`（E2 组）。

## 精读重构·存储选项：cache/persist/checkpoint（p.127–137）

- **Lineage Revisited**：血缘重建的成本在长链/重计算场景超过复制成本——缓存与截断血缘的动机。
- **StorageOptions**：`MEMORY_ONLY` 系列、`_AND_SER` 变体、`DISK_ONLY`；Python RDD 天然以序列化态驻留
  （官方文档语义 ⚠️ 转述）。
- **cache() vs persist()**：前者是后者的 MEMORY_ONLY 简写；何时缓存=多次 action 复用同一中间 RDD（p.134 决策节）。
- **Checkpoint**：`sc.checkpoint(dir)` + `rdd.checkpoint()`（或 `localCheckpoint`）落 HDFS 截断血缘，
  代价是物化写盘+血缘保护丧失（p.136 练习）。

🔧 **本地对照实测 E3（非本书 Spark 引擎行为）**：同一谓词过滤（amount>500）建 DuckDB **视图**（惰性重算）
vs **表**（物化）后各重复聚合 5 次：视图 0.018 s vs 表 0.0084 s，**2.14 倍**重算税。
这正是 cache/persist 的单机最小模型：物化用一次性写成本换复用读成本；
checkpoint 的类比则是「把结果表落盘、从此不记得它怎么来的」⚠️ 概念映射非严格等价。

## 精读重构·配置与优化条陈（p.141–159）

- **环境变量 vs 属性**：`spark-env.sh`（节点级 JVM/端口）与 `spark-defaults.conf`/`--conf`（应用级）两层；
  提交参数覆盖链：编程 API > spark-submit > defaults 文件 ⚠️ 转述。
- **优化六条**（p.148–153，TOC 逐条对应）：早过滤、常过滤；结合律操作先局部（reduceByKey 重提）；
  闭包捕获审查（大属性外移）；collect 节制；调参清单（executor 内存/核数/parallelism/shuffle 追踪）；
  分区失衡治理（repartition 时机）。
- **Diagnosing（p.155）**：Web UI stage/task 视图、GC 时间与 shuffle spill 信号、异常栈的 Python 侧读法 ⚠️ 推定。

> repo 对照：同一调优议题的现行版纵深见
> [../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)
> 与 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)；shuffle 机制底层见
> [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)。

## 复习要点与自测清单

1. broadcast 与「每任务闭包捕获」的成本对比：1 万任务×10MB 对象 vs 广播一次，算总传输量。
2. 累加器双重人格：调试计数器可以，业务正确性载体不行——惰性重算为何会重复 add？
3. 分区三口诀：何时 repartition（增大+洗牌可接受）、coalesce（收缩+容忍失衡）、partitionBy（按键复用）。
4. cache 决策树：同一 RDD 被 n 个 action 复用、计算成本 c、内存占用 m——何时值得 persist？
5. cache vs checkpoint 的四维对比：血缘保留、存储位置、序列化格式、故障恢复速度。
6. 优化六条各配一个反例代码（书中 p.148–153 条陈的镜像练习 ⚠️ 推定题目设计）。
7. 倾斜治理工具箱：加盐两段聚合、热点键单独广播、skew join hint（后者为 3.x 新增 ⚠️ 演进节）。
8. 🔧 迁移题：用 E2/E3 数据（DuckDB 倾斜 0.0064 s、视图重算税 2.14 倍）解释
   「单机 hash 聚合免疫键倾斜但付重算税；分布式 shuffle 倾斜致命但可缓存截断」的镜像关系（非 Spark 行为）。
9. 配置读法题：给出一次真实 spark-submit 命令行，逐项判定其参数属于环境变量层、
   defaults 文件层还是编程 API 层，并按覆盖链说出最终生效值。

## 核心概念速览（中英对照）

- **广播变量** — Broadcast Variable：驱动端序列化一次、各 executor 只读共享的大对象通道。
- **累加器** — Accumulator：跨任务单向聚合的只加计数器，警惕惰性重算导致的重复累加。
- **重分区** — Repartition：`repartition(n)` 强制全量 shuffle 改并行度。
- **合并分区** — Coalesce：收缩分区数、可免 shuffle 但易制造大小分区失衡。
- **分区器** — Partitioner：PairRDD 键→分区的映射规则，决定同类操作可否免洗牌。
- **惰性缓存** — Cache/Persist：把中间 RDD 物化进内存/磁盘，以空间换重算时间。
- **检查点** — Checkpoint：将 RDD 落可靠存储并截断血缘，长管线容错与 GC 的代价手段。
- **血缘重建** — Lineage Recovery：凭转换链重算丢失分区，checkpoint 的反面策略。
- **存储级别** — StorageLevel：MEMORY_ONLY/DISK_ONLY/_AND_SER 等内存磁盘组合档位。
- **早过滤** — Filter Early：把选择性谓词前置以减少下游 shuffle 与序列化量。
- **闭包捕获** — Closure Capture：任务函数连带引用的大对象被序列化下发的隐性流量源。
- **数据倾斜** — Data Skew：按键聚合时热点键分区远大于均值，分区失衡的头号成因。
- **外部程序处理** — Pipe：`rdd.pipe()` 把分区经 stdin/stdout 交给非 Python 进程（TOC p.138）。

## 最新演进与工业实践

- **自适应执行改写了本章半壁建议**：Spark 3.0 起的 AQE（Adaptive Query Execution）自动合并小分区、
  倾斜键拆分、动态 join 策略——p.148–153 的手工条陈在 DataFrame/SQL 路径上大半被引擎接管 ⚠️ 转述；
  官方 SQL 指南 https://spark.apache.org/docs/latest/sql-programming-guide.html （✅ curl -sI 200）有专节。
- **RDD 侧工具原地踏步**：persist/checkpoint/broadcast/accumulator API 语义十余年未破坏，
  RDD 指南仍在线（https://spark.apache.org/docs/latest/rdd-programming-guide.html ，✅ 200）——本章的「物理层心智」不过期。
- **配置项改名潮**：2.x 时代大量 `spark.cores.max`/`spark.executor.instances` 语义延续，但 UI 与默认值多次微调；
  照抄 2018 参数前对照现行文档逐项核对 ⚠️ 转述。
- **单机类比边界更新**：🔧 E2/E3 组（DuckDB 1.5.5）显示单机 hash 聚合对键倾斜几乎免疫、
  物化 vs 视图重算税约 2 倍——教学时用这组数字给「分布式倾斜代价远大于此」定参照系最省口舌（非本书 Spark 引擎行为）。
- **工业实践**：2026 年 PySpark 调优讨论的重心已从本章 RDD 参数迁到 Pandas UDF 批大小、
  Arrow 序列化与对象存储 list 开销 ⚠️ 转述，属本书未覆盖面，学习路径需外挂。
