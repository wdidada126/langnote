# 01 大数据、Hadoop 与 Spark 导论（对应原书 Ch1，印张页 5–25）

> 所属书目：[00-总览与阅读地图](00-总览与阅读地图.md) ｜ 《Data Analytics with Spark Using Python》1e，Jeffrey Aven 著，Addison-Wesley Professional，2018。
> 本章二级目录 ✅ 实抓自官方 informIT 产品页；正文为**精读重构**（基于官方 TOC + Spark/Hadoop 公开文档），非原书文本，⚠️ 具体论述措辞不逐句对应。

## 本章在书中的位置

Ch1 是全书「Spark 基座篇」(Part I: Spark Foundations, Ch1–Ch4) 的开局章。作者的写法是典型的
「先史后技」：从大数据与分布式计算的动机讲起，经 Hadoop 生态过渡到 Spark，最后落在
**Python 函数式编程**这一本书贯穿的 API 视角上（书名中的 Using Python 由此得名）。

## 官方二级目录（✅ 实抓）

- Introduction to Big Data, Distributed Computing, and Hadoop (p.5)
- A Brief History of Big Data and Hadoop (p.6)
- Hadoop Explained (p.7)
- Introduction to Apache Spark (p.13)
- Apache Spark Background (p.13) ／ Uses for Spark (p.14)
- Programming Interfaces to Spark (p.14)
- Submission Types for Spark Programs (p.14)
- Input/Output Types for Spark Applications (p.16)
- The Spark RDD (p.16) ／ Spark and Hadoop (p.16)
- Functional Programming Using Python (p.17)
- Data Structures Used in Functional Python Programming (p.17)
- Python Object Serialization (p.20)
- Python Functional Programming Basics (p.23)
- Summary (p.25)

## 精读重构·主线一：Hadoop 叙事（p.5–13）

重构作者脉络（⚠️ 依据公开通识，非原书逐句）：

1. 大数据动机：单机磁盘/内存/CPU 的线性扩展天花板，GFS/MapReduce 论文谱系。
2. Hadoop 栈：HDFS（主从 NameNode/DataNode、块复制）、MapReduce（批式两阶段、
   中间结果落盘）、以及围绕它们的 ecosystem（Hive/Pig/HBase/ZooKeeper，书中点到为止 ⚠️ 推定）。
3. 史前史侧写：Nutch → Hadoop 0.x → YARN 分家（Hadoop 2），为 Ch2 的「Spark on YARN」埋点。

> repo 对照：这段叙事的浓缩版见 [../bigdata/01-大数据技术全景.md](../bigdata/01-大数据技术全景.md)，
> 其「计算引擎的演进」视角在 [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。

## 精读重构·主线二：Spark 与 RDD 亮相（p.13–17）

官方 TOC 给出的关键概念清单（这些是本章的「术语锚点」）：

- **Programming Interfaces**：TOC 列出的接口面即 Spark 对 Python 暴露的 API 层次——
  RDD 核心 API 与（后文 Ch6 登场的）DataFrame/Spark SQL 双轨。2018 年书写时 RDD 仍是教学主轴。
- **Submission Types**：spark-submit / shell / 编程内嵌 SparkContext 三类提交形态 ⚠️ 推定展开。
- **Input/Output Types**：HDFS、本地文件系统、对象存储（S3，呼应 Ch2 云部署）、
  键值存储（HBase/Cassandra，呼应 Ch6）等 Hadoop 兼容 I/O 面。
- **The Spark RDD**：弹性分布式数据集——不可变、分区、可并行操作的记录集合；
  靠 lineage（血缘）重建分区容错。这是 Ch4/Ch5 全部深化的种子概念。

示意代码（Spark 2.x 时代风格 ⚠️ 未实测，本机 pyspark 不可装，沿用波6 实测结论）：

```python
# 仅作概念示意：RDD 的最小心智模型
sc = SparkContext("local[*]", "ch1-demo")      # 本地全核
rdd = sc.parallelize(["data", "spark", "data"], 2)  # 2 个分区
counts = rdd.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
print(counts.collect())
```

> repo 对照：RDD 心智模型的更新版（Spark 3.x 视角）在
> [../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md)
> 与 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)。

## 精读重构·主线三：Python 函数式编程铺垫（p.17–25）

TOC 的三小节（数据结构 / 对象序列化 / 函数式基础）指向一组明确的预备知识：

| 书中锚点 | 内容重构（⚠️ 推定展开） | 对后续章的意义 |
|---|---|---|
| Data Structures | list/tuple/dict/set 与生成器；函数优先的一等公民对象 | Ch4 RDD 闭包传参 |
| Python Object Serialization | pickle 协议、__getstate__/__setstate__；自定义序列化器注册 | Spark 任务闭包与 shuffle 数据跨节点传输（Python worker 走 pickle） |
| Functional Basics | map/filter/reduce、lambda、高阶函数、惰性（生成器） | RDD 转换即函数式范式的集群化 |

🔧 **本地对照实测（pandas，非本书 Spark 引擎行为）**：
用 20 万行模拟事件表（user_id 2 万键含热点倾斜、category 5 类、amount 对数正态）。
手写 Python 循环 map+dict 合并（模拟 reduceByKey 语义）耗时 **0.153 s**，得到 485 个组合键；
同一数据用 pandas `groupby("category").agg(count/sum/mean)` 向量化路径耗时 **0.0196 s**，
约 **7.8 倍**差距。结论（类比面）：函数式逐元素路径在单机即不敌批式向量化——
Spark 的 map/reduce 语义同理，这正是 Ch5「优化」议题的动机；数据脚本见
`D:\develops\tmp\dbwave_w8_daspark\analogies.py`（E1 组，另有结果 results.json）。

## 常见误区与读法提示

1. 把「Spark 取代 Hadoop」当本章结论——错，TOC 明确保留「Spark and Hadoop (p.16)」共存节；
   Spark 替换的是 MapReduce 计算层，HDFS/生态存储层仍在。
2. 忽略 Python 序列化铺垫：Ch5 闭包/共享变量的坑（大对象随闭包广播）在这里已有伏笔。
3. 2018 年书的「Uses for Spark」以批处理/交互/ML 三分法讲述；2026 年视角需叠加
   结构化流与 pandas API 的新三分（见文末演进节）。

## 核心概念速览（中英对照）

- **弹性分布式数据集** — Resilient Distributed Dataset (RDD)：不可变、分区、凭 lineage 容错的分布式记录集合。
- **血缘** — Lineage：RDD 间转换关系链，故障时按链重建丢失分区而非副本复制。
- **Hadoop 分布式文件系统** — HDFS：分块(默认128MB)+多副本+主单元管理的批式吞吐优先存储。
- **映射与归约** — MapReduce：中间结果落盘的两阶段批处理模型，Spark 所要改良的对象。
- **资源协调层** — YARN：Hadoop 2 起的通用资源调度层，Spark 的部署目标之一（Ch2/Ch3 展开）。
- **转换** — Transformation：RDD 上惰性求值的重生成操作（map/filter/reduceByKey）。
- **行动** — Action：触发计算图执行并返回/写出结果的操作（collect/count/save）。
- **分区** — Partition：RDD 的并行粒度单元，键分布决定局部性（Ch5 分区控制前导）。
- **一等函数** — First-class Function：Python 中函数可赋值/传参/返回，Spark 闭包 API 的语言基础。
- **对象序列化** — Pickling/Serialization：Python 对象转字节流跨进程/节点传输，闭包与大变量的成本来源。
- **高阶函数** — Higher-order Function：map/filter/reduce 等接受函数为参的操作，函数式编程核心词汇。
- **生成器** — Generator：惰性求值的 Python 序列构造，单机「按需计算」的 RDD 类比物。

## 最新演进与工业实践

- **RDD 的当前地位**：官方 RDD 编程指南仍在线维护（https://spark.apache.org/docs/latest/rdd-programming-guide.html ，✅ 本次 curl -sI 200），但定位已是「底层 API」；
  2018 年书以 RDD 为主轴的教法在 2024–2026 工业实践里应倒序为「DataFrame/SQL 优先，RDD 兜底」⚠️ 转述。
- **Python 侧演进**：Spark 3.2 起内置 pandas API on Spark（Koalas 收编），
  官方 API 文档 https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/index.html （✅ curl -sI 200）——
  Ch1 铺垫的 pandas 式思维如今有官方直通通道，本书写作时该通道尚不存在。
- **SparkR 退役方向**：本书 Ch8 专章讲 Spark+R；4.x 系列 R on Spark 已被移除/边缘化 ⚠️ 转述（本地无法装 Spark 实证，沿用波6 不可实测结论）。
- **Hadoop 叙事瘦身**：2026 年新读者可将本章 Hadoop 史当作背景档案：湖仓与对象存储(Iceberg/S3 类)已是主流存储叙事，
  repo 内对应更新视角见 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。
- **奠基论文**（题录+⚠️ 未过 DOI 校验，故不给 DOI）：
  "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory MapReduce"，NSDI 2012；
  "Spark SQL: Relational Data Processing in Spark"，SIGMOD 2016。⚠️ 二者 DOI 本次未校验，仅存题录。
- **单机向量化基线更新**：🔧 本机构环境 pandas 3.0.2/Python 3.13.2 下向量化聚合对函数式循环的优势（E1 实测约 8 倍）
  在 numpy/pandas 新版本上持续扩大；pandas 3.x 的 Copy-on-Write 语义使「序列化传递」概念上更省（https://pandas.pydata.org/docs/ ，✅ 200）。
