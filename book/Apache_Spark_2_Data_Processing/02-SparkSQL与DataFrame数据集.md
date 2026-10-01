# 02 SparkSQL 与 DataFrame/Dataset：2.0 大合并

> **取证态**：对应 Learning Path 主题「interactive querying with Spark SQL, using DataFrames and datasets」与仓库 Module_1/Chapter 6（含讲义 `B05868_09.key`）✅ 目录级实抓；章名级 TOC 不可得 ⚠️（00 §3）。Spark SQL 引擎行为不可本机实测 → ⚠️ 转述 + 官方 [SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)（✅ 可达）锚定；🔧 实验为**概念类比、非本书 Spark 引擎行为**。对位正读：[../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)。

## 1. 为什么说 2.0 是「SQL 路线的胜利」

Spark 1.x 里 DataFrame（Codegen 前的 SchemaRDD 后裔）与 RDD 并行，SQLContext/HiveContext 双轨；**2.0 将 SQL 能力并入 SparkSession、DataFrame 成为默认 API**，RDD 退居底座——本册通篇的「DataFrame 优先」教风即源自这一统合 ⚠️（转述官方发布口径）。

```scala
val df = spark.read.parquet("hdfs:/data/events")        // 2.x 标准读法
df.createOrReplaceTempView("events")                    // 注意：2.x 起 createTempView 已弃用
val top = spark.sql("""
  SELECT user_id, COUNT(*) c FROM events
  WHERE dt = '2019-05-01' GROUP BY user_id ORDER BY c DESC LIMIT 10""")
```

```python
# PySpark 2.x：没有 Dataset——类型化 API 仅 Scala/Java（时代事实）
from pyspark.sql.functions import col, count, desc
df.filter(col("dt") == "2019-05-01").groupBy("user_id") \
  .agg(count("*").alias("c")).orderBy(desc("c")).limit(10)
```

**Dataset 的昙花一现**：2.0 力推的 `Dataset[CaseClass]`（类型化 + Catalyst 优化兼得）在实践中因跨语言不对称（PySpark/R 拿不到）而热度衰减 ⚠️——本册正身处其巅峰期，是记录该 API 设计野心的史料层。

## 2. Catalyst 优化器与 Tungsten 执行引擎

- **四段流水线** ⚠️：Unresolved LogicalPlan →（Analyzer 借 Catalog 补 schema）→ Resolved →（Optimizer 规则改写：谓词下推/列裁剪/常量折叠/子列裁剪）→ PhysicalPlan 选型（Planner）→（Tungsten）代码生成 + 堆外内存管理执行。
- **whole-stage codegen**（2.0 起）：火山模型折叠为单函数循环，行数据以 CPU 寄存器传递 ⚠️。
- **数据源 SPI**：`spark.read.format(...).options(...)` 统一 Parquet/JSON/CSV/JDBC/Hive；Parquet 谓词下推 + 列裁剪是 2.x 教学的标准性能叙事 ⚠️。

### 🔧 E4 类比：惰性计划融合 vs 手工物化（DuckDB 1.5.5 / SQLite 3.45.3）

把「投影→过滤→聚合→排序取前 K」写成视图链再查询，DuckDB 的**单条物理计划**文本（约 2010 字符）内同时出现 `FILTER`、`HASH_GROUP_BY`、`TOP_N`、`PROJECTION`——过滤被下推进扫描、Top-K 与聚合融合，等价 Catalyst「全计划改写后再执行」。同一链在 SQLite 无优化器视角，需**三步 CREATE TABLE AS 物化**（2 万行耗时 6.8ms）才得到同一结果 `[g6:21439278.0, g4:21434994.0, g2:21430710.0, g0:21426426.0, g5:21422142.0]`。结论：差异不在结果而在**优化发生的位置**（计划期 vs 人工步骤）；**非 Spark 引擎实测**。

## 3. Hive 集成与元数据层（2.x 部署现实）

- `enableHiveSupport()` 挂接 Hive Metastore：UDF/serde/已有表复用，本书环境清单的 HDP 沙箱即为此场景服务 ⚠️。
- `spark.sql.warehouse.dir`、外部表/内部表分野、`INSERT OVERWRITE` 语义 ⚠️。
- 分区表发现（partition discovery）在 2.4 前后是运维高频话题 ⚠️ 转述，不展开版本细节以免臆写。

## 4. sparklyr 与 R-SQL 桥（SparkR 尾声的另一种写法）

```r
# sparklyr（README 时代环境）：dplyr 语法惰性翻译成 Spark SQL 再交 Catalyst
library(sparklyr)
sc <- spark_connect(master = "local", version = "2.4.0")
tbl(sc, "events") %>% filter(dt == "2019-05-01") %>%
  group_by(user_id) %>% summarise(c = n()) %>% arrange(desc(c))
```

dplyr→SQL 的翻译延迟与 Catalyst 的再优化，和 §2 的融合语义同构（计划期优化）——🔧 E4 可类比。R 线在本书年代的「教学繁荣/工程退潮」定位见 00 §4。

## 5. Dataset/UDF 的工程教训（本书年代语境）

- UDF 黑箱切断优化（谓词不能穿过）→ 优先内建函数 ⚠️；
- `collect()`/`toPandas()` 的 driver 内存悬崖是 2.x 教程反复告诫 ⚠️；
- Dataset 强类型带来的编译期安全 vs 演进摩擦（encoder 序列化成本）⚠️。
互见：[../Spark_The_Definitive_Guide/05-UDF与数据源.md](../Spark_The_Definitive_Guide/05-UDF与数据源.md)、[../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md](../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md)。

## 5.5 数据源矩阵与 SQL 常规面（2.x 教参汇总）

| 形态 | 读入口 | 关键项/教义 ⚠️ |
|---|---|---|
| Parquet | `spark.read.parquet(path)` | 列裁剪+谓词下推双红利；`mergeSchema` 处理 schema 演进 |
| JSON | `spark.read.json` | `multiLine`、损坏行进 `columnNameOfCorruptRecord` 的脏数据收纳口 |
| CSV | 2.x 起原生 `read.csv` | `header/sep/quote/escape`，`inferSchema` 逐列探型的代价告诫 |
| JDBC | `format("jdbc")` | `dbtable/predicate` 下推；`partitionColumn+lowerBound+upperBound+numPartitions` 并行读 |
| ORC/Hive | `enableHiveSupport()` | serde/bucketed 表复用（§3 元数据线） |
| 文本/二进制 | `textFile`（RDD 轨） | 行切分即 schema——非结构化「表化」入口（05 建图管线的前段） |

## 5.6 函数族、注册件与「同一计划的两个写法」

- 内建函数族四大张：字符串/数组-Map/窗口/聚合——`window(ts, "10 minutes")` 事件时间窗是 SQL 与结构化流（03）的**同一张脸**；
- `spark.udf.register("norm", fn)` 把 §5 的黑箱件挂进 SQL 目录——DataFrame 与 SQL 两写法在 Catalyst 里合成同一计划（🔧 E4 融合计划的教室同学）⚠️；
- 视图即计划复用：`createOrReplaceTempView` 之后，`spark.sql("SELECT ...")` 与 `df.filter(...)` 的差别只剩语法糖层级；
- 教参提醒（2.x 原声）：`spark.sql.*` 全家（warehouse/自动广播阈值 `autoBroadcastJoinThreshold` 等）写在会话 builder 里——**参数名即调优词汇表**，06 章的失效清单审计的就是这批名字 ⚠️。

## 5.7 时代差问答与自测（本章四问）

- **问：Dataset 为什么「昙花一现」？** 答：类型化收益只在 Scala/Java 侧兑现，跨语言生态（Python/R）拿不到对等物，工程界最终用「DataFrame+schema 校验+SQL 测试」替代了编译期承诺（§1）。
- **问：Catalyst 今天还成立吗？** 答：四段流水线的骨架完全成立，增量是 AQE 把「运行时统计」接回了计划回路（§2+演进表）。
- **问：UDF 还是原罪吗？** 答：黑箱切断优化的原理未变，缓解手段是 Arrow 化批式执行——「优先内建函数」教义在 4.x 仍然印在文档里（演进表 ⚠️ 项）。
- **问：🔧 E4 证明了什么、没证明什么？** 答：证明了「计划期融合 vs 人工物化」的形态差异是真实可观测的；没有证明 Spark 计划长得和 DuckDB 一样——跨引擎类比止于语义（00 §7）。

自测四题：① 说出 Analyzer 与 Optimizer 各解决什么「看不到」的问题；② `createOrReplaceTempView` 之后 SQL 与 DataFrame 写法在计划层还剩什么差别；③ Parquet 的哪两种下推各自省的是读放大还是算放大；④ 为什么 `collect()` 是教参级反模式。

## 5.8 一分钟带走（本册原声四句）

- 本册承诺位原声：`interactive querying with Spark SQL, using DataFrames and datasets`（✅ 官方 README 实抓）——2.x 合并叙事的正主。
- Dataset 一句断：类型化的甜头只发给了 Scala/Java，跨语言的苦头人人有份（§1）。
- 计划一句断：Catalyst 优化的是「怎么算」，SQL 与 DataFrame 两种写法只是「怎么说」（§5.7）。
- 一句戒：UDF 进计划如黑箱、手工档位如旧地图——它们的收尸仪式在 06 章演进表。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
|---|---|---|
| 结构化数据框架 | DataFrame | 带 schema 的分布式表，2.0 起 Spark 默认 API |
| 类型化数据集 | Dataset[T] | Scala/Java 独有的编译期强类型层，2.x 主推后热度回落 |
| 查询优化器 | Catalyst | 规则化逻辑改写+物理计划选择的可扩展优化框架 |
| 谓词下推 | Predicate Pushdown | 过滤条件前移至数据源/扫描层以减少读放大 |
| 列裁剪 | Column Pruning | 只读查询实际引用的列，列式文件格式的共生优化 |
| 全阶段代码生成 | Whole-Stage CodeGen | Tungsten 将算子树折叠为单函数循环的执行技术 |
| 堆外内存 | Off-heap Memory | Tungsten 摆脱 JVM GC 扰动的二进制布局管理 |
| 临时视图 | Temp View | DataFrame 注册进 SQL 目录以表名查询的桥（`createOrReplaceTempView`） |
| 用户定义函数 | UDF | 自定义行函数；对优化器是黑箱，2.x 起即被告诫慎用 |
| 数据源接口 | Data Source API | format/options/schema 统一读写 Parquet/JSON/JDBC/Hive 的 SPI |
| 数据仓库目录 | Hive Metastore | 表/schema 的中央元数据服务，`enableHiveSupport()` 对接对象 |
| R-SQL 桥 | sparklyr | dplyr 语法惰性翻译为 Spark SQL 的 R 前端 |
| Schema 演进 | mergeSchema | Parquet/JSON 读侧合列教义（§5.5 表首行的展开） |
| 运行时再优化 | Adaptive Query Execution | 3.x 起以运行时统计回填基数决策——2.x 手工档位的终结者（演进表） |

## 最新演进与工业实践

**2.x 知识点 → 2026 Spark 4.x 对位**：

| 本书（2.x） | 2026 现状 | 依据 |
|---|---|---|
| Catalyst 静态规则优化 | 3.0 引入、后续默认化的 **AQE**（运行时重估：动态合分区/动态 join 策略/倾斜处理）补上了「编译期优化看不到基数」的缺口 | ✅ [SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html)（adaptive 章节在页） |
| 手写 `spark.sql.shuffle.partitions=200` 调参教义 | AQE 让默认值自适应，2.x 式手工定档大面积失效 | ✅ 同上页 ⚠️ 效果描述转述 |
| Dataset[T] 双轨 | Scala/Java 仍存但工业重心在 DataFrame/SQL 与 Python 生态；4.x SQL 语义强化（ANSI 化、新类型/新函数一批） | ⚠️ 逐项 4.0 专页本次未逐字可达，口径以 [docs/latest](https://spark.apache.org/docs/latest/) 为总锚 |
| PySpark 无类型化对等 | Python DataFrame API 覆盖为 Connect 时代第一公民，pandas 生态桥持续加厚 | ✅ [api/python](https://spark.apache.org/docs/latest/api/python/) |
| Hive Metastore 中心化 | 开放表格式（Iceberg 等）+ 目录服务（如 Polaris 线）接棒元数据层 | 盘上互见 [../Use_Iceberg_with_Spark/](../Use_Iceberg_with_Spark/)（目录实名登记）；外部 URL 不赘引 ⚠️ |
| UDF=黑箱 | Arrow 化 Python UDF/批式 UDF 等缓解跨 JVM/进程边界的成本（细节代际 ⚠️） | ✅ [sql-programming-guide](https://spark.apache.org/docs/latest/sql-programming-guide.html) 总锚 |

**判语**：本册 SQL 部分的概念骨架（逻辑计划→优化→物理执行、视图桥、数据源 SPI）在 4.x 完全成立——这是目录版仍值得精读重构的原因；失效的是调参数值与 Dataset/R 双轨教义。分析纵深正读另见 [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)。
