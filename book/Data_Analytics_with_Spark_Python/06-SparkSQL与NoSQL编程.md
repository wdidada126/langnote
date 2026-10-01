# 06 Spark SQL 与 NoSQL 编程（对应原书 Ch6，印张页 161–206）

> 所属书目：[00-总览与阅读地图](00-总览与阅读地图.md) ｜ 《Data Analytics with Spark Using Python》1e，Jeffrey Aven 著，Addison-Wesley Professional，2018。
> 本章二级目录 ✅ 实抓自官方 informIT 产品页；正文为**精读重构**，非原书文本；连接器/版本细节按公开文档 ⚠️ 转述。

## 官方二级目录（✅ 实抓）

- Introduction to Spark SQL (p.161) ／ Introduction to Hive (p.162) ／ Spark SQL Architecture (p.166)
- Getting Started with DataFrames (p.168) ／ Using DataFrames (p.179)
- Caching, Persisting, and Repartitioning DataFrames (p.187) ／ Saving DataFrame Output (p.188)
- Accessing Spark SQL (p.191) ／ Exercise: Using Spark SQL (p.194)
- Using Spark with NoSQL Systems (p.195) ／ Introduction to NoSQL (p.196)
- Using Spark with HBase (p.197) ／ Exercise: Using Spark with HBase (p.200)
- Using Spark with Cassandra (p.202) ／ Using Spark with DynamoDB (p.204) ／ Other NoSQL Platforms (p.206)
- Summary (p.206)

## 精读重构·Spark SQL 侧（p.161–194）

- **动机叙事（p.161–166 ⚠️ 推定）**：RDD 表达力有余而优化器缺位；Hive 生态（表元数据 metastore、
  QL 习惯）是 DataFrame 概念的直接前身；Spark SQL 架构=逻辑计划→Catalyst 优化器→Tungsten 物理执行（题录见文末）。
- **Getting Started with DataFrames（p.168–179）**：`SparkSession.builder` 入口、
  `read.json/csv/parquet`、schema 推断与显式 `StructType` 双轨、`createDataFrame(pandas_df)`——
  书名 Using Python 在本章最讨便宜：pandas 用户到 DataFrame API 几乎零翻译成本（⚠️ 推定书中强调点）。
- **Using DataFrames（p.179–187）**：`select/filter/groupBy/agg/withColumn/join/sort/window` 算子族、
  `SparkSession.sql("...")` 注册临时视图混写 SQL、`explain()` 看计划。
- **Caching/Repartition（p.187）**：Ch5 的 RDD 存储课在关系层的复写：`df.cache()/persist(storageLevel)`
  + `repartition/coalesce`，新增列式(parquet)缓存红利语境 ⚠️ 转述。
- **Saving Output（p.188–191）**：`write.mode/save(path)`，格式 parquet/orc/json/csv，
  `partitionBy` 目录分区——与 Ch5 键分区是两个正交的「partition」概念（高频混淆点）。
- **Accessing Spark SQL（p.191–194）**：JDBC/ODBC(thriftserver) 供 BI 工具接入 ⚠️ 推定，练习节用内置表与
  JSON/CSV 数据集走一遍 SQL 路径（p.194）。

## 精读重构·NoSQL 侧（p.195–206）

TOC 的 NoSQL 三练习各对应一类键值/宽列连接器（语义按公开资料 ⚠️ 转述）：

| 系统 | 数据模型 | Spark 接入形态（2018） | 书中练习点 |
|---|---|---|---|
| HBase | 宽列、rowkey 有序 | `newAPIHadoopRDD`/connector 读写出 HBase 表 | p.200 双向：读表→RDD→条件写回 |
| Cassandra | 宽列、DCAware 分片 | spark-cassandra-connector 产 DataFrame | p.202 pushdown 谓词下推语境 |
| DynamoDB | 托管键值 | AWS connector（书中以 Python+boto/connector 双叙事 ⚠️ 推定） | p.204 云端衔接 Ch2 AWS 节 |
| Other | MongoDB/Redis 等 | connector 生态一览 | p.206 索引式扫尾 |

读法提示：NoSQL 节在 2026 年的价值是「模式映射学」——rowkey↔分区、谓词下推↔早过滤（Ch5 p.149 复现）、
连接器版本地狱；具体 connector 名与坐标全部过期，按现行官方/社区仓库重查 ⚠️。

🔧 **本地对照实测 E4（非本书 Spark 引擎行为）**：模拟「事实表 events(20 万行) join 维度表 users(2 万行)
再按 (category, tier) 聚合 Top5」的书中典型查询：
DuckDB 1.5.5（列式、进程内并行）0.0246 s；SQLite 3.45.3（行式、单线程 B 树）0.1678 s，
**6.8 倍**差距，且两引擎 Top5 金额逐位一致（`np.allclose` 校验通过，top1 = tool/gold 合计 542433.12）。
教学结论：本章「SQL 层抽象让同一查询在不同物理引擎间平移」的论点获得单机双引擎实证——
Spark SQL 之于 Catalyst，恰如 DuckDB 之于 SQLite：声明式接口、可替换执行体（脚本 `analogies.py` E4 组）。

示意（Spark 2.x Python ⚠️ 未实测）：

```python
spark = SparkSession.builder.appName("ch6").getOrCreate()
df = spark.read.json("events/*.json")
df.createOrReplaceTempView("events")
top = spark.sql("""
  SELECT e.category, u.tier, sum(e.amount) s
  FROM events e JOIN users u ON e.user_id = u.user_id
  GROUP BY e.category, u.tier ORDER BY s DESC LIMIT 5""")
top.write.mode("overwrite").parquet("out/top")
```

> repo 对照：现行 Spark SQL/DataFrame 全谱见
> [../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)；
> 中文类比见 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)；
> 关系引擎的通用原理（本波系列纵向支撑）见 [../../db/db.md](../../db/db.md) 论文线的查询处理条目。

## 常见误区与读法提示

1. 两个「partition」：目录分区（partitionBy 写盘）≠ RDD 分区（并行度），Ch5/Ch6 之间来回跳读的读者必混。
2. `spark.read.json` 的 schema 推断是**全表扫描**代价——生产必给显式 schema ⚠️ 转述（书 p.168 语境应有此警告 ⚠️ 推定）。
3. NoSQL connector 是版本地狱重灾区：本书 2018 年的坐标全部失效，只学映射模式不抄配置。

## 复习要点与自测清单

1. 用 Catalyst/Tungsten 两词解释「为什么 DataFrame 通常快过等价 RDD 代码」。
2. Schema 双轨：显式 StructType vs 推断，各自适用面与代价（全表扫描、类型漂移）。
3. 两个 partition 概念造句区分：`partitionBy` 写目录 vs `repartition` 调并行度。
4. DataFrame 算子→SQL 等价改写练习：select/filter/groupBy 三件套与 join 各写两遍。
5. 写出 `explain()` 输出里能找到的三种优化证据（谓词下推、列裁剪、join 策略选择）。
6. NoSQL 映射题：给定 HBase rowkey 设计，说明 Spark 读入后分区/过滤应在哪侧做（pushdown 语义）。
7. 缓存对比：`df.cache()` 与 Ch5 `rdd.persist()` 在序列化形态上的差别 ⚠️ 转述。
8. 🔧 双引擎验证题：解释 E4 实验中 DuckDB 与 SQLite 结果逐位一致而耗时差 6.8 倍，
   对「SQL 是可移植接口、性能是物理引擎属性」命题的支持与边界（非 Spark 行为）。
9. 存储侧思考题：同一张表分别按目录分区/ RDD 键分区组织，写出各自的查询受益面与失衡风险，
   并说明 Spark 读侧两种「裁剪」（partition pruning 与分区数推断）如何发生。

## 核心概念速览（中英对照）

- **数据框** — DataFrame：带 schema 的分布式表抽象，关系算子+惰性执行的 RDD 上层封装。
- **SparkSession** — SparkSession：2.x 起的统一入口对象，聚合上下文/SQL/catalog。
- **Catalyst** — Catalyst Optimizer：逻辑→优化的物理计划管线（谓词/列裁剪/join 策略）。
- **Tungsten** — Tungsten：脱离 JVM 对象模型的二进制执行与内存管理层。
- **临时视图** — Temporal View：`createOrReplaceTempView` 把 DataFrame 挂进 SQL 命名空间。
- **Schema 推断** — Schema Inference：read 时探测列型，便利但带全表扫描成本。
- **写模式** — Save Mode：overwrite/append/ignore/error 四类冲突策略。
- **目录分区** — Partitioned Directory：`partitionBy` 的 Hive 风格目录布局，读时分区裁剪。
- **列式格式** — Columnar Format (Parquet/ORC)：按列组织+谓词下推的存储格式，DataFrame 落盘首选。
- **宽列存储** — Wide-column Store (HBase/Cassandra)：按 rowkey 聚簇的大表模型，Spark 经连接器双向。
- **连接器** — Connector：Spark 与外部存储的适配库，版本强耦合源系统。
- **JDBC/ODBC 服务** — Thrift Server / JDBC-ODBC：把 Spark SQL 暴露给 BI 工具的兼容服务面。

## 最新演进与工业实践

- **DataFrame 成为唯一门面**：官方 SQL 与结构化数据指南持续维护
  （https://spark.apache.org/docs/latest/sql-programming-guide.html ，✅ curl -sI 200）；
  2024–2026 的 PySpark 新特性（类型提示、connect 会话、流缓冲读法）全部只加在 DataFrame 面 ⚠️ 转述。
- **pandas API on Spark 直接吃本章红利**：ps 命名空间让本章查询可以用 pandas 写法跑在 Spark 上，
  https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/index.html （✅ curl -sI 200）。
- **AQE 常态化**：本书时代要手工做的 join 重排/倾斜处理，3.x 起优化器默认接管 ⚠️ 转述，参见
  [../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)。
- **NoSQL 叙事被湖仓替换**：DynamoDB/HBase 直连模式在分析线退潮，Iceberg/Delta 表格式+对象存储
  成为「关系层与存储层」之间的主流答案——repo 内现行叙事见
  [../Advanced_Analytics_with_Spark_2e/01-大数据分析.md](../Advanced_Analytics_with_Spark_2e/01-大数据分析.md) 的生态更新视角（波4在盘）。
- **单机双引擎实证可复用**：🔧 E4 的 DuckDB vs SQLite（6.8 倍、结果逐位一致）是本波「声明式接口可移植」论点的
  低成本课堂实验，可替代当年必须起 Spark 集群演示 SQL 层的旧做法（非本书 Spark 引擎行为）。
