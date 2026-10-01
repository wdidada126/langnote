# 03 · Apache Spark 结构化 API

> 原书第 3 章（Apache Spark's Structured APIs）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原；正文为精读重构，Spark 行为 = ⚠️ 转述 + spark.apache.org 文档实链。本章是全书技术心脏、也是与 1e 分歧最大的一章（RDD 从主角降为一节）。对位：[bigdata 02 RDD 模型](../bigdata/02-Spark核心与RDD模型.md)、[TDG 03 结构化 API 概览](../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md)、[TDG 07 RDD 底层](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md)。

## 3.1 RDD 之下是什么（章内第一节）

RDD 是 Spark 的底层通用抽象：分布式不可变对象集合 + 血缘（lineage）容错 + 分区级并行。2e 的立场旗帜鲜明：**"从 RDD 开始写 Spark 是 2015 年的正确、2020 年的弯路"**——除非处理非结构化文本的极端定制场景，一律先试结构化 API。RDD 保留通道（`df.rdd` / `spark.createDataFrame(rdd)`），共享变量（broadcast/accumulator）归入 RDD 侧讨论。

## 3.2 结构化 Spark：DataFrame 一侧

- **基本类型 ↔ SQL 类型**：StringType/IntegerType/… 与 DDL 字符串（`"id BIGINT, name STRING"`）互译；
- **复杂类型**：ArrayType/MapType/StructType——原书强调"嵌套是现代数据的第一形状"（JSON/Parquet 天然嵌套），配套 `col.a.b`、`explode`、`getElement` 等取数语法（⚠️ 转述）；
- **Schema 两定义法**：代码式（StructField 树）与 DDL 式字符串；`printSchema()` 检查；
- **列与表达式**：Column = 表达式树的节点，`df.select(col("x") + 1)` 记的是"计划"不是"值"；
- **行**：Row = 带序字段袋，可索引可解包；
- **常用 DataFrame 操作**：select/filter/withColumn/drop/distinct/order_by/limit（语义与 SQL 对应）；
- **DataFrameReader/Writer**：`spark.read.format(...).option(...).load(...)` 与 `df.write...`——第 4/5 章整两章展开；
- **转换与操作**：transformations（惰性）vs actions（count/show/collect/write），惰性是"可以整体优化"的前提。

## 3.3 Dataset API 一侧（类型化）

- **类型化 vs 无类型**：Dataset[T] 编译期类型安全（Scala）；Python 里 Dataset≡DataFrame（**没有类型化 Dataset**——2e 明说这是 API 统一后的历史不对称）；
- **Scala case class 建 Dataset**；`map` 在 Dataset 上是真用户代码（走 JVM 对象）、在 DataFrame 上是表达式操作（走 codegen）——**性能差异的第一解释点**；
- **Encoder**：类型化行与内部 UnsafeRow 之间的编解码器（⚠️ 转述）；
- **端到端示例**：读取→类型化 map→聚合→写出；
- **DataFrame vs Dataset 对照**：2.0 合并后，DataFrame = Dataset[Row] 的别名；日常工程默认 DataFrame。

## 3.4 何时还用 RDD（小节）

非结构化逐行定制、需要精细控制分区器/持久化语义、遗留代码迁移。教学结论：**RDD 是逃生通道，不是入口**。1e 全书的 RDD 章节体量为迁移者保留——盘上中文社区 2016–2019 年的大量 RDD 笔记（如对位 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)）在 2e 世界观下要整体"降半格"看待。

## 3.5 Catalyst 优化器四阶段（章末高潮）

⚠️ 转述（口径同时对照 Spark SQL 论文 Armbrust et al., SIGMOD 2015，DOI `10.1145/2723372.2742797` ✅ Crossref，论文线语境见 [../../db/db.md](../../db/db.md)）：

1. **分析**：未解析逻辑计划（字符串列名）→ 解析逻辑计划（绑 catalog）；
2. **逻辑优化**：谓词下推、列裁剪、常量折叠等规则改写；
3. **物理规划**：生成候选物理计划（join 策略选择等），代价模型/启发式选优；
4. **代码生成**：Whole-stage codegen 把算子熔成 Java 字节码，减虚调用与物化。

🔧 **概念类比实测（非本书 Spark 引擎行为）**：DuckDB 同样"逻辑→物理→向量化执行"，用 `EXPLAIN SELECT ... JOIN ... GROUP BY` 得 `HASH_JOIN + HASH_GROUP_BY + SEQ_SCAN`（meas.txt G4 组）——可拿它当 Catalyst 输出的"单机替身"建立直觉：列名解析失败即报错、计划树文本可读、谓词自动下进扫描。**差别**：Spark 多了分布式切片（分区）与 shuffle 决策维度，且 codegen 粒度是整段 stage；DuckDB 无这些概念。

🔧 **惰性 vs 物化实测（同上 G6，非 Spark 行为）**：见第 2 章 SQLite 视图组；DuckDB 侧对照：视图首读 17.8ms（现场算）vs CTAS 后复读 0.63ms（已物化）——把 Spark "缓存 DataFrame（`persist`/`cache`）" 的直觉先在这里建立，第 7 章回收。

## 3.6 本章的工程判断（重构观点）

- 结构化 API 的红利不是"语法像 SQL"，而是**引擎拿到了 schema**：才能做列裁剪、类型检查、codegen、格式下推。写 RDD 等于把 schema 还给用户自己管。
- Python 用户没有类型化 Dataset 不是损失而是聚焦：PySpark 的"类型"路线后来由 pandas API on Spark（类型注解 + Arrow）接力——书出版时该线已萌芽（⚠️ 演进节展开）。

## 3.7 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| Spark：RDD 底层是什么？ | 3.1 |
| 结构化 Spark／关键优势和益处 | 3.2 首段 |
| DataFrame API | 3.2 |
| Spark 的基本数据类型 | 3.2 第一条 |
| Spark 的结构化和复杂数据类型 | 3.2 第二条 |
| Schema 和创建 DataFrame／两种定义模式的方式 | 3.2 第三条 |
| 列和表达式 | 3.2 第四条 |
| 行 | 3.2 第四条旁 |
| 常见的 DataFrame 操作 | 3.2 第五条 |
| 使用 DataFrameReader 和 DataFrameWriter | 3.2 第六条（4/5 章主场） |
| 转换和操作（惰性/动作） | 3.2 第七条 |
| 端到端 DataFrame 示例 | 3.8 重建代码 |
| Dataset API／类型化·无类型·通用行 | 3.3 |
| 创建数据集／Scala：案例类 | 3.3 第二、三条 |
| 数据集操作／端到端数据集示例 | 3.3 |
| 数据帧与数据集 | 3.3 末条 |
| 何时使用 RDDs | 3.4 |
| Spark SQL 和底层引擎／Catalyst（阶段 1 分析→2 逻辑优化→3 物理规划→4 代码生成）／概要 | 3.5 |

## 3.8 重建示例：schema→惰性→计划（本目录重做，非原书清单；⚠️ API 语义转述官方文档）

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("ch03").getOrCreate()

# schema 两种定义法之一：DDL 字符串
df = spark.createDataFrame([(1, "ann", 9.5), (2, "bob", None)], "id INT, name STRING, score DOUBLE")

# 列=表达式：登记的是计划树
plan = df.filter(df.score > 8).select("name")
plan.explain(True)   # == Parsed/Analyzed/Optimized/Physical 四段——Catalyst 的 X 光片
# OptimizedPlan 里应看到 PushedFilters 与只投影 name 列（列裁剪）；== ⚠️ 本目录未执行，口径转述
plan.show()          # action：此刻才编译执行
```

对照 🔧 G1（DuckDB 同型实验，第 4 章）与 G4/G6（第 6/7 章）：计划树可读、下推可见、物化可量化——三件事在任何现代引擎里是同构的，Spark 只是把它放到分区尺度上。

## 3.9 课堂问题（答不出回本文件）

1. "引擎拿到 schema"具体解锁了哪四件事？（3.6 第一条）
2. DDL 式与 StructType 式各适合什么团队流程？
3. `filter` 之后 `count` 之前，数据动了吗？谁在动？
4. Catalyst 阶段 2 与阶段 3 的分工一句话（规则 vs 策略）？
5. Python 用户的"类型感"替代品时间线（3.6 末条→演进节）？
6. `df.rdd` 什么时候合理？给出两个场景（3.4）。

## 核心概念速览（中英对照）

- **RDD** — Resilient Distributed Dataset：血缘容错的底层分布式集合；本书定位为逃生通道。
- **DataFrame** — 带 schema 的分布式表；全书主 API。
- **Dataset[T]** — 类型化分布式集合（Scala 专属红利）。
- **Encoder** — 类型化行与 UnsafeRow 的编解码器。
- **Column/Expression** — 列即表达式树节点：记计划不记值。
- **Schema（DDL/StructType）** — 两种定义路径：字符串 DSL 或对象树。
- **复杂类型** — Array/Map/Struct：嵌套是一等公民。
- **Transformation/Action** — 惰性登记/物化触发两段式。
- **Catalyst** — 规则+代价双驱动的查询优化器框架。
- **逻辑计划/物理计划** — 优化前后两棵树；join 策略在物理侧选定。
- **Whole-Stage CodeGen** — 整段算子融合生成字节码的执行技术。
- **Broadcast/accumulator** — 只读广播变量与聚合累加器（RDD 侧共享变量）。
- **UnsafeRow** — Tungsten 时代的二进制行布局（⚠️ 术语出处为官方文档）。

## 最新演进与工业实践

- **Spark 4.0**（✅ https://spark.apache.org/releases/spark-release-4-0-0.html）：Python Data Source API、Python UDTF、统一 UDF profiling——3.4–3.5 时代"Python 一等公民化"路线的延续；本章"Python 无类型化 Dataset"的表述在 4.x 依旧是事实，但 pandas API on Spark（`ps.DataFrame`，类型注解 + Arrow）已成为 Python 侧"结构化红利"的新载体。
- **Spark Connect**（4.0）：客户端-服务端分离后，Catalyst/代码生成完整保留在服务端（⚠️ 转述官方 release note：Connect API 覆盖面大扩展、ML on Connect）——"瘦客户端 + 远端引擎"正在改写本章的教学入口（本地 shell → pip 瘦客户端）。
- **优化器对读**：DuckDB/ClickHouse 等单机/向量引擎证明"逻辑计划→向量化"同样能快；工业界 2024–2026 的分工是：交互式分析偏 DuckDB/ClickHouse，超宽表 PB 级批流偏 Spark AQE——不是替代而是分层。
- **RDD 现状**：官方仍支持（✅ https://spark.apache.org/docs/latest/rdd-programming-guide.html curl 200），但社区新增算子基本不再落 RDD 层；GraphX 是 RDD 最后的"活化石"用户。
- **对读**：RDD 心法与血缘调试的中文实战叙述见 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)；结构化 API 全量操作手册式覆盖见 [../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md](../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md)。
