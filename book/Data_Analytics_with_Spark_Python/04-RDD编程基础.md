# 04 RDD 编程基础（对应原书 Ch4，印张页 59–108）

> 所属书目：[00-总览与阅读地图](00-总览与阅读地图.md) ｜ 《Data Analytics with Spark Using Python》1e，Jeffrey Aven 著，Addison-Wesley Professional，2018。
> 本章二级目录 ✅ 实抓自官方 informIT 产品页（原书章内小节极细，全量照录）；正文为**精读重构**，非原书文本。
> 章内代码风格为 Spark 2.x RDD API 示意 ⚠️ 未实测（本机 pyspark 不可装，沿用波6 实测结论）。

## 官方二级目录（✅ 实抓）

- Introduction to RDDs (p.59)
- Loading Data into RDDs (p.61)
  - Creating an RDD from a File or Files (p.61) ／ Methods for Creating RDDs from a Text File or Files (p.63)
  - Creating an RDD from an Object File (p.66) ／ Creating an RDD from a Data Source (p.66)
  - Creating RDDs from JSON Files (p.69) ／ Creating an RDD Programmatically (p.71)
- Operations on RDDs (p.72) ／ Key RDD Concepts (p.72)
- Basic RDD Transformations (p.77) ／ Basic RDD Actions (p.81)
- Transformations on PairRDDs (p.85)
- MapReduce and Word Count Exercise (p.92)
- Join Transformations (p.95) ／ Joining Datasets in Spark (p.100)
- Transformations on Sets (p.103) ／ Transformations on Numeric RDDs (p.105)
- Summary (p.108)

## 精读重构·装载 RDD 的五条路（p.61–71）

TOC 给出的构造面清单，对应 Python API 的入口（语义按公开文档 ⚠️ 转述）：

1. **textFile 族**：`sc.textFile(path, minPartitions)` 单文件/目录/glob；
   多行压缩文本走 HadoopInputFormat 路线（书中 p.63 的 "Methods for Creating RDDs from a Text File(s)" 即此分叉）。
2. **Object File**：`hadoopFile`/sequence-file 类二进制键值对象文件（p.66），Hadoop 生态互导的前门。
3. **Data Source**：JDBC 等经 HadoopInputFormat/Spark SQL 前身读取（p.66–69）。
4. **JSON Files**：逐行 JSON → RDD[dict]，手工 `json.loads` 映射（p.69；DataFrame 路线留到 Ch6）。
5. **Programmatically**：`parallelize(collection, n)` 与 `makeRDD`——教学与小数据入口（p.71）。

## 精读重构·转换与行动的分野（p.72–85）

Key RDD Concepts（p.72–77）承担全书最重要的一次概念定桩（⚠️ 推定展开）：

- **惰性**：transformation 只记账（构图），action 才执行。
- **不可变+血缘**：每次转换产生新 RDD；窄依赖同分区流转、宽依赖跨分区重排（→ Ch5 分区议题）。
- **确定性**：同输入同转换可重放，容错由此免费获得。

转换清单（p.77 起，按 TOC 分类）：`map`/`flatMap`/`filter`/`mapPartitions`/`mapPartitionsWithIndex`、
`distinct`、`union`、`intersection`、`subtract`（集合三件套对应 p.103 "Transformations on Sets"）、
`sample`（p.105 数值 RDD 亦铺垫）、`sortBy`/`groupBy`；行动清单（p.81 起）：
`collect`/`count`/`countByKey`/`reduce`/`fold`/`aggregate`/`take`/`first`/`top`/`foreach`/`saveAsTextFile`。

PairRDD 专题（p.85–92）：`reduceByKey` vs `groupByKey`（先局部聚合再洗牌）、
`combineByKey` 的通用聚合骨架、`keys/values`、`sortByKey`、`countByKey`——
Python API 中键值对以 `(k, v)` 元组 RDD 表达，无独立类型（语义按公开文档 ⚠️ 转述）。

## 精读重构·WordCount 练习与 Join（p.92–100）

书中标志性的 MapReduce-WordCount 练习（p.92）骨架：

```python
rdd = sc.textFile("logs/*.txt")
counts = (rdd.flatMap(lambda line: line.split())
              .map(lambda w: (w, 1))
              .reduceByKey(lambda a, b: a + b))
counts.saveAsTextFile("out/wc")
```

Join 谱系（p.95–100，⚠️ 推定展开）：`join`/`leftOuterJoin`/`fullOuterJoin` 基于键的 shuffle 合并；
p.100 "Joining Datasets in Spark" 讨论广播小表的替代路径（map-side join 思想，Python 里常手搓
`sc.broadcast(dict)`——Ch5 broadcast 变量在 p.112 才正式展开，书在此埋线）。

🔧 **本地对照实测 E1（非本书 Spark 引擎行为）**：20 万行模拟事件表上，
逐条 Python 循环 map+dict 归并（reduceByKey 语义的单机版）耗时 **0.153 s**、得 485 键；
pandas 向量化 `groupby` 聚合耗时 **0.0196 s**——同语义两种执行范式相差约 **7.8 倍**。
教学结论：`reduceByKey` 的「局部预聚合」之所以关键，是因为逐元素函数路径在任何引擎上都是最贵档；
数据与脚本：`D:\develops\tmp\dbwave_w8_daspark\analogies.py`（E1 组）。

## 常见误区与读法提示

1. `collect()` 是教学便利品、生产毒药（驱动端 OOM 主因），书中 p.152 的收集成本在 Ch5 回马枪。
2. `groupByKey` 默认姿势问题：2018 年书已提醒改 `reduceByKey`；2026 年更应直接 DataFrame——
   但本章把 RDD 语义讲透，恰好是理解 DataFrame shuffle 的脚手架。
3. 本章页码跨度 50 页（59–108），是全书密度最高章；建议拆三次读：装载/转换/Join。

> repo 对照：现行文档版同主题（含 3.x 语义纠偏）见
> [../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md)；
> 中文类比见 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)；
> shuffle 与宽依赖的机制纵深见 [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md)。

## 复习要点与自测清单

1. 装载五路（text 族/object file/数据源/JSON/parallelize）各举一个生产场景与一个坑（如小文件、glob 语法）。
2. 转换/行动分类默写：给定 10 个算子，2 分钟内正确归档，并标出其中哪些产生 shuffle。
3. 用一句话说清惰性：为什么连续 5 个 map 不花时间，`count()` 才花时间？
4. `reduceByKey` 与 `groupByKey` 的执行计划差异图；何时二者不可互换（需全量值列表时）。
5. PairRDD 三板斧：`combineByKey` 的三个函数参数各自职责，能现场手写均值聚合。
6. Join 谱系：inner/leftOuter/fullOuter 的键丢失规则；广播连接免 shuffle 的条件（小表阈值与内存）。
7. WordCount 变体：改造成「按用户统计金额总和+计数」双聚合——恰好是 🔧 E1 实验的 Spark 化写法。
8. 自检题：`collect()` 在生产禁用、`take(10)` 相对安全的原因？（驱动端物化 vs 有界取样，Ch5 p.152 回收）

## 核心概念速览（中英对照）

- **textFile** — textFile：按路径（支持 glob/目录）产 RDD 的最常用装载入口，`minPartitions` 定并行下限。
- **parallelize** — parallelize：把驱动端集合切片分发成 RDD 的程序化构造。
- **窄依赖** — Narrow Dependency：子 RDD 每个分区只依赖父固定少数分区，可流水线执行免洗牌。
- **宽依赖** — Wide Dependency/Shuffle Dependency：按键重排跨分区，产生 stage 边界。
- **flatMap** — flatMap：一进多出的展平映射，词切分类任务标配。
- **mapPartitions** — mapPartitions：以整个分区为单元的映射，摊销逐条函数调用开销。
- **reduceByKey** — reduceByKey：同键先局部聚合再跨节点合并，优于 groupByKey 的默认原因。
- **combineByKey** — combineByKey：PairRDD 自定义聚合三板斧（创建/区内合并/区间合并）。
- **行动** — Action：触发 DAG 求值的终结操作，collect/count/save 各代表一种结果去向。
- **内连接/外连接** — join/leftOuterJoin/fullOuterJoin：基于键 shuffle 的双 RDD 合并算子族。
- **广播连接** — Broadcast Join：小表随闭包分发、大表免洗牌的连接替代路径。
- **collect 成本** — Collect Cost：把分布式结果物化回驱动端的内存与网络风险，教学 API 的生产禁忌。

## 最新演进与工业实践

- **RDD API 的稳定与冻结**：官方 RDD 指南仍完整在线（https://spark.apache.org/docs/latest/rdd-programming-guide.html ，✅ curl -sI 200），
  但 2024–2026 新功能基本不再向 RDD 面加车；本章是「语义地基」而非「日用 API」⚠️ 转述定位。
- **DataFrame 吸收教学位**：本章词汇在现行教材中由结构化 API 重讲——对照
  [../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md](../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md)。
- **pandas API on Spark**：`ps.DataFrame.groupby` 等把本章语义直接映射到 pandas 用户习惯，
  官方参考 https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/index.html （✅ curl -sI 200）。
- **单机等价工具更强**：🔧 E1 实测（pandas 3.0.2/Python 3.13.2）显示向量化引擎对逐元素路径的优势扩大；
  DuckDB 1.5.5（🔧 本机可用）的 group by 更是聚合型「action」的单机最优实现——概念学习可全程离线完成（非本书 Spark 引擎行为）。
- **教学遗产确认**：WordCount 作为入门练习的地位未动；本目录用 E1 数据把它量化，2026 年带新人建议「先 pandas 语义、后 RDD 类比」的倒序讲法。
