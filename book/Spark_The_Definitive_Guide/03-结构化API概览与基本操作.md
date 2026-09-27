# 03 — 结构化 API 概览与基本操作

> 原书 Ch 4: Structured API Overview
> 原书 Ch 5: Basic Structured Operations

---

## 结构化 API 三层体系

✅ **Spark 2.0+ 的统一结构化 API**：DataFrame 和 Dataset 共享同一套操作接口。

```
结构化 API 层次
├── 最高层: SQL 语法 (最声明式)
├── 中间层: DataFrame API (推荐, Catalyst 可优化)
└── 底层: Dataset API (仅 Scala/Java, 类型安全)
```

⚠️ Dataset API 仅 Scala/Java 可用；Python/R 只能用 DataFrame。
✅ 无论使用哪层 API，最终都编译为相同的 Logical Plan → Catalyst 统一优化。

### DataFrame 的本质

✅ **DataFrame = 分布式数据表 + Schema 元信息**
- 逻辑上等价于一张数据库表
- 物理上分布在多个 Partition 上
- 每行数据类型为 `Row`（无编译时类型检查）

```scala
// DataFrame 创建
val df = spark.read.json("/path/to/file.json")

// 查看 Schema
df.printSchema()
// root
//  |-- age: long (nullable = true)
//  |-- name: string (nullable = true)

// 查看 Plan
df.explain()  // 输出 Logical Plan → Physical Plan
```

---

## Ch 4 核心：Schema 与类型系统

### Spark 数据类型（精选）

| Spark 类型 | Python 类型 | SQL 类型 | 说明 |
|-----------|-------------|----------|------|
| IntegerType / LongType | int | INT / BIGINT | 整数 |
| FloatType / DoubleType | float | FLOAT / DOUBLE | 浮点 |
| StringType | str | STRING | 字符串 |
| BooleanType | bool | BOOLEAN | 布尔 |
| DateType / TimestampType | date / datetime | DATE / TIMESTAMP | 时间 |
| ArrayType / MapType / StructType | list / dict / Row | ARRAY / MAP / STRUCT | 复杂类型 |

### StructType 与 StructField

```scala
import org.apache.spark.sql.types._

val schema = StructType(Seq(
  StructField("name", StringType, nullable = true),
  StructField("age", IntegerType, nullable = false),
  StructField("address", StructType(Seq(
    StructField("city", StringType),
    StructField("state", StringType)
  )))
))
```

✅ `StructType` 是 `StructField` 的集合，定义 DataFrame 的列结构
✅ Schema 可以在读取时指定（`schema` 参数），避免推断开销

---

## Ch 5 核心：基本操作详解

### 行与列操作

```python
# 选择列
df.select("name", "age")
df.select(col("name"), col("age"))
df.selectExpr("name", "age + 1 AS age_plus_one")

# 过滤
df.where(col("age") > 21)
df.filter("age > 21")  # SQL 字符串形式

# 新增列
df.withColumn("age_plus_one", col("age") + 1)

# 删除列
df.drop("age")

# 重命名列
df.withColumnRenamed("name", "full_name")
```

### 列表达式 (Column Expressions)

✅ **Column 对象是一等公民**：支持 `+`, `-`, `*`, `/`, `%` 运算符，以及 `like()`, `between()`, `isin()` 等方法。
✅ 常用函数：`lower`, `upper`, `concat`, `round`, `ceil`, `floor`, `abs`（来自 `pyspark.sql.functions`）

### 行操作

```python
df.union(newRow)                              # 合并行
df.distinct() / df.dropDuplicates("name")     # 去重
df.sample(False, 0.1, seed=42)                # 采样
df.randomSplit([0.8, 0.2], seed=42)           # 切分 (ML 常用)
df.sort(col("age").desc).limit(10)            # 排序 + 限制
df.show()        # 打印前 20 行
df.collect()     # 收集到 Driver (⚠️ 大数据慎用)
df.count()       # 行数 (触发 Action)
```

---

## 🔧 DuckDB / SQLite 类比

> 以下类比均为辅助理解，**非本书引擎行为**。

🔧 **类比 1：DataFrame.select ≈ DuckDB/SQLite SELECT**
- DuckDB: `SELECT name, age FROM df WHERE age > 21` ≈ Spark: `df.select("name","age").where(col("age")>21)`
- 语义等价；Spark 额外经过 Catalyst 优化 · ⚠️ 非本书引擎行为

🔧 **类比 2：withColumn ≈ SQL 计算列**
- DuckDB: `SELECT *, age+1 AS age_plus FROM df` ≈ Spark: `df.withColumn("age_plus", col("age")+1)`
- DuckDB 单条 SQL 完成；Spark 分步构建逻辑计划 · ⚠️ 非本书引擎行为

🔧 **类比 3：Schema 推断 ≈ DuckDB read_csv_auto**
- DuckDB: `read_csv_auto('file.csv')` ≈ Spark: `spark.read.csv("file.csv", inferSchema=true)`
- 两者都建议生产环境显式指定 Schema · ⚠️ 非本书引擎行为

🔧 **类比 4：collect() ≈ DuckDB.fetchall() / SQLite.fetchall()**
- 都是将数据拉取到客户端内存；大数据集都可能 OOM · ⚠️ 非本书引擎行为

---

## 核心概念速览（中英对照）

| 中文 | English | 简述 |
|------|---------|------|
| 结构化 API | Structured API | DataFrame + Dataset 统一接口 |
| Schema | Schema | DataFrame 的列名与类型定义 |
| 列表达式 | Column Expression | 可组合的计算单元 |
| 惰性求值 | Lazy Evaluation | Transformation 不立即执行 |
| 行对象 | Row | DataFrame 中一行的数据表示 |
| 结构类型 | StructType | 列定义的集合 |
| 结构字段 | StructField | 单列的名称、类型、可空性 |
| 去重 | Drop Duplicates | 基于指定列去重 |
| 采样 | Sample | 按比例随机抽取数据 |

---

## 最新演进与工业实践

**结构化 API 的演进（书后发展）：**

| 演进 | 版本 | 影响 |
|------|------|------|
| Dataset API 增强 | 2.x | Scala/Java 类型安全，编译时检查 |
| pandas API on Spark | 3.2+ | PySpark 支持 pandas 接口操作 DataFrame |
| Spark Connect | 3.4+ | DataFrame API 可通过 gRPC 远程调用 |
| Arrow 优化 | 2.3+ | PySpark ↔ JVM 数据传输使用 Apache Arrow |
| Variant 类型 | 4.0+ | 半结构化数据的新类型（类 JSON） |

> 来源: spark.apache.org ✅

**工业实践（2026）：**
- pandas API on Spark (`pyspark.pandas`) 已成为 PySpark 用户的默认选择
- Spark Connect 使得 Python 客户端不再需要 JVM 环境
- Apache Arrow 作为跨语言数据交换标准，已被 DuckDB / Spark / Pandas 共同采用
- 相关参考: [Data_Lakehouse_in_Action](../Data_Lakehouse_in_Action/04-存储层对象存储文件格式与分区.md) 讨论了 Schema 演进与文件格式的关系
