# 02 Spark 核心与 RDD 模型：从弹性数据集到 DAG 调度

> **本章地图**：**RDD 是什么**（不可变 + 分区 + 血缘）→ **两类算子**（转换 / 行动）与惰性求值 → **DAG 构建与 stage 划分**（窄依赖 vs. 宽依赖）→ **Task 调度与执行**（worker、shuffle service、Triton）→ **为什么 RDD 在 2020 年代被 Dataset 取代**（类型安全、Catalyst、Tungsten）→ 2026 年的现实：Structured Streaming 与 Spark 4.x。
> **主要支撑**：《Spark 大数据实时计算：基于 Scala 开发实战》**第 6 章（Spark Core 编程）与第 7 章（Spark Core 运行原理）**。这是全书最硬的两章，也是本目录技术深度最高的部分。
> **交叉**：本章的调度思想与 `book/多处理器编程的艺术2/16-调度与工作分配.md` 同源。

---

## 一、本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 | RDD 的五个属性 | 「不可变 + 分区 + 血缘」三件套决定了 Spark 的一切 |
| 2.2 | 转换 / 行动与惰性求值 | 只有行动算子才会触发一次从数据源开始的**重新计算** |
| 2.3 | 宽窄依赖与 stage 划分 | `map`/`filter` 是窄依赖，`reduceByKey`/`join` 是宽依赖；stage 边界 = 宽依赖 |
| 2.4 | 任务调度与执行 | DAGScheduler → TaskScheduler → Executor；**推测执行**与**本地性** |
| 2.5 | RDD 的代价与替代 | 序列化、GC、无类型安全 → DataFrame/Dataset |
| 2.6 | 2026 的现实 | Structured Streaming 之上没有 RDD；Spark 4.x 的走向 |

---

## 二、核心精讲

### 2.1 RDD 的五个属性（读 Spark 源码的顺序）

 academy 版本的教材常把 RDD 定义成「弹性分布式数据集」一句话带过，但真正理解 Spark 源码，需要记住 RDD 里的**五个字段**（`org.apache.spark.rdd.RDD`）：

```scala
// 教学示意，不参与构建；仅摘录 RDD 抽象中最关键的字段与语义
abstract class RDD[T] extends Serializable with Logging {
  def getPartitions: Array[Partition]          // ① 分区：数据被切成几块、每块的描述
  def dependencies: Seq[Dependency[_]]         // ② 血缘（lineage）：父 RDD 与依赖类型
  def compute(split: Partition, context: TaskContext): Iterator[T] // ③ 如何在一个分区上算出来
  val partitioner: Option[Partitioner]         // ④ 是否按 key 分区（决定 shuffle 代价）
  def preferredLocations(split: Partition): Seq[HostName] // ⑤ 数据本地性
}
```

1. **分区（partitions）**：一个 RDD 逻辑上是**一个不可变的、元素按分区切分的数据集**；物理上它只是「一堆分区的描述」，分区里的数据**不一定**已经在内存里。
2. **不可变**：任何转换都**产生新 RDD**，绝不在原 RDD 上原地改。这是「缓存失效可预测」的前提，也是 Spark 能在节点失败时**重算而不是回滚**的前提。
3. **血缘（lineage / dependencies）**：只记录「这个 RDD 是怎么算出来的」，**不存数据**。
4. **compute**：**「一个分区丢了就靠 compute 重算」**，不需要写任何日志。
5. **Partitioner 与 preferredLocations**：前者决定宽依赖的代价，后者决定调度往哪儿放任务。

> **一句话记住 RDD**：**「数据算过之后不再存在；丢了就靠血缘重算」**。这是 Spark 与 MapReduce 最大的差别——MapReduce 没有 lineage，失败就要从 job 起点重跑。

### 2.2 转换 / 行动与惰性求值

```scala
// 教学示意，不参与构建；不是可提交作业
val base: RDD[(String, Int)] = sc.textFile("hdfs://.../access.log")   // 读文件 = RDD
  .map(line => parse(line))                                            // 转换：不执行
  .filter(_.status == 200)                                             // 转换：不执行
  .map(r => (r.uid, 1))                                                // 转换：不执行
  .reduceByKey(_ + _).sortBy(_._2, ascending = false)                  // 宽依赖 + 排序：都不执行

val top: Array[(String, Int)] = base.take(10)                          // 行动：这一行才开始算
```

- **惰性求值的关键推论**：`map`/`filter`/`reduceByKey` 都是「只记血缘」，Action 才触发。因此：
  - 同一段代码里放两个 action，会**算两遍**（除非用了 `cache`/`persist`）；
  - `cache()` 是**懒执行**的（没有 action 就什么都不会发生），这一点两本教材都提过但容易被忽略；
  - 在 action 之间如果想复用数据，只在中间 `cache` **一次**，且不要忘记 ** interchangeable 的序列化级别**。
- **共享变量**：`broadcast`（只读、跨节点只读一份、适合小维表）与 `accumulator`（只增、跨 executor 累加）。注意：**accumulator 的结果在 action 里才可靠**，不能用它做控制流。

### 2.3 宽窄依赖与 stage 划分

| 依赖类型 | 子分区与父分区的关系 | 算子 | stage 内？ | shuffle 代价 |
| --- | --- | --- | --- | --- |
| **窄依赖 NarrowDependency** | 每个子分区只依赖**一个**父分区（1:1 / n:1） | `map`、`filter`、`union`、`coalesce`（小范围） | **同 stage** | 无 |
| **宽依赖 ShuffleDependency** | 每个子分区依赖**多个（或全部）**父分区 | `reduceByKey`、`groupByKey`、`join`、`distinct`、`sortBy` | **stage 边界** | 有 |

```scala
// 教学示意，不参与构建；用一个极简的 DAG 描述 stage 划分
val a = sc.makeRDD(1 to 4, 4)                 // 4 个分区
val b = a.map(_ * 2)                          // 窄依赖：map
val c = b.filter(_ > 3)                        // 窄依赖：filter
val d = c.map(x => (x % 2, x))                // 窄依赖
val e = d.reduceByKey(_ + _)                  // 宽依赖：此处切断
// 最终 stage：S1[makeRDD→map→filter→map]│S2[reduceByKey]
```

- **stage 划分规则**：从后向前回溯血缘，**遇到宽依赖就切一刀**。所以一段代码里有几个宽依赖，就有几段 stage。
- **stage 内可以流水线执行**：窄依赖链上的算子会合并成一个 **pipeline**，在**同一个 task 里连续执行**，中间不落盘。这是 Spark 快于 MapReduce 的核心原因之一（MapReduce 的每个阶段都要落盘）。
- **shuffle 中「不落盘的例外」**：在 Spark 3.x 之后，`map-side combine`（如 `reduceByKey` 在 map 端先本地聚合）会大幅减少写流量，但 shuffle 文件仍要经过 **External Shuffle Service**。
- **Pipeline 与本地性的关系**：`preferredLocations` 决定 task 优先跑在哪个 executor 上；调度器会按 **PROCESS_LOCAL → NODE_LOCAL → RACK_LOCAL → ANY** 的偏好降级。

### 2.4 任务调度与执行

```
[DAG创建]  RDD 图
   │
   ▼
[DAGScheduler]  按宽依赖切 stage，为每个 stage 生成 TaskSet（每个分区一个 task）
   │
   ▼
[TaskScheduler] 把 TaskSet 交给 SchedulerBackend，按本地性 + 延迟调度到 Executor
   │
   ▼
[Executor]  线程池执行 task；shuffle 写/读走 Shuffle Service（或 process-local 直连）
```

- **stage 级别的调度优化**：**skip stage**（某 stage 的所有 task 都跑了，其他 stage 的依赖就免了）、**推测执行 speculation**（慢节点上重跑同一 task，取先完成的那个结果）——注意推测执行只在 **stage 可重复、结果幂等**时安全。
- **为什么 shuffle 阶段要落到磁盘**：宽依赖要按 key 重排出，"按 key 排序后的数据" 需要稳定存储，因而 shuffle 期间会产生大量网络与磁盘 I/O。**shuffle 是 Spark 作业慢的第一原因**（详见 `03`）。

### 2.5 RDD 的代价与为什么它被 Dataset 取代

| 问题 | 表现 | 解法 |
| --- | --- | --- |
| 序列化开销 | Java/Scala 对象序列化贵，网络与堆内存压力大 | Kryo 序列化器、Tungsten 的 off-heap **整段编码（whole-stage codegen）** |
| GC 压力 | 大量小对象在堆上 → GC 占掉 30%+ 时间 | off-heap 存储、减少小对象 |
| 无类型安全 / 无优化空间 | `rdd.map(x => x)` 里 x 的类型只有你在写；优化器无从下手 | Dataset/DataFrame 有 **schema**，Catalyst 才能优化 |
| 无 SQL 生态 | 无法直接写 SQL | `SparkSession.sql()` 直接复用 |

**因此 Spark 2.x 之后的推荐写法已经明确**：**优先写 Dataset/DataFrame，把 RDD 留给真的需要手写算子的场景**。《Spark 大数据实时计算》第 8–9 章讲 Spark SQL 时正是这个转向。

> 🔧 **2026 的现实补充**：Spark 3.x 之后，用户层几乎不再直接写 RDD；RDD 主要活在两处——① 引擎内部（DAG、shuffle、Broadcast join 的实现仍建立在 RDD 之上）；② 需要自定义 `PairRDDFunctions` 之外的控制流时。因此本目录建议：**读《Spark 大数据实时计算》第 6 章建立模型，用第 8–9 章的方式写代码**。

### 2.6 版本演进

| 版本 | 关键变化 |
| --- | --- |
| 1.x | RDD、DStream、Broadcast；shuffle 落盘 |
| 2.0 | **Tungsten**（堆外、代码生成）、**Structured Streaming**（`spark.sql` 上的流）、Dataset API 稳定 |
| 2.1–2.4 | **`spark.sql.ansi.enabled`** 雏形、`broadcast join` 的 AQE 雏形、Python/PySpark 增强 |
| 3.0 | **Adaptive Query Execution(AQE)** 引入、`spark.sql.ansi.enabled` 成为正式配置项、Python 类型提示 |
| 3.1–3.3 | **动态分区裁剪 DPP**、SPIP（SPark Improvement Proposal）机制落地、ANSI 模式逐步完善、Photon 部分能力贡献 |
| 4.0（进行中） | ANSI **默认**开启（与标准 SQL 对齐，`'1' + 2` 从隐式转换变成报错）、**SI（Spark Improvement）** 规范化的演进路径；对老代码的最大冲击是「以前能跑的隐式转换现在会失败」 |

---

## 三、核心精讲（续）：教学示意代码

```scala
// 教学示意，不参与构建；以下是「血缘可视化」的等价伪代码，不是可运行程序
// 目的：说明 stage 与 task 的数量关系，不要试图编译
object LineageTeaching {
  // 一个 stage = 一组可以流水线执行的窄依赖
  case class Stage(id: Int, tasks: Int, parents: Seq[Int], shuffle: Boolean)

  def buildStageGraph(root: /* RDD[_] */ Any): Map[Int, Stage] = {
    var counter  = 0
    val stages   = scala.collection.mutable.Map.empty[Int, Stage]
    def visit(rdd: /* RDD[_] */ Any): Int = {
      if (rdd 宽依赖链已访问) return 已缓存的 stage id
      val hasWide = 该 rdd 的依赖里存在 ShuffleDependency
      if (!hasWide) {
        // 与下游合并；这里简化处理
        val parent = 父 rdd 的 stage id
        counter += 1
        stages(counter) = Stage(counter, 分区数, Seq(parent), shuffle = false)
        counter
      } else {
        counter += 1
        stages(counter) = Stage(counter, 分区数, 父 stage 列表, shuffle = true)
        counter
      }
    }
    visit(root); stages.toMap
  }
}
```

> **不要真的跑它**，它的价值只在说明「stage 数量 = 宽依赖数量 + 1」。真正要看的是 Spark UI 里 **Stages** 标签页的 `Shuffle Read/Write` 与 `Task` 分布。

---

## 四、经典论文与原始文献

| 论文 | 出处 | 与本节的联系 |
| --- | --- | --- |
| Zaharia、Mosharaf、Chowdhury、Franklin、Stoica、Zaharia，*Spark: Cluster Computing with Working Sets* | **HotCloud 2010** | RDD 的原始构想：能复用工作集的集群计算 |
| Zaharia 等，*Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing* | **SOSP 2013** | **血缘 + 重计算 = 容错**；本章 2.1 节的五个属性即论文核心 |
| Zaharia 等，*Distributed Stream Processing with Spark Streaming* | **SOSP 2013** | 微批（DStream）路线 |
| Armbrust 等，*Spark SQL: Relational Data Processing in Spark* | **SIGMOD 2014** | Dataset/DataFrame 的由来，2.5 节「为什么取代 RDD」的出处 |
| Zaharia 等，*Fast and Interactive Analytics over Data Fabric: Photon...*（见 SIGMOD 2024） | SIGMOD 2024 | Photon 引擎的公开论文（详见 `10`） |

---

## 五、近年研究与工业界开源实践（2015–2026）

**研究侧**：

- **编译执行与向量化**：Spark 3.x 的 **Whole-Stage Java Codegen** 与 **Volcano-style 向量化**（`spark.sql.codegen.wholeStage`、向量化读 Parquet）之争，最终两条路都留下了：OLAP 小批量用向量化、复杂表达式用代码生成。
- **调度理论**：Spark 的调度与 **DAG 上的贪心调度定理**同源，可对照 `book/多处理器编程的艺术2/16-调度与工作分配.md` 的 `T₁/P + T∞` 界理解。
- **shuffle 与存储**：从 Spark 1.x 的 hash shuffle → 2.x 的 sort shuffle → 3.x 的 **Push-based Shuffle / Combined shuffle write**（减少小文件与小请求），shuffle 的研究重心是「**减少网络往返与连接数**」。
- **容错**：推测执行与 **reliable execution** 的形式化；以及 **straggler 归因**（用 HdrHistogram 看尾延迟）。

**工业界开源（star 数为 2026-09-25 用 `gh api` 实测）**：

| 项目 | star | 与本节的联系 |
| --- | --- | --- |
| `apache/spark` | **44036** | 本章的全部对象；`RDD`、`DAGScheduler`、`TaskScheduler` 都在其中 |
| `apache/flink` | **26362** | 对偶实现：Flink 用 `StreamGraph`/`JobGraph` + slot 共享，思路与 stage 划分同构 |
| `facebook/rocksdb` | **32131** | Spark 3.2+ 的 shuffle 部分场景与状态后端依赖 LSM；Flink 的状态后端也用它 |
| `apache/kubernetes` | **127976** | Spark on K8s 的底座（详见 `11`） |
| `apache/iceberg` | **9271** | Spark 写入的开放表格式（详见 `09`、`10`） |

**工程建议（可直接照做的清单）**：

1. 打开 Spark UI 的 **Stages** 页，对每个 stage 看两列：`Tasks`（是否远超核心数）、`Shuffle Read Size`（是否超过你预期的一个数量级）。
2. 若 `Tasks` 数是 2000 而数据量只有几 GB，说明并行度设高了 → 用 `spark.default.parallelism` 或 `repartition` 降下来。
3. 若某个 stage 的 shuffle 写是 TB 级，先找是不是 **`groupByKey` 而不是 `reduceByKey`**（key 数量大时 `reduceByKey` 的 map 端预聚合能省一个数量级）。
4. 只有在确实需要手写算子时才写 RDD；否则用 Dataset。

---

## 六、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | 「RDD 是分布在内存里的数据集，所以 Spark 是内存计算」 | RDD **只是逻辑上的分区描述**；数据可以不在内存（ spills to disk）、也可以被淘汰（**弹性**二字的来源）。`cache` 失败时按血缘重算 | 《Spark 大数据实时计算》第 6 章 |
| 2 | 「`cache()` 之后数据就在内存里了」 | `cache` 是**惰性**的；没有后续 action，什么都没发生 | 《Spark 大数据实时计算》第 6 章 |
| 3 | 「血缘可以替换缓存」 | 血缘重算的**代价远高于缓存**；血缘只能用于**容错**，不能用于「复用」。复用必须用 `cache`/`broadcast` | 《Spark 大数据实时计算》第 7 章 |
| 4 | 「宽依赖 = 慢，窄依赖 = 快，所以少用宽依赖」 | 宽依赖是**必需的**（按 key 聚合、按 key join 总要搬数据）；优化方向是减少 shuffle 的**数据量与请求数**（map 端预聚合、broadcast join、避免 `groupByKey`） | 《Spark 大数据实时计算》第 7 章 + 《离线》第 5 章 |
| 5 | 🔧 「新代码应该直接写 RDD」 | Spark 2.x 之后官方推荐 **Dataset/DataFrame**；RDD 只在需要细粒度控制时使用。本书第 6 章之后立刻用第 8–9 章写法，正是这个转向 | 《Spark 大数据实时计算》第 6 章（倾向 RDD）vs 第 8 章（转向 Dataset） |
| 6 | 🔧 本书未覆盖 **Structured Streaming 与 DStream 的关系** | 本书第 10 章讲 DStream；2026 年的流式 API 是 **Structured Streaming**（`writeStream` + watermark + 状态存储）。DStream 仍在维护但不再是新项目首选 | 《Spark 大数据实时计算》第 10 章 DStream |
| 7 | 🔧 本书未覆盖 **Spark 3.x/4.x 的 ANSI 模式对 RDD 之外语义的影响** | ANSI 开启后 `'2' + 1` 从隐式转换变报错、` CAST` 行为变化；从 Spark 2.x 迁到 4.x 的老 SQL 会「运行得更慢」或「直接失败」 | 《Spark 大数据实时计算》第 8–9 章；详见 `04`、`10` |
| 8 | 🔧 本书未覆盖 **推测执行在某些作业上反而更慢** | 推测执行会额外消耗资源、在 IO 密集作业上放大负载；2026 年的常见做法是关掉 speculation 而改用**队列隔离 + 性能基线** | 《Spark 大数据实时计算》第 7 章提到推测执行但未给出适用边界 |

---

## 七、与其他章 / 其他书的联系

**本目录内部**：

- **`03-Shuffle与宽依赖.md`**：本章 2.3 节只说「宽依赖切 stage」，`03` 把「宽依赖到底要搬什么、怎么搬、怎么不搬」讲透。
- **`04-SparkSQL与结构化数据.md`**：RDD 之后 Spark 的正式形态；Catalyst 优化器、**Tungsten** 的执行层都在 `04`。
- **`05-Spark性能优化.md`**：本章 2.5 节的序列化/GC 问题在 `05` 中展开为可执行的调优清单。
- **`07-实时计算与流式架构.md`**：DStream 属于 Spark 的流侧，其架构位置在 `07` 讨论。
- **`11-调度资源与运维.md`**：本章 2.4 节的调度在 K8s/YARN 上的形态在 `11`。

**其他书**：

- **`book/多处理器编程的艺术2/16-调度与工作分配.md`**：**强烈对照阅读**。Spark 的 stage→task 调度（本地性降级、推测执行）是**分布式**版本的调度；该书第 16 章讲的 Chase-Lev 双端队列与 `T₁/P + T∞` 贪心界是**单机**版本的实现细节。两者是同一个思想的两层。
- **`book/数据库系统概念6/13-查询优化.md`**：Spark 的 stage 划分在概念上等价于数据库的 **operator tree 切块 + 流水执行**；Catalyst 的优化规则与数据库的逻辑/物理算子改写同源（详见 `04`）。
- **`book/数据库系统概念6/26-高级事务处理.md`**：RDD 的「按血缘重算」= 一个**无锁的、确定性的重执行恢复模型**，与 WAL 的重放不同（不需要日志，因为输入是确定的）。
- **`book/Linux内核完全剖析/13-内存管理.md`**：`cache`/`persist` 的 off-heap 与页缓存交互、shuffle 落盘的 page cache 行为，都落在这层。
- **`book/软件架构设计/08-高并发问题.md`**：推测执行与本地性降级本质是「排队 + 超时重试 + 冗余请求」。
