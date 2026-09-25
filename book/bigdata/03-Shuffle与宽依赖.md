# 03 Shuffle 与宽依赖：数据是怎么搬的，以及为什么会倾斜

> **本章地图**：**宽依赖要做什么**（按 key 重分区）→ **shuffle write 的三种形态**（hash / sort / bypass）→ **shuffle read 与 fetch 模型**（Shuffle Service、连接复用、解压）→ **数据倾斜**（怎么诊断、怎么治）→ **shuffle 的 2026 改进**（push-based shuffle、避免小文件）→ **Hive/Spark 侧的同构问题**。
> **主要支撑**：《Spark 大数据实时计算：基于 Scala 开发实战》第 7 章（Spark Core 运行原理）；《离线和实时大数据开发实战》**第 5 章「Hive优化实践」**——该书对数据倾斜的论述几乎全部是关于 Hive 的，正好与 Spark 的 shuffle 对照。**两书在这一章是互补关系**。

---

## 一、本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 | 宽依赖的本质 | 宽依赖 = 一次「按 key 的重新分布」，代价 = **数据量 × 复制系数** |
| 3.2 | shuffle write：hash / sort / bypass | 小数据用 hash、大数据用 sort；`spark.shuffle.file.buffer` 一类的参数只在特殊场景才动 |
| 3.3 | shuffle read 与 fetch 模型 | 一个 reduce task 要向所有 map 端各拉一份；连接数与请求数是主要瓶颈 |
| 3.4 | 数据倾斜 | 不是 bug 而是**数据分布事实**；治法是「打散 + 局部聚合 + 二次聚合」或「广播」 |
| 3.5 | 参数与默认值 | 真正影响全局的只有几个：`spark.sql.shuffle.partitions`、AQE、广播阈值 |
| 3.6 | 2026 的改进 | push-based shuffle、map 端预聚合、避免小文件 |

---

## 二、核心精讲

### 3.1 宽依赖的本质

```scala
// 教学示意，不参与构建；说明「宽依赖 = 一次重分区」
// map 端：按 partitioner 把每条记录写到对应的桶
// reduce 端：把同一个 key 的所有记录捞到一起做聚合
val pairs = sc.parallelize(Seq("a1", "b2", "c3", "a4", "a5"), 2)
val counts = pairs.map(p => (p.head, 1)).reduceByKey(_ + _)   // 宽依赖
// shuffle 代价 ≈ 记录数 × 平均记录大小 × (目标分区数 / 本地性命中率)
```

- 宽依赖的代价可以近似写成：**搬的数据量 × 目标分区数**；因此**把目标分区数从 2000 调到 200，常常能省掉 90% 的 shuffle 时间**。
- 关键认知：**shuffle 没有「免费模式」**。任何按 key 聚合，都必然产生一次网络传输。

### 3.2 shuffle write：三种形态

| 形态 | 触发条件 | 写文件数 | 特点 | 现状 |
| --- | --- | --- | --- | --- |
| **Hash shuffle（1.6 之前默认）** | reducer 数不大 | `mapTask × reducePartitions` | 无排序，快；但文件数爆炸，小文件问题严重 | **已移除** |
| **Sort shuffle（1.6–3.0 默认）** | 通用 | `2 × mapTask`（索引 + 数据） | 先按 partitionId 排、再按 key 排；支持 map 端 combine 与 spill | Spark 3.x 的默认路径 |
| **Bypass / combine（小数据量）** | map 端无 combine 且分区数少（默认 ≤ 200） | `2 × mapTask` | 无排序、无 spill，直接写；适合小作业 | 仍存在，AQE 会自动选择 |

```scala
// 教学示意，不参与构建；map 端预聚合为什么能省一个数量级
// 反例：groupByKey —— 不预聚合，所有 (key, value) 都要过网络
val bad = pairs.map(p => (p.head, p)).groupByKey()
// 正例：reduceByKey —— map 端先本地聚合，网络流量往往是原来的 1/K（K = 每 key 的平均条数）
val good = pairs.map(p => (p.head, 1)).reduceByKey(_ + _)
```

> **记住这条**：**能用 `reduceByKey`/`aggregateByKey` 就别用 `groupByKey`**；能用 `count` 就别 `map(...).count`；能用一次 pass 就别多次 pass。

### 3.3 shuffle read 与 fetch 模型

- **一个 reduce task 需要向所有上游 map task 各发一次 fetch 请求**。因此**：
  - 上游 map task 数 × 下游 reduce task 数 = **连接数**，`fetch 请求数` 同理；
  - 请求数过多 → **TCP 连接建立开销** 与 **元数据开销** 主导（这就是 shuffle 小文件/小请求问题的根源）。
- **External Shuffle Service（ESS）**：把 shuffle 数据的生命周期从 **executor（JVM）** 解耦到 **NodeManager（外部服务）**，executor 挂掉时 shuffle 文件仍在，下游可以继续拉 —— 这是 **spark.default.dynamicAllocation 开启时**必须开的。
- **fetch 失败**：网络/超时/ESS 挂掉都会导致 stage 失败。常见缓解：`spark.shuffle.io.maxRetries`、`spark.shuffle.io.retryWait`，但**真正的问题是让 stage 变短（少依赖、少重试成本）**。
- **窄化读取（narrow down）**：Spark 3.x 后引入 `spark.sql.shuffle.partitions` 与 AQE 的**合并 shuffle 分区**能力，会在运行时把下游 task 合并跑，减少连接数。

### 3.4 数据倾斜

**诊断**（按顺序做这三件事）：

1. 打开 Spark UI 的 **Stages → Shuffle Read Size per Task**，看 task 的分布：如果最大 vs 中位数的比值 > 5，就在倾斜；
2. 看数据侧：抽样统计 key 的频次分布，找 **top 1% 的 key 占了 50% 的量**（这就是《离线》第 5 章说的「倾斜」）；
3. 定位 SQL：如果是大表 join 大表，多半是 join key 上有几个超大值（空值、`-1`、`null`、`0`、热门商品 id）。

**治理手段（按代价从小到大）**：

| 手段 | 适用 | 代价 |
| --- | --- | --- |
| **过滤倾斜 key**（空值不参与 join） | 空值/哨兵值导致的倾斜 | 最简单，注意不要改变业务语义 |
| **打散 + 双聚合**（附加随机前缀，局部聚合后再全局聚合） | `groupByKey` 倾斜 | 需要两次 shuffle，但负载均衡 |
| **两阶段 join**（加随机前缀打散大表，小表复制 N 份） | join 倾斜 | 小表要能放进广播；大表被放大 N 倍 |
| **广播 join**（`broadcast()` 或 `spark.sql.autoBroadcastJoinThreshold`） | 一个表能放进内存（< 数百 MB） | **最好的解法** —— 直接消灭 shuffle |
| **盐值 + 分桶 hire** | 极端倾斜且两边都大 | 复杂度最高 |
| **AQE 自动倾斜处理**（`spark.sql.adaptive.skewJoin.enabled`） | Spark 3.0+ | 引擎自动把倾斜的分区拆成小分区分别 join |

```scala
// 教学示意，不参与构建；倾斜双聚合的标准写法
// 阶段一：给 key 加随机前缀，先局部聚合
val salted = largeRdd.map { case (k, v) => ((k, rnd.nextInt(10)), v) }
val partial = salted.reduceByKey(_ + _)
// 阶段二：去掉前缀，做全局聚合
val final_ = partial.map { case ((k, _), c) => (k, c) }.reduceByKey(_ + _)
```

> 《离线和实时大数据开发实战》第 5 章的**「方案 4：动态一分为二」**（用 `case when` 把倾斜 key 拆成两路）与上面的「两阶段 join」是**完全同一个想法**，只是用 SQL 表达。这说明倾斜治理的**方法论是通用的**，换引擎不用重学 —— 这是两本书合作的价值所在。

### 3.5 真正值得调的参数

| 参数 | 默认值（Spark 3.x） | 什么时候动 |
| --- | --- | --- |
| `spark.sql.shuffle.partitions` | 200 | **默认就调它**：小事 50–100、大作业 1000–5000，关键是让单个 task 处理 128MB–1GB |
| `spark.sql.autoBroadcastJoinThreshold` | 10MB | 广播 join 是消灭倾斜的正解；调大到 100–500MB，但小表必须能常驻 executor 内存 |
| `spark.shuffle.file.buffer` | 1m | 只在 shuffle 特别小时微调；调大反而增加内存占用 |
| `spark.reducer.maxSizeInFlight` | 48m | fetch 并行度，网络带宽受限时可降 |
| `spark.sql.adaptive.enabled` | true（3.2+） | **不要关**。它会自动合并小分区、倾斜 join、调并行度 |
| `spark.dynamicAllocation.enabled` | false | 与 ESS 一起开；否则 executor 退不出，shuffle 会失败 |

> 经验法则：**90% 的性能问题靠改 `shuffle.partitions` 与「换成 broadcast join」就能解决**，而不是靠调 shuffle 缓冲区。

### 3.6 版本演进

| 版本 | shuffle 相关变化 |
| --- | --- |
| 1.x | Hash shuffle（文件爆炸）、ES 之前没有 ESS |
| 1.6 | Sort shuffle 成为默认；引入 ESS |
| 2.0 | Tungsten 的 shuffle 编码（off-heap，减少序列化与 GC） |
| 2.3 | Push-based shuffle（实验）→ 在 3.x 逐步成型 |
| 3.0 | **AQE** 引入：运行时合并 shuffle 分区、自动 broadcast join、倾斜 join 处理 |
| 3.2+ | AQE 的 `optimizeSkewsInRebalancePartitions` 等；`spark.sql.shuffle.partitions` 在 AQE 下可运行时调整 |
| 3.3+ | Push-based shuffle（Magnet/Spark 4 方向）继续推进：把 shuffle 结果推送到远端存储，减少 fetch 连接数 |

---

## 三、核心精讲（续）：shuffle 代价的估算

```scala
// 教学示意，不参与构建；一个用来判断「值不值得优化」的粗算模型
// 目的：给出「优化前后 shuffle 字节数」的对比，不要运行
object ShuffleCostModel {
  def main(args: Array[String]): Unit = {
    val records = 1e9            // 1e9 条记录
    val bytesPerRecord = 64      // 平均 64 字节
    val sourcePartitions = 2000  // 当前 shuffle 分区数
    val targetPartitions = 200   // 调整后的分区数

    // 不预聚合（groupByKey 语义）：所有记录都要过网络
    val withoutCombine = records * bytesPerRecord
    // 有 map 端预聚合且每个 key 平均 K 条：网络流量降到 1/K
    val withCombine = withoutCombine / 8
    // 分区数从 2000 降到 200：fetch 请求数减少 10 倍
    val requestsBefore = (records / sourcePartitions) * sourcePartitions
    val requestsAfter  = (records / targetPartitions) * targetPartitions

    println(s"shuffle bytes: ${withoutCombine / 1e9} GB -> ${withCombine / 1e9} GB")
    println(s"fetch requests: $requestsBefore -> $requestsAfter")
  }
}
```

> 这个模型的目的不是给出精确数字，而是让你在写代码时心里有个量级：**「这一段会不会搬几百 GB？」** 大多数慢作业的问题就在这里。

---

## 四、经典论文与原始文献

| 论文 | 出处 | 与本节的联系 |
| --- | --- | --- |
| Zaharia 等，*Resilient Distributed Datasets* | **SOSP 2013** | 宽依赖（ShuffleDependency）的正式定义与 stage 切分规则 |
| Zaharia 等，*Spark: Cluster Computing with Working Sets* | **HotCloud 2010** | shuffle 作为「工作集交换」的原始形态 |
| Isard、Birrell 等，*Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks* | **EuroSys 2007** | 与 Spark 的 DAG 调度同代；宽依赖在 Dryad 里就是 redistribute 边 |
| Zaharia 等，*Magically Decoupling Shuffle and Scheduling...*（Push-based shuffle 相关报告/技术分享） | Spark Summit / 社区分享（非论文） | push-based shuffle 的思路来源；此处只作背景，不冒充论文 |

> 注：**shuffle 机制本身没有一篇单独的 canonical 论文**，其知识来源是 RDD 论文 + 源码 + Spark Summit 的技术分享。本节不杜撰论文。

---

## 五、近年研究与工业界开源实践（2015–2026）

**研究侧**：

- **调度感知的 shuffle**：把「下游 fetch 需求」纳入调度（哪个 task 快、哪个慢），减少 straggler 放大；与 `book/多处理器编程的艺术2/16-调度与工作分配.md` 的思路直接相通。
- **shuffle 与存储解耦**：存算分离之后，shuffle 数据放本地磁盘不再划算；**remote shuffle service**（把 shuffle 数据写到对象存储/远端）成为 2023–2026 年的研究热点，核心问题是**小对象与小请求**。
- **倾斜的自适应处理**：AQE 的倾斜 join 自动拆分是从「人工经验」到「引擎自治」的关键一步；相关思路也出现在 Flink 的自适应 parallelism 中。
- **小文件问题**：湖仓一体时代，流式小文件（每个 checkpoint 一个小文件）成为表格式的头号敌人，Iceberg/Hudi/Delta 都提供了 **`compact` / `rewrite_data_files` / clustering** 运维任务。

**工业界开源（star 数为 2026-09-25 用 `gh api` 实测）**：

| 项目 | star | 与本节的联系 |
| --- | --- | --- |
| `apache/spark` | **44036** | shuffle 的全部实现都在 `ShuffleManager` / `BlockManager` |
| `apache/hive` | **6027** | 《离线》第 5 章的倾斜治理发生在 Hive 上：`map join`（= 广播 join）、`group by` 的 `hive.groupby.skewindata` |
| `facebook/rocksdb` | **32131** | Flink 的 RocksDB state backend 与部分 shuffle 场景使用 LSM |
| `apache/iceberg` | **9271** | 小文件压缩（compact）是 shuffle 问题的湖仓侧延伸 |
| `apache/hudi` | **6273** | 同样提供 incremental + compaction |

**可以直接照做的排查清单**：

1. Spark UI → Stages：找到 `Shuffle Read Size` 最大的那几个 task，看它的数据量是不是中位数的一个数量级以上。
2. 如果最大 task 是中位数 10 倍 → 倾斜，按 3.4 节的手段处理。
3. 如果 shuffle **总字节**大但分布均匀 → 减少数据（预聚合、只选需要的列、用 Parquet 列存裁剪），而不是调并行度。
4. 如果 task 数极多（>5000）而数据量小 → 调低 `spark.sql.shuffle.partitions`。
5. 如果作业有 shuffle 但 executor 反复 lost → 检查**是否开了 dynamic allocation 而没开 ESS**。

---

## 六、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | 「数据倾斜是执行时偶发的 bug」 | 倾斜是**数据的固有属性**（少数 key 占多数记录），只要数据分布不变、倾斜就会重现 | 《离线》第 5.1 节「离线数据处理的主要挑战：数据倾斜」 |
| 2 | 「调大并行度能治倾斜」 | 调大并行度只是把倾斜的 key 切得更碎，**总数据量不变、单 task 时间可能更差**；正解是打散或广播 | 《离线》第 5.2 节 Hive 优化；Spark 侧见本章 3.4 |
| 3 | 「Hive 与 Spark 的倾斜是两回事」 | 方法论同构：Hive 的「动态一分为二」≈ Spark 的「两阶段 join」；区别只在实现手段 | 《离线》第 5.5.4 节 vs 《Spark》第 7 章 |
| 4 | 「`groupByKey` 和 `reduceByKey` 结果一样，可以随便换」 | `reduceByKey` 有 **map 端预聚合**，网络流量常常差一个数量级 | 《Spark 大数据实时计算》第 6 章 |
| 5 | 🔧 「shuffle 只能调缓冲区大小」 | 真正有效的顺序是：**AQE 打开 → broadcast join → 降 `shuffle.partitions` → 预聚合**；调缓冲区是最不重要的一步 | 《Spark 大数据实时计算》第 7 章 |
| 6 | 🔧 本书未覆盖 **Spark 3.x 的 AQE** | AQE 会自动做三件事：合并小 shuffle 分区、自动 broadcast join、倾斜 join 拆分。**在不改代码的前提下**，AQE 本身就解决了一部分倾斜 | 《Spark 大数据实时计算》第 7 章（写作时 AQE 尚未成为默认） |
| 7 | 🔧 本书未覆盖 **push-based shuffle / remote shuffle** | 2023 年之后 shuffle 与计算解耦（数据写远端、fetch 走网络+对象存储），这是存算分离架构下的必然演化 | 《Spark 大数据实时计算》第 5、7 章（假设 shuffle 在本地磁盘） |
| 8 | 🔧 本书未覆盖 **流式小文件** | 流作业高频 checkpoint 写出大量小文件，会拖垮元数据；2026 年靠 Iceberg/Hudi/Delta 的 compaction 解决 | 《离线》第 7.5 节数据湖未展开；详见 `09`、`10` |

---

## 七、与其他章 / 其他书的联系

**本目录内部**：

- **`02-Spark核心与RDD模型.md`**：本章 3.1 节的「宽依赖切 stage」是 `02` 第 2.3 节的伸延；两章要一起读。
- **`04-SparkSQL与结构化数据.md`**：Catalyst 负责把 SQL 翻译成带宽依赖的 DAG；AQE 在 `04` 中作为优化器的一部分讨论。
- **`05-Spark性能优化.md`**：倾斜与并行度调优在 `05` 中被汇总为一张清单。
- **`09-存储与文件格式.md`**：Parquet 的**列裁剪 + 统计信息**能直接从源头减少 shuffle 的输入量，是「治 shuffle」的另一种思路。

**其他书**：

- **`book/数据库系统概念6/13-查询优化.md`**：数据库里的 hash join / sort-merge join 与 Spark 的 shuffle 是同一件事的两面；**「小表 broadcast」≈ 数据库的 eligible-for-hash-join 小表**。
- **`book/多处理器编程的艺术2/16-调度与工作分配.md`**：shuffle 的 fetch 请求风暴是「调度器需要考虑数据位置」的经典案例；工作窃取里的「窃取谁」在这里变成「谁有我要的数据」。
- **`book/Linux内核完全剖析/12-文件系统.md`**：shuffle 落盘与小文件读写，最终都落到 inode、page cache 与文件系统层；一次 fetch 一个 4KB 小文件在 HDFS 上的代价远高于本地盘。
- **`book/软件架构设计/08-高并发问题.md`**：倾斜 = 负载不均，与「热点 key 导致缓存击穿」是同一个问题在分布式数据上的形态。
