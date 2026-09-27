# 06 — Spark SQL 与 Dataset

> 原书 Ch 10: Spark SQL
> 原书 Ch 11: Datasets

---

## Ch 10 核心：Spark SQL

### Spark SQL 的定位

✅ **Spark SQL 是 Spark 中处理结构化数据的统一接口**：
- 提供 SQL 查询能力（兼容 HiveQL）
- DataFrame API 底层由 Spark SQL 引擎执行
- Catalyst 优化器自动优化查询计划

### Catalyst 优化器

```
SQL/DataFrame API
       ↓
  解析 (Analysis)          ← 解析列名、表名、类型
       ↓
  逻辑计划 (Logical Plan)  ← 未优化的逻辑表示
       ↓
  优化逻辑计划 (Optimized Logical Plan) ← 谓词下推、列裁剪等
       ↓
  物理计划 (Physical Plan) ← 选择具体算法（Hash Join / Sort Merge Join）
       ↓
  代码生成 (Code Generation) ← Tungsten 二进制处理
       ↓
  执行 (Execution)
```

✅ **Catalyst 的四大优化阶段**：
1. **Analysis（分析）**：解析未解析的逻辑计划，绑定表/列引用
2. **Logical Optimization（逻辑优化）**：谓词下推、常量折叠、子查询消除
3. **Physical Planning（物理计划）**：选择 Join 算法、扫描策略
4. **Code Generation（代码生成）**：生成 Java 字节码（Whole-Stage CodeGen）

### 查看执行计划

```python
df.explain()                    # 简要物理计划
df.explain(True)                # 完整计划（含逻辑计划）
df.explain(mode="formatted")    # 格式化输出 (3.x+)
```

### Spark SQL 内置函数

| 类别 | 示例函数 |
|------|----------|
| 聚合 | `sum`, `avg`, `count`, `min`, `max`, `collect_list` |
| 字符串 | `concat`, `substring`, `trim`, `upper`, `lower`, `regexp_extract` |
| 日期 | `current_date`, `date_add`, `datediff`, `date_format`, `to_date` |
| 窗口 | `rank`, `row_number`, `lag`, `lead`, `ntile` |
| 条件 | `when().otherwise()`, `coalesce`, `nullif` |
| 复杂类型 | `explode`, `split`, `struct`, `array`, `map` |

### Hive 兼容性

✅ Spark SQL 兼容大部分 HiveQL 语法
✅ 可直接读取 Hive Metastore 中的表定义
⚠️ Hive UDF 可用但性能不如原生 Spark UDF

```python
# 连接 Hive
spark = SparkSession.builder \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("SELECT * FROM hive_db.hive_table").show()
```

### 临时视图与全局视图

```python
df.createOrReplaceTempView("people")       # Session 级
df.createOrReplaceGlobalTempView("people")  # Application 级 (global_temp. 前缀)
```

---

## Ch 11 核心：Dataset

### Dataset 的定位

✅ **Dataset = DataFrame + RDD 的优势**
- 像 DataFrame：被 Catalyst 优化
- 像 RDD：编译时类型安全（仅 Scala/Java）

```scala
// 强类型 Dataset
case class Employee(name: String, age: Int, salary: Double)
val ds: Dataset[Employee] = spark.read.json("emp.json").as[Employee]

// 类型安全操作
ds.filter(_.age > 21).map(_.name).show()
```

⚠️ **Dataset API 仅 Scala/Java 可用**；Python/R 只能用 DataFrame。
⚠️ Python 中 `pyspark.sql.DataFrame` 就是最终 API，无 Dataset 等价物。

### Dataset vs DataFrame vs RDD

| 特性 | DataFrame | Dataset | RDD |
|------|-----------|---------|-----|
| 类型安全 | 运行时 | 编译时 (Scala) | 编译时 |
| Catalyst 优化 | ✅ | ✅ | ❌ |
| 序列化 | Tungsten | Encoder | Java/Kryo |
| 语言 | 全部 | Scala/Java | 全部 |
| 推荐度 | ✅ 首选 | ✅ Scala 项目 | ⚠️ 仅必要时 |

### Encoder

✅ **Encoder 是 Dataset 的核心组件**：负责在 JVM 对象和 Spark 内部二进制格式之间转换。
✅ 内置 Encoder 覆盖常见类型；自定义类型需要 `Encoders.kryo[MyType]`

```scala
import org.apache.spark.sql.Encoders
val encoder = Encoders.kryo[MyCustomClass]
```

---

## 🔧 DuckDB / SQLite 类比

> 以下类比均为辅助理解，**非本书引擎行为**。

🔧 **类比 1：Catalyst 优化器 ≈ DuckDB 查询优化器 / SQLite 查询优化器**
- 三者都有 逻辑计划→物理计划 的优化流程
- DuckDB 优化器更现代（向量化执行）；SQLite 优化器相对简单
- Catalyst 的 Whole-Stage CodeGen 是独有特性 · ⚠️ 非本书引擎行为

🔧 **类比 2：临时视图 ≈ DuckDB VIEW / SQLite VIEW**
- `df.createOrReplaceTempView("t")` ≈ `CREATE VIEW t AS SELECT ...`
- Spark 临时视图仅 Session 有效；DuckDB/SQLite 可持久化 · ⚠️ 非本书引擎行为

🔧 **类比 3：Dataset 类型安全 ≈ DuckDB 列类型 / SQLite 类型亲和**
- Dataset 在编译时检查类型（Scala）
- DuckDB 严格类型系统；SQLite 动态类型（类型亲和）
- 三者对类型的严格程度不同 · ⚠️ 非本书引擎行为

🔧 **类比 4：spark.sql() ≈ DuckDB sql() / SQLite execute()**
- Spark: `spark.sql("SELECT * FROM t WHERE age > 21")`
- DuckDB: `con.sql("SELECT * FROM t WHERE age > 21")`
- SQLite: `cursor.execute("SELECT * FROM t WHERE age > 21")`
- 接口模式一致，底层执行引擎完全不同 · ⚠️ 非本书引擎行为

---

## 核心概念速览（中英对照）

| 中文 | English | 简述 |
|------|---------|------|
| Catalyst 优化器 | Catalyst Optimizer | Spark SQL 查询优化框架 |
| 逻辑计划 | Logical Plan | 查询的逻辑表示 |
| 物理计划 | Physical Plan | 具体执行策略 |
| 代码生成 | Whole-Stage Code Generation | 生成 Java 字节码加速执行 |
| 临时视图 | Temp View | Session 级的命名引用 |
| 数据集 | Dataset | 强类型分布式数据抽象 |
| 编码器 | Encoder | JVM 对象 ↔ 二进制格式转换器 |
| 谓词下推 | Predicate Pushdown | 将过滤条件下推到数据源 |

---

## 最新演进与工业实践

**Spark SQL 与 Dataset 的演进（书后发展）：**

| 演进 | 版本 | 影响 |
|------|------|------|
| AQE (Adaptive Query Execution) | 3.0 GA | 运行时动态调整 Join 策略和分区数 |
| Dynamic Partition Pruning | 3.0+ | 运行时裁剪不需要的分区 |
| Variant 类型 | 4.0+ | 半结构化数据原生支持 |
| Spark Connect | 3.4+ | SQL/DataFrame 可远程执行 |
| Photon (Databricks) | 3.5+ | 非 JVM 向量引擎替代 Tungsten |

> 来源: spark.apache.org ✅

**工业实践（2026）：**
- AQE 已成为生产默认配置；动态 Join 策略选择消除了大量手动调优
- Dataset API 在 Python 生态中无对应物；PySpark 用户直接用 DataFrame
- DuckDB 的查询优化器设计受 Catalyst 启发，但走向量执行路线
- 相关参考: [bigdata/04-SparkSQL与结构化数据](../bigdata/04-SparkSQL与结构化数据.md) 对 Catalyst 有更详细讨论
