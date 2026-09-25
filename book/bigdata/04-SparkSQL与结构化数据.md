# 04 Spark SQL 与结构化数据：Catalyst、Tungsten 与向量化执行

> **本章地图**：**为什么需要 Spark SQL**（RDD 缺 schema）→ **Dataset/DataFrame 的三层抽象** → **Catalyst 优化器**（解析 → 分析 → 逻辑优化 → 物理计划）→ **Tungsten 与执行层**（代码生成、向量化、堆外内存）→ **与数据库系统的对照**（有意思的相似、有本质区别）→ **2026 的现实**：ANSI 模式、DPP、AQE、Photon。
> **主要支撑**：《Spark 大数据实时计算：基于 Scala 开发实战》**第 8 章（Spark SQL 结构化数据处理入门）与第 9 章（高级应用）**。
> **强烈对照**：`book/数据库系统概念6/12-查询处理.md`、`13-查询优化.md`。

---

## 一、本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 | 三层 API 抽象 | RDD → DataFrame → Dataset；类型安全与运行优化的取舍 |
| 4.2 | 一段 SQL 的生命周期 | 12 步；记住 `Unresolved → Resolved` 这一步最容易出错 |
| 4.3 | Catalyst 优化器 | 基于规则的优化（RBO）+ 基于代价的优化（CBO）部分 |
| 4.4 | Tungsten 与执行层 | Whole-stage codegen、off-heap、向量化；与数据库的「火山模型」对照 |
| 4.5 | 与数据库系统的同与不同 | 优化器的思路一样，代价模型与事务语义差很远 |
| 4.6 | 2026 的现实 | ANSI 模式、DPP、AQE、Photon、SI（Spark 4.0 动向） |

---

## 二、核心精讲

### 4.1 三层 API 抽象

| API | 类型安全（编译期） | 优化空间 | 适用场景（2026） |
| --- | --- | --- | --- |
| `RDD[T]` | **是** | 无 schema，优化器无从下手 | 手写算子、非结构化处理 |
| `DataFrame` / `Dataset[Row]` | 编译期无（运行时有） | 有 schema，**可被 Catalyst 优化** | 主力写法 |
| `Dataset[T]`（Scala/Java） | **是**（case class 有类型） | 有 schema + 编译期类型 | 需要类型安全的结构化作业 |

```scala
// 教学示意，不参与构建；同一份逻辑的三种写法，注意只有第三种有编译期类型
// (1) RDD：没有 schema，优化器帮不上忙
rdd.map(l => (l.split(",")(0), l.split(",")(1).toInt))

// (2) Dataset[Row]：编译期不报错，运行时才发现列名/类型问题
spark.read.option("header", "true").csv("hdfs:///users.csv")
  .filter($"age" > 18)     // 列名写错要到运行时才发现

// (3) Dataset[CaseClass]：列错、类型错都能在编译期发现
case class User(id: Long, name: String, age: Int)
val users: Dataset[User] = spark.read.option("header", "true").csv("hdfs:///users.csv").as[User]
```

> **理解这条是读懂 Spark 2.x+ 的关键**：Spark 说的「比 MapReduce 快」，一大半来自**优化器能看见 schema**；把 RDD 换成 Dataset，等于把一段手写代码交给数据库优化器。

### 4.2 一段 SQL 的生命周期

```
SQL/DSL 文本
  │ ① Parse        : SqlParser → Unresolved Logical Plan（只有表名/列名字符串，不知道类型）
  ▼
② Analyze        : Analyzer 查 Catalog，补类型、补列名 → Resolved Logical Plan
  ▼
③ Logical Optimize : Catalyst 规则改写（谓词下推、列裁剪、常量折叠、join 重排）→ Optimized Logical Plan
  ▼
④ Physical Plan   : 按策略生成若干候选物理计划；CBO 用统计信息挑最便宜的
  ▼
⑤ Cost Model      : 估算行数/IO/CPU，挑代价最低的
  ▼
⑥ Code Generation : 把物理计划编译成一个个 Java 方法（Whole-Stage CodeGen）
  ▼
⑦ Execution       : 同一 stage 内的算子不要中间对象，直接在栈上循环
```

**最容易出问题的地方是 ②**：

- 列名写错 → `AnalysisException`（这是最常见的错误）；
- 通配符/隐式转换在 ANSI 模式开启后可能报错；
- 找不到数据源（`Catalog`/`DataSource` 注册问题，尤其是 `hive metastore` 未配置）。

```scala
// 教学示意，不参与构建；查看优化计划的三个入口
val df = spark.read.format("parquet").load("hdfs:///ods/user")
  .filter($"age" > 18).select($"id", $"name")

df.explain(true)                       // 打印物理计划
df.explain("formatted")                 // 更可读：带子计划与排序信息
spark.sql("EXPLAIN EXTENDED SELECT ...")// SQL 方式
```

- `== Physical Plan ==` 里应该看到的关键点：**谓词下推**（`PushedFilters`）、**列裁剪**（只扫描需要的列）、**Dynamic Partition Pruning（DPP）**、**Stat estimates**（行数估算是否接近真实）。
- **诊断技巧**：如果 `Stat estimates` 的数字离谱（比如估算 1 行实际 1 亿行），说明 **统计信息缺失或过期**，CBO 会做出错误选择。

### 4.3 Catalyst 优化器

Catalyst 用 **Scala 的函数式特性**（case class 的 pattern match、集合的 map/flatMap/fold）实现，这本身就是「用 Scala 写编译器」的典型范例：

```scala
// 教学示意，不参与构建；Catalyst 规则的主要形态
// 一条规则 = 对一棵树做一次模式匹配 + 改写
object PushDownPredicate extends Rule[LogicalPlan] {
  def apply(plan: LogicalPlan): LogicalPlan = plan.transformDown {
    case Filter(cond, project @ Project(_, child)) if !cond.references.subsetOf(project.outputSet) =>
      Filter(cond, project)            // 谓词推不下去就留在原地
    case Filter(cond, child) =>
      Filter(cond, cond.referenceEqual(child))  // 真正的下推逻辑（示意）
  }
}
```

主要规则类别（读代码时按这个顺序找）：

| 类别 | 例子 | 效果 |
| --- | --- | --- |
| **谓词下推 Predicate Pushdown** | `Filter` 推到 `Relation` 下 | 只读需要的行 |
| **列裁剪 Column Pruning** | 只 `select` 用到的列 | 只读需要的列（列存收益放大） |
| **常量折叠 Constant Folding** | `1 + 2 → 3` | 少算 |
| **Join 重排 Join Reorder** | 多表 join 交换顺序 | 显著减少中间结果 |
| **投影裁剪 / 算子下推** | `Limit` 下推到聚合 | 减少上游数据量 |
| **AQE 的运行时规则** | 运行时合并分区、倾斜 join 拆分 | 不需要懂数据也能优化 |

### 4.4 Tungsten 与执行层

Tungsten 的目标一句话：**「让 Spark 尽量接近裸机性能」**，三条路：

| 手段 | 做法 | 解决什么 |
| --- | --- | --- |
| **Whole-Stage Java Codegen** | 把整个 stage 的算子链编译成一个 Java 方法，用栈上局部变量代替中间对象 | 消除虚调用与序列化开销 |
| **Off-heap 二进制编码** | 数据以紧凑二进制格式存在堆外（`UnsafeRow`），指针 = 偏移量 | 消除 Java 对象头、减少 GC 压力 |
| **Cache-aware 数据结构** | 按内存对齐与访问局部性组织数据 | 提高 CPU cache 命中率 |

**与数据库的对照（重要）**：

| 维度 | 传统数据库（火山/Nested Loop 模型） | Spark（Codegen / Tungsten） |
| --- | --- | --- |
| 算子执行 | 每个算子 `next()` 一次，逐行迭代 | 编译成整体循环，**批量/整段执行** |
| 中间结果 | 每行一个对象（物化在内存） | 尽量不物化（流水线） |
| 编译执行 | Spark 相对晚（2.0 之后）；数据库更早（如 DB2/SQL Server 的 codegen） | Spark 在「代码生成 + 向量化」两端都做了 |
| 向量化 | 现代 OLAP 数据库普遍采用（ClickHouse、Doris、Velox） | Spark 也支持（`spark.sql.parquet.enableVectorizedReader`） |

> **结论**：Spark 的执行层在 2020 年代已经**基本追平专门的 OLAP 数据库**，差别只剩「事务语义、索引、UDF 生态」。

### 4.5 与数据库系统的同与不同

**相同**（这也是《数据库系统概念》阅读本节的价值）：

- 都是**代价模型驱动**的选择（选 hash join 还是 sort-merge join，取决于行数与内存）；
- 都有**统计信息**（行数、NDV、min/max、直方图）驱动优化；
- 都有**谓词下推与列裁剪**这类物理优化。

**不同**（Spark 的关键取舍）：

| 不同点 | 数据库 | Spark |
| --- | --- | --- |
| 数据量 | GB ~ TB | TB ~ PB |
| 是否需要索引 | 强依赖 B+ 树/位图 | 一般**不用索引**，靠扫描 + 谓词下推 + 列存 |
| 事务 | 完整 ACID、MVCC、WAL | 没有行级事务；靠**表格式的 ACID 提交**在 2020 年代补上 |
| 执行位置 | 单机 / shared-nothing 集群 | 集群，数据不动代码动 |

**这解释了为什么「Spark 上跑的 SQL 和 MySQL 里跑的 SQL」行为可能不一样**：同样的 `INSERT OR UPDATE`，MySQL 有行锁与唯一约束，Spark 只有「写出去的表格式保证原子可见性」。

### 4.6 版本演进与 2026 的现实

| 版本 | 关键变化 |
| --- | --- |
| 1.4 / 1.5 | Spark SQL 雏形；DataFrame API |
| 2.0 | **Tungsten**、**Dataset**、**Structured Streaming**（Spark SQL 上的流） |
| 2.1 | 二级缓存、Python 支持 |
| 3.0 | **ANSI 模式**（`spark.sql.ansi.enabled`）、**AQE**、**DPP（动态分区裁剪）**、DataSource V2 API |
| 3.1–3.3 | ANSI 完善、`spark.sql.ansi.cast` 细分行为、SPIP 流程、SPIP 的 SI（Spark Improvement）规范 |
| 4.0（进行中） | **ANSI 与 SI 逐步成为默认**；目标是「与标准 SQL 完全一致的语义」；对老代码的冲击是**隐式转换失败**与**数字溢出报错** |

🔧 **2026 必须补的四条**：

1. **ANSI 模式**：开启后 `'1' + 2` 不再是隐式转换而是 `AnalysisException`；`CAST` 越界会报错而不是返回 null；字符串与数字比较不再静默。**从 2.x 迁移到 4.x 时，这是第一件要测的事**（用 `SELECT /*+ ... */` 或逐条跑 `EXPLAIN` 定位）。
2. **动态分区裁剪 DPP**：`spark.sql.optimizer.dynamicPartitionPruning.enabled=true`（3.x 默认开），在 join 时把过滤条件推到**扫描侧**，跳过不需要的分区/文件，**对分区表是数量级的收益**。
3. **AQE**：`spark.sql.adaptive.enabled=true`（3.2+ 默认）。它把优化从「计划时」推到「运行时」，能自动做广播 join、分区合并、倾斜拆分。**这是 2018 年之后最大的性能变化，两本书都未覆盖**。
4. **Photon（Databricks 的向量化编译引擎）**：以 SIGMOD 2024 的论文《*Photon: Fault-Tolerant Execution Engine for Fast Analytics*》公开，主打「向量化 + 原生执行 + 容错」，可作为 Spark 执行层 Future 的参考；开源社区（Velox、DuckDB）在做同样的事。

---

## 三、核心精讲（续）：教学示意代码

```scala
// 教学示意，不参与构建；下面演示「为什么列裁剪 + 谓词下推在列存上是数量级的收益」
// 一张 100 列的表，只读 3 列 + 过滤 1 列
object ColumnPruningTeaching {
  // 参数示意（真实数字随版本变化，此处只表达量级）
  val totalColumns = 100
  val usedColumns  = 3
  val rowSize      = 1024   // bytes
  val rowCount     = 1e9

  def scanBytes(nCols: Int): Double = rowCount * rowSize * (nCols.toDouble / totalColumns)

  def main(args: Array[String]): Unit = {
    println(s"扫描全部列: ${scanBytes(totalColumns) / 1e9} GB")
    println(s"只扫描 3 列: ${scanBytes(usedColumns) / 1e9} GB")
    // 在 Parquet/ORC 上，这两行的差距就是列存 + 列裁剪的收益
  }
}
```

> 结合 `09-存储与文件格式.md`：Parquet 的 **row group / statistics / bloom filter** 让下推真正生效；如果文件没有统计信息，谓词下推只能做到「文件级」而不是「行组级」。

---

## 四、经典论文与原始文献

| 论文 | 出处 | 与本节的联系 |
| --- | --- | --- |
| Armbrust 等，*Spark SQL: Relational Data Processing in Spark* | **SIGMOD 2014** | DataFrame 与 Catalyst 的正式出处 |
| Zaharia 等，*Resilient Distributed Datasets* | **SOSP 2013** | RDD 与宽窄依赖（`02`、`03` 的内容） |
| Armbrust 等，*Delta Lake: High-Performance Open Storage Formats for Hadoop Table Storage* | **SIGMOD 2020** | 表格式的 ACID 与 MVCC，补上 Spark「没有事务」的一块（详见 `10`） |
| Be、Scandinav 等，*Photon: Fault-Tolerant Execution Engine for Fast Analytics* | **SIGMOD 2024** | 向量化 + 原生执行 + 容错的现代形态 |
| Graefe，*Volcano, an Optimizer for Query Processing* | **IEEE Trans. on Knowledge and Data Engineering, 1994** | 火山模型；对比 Spark 的 codegen 执行 |
| Anwar 等，*Apache Arrow: A Cross-Language Platform for In-Memory Data* | Arrow 项目（见 arrow.apache.org 的规格文档；paper 版本请以后续 SIGMOD 论文页为准） | 跨语言的内存列格式，是 Spark/Trino/Flink 零拷贝交换的基础（详见 `09`、`10`） |
| 相关规范：Apache Parquet format spec、Apache ORC spec | 官方文档 | 列存格式本身没有 canonical 论文，只引规范文档 |

---

## 五、近年研究与工业界开源实践（2015–2026）

**研究侧**：

- **查询编译**：Codegen vs. Vectorization 的实测对比（不同算子上互有胜负），最终在实践中**两者并存**（小批量/点查用向量化、复杂表达式用 codegen）。
- **统计信息与 CBO**：Spark 3.x 引入**多列统计（`analyze table ... partition` 的 `columns` 子句、NDV via HyperLogLog）** 与 **correlated auto-statistics**；核心难题依然是「估算行数不准导致 join 顺序错」。
- **自适应执行**：从 RBO 到 **AQE（运行时重规划）** 是 2015–2026 年查询引擎最大的范式变化之一；Flink、Trino、Presto 都做了自己的版本。
- **向量化与 SIMD**：Arrow（2016 起）、Velox（2022 起）、DuckDB（2019 起）把「内存列格式 + 向量化算子 + 本地持久化」做成了一个完整的嵌入式引擎，对 Spark 形成压力。

**工业界开源（star 数为 2026-09-25 用 `gh api` 实测）**：

| 项目 | star | 与本节的联系 |
| --- | --- | --- |
| `apache/spark` | **44036** | Catalyst 与 Tungsten 的实现所在（本节 4.2/4.3/4.4） |
| `facebookincubator/velox` | **4216** | Meta 开源的向量化执行引擎，是 Spark/Presto 执行层的重要参考 |
| `duckdb/duckdb` | **41702** | 嵌入式 OLAP，用 SQL 就能证明「一个进程内跑得比 Spark 快」 |
| `apache/arrow` | **17155** | 内存列格式标准；Spark/Trino/Flink/Pandas 之间的通用货币 |
| `trinodb/trino` | **13279** | 联邦查询引擎，与 Spark SQL 在「Ad-hoc 交互分析」上正面竞争 |
| `clickhouse/clickhouse` | **50069** | 实时分析的事实标准之一，是 Spark SQL 的竞品而非补充 |
| `apache/hive` | **6027** |  metastore 与 Hive QL 兼容层，Spark SQL 仍大量依赖它 |

**工程建议**：

1. `explain(mode="extended")` 看三件事：`PushedFilters`、`PushedFilters: [...]` 中是否包含了你的过滤条件；`Output` 中列数；`Stat estimates` 是否接近真实。
2. 分区表上的 join，打开 **DPP**（3.x 默认开）；非分区表 DPP 无效。
3. 统计信息过期是 CBO 出错的第一原因：定期跑 `ANALYZE TABLE ... COMPUTE STATISTICS`。
4. 从 Spark 2.x 升到 3.x/4.x：**先开 `ansi.enabled=false` 跑一遍，把报错的 SQL 找出来，再逐条决定是修数据还是修 SQL**。

---

## 六、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | 「Spark 是 SQL 引擎，写 SQL 就行」 | Spark 是**分布式计算引擎 + SQL 前端**；没有事务、没有索引依赖，行为与 MySQL 不同 | 《Spark 大数据实时计算》第 8 章 |
| 2 | 「列名写错了会编译失败」 | `Dataset[Row]` 的列名错误要到**运行时**才报 `AnalysisException`；只有 `Dataset[CaseClass]` 才有编译期检查 | 《Spark 大数据实时计算》第 9 章 |
| 3 | 「优化器能看懂我 RDD 里的算子」 | RDD **没有 schema**，Catalyst 完全无法优化；这是 RDD 的最大代价 | 《Spark 大数据实时计算》第 6 章 vs 第 8–9 章 |
| 4 | 「表里有 1 亿行，SQL 里写了过滤，所以只扫一点点」 | 必须确认 **Parquet/ORC 的统计信息生效 + 谓词下推生效**，否则是全表扫描 | 《Spark 大数据实时计算》第 9 章 |
| 5 | 🔧 本书未覆盖 **ANSI 模式** | 2026 年的 Spark 4.x 正在把 ANSI SQL 语义**默认开启**：隐式转换、越界 CAST、数字溢出都会**从静默变成报错**。老 SQL 迁移必须测 | 《Spark 大数据实时计算》第 8–9 章 |
| 6 | 🔧 本书未覆盖 **DPP（动态分区裁剪）** | 3.x 起默认开启，在 join 时把过滤推到扫描侧；**分区表上收益可达数量级** | 《Spark 大数据实时计算》第 8 章（写作时 DPP 尚未成为默认） |
| 7 | 🔧 本书未覆盖 **AQE（自适应查询执行）** | AQE 把静态优化变成运行时优化：自动 broadcast join、合并小分区、倾斜拆分。**这是 Spark 性能优化中最重要的一次变化** | 《Spark 大数据实时计算》第 7、9 章；详见 `05` |
| 8 | 🔧 本书未覆盖 **Photon / 向量化执行的竞争** | 2026 年执行层的竞争在「向量化 + 编译执行 + 列格式」；Spark 之外还有 Velox、DuckDB、ClickHouse、Trino | 《Spark 大数据实时计算》第 9 章；详见 `10` |

---

## 七、与其他章 / 其他书的联系

**本目录内部**：

- **`02-Spark核心与RDD模型.md`**：`02` 讲 RDD 的血缘与 stage；`04` 讲同一份计算的**结构化与优化版本**。两者是「一条流水线上的前后两个抽象」。
- **`03-Shuffle与宽依赖.md`**：Catalyst 决定**是否产生宽依赖**（join 策略选择），`03` 讲宽依赖**产生之后**的代价。
- **`05-Spark性能优化.md`**：本章的 AQE/DPP/统计信息在 `05` 中并入调优清单。
- **`09-存储与文件格式.md`**：谓词下推与列裁剪能否生效，取决于文件格式与统计信息，在 `09` 中展开。
- **`10-计算引擎的演进.md`**：Spark 2/3/4 与 Flink、Lakehouse 的对比在 `10`。

**其他书**：

- **`book/数据库系统概念6/12-查询处理.md`**：**必须对照阅读**。Spark SQL 的执行流程（解析/优化/执行）就是数据库的 Standard Query Processing 步骤；`12` 讲「怎么把一个 SQL 变成执行计划」，`04` 讲「Spark 怎么在集群上执行这个计划」。
- **`book/数据库系统概念6/13-查询优化.md`**：Catalyst 的规则与 CBO 与数据库的逻辑改写、物理计划选择是一一对应的。
- **`book/数据库系统概念6/11-索引与散列.md`**：**Spark 不用索引这件事在此对照**。Spark 靠列存 + 统计信息 + 扫描，而不是 B+ 树；这也解释了为什么 Spark 在「点查 + 更新」场景远不如数据库。
- **`book/数据库系统概念6/26-高级事务处理.md`**：Spark 缺事务，直到表格式（Delta/Iceberg/Hudi，见 `10`）才补上；`26` 讲的 WAL、MVCC、隔离级别正是那一层的理论来源。
- **`book/多处理器编程的艺术2/16-调度与工作分配.md`**：Whole-stage codegen 的产物在集群上执行时，仍然受「本地性 + 窃取」调度支配。
