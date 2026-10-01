# 03 Spark SQL: Foundation（Spark SQL 基础）

> 原书 Ch3，pp.51–109——全书最厚的一章之一（59 页），承担「把 SQL 用户带进 DataFrame 世界」。二级小节未实抓 ⚠️，以下依章题、页幅与 Spark 官方 SQL 文档结构推定主题簇；属**精读重构**。

## 3.1 SparkSession 与 Catalog：一切从入口对象开始 ⚠️

- `SparkSession.builder...getOrCreate()` 是 API 面唯一入口：DataFrame 读取、SQL 字符串执行、Catalog 元数据都挂在它身上。
- Catalog 三件事：**库/表命名空间**（`showDatabases/showTables`）、**临时视图**（`createOrReplaceTempView`——SQL 与 DataFrame 两个面的转接头）、**函数注册**（临时 UDF，见 `04`）。
- 概念澄清（重构表述）：Spark 的「表」默认只是**文件路径的命名**（Hive 元数据可选）——没有存储、没有事务，这是理解后面表格式层（Delta/Iceberg）的前提。官方锚点：https://spark.apache.org/docs/latest/sql-programming-guide.html（✅ curl 200）。
- 对照盘上：TDG 同一主题在 [../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md](../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md)，本册差别在节奏——先用 `spark-sql` CLI 跑通查询再回 Scala/Python。

## 3.2 读数据：schema 推断 vs 显式 schema ⚠️

- 三种入口：`spark.read.csv/json/parquet(path)`、带选项（`header/inferSchema/schema`）、`load` 泛化（格式名+路径）。
- 原书立场（依章骨架推定 ⚠️）：**永远给显式 schema**。理由链：推断=先扫一遍数据（成本）+ 类型猜错（风险）+ 列序漂移（事故）。CSV 是脏数据重灾区：空串/NULL 区分（`nullValue` 选项）、坏行处理（`mode=PERMISSIVE/DROPMALFORMED/FAILFAST`）。
- Parquet 的正向教学：自带 schema、列式压缩、谓词下推三件套——本册从 Ch3 起示例数据在 JSON/CSV/Parquet 间切换，教的就是「同一 DataFrame 语义、不同物理底座」。
- Spark 3 时间面：日期/时间类型族重整（TIMESTAMP/TIMESTAMP_NTZ、ANSI 模式）⚠️ 是否在本章给足存疑，按演进诚实登记：本册成书于 3.1/3.2 之交，NTZ 是 3.1 新特性，读到相关示例时以官方文档为准。

## 3.3 DataFrame 基本操作：select/where/agg/join ⚠️

- 关系代数五件套的 DataFrame 写法与等价 SQL 字符串双轨教学（`df.filter(...)` ⇄ `spark.sql("SELECT ... WHERE ...")`）；`col`/`column` 表达式树概念点到为止，深度留给 Ch4。
- 聚合：`groupBy().agg()` 多聚合器一次挂、`pivot` 一行带过；连接：`join(df2, on, how)` 各 outer 语义——这些是本章 109 页里反复练的主体 ⚠️ 主题簇推定。
- 缺失值：`na.drop/fill` 与 SQL 三值逻辑的衔接是入门者第一个「为什么我的行数不对」现场。
- 对照盘上：聚合与复杂类型的权威展开在 [../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md](../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md)；中文教材同题为 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。

## 3.4 写数据与分区布局 ⚠️

- 写出三参：格式（`save/write` + `csv/json/parquet`）、模式（Append/Overwrite/Ignore/ErrorExists）、分区（`partitionBy("year","month")`）——目录即数据：`part=...` Hive 风格布局，被 Spark/DuckDB/Trino/Hive 共同复用。
- 本册的教学缺口（诚实登记）：写侧讲了目录布局，但**没有讲表格式**（无事务/无 schema 演进/小文件问题）——这正是 2022 后入门者必须自己补的一层：盘上 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)、[../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)、[../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md](../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md)。

## 3.5 🔧 实验 E5：分区裁剪与谓词下推的「长相」（DuckDB 1.5.5，**非本书 Spark 引擎行为**）

- 方法：本机 DuckDB 写三分区 parquet 数据集（`data/part=0|1|2/f.parquet`，各 10 万行），`read_parquet('data/*/*.parquet', hive_partitioning=true)` 建等价视图；查询 `WHERE part=1` → 返回恰 100,000 行、`sum(amt)=2,475,000.0`，7.9ms。
- EXPLAIN 证据：计划仅一个 `READ_PARQUET` 扫描节点，节点内含 **File Filters: (part = 1)**、**Scanning Files: 1/3**、行级 `Filters: amt>49.0`（加行过滤时）——分区目录被裁成 1/3，谓词进扫描节点，没有独立 FILTER 算子。
- 类比映射：这正是 Spark「partition pruning + data skipping」在单机引擎上的同构现象——Spark 里由 Catalyst 把分区谓词折进文件列表枚举、由 Parquet min/max 统计跳过 row group ⚠️（Spark 侧机制转述官方文档，本机未测）。
- 边界声明：7.9ms 是单线程进程内数字，不可与任何 Spark 集群指标对比；「File Filters」为 DuckDB 术语，Spark 对应物名不同。

## 3.6 本章练习视角（重构）⚠️

- 章末练习风格：给定脏 CSV→建显式 schema→清洗→groupby 出指标→按日期分区写 parquet→再读回验证。自建检验清单：① 去掉 inferSchema 后时间成本变化；② 用错 `nullValue` 导致空串成 `""` 而非 NULL 的行数差异；③ partitionBy 列基数过高（如 ID 列）造成小文件爆炸——这三个坑在 2026 年依旧每日重演。

## 3.7 读数据决策表（重构 ⚠️）

| 数据形态 | 首选入口 | 必配选项 | 常见事故 |
| --- | --- | --- | --- |
| 干净 Parquet | `read.parquet` | 什么都不配（schema 自带） | 误用 glob 漏子目录 |
| 脏 CSV | `read.csv` | 显式 schema、`nullValue`、`mode` | 空串当 NULL/列错位 |
| 半结构化 JSON | `read.json`（一行一对象） | 显式 schema、`multiLine` | 换行内嵌 JSON 静默丢行 |
| 多文件混合 | 分区目录 + `load` | `recursiveFileLookup` 或分区列 | 分区列 schema 冲突 |
| 数据库表 | JDBC 源（概念级） | 谓词下推生效性验证 | 拉全表再 filter |

- 使用律：schema 一次写死、路径参数化、坏行策略显式声明——三条各对应上面一行事故。

## 3.8 基本操作语法卡（DSL ⇄ SQL 双轨对照 ⚠️ 重构）

- 投影：`df.select("a", col("b")*2)` ⇄ `SELECT a, b*2 FROM t`
- 过滤：`df.where("status='shipped' AND amt>100")` ⇄ 同文 WHERE
- 分组：`df.groupBy("k").agg(count("*"), sum("v"))` ⇄ `SELECT k, count(*), sum(v) GROUP BY k`
- 连接：`a.join(b, a["k"]==b["k"], "inner")` ⇄ `FROM a JOIN b ON a.k=b.k`
- 排序：`df.orderBy(col("v").desc_nulls_last)` ⇄ `ORDER BY v DESC NULLS LAST`
- 去重：`df.dropDuplicates(["k"])` ⇄ 窗口 `ROW_NUMBER()` 一行式
- 合并：`df.unionByName(other, allowMissingColumns=True)`（3.1+ 选项 ⚠️ 本册收录存疑）⇄ `UNION`
- 记住「等价但计划同源」：两轨写法的物理计划一致——这是 Ch4 `explain()` 实验的理论前提。

## 3.9 练习扩展：一张订单表的完整走查（重构 ⚠️）

1. 读脏 CSV（给定显式 schema），断言行数=文件行数-1（header）。
2. `filter(status in 合法集)` + `withColumn` 清洗金额（空串→NULL→fillna 策略讨论）。
3. join 维表出城市指标，groupBy+pivot 双写法各一遍。
4. 按日期 `partitionBy` 写 parquet；再读回，比对 `explain` 里 File Filters/分区列出现位置。
5. 🔧 收尾自测：把第 4 步换成 3.5 的 DuckDB 脚本跑一遍，亲眼看「Scanning Files: 1/3」——这是你在 Spark 里 `explain()` 要找的同类证据（机制类比，非 Spark 数值）。

## 3.10 本章边界声明

- 不讲的：Hive 集成深度（external metastore 配置）、流式读写（Ch6 后）、表格式事务（见 3.4 缺口登记）、JDBC/云源细节 ⚠️。
- 讲到 60 分的：schema 纪律、脏数据容错三档、分区布局直觉。
- 需要校外补课的：任何「为什么我的谓词没下推到 Parquet」类问题——答案是统计/分区两层机制，本册只给概念，深入读盘上 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)。

## 3.11 速自检（答案在上文）

1. SparkSession 挂着的三个门面各是什么？
2. 临时视图解决的是哪两个 API 面之间的转接？
3. inferSchema 的三宗罪（成本/类型/列序）。
4. CSV 坏行三档模式各自的适用场景？
5. Parquet 三件套优势是什么？
6. `partitionBy` 列的选型禁忌与理由？
7. Append/Overwrite/Ignore/ErrorExists 里哪两个最容易写出事故？
8. 为什么 NULL 会让「行数对不上」？
9. 🔧 E5 里「Scanning Files: 1/3」对应 Spark 的什么机制族？
10. 本册在写侧留下的最大概念缺口是什么、去哪补？

## 3.12 常见错误速修（一行卡 ⚠️ 重构）

- 列名报 `ANALYSIS_EXCEPTION`：先 `printSchema()` 再怀疑大小写——CSV 表头未开 `header` 是首号元凶。
- 日期列读成字符串：显式 schema 里用 `TimestampType` 而非 `StringType`，Spark 3 注意 NTZ 语义差异。
- join 后行数暴涨：键列有重复——右表先 `dropDuplicates([k])` 或改 semi join 语义。
- `where(col("x")=="literal")` 不生效：Python 里用了 `==` 于 Column 与 str 混比，改 `col("x")==lit("...")`。
- 写出目录「莫名其妙多了层」：`partitionBy` 列进了数据列又没 drop——写出前确认列清单。
- 重跑覆盖不生效：save mode 还是 ErrorExists——幂等回填日改 Overwrite/表格式 merge。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 会话入口 | SparkSession | DataFrame/SQL/Catalog 的统一门面 |
| 目录 | Catalog | 库/表/函数/视图的元数据空间 |
| 临时视图 | Temp View | DataFrame 与 SQL 文本互转的注册点 |
| 显式 schema | Explicit Schema | 声明式类型契约，替代扫描推断 |
| 坏行模式 | Parse Mode | PERMISSIVE/DROPMALFORMED/FAILFAST 三档容错 |
| 列式文件 | Columnar Format | Parquet 按列存取，压缩+投影裁剪友好 |
| 分区目录 | Partitioned Directory Layout | `col=value` Hive 风格目录即分区 |
| 分区裁剪 | Partition Pruning | 分区谓词只用于枚举文件，不进执行层 |
| 谓词下推 | Predicate Pushdown | 过滤条件进入扫描节点，借统计跳过数据 |
| 写入模式 | Save Mode | Append/Overwrite/Ignore/ErrorExists 四选一 |
| 三值逻辑 | Three-Valued Logic | NULL 比较非真非假，行数对不上常源于此 |
| 表格式缺口 | Table Format Gap | 裸目录无事务/演进——本册未讲的必修课 |

## 最新演进与工业实践

- **Spark 3→4 的本章面变化**：Variant 半结构化类型（Shredded Variant，3.4+/4.0）直接改写「JSON 读法」的教学——2026 年新教材已不再从 `from_json` 起步 ⚠️（官方 SQL 文档口径：https://spark.apache.org/docs/latest/sql-programming-guide.html ✅ 200）；ANSI 模式默认化让 3.2 时代「除零返回 NULL 还是报错」的示例行为改变。
- **表格式成为标配**：本册 2021 年的裸 parquet 教学在今天应读作「铺垫」；工业默认路径：Spark + Delta Lake（https://docs.delta.io/latest/index.html ✅ 200 / https://delta.io/ ✅ 200）或 Iceberg（多引擎表格式，盘上对位册：[../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)）。
- **单机侧镜像**：DuckDB/SQLite 生态 2024–2026 把 `read_parquet + hive_partitioning` 做成一等体验（本目录 🔧 实验即跑在其 1.5.5 上）；入门者用单机理解「目录布局/下推」的成本已趋零——但务必记住本目录的 E5 只是机制标本，不是 Spark 标本。
- **论文线登记**：Spark SQL 奠基论文《Spark SQL: Relational Data Processing in Spark》（Michael Armbrust 等，SIGMOD 2015）⚠️ DOI 本次未校验，仅题目+会议+年份；下游深读盘上 [../数据库系列·总索引.md](../数据库系列·总索引.md) 的引擎条目。
