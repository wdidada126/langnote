# 01 Spark 2.x 时代的集群与 RDD 编程模型

> **取证态**：本单元对应 Learning Path 主题「Get to grips with all the features of Apache Spark 2.x」与仓库 Module_1/Chapter 3、Chapter 5（`scalascript.scala` 线索）✅ 目录级实抓；逐章章名不可得 ⚠️（见 00 §3）。Spark 引擎行为本机不可实测 → 全部 ⚠️ 转述 + 官方文档锚；🔧 实验仅为概念类比、**非本书 Spark 引擎行为**。对位总锚：[../Spark_The_Definitive_Guide/00-总览与阅读地图.md](../Spark_The_Definitive_Guide/00-总览与阅读地图.md)；同题正读：[../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md)。

## 1. 2.0 的分水岭意义：一个入口统治全部

Spark 1.x 时代的应用入口是碎片化的：`SparkContext` 管 RDD、`SQLContext` 管 SQL、`HiveContext` 管 Hive 元数据，Streaming 另起 `StreamingContext`。**Spark 2.0 把三者合体为 `SparkSession`**——这是本册「Spark 2」标题的实质所指 ⚠️（转述自官方 2.x 文档口径）：

```scala
// Spark 2.x 标准开场（Scala，时代写法）
val spark = SparkSession.builder()
  .appName("spark2-learning-path")
  .master("yarn")                      // 2.x 教学环境常见 yarn/local[*]
  .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
  .getOrCreate()
val sc = spark.sparkContext            // RDD 底座仍可取回
```

```r
# SparkR 时代尾声的教学面貌（本书 README 环境清单仍要求 R 3.1+）
library(SparkR, lib.loc = file.path(Sys.getenv("SPARK_HOME"), "R", "lib"))
sparkR.session(master = "local[*]",
               sparkConfig = list(spark.sql.warehouse.dir = "/tmp/warehouse"))
df <- as.DataFrame(iris)
head(df)
```

SparkR 与 `sparklyr`（R 的 dplyr 后端翻译到 Spark SQL）在 2019 年处于「教程供给峰值、社区热度拐点」——本书环境清单里的 `R 3.1+/Rstudio`、`Python 2.7+/3.4`、`Scala 2.11`、Hortonworks HDP 沙箱，是 2.x 教学生态的**时代化石**（其后的 Python 2.7 EOL 与 HDP 并入 Cloudera 属 2020–2021 事件 ⚠️ 转述）。

## 2. RDD：弹性分布式数据集的执行语义

- **定义**：带分区信息的不可变对象集合，算子惰性求值，动作为触发点 ⚠️（官方 [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)，✅ URL 可达，2026-10 仍在 4.x 文档树内）。
- **DAG 调度**：转换算子串成 DAG；调度器按**窄依赖**（一对一/桶化，如 `map`/`filter`/`union`）连成 pipeline 在单 stage 内流水执行；遇**宽依赖**（按 key 重分布，如 `groupBy`/`join`）切 stage、触发 shuffle 落盘 ⚠️。
- **容错**：谱系（lineage）重算——失败分区沿转换链回放而非整体回滚；`persist()` 切断谱系换读写权衡 ⚠️。
- **存储级别**：`MEMORY_ONLY` / `MEMORY_AND_DISK_SER` / `DISK_ONLY` 等序列化合约，2.x 教学标配 ⚠️。

### 🔧 E3 类比：分区局部聚合 + shuffle 的两阶段语义（DuckDB 1.5.5）

```sql
WITH partial AS (SELECT part, SUM(v) sp, COUNT(*) cp FROM t GROUP BY part),  -- map 端局部聚合（combiner 类比）
     final  AS (SELECT part, SUM(sp)/SUM(cp) avg_v FROM partial GROUP BY part) -- reduce 端合并（shuffle 后）
SELECT * FROM final ORDER BY part;
```

4000 行、4 分区模拟：两阶段结果 `[47.931, 47.949, 48.027, 47.874]` 与 SQLite 直接全局 `AVG(v) GROUP BY part` **逐分区完全一致**——演示「均值不能由均值再平均、必须由 (sum,count) 半群对传递」这一 shuffle 聚合的代数前提。**非本书 Spark 引擎行为**（无分布式/无真正落盘）。

### 🔧 E5 类比：谱系重算 vs 持久化（SQLite 3.45.3）

20000 行基表派生 `SUM/COUNT` 聚合表：重放转换链重建 **10.6ms**；改读预先落盘的持久化表 **0.08ms**——两个数量级的读写权衡正是 `persist()` 的动机；小数据下重算廉价（谱系红利），数据/链条一大即反转。**类比 RDD lineage，非 Spark 实测**。

## 3. 共享变量与分区级编程

- **广播变量** `spark.sparkContext.broadcast()`：只读大表随任务分发前物化一次，替代逐任务发送（broadcast join 的底层原语）⚠️。
- **累加器**：仅任务侧写、driver 侧读的单向聚合器；2.x 已有 `AccumulatorV2` 取代 v1（v1 后续版本退役 ⚠️）。
- **`mapPartitions`/`foreachPartition`**：以分区为粒度持连接（JDBC/Kafka 客户端复用），是 2.x 手册反复强调的资源模式 ⚠️。

## 4. 集群管理与部署形态（2.x 语境）

README 环境清单的 `local[*]`/standalone/YARN 三形态 + Hortonworks 沙箱是 2.x 教学主流 ⚠️；Mesos 支持同期仍在但已进入末期（社区风向转向 YARN 与新兴容器编排 ⚠️ 转述）。动态资源分配 `spark.dynamicAllocation.enabled` 需 shuffle 服务外置 ⚠️——细节以官方 [tuning 文档](https://spark.apache.org/docs/latest/tuning.html)（✅ URL 可达）为准，本册不可实测面不展开数值。

## 5. 与其他书目的分工

- RDD→DataFrame 的「让位」叙事与 3.x/4.x 头名对位见 [../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md)；
- 结构化 API 概览的正读在 [../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md](../Spark_The_Definitive_Guide/03-结构化API概览与基本操作.md)；
- 盘上中文单文件 `../Spark大数据分析与实战.md`（登记，见 00 §5）。

## 4.5 应用生命周期与 checkpoint：2.x 教义补全

- **提交链** ⚠️：`spark-submit --class X --master yarn --deploy-mode cluster app.jar` → driver 起 `SparkContext` → 向 ResourceManager 注册 Application → executor 分配并接任务 → 心跳汇报。driver/executor/task 三件套是本章一切调优语言的空间坐标（06 的容量公式在此取数）。
- **失败重试两层级** ⚠️：task 失败沿谱系重试（有限次）；executor 丢失或 shuffle 文件损毁触发**祖先 stage 重放**——🔧 E5 的「重算廉价」在这里第一次显出账单形状：链条越长、重放越贵。
- **`checkpoint()` vs `persist()`** ⚠️：checkpoint 写物化到 HDFS 并**截断 lineage**（长作业防 driver 元数据膨胀），persist 留在故障域内；2.x 教参的「谱系超过约四十级即 checkpoint」为经验值（⚠️ 转述，不列精确版本参数名以免臆写）。

```scala
val feed = source.map(parse).filter(nonNull).flatMap(emit)  // 长转换链
feed.checkpoint()          // 截断谱系 + 可靠存储（HDFS 语义）
val cached = feed.persist(StorageLevel.MEMORY_AND_DISK_SER)  // 作业内复用
```

- **反噬面**：截断即放弃 §2/E5 的重算路径——checkpoint 后故障要**从 checkpoint 点全量重放**；checkpoint 间隔过密则 HDFS 往返吃光收益。这一对张力正是 Spark「存储-计算互换」世界观的起点，06 章的内存模型调优是它的现代续篇。
- **排障动线（2.x 教参顺序）**：UI stage 页看 task 时长分布（倾斜）→ driver/executor stderr 看 GC → 日志找 fetch failed（重放风暴）→ 再动内存参数——先观测后调参，06 §2 的监控栈为其基础设施。

## 4.6 时代差问答与自测（本章四问）

- **问：为什么书名把「Spark 2」当卖点？** 答：2.0 把 SparkContext/SQLContext/HiveContext/StreamingContext 的多门面统一进 SparkSession，并把 DataFrame 扶正为默认 API——入口与世界观的双重换代（§1）。
- **问：RDD 过时了吗？** 答：在本册它仍是底座与排障词汇表；在 4.x 它是「底层逃生通道」——先 DataFrame，精细控制面才下 RDD（§2+演进表）。
- **问：R 代码还要不要学？** 答：本册的 SparkR/sparklyr 内容按「SparkR 时代尾声」史料读；4.x 官方仍保留 R API 之名（演进表逐语），但学习预算应让给 PySpark。
- **问：🔧 数字能当性能结论用吗？** 答：不能。E3/E5 是单机语义类比，标了「非本书 Spark 引擎行为」；任何集群数字都不要从它们外推（00 §7 硬纪律）。

自测四题（答案均在本章正文）：① 用 `map/groupBy/join` 各画一条依赖边，标出哪里切 stage；② 广播变量替代了什么传输模式、省在哪；③ `checkpoint()` 截断谱系后，故障重放从哪里起步、代价形态如何变化；④ E3 两阶段结果为什么必然与全局 GROUP BY 一致（半群条件）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
|---|---|---|
| 会话入口 | SparkSession | 2.0 起统一 SparkContext/SQLContext/HiveContext 的唯一应用入口 |
| 弹性分布式数据集 | RDD (Resilient Distributed Dataset) | 分区不可变对象集合，惰性转换+动作触发+谱系容错 |
| 有向无环图 | DAG (Directed Acyclic Graph) | 转换算子连成的执行蓝图，按依赖切 stage |
| 窄依赖 | Narrow Dependency | 父分区至多被子分区使用一次的依赖，可流水免 shuffle |
| 宽依赖 | Wide Dependency | 按 key 重分布的依赖，切 stage 并触发 shuffle |
| 混洗 | Shuffle | stage 间的按键重分布与落盘交换 |
| 谱系重算 | Lineage Recomputation | 丢失分区沿转换链回放重建的容错机制 |
| 持久化 | Persistence / Cache | `persist()` 物化 RDD 切断重算链的读写权衡 |
| 广播变量 | Broadcast Variable | 只读大对象一次分发多任务复用的共享通道 |
| 累加器 | Accumulator | 任务侧单向写、driver 侧读的聚合变量（V2 代际） |
| 分区算子 | mapPartitions | 以分区为粒度执行、支持连接复用的编程模式 |
| 资源协商 | Dynamic Allocation | 按负载增减 executor 的动态资源模式，需外部 shuffle 服务 |

## 最新演进与工业实践

**2.x 知识点逐条对位 2026 Spark 4.x**（官方源，✅=URL 本次 `curl` 可达；行内引用均为可达页面文本或 ⚠️ 转述）：

| 本书（Spark 2.x） | 2026 现状（Spark 4.x 线） | 依据 |
|---|---|---|
| SparkSession 统一入口（2.0 新） | 仍是唯一入口；且客户端-服务器化：Spark Connect（3.4 引入、4.x 主推）让会话可远程挂载 | ✅ [4.0.1 文档首页](https://spark.apache.org/docs/4.0.1/) 逐语 `Spark Connect is a new client-server architecture introduced in Spark 3.4` |
| Scala 2.11 编译 | 2.11/2.12 退役，2.13 为 4.x 主线代际 | ⚠️ 转述，具体矩阵未在可达页逐字核对 |
| Python 2.7/3.4 教学 | 仅现代 Python 3.x；PySpark 文档树独立成线 | ✅ [api/python](https://spark.apache.org/docs/latest/api/python/) |
| SparkR/R 教程热度峰值 | R API 官方仍未废弃——4.0.1 首页逐语 `high-level APIs in Java, Scala, Python and R`；但社区教学重心已移向 PySpark | ✅ [sparkr.html](https://spark.apache.org/docs/latest/sparkr.html) 200 |
| RDD 作为日常编程层 | 降为「底层逃生通道」：新代码先 DataFrame/SQL，RDD 仅精细控制面使用 | ✅ [rdd-programming-guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html) 仍存 + [../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md) 对位口径 |
| YARN/standalone/Mesos | Mesos 线落幕、容器编排成为一线形态 | ⚠️ 具体页本次不可达，不列 URL |
| 版本坐标 | 4.2.0（2026-07-14）/4.1.3/4.0.4 与 LTS 线 3.5.9 并行发版 | ✅ [releases.html](https://spark.apache.org/releases.html) GET 实抓逐字 |

**工业实践判语**：2.x 合订册的环境清单（HDP 沙箱、Python 2.7、R 3.1）在今天任何生产/教学场景都应视为**反模式化石**；本册价值在于它保留了「DataFrame 统一前夜」的概念地层学——理解 stage/shuffle/lineage 的手感仍是有用的面试与调优底层语言（互见 [../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)）。
