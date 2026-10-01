# 05 DataFrame与SparkSQL（Ch5: DataFrames, Datasets, and Spark SQL）

> 章题取证 ✅（终版第 5 章＝草案第 3 章对位）；节级结构参考草案实抓：SparkSession 入门 / SQL 依赖管理 / schema 基础 / DataFrame 转换 / 多表转换 / SQL 与 Hive 交互 / 数据表示 / 加载与保存（Reader/Writer、格式、保存模式、分区）/ Dataset / UDF·UDAF / 查询优化器（逻辑物理计划、codegen、大型计划）/ 调试查询 / JDBC-ODBC 服务器。⚠️ 终版或有调序。本章安置 🔧 E3、E4、E6（**均非 Spark 引擎行为**）。

## 0. 本章主线

DataFrame 不只是一组 API，它是**把"你的数据"翻译成"引擎的列式二进制内存表示"的通道**——走上这条通道才有 Catalyst 与 codegen 的全部红利；留在通道外（RDD/逐行 UDF），就还在 2016 年的成本结构里。

## 5.1 入口与依赖（草案 3.1/3.2 ✅）

- SparkSession 唯一入口；SQLContext/HiveContext 已是历史名词（升级章词汇）。⚠️
- 依赖纪律：catalog 与连接器版本必须与引擎大版本配对；草案"避免使用 Hive JAR"的告诫演化为"用官方打包的 connector，别自己拼 classpath"（接 12 章打包学）。⚠️

## 5.2 schema 与转换 API（草案 3.3/3.4/3.5 ✅）

- schema 是优化器的地图：类型声明精度决定谓词下推与列裁剪的射程；`stringly-typed` 列是下推的第一坟场。
- 转换分两类：
  - 确定性列代数（select/filter/withColumn 链）——可被 Catalyst 合并进同一 codegen 循环，近零成本；
  - 聚合/join——触发 shuffle 边界，是账本上的大头。
- 调优第一问：**你的算子链里有几个 shuffle 边界**？每减一个都是数量级候选。
- 数据表示（草案 3.5）：Row→内部二进制行格式（堆外紧凑布局）——Tungsten 叙事的落点；语言税恰发生在"表示转换"处（09 章清算）。⚠️＋ https://spark.apache.org/docs/latest/rdd-programming-guide.html ✅

## 5.3 加载、保存与分区（草案 3.6 ✅）

- 格式谱系：parquet/orc/csv/json/jdbc，湖仓经 DSv2 接入；保存模式：append/overwrite/ignore/errorifexists——写入分区＝目录树重排。
- 🔧 **E3 分区裁剪实测（DuckDB，非 Spark）**：
  - 方法：`COPY (SELECT id, dt FROM src) TO 'part' (FORMAT parquet, PARTITION_BY (dt))` 写出 24 目录 120 万行；分别全量 `count` 与 `WHERE dt='2026-07'` 计时并 EXPLAIN。
  - 结果（本机）：全扫 0.01s vs 单分区 0.00s（读 5 万行/24 分之一文件集），EXPLAIN 输出含 `dt` 谓词与文件裁剪证据。
  - 概念映射：Spark 对 Hive 风格分区目录做同构裁剪；下一层是 Parquet row-group 的 min/max 统计跳过；湖仓格式再叠文件级元数据（../Use_Iceberg_with_Spark/05-演化与隐藏分区.md、../Use_Iceberg_with_Spark/04-时间旅行与元数据表.md）。⚠️ 引擎侧规则以 sql-performance-tuning 页 ✅ 为准。
- 🔧 **E4 列存 vs 行存实测（DuckDB vs SQLite，非 Spark）**：
  - 方法：同构 200 万行×10 列各入两库，执行"两列投影＋一谓词"聚合，比时。
  - 结果（本机）：列存 0.01s vs 行存 0.16s（**≈24 倍**）——列存红利＝只读需要的列×批式解码，与分布式无关，单机已成立；Parquet＋向量化读对"CSV 全解析＋JVM 行对象"的碾压同源于此。
  - 中文格式谱系：../bigdata/09-存储与文件格式.md。

## 5.4 Dataset 与强类型（草案 3.7 ✅）

- Dataset＝DataFrame＋编译期类型；encoders 决定它离列式二进制内存有多远。
- 红线：对 Dataset 滥用 `map` 会把 codegen 红利退回"逐对象"路径——类型安全与向量化在此直接互斥（07 章对象经济学的镜像）。⚠️
- API 侧同题：../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md 从教学面讲同一折衷。

## 5.5 UDF/UDAF 与优化器的边界（草案 3.8/3.9 ✅）

- UDF＝优化器眼里的黑箱，三宗罪：**不可下推、不可合并、打断 codegen**；能内建函数解决就别 UDF。⚠️＋ https://spark.apache.org/docs/latest/tuning.html ✅
- Catalyst 三段式：解析→逻辑计划重写（谓词下推/列裁剪/常量折叠）→物理策略选择；`explain` 三层读法是本章的手艺。⚠️
- 代码生成：whole-stage 把算子融合成单循环；"大型计划与迭代算法"小节讲计划体积反噬编译时间——SQL 分段物化是对策。⚠️
- 🔧 **E6 统计驱动重规划实测（SQLite，非 Spark）**：
  - 方法：40 万行、双索引（低基数 a／高基数 b），查询 `WHERE a=0 AND b>1000 AND b<1003`；比对 ANALYZE 前后 EXPLAIN QUERY PLAN 与时序。
  - 结果（本机）：无统计时选 ia 扫 20 万条目 39.9ms；`ANALYZE` 后计划**逐字翻转**为 ib 区间扫 0.0ms。
  - 概念映射：AQE＝"分布式版 ANALYZE 在 Stage 之间自动发生"——上一 Stage 的真实行数作为下一 Stage 的策略输入；代价模型只在有统计时才敢做聪明决定。⚠️ AQE 细节见 sql-performance-tuning ✅。

## 5.6 调试与服务器（草案 3.10/3.11 ✅）

- SQL 调试工具箱：`explain formatted`/extended 指标、deprecation 日志开关、事件日志回放（配置族 ✅ https://spark.apache.org/docs/latest/configuration.html）。
- JDBC/ODBC（Thrift）服务器：BI 小查询高并发会放大 driver 负担——现代解法是 gateway 化/独立 SQL 前端（⚠️ 转述趋势）。

## 5.7 小结自检

1. 你的算子链里 shuffle 边界数＝？能否用分区设计减一？
2. E3/E4 合起来说明"数据布局"比"算子技巧"更值钱，对吗？
3. UDF 三宗罪各自对应优化器哪条规则失效？

## 5.8 互链

- API 教学面：../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md、../Spark_The_Definitive_Guide/05-UDF与数据源.md、../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md
- 中文 SQL 性能叙事：../bigdata/04-SparkSQL与结构化数据.md、../bigdata/05-Spark性能优化.md
- 下章接棒：Join 策略全谱 → [06-Join优化](06-Join优化.md)；湖仓元数据：../Use_Iceberg_with_Spark/00-总览与阅读地图.md

## 核心概念速览（中英对照）

- **DataFrame** — 带 schema 的分布式表：Catalyst 与 codegen 的入场券。
- **Dataset** — 强类型分布式集合：编译期类型＋encoder 的折衷层。
- **Catalyst** — 优化器框架：分析→逻辑重写→物理策略三段式规则引擎。
- **物理计划** — Physical plan：Join 策略/Exchange 节点的选择结果，explain 的最后一层。
- **whole-stage codegen** — 全阶段代码生成：算子融合为单 JVM 循环，逐行开销坍缩的来源。
- **UnsafeRow** — 堆外二进制行：Tungsten 紧凑内存格式，语言税的计量单位。
- **分区裁剪** — Partition pruning：按分区键谓词跳读目录/文件，E3 演示对象。
- **列式投影** — Columnar projection：只读所需列，E4 的 24 倍差之根本。
- **UDF 黑箱性** — Opaque UDF：不可下推/合并/生成的优化器边界成本。
- **AQE 统计链** — Runtime stats chaining：Stage 间真实行数反哺后续策略选择。
- **Thrift/JDBC 服务器** — SQL 前端：BI 并发直达 driver 的入口层。
- **保存模式** — Save mode：append/overwrite 等写出语义，下游可复现性的合同条款。

## 最新演进与工业实践

- **AQE 为默认心智**（3.0+）：官方 sql-performance-tuning 页 ✅ 现行条目涵盖分区合并/策略切换/倾斜拆分；"手工广播阈值"多数场景已可交给 AQE，倾斜提示与 Hint 仍是存量刚需。⚠️
- **Python UDF 性能路径更新**：pandas API/Arrow 批式通道把 E4 式列式红利延伸到 Python 生态；"UDF 打断 codegen"的结论不变。⚠️
- **湖仓元数据层前移**：Iceberg/Delta 的隐藏分区与统计裁剪把 E3 的"目录级裁剪"升级为"元数据级裁剪"——谱系见 ../Use_Iceberg_with_Spark/00-总览与阅读地图.md。
- **文献锚（均过 Crossref 200）**：Spark SQL（SIGMOD 2015，DOI 10.1145/2723372.2742797 ✅，Crossref 记录标题作 "Spark SQL"，页 1383-1394）——本章一切自动化优化器的思想源头；Shark（SIGMOD 2013，DOI 10.1145/2463676.2465288 ✅）为其先导。
