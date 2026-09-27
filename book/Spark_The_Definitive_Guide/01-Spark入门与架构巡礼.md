# 01 — Spark 入门与架构巡礼

> 原书 Ch 1: A Gentle Introduction to Spark
> 原书 Ch 2: A Tour of Spark's Toolset

---

## Ch 1 核心：什么是 Spark

✅ **统一分析引擎**：Spark 不是单纯的批处理框架，而是覆盖批处理、交互式查询、流处理、机器学习的统一平台。

✅ **核心设计哲学**：
- **内存计算** (In-Memory Computing)：中间结果缓存于内存，避免重复磁盘 I/O
- **惰性求值** (Lazy Evaluation)：Transformation 只记录逻辑计划，Action 才触发执行
- **声明式 API**：用户描述"要什么"，Catalyst 优化器决定"怎么做"
- **统一数据抽象**：DataFrame 同时服务批处理和流处理

### Spark vs Hadoop MapReduce

| 维度 | MapReduce | Spark |
|------|-----------|-------|
| 中间数据存储 | 磁盘 (HDFS) | 内存 (可溢出到磁盘) |
| 执行模型 | Map → Reduce 两阶段 | DAG 多阶段 |
| 迭代计算 | 每轮重写 HDFS | 内存缓存 RDD |
| API 层级 | 低层 Map/Reduce | 高层 DataFrame/SQL |
| 延迟 | 分钟级 | 秒级（内存命中时） |

### 关键概念：RDD 初探

```scala
// 最简 RDD 操作
val data = Seq(1, 2, 3, 4, 5)
val rdd = sc.parallelize(data)
val doubled = rdd.map(x => x * 2)  // Transformation (惰性)
doubled.collect()                    // Action (触发执行)
```

⚠️ RDD 是底层 API，本书推荐优先使用 DataFrame API（性能更优，Catalyst 可优化）。

---

## Ch 2 核心：Spark 工具集巡礼

### Spark 生态系统全景

```
Spark 工具集
├── Spark SQL        — 结构化数据处理 (DataFrame + SQL)
├── Spark Streaming  — 流处理 (微批模型 → Structured Streaming)
├── MLlib            — 分布式机器学习库
├── GraphX           — 图计算 (仅 Scala)
└── Spark Core       — 任务调度、内存管理、I/O 管理
```

### Spark SQL：最常用组件

✅ DataFrame API + SQL 查询的统一接口
✅ Catalyst 优化器自动重写查询计划
✅ 支持 JSON / Parquet / CSV / JDBC / Hive 等多种数据源

```python
# PySpark 示例
df = spark.read.json("people.json")
df.where("age > 21").select("name", "age").show()

# 等价 SQL
spark.sql("SELECT name, age FROM people WHERE age > 21").show()
```

### MLlib：分布式机器学习

✅ 基于 DataFrame 的 ML Pipeline API
✅ 内置分类、回归、聚类、协同过滤等算法
✅ 特征提取/转换/选择工具集

### Structured Streaming

✅ 基于 Spark SQL 引擎的流处理
✅ 与批处理共享 API（同一套 DataFrame 操作）
✅ 支持 Event-Time 处理、Watermark、Output Mode

### Spark 运行模式

| 模式 | 场景 | 说明 |
|------|------|------|
| local[N] | 开发/测试 | 单机 N 线程 |
| Standalone | 小型集群 | Spark 自带集群管理器 |
| YARN | 企业级 | Hadoop YARN 资源管理 |
| Kubernetes | 云原生 | K8s 容器编排 |
| Mesos | ⚠️ 已弃用 | Spark 3.0+ 不再支持 |

### SparkSession：统一入口

```scala
// Spark 2.0+ 统一入口
val spark = SparkSession.builder()
  .appName("MyApp")
  .master("local[*]")
  .config("spark.sql.shuffle.partitions", "200")
  .getOrCreate()
```

⚠️ 本书基于 Spark 2.x；Spark 4.x 中 SparkSession 仍为入口，但 Spark Connect 改变了客户端连接方式。

---

## 🔧 DuckDB / SQLite 类比

> 以下类比均为辅助理解，**非本书引擎行为**。

🔧 **类比 1：Spark DataFrame ≈ DuckDB 表**
- DuckDB 的 `SELECT * FROM table WHERE age > 21` 与 Spark 的 `df.where("age > 21")` 语义等价
- 差异：DuckDB 单机 OLAP；Spark 分布式计算
- ⚠️ 非本书引擎行为

🔧 **类比 2：Spark lazy evaluation ≈ DuckDB 查询优化**
- DuckDB 也有逻辑计划→物理计划的优化过程（类似 Catalyst）
- DuckDB 的 `EXPLAIN` 类似 Spark 的 `df.explain()`
- ⚠️ 非本书引擎行为

🔧 **类比 3：SparkSession ≈ DuckDB Connection**
- `SparkSession.builder().getOrCreate()` ≈ `duckdb.connect()`
- 都是操作的统一入口点
- ⚠️ 非本书引擎行为

🔧 **类比 4：spark.read.json/csv ≈ DuckDB read_json_auto/read_csv_auto**
- 两者都支持自动推断 Schema 读取半结构化文件
- DuckDB 的 `read_json_auto` 更智能（自动处理嵌套）；Spark 需要 `multiLine=true` 等配置
- ⚠️ 非本书引擎行为

---

## 核心概念速览（中英对照）

| 中文 | English | 简述 |
|------|---------|------|
| 统一分析引擎 | Unified Analytics Engine | Spark 的定位：批+流+ML+SQL |
| 惰性求值 | Lazy Evaluation | Transformation 延迟到 Action 执行 |
| Spark 会话 | SparkSession | 2.0+ 统一编程入口 |
| 弹性分布式数据集 | RDD | 底层分布式数据抽象 |
| 转换 | Transformation | 惰性操作，返回新 Dataset |
| 行动 | Action | 触发执行，返回结果或写数据 |
| 有向无环图 | DAG | 任务执行的依赖图 |
| 微批处理 | Micro-Batch Processing | Structured Streaming 默认模型 |

---

## 最新演进与工业实践

**Spark 3.x → 4.x 关键变更（书后发展）：**

| 变更 | 版本 | 影响 |
|------|------|------|
| Spark Connect | 3.4+ | 客户端-服务器架构，解耦 Driver 与客户端 |
| pandas API on Spark | 3.2+ | PySpark 原生支持 pandas 接口 |
| Photon 引擎 | 3.5+ | Databricks 原生向量引擎集成 |
| R API 废弃 | 4.0 | SparkR 不再维护 |
| Scala 2.13 only | 4.0 | 2.12 支持移除 |

> 来源: spark.apache.org ✅

**工业实践（2026）：**
- Spark Connect 正在成为 PySpark 客户端的默认连接方式
- Databricks Runtime (Photon) 在商业场景中替代部分 JVM 执行
- 本地开发中 DuckDB 正成为 Spark 的轻量替代品（→ 见 🔧 类比）
- 相关参考: [Data_Lakehouse_in_Action](../Data_Lakehouse_in_Action/05-加工层计算引擎与存算分离.md) 对 Spark 在湖仓架构中的定位有详细讨论
