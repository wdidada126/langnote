# 05 GraphX 图计算与深度学习生态模块

> **取证态**：对应 Learning Path 主题「Analyze structured and unstructured data using SparkSQL and GraphX」「ML and DL techniques ... using MLlib and various external tools」与仓库实据：Module_3/Chapter 13、15（`Code + Data`）、根数据 `enwiki_dump.xml`（维基转储——链接图的经典原料）✅ 目录级；章名 ⚠️ 不可得（00 §3）。GraphX/DL 行为不可本机实测 → ⚠️ 转述 + 官方 [GraphX Guide](https://spark.apache.org/docs/latest/graphx-programming-guide.html)（✅ 可达）锚；🔧 类比复用 E5（谱系重算）**非本书 Spark 引擎行为**。

## 1. GraphX 的数据模型：属性图叠在 RDD 上

GraphX 把图视为 `Graph[VertexProperty, EdgeProperty]` = 两个并行 RDD（顶点表/边表）+ 索引视图；**triplet（三元组）** 视角让顶点计算同时看见「源边/目标边」⚠️：

```scala
val graph = Graph(verticesRDD, edgesRDD, defaultVertex)
// 页式迭代（Pregel 变体）：沿超步传消息
val pr = graph.pageRank(0.001).vertices
// 连通分量：无向可达性的批式收敛
val cc = graph.connectedComponents().vertices
// 从原始文本建图（enwiki_dump.xml 的典型第一步）
import scala.io.Source
val links = Source.fromFile("enwiki_dump.xml")     // 单机教学口径，真实规模走 spark.read.text
  .getLines.filter(_.contains("<a href=")).map(extractTitle(_)).toSeq  // 示意
val g2 = Graph.fromEdgeTuples(sc.parallelize(links).map(e => (h(e._1), h(e._2))), 0L)
```

- **定向视图**：`outerVertices/innerVertices` + `EdgeDirection.In/Out`；双向图常以重复边策略表达 ⚠️。
- **持久顶点存储**（GraphX 2.x 教程常提的 external storage 设想）从未成为主干 ⚠️——这是「图当数据集」与「图当数据库」的分界伏笔。
- **图算法≠图库**：GraphX 提供收敛式批算法（PageRank/CC/三角计数/LBP），不提供毫秒级图查询；现代图查询正读见 [../Graph_Databases_2e/](../Graph_Databases_2e/)（目录实名登记）与 [../Neo4j_Graph_Data_Modelling/](../Neo4j_Graph_Data_Modelling/)。

## 2. 为什么维基转储是「GraphX 之友」（仓库数据实证）

`enwiki_dump.xml` 在仓库根 ✅ 实抓——维基链接图是度分布重尾、连通核心显著的天然实验场：入链度≈权威性的结构代理指标，正是 PageRank 教学的零成本语料。🔧 类比（非 Spark）：SQLite 上重建「页面-链接」二部表跑 `connectedComponents` 的 SQL 闭包近似，可见批式收敛 = 反复 join + GROUP BY 的最小模型；其代价曲线与 §01 E5「谱系重算廉价、迭代深则贵」直接对应——迭代图算法因此几乎必然要求 `persist()` 中间结果 ⚠️。

## 3. 深度学习：2.x 本体的缺位与外接生态的补位（时代真相）

MLlib 的 MLP（见 04 §3）之外，2.x 时代在 Spark 上做 DL 的全部现实路径是**「Spark 管数据、专用引擎管训练」** ⚠️（README 原文 `various external tools` 即此意）。Learning Path 单品书中出现过的对接形态按年代口径登记（具体版本映射 ⚠️ 不可达源坐实，只列名目不编细节）：

| 外接件（2.x 年代） | 分工模式 | 2026 存废判语 |
|---|---|---|
| H2O-sparkling-water | R/Python 三件套桥接（gbm/deepLearning 跑在 H2O 分布式后端） | 产品线其后终止 ⚠️ 转述 |
| AI Summit 系框架（Cntk/BigDL/TensorFlow-RDD 桥） | 参数服务器或 RDD 喂图 | 多数退役或让位；BigDL 转 ORC 线 ⚠️ 转述 |
| Keras 批量推理挂载 | Spark 只做数据并行外壳 | 被 pandas UDF/批量推理原语正规化（02 §5 UDF 教训的 ML 版） |
| PySpark + 单机 DL 库 | 分区内各自训练、不追求全局收敛 | 仍是中小规模主流姿势 ⚠️ |

判语：本册若给「Spark 做深度学习」留下幻觉，04/05 两章的 ANN 与外接清单恰好是它的解毒剂——**分布式数据管道 + 单机/专用训练器** 才是 2.x 的可辩护现实。

## 4. 非结构化数据的谱系位置（SQL⇄图⇄文本）

README 承诺的 `structured and unstructured data` 三角在 2.x 的落地=SQL(DataFrame) 通吃文本/JSON/二进制的「表化」+ GraphX 的「图化」+ MLlib 的「特征化」；三姿态共享 RDD 底座（01）与惰性执行（02/E4）。湖仓时代的续命版是「表格式统一存储、多引擎各取所需」——盘上对口：[../Apache_Iceberg活用入門/](../Apache_Iceberg活用入門/)、[../Apache_Paimon_Streaming_Lakehouse/](../Apache_Paimon_Streaming_Lakehouse/)、[../Apache_Hudi_Definitive_Guide/](../Apache_Hudi_Definitive_Guide/)（三目录 ls 实名登记 ✅，跨波对位另见各自 00）。

## 4.5 GraphX 算子手册与建图管线（教学流全录）

**算子四族** ⚠️（转述官方 guide 结构）：
- 结构族：`subgraph(epTripletFilter)` 导出诱导子图、`withReverseEdges`（双向遍历的重复边策略）、`cache()` 三件套（`persist(StorageLevel.DISK_ONLY)` 大图兜底）；
- 映射族：`mapVertices`（挂属性）、`mapEdges/edges.filter`（边清洗）、`groupEdges(reduce)`（平行边归并——新闻共现实体的常见前置）；
- 聚合族：`aggregateMessages(sendToSrc/sendToDst + mergeMsg)` 一切自定义消息传递的总入口、`degrees/inDegrees/outDegrees` 度统计；
- 连接族：`joinVertices`（特征表→图，广播字典是它的轻量替身）、`outerJoinVertices`（左连接保顶点）。

```scala
// 加权入度 = PageRank 消息原语（官方 guide 同款教学习惯）
val inW = graph.aggregateMessages[Double](
  triplet => triplet.sendToDst(triplet.attr), _ + _, TripletFields.In)
```

**文本→图管线**（`enwiki_dump.xml` 的标准消化流 ⚠️ 转述；仓库根数据 ✅ 实抓）：

1. 文本切分：`wholeTextFiles`/流式分片 → `title|<a>链接列表` 行式（02 文本源、03 源教义在此汇合）；
2. 实体解析：正则抽 `(srcTitle, dstTitle)` 边表；title→ID 字典 RDD + `broadcast`（01 §3 广播通道第一次真实用）；
3. 建图与收敛：`Graph(v, e)` → `connectedComponents` 量巨型分量 → `pageRank(tol)` 出权威榜（迭代前必 `persist`——否则每超步重放 dump 读取，🔧 E5 曲线的集群侧放大）；
4. 出图回表：顶点结果 `join` 回 DataFrame → `write.parquet`——「表化/图化/特征化」三姿态（§4）在此闭环。

**读图分寸**：GraphX 的一切「实时性」承诺都没有——它是**批式图分析框架**（收敛式算法+RDD 底座），把它当图数据库用是本册目录版要反复拆掉的误读；毫秒级图遍历的正读见盘上图数据库册（§1 已链）。

## 4.6 史料注：Learning Path 的图与 DL 章为什么「目录残缺」

合订册机制（00 §2）在本章留痕最重：Module_3 的 Chapter 10–16 文件夹带 `Code + Data` 成对交付，但**章名与叙事顺序属于被缝合单品书**——三本已证单品的图/DL 章节比例不可从可达源核定（⚠️ 00 §9.2）。因此本目录把 05 写成「GraphX 语义学 + 外接生态普查」的合题而非任何单品的转写：前者有官方 guide 恒久锚（✅），后者有 README `various external tools` 原句为证（✅ 实抓）。这是史册目录化的一种诚实姿势——**章不缺，归属不猜**。

## 4.7 时代差问答与自测（本章四问）

- **问：GraphX 算图数据库吗？** 答：不算——收敛式批算法+RDD 底座，没有毫秒级查询面（§1 判语行）；图库正读见 §1 链接的盘上目录。
- **问：本册的 DL 内容今天怎么处理？** 答：当 2019 年框架生态普查快照读（§3 存废表），任何「照搬外接件清单」的行为都是时代误置 ⚠️。
- **问：建图管线哪步最易翻车？** 答：第 2 步实体解析——正则抽链在维基 dump 上的假阳性率足以污染度分布；第 3 步忘 persist 则迭代重放 dump（§4.5，E5 曲线）⚠️ 转述经验。
- **问：E5 之于图的类比边界在哪？** 答：边界在「单机重放廉价、集群重放含网络与故障域」——量级直觉可迁，数字不可迁（00 §7）。

自测四题：① triplet 与 `aggregateMessages` 各在什么场景成为唯一选择；② 双向图在 GraphX 的两种表达及其代价；③ 三姿态（表化/图化/特征化）在 §4.5 管线四步中各自的落点；④ 为什么「Spark 备料+专用训练器」是 2.x DL 的可辩护现实而非退让。

## 4.8 一分钟带走（本册原声四句）

- 本册承诺位原声：`Analyze structured and unstructured data using SparkSQL and GraphX`（✅ 官方 README 实抓）——GraphX 在书名承诺中的分量与它实际的社区投入构成史料级反差（§4.6）。
- 图一句断：GraphX 是批式图分析的算子箱，不是图数据库的任何替身（§1 判语行）。
- DL 一句断：外接生态存废表（§3）是本册最诚实的一页时代墓志铭。
- 数据一句断：仓库根的 `enwiki_dump.xml` 与 `newsCorpora.csv`（✅ 实抓）就是 Learning Path 教学选材观的物证——dump 当教材、语料当玩具、沙箱当集群。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
|---|---|---|
| 属性图 | Property Graph (GraphX 形态) | 顶点/边各带属性、以并行列 RDD 表达的图模型 |
| 三元组 | Triplet | (源顶点, 目标顶点, 边属性) 的联表计算视角 |
| 超步迭代 | Pregel-style Iteration / BSP | 消息沿边传播、顶点在屏障处聚合更新的图计算范式 |
| 页码排名 | PageRank | 链接图的权威度收敛算法，GraphX 教学招牌 |
| 连通分量 | Connected Components | 无向可达分组的批式图算法 |
| 三角计数 | Triangle Count | 局部密集度指标（聚集系数的分子） |
| 顶点视图 | Vertex Views | 以顶点为轴看邻接边的 inner/outer/join 视图族 |
| 定向访问 | EdgeDirection | In/Out/Both 的边遍历取向 |
| 重尾度分布 | Heavy-tailed Degree | 维基链接图类现实图的核心统计特征 |
| 参数服务器 | Parameter Server | 外接 DL 时代 Spark 侧的梯度托管形态（史项） |
| 数据并行外壳 | Data-parallel Frontstage | Spark 只做分片与编排、训练让位专用引擎的分工模式 |
| 表化/图化/特征化 | Tabularization / Graphification / Featurization | 非结构化数据的三种 2.x 消化姿态 |
| 平行边归并 | groupEdges | 多重边折叠为单边的预处理算子（§4.5 映射族） |
| 收敛容差 | Tolerance (PageRank) | 超步迭代的停机判据，巨型分量与排名榜共用的「够了」定义 |

## 最新演进与工业实践

| 本书（2.x） | 2026 现状 | 依据 |
|---|---|---|
| GraphX 与核心同捆 | 官方文档线仍在（4.x 文档树可导航），但社区投入长期偏冷；工业图负载多迁专职图库/图计算引擎 | ✅ [graphx-guide](https://spark.apache.org/docs/latest/graphx-programming-guide.html) 在位；⚠️ 投入度为转述判语 |
| GraphFrames（DataFrame 图谱） | 独立社区项目线延续，属性图 API 比原生 GraphX 更贴 SQL 世界 | ⚠️ 外部项目 URL 本次不赘引 |
| 外接 DL 全家桶 | H2O/BigDL/CNTK 诸线谢幕或转型；「Spark 备料 + GPU 训练器」收敛为通用姿势 | ⚠️ 转述（存废表 §3 已标） |
| enwiki 式教学语料 | 图/文本基准数据集全面对象存储化，dump 直读教学已成复古姿势 | 类比锚 [../Streaming_Systems/10-大规模数据处理的演进.md](../Streaming_Systems/10-大规模数据处理的演进.md) |
| 版本坐标 | GraphX 无重大 API 代差，随 4.x 被动带版本 | ✅ [4.0.1](https://spark.apache.org/docs/4.0.1/) 文档树实抓 |
| 图基准数据集 | dump 直读教学让位于对象存储上的标准图基准（SNAP 系等） | ⚠️ 判语级转述，外部专页未赘引 |

**判语**：05 是本册「承诺与兑现落差」的计量章——README 的 DL 大伞下，2.x 能兑现的只有 MLP 与外接清单；诚实读法是把 §3 存废表当作 2019 年框架生态的一次普查快照，再用 ⚠️ 项对照 2026 现状。
