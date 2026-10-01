# 03 · Spark SQL 配方（原书 Ch4 Spark SQL）

> 精读重构笔记，非原书文本。目录取证：微信读书官方电子版目录快照（✅ 实抓）；Spark 侧行为 ⚠️ 转述；🔧 组为 SQLite/DuckDB **类比，非本书 Spark 引擎行为**。

## 1. 章域定位

Ch4 是全书技术含量最高、也是**报废率最高**的一章：Spark 1.x 的 Spark SQL 以 `HiveContext` 为门户、case class 推断 schema、SchemaRDD 更名 DataFrame 的过渡态为中心；其后的「Parquet/JSON/关系库/任意源」读写食谱则大多以换皮形式存活至今。这一章的配方清单恰好构成一条「手写 RDD 解析 → 声明式 SQL 引擎」的迁移路径，是理解 2015-2016 年 Spark 战略重心从 RDD 移向结构化层的最佳切片。Catalyst 食谱（4.1）放在章首是 __A1__ 的自觉——先给读者优化器的认知模型，再给一堆「为什么这样写更快」的配方解释。

## 2. 食谱地图

| # | 食谱（官方目录逐字） | 配方核心 | 2026 等价物 ⚠️ |
|---|---|---|---|
| 4.1 | Understanding the Catalyst optimizer | 分析树→优化→计划生成的认知框架 | 同一框架 + AQE 运行时再优化 |
| 4.2 | Creating HiveContext | SQL 门户对象 | `SparkSession`（2.0 统一入口） |
| 4.3 | Inferring schema using case classes | RDD[case class] 隐式转 SchemaRDD | `spark.read.schema(...)` / 类型推断 DSL |
| 4.4 | Programmatically specifying the schema | StructType/StructField 手工建 schema | 同构存活，仍是不可信数据首选 |
| 4.5 | Loading and saving data using the Parquet format | saveAsParquetFile / parquetFile | `write.parquet` / 湖仓格式 |
| 4.6 | Loading and saving data using the JSON format | JsonRDD 与 SchemaRDD.jsonRDD() | `read.json` / 多行模式选项 |
| 4.7 | Loading and saving data from relational databases | DataFrameReader.jdbc 双向往返 | 同 API 存活，谓词下推增强 |
| 4.8 | Loading and saving data from an arbitrary source | 换 Ch3 InputFormat 接口的 SQL 皮 | DataSource V2 provider |

## 3. 精读块一：Catalyst——食谱背后的「为什么」（4.1）

**问题**：为什么同一逻辑查询换种写法性能差一个数量级？
**配方骨架**：unresolved plan → analyzer（catalog 绑列）→ logical optimizations（谓词/投影下推）→ physical planning（成本与启发式）→ codegen 执行。
**评注 ⚠️**：1.x 时代 Catalyst 只有规则优化无成本模型，2.x 引入 CBO、3.x 的 AQE（adaptive query execution）才把运行时统计闭环。食谱让读者「知道有优化器」，2026 的生产要求是「会读 physical plan 并验证 join 策略」。
**与 repo 对照**：现代展开见 [../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)；中文口径见 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。SQL 语言层的优化直觉可回看 [../SQL系列·总索引.md](../SQL系列·总索引.md) 的调优书目群。

## 4. 精读块二：schema 两手策略——推断 vs 声明（4.3/4.4）

**问题**：半结构化数据何时可以让引擎猜 schema，何时必须手写？
**配方骨架**：受控数据用 case class 白嫖推断；不可信/演化数据用 StructType 显式声明。
**评注 ⚠️**：推断要**全量采样一遍**（Spark JSON 源默认采样所有分区），大文件上这比转换本身还贵——该结论在 3.x 的 `mode=PERMISSIVE/FAILFAST` 体系里仍成立。类型陷阱（数字串、null 列推断为 NULL 型）当年靠 StructType 兜底，如今仍是兜底方案，4.4 是全书保值率最高的食谱之一。
**🔧 类比（DuckDB 1.5.5，非本书 Spark 引擎行为）**：`read_json_auto` 对 20,000 行 JSONL 一次性推断出含 `VARCHAR[]` 嵌套列的五列 schema，54.5 ms——推断已下沉为流式采样实现；对比 Spark 当年的两段式（先 RDD 解析再注册临时表），可以看到「schema 推断成本」被工程压缩了两个数量级，配方 4.3 的谨慎前提在现代引擎下需要重估。

## 5. 精读块三：SQL 化的三个日常动作——去重/行列转换/窗口（4.5-4.8 的查询侧延伸）

**问题**：RDD 时代的 `distinct`/`groupByKey`/`mapPartitions` 惯用法在 SQL 层的对应配方。
**配方骨架**：`dropDuplicates` 保最新、`stack/pivot` 做行列互转、`Window.partitionBy.orderBy` 组内排序取 topN。
**🔧 实测组（DuckDB 1.5.5，非本书 Spark 引擎行为）**，同一 20,000 行 `ev` 表：
1. **去重**：`QUALIFY row_number() OVER (PARTITION BY uid ORDER BY ts DESC)=1` 保留 4,000 行，7.2 ms——等价 DataFrame `dropDuplicates("uid")` 保最新语义的单机版；SQLite 侧同题 34.2 ms（02 章 E1），差距即「列存向量化 vs 行存逐行」的直观教材。
2. **行列转换**：`PIVOT (SELECT user, CASE WHEN amount>3 THEN 'hi' ELSE 'lo' END b, count(*) c FROM ev GROUP BY 1,2) ON b USING sum(c)` 得 5 用户 ×2 桶矩阵（alice 3412/588 等），31.3 ms——对应 `stack()`/`explode` 互逆操作家族。
3. **窗口 topN**：`rank() OVER (PARTITION BY user ORDER BY amount DESC)` 取每用户前 2 共 10 行，12.7 ms——即 `Window.partitionBy("user").orderBy(col("amount").desc)` + `filter(rank<=2)` 的直译。
**坑**：Spark 的 `pivot` 需要预枚举列值（或额外扫描求 distinct 列），SQLite/DuckDB 无此限制——写 Spark 配方时「先一查询探列值、再拼 pivot」的两段式是 2026 仍存在的显式成本 ⚠️。

## 6. 精读块四：Parquet/JSON 双格式策略（4.5/4.6）

**要点**：Parquet 列存 + 谓词下推做「分析面」，JSON 行式自描述做「交换面」；两格式间转换即 schema 治理现场。
**🔧 呼应**：格式带来的体积差在本目录 08 章 E7 有量化实验（CSV 696,182 B → Parquet 231,807 B → ZSTD 124,177 B）。
**对位阅读**：[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md) 的列存分块动机；湖仓化续篇见 [../Use_Iceberg_with_Spark/04-时间旅行与元数据表.md](../Use_Iceberg_with_Spark/04-时间旅行与元数据表.md)。

## 7. 互链清单

- 主参照：[../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)、[../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md](../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md)
- 底座：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)、[../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)
- 数据源前章：[02-外部数据源配方.md](02-外部数据源配方.md) ｜ 流式续章：[04-Spark流处理配方.md](04-Spark流处理配方.md)
- RDD 旧API考古：[../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md)

## 8. 配方骨架速查（考古重构，⚠️ 转述，语法按 1.x 惯例）

- **4.2**：`val sqlContext = new HiveContext(sc)`，之后 `sqlContext.sql(...)`/`df.registerTempTable(...)` 双向切换 ⚠️。
- **4.3**：`case class Person(name: String, age: Int)` + `sc.textFile(...).map(parse).toDF()` 即完成推断；或 JSON 直接 `SchemaRDD.jsonRDD()` ⚠️。
- **4.4**：`StructType(Seq(StructField(col, StringType, nullable = true), ...))` 传给解析函数，显式优于推断 ⚠️。
- **4.5/4.6**：`df.saveAsParquetFile(path)` / `sqlContext.parquetFile(path)`；JSON 侧 `jsonFile/jsonRDD` 往返 ⚠️。
- **4.7**：`DataFrameReader.jdbc(url, dbtable, properties)` 读、`df.write.mode(...).jdbc(...)` 写 ⚠️。
- **4.8**：`sqlContext.applySchema(rdd, schema)` 或包一层 RelationProvider 即「任意源」⚠️。

## 9. 自测卡（合卷作答，8 问）

1. Catalyst 四阶段各自输入输出是什么？（unresolved→analyzed→optimized→physical）
2. HiveContext 与 SQLContext 的差别关键词？（元数据 catalog/Hive 依赖）
3. case class 推断的隐性成本在哪一步？（采样全量扫一遍）
4. 何时必须用 4.4？列三个触发条件。（不可信输入/列序漂移/类型串化）
5. Parquet 收益的前置条件是什么？（列裁剪+选择率+谓词下推生效）
6. E4 的 QUALIFY 写法对应 Spark 哪个 API 族？（dropDuplicates + 保最新需窗口自拼）
7. Spark pivot 与 DuckDB PIVOT 的最大用法差？（列值需预枚举 ⚠️）
8. 本章哪两个食谱在 2026 仍「原文可用」？（4.4 与 4.7）

## 10. 小练习

1. 把 4.3→4.4 改写成 2026 的 `spark.read.schema(userProvidedSchema)` 三行伪码，标出当年/现在的默认分歧。
2. 重放 E4/E5/E6（脚本见 `D:\develops\tmp\dbwave_w8_scbkt\exp.py`），改动窗口 order 方向与 PIVOT 阈值各观察一次输出变化。
3. 写一页「Catalyst vs 传统数仓优化器」对比提纲，素材取 4.1 食谱 + 03 章 §3 + TDG 06 章链接段。

## 核心概念速览（中英对照）

- **Catalyst** — Catalyst：Spark SQL 的可扩展优化器框架，规则驱动的逻辑计划变换加物理计划选择。
- **HiveContext** — HiveContext：1.x 时代 SQL 能力入口对象，Spark 2.0 后由 SparkSession 取代。
- **SchemaRDD/DataFrame** — SchemaRDD → DataFrame：带 schema 的 RDD 到声明式表的演进，本书正处更名过渡期。
- **case class 推断** — schema inference via case classes：以 Scala 类型系统为 schema 来源的轻量配方。
- **StructType** — programmatic schema：字段名/类型/null 性显式声明，不可信数据的防御写法。
- **谓词下推** — predicate pushdown：过滤条件经优化器压到扫描层（文件/分区/行组） skipping 数据。
- **列式存储** — columnar storage（Parquet）：按列组织加压缩的 analytic 格式，扫描选择性决定收益。
- **行式 JSON 源** — JSON datasource：自描述半结构化入口，采样推断是其成本特征。
- **QUALIFY/窗口去重** — window-function dedup：row_number 保最新一类的幂等去重表达。
- **透视/逆透视** — pivot / unpivot：行列互转算子族，Spark pivot 需预枚举列值为其特色约束 ⚠️。
- **AQE** — adaptive query execution：3.x 运行时统计驱动的再优化，对 4.1 食谱的当代答复 ⚠️。

## 最新演进与工业实践

- **入口统一**：SQLContext/HiveContext 归并进 `SparkSession`（Spark 2.0 起），`spark.sql()`/`read.table()` 成为唯一门户；官方 SQL 指南 ✅ https://spark.apache.org/docs/latest/sql-programming-guide.html （2026-10-01 curl -sI 200）。
- **优化器演进**：Catalyst 之上叠加 CBO（2.0）与 AQE（3.0+，默认开）：动态合分区、join 策略运行时翻转、skew join 自动拆热键——把本章「手工 repartition/广播提示」类技巧逐条吸收进引擎 ⚠️。
- **JSON 谱系**：社区论文《Spark SQL: Relational Data Processing in Spark》（SIGMOD 2015）是该章技术栈的一手文献；其 DOI 本波 Crossref 校验未通过 → ⚠️ 仅题录引用，勿据此写链接。
- **格式层上移**：纯 Parquet 读写配方在 2020s 被表格式（Iceberg/Delta/Hudi）接管——ACID、时间旅行、schema 演化都在 Parquet 之上；对位实践见 [../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md](../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md)。
- **SQL 方言趋同**：pivot/QUALIFY/try_cast 等本章当年要靠 UDF 手搓的算子已全部进入 Spark SQL 语法面（3.x+），配合 ANSI 模式选项；食谱 4.3-4.4 的 Scala 侧写法在纯 SQL 团队中基本退役 ⚠️。
- **工业口径**：数据湖查询引擎选型（Spark/Trino/DuckDB 分层）成为 2026 常态，本章三组 🔧 实验（7.2/12.7/31.3 ms 单机）恰好演示了「同一 SQL 语义在不同引擎族的成本形态」，可作为引擎选型的入门复算素材——结论边界再次声明：**类比数据非本书 Spark 引擎行为**。
