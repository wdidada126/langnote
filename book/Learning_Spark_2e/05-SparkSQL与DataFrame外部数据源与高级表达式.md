# 05 · Spark SQL 与 DataFrame：外部数据源与高级表达式

> 原书第 5 章（Spark SQL and DataFrames, Part 2）。章骨架 ✅ 按 ApacheCN 全译镜像实抓的二级标题还原：Spark SQL 与 Apache Hive／用户定义函数（SQL UDF、求值顺序与空值检查、Pandas UDF 加速 PySpark）／Spark SQL Shell、Beeline、Tableau／外部数据源（JDBC 与 SQL 数据库：PostgreSQL、MySQL、Azure Cosmos DB、MS SQL Server；其他外部来源）／高阶函数（explode 与 collect、内置复杂类型函数、transform/filter/exists/reduce）／常见关系操作（联合、连接、窗口化、增列、改名、透视）。Spark 行为 = ⚠️ 转述 + 官方文档实链。对位：[bigdata 09 存储与文件格式](../bigdata/09-存储与文件格式.md)、[TDG 05 UDF 与数据源](../Spark_The_Definitive_Guide/05-UDF与数据源.md)。

## 5.1 Hive 与 JDBC 两线

- **Spark SQL 与 Hive**：`enableHiveSupport()` 复用 Hive Metastore 的库表/分区/UDF；表发现两姿势——目录直读 vs 元数据表；`MSCK REPAIR`/`INSERT OVERWRITE PARTITION` 方言衔接（⚠️ 转述）。2e 立场：Hive 兼容层是迁移桥，新体系交给表格式（第 9 章伏笔）。
- **JDBC 读**：`format("jdbc")` + url/dbtable/user/password；**默认单连接单分区**，并行靠 `partitionColumn/lowerBound/upperBound/numPartitions` 四件套（按数值列切谓词区间）；PostgreSQL/MySQL/Cosmos/SQLServer 四例各给方言注意点（fetchsize、驱动、认证）；
- **JDBC 写**：mode/truncate/createTableOptions——**跨分区写无全局事务**，本章最该记住的运维结论；
- **其他外部来源**：Avro（`--packages com.databricks:spark-avro`，"外部包"代表形态）、云对象存储连接器（S3/ADLS/GCS）。

## 5.2 UDF 三阶梯（本章教学高潮之一）

⚠️ 转述（官方口径 https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅ curl 200 同族线）：

1. **SQL/表达式优先**：内置函数能表达的一律不写 UDF——保持 Catalyst 可见性；
2. **普通 UDF**：黑盒函数，打断 codegen、跨 JVM/Python 进程要序列化；书中专设"求值顺序与空值检查"节讲 UDF 里 null 处理责任转移给用户；
3. **Pandas UDF（批式 arrow UDF）**：以 pandas.Series 为单位向量化执行，Python 侧性能数量级改善——"加速和分发 PySpark UDF"小节的承诺句；聚合型/窗口型 Pandas UDF 与 mapInPandas 属 3.0 新武器（第 12 章回收）。

## 5.3 SQL 服务化三件套：spark-sql shell / Beeline+ThriftServer / Tableau

- `spark-sql` CLI：本地即时 REPL；
- **Thrift Server + Beeline**：JDBC 协议对外暴露 Spark SQL——BI 工具接入口；书中给启动参数、建表、插数、查询全流程；
- **Tableau**：以 Thrift 为底的数据源示例——2020 年"Spark 即交互查询服务"的姿态；2026 回看被 Livy/SQL Gateway/Spark Connect 与各家 BI 原生连接器接力（演进节）。

## 5.4 高阶函数与关系操作全家福

- **Array/Map 表达式**：`transform(arr, x -> x*2)`、`filter`、`exists`、`reduce`——不 explode 再 group 的"就地嵌套计算"（vs 选项 1"展开收集"、选项 2"UDF"的三路线对照，本章标题级结构）；
- **联合/连接**：union/unionByName；join 五型（inner/outer/left/semi/anti）+ cross；
- **窗口化**：Window.partitionBy/orderBy + rowsBetween/rangeBetween，rank 族、lead/lag、collect_list over window；
- **增列/改名/透视**：withColumn(Expr)、withColumnRenamed、pivot（聚合透视）。

🔧 **窗口实测类比（非本书 Spark 引擎行为）**：DuckDB 对分区 parquet 集执行 `count(*) OVER (PARTITION BY yr ORDER BY id ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)`，前 3 行输出 `(0,2024,1),(2,2024,2),(4,2024,2)`（meas.txt G2 组）——滑动帧语义与 Spark Window 一致；**差异**：Spark 窗口按分区执行，跨分区的窗口需先 shuffle 排序（⚠️ 转述），DuckDB 无此成本。

🔧 **分区目录裁剪实测类比（非本书 Spark 引擎行为）**：`COPY ... PARTITION_BY (yr)` 落两目录（`yr=2024/`、`yr=2025/`），`read_parquet(..., hive_partitioning=1) WHERE yr=2024` 精确 500 行、EXPLAIN 可见按目录常量裁剪（meas.txt G3 组）——即 Spark "分区目录名 + 谓词命中跳文件"的单机复刻（⚠️ Spark 侧裁剪发生在 driver 文件列表阶段为转述）。

## 5.5 工程判断（重构观点）

本章的暗线是**表达式可见性经济学**：内置表达式→优化器全权处理；UDF→黑盒；Pandas UDF→黑盒但批发。写 Python 的团队从"逐行 UDF"迁到"批式 Pandas UDF"是 2.x→3.0 时代最划算的一次性能投资——书中此点埋在第 5 章，其 3.0 完整形态要到第 12 章才亮出。

## 5.6 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| Spark SQL 和 Apache Hive | 5.1 Hive 段 |
| 用户定义函数／Spark SQL UDFs | 5.2 阶梯 1–2 |
| 在 Spark SQL 中进行评估顺序和空值检查 | 5.2 第 2 级注 |
| 使用 Pandas UDF 加速和分发 PySpark UDF | 5.2 第 3 级 |
| 使用 Spark SQL Shell、Beeline 和 Tableau 进行查询（shell：建表/插数/查询；Beeline：起 Thrift/连接/执行/停止；Tableau：启动） | 5.3 |
| 外部数据源：JDBC 和 SQL 数据库／分区的重要性 | 5.1 JDBC 段、5.6 分区块 |
| PostgreSQL／MySQL／Azure Cosmos DB／MS SQL Server | 5.1 四例注 |
| 其他外部来源 | 5.1 末段 |
| 数据框架和 Spark SQL 中的高阶函数（选项 1 展开和收集／选项 2 用户定义函数；内置复杂类型函数；transform()/filter()/exists()/reduce()） | 5.4 高阶段 |
| 常见的 DataFrame 和 Spark SQL 操作：联合／连接／窗口化／添加新列／重命名列／透视 | 5.4 全家福 |

## 5.7 重建示例：JDBC 并行读 + 窗口 + 高阶函数（本目录重做；⚠️ 语义转述）

```python
pg = (spark.read.format("jdbc")
      .option("url", "jdbc:postgresql://db:5432/app")
      .option("dbtable", "(SELECT id, ts, amount FROM orders) t")
      .option("partitionColumn", "id").option("lowerBound", "1")
      .option("upperBound", "1000000").option("numPartitions", "16")
      .option("fetchsize", "10000").load())

from pyspark.sql.window import Window
from pyspark.sql import functions as F
w = Window.partitionBy("id").orderBy("ts")
top = (pg.withColumn("run_sum", F.sum("amount").over(w))     # 累计帧
         .withColumn("rn", F.row_number().over(w)))           # rank 族

df2 = df.withColumn("vals2", F.transform("vals", lambda x: x * 2))   # 高阶：不 explode
df3 = df2.withColumnRenamed("rn", "seq").groupBy().pivot("k").sum("amount")
```

三段分别对应镜像小节"JDBC 四件套""窗口化""高阶函数/透视"；**⚠️ 本目录未执行 Spark，API 形态以官方 sql-ref-functions-window / higher-order functions 文档为准**。

## 5.8 课堂问题（答不出回本文件）

1. 为什么 JDBC 读默认单分区？四件套的切分依据是什么字段？
2. Spark 写库的事务边界到哪为止（5.1 运维结论）？
3. 普通 UDF 让优化器"看不见"什么？Pandas UDF 拿回了什么？
4. Beeline 连的是哪个进程？它在生产里被什么替代（演进节）？
5. explode-再-collect 与 `transform()` 的三条取舍（行数放大/shuffle/可读性）？
6. 流-流之外的"窗口化"在本章指什么？与第 8 章 event-time 窗口的词义区分？

### 外部源与高级表达式：误区速记

- JDBC 读侧谓词下推依赖目标库方言，开源 Spark 不保证对所有 dbtable 写法生效。
- Kafka 读取按 topic 分区并行；Spark 分区数与 Kafka 分区数不是一一对应，批式 load 与流式 read 行为也不同。
- UDF 注册后进不了 Catalyst 的表达式重写，是常见性能陷阱；优先用内置函数。
- UDAF 与批量向量化路径不是本章对象：本章只覆盖 UDF，向化视角在 07 章调优再提。
- window 函数必须先构造 Window 对象再 partitionBy/orderBy；不存在 withWindow 这种 API。
- 高阶函数（transform/filter/aggregate/zip_with）作用于 array/map 列，避免为此写 UDF。
- 连接外部库时凭据不要写进 URL 明文；用 options 传并注意日志脱敏。
- fetchsize、分区列读参数对性能的影响大于语法本身。
- 本章 G2/G3 两组 🔧 类比（DuckDB/SQLite）只验证 SQL 概念，不映射 Spark 连接器实现。
- 对损坏行与空值：nullFormat 与 mode 是两个不同开关，不要混记。
- 小节骨架表已按镜像逐节对账；若版本页码不同，以小节标题而非页码为准。
- 外部 sink 的 save mode 与本地文件语义一致：append/overwrite/errorifexists/ignore。

## 核心概念速览（中英对照）

- **JDBC 四件套** — partitionColumn/lowerBound/upperBound/numPartitions：并行读的正解。
- **fetchSize** — 游标批量：驱动方言强耦合。
- **enableHiveSupport** — Hive Metastore 接入开关。
- **MSCK REPAIR** — 目录分区回填。
- **Thrift Server/Beeline** — JDBC 协议服务化 Spark SQL。
- **SQL UDF** — 表达式级用户函数。
- **Pandas UDF** — Arrow 批式向量化 UDF：Python 性能正解。
- **求值顺序/空值检查** — UDF 把 null 责任接到用户身上。
- **高阶函数** — transform/filter/exists/reduce：数组/map 就地计算。
- **explode/collect_list** — 展开-收集路线（对照高阶函数的笨办法）。
- **Window 帧** — rowsBetween/rangeBetween + rank/lead/lag。
- **pivot** — 聚合透视：行转列。
- **unionByName** — 按列名并集：防错位。
- **small file** — 分区×并行度写出副产物（第 7 章回收）。

## 最新演进与工业实践

- **UDF 家族扩容（Spark 4.0，✅ 官方 Release Notes 实抓）**：SQL UDF（纯 SQL 体函数）、Python UDTF、PySpark UDF 统一 profiling——本章"三阶梯"变成"多阶梯"，但"表达式优先"原则不变（✅ https://spark.apache.org/docs/latest/sql-ref-functions-udf-scalar.html 线，curl 200 见文末报告）。
- **BI 接入面**：Thrift/Beeline 路线边缘化；Livy 归档、Spark Connect + SQL Gateway 生态成为程序化入口，Tableau 等 BI 走各云原生连接器（⚠️ 转述）。
- **JDBC 退位**：库↔湖主力通道换成官方云仓连接器与 CDC（Debezium + MERGE）；四件套技巧降级为兜底（表格式纵深对读 [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)）。
- **窗口语义统一**：Spark/Flink/DuckDB 三家 ANSI 窗口帧语义对齐，跨引擎迁移成本下降；中文实战对读 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。
- **AQE 改写 join 生态**：smj/bhj 的手动选择学在 3.0 后让位于自动（第 7/12 章主场），本章"连接全家福"的运维分量减轻。
