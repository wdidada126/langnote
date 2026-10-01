# 04 Spark SQL: Advanced（Spark SQL 进阶）

> 原书 Ch4，pp.111–182——72 页的全书技术核心：Catalyst/Tungsten 内部机制、UDF、表达式与 Dataset、窗口函数、连接策略。二级小节未实抓 ⚠️，主题簇依章题、页幅与官方文档骨架推定重构；属**精读重构**。

## 4.1 Catalyst：四步计划流水线 ⚠️（转述+🔧 类比）

- 骨架（官方口径）：unresolved logical plan →（Analyzer 对 Catalog 解析）analyzed →（Optimizer 规则改写）optimized logical →（Planner 选执行策略）physical plan → RDD 流水线执行。
- 规则改写族：谓词下推、列裁剪、常量折叠、join 重排；「表达式编码」把计划变成 Scala AST 交给 Tungsten 整段代码生成。
- 入门者正确的使用姿势不是背流程，而是学会 `explain()`/`EXPLAIN FORMATTED` 读物理计划：认得出 `*(1) HashAggregate`、`SortMergeJoin`、`BroadcastHashJoin`、`Exchange`（=shuffle 边界）⚠️（Spark 计划文本面转述官方文档）。
- 🔧 **实验 E1**（DuckDB 1.5.5，**非本书 Spark 引擎行为**）：orders(200k 行)⋈customers(97 行)+双谓词+group by——EXPLAIN 产出 `SEQ_SCAN → HASH_JOIN(INNER) → HASH_GROUP_BY` 算子树，执行 9.7ms。同构点：优化后的物理计划同样以「扫描/连接/聚合」三算子成形，谓词并入扫描/连接；差异点：Spark 的 Exchange 显式标注 shuffle，DuckDB 单机计划没有网络重分布这一维。类比只证「计划树长这样」，不证 Spark 的数值与规则集。

## 4.2 Tungsten：内存与代码生成 ⚠️

- 三件套叙事：off-heap 二进制行布局（免 JVM 对象头/GC 指针追逐）、cache-aware 计算、whole-stage code generation（janino 编译执行）。
- 教学落点：本册用「生成代码 vs 火山模型逐算子虚调用」解释为什么 SQL 路径比 RDD 手写快——结论级记忆：**走 DataFrame/SQL，把优化器的活交给优化器**。
- 版本诚实：3.x 的 Adaptive Query Execution（AQE，2020 默认开启）补上了运行期重规划（动态 coalesce 分区、运行期改 join 策略、倾斜拆分）——本册成书时 AQE 已 GA 但篇幅地位 ⚠️ 存疑；2026 视角：不读 AQE 的 Spark SQL 教学等于没教优化。引用纪律：本章 URL 仅采信已验证 200 的 latest 主页与 sql-programming-guide.html/sql-ref-functions-builtin.html，其余路径不写全防 404。

## 4.3 UDF/UDAF：能力与代价的对称课 ⚠️ + 🔧 E2

- 注册面：`spark.udf.register`（SQL 文本用）/ Scala/Python 函数直挂 DataFrame 表达式；UDAF 旧线（Aggregator API）在本册给 Python 侧 ⚠️。
- 代价面（本册金句级论点重构）：UDF 对 Catalyst 是**不透明黑箱**——规则无法下推其内部谓词、无法折叠、codegen 无法内联标量函数体，还引入逐行序列化。解法排序：内置函数 > pandas/vectorized UDF > 普通 UDF。
- 🔧 **实验 E2**（DuckDB 1.5.5，**非本书 Spark 引擎行为**）：200 万行字符串谓词计数——原生表达式 `upper(st)='SHIPPED'` **14.0ms** vs Python UDF（逐行）`pycheck(st)` **1468.7ms**，**约 105 倍**；且 EXPLAIN 中 UDF 查询无任何下推收益（UDF 作为不可拆函数留在投影层）。同构现象在 Spark 里同样成立 ⚠️（官方文档明确 UDF 阻断优化）；105 倍这个数值纯属单机 DuckDB 标本，量级方向可借来记「UDF 不是免费的」。
- 边界：DuckDB 的 Python UDF 无 Arrow 批量模式对比项，故「vectorized UDF 挽回多少」在本类比中**缺席**，勿据此外推 pandas_udf 收益 ⚠️。

## 4.4 表达式 API 与 Dataset：typed/untyped 双面 ⚠️

- Column 表达式树：操作符重载背后是 `UnresolvedAttribute/GreaterThan/...` 逻辑节点——本册用 `expr()` 与字符串表达式证明「SQL 文本、表达式对象、DSL 三者同构」。
- Dataset[T]（Scala/Java）：类型安全+编码器（Encoder）桥进行列式内存；Python 无此层，只有 DataFrame——入门者常误以为 Python 缺了「高级面」，实则 DataFrame 就是那条主线。
- `withColumn` 链式打补丁的反模式教学（列爆炸、重复表达式不折叠）⚠️ 主题簇推定，2026 社区口径依旧。
- 对照盘上：Dataset/类型面权威章 [../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)。

## 4.5 窗口函数与 join 策略 ⚠️

- 窗口面：`Window.partitionBy().orderBy()` + rows/range frame；over-watermark 概念在此预铺（Ch7 收费）；内置函数清单官方锚点 https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html（✅ curl 200）。
- join 策略三面：BroadcastHashJoin（小表广播，阈值 `spark.sql.autoBroadcastJoinThreshold`）、SortMergeJoin（大表标配，先 shuffle 排序）、ShuffleHashJoin（不排序变体）；`hint` 语法（BROADCAST/SORT_MERGE）是入门者第一次「手调计划」的合法入口 ⚠️。
- AQE 时代修正：join 选择可运行期改判，静态阈值不再是命运——读本册此节时叠这层 ⚠️。

## 4.6 本章练习视角（重构）⚠️

自建四连：① 对同一查询写 DSL/SQL 两版并 `compare` 计划一致；② 把内置谓词换成等价 UDF，观察 `Exchange`/`Filters` 文本差异；③ 一张 99% 命中一值的倾斜键表 join，对比 broadcast 与 shuffle 路线；④ 窗口跑累计和，改 range frame 验证边界行变化。

## 4.7 explain 读法图解（文字版 ⚠️ 转述官方计划文本面）

- 自底向上读三件事：扫描节点（读了多少/裁了什么）→ Exchange 行（几次洗牌/分区键）→ 顶层聚合/写出。
- 认算子（Spark 计划文本惯例）：`HashAggregate`/`SortAggregate`、`BroadcastExchange`+`BroadcastHashJoin`（无 Exchange=广播路线）、`SortMergeJoin` 前置两个 `Exchange`+`Sort`、`*(n)` 星号=codegen 融合段。
- AQE 生效后计划会出现 `Coalesce`/AdaptiveSparkPlan 包装行——入门教材（含本册）大多没画它，见到别慌 ⚠️。
- 🔧 同构练习（**非 Spark 行为**）：把 4.1 的 DuckDB 计划文本（`SEQ_SCAN→HASH_JOIN→HASH_GROUP_BY`）当「无 Exchange 版 Spark 计划」读——算子语义一一对应，只差网络维；训练「先读计划再调参数」的反射，比背十张调参表有用。

## 4.8 Catalyst 规则与扩展面（重构 ⚠️）

- 规则族速记：
  - 谓词下推 PushDownPredicates（穿 project/join/agg 找可下推条件）；
  - 列裁剪 ColumnPruning（没被引用的列不进扫描）；
  - 常量折叠 FoldableExpression（`1+2`→`3`）；
  - 布尔化简 SimplifyBooleanExpressions；
  - join 重排与优化器策略（低基数侧先连）。
- 可扩展性一句话：Catalyst 是规则引擎，企业可注入自定义 Rule/Strategy（本册概念级点到 ⚠️ 存疑）——这是 Spark SQL 能吞百种数据源的架构原因，与 Trino 的 optimizer 叙事对照：盘上 [../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md](../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md)。
- 与 DuckDB 对照的诚实边界：DuckDB 优化器同样有谓词下推/聚合改写，但无「分布式策略选择」问题空间——本目录 🔧 E1 只借它的「计划可见性」，不借它的规则集 ⚠️。

## 4.9 UDF 使用守则（重构清单 ⚠️）

1. 先查内置函数清单（✅ https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html 已验证可达）——90% 的「我要写 UDF」在这里终结。
2. 非写不可：Python 侧优先 pandas_udf（Arrow 批量）；Scala 侧优先高阶函数/表达式组合。
3. 注册即契约：给 UDF 声明确定性（deterministic），否则下推/折叠彻底失去它。
4. 性能怀疑顺序：UDF > join 策略 > 分区数——E2 的 105 倍是「先查 UDF」的数据依据（DuckDB 标本方向，Spark 幅度另计 ⚠️）。
5. 逃生通道：UDF 里做的事能改写成 SQL 时，改写成 SQL——代码即文档，计划也可读。

## 4.10 窗口与 join 的最小例题（重构 ⚠️）

- 窗口题眼：「每城市取金额前 2 名订单」——`row_number().over(Window.partitionBy(city).orderBy(desc(amt)))` 过滤 ≤2；变体：dense_rank 与 rank 的并列语义差异，练习时三种都跑一遍看行数。
- join 题眼：订单表⋈客户表，客户侧 97 行/3KB——广播阈值默认 10MB 内，观察计划里没有 Exchange 只有 `BroadcastExchange`；把阈值调 0 后同一查询多出两个 `Exchange`——一次「计划肉眼可见的决策改变」入门实验（Spark 侧 ⚠️ 转述，非本机可跑）。
- 与本目录 🔧 E1 的衔接：同题在单机引擎只有一种 join 选择面，「策略」这个概念在单机世界里不存在——理解这一点，就理解了分布式 SQL 优化的第一课。

## 4.11 速自检（答案在上文）

1. Catalyst 四步流水线的输入输出各是什么形态的计划？
2. Analyzer 靠什么把「未解析」变「已解析」？
3. 规则改写五族各举一例。
4. Tungsten 三件套解决 JVM 的什么病？
5. codegen 融合段的标记（`*(n)`）在计划文本里怎么认？
6. AQE 的三项运行期能力是什么？
7. UDF 为什么阻断下推？三条补救路径？
8. pandas_udf 快在哪一层（序列化/循环/内存格式）？
9. Dataset[T] 与 DataFrame 的关系一句话？
10. rows 与 range 窗口框的差别用一句话说清。
11. 三种 join 策略各自的前提与代价？
12. 🔧 E2 的 105 倍在 Spark 里能直接引用吗，为什么？

## 4.12 易混淆三连（辨析卡 ⚠️）

- 逻辑优化 vs 物理策略：谓词下推改的是「算什么」，广播/SMJ 选的是「怎么算」——`explain` 里分别看 Filter 位置与 Exchange 数。
- UDF vs UDTF vs 表达式函数：一行一进一出是标量 UDF；一行多变是 explode 族；列间组合优先内置表达式而非封装 UDF。
- cache table vs cache DataFrame：Catalog 级缓存与会话级缓存两套账本，混用时 `clearCache()` 的可见范围要分清（官方文档口径 ⚠️）。

## 4.13 微补：计划文本的两种口径

- `df.explain()` 默认给「简化+逻辑+物理」三段；`EXPLAIN FORMATTED` 才是本目录 4.7 读法对应的形态——入门教材截图常混用两口径，读图先认口径。
- 本目录 🔧 类比统一采用「物理计划」口径对齐（DuckDB `EXPLAIN` 产物是物理算子树），逻辑计划层类比缺席，特此登记。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 优化器 | Catalyst | Spark SQL 的规则式逻辑+物理优化器 |
| 分析器 | Analyzer | 用 Catalog 把未解析计划变成解析计划 |
| 物理计划 | Physical Plan | 选定执行策略后、可编译执行的算子树 |
| 全阶段代码生成 | Whole-Stage CodeGen | 多算子融合成一段 JVM 字节码 |
| 堆外内存 | Off-heap/Tungsten Memory | 二进制布局绕开 JVM 对象开销 |
| 自适应执行 | AQE | 运行期统计驱动的重规划 |
| 用户自定义函数 | UDF | 对优化器不透明的标量黑箱 |
| 向量化 UDF | Pandas/Vectorized UDF | Arrow 批量执行缩小黑箱代价 |
| 编码器 | Encoder | 类型对象↔列式内存的桥 |
| 窗口框 | Window Frame | rows/range 定义的移动聚合视界 |
| 广播连接 | BroadcastHashJoin | 小表侧整份分发避免 shuffle |
| 排序合并连接 | SortMergeJoin | 双侧重分布排序后归并的大表路线 |
| 连接提示 | Join Hint | 用户干预策略选择的合法入口 |

## 最新演进与工业实践

- **AQE 成为默认心智（2021→2026）**：本册成书时 AQE 刚 GA（3.0），2026 文档已把「先让 AQE 干、不效再 hint」写成标准流程 ⚠️（官方口径）；DPP（动态分区裁剪）补上 join 侧的运行时分区裁剪，与本目录 🔧 E5 的静态 File Filters 形成两级对照。
- **UDF 面的两条新解法**：Python side 的 pandas API on Spark 与 Query Commerce 时代的「用 SQL 内建函数重写」运动；社区统计性结论「UDF 是性能问题第一来源」在 2024–2026 各 Spark 峰会议题中持续在榜 ⚠️（会议公开议题，非实证数字）。
- **计划可观测工业栈**：Spark UI SQL 页签的 planviz、外部（云厂商）执行画像；论文线：Catalyst 本体无独立正式论文、Tungsten 见官方博文系 ⚠️——本目录不造 DOI，深读走 [../../db/db.md](../../db/db.md) 引擎条目与 [../数据库系列·总索引.md](../数据库系列·总索引.md)。
- 4.0 提示：ANSI 默认化改变比较/溢出/除零语义，回读本章任何「边界值行为」断言需先确认 ANSI 开关状态 ⚠️。
