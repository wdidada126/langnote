# 05 Spark 性能优化：内存、GC、并行度、倾斜与调优清单

> **本章地图**：**先定位再优化**（看 UI 而不是猜）→ **内存管理**（executor 内存区域划分、Tungsten off-heap）→ **GC 调优** → **并行度与 shuffle 分区** → **join 策略与倾斜** → **数据倾斜与结构调整** → **序列化与数据局部性** → **2026 的现代调优面**（AQE、自适应、对象存储上的 I/O）。
> **主要支撑**：《Spark 大数据实时计算：基于 Scala 开发实战》第 7 章（运行原理，含部分调优）；《离线和实时大数据开发实战》**第 5 章「Hive优化实践」**（该书把倾斜治理写得很细，正好与 Spark 调优互为方法论）。

---

## 一、本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 | 优化的顺序 | **先诊断后优化**；90% 的收益来自 3 个开关 |
| 5.2 | Executor 内存模型 | `spark.executor.memory` 如何被切成 storage / execution / user 三块 |
| 5.3 | GC 调优 | 减少对象分配比换收集器更有效 |
| 5.4 | 并行度与 shuffle 分区 | 单个 task 处理 128MB–1GB 是经验区间 |
| 5.5 | join 策略与倾斜治理 | broadcast > 打散 > 过滤；AQE 可自动 |
| 5.6 | 序列化与数据布局 | Kryo、列存、减少小文件 |
| 5.7 | 2026 的现代调优 | AQE、DPP、对象存储 I/O、存算分离下的调优变化 |

---

## 二、核心精讲

### 5.1 优化的顺序（先看这张表再动手）

| 顺序 | 检查项 | 常见症状 | 手段 |
| --- | --- | --- | --- |
| 1 | 是否在扫全表 | `explain` 里没有 `PushedFilters`；stage 输入远大于表大小 | 开谓词下推、列裁剪、DPP、分区裁剪 |
| 2 | 是否有 shuffle 倾斜 | 个别 task 时间远高于中位数 | broadcast join / 打散 / AQE |
| 3 | 并行度是否合理 | task 数几千而数据很小，或 task 数过少导致单 task 超长 | `spark.sql.shuffle.partitions` / `spark.default.parallelism` |
| 4 | 是否重复计算同一份数据 | 多个 action 各算一遍 | 中间 `cache`/`persist`（**一次**） |
| 5 | GC 是否占时间 | Stage 页里 `Shuffle Spill (memory)` 与 GC 时间占比高 | 减少对象、增大 executor、换 GC |
| 6 | 数据是否太小以致 JVM 开销大 | 小数据集跑很久 | 降并行度、用 local 模式调试 |

> **核心原则**：**先做「减少数据移动」，再做「减少对象分配」，最后才是「调 GC 和内存」。** 很多工程师一上来就换 G1、调 `ExecutorMemory`，但真正的问题是「这段 SQL 不该 shuffle 200GB」。

### 5.2 Executor 内存模型

Spark 的 executor 内存统一由 `spark.executor.memory`（或 K8s 上的 `spark.kubernetes.executor.limit`）指定，**逻辑上**分成：

```
┌───────────────────── spark.executor.memory ─────────────────────┐
│                                                                  │
│  ┌────────── storage (缓存 RDD/DataFrame) ────────────────────┐  │
│  │  spark.memory.storageFraction（默认 0.6）                   │  │
│  ├────────── execution (shuffle、sort、join 的内存) ───────────┤  │
│  │  spark.memory.fraction × (1 - storageFraction)              │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  └──── user memory（算子代码、用户对象的分配）                   │  │
└──────────────────────────────────────────────────────────────────┘
```

- **Unified Memory Manager（Spark 1.6+）**：storage 与 execution 之间的边界是**动态的**（execution 需要时可以从 storage 借），所以不必为了缓存而牺牲 shuffle。
- **Tungsten 的 off-heap**：shuffle、sort、join 的数据以 `UnsafeRow` 形式存在堆外，于是**GC 不扫它们**；代价是需要自己管理内存溢出（`spill`）。
- **调优要点**：
  - executor **不要设太大**（常见错误：一个 executor 40GB）。大的 executor = 长 GC pause + 单点故障代价高（一个挂掉要重跑一个大 task）。
  - 经验值：executor 内存 **8–16GB**、core **4–8 个**，`spark.executor.cores × spark.executor.memory` 之间保持「每 core 2–4GB」的比例。
  - GC 占比超过 **10%** 就要管，超过 **30%** 说明有系统在性问题。

```scala
// 教学示意，不参与构建；缓存级别的选择（错误示范 vs 正确示范）
// 错误：对会被 lineage 重算的数据反复 cache，且不指定级别
df.cache()                                  // 默认只有 MEMORY_ONLY，可能丢一次

// 正确：明确级别与序列化（数据量大时 MEMORY_ONLY_SER 更省内存但更慢反序列化）
import org.apache.spark.storage.StorageLevel
val cached = df.persist(StorageLevel.MEMORY_ONLY_SER)
cached.count()                              // 触发一次，后续 action 复用
```

### 5.3 GC 调优

**先做这三件事，比换收集器有效**：

1. **减少对象分配**：避免在算子里 `new` 大对象、避免字符串拼接、避免 `Option` 嵌套；能用 primitive 就不用 tuple 装箱。
2. **让 shuffle 走 off-heap**（Tungsten 默认会做一部分），减少堆上压力。
3. **用 Kryo 序列化器**（`spark.serializer=org.apache.spark.serializer.KryoSerializer`），显著减少序列化后的字节数。

**换收集器的场景**：

| 情况 | 建议 |
| --- | --- |
| 对象多、存活短、年轻代频繁 Full GC | 增大新生代（`spark.executor.newMemoryRatio` / 老式 `-Xmn`） |
| 大堆 + 长 pause 不可接受 | 用 G1（Spark 3.x 默认已是 G1 友好配置） |
| 频繁 full GC 且堆已很大 | 检查是否有数据倾斜导致单个 executor 要装 TB 级数据 → **倾斜优先** |

> **反直觉但重要**：GC 调优常常无效，因为**慢的原因不是 GC，是 shuffle**。先确认「是不是倾斜」，再动 GC。

### 5.4 并行度与 shuffle 分区

```scala
// 教学示意，不参与构建；设置并行度的三种位置（优先级从低到高）
// 1) 集群级默认
spark.conf.set("spark.sql.shuffle.partitions", "400")
spark.conf.set("spark.default.parallelism", "200")        // RDD 侧

// 2) 作业级（最常用）
spark.conf.set("spark.sql.shuffle.partitions", "1000")

// 3) 算子级（最灵活）
val repartitioned = df.repartition(1000)                  // 重分区，会 shuffle
val coalesced = wide.repartition(400).coalesce(100)       // coalesce 只在下游合并时便宜
```

- **经验区间**：每个 task 处理 **128MB–1GB** 数据。数据 1TB → 分区数 1000 左右；数据 10GB → 分区数 100 左右。
- **太大**的后果：task 启动与调度开销、shuffle 文件/请求数爆炸、小文件。
- **太小**的后果：单 task 跑太久、集群利用不足、倾斜更难缓解。
- **AQE 会自适应合并**：Spark 3.x 下 `spark.sql.shuffle.partitions=200` 配 AQE，运行时会按目标大小（默认 128MB）**合并小分区**，所以「保守设置 + AQE」比「手动调到完美」更稳。

### 5.5 join 策略与倾斜治理

| 策略 | 条件 | 代价 | 备注 |
| --- | --- | --- | --- |
| **BroadcastHashJoin** | 一侧能放进广播阈值（默认 10MB，可调到数百 MB） | **最低**（无 shuffle） | **首选** |
| SortMergeJoin | 两侧都大 | 高（排序 + shuffle） | 默认兜底 |
| ShuffledHashJoin | 一侧远大于另一侧但都能放进内存 | 中 | 需 `spark.sql.adaptive.advisoryPartitionSizeInBytes` 配合 |
| 倾斜拆分（AQE） | 识别出大分区 | 自动 | 3.0+ 开启 |
| CartesianProduct | 无 join 键 | 极高 | **几乎总是写错了** |

```scala
// 教学示意，不参与构建；广播 join 与倾斜的两种标准写法
import org.apache.spark.sql.functions._
// (1) 显式广播（当 autoBroadcastJoinThreshold 不够大时）
val joined = small.df.join(broadcast(large.df), "id")

// (2) 打开 AQE 的倾斜处理，不必手写打散
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

> **与《离线》第 5 章的对照**：《离线》第 5.4 节「大表 join 小表优化」（Hive 的 `map join`）就是 broadcast join；第 5.5 节「大表 join 大表优化」给出四种方案，**其中「方案 3：倍数 B 表」和「方案 4：动态一分为二」正是 Spark 侧打散 join 的 SQL 写法**。两本书讲的是同一套方法论，语言不同而已 —— 这正是本目录把两本并列的原因。

### 5.6 序列化与数据布局

| 项 | 建议 |
| --- | --- |
| 序列化器 | `KryoSerializer`（注意要注册自定义类型以获得最佳性能） |
| 闭包大小 | 广播一个 100MB 的配置对象会拖慢所有 executor；只传需要的字段 |
| 中间文件 | 用列存（Parquet）而不是 `saveAsTextFile` 输出小文件 |
| 小文件 | **输出前 `coalesce`/`repartition` 到目标分区数**，否则下一级又变慢 |
| 本地性 | 尽量让 shuffle 前的 task 跑在数据所在节点（`preferredLocations`，AQE 会考虑） |

### 5.7 版本演进与 2026 的现代调优面

| 时间 | 变化 |
| --- | --- |
| 1.6 | Unified Memory Manager |
| 2.0 | Tungsten 全套（off-heap、codegen） |
| 3.0 | AQE、ANSI、DPP |
| 3.1–3.3 | `spark.sql.adaptive.*` 参数家族扩张；SPIP 流程 |
| 4.0 | ANSI 默认化；新一批 SI 提案影响执行语义 |

🔧 **2026 必须补的四条**：

1. **AQE 是默认调优开关**：`spark.sql.adaptive.enabled=true`（3.2+ 默认），自动 broadcast join、合并分区、倾斜拆分。**调优的第一件事就是确认它开着**，而不是调 `shuffle.partitions`。
2. **DPP 与统计信息**：3.x 默认开 DPP；定期 `ANALYZE TABLE` 更新统计信息是 CBO 正确的前提。
3. **对象存储上的 I/O 调优**：存算分离后，`S3A/OSS` 的 `fs.s3a.connection.maximum`（HTTP 连接数）与读模式（sequential vs. multi-partial-read）成为新的瓶颈；小文件在对象存储上比在 HDFS 上更致命（每个 GET 都是一次 HTTP 请求）。
4. **倾斜治理的工业化**：从「人肉看 UI」到**建基线**（每个作业记录 shuffle 字节、task 分布、GC 时间），用告警而不是工单发现回退。

---

## 三、核心精讲（续）：一个可复制的调优清单

```scala
// 教学示意，不参与构建；下面是一个「标准作业模板」示意，不是可提交的配置文件
object TuningChecklist {
  // 只写意图，不写真实运行；目的是把「调优顺序」固定下来
  val essentials = Map(
    "spark.sql.adaptive.enabled"        -> "true",   // 3.x：运行时自适应
    "spark.sql.adaptive.coalescePartitions.enabled" -> "true",
    "spark.sql.adaptive.skewJoin.enabled"          -> "true",
    "spark.sql.optimizer.dynamicPartitionPruning.enabled" -> "true",
    "spark.serializer"                  -> "org.apache.spark.serializer.KryoSerializer",
    "spark.sql.shuffle.partitions"      -> "400",    // 按数据量定，不是越大越好
    "spark.sql.autoBroadcastJoinThreshold" -> "100MB",
    "spark.dynamicAllocation.enabled"   -> "true",   // 与 shuffle service 一起开
    "spark.shuffle.service.enabled"     -> "true"
  )
  // 调优顺序：先看 explain → 再看 stage 的 shuffle/task 分布 → 再动内存与 GC
}
```

---

## 四、经典论文与原始文献

| 论文 | 出处 | 与本节的联系 |
| --- | --- | --- |
| Zaharia 等，*Resilient Distributed Datasets* | **SOSP 2013** | 缓存级别、弹性、重算代价 |
| Zaharia 等，*Spark: Cluster Computing with Working Sets* | **HotCloud 2010** | 内存复用倡议 |
| Armbrust 等，*Spark SQL: Relational Data Processing in Spark* | **SIGMOD 2014** | Catalyst 优化带来的自动收益 |
| Armbrust 等，*Delta Lake* | **SIGMOD 2020** | 表格式层的 ACID 与性能优化（小文件治理） |
| Be 等，*Photon: Fault-Tolerant Execution Engine for Fast Analytics* | **SIGMOD 2024** | 现代执行引擎的性能方法论 |
| Stonebraker 等，*The End of an Architectural Era* | **VLDB 2007** | 系统开销剖析的方法论：先测量时间去向，再优化（与本节的诊断顺序同构） |

---

## 五、近年研究与工业界开源实践（2015–2026）

**研究侧**：

- **自适应执行**：AQE 之后，研究方向转向「**运行时代价模型的准确性**」与「**自动调优参数**」（自动设置 `shuffle.partitions`、自动选 executor 数）。
- **尾延迟（tail latency）**：straggler 是大规模系统的固有问题；HdrHistogram 是测量尾延迟的标准工具。
- **内存与 GC**：off-heap、value types、以及 2020 年代对 **持久化内存（PMem）** 探索，都在减少分配这一条主线上。
- **I/O 与对象存储**：多部分上传、连接池、读放大分析，是「存算分离后调优」的核心文献来源。

**工业界开源（star 数为 2026-09-25 用 `gh api` 实测）**：

| 项目 | star | 与本节的联系 |
| --- | --- | --- |
| `apache/spark` | **44036** | 被调优的对象本身 |
| `apache/hive` | **6027** | 《离线》第 5 章的优化对象；`hive.groupby.skewindata`、`map join` 等开关 |
| `facebook/rocksdb` | **32131** | 状态与部分 shuffle 场景的 LSM |
| `apache/iceberg` | **9271** | 小文件治理（compact）直接决定后续作业性能 |
| `apache/hudi` | **6273** | 同上，且 upsert 路径对内存压力更敏感 |
| `apache/arrow` | **17155** | 零拷贝列数据交换，减少序列化 |
| `facebookincubator/velox` | **4216** | 向量化执行的性能上限参考 |

**可直接照做的清单**：

1. `Spark UI → Environment`：确认 AQE、DPP、Kryo、ESS 都开着。
2. `Spark UI → Stages`：对每个 stage 记录 `Shuffle Read Size`；排序找最大。
3. `Spark UI → Executors`：看 `GC Time` 与 `Shuffle Spill (Memory)`，判断是内存问题还是倾斜问题。
4. `explain(mode="formatted")`：确认 `PushedFilters` 非空、`Output` 列数合理。
5. 输出环节：作业结束前 `repartition(n)` 到目标分区数，避免下游读小文件。

---

## 六、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | 「优化先从调内存和 GC 开始」 | 正确顺序是：减少数据移动 → 减少对象分配 → 再调 GC/内存。多数人第一步就走错了 | 《Spark 大数据实时计算》第 7 章；《离线》第 5 章 |
| 2 | 「executor 内存越大越好」 | 大 executor = 长 GC pause + 单点故障代价高；推荐 8–16GB / 4–8 core | 《Spark 大数据实时计算》第 7 章 |
| 3 | 「`cache()` 一定加速」 | `cache` 只在该数据被**多个 action** 复用时加速；对单次 action 是净开销（序列化 + 内存） | 《Spark 大数据实时计算》第 6 章 |
| 4 | 「数据倾斜靠调并行度解决」 | 调并行度只切得更碎；正解是 broadcast join / 打散 / AQE 倾斜拆分 | 《离线》第 5.1–5.5 节 |
| 5 | 「换 G1 就能快」 | GC 占比低时换收集器几乎无收益；先解决倾斜与对象分配 | 《Spark 大数据实时计算》第 7 章 |
| 6 | 🔧 本书未覆盖 **AQE** | AQE 自动做 broadcast join、分区合并、倾斜拆分，是 Spark 3.x 之后最大的性能变化。《Spark 大数据实时计算》写于 2022 年前后、基于 Spark 2.x/3.0 早期，未把 AQE 作为默认前提 | 《Spark 大数据实时计算》第 7、9 章 |
| 7 | 🔧 本书未覆盖 **DPP 与 ANSI 模式带来的性能/兼容变化** | DPP 让分区表的 join 大幅减少读文件；ANSI 让部分隐式转换**报错**，可能影响既有作业的成功率而非性能 | 《Spark 大数据实时计算》第 8–9 章 |
| 8 | 🔧 本书未覆盖 **对象存储（S3/OSS）上的调优差异** | 存算分离后，连接数、HTTP 请求数、小文件成为新瓶颈；在 HDFS 上有效的参数在 S3 上可能起反作用 | 两书均假设本地 HDFS；详见 `09`、`11` |

---

## 七、与其他章 / 其他书的联系

**本目录内部**：

- **`02-Spark核心与RDD模型.md`**：本章 5.2 节的缓存与 stage 行为是 `02` 的应用。
- **`03-Shuffle与宽依赖.md`**：本章 5.4/5.5 节的并行度与倾斜是 `03` 的落地手段。
- **`04-SparkSQL与结构化数据.md`**：AQE、DPP、统计信息属于 `04` 的优化器范畴。
- **`06-Scala函数式与集合编程.md`**：「减少对象分配」在 Scala 侧的对应写法（避免闭包捕获大对象、`Array` 代替 case class 批量处理）在 `06`。
- **`09-存储与文件格式.md`**：小文件与列存裁剪直接决定本节的磁盘 I/O。

**其他书**：

- **`book/数据库系统概念6/12-查询处理.md`**：数据库侧的物理算子选择（hash join vs. sort-merge）与 Spark 的 join 策略选择一一对应；`12` 讲单机，`05` 讲集群。
- **`book/数据库系统概念6/13-查询优化.md`**：代价模型与统计信息，是 AQE 与 CBO 的理论来源。
- **`book/多处理器编程的艺术2/16-调度与工作分配.md`**：**executor 内的 task 执行**与**集群级调度**两层；工作窃取在 Spark 里体现为 `ForkJoinPool` 式的 task 执行器。
- **`book/Linux内核完全剖析/13-内存管理.md`**：GC、页缓存、off-heap 分配最终落到虚拟内存与 page cache；理解 `spill` 与 swap 的差别有助于判断「内存到底够不够」。
- **`book/软件架构设计/08-高并发问题.md`**：倾斜 = 热点，与「热点 key 打散」是同一套手法。
