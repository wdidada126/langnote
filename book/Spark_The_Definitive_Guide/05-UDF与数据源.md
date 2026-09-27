# 05 — UDF 与数据源

> 原书 Ch 8: User-Defined Functions
> 原书 Ch 9: Data Sources

---

## Ch 8 核心：用户自定义函数

### UDF 的三种形式

| 类型 | 语言 | 性能 | 说明 |
|------|------|------|------|
| Scala UDF | Scala | ⚠️ 慢 | 序列化开销大，无法被 Catalyst 优化 |
| Python UDF | Python | ⚠️ 慢 | JVM↔Python 进程间通信开销 |
| pandas UDF (Vectorized) | Python | ✅ 快 | Apache Arrow 传输，向量化执行 |

```python
# 普通 Python UDF (慢)
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def normalize_name(name):
    return name.strip().lower() if name else None

df.withColumn("norm_name", normalize_name(col("name")))
```

```python
# pandas UDF (快, Spark 2.3+)
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf(returnType="double")
def multiply(salary: pd.Series, factor: float) -> pd.Series:
    return salary * factor

df.withColumn("new_salary", multiply(col("salary"), lit(1.1)))
```

⚠️ **核心原则**：优先使用内置函数（Catalyst 可优化）；UDF 是最后手段。
⚠️ 普通 Python UDF 每行需 JVM↔Python 往返；pandas UDF 批量传输，快 10-100x。

### UDF 注册与 SQL 调用

```python
# 注册为 SQL 函数
spark.udf.register("normalize", normalize_name)
spark.sql("SELECT normalize(name) FROM people")
```

### Hive UDF 兼容

✅ Spark 可直接使用 Hive UDF/UDAF/UDTF（需 `hive.exec` jar 在 classpath）

---

## Ch 9 核心：数据源

### 通用读写接口

```python
# 读取
spark.read.format("json|parquet|csv|jdbc|orc").load("path")
spark.read.json("path")  # 快捷方式

# 写入
df.write.format("parquet").mode("overwrite").save("path")
df.write.parquet("path")  # 快捷方式
```

### 写入模式 (SaveMode)

| 模式 | 行为 |
|------|------|
| `append` | 追加到已有数据 |
| `overwrite` | 覆盖已有数据 |
| `errorifexists` | 存在则报错（默认） |
| `ignore` | 存在则忽略（不报错） |

### 各数据源特性

| 数据源 | 压缩 | Schema 嵌入 | 列式 | 谓词下推 | 推荐场景 |
|--------|------|------------|------|----------|----------|
| **Parquet** | ✅ 默认 Snappy | ✅ | ✅ | ✅ | 首选存储格式 |
| **ORC** | ✅ 默认 ZLIB | ✅ | ✅ | ✅ | Hive 生态兼容 |
| **CSV** | ❌ | ❌ | ❌ | ❌ | 数据交换/导入 |
| **JSON** | ❌ | ❌ | ❌ | ❌ | 半结构化数据 |
| **JDBC** | N/A | N/A | N/A | ✅ | 数据库对接 |

✅ **Parquet 是 Spark 的默认格式**，与 Catalyst 优化器深度集成。

### 分区与分桶

```python
# 按列分区写入
df.write.partitionBy("year", "month").parquet("data/")

# 分桶 (Bucket) — 优化 Join
df.write.bucketBy(4, "department").sortBy("name").saveAsTable("emp")
```

⚠️ 分区目录结构：`data/year=2024/month=01/` — 查询时自动分区裁剪 (Partition Pruning)

### JDBC 数据源

```python
# 读取数据库
df = spark.read.jdbc(url="jdbc:postgresql://host/db",
                     table="employees",
                     properties={"user":"u", "password":"p"})

# 写入数据库 (注意 batch 大小)
df.write.jdbc(url="...", table="output",
             mode="append",
             properties={"batchsize": "10000"})
```

⚠️ JDBC 读写是常见瓶颈；建议用 `numPartitions` 控制并行度。

---

## 🔧 DuckDB / SQLite 类比

> 以下类比均为辅助理解，**非本书引擎行为**。

🔧 **类比 1：Parquet 读写 ≈ DuckDB 原生 Parquet / SQLite 无直接支持**
- DuckDB: `SELECT * FROM read_parquet('file.parquet')` 直接查询 Parquet
- Spark: `spark.read.parquet("file.parquet")` 同样原生支持
- SQLite 不支持 Parquet（需扩展） · ⚠️ 非本书引擎行为

🔧 **类比 2：JDBC 读写 ≈ DuckDB attach / SQLite 外部表**
- DuckDB: `ATTACH 'host' (TYPE POSTGRES)` 直接查询远程数据库
- Spark: `spark.read.jdbc(...)` 通过 JDBC 连接外部数据库
- 都是联邦查询的早期形式 · ⚠️ 非本书引擎行为

🔧 **类比 3：CSV 读写 ≈ DuckDB read_csv / SQLite .import**
- DuckDB: `read_csv_auto('file.csv')` 自动推断类型
- Spark: `spark.read.csv("file.csv", inferSchema=true, header=true)`
- 两者都支持自定义分隔符/引号/编码 · ⚠️ 非本书引擎行为

🔧 **类比 4：分区表 ≈ DuckDB Hive 分区 / SQLite 手动分区**
- DuckDB 支持读取 Hive 分区目录结构
- Spark 的 `partitionBy` 写入 `key=value/` 目录结构
- SQLite 无原生分区概念，需手动按表拆分 · ⚠️ 非本书引擎行为

---

## 核心概念速览（中英对照）

| 中文 | English | 简述 |
|------|---------|------|
| 用户自定义函数 | User-Defined Function (UDF) | 用户扩展的计算函数 |
| 向量化 UDF | pandas UDF / Vectorized UDF | 基于 Arrow 的批量 UDF |
| 数据源 | Data Source | 外部数据读写接口 |
| 写入模式 | Save Mode | 控制写入时如何处理已有数据 |
| 列式存储 | Columnar Storage | 按列组织数据（Parquet/ORC） |
| 谓词下推 | Predicate Pushdown | 将过滤条件下推到数据源层 |
| 分区 | Partition | 按列值组织数据目录 |
| 分桶 | Bucket | 按 Hash 组织数据文件 |

---

## 最新演进与工业实践

**UDF 与数据源的演进（书后发展）：**

| 演进 | 版本 | 影响 |
|------|------|------|
| pandas UDF 增强 | 3.0+ | 支持 Grouped Map / Grouped Agg / Window 三种类型 |
| Apache Arrow 默认 | 3.0+ | PySpark ↔ Pandas 零拷贝传输 |
| Delta Lake 集成 | 3.0+ | `spark.read.format("delta")` 成为湖仓标准 |
| Variant 类型 | 4.0+ | 替代 JSON 字符串的半结构化类型 |
| Spark Connect + 数据源 | 3.4+ | 远程客户端也可访问数据源 |

> 来源: spark.apache.org ✅

**工业实践（2026）：**
- Delta Lake / Iceberg / Hudi 已取代裸 Parquet 成为生产首选
- pandas UDF 已替代普通 Python UDF 成为 PySpark 推荐方式
- DuckDB 正成为本地 Parquet 查询的首选工具（替代 `spark.read.parquet`）
- 相关参考: [Data_Lakehouse_in_Action](../Data_Lakehouse_in_Action/04-存储层对象存储文件格式与分区.md) 详述了湖仓格式演进
