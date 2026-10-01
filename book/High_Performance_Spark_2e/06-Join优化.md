# 06 Join优化（Ch6: Joins (SQL and Core)）

> 章题取证 ✅（终版第 6 章＝草案第 4 章"Join (SQL 和 Spark Core)"对位）；草案节级结构 ✅ 实抓：4.1 Spark Core 的 Join（选类型 4.1.1 / 选执行计划 4.1.2）/ 4.2 Spark SQL 的 Join（DataFrame 4.2.1 / Dataset 4.2.2）/ 4.3 小结。本章安置 🔧 E2、E5（**非 Spark 引擎行为**）。

## 0. 本章主线

Join 是分布式 SQL 的第一成本大户：**一切 join 策略差异，本质是"移动数据 vs 移动计算"的汇率问题**。

- 1e 没有独立 Join 章，2e 把它从中段提到核心位——这个动作本身宣告调优对象从 RDD 转向 SQL 执行计划。
- 本章三张地图：策略全谱（6.2）× 倾斜病理（6.3）× 写法纪律（6.4）。

## 6.1 Spark Core 层的 Join（草案 4.1 ✅）

- PairRDD 家族 join/cogroup 的成本构成：两侧都要按同一分区器对齐（同 key 同分区）→ 没有 co-partitioning 就先付一次 shuffle。⚠️＋ https://spark.apache.org/docs/latest/rdd-programming-guide.html ✅
- "选择执行计划"（草案 4.1.2）：小表侧手工广播到对方分区（BHJ 原型）、用分区器换共置——SQL 层优化器的这些策略全部脱胎于此。
- 中文互证：../bigdata/02-Spark核心与RDD模型.md、../bigdata/03-Shuffle与宽依赖.md。

## 6.2 Spark SQL 层的策略全谱（草案 4.2 ✅；⚠️ 策略与阈值按官方 sql-performance-tuning 页 ✅ 转述）

- **BroadcastHashJoin（BHJ）**：小表上发、大表零 shuffle；`spark.sql.autoBroadcastJoinThreshold`（约 10MB 量级默认）是经典旋钮；AQE 可运行时纠正误判。
- **SortMergeJoin（SMJ）**：双侧按 join key 重分布＋分区内排序归并——大表对大表的默认解，排序是隐性税。
- **ShuffleHashJoin（SHJ）**：SMJ 的免排序变体，吃内存换排序。
- **Cartesian 避免**：无等值键→笛卡尔积灾难；重写谓词优先于调参。
- **Join 类型语义**：inner/left/semi/anti 的执行差异（anti/semi 免收集右列）；等值与否决定策略射程。
- 策略选择一览（示意）：

| 规模组合 | 首选 | 触发条件 |
|---|---|---|
| 大×小（可广播） | BHJ | 统计显示一侧低于阈值 |
| 大×大 等值 | SMJ | 默认 |
| 大×大 内存富余 | SHJ | 免排序换空间 |
| 无等值键 | 重写查询 | 任何引擎都救不了笛卡尔 |

- 🔧 **E2 策略量级差实测（DuckDB，非 Spark）**：
  - 方法：500 万 fact × 40 万 dim；(a) 等值 join；(b) 同数据量改不等值区间条件 `f.k>=d.k AND f.k<d.k+3`；分别计时＋EXPLAIN 记节点名。
  - 结果（本机）：等值得 **HASH_JOIN** 节点 0.02s；不等值落入专用区间算子节点（计划显示 IE_JOIN）1.65s——**约 80 倍**。
  - 概念映射：谓词形状决定 join 节点、节点决定数量级；Spark 侧同理——join key 被函数包裹/等值条件写漏，就能让 BHJ/SMJ 跌进低效路径。⚠️
- 🔧 **E5 热点键拆分实测（SQLite，非 Spark）**：
  - 方法：150 万行事实表、热键 k=7 占 30%；(a) 直接 join 维表；(b) 热键单独拆出聚合＋冷键正常 join；比时。
  - 结果（本机）：(a) 3.37s vs (b) 3.50s——**单机拆分无收益**。
  - 诚实判读：salting/热拆的红利**只在并行分区间负载均衡时兑现**；单执行器上拆分只添开销。这条负结果是"背技巧不背前提"的解药，也解释了为何 E5 的解药要等 AQE 的"分区拆分"才有分布式落点。⚠️ Spark 侧 SKEW hint/AQE skew 开关见 sql-performance-tuning ✅。

## 6.3 倾斜：分布式 join 的慢性病（⚠️ 转述）

- 形态学：key 频率长尾（热点业务实体、NULL/默认值堆积、日期粒度不足）。
- 诊断式：task 时长分布 vs 输入字节分布（UI Stage 详情），两分布错位即倾斜实锤。
- 药方阶梯（先便宜后昂贵）：
  1. 修数据：NULL 打散、脏键过滤、粒度重选；
  2. 调并行/分区：加盐粒度、预聚合缩热键；
  3. 引擎开关：AQE 倾斜拆分、SKEW hint；
  4. 改架构：维表打宽进事实表、Lambda 侧预 join。
- 中文互证：../bigdata/05-Spark性能优化.md 倾斜条目。

## 6.4 写法层纪律清单（草案 4.2.1/4.2.2 ✅）

- join key 保持裸列（函数包裹＝下推失效＋策略降级）；
- join 前先 filter 缩两侧（列裁剪与谓词下推的自家用法，接 05 章）；
- 多表链式 join 警惕中间膨胀（星型先维后事实、或先半连接收敛）；
- 同 key 反复 join 考虑合并成一次宽表；
- Dataset 强类型 join 的 encoder 成本与 05 章互引；区间 join（asof）需求走专用实现，别硬写不等值自连接（E2 的 80 倍教训）。⚠️

## 6.5 小结自检

1. 三种主力策略各自"移动什么"？一句话说清。
2. E5 为什么单机无收益？红利的物理位置在哪？
3. AQE 默认时代，hint 还有存在价值吗？举一例。

## 6.6 互链

- 上游统计与计划：[05-DataFrame与SparkSQL](05-DataFrame与SparkSQL.md)；下游分区机理：[08-键值对数据与Shuffle](08-键值对数据与Shuffle.md)
- 架构口径：../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md；SQL 侧：../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md
- 中文叙事：../bigdata/03-Shuffle与宽依赖.md、../bigdata/05-Spark性能优化.md
- 食谱式条目对位（登记不链）：#154 Spark Cookbook
- 论文锚（均过 Crossref 200）：Shark（SIGMOD 2013，DOI 10.1145/2463676.2465288 ✅，记录标题作 "Shark"）；Spark SQL（SIGMOD 2015，DOI 10.1145/2723372.2742797 ✅，页 1383-1394）——SQL-on-Spark 策略谱系由此奠基；书目线 ../../db/db.md。

## 核心概念速览（中英对照）

- **BroadcastHashJoin** — 广播哈希连接：小侧上发、大侧零 shuffle 的最优等值策略。
- **SortMergeJoin** — 排序归并连接：双侧重分布＋排序归并，大表对大表默认解。
- **ShuffleHashJoin** — 洗牌哈希连接：以内存换排序的 SMJ 变体。
- **autoBroadcastJoinThreshold** — 广播阈值：统计决定 BHJ 资格的旋钮，AQE 可运行期纠错。
- **数据倾斜** — Data skew：key 分布长尾把并行任务拖成串行短板，join 与聚合通病。
- **salting** — 加盐：热点 key 打散再归并的技巧，红利仅在并行区间（E5 负结果）。
- **co-partitioning** — 同分区：join 前免费条件，PairRDD 层的古老智慧。
- **semi/anti join** — 半/反连接：存在性过滤专用，可免收集右列。
- **笛卡尔积** — Cartesian product：无等值键的默认下场，数量级灾难一号。
- **SKEW hint** — 倾斜提示：优化器统计失明时的人工补光。
- **IEJoin** — 区间连接算子：不等值连接的专用节点（E2 中 80 倍差的当事节点，DuckDB 名词）。
- **中间膨胀** — Intermediate blow-up：多表链式 join 的行数波峰，重排与收敛的对象。

## 最新演进与工业实践

- **AQE 倾斜拆分为默认路径**（3.x+，✅ sql-performance-tuning 页）：运行时按字节/行数阈值自动拆热分区并行化；"手工 salting"退居极端热点与广播失败兜底。⚠️
- **Photon 类原生引擎**（商业发行版）以向量化哈希表把 BHJ/SMJ 再提一档，开源主线以向量化读＋codegen 跟进；系统名叙述不引文献（该论文本轮取证未过，⚠️）。
- **工业复盘共识**："join 慢先看 key 形状再看参数"——脏键（NULL/默认值堆积）修复的事故出场率高于任何调参故事。
- **与湖仓交互**：维表入湖后，"小表可广播"的大小判断变成表维护问题——compaction 直接影响文件数与统计质量，见 ../Use_Iceberg_with_Spark/06-维护过程与流式写入.md。
- **口径提醒**：Spark 的 join 策略细节（阈值默认值、hint 语法效力）一律以当版官方调优页 ✅ 为准，本册全部 ⚠️ 转述不实测。
