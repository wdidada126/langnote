# 07 — 底层 API：RDD 与共享变量

> 原书 Ch 14: The Low-Level RDD API
> 原书 Ch 15: Distributed Shared Variables
> 原书 Ch 16: Developing Spark Applications (调试部分)

---

## Ch 14 核心：RDD API

### RDD 的定位

⚠️ **RDD 是 Spark 的底层 API**，本书推荐优先使用 DataFrame/Dataset（Catalyst 可优化）。
✅ 但在某些场景仍需 RDD：自定义分区、非结构化数据处理、与底层执行模型交互。

### RDD 的创建

```scala
// 从集合创建
val rdd = sc.parallelize(Seq(1, 2, 3, 4, 5))
val rdd2 = sc.parallelize(Seq(1, 2, 3), numSlices = 4)  // 指定分区数

// 从外部存储创建
val textFile = sc.textFile("hdfs://path/to/file")
val jsonRDD = sc.textFile("s3a://bucket/data/*.json")

// 从 DataFrame 转换
val rddFromDF = df.rdd  // DataFrame → RDD[Row]
```

### RDD 操作分类

| 类型 | 操作 | 说明 |
|------|------|------|
| Transformation | `map`, `flatMap`, `filter`, `distinct` | 返回新 RDD，惰性 |
| Transformation | `union`, `intersection`, `subtract` | 集合操作 |
| Transformation | `join`, `cogroup`, `groupByKey`, `reduceByKey` | 宽依赖 (Shuffle) |
| Action | `collect`, `count`, `first`, `take` | 返回结果到 Driver |
| Action | `reduce`, `fold`, `aggregate` | 聚合操作 |
| Action | `saveAsTextFile`, `saveAsObjectFile` | 持久化 |

### 关键操作示例

```scala
val numbers = sc.parallelize(1 to 100)

// map vs flatMap
numbers.map(x => Seq(x, x*2))    // RDD[Seq[Int]]
numbers.flatMap(x => Seq(x, x*2)) // RDD[Int] — 展平

// reduceByKey vs groupByKey (性能差异巨大)
val pairs = sc.parallelize(Seq(("a",1),("b",2),("a",3)))
pairs.reduceByKey(_ + _)   // ✅ 预聚合，Shuffle 数据少
pairs.groupByKey()          // ⚠️ 全量 Shuffle，内存风险

// aggregate (两阶段聚合)
pairs.aggregate(0)(
  (acc, value) => acc + value,    // 分区内聚合
  (acc1, acc2) => acc1 + acc2     // 分区间聚合
)
```

### RDD 缓存与持久化

```scala
rdd.cache()           // 默认 MEMORY_ONLY
rdd.persist(StorageLevel.MEMORY_AND_DISK)  // 内存+磁盘
rdd.persist(StorageLevel.DISK_ONLY)
rdd.unpersist()       // 手动释放
```

| 存储级别 | 内存 | 磁盘 | 序列化 | 说明 |
|----------|------|------|--------|------|
| MEMORY_ONLY | ✅ | ❌ | ❌ | 默认，最快 |
| MEMORY_AND_DISK | ✅ | ✅ | ❌ | 溢出到磁盘 |
| DISK_ONLY | ❌ | ✅ | ❌ | 仅磁盘 |
| MEMORY_ONLY_SER | ✅ | ❌ | ✅ | 节省内存 |

---

## Ch 15 核心：分布式共享变量

### Broadcast 变量

✅ **Broadcast 变量**：将小数据集高效分发到所有 Executor（只读）。

```scala
val broadcastVar = sc.broadcast(Map("a" -> 1, "b" -> 2))
val result = rdd.map(x => broadcastVar.value.getOrElse(x, 0))
```

⚠️ 适合小表 Join（Broadcast Join）；不适合大数据（会占满 Executor 内存）。
⚠️ Broadcast 变量在 Task 间只读，不可修改。

### Accumulator 变量

✅ **Accumulator**：Executor 向 Driver 聚合信息的通道（只加）。

```scala
val errorCount = sc.longAccumulator("ErrorCount")
rdd.foreach(line => {
  try { process(line) }
  catch { case _: Exception => errorCount.add(1) }
})
println(s"Total errors: ${errorCount.value}")
```

⚠️ Accumulator 的更新在 Task 重试时可能重复计数。

---

## Ch 16 补充：调试与测试

✅ **Spark UI**：调试首选工具（Stages/SQL/Executors 页面）
✅ **日志级别**：`spark.sparkContext.setLogLevel("DEBUG")` 临时调试
⚠️ `collect()` 到 Driver 调试小数据集；切勿在大数据集上使用

---

## 🔧 DuckDB / SQLite 类比

> 以下类比均为辅助理解，**非本书引擎行为**。

🔧 **类比 1：RDD.map ≈ DuckDB 列操作 / SQLite 标量函数**
- RDD 的 `map(x => x * 2)` 是逐元素变换
- DuckDB 的 `SELECT x * 2 FROM t` 是向量化列操作（更快）
- SQLite 的自定义函数类似但单机 · ⚠️ 非本书引擎行为

🔧 **类比 2：Broadcast 变量 ≈ DuckDB 的 Hash Table 预加载**
- Spark Broadcast 将小表分发到所有节点
- DuckDB Hash Join 也将小表加载到内存中的 Hash Table
- 思路相同：避免重复扫描小表 · ⚠️ 非本书引擎行为

🔧 **类比 3：RDD.cache() ≈ DuckDB 的临时表 / SQLite 的内存表**
- Spark: `rdd.cache()` 将数据缓存在内存
- DuckDB: `CREATE TEMP TABLE t AS SELECT ...` 缓存查询结果
- SQLite: `CREATE TABLE t AS SELECT ...` (内存数据库时) · ⚠️ 非本书引擎行为

🔧 **类比 4：reduceByKey ≈ DuckDB GROUP BY / SQLite GROUP BY**
- `rdd.reduceByKey(_ + _)` ≈ `SELECT key, SUM(value) FROM t GROUP BY key`
- reduceByKey 在 Map 端预聚合，类似 DuckDB 的 Partial Aggregate · ⚠️ 非本书引擎行为

---

## 核心概念速览（中英对照）

| 中文 | English | 简述 |
|------|---------|------|
| 弹性分布式数据集 | RDD | 底层分布式数据抽象 |
| 转换 | Transformation | 惰性操作，返回新 RDD |
| 行动 | Action | 触发执行，返回结果 |
| 广播变量 | Broadcast Variable | 只读数据分发到所有节点 |
| 累加器 | Accumulator | Executor→Driver 的只加聚合 |
| 持久化 | Persistence / Caching | 将 RDD 缓存在内存/磁盘 |
| 预聚合 | Map-side Combine | Shuffle 前在本地先聚合 |
| 分区 | Partition | RDD 的数据分片 |

---

## 最新演进与工业实践

**RDD 与底层 API 的演进（书后发展）：**

| 演进 | 版本 | 影响 |
|------|------|------|
| DataFrame 成为首选 | 2.0+ | RDD 使用场景大幅缩小 |
| Tungsten 引擎 | 2.x | 二进制内存管理，绕过 Java 序列化 |
| AQE 动态优化 | 3.0+ | 底层物理计划可运行时调整 |
| Spark Connect | 3.4+ | RDD API 不可通过 Connect 访问 |
| RDD 维护模式 | 4.x | 官方推荐 DataFrame；RDD 仅保留兼容 |

> 来源: spark.apache.org ✅

**工业实践（2026）：**
- 新项目几乎全部使用 DataFrame API；RDD 仅用于特殊场景（自定义分区器）
- Broadcast Join 仍是小表 Join 大表的首选策略
- DuckDB 在单机场景已可替代大部分 RDD 操作
- 相关参考: [bigdata/02-Spark核心与RDD模型](../bigdata/02-Spark核心与RDD模型.md) 对 RDD 有更详细讨论
