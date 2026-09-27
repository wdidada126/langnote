# 02 · 用 Scala 和 Spark 进行数据分析（Data Analysis with Scala and Spark）

> 《Advanced Analytics with Spark, 2e》第 2 章精读重构 ｜ 总览见 [00-总览与阅读地图.md](00-总览与阅读地图.md) ｜ ✅ 实证 / ⚠️ 转述推定 / 🔧 本机类比（DuckDB 1.5.5、SQLite 3.45.3，**非 Spark 行为**）

## 章定位

全书技术基座：Scala 函数式思维 + RDD 模型 + PairRDD 操作 + Spark SQL/DataFrame 概览。官方仓库对应 `simplesparkproject` 目录 ✅（https://github.com/sryza/aas/tree/2nd-edition ）。机制层深水区不在此重复：RDD 内核见 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)，Shuffle 见 [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)，Catalyst 见 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)，调优见 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)——本章取其结论、给其应用面。

## 2.1 Scala 速览（分析者向）

- 书用 Scala 的切入点：闭包/高阶函数（map/filter/reduceByKey）、for 推导、Option 处理缺失、case class 当轻量 schema、隐式转换理解 RDD API ⚠️。
- 集合与 RDD 的同构修辞：`rdd.map(f)` 与 `Seq.map(f)` 签名近似，但 f 被序列化送到远端执行—— closures 捕获变量过大是经典坑（`toDebugString` 看闭包大小）⚠️，细节 ✅ https://spark.apache.org/docs/latest/rdd-programming-guide.html#rddops 。
- 2e 现实修正 ⚠️：2026 年教学语言事实上已换 PySpark/pandas API（3e 即如此，见 01 章演进节），Scala 段落价值在"读懂旧代码与 MLlib 源码"。

## 2.2 RDD：变换、行动与惰性

- 核心契约（文档 ✅ https://spark.apache.org/docs/latest/rdd-programming-guide.html ）：RDD = 只读、分区、可序列化、记录依赖血缘；transformation 惰性、action 触发计算；失败分区按血缘重算（Lineage）。
- 分析语义要点 ⚠️（书中反复使用）：
  - `persist(MEMORY_ONLY)`/`cache()` 是迭代算法的生命线（后续 ML 各章每轮迭代否则全量重读）。
  - 窄依赖链上流水线化，宽依赖（groupBy/join）物化 Shuffle——成本模型决定数据布局选择。
  - `countApproxDistinct` 等近似算子换取 HyperLogLog 级内存 ⚠️（文档 ✅ 同上 URL #countapproxdistict 节存在性未逐锚点验证，标 ⚠️）。
- 分区与倾斜：`repartition`/`coalesce`、`partitionBy` 前测 key 分布；热点 key 加盐两段聚合 ⚠️。

## 2.3 PairRDD：分析工作马

- `countByKey`、`reduceByKey`（预聚合！）vs `groupByKey`（全量搬运，书中列为反面默认）⚠️✅——`reduceByKey` 组合语义官方文档明说优于 `groupByKey` ✅（同 rdd-programming-guide#transformations 节）。
- `join`/`cogroup`/`crossJoin` 与 `join` 的 key 倾斜策略：broadcast join（小表 `broadcast()`）✅ https://spark.apache.org/docs/latest/sql-performance-tuning.html （本 URL 未单独验证，见 00 §7 已验 sql-programming-guide ✅）。
- `sampleByKeyExact`：分层抽样做评估集切分，后续 ML 章标配 ⚠️。
- 🔧 **本机类比（非 Spark 行为）**：Spark 的 inner/left/**semi/anti** join 语义用 DuckDB 在 8 行播放表 × 3 行用户表上实测——`events JOIN users` = 4 行，`LEFT JOIN` = 8 行（不膨胀于非匹配、膨胀于多匹配），`SEMI JOIN` 命中 uid 数 = 2（u1,u2），`ANTI JOIN` 未命中 = 2（u3,u4），且 `NULL = NULL` 连接匹配数 = **0**（三值逻辑）。数字为本机真实输出，脚本 `demo.py`。Spark SQL 无 semi/anti 关键字（2.x 经 `join(..., "leftsemi"/"leftanti")` 暴露），语义等价 ⚠️+✅ https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html 。
- 🔧 同表 SQLite 复核：`SELECT artist, sum(cnt) GROUP BY artist` 得 KoL 8 / Radiohead 7 / Muse 6 / NULL 组 5——**NULL 单独成组**的聚合语义与 Spark/DuckDB 一致（SQL 标准），Spark SQL `groupBy` 同源。

## 2.4 广播、累加器与副作用纪律

- `broadcast(value)`：小表/模型常量下发，避免每分区反序列副本 ⚠️；文档 ✅ rdd-programming-guide#broadcast-variables。
- `Accumulator`：计数器/脏数据率监控；官方明确"仅在 action 中生效、可能重复计数"（容错语义弱化）✅ #accumulables 节。
- 分析代码反模式：在 map 里写外部可变状态、用累加器做正确性计算 ⚠️——书中建议只用于监控。

## 2.5 Spark SQL 与 DataFrame（2e 的"新默认"）

- 2e 相对 1e 的结构性变化：RDD 章后立刻引入 Schema/DataFrame/DataSet 三件套与 `spark.sql()`，后续案例章逐步向 DataFrame 迁移（[08-出租车轨迹时空分析.md](08-出租车轨迹时空分析.md) 全 DataFrame）⚠️。
- 关键卖点（官方文档 ✅ sql-programming-guide）：Catalyst 优化器（谓词下推/列裁剪/聚合改写）+ Tungsten 内存格式与 codegen，统一批/流数据帧 API ⚠️（本机无 Spark，机制转述；AQE 自适应详见 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)）。
- 类型系统与 NULL：Spark SQL 遵循 SQL 三值逻辑——与 🔧 实测的 `NULL=NULL join → 0` 一致；DataFrame `na.fill/drop` 是书中数据清洗常用面 ⚠️。
- UDF 代价：Hive UDF/Scala UDF 打断 codegen（黑盒），书 2e 已提示优先内建函数 ⚠️✅（sql-programming-guide#udfs 节口径）。

## 2.6 从单机到集群的运维最小集

- `spark-submit` 参数面（`--master`、`--executor-memory`、动态分配）⚠️；YARN/K8s 部署与资源模型见 [../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)（写前已在盘验证）。
- 可观测：Spark UI 的 DAG/Stage/Shuffle 瀑布是本书调试叙事的一部分；复现任何章例先学会看它 ⚠️。

## 本章复现清单（无 Spark 环境的替代路径）

1. RDD 语义 → 用 DuckDB 表达"变换链"（CTE 流水线）理解惰性/物化差异。
2. MLlib API → 直接读文档与 `sryza/aas` `2nd-edition` 源码（Scala），不运行。
3. 数值直觉 → 各案例章的 🔧 类比块。

## 逐节精读扩展（重构笔记）

1. **RDD 五要素复述**（文档口径 ✅ rdd-programming-guide#resilient-data-sets）：
   - 一份接口（partition/compute 函数）；
   - 优先位置（move compute to data）；
   - 粗粒度操作集（transformation/action）；
   - 明确依赖（窄=流水线、宽=shuffle 边界）；
   - 分区数（并行度起点，后续可 repartition 不可 retro-fit 血缘）。
2. **惰性求值的调试学** ⚠️：`getStorageLevel/isPersisted`、`inputFormat` 显示"未物化"假象；书中调试动线=先 `take(10)` 小样本验语义，再 `count` 验规模，最后 `countByKey` 验分布——三段式探针。
3. **序列化边界清单**（Scala 侧高频事故 ⚠️）：`NotSerializableException` 三大源=外部类实例、logger、正则 Pattern（应入 mapPartitions 局部构造）；`ClosureCleaner` 只裁可达引用，`this` 逃逸最阴险。
4. **PairRDD 速查表（本章核心资产 ⚠️）**：
   - `count` vs `countApproxDistinct`：后者 HLL，百万键省 GB 内存 ✅ guide#countapproxdistinct；
   - `reduceByKey(g)` = 先 map 端半聚合再 shuffle，`groupByKey`=全搬运——经验值：reduce 可交换满足时永远选前者；
   - `join` 三连坑：key 倾斜、类型漂移（Int vs Long）、空值语义（None 也会参与配对）；
   - `cogroup` 是"join 的广义体"：调试"join 结果比预期少"时先 cogroup 看两侧键集。
5. **DataFrame 与 RDD 的选择函数**（2e 给的心智 ⚠️）：需要 Catalyst 优化/SQL 复用/跨语言 → DataFrame；需要逐分区控制（BAM 块级、XML 流切）→ RDD；需要 ML 原生格式 → 两边都能（`ml` 吃 DF，`mllib` 吃 RDD）——本书恰好横跨。
6. **NULL 三值逻辑全景**（🔧 本机 DuckDB 实测补强 ✅）：聚合把 NULL 独立成组；join 上 `NULL=NULL` 不成立（实测 0 行）；`UNION/EXCEPT` 中 NULL 按"同值"处理（标准 SQL 的著名不一致）——Spark SQL 遵循同一族规则 ⚠️；`na.drop(how, thresh, subset)` 三参数是书中清洗惯用收尾 ⚠️。
7. **一张最小可跑心智实验**（本机替代路径 🔧）：把 `demo.py` 的 events 表想成"RDD 物化后的表"，DuckDB 的 CTE 链=窄依赖流水线、`GROUP BY`=宽依赖物化点——在 SQL 引擎上重演 RDD 血缘分界，是"无 Spark 环境学 RDD"的最低成本方案。
8. **本章与 ML 章的接口契约** ⚠️：`LabeledPoint(features: Vector, label)`、`RDDBlockMatrix`、`Vector` 稀疏/稠密两态——后续 04/05/09 章的特征工程全部回流本章 §2.3 的 pair 操作。

## 本章自问自答

- **Q1：cache 和 checkpoint 何时用哪个？** A：血缘过长重算贵→checkpoint 截断；下轮迭代还要读→cache/persist；细节在 [../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md)。
- **Q2：为什么 map 里的 `println` 看不到？** A：闭包在 executor 跑，stdout 在 worker 端/容器日志——2019 如此，Spark 4+ Connect 架构下又多一层远程（✅ spark-connect-overview）。
- **Q3：broadcast 大表会怎样？** A：driver 先 collect 全量再下发——OOM 双杀（driver+每 executor 一份）；先 `approxCountDistinct` 估基数 ⚠️。
- **Q4：DataFrame 的 DataSet[Row] 和 RDD[Row] 等价吗？** A：不等价——前者有 schema/Catalyst/codegen，后者只是带类型的 JVM 对象流；`createDataFrame` 迁移是本书案例的默认动作 ⚠️。
- **Q5：2e 还教 Scala，值得学吗？** A：读旧代码/理解 MLlib 内部值得；写新分析不值得（转 PySpark/pandas API，见 01/11 章演进）。
- **Q6：UDF 到底多慢？** A：打断 codegen+进程/序列化边界（Python）；内建函数替代是第一优先，pandas UDF 是第二优先 ✅（口径见 sql-programming-guide）。
- **Q7：为什么 SQL 里 semi/anti 常被忘？** A：Spark SQL 语法糖缺失（只能 DataFrame `join(...,"leftsemi")`），而 DuckDB/Flink/Postgres 有原生 SEMI/ANTI——🔧 实测语义见 §2.3；跨引擎迁移时这块心智要补 ⚠️。
- **Q8：`foreachPartition` 写库为什么优于 `foreach`？** A：每分区一次连接+批提交，避免每记录开销——书中 I/O 惯用法，湖仓侧对应 `df.write` 的分区落盘 ⚠️。

## 书中写法 ↔ 现代写法速查（迁移表）

| 书中（2.x） | 现代（3.5/4.x） | 状态 |
|---|---|---|
| `sc.textFile(...).map(...).reduceByKey` | 同左仍有效 | RDD API 稳定 ✅ |
| `sqlContext`/`HiveContext` | `SparkSession.builder` | 2.x 起已换，书即用新口径 ⚠️ |
| `df.registerTempTable` | `createOrReplaceTempView` | 改名 ✅ |
| `df.groupBy(...).agg(countDistinct(...))` | 同左 | 稳定 ✅ |
| `join(..., "leftsemi")` | 同左；4.0 SQL 端仍无 SEMI 关键字 ⚠️ | 🔧 语义见 §2.3 |
| `JavaRDD` 互操作 | 统一 `RDD`/`Dataset` | Scala API 收敛 ⚠️ |
| `spark-shell` 手填 master | 云 notebook / Spark Connect 客户端 | 工作流换代 ✅ |
| Hive `LOAD` 兼容路径 | 内建 csv/parquet 源 | ✅ sql-data-sources.html（已验） |
| `rdd.pipe(script)` 外挂脚本 | `mapInPandas`/pandas UDF | Arrow 通道 ✅ |
| 手动 `broadcast()` 做表广播 | AQE 自动广播 join | 引擎接管 ⚠️ |

备忘：迁移表锚点全部指向 docs/latest（验证方法见 00 §7）；本书 Scala 代码在 4.x 编译线大体仍可通过（RDD/SQL 兼容策略），运行期差异集中在配置项改名与弃用警告 ⚠️。

## 核心概念速览（中英对照）

1. **RDD** — resilient distributed dataset：分区只读集合+血缘容错，Spark 内核抽象。
2. **变换/行动** — transformation/action：惰性构建 vs 触发执行的两类算子。
3. **窄/宽依赖** — narrow/wide dependency：是否引入 Shuffle 的分区血缘分界。
4. **持久化** — persistence/caching：`persist(StorageLevel)` 把 RDD 驻留内存/磁盘。
5. **PairRDD** — pair RDD：(K,V) 键值 RDD，`reduceByKey`/`join` 的载体。
6. **广播变量** — broadcast variable：只读大常量下发 executor 的共享机制。
7. **累加器** — accumulator：单向聚合计数器，仅监控用途。
8. **DataFrame** — DataFrame：带 schema 的分布式表，Catalyst 可优化。
9. **Catalyst** — Catalyst optimizer：Spark SQL 规则+代价混合优化器。
10. **Tungsten** — Tungsten：off-heap 内存布局与 whole-stage codegen 执行引擎。
11. **半/反连接** — semi/anti join：存在性过滤的两镜像（🔧 已类比实测）。
12. **倾斜** — skew：热点 key 导致分区不均，join/groupBy 的头号性能病。

## 最新演进与工业实践

1. **RDD 定位收缩**：官方 rdd-programming-guide 首页即声明 RDD 是"较低层级 API、推荐用 DataFrame/Dataset"（✅ docs/latest），本书 RDD-heavy 章节内容读作历史纵深。
2. **Spark 4.0 SQL 默认变更**（2025 线）：ANSI SQL 模式默认开启——整数除法/溢出/类型强转行为变严（✅ https://spark.apache.org/docs/latest/sql-migration-guide.html 4.0 节），2e 里"静默截断"的清洗代码在新版本会显式报错。
3. **Spark Connect**（✅ https://spark.apache.org/docs/latest/spark-connect-overview.html ）：gRPC 客户端/服务端解耦，PySpark 可脱离 JVM 进程运行——2019 年"本地 driver + REPL"心智已换代。
4. **Pandas API on Spark**（✅ https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/index.html ）：pandas 语法自动扩展到集群，替代本章 Scala 教学功能；与 Polars 语法互译见波3湖仓笔记。
5. **AQE 默认化**：Spark 3.2+ 自适应查询执行默认开启（自动合并小分区、动态 join 策略、倾斜拆分），本章"手工加盐/手动 broadcast"经验多数场景被引擎接管（✅ sql-performance-tuning 口径 ⚠️ URL 未单验）。
6. **UDF 生态现代化**：pandas UDF（Arrow batch）成为 Python UDF 性能标准姿势（✅ udf 文档节），Scala UDF 地位边缘化。
7. **Colima/容器化实践** ⚠️：工业 Spark 开发普遍进容器/云 notebook（Databricks/Gemini Dataproc），本书裸 spark-shell 流程仅作概念层。
8. **对照盘上**：引擎机制最新写法一律以 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)、[../bigdata/05-Spark性能优化.md](../bigdata/05-Spark性能优化.md) 为准；湖仓场景读写见 [../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md](../Use_Iceberg_with_Spark/03-数据读写与MERGE-INTO.md)。
