# 08 键值对数据与Shuffle（Ch8: Working with Key/Value Data）

> 章题取证 ✅（终版第 8 章＝草案第 6 章"处理键值对数据"对位）；草案节级结构 ✅ 实抓：金发女孩案例（v0 迭代方案、PairRDDFunctions/OrderedRDDFunctions）/ 键值上的行动 / groupByKey 的风险 / 选聚合操作 / 多 RDD 操作 / 分区器（Spark 分区器、哈希、范围、自定义、跨转换保留分区、co-located/co-partitioned、映射与分区函数字典）/ OrderedRDDFunctions 字典 / 二级排序与 repartitionAndSortWithinPartitions（版本 2/3/4）/ 掉队检测与不均衡数据。⚠️ 终版或有改序，以"机制透明层"读之不失其值。

## 0. 本章主线

PairRDD 世界是 Spark 调优的"解剖室"：key 决定分区去向、分区器决定 co-location、排序发生在分区内——**三级机制全透明**，而 SQL 层把这些旋钮藏在优化器后面。学这里不是为了写 PairRDD，是为了在 SQL 出问题时知道"引擎本来可以做什么"、优化的物理边界在哪里。

本章的三层解剖图：

```
key 值域 ──> Partitioner.getPartition(key) ──> 分区号（数据去向）
分区号一致 ──> co-partitioned（join/合并免 shuffle）
分区内序   ──> OrderedRDDFunctions（二级排序/组内归并的前提）
```

## 8.1 金发女孩案例（Goldilocks，草案 6.1 ✅）

- 题面：对时间序列按设备聚合"不同读数"的边界统计，数据量大到单机表装不下、查询又要求跨记录合并——"太小的并行不够、太大的内存不够"的金发女孩式两难。作者用**同一道题连解四版**串起全章。⚠️ 数字细节从略（转述）。
- v0：朴素迭代方案——先全量排序一次再线性扫描，演示"全局排序是杀鸡牛刀"：只需要分区内有序时，全 shuffle 排序多付了跨区比较的钱。
- v1：groupByKey 直解——演示爆炸：shuffle 通过量＝原样搬运全部记录，reducer 端把整组物化成 List。
- v2/v3：二级排序变体——复合 key 让"同设备读数相邻"，一次 sort-shuffle 后在分区内流式扫描归并，内存占用从"整组"降到"一行"。
- v4：分区内归并不同值——利用"不同读数"本身可先在 map 端去重折叠的性质，把搬运量压到最小。⚠️
- 教学价值：一道题看尽"并行度 / 内存 / 排序 / 合并"的四角博弈；每换一版只动一个旋钮，代价与收益都可归因——这是后面各节所有机制的预演。
- 🔧 概念锚回 [06-Join优化](06-Join优化.md) 的 E5（SQLite 1.5M 行热键 30%）：单机拆热键反而 3.37s→3.50s 变慢——**加并行救不了单线程瓶颈**，这条负结果正是金发女孩"太大/太小"两难的镜像（**类比非 Spark**）。

## 8.2 groupByKey 为什么危险（草案 6.3 ✅）

- 机理：groupByKey＝把整张表按 key 原样搬运后在 reducer 内聚合成 List——**shuffle 通过量最大化＋目标端内存爆炸**双重罪。第一罪发生在跨网络搬运段（每行都过一遍磁盘+网络），第二罪发生在聚合落地段（最大 key 决定单 task 内存上限）。⚠️＋ https://spark.apache.org/docs/latest/rdd-programming-guide.html ✅（官方"用 reduceByKey 代替 groupByKey"的同源告诫）
- 症状三件套：shuffle write/read 字节≈输入规模、单 task spill 巨量、GC 时间占比飙升——在 UI 上一眼可辨（接 [02-Spark运行原理](02-Spark运行原理.md) 的观测面）。
- 替身谱系（"先折叠后搬运"是一切修复的母题）：
  - reduceByKey：map 端自动挂 combine，聚合语义最简；
  - aggregateByKey：带初始值与组合器，中间类型可不同于值类型——自定义折叠的万能位；
  - foldByKey：无初始值的折叠，对幺半元算子友好；
  - combineByKey：三函数裸接口（创建/进/出），其余三者的底座。
- 与 ../bigdata/03-Shuffle与宽依赖.md 的"map 端 combine"口径完全互证：MapReduce 时代的 combiner 思想在 Spark 里是内建默认，但**只有聚合类算子享受，groupByKey 明确不享受**——这是反模式的根。
- 深水区：聚合函数不可结合时（如"去重集合"其实可结合——并集；而"精确中位数"不可），预聚合失效，转入 8.4 的排序路线或近似算法。⚠️

## 8.3 键值上的行动与聚合选择（草案 6.2/6.4 ✅）

- PairRDD 操作族谱按"是否触发 shuffle、是否保留分区器"两轴分格：
  - 窄且保分区：mapValues、filter（对 key）、changed/partition 感知算子；
  - 窄不保分区：以 key 为变量的 map（分区函数依赖旧 key 分布，改 key 即毁序）；
  - 宽免 shuffle：两侧 co-partitioned 时的 join/cogroup（见 8.4）；
  - 宽必 shuffle：partitionBy、groupByKey、join（分区不匹配时）。⚠️
- 选聚合操作决策清单（草案 6.4 的判定树重排）：
  1. 有可结合交换的归约函数？→ reduceByKey/foldByKey（默认答案）；
  2. 归约需要初始状态或改变类型？→ aggregateByKey；
  3. 需要组内全部原始值？→ 先问"真的需要全部吗"，再考虑组内排序流式消费（8.5）而非 groupByKey 物化；
  4. 需要多算子共享同一分组？→ 一次 partitionBy＋多次窄操作，胜过多次宽聚合。
- 对象经济学：每行 `(K, V)` 在 JVM 里的装箱/引用成本——key 复用字典化、原始类型特化（草案年代技巧，今天多归序列化章）。⚠️＋ https://spark.apache.org/docs/latest/tuning.html ✅

## 8.4 多 RDD 操作与分区器（草案 6.5/6.6 ✅）

- 多个 RDD 同 key join/cogroup：两侧**分区函数相同＋分区数一致**则完全免 shuffle（co-partitioned 红利）；否则引擎按最贵的一侧重排。`partitionBy` 主动塑形上游，是"把一次 shuffle 的钱花在刀刃上"的标准动作：先 partitionBy 再多次 join 复用布局。⚠️＋rdd-programming-guide（PairRDDFunctions 条目）✅
- 分区器三型＋一自定义：
  - HashPartitioner：`key.## % n` 取模——均匀但怕热键，分区数一旦定死改不动；
  - RangePartitioner：对 key **采样**后按分位数切段——有序、可二分定位，代价是采样一次全量 key 的 shuffle＋段边界倾斜风险；二级排序与"按日期段分文件"的前提；
  - 自定义分区器：业务邻域感知（同客户进同区、同地域进同区），接口极简（getPartition/equals），责任极重（分区不均的锅全在实现者）；
  - "跨转换保留分区信息"清单＝哪些算子继承父分区器——这是免费 co-location 的账本，判读以官方文档为准 ⚠️＋rdd-programming-guide ✅。
- co-located vs co-partitioned 辨析：前者指数据恰好在同节点（局部性红利，可能随机命中），后者指**按构造**共享分区函数与分区数（join 免费的前提是后者）；把希望寄托在前者是事故来源。
- 🔧 概念锚：分区器≈分库分表的 hash/range 路由两派——E3（DuckDB 24 分区 parquet，全扫 0.01s vs 裁剪 0.00s）演示"路由对了查询就便宜"的同一物理：**类比非 Spark**。

## 8.5 二级排序与 repartitionAndSortWithinPartitions（草案 6.8 ✅）

- OrderedRDDFunctions 底座（草案 6.7 字典节）：key 有序 ⇒ 范围查询、按键 join、组内遍历三类操作获得"免全扫"红利；有序性不是装饰，是 RangePartitioner＋分区内排序的**合成产物**。⚠️
- 技术内核：把 `(k, v2)` 装进复合 key `(k, v2)`——`k` 上 hash/range 分区保证同组同区，`(k, v2)` 整体排序保证组内有序——repartitionAndSortWithinPartitions 一次 shuffle 同时完成"分组"与"组内有序"，之后分区内流式扫描即得 groupWithinPartitions 语义，替代 groupByKey 物化。
- 版本 2→4 的递进（金发女孩续解）：
  - v2：排序键＝(设备, 读数)——组内读数天然有序，边界统计免聚合；
  - v3：值域排序键——对"不同读数"先去重再排序，搬运量按唯一值收缩；
  - v4：分区内归并——多路有序流归并取代物化 List，内存 O(分区) 而非 O(最大组)。⚠️
  - 每一步都在"搬运量 vs 内存 vs 排序代价"三角里挪砝码，没有免费档。
- SQL 侧镜像：没有名为 sortWithinGroup 的旋钮，但 `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` / `COLLECT_LIST`＋排序承担同职——代价与红利在 AQE 下重新分配；窗口函数物化整组仍是 groupByKey 型风险。⚠️＋ https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅

## 8.6 掉队者与不均衡数据（草案 6.9 ✅）

- 症状识别：Stage 内 task 时长长尾（max/median≫1）；根因三查：
  1. 分区字节分布——单分区文件/记录数远超均值 ⇒ 并行度或分区器问题；
  2. 单分区计算形状——热键让"均匀字节"的分区做"不均匀工作" ⇒ key 形状问题；
  3. 节点层面资源噪声——同规格 task 在某些节点恒慢 ⇒ 硬件/邻居问题，推测执行对策。⚠️＋ https://spark.apache.org/docs/latest/configuration.html ✅（spark.speculation 参数族）
- 两种病两张处方：**并行不均衡**（分区数不足/粒度失当）加并行度、重分区治；**数据不均衡**（热键）改 key 形状（加盐打散-两段聚合、分离热点-单独广播）治；混用即无效甚至有害——E5 单机负结果（3.37s→3.50s）是"在不存在并行收益处拆并行"的实证对偶，分布式的真收益出现在**分区数足以摊开冷热之后**。🔧（类比非 Spark）
- 检测先行：每分区行数/字节直方图是本章所有结论的测量基座；不测量就调参＝掷骰子（接 [10-测试与验证](10-测试与验证.md) 计数器法）。

## 8.7 误区清单

| # | 误区 | 正解 | 机制出处 |
|---|------|------|----------|
| 1 | groupByKey 只是"慢一点" | 通过量与内存双重爆炸，最大 key 决定单 task 生死 | 8.2 |
| 2 | partitionBy 之后所有转换都保分区 | 改 key 的窄算子即毁分区信息，需查继承清单 | 8.4 |
| 3 | join 快是因为数据在同节点 | co-located 是运气，co-partitioned 才是构造 | 8.4 |
| 4 | 二级排序需要两次 shuffle | 复合 key＋一次 sort-shuffle 完成分组与有序 | 8.5 |
| 5 | RangePartitioner 采样全量数据 | 采样 key 即可；但采样本身仍是一次 shuffle 代价 | 8.4 |
| 6 | 长尾 task 一律开推测执行 | 先分诊：热键型长尾重复任务只会加倍拥塞 | 8.6 |
| 7 | 加分区数治倾斜 | 加并行治粒度不均，不改 key 形状热键依旧 | 8.6 |

## 8.8 小结自检

1. groupByKey 的"双重罪"分别发生在链路的哪一段？各自的量纲是什么？
2. RangePartitioner 采样的是什么、代价是什么、红利是什么？
3. 用一句话说清 co-partitioned 为何让 join 免 shuffle。
4. 二级排序的复合 key 里，分区看谁、排序看谁？
5. E5 的单机负结果对分布式拆热键给出了什么前提约束？

## 8.9 互链

- 上游机制图：[02-Spark运行原理](02-Spark运行原理.md)；同病灶章：[06-Join优化](06-Join优化.md)；算子经济学：[07-高效转换算子](07-高效转换算子.md)
- API 权威：../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md、../Spark_The_Definitive_Guide/04-聚合与复杂数据类型.md
- 中文叙事：../bigdata/03-Shuffle与宽依赖.md、../bigdata/02-Spark核心与RDD模型.md
- 配方侧对位：../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md（其协同过滤/图算法配方的性能前提即本章 co-partitioning 纪律）

## 核心概念速览（中英对照）

- **PairRDD** — 键值 RDD：分区/排序/合并三大机制全暴露的教学标本层。
- **Partitioner** — 分区器：key→分区的函数，co-location 的宪法。
- **Hash/Range Partitioner** — 哈希/范围分区器：均匀取模 vs 有序切段的两种世界观。
- **Custom Partitioner** — 自定义分区器：业务邻域感知的路由，接口小责任大。
- **co-partitioned** — 同分区：两 RDD 共享分区函数与分区数，join 免 shuffle 的门票。
- **map 端预聚合** — Map-side combine：先折叠后搬运，shuffle 通过量的第一减肥法。
- **reduceByKey** — 按键归约：带 combiner 的聚合，groupByKey 的默认替身。
- **aggregateByKey** — 按键聚合：自定义组合器的分区内折叠，中间类型可不同于值类型。
- **combineByKey** — 三函数聚合裸接口：创建/进/出，其余聚合算子的底座。
- **二级排序** — Secondary sort：复合 key 让"分组有序"一次 shuffle 完成。
- **repartitionAndSortWithinPartitions** — 重分区内排序：RangePartitioner＋组内有序的合体算子。
- **OrderedRDDFunctions** — 有序键值算子族：分区内有序解锁的范围查询与组内遍历。
- **straggler** — 掉队任务：Stage 长尾个体，并行不均/热键/节点噪声三源。
- **推测执行** — Speculative execution：以重复任务赌节点噪声的缓解开关。
- **数据倾斜** — Data skew：key 分布不均把并行程序退化为串行瓶颈的总病因。

## 最新演进与工业实践

- **PairRDD 的存量角色**：新代码几乎不再直接写（2.x→4.x 的迁移现实，参见 [03-Spark升级与迁移](03-Spark升级与迁移.md)），但 Spark 内部 Stage 形状仍是"分区器＋排序"模型——本章概念全部换皮存活于 SQL 执行计划：join 策略、窗口物化、写出分桶都是同一物理的抽象层投影。⚠️
- **AQE 时代的倾斜**：运行时热分区拆分（skew join 优化）接管"金发女孩 v4"的手工解，`sql-performance-tuning` 页为其权威口径 ✅；代价是"何时不该让 AQE 管"（多分区同时倾斜/统计采样失真）仍需本章的分布直觉。⚠️＋ https://spark.apache.org/docs/latest/sql-performance-tuning.html ✅
- **Buckets 的余温**：早期"按 key 分桶预分区"的表级 co-partitioning 手法在湖仓时代被格式侧隐藏分区/聚类（clustering）接棒——思想未死，旋钮换了面板（对位 ../Use_Iceberg_with_Spark/05-演化与隐藏分区.md）。⚠️
- **工业口径**：groupByKey 类反模式在现代 UI 里以"单 task shuffle write 巨大＋spill 阶梯"现身；面试高频（reduceByKey vs groupByKey、二级排序、分区器三型）持续在场，是理解 join 策略题的前置骨架。
- **文献锚**：MapReduce combine 思想远溯 OSDI 2004（本册不另引，经 ../../db/db.md 书目线可及）；Spark 内建排序 shuffle 见 rdd-programming-guide ✅。
