# 01 Introduction to Apache Spark（Spark 入门）

> 原书 Ch1，pp.1–15。本章是全书最短的一章：15 页里讲完 Spark 的历史定位、编程模型分层与「为什么本册从 DataFrame 出发」。二级小节未实抓 ⚠️，以下主题簇依章题、页幅与同谱系册交叉推定重构，属**精读重构**而非原书文本。

## 1.1 Spark 是什么：一句话与一段历史 ⚠️（主题簇推定）

- 官方定义面：Apache Spark 是**统一分析引擎**——一个运行时（Spark Session）之上承载多种负载：SQL、批处理、流处理、机器学习、图计算。这个「统一」叙事是 Hadoop 时代「多引擎拼装」的反动：MR 做批、Storm 做流、Mahout 做 ML，各套 API 各套数据搬运。
- 历史锚点（转述 ⚠️，据官方文档口径）：Spark 诞生于 UC Berkeley AMPLab（约 2009），核心论文与项目由 Matei Zaharia 主导；2013 年进入 Apache 孵化、2014 年成为顶级项目；本册写作时（2021-10）主线为 Spark 3.2。
- 与 Hadoop 的常见误解：Spark **不是** HDFS 的替代（存储层可复用），也**不是**必须依赖 YARN（cluster manager 可插拔：Standalone/YARN/K8s，见 `02`）。国内教材（如盘上 [../Hadoop大数据技术原理与应用.md](../Hadoop大数据技术原理与应用.md)）把 Spark 放在 Hadoop 生态课里讲，是「生态视角」；本册是「引擎视角」，两种地图别混。

## 1.2 分层：RDD → DataFrame/Dataset → SQL → 高层库 ⚠️

本章给出的心智模型（重构表述）：

| 层 | API | 给谁用 | 优化器可见性 |
| --- | --- | --- | --- |
| 底层 | RDD | 框架作者/特殊算子 | Catalyst 不可见，黑盒 |
| 中层 | DataFrame/Dataset | 数据工程师主战场 | 逻辑计划级可见 |
| 接口 | Spark SQL | SQL 用户/BI 接入 | 全计划可见 |
| 上层 | Structured Streaming / MLlib / GraphX | 场景库 | 建在中层之上 |

- 本册的立场非常明确：**入门直接学 DataFrame/SQL，RDD 只做背景知识**。这与 2015 年代教材（先 RDD 后 SQL）相反，是 Spark 2.x 合并 API 之后的教学共识；盘上中文单文件《Spark大数据分析与实战》（黑马程序员）仍以 RDD/Scala 起步 ⚠️（读其头注所得），这是两册教学路径的最大差异。
- Structured Streaming 不是「另一套流引擎」，而是**同一查询引擎在增量数据上的复用**——这个论点在 Ch6 才展开，Ch1 只埋线。

## 1.3 三根支柱与全书路线 ⚠️

- Ch3–5 = 支柱一（Spark SQL/DataFrame：读写、进阶、优化）；Ch6–7 = 支柱二（流）；Ch8–9 = 支柱三（ML 与其生命周期）。
- 原书前言声明读者画像：会基础 SQL、有一门语言（Scala 或 Python）常识即可；本书代码以 Spark 3.2 为准 ⚠️（据出版社页语言/主题标签推定）。
- 本目录的读法修正：三支柱「都学」= 都只能到 60 分；把本册当**选路器**，选定一根后转盘上权威册（[../Spark_The_Definitive_Guide/00-总览与阅读地图.md](../Spark_The_Definitive_Guide/00-总览与阅读地图.md)）。

## 1.4 本地起步：spark-shell / PySpark / spark-submit ⚠️（转述+本机状态）

- 官方文档给出的入门三件套：`spark-shell`（Scala REPL）、`pyspark`（Python REPL）、`spark-submit`（提交应用）；本地 `--master local[*]` 模式单进程即可体验。锚点：https://spark.apache.org/docs/latest/（✅ curl 200 主页；API 文档 4.0 面 https://spark.apache.org/docs/4.0.0/api/python/index.html ✅ 200）。
- 🔧 本机状态：Spark/PySpark **不可安装**（JVM 环境+分发限制，沿用波6 #215 实测结论，本波直接沿用）——因此本目录一切「执行/计划」类断言用 SQLite/DuckDB 做概念类比并逐组标注**非本书 Spark 引擎行为**；Spark 行为本体全部 ⚠️ 转述官方文档。
- 类比锚（供后续实验预热）：把 `local[2]` 理解成 DuckDB 的进程内实例、把 cluster 理解成 Client/Server——机制相似度有限，仅作「先单机后分布式」的入门节奏类比，不外推性能。

## 1.5 本章练习视角与易错点 ⚠️

- 原书章末有小结+练习（Beginning 线标配）⚠️；最有价值的自建练习：安装本册依赖链（JDK+Spark 发行包，本机不可行 → 改为在 Databricks Community/学院版云集群上跑官方 quickstart，⚠️ 转述，非本目录实测）。
- 入门者三大概念陷阱（重构自书评与常见问答，⚠️）：① 把 Spark 当数据库（它是引擎，持久化靠表格式/文件系统，见 `03`）；② 把 DataFrame 当 pandas（惰性求值+分布式分区是根本差异，见 `02`）；③ 把「Spark Streaming」和「Structured Streaming」当同义词（旧 DStream 与新 SS 是两代模型，本册 Ch6 两者都讲，读时注意分界，见 `06`）。

## repo 视角：本谱系对照关系

| 对照 | 链接 |
| --- | --- |
| Spark 权威参考册的入门章 | [../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md](../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md) |
| 中文 bigdata 目录的引擎演进章 | [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md) |
| Flink 入门对照（同「统一引擎」叙事的另一版本） | [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md) |

## 1.6 导言卡：本册承诺与不承诺（重构表述 ⚠️）

- 承诺一：读完能看懂 Spark 三套 API 的**门面**——知道 DataFrame、Structured Streaming、ML Pipeline 各自解决什么。
- 承诺二：能独立完成「读脏数据→清洗→聚合→写出分区表」的最小工作闭环。
- 承诺三：对 ML 生命周期有地图感（知道 MLflow/特征平台/监控这些站名）。
- 不承诺一：生产集群部署与容量规划（37 页优化章撑不起，见 `05` 的清单性质）。
- 不承诺二：任何一根支柱的纵深（SQL 内核、流式语义、算法原理都只到「概念正确」）。
- 不承诺三：Scala 语言教学——语法假定读者自学过，全书示例双轨给 Scala/Python ⚠️ 比例推定。
- 读者画像（依出版社主题标签与前言惯例 ⚠️）：会 SQL、有一门编程语言常识、想在本职里用上 Spark 的分析工程师/初学者。

## 1.7 常见问题与修正（重构自书评与社区答疑语境 ⚠️）

- Q：要不要先学 Scala？
  A：本册答案：不要。Python 主线走完再按需补 Scala 阅读能力；Scala 门槛在本册被刻意压低（Ch2 才出现双轨示例）。
- Q：Spark 会取代 Hadoop 吗？
  A：问错了层。Spark 是计算引擎，Hadoop 的 HDFS/YARN 是存储与资源层；本册示例甚至用不上 YARN（local 模式起步）。
- Q：学 Spark 还是 Flink？
  A：批与 SQL 主导选 Spark（本册三支柱），低延迟流主导选 Flink（盘上 [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)）；2026 的现实是很多岗位两者都要，本册的价值是给你「统一引擎」的第一心智。
- Q：GraphX 怎么不讲？
  A：本册副题里就没有图；GraphX 在 TDG 有专面 ⚠️，入门阶段可安全忽略。
- Q：这本书过时了吗（2026 读 2021 册）？
  A：三支柱框架未过时；版本细节（3.2 API 面、DStream 篇幅、MLlib 地位）已漂移——按本目录各章「最新演进」节打补丁读即可。

## 1.8 三件必做与一张自检单（重构）⚠️

- 必做一：把 1.2 的分层表反向默写一次（给 API 名，说层级与优化器可见性）。
- 必做二：用一句话向同事解释「Spark 不是数据库」，并给出你依据的分层位置。
- 必做三：选定你的第一根支柱（SQL/流/ML），在 00 §四的动线表里找到你的路线编号。
- 自检单（5 项，全勾才进 Ch2）：
  - [ ] 能说出 Spark 诞生地与公司线（AMPLab→Apache→Databricks 商业化的三角）⚠️
  - [ ] 能区分 transformation 与 action（各举一例）
  - [ ] 能解释「统一引擎」对「多引擎拼装」的胜利点
  - [ ] 知道本机 Spark 不可装的现实约束与本目录的双轨验证法
  - [ ] 知道 RDD 在本册的「背景知识」定位，不会去找 RDD 专章

## 1.9 与前人笔记的关系（本谱系互读指引）

- 若你读过黑马程序员《Spark大数据分析与实战》：本册 Ch1≈其第 1 章的英文原版，但把「环境搭建」换成「分层地图」——用本目录 `01` 补引擎视角，用 `02` 的对照表补回你熟悉的中文术语。
- 若你读过 bigdata/ 两册（杨力/朱松岭）：本册等于其「框架视角」部分的英文平行版；差异集中在 Scala 前置缺失（杨力册 Ch1–4 全在补 Scala）与 ML 线增加（两册均无 ML 章）——这正是本册第三支柱的增量价值，见 `08`。
- 若你直接跳过入门想读 TDG：可以先读其 [../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md](../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md)，再回本目录补「练习题与读者画像」层——两册是参考书与讲义的关系，不是替代关系。

## 1.10 速自检十问（30 秒版，答案都在上文）

1. Spark 的统一引擎叙事反对的是什么旧格局？
2. 四层 API 中优化器可见性最高的是哪层？
3. RDD 在本册的教学定位一句话？
4. Structured Streaming 与批查询共享什么？
5. local 模式与集群模式的语义分界在哪？
6. 为什么本册把「装 Spark」外包给云/文档？
7. DStream 与 Structured Streaming 的分界是什么？
8. 本册三支柱指哪三根？
9. 「Spark 不是数据库」——那数据活在谁手里？
10. 读完 Ch1 你该做出的第一个选择是什么？

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 统一分析引擎 | Unified Analytics Engine | 一套运行时承载 SQL/批/流/ML 的定位叙事 |
| 惰性求值 | Lazy Evaluation | 转换只建计划，行动作才执行——DataFrame 语义的根 |
| 编程模型分层 | RDD / DataFrame / SQL layering | 优化器可见性自上而下递减，控制力递增 |
| AMPLab 血统 | UC Berkeley AMPLab | Spark 起源地，Matei Zaharia 主导 |
| local 模式 | local[*] | 单机多线程，入门与单测标配 |
| 提交式运行 | spark-submit | 应用打包提交到 cluster manager 的交付形态 |
| 引擎≠存储 | Engine vs Storage | Spark 不拥有数据，读写经数据源/表格式 |
| 两代流 API | DStream vs Structured Streaming | 旧 RDD 流与新查询引擎流的代际分界 |
| 三支柱选路 | SQL / Streaming / ML | 本册均衡入门后应择一深入 |
| 生态视角 vs 引擎视角 | Hadoop-course vs Spark-book | 国内教材与国际专册的两种讲法 |

## 最新演进与工业实践

- **版本面（2021→2026）**：本册基于 Spark 3.2；此后 3.3/3.4/3.5 连发，**4.0 于 2025 年发布**（Scala 3 实验支持、Spark Connect 成为一等公民、ANSI SQL 合规默认化）。官方新闻与发布说明：https://spark.apache.org/news/（✅ curl 200）。入门结论到 2026 仍成立的：DataFrame-first 教学路径、三支柱地图；已过时的：DStream 教学占比（官方已把 3.x 后期重心全压 Structured Streaming，DStream 文档仍在但属遗留 ⚠️）。
- **架构演化对「统一引擎」叙事的修正**：Spark Connect（客户端-引擎协议分离）让「一个 JVM 里跑 REPL」的经典入门画面变成「瘦客户端连远端会话」；工业界（云托管 Databricks/EMR/GCP Dataproc）已把「装 Spark」这一课从入门路径中删除 ⚠️（云产品文档口径，非本机实测）。
- **入门读物现状（2024–2026）**：官方 Programming Guide 与盘上 [../Spark_The_Definitive_Guide/00-总览与阅读地图.md](../Spark_The_Definitive_Guide/00-总览与阅读地图.md) 仍是权威面；「Beginning 线」的同类竞品（Learning Spark 2e）在本工程为波8 兄弟 #196，仅登记不链。本册的差异化价值维持：以最短篇幅把 SQL/流/ML 三根柱子各立一根，再让读者自选深潜方向。
