# 02 — Apache Spark 入门（Getting Started with Apache Spark）

> 《Modern Data Engineering with Apache Spark》第 2 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_2` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 hands-on 册通行编排反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

全书第一次按下 Spark 运行键的章节：安装、启动、跑通第一个应用。它的教学功能是**把「引擎」从抽象名词变成可用工具**，为 3–13 章提供可执行的心智底座；工程功能是把 local 模式与集群模式的边界画清楚——这直接决定 14/15 章为什么要「搬家」。

## 2. Spark 的最小概念栈（⚠️ 按章题域重构）

- **SparkSession**：一切结构化 API 的入口对象；`SparkSession.builder.appName(...).master("local[*]").getOrCreate()` 是本书 hands-on 的第一行咒语（⚠️ 通行惯例推定）。
- **执行单元三层**：Application（一个 driver 进程）→ Job（一个 action 触发）→ Stage（按 shuffle 切分）→ Task（分区级并行单元）。本书作为工程册大概率在入门章给出此金字塔，供后文排错时引用（⚠️ 推定）。
- **API 层次**：DataFrame/Spark SQL 为默认工作面；RDD 保留为底层逃生门——2022 年出版物普遍采取这种「结构化优先」的教学次序，与 TDG 的 2.x 时代叙事（RDD 先行）形成刻意的代际差。
- **资源模式**：`local` / `local[N]` / `local[*]` 的线程语义差异；单机即可体验分区并行，这是「本地数据平台」承诺的技术支点。

## 3. 发行形态与安装路径（⚠️ 重构 + 官方文档校核）

- 官方预编译包（download 页选择 Spark release + Hadoop 组合）——tar 解压即得 `spark-shell`/`spark-submit`/`pyspark` 三件套；校核文档 ✅ https://spark.apache.org/downloads.html。
- Windows 环境下 hands-on 册的常见坑（winutils/HADOOP_HOME）：2022 年 Apress 读者高频问题，⚠️ 本书是否展开未证实。
- pip 安装 `pyspark` 作为替代路径：对「只要 Python API」的读者更短，但本书若走 spark-submit 部署线（14/15 章），预编译包更像主线（⚠️ 推定）。
- 版本策略：本书成书于 Spark 3.2 时代（3.3 出版同期），入门章通常锁定单一版本避免兼容分叉（⚠️ 推定）。

## 4. 第一个应用解剖（⚠️ 按章题域重构）

典型入门样本的解剖切片：

1. 读入本地文本/CSV → 形成 Dataset 行。
2. 一次转换（filter/select/groupBy）→ 惰性求值，**此时什么都不发生**。
3. 一次动作（show/count/write）→ 触发 DAG 调度，UI(4040) 里出现 Job/Stage。
4. 观察 Spark UI：这是 hands-on 册与参考书的教学分野——工程册会强迫你**看**执行，而非只看结果。

> 对位精读：本节心智模型的系统化展开在 [../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md)，本书此处止于「能跑能看」。

## 5. 与 repo 谱系书的入门分工

| 问题 | 本书答法（工程册） | 盘上更深的答法 |
|------|--------------------|----------------|
| Spark 是什么 | 数据工程师的主引擎 | [../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md](../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md) |
| 为什么快 | 不展开论文级论证 | [../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md) |
| RDD 细节 | 点到为止 | [../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)（中文早期语境） |
| 集群调度全景 | 留给 14/15 章 | 官方总览 ✅ https://spark.apache.org/docs/latest/cluster-overview.html |

## 6. 🔧 类比实验：「惰性求值+分区并行」的单机投影（非 Spark 行为）

Spark 的 transform/action 二分可用 DuckDB 直接类比：

```python
import duckdb
con = duckdb.connect()
con.execute("CREATE TABLE t(i INT)")
con.execute("INSERT INTO t SELECT * FROM range(1_000_000)")
rel = con.sql("SELECT i%10 k, sum(i) s FROM t WHERE i>100 GROUP BY k")  # 惰性：未执行
print(rel.explain())   # 只出计划，不耗 CPU
print(rel.fetchall())  # 物化：此刻才算
```

- 观察 1：构建 `rel` 无耗时，`explain()` 揭示计划树——对应 Spark「transformation 惰性、action 触发」。
- 观察 2：DuckDB 多线程按分片并行聚合——对应 `local[*]` 的分区并行语义。
- 边界声明：DuckDB 是单进程向量化引擎，没有 Stage/shuffle 容错线；「Spark 的 RDD 血缘恢复」在本类比中**不存在**，不可外推（🔧 类比止于此）。

## 7. 常见入门事故清单（工程册必有节，⚠️ 重构）

- master 串写错（`local[*]` 打成 `local *`）→ 静默回退或异常栈。
- JAVA_HOME/模块系统（Java 17+ 对 Spark 3.2/3.3 需要 `--add-opens`，Spark 4 才原生支持高版本 JDK）⚠️ 本书成书时 JDK11 尚为主流，此坑为后补。
- Python 版本与 pyspark 打包版本不一致 → worker 找不到模块。
- 把 `getOrCreate` 当幂等魔法，多 Session 混用导致 accumulator/UI 指向漂移。
- 误用 `collect()` 拉爆 driver 内存——入门章最常被引用的一条纪律（✅ 官方文档强调见 programming guide）。

## 8. 本章校读清单

- 本书入门章是否配置过 `spark.sql.shuffle.partitions` 之类的调优钩子？——决定 14 章资源讨论的伏笔。
- spark-shell/PyCharm/Jupyter 三者作者用哪个？——hands-on 体验差异大（⚠️ 未证实）。
- 是否演示 Event Log + History Server？——若演示，14 章会复用。

## 9. 本章实验卡（hands-on 重构导引，⚠️ 非原书代码照录）

1. 启动：`spark-shell --master "local[*]"` 或 `bin/pyspark --master local[*]`；记录 banner 里的版本行（对照 §3 的版本策略）。
2. 一行数据：`spark.range(1000000).groupBy($"id" % 100).count().show()`——同时体验惰性构建与 action 触发。
3. 打开 4040 UI：找出本页的 Job 数、Stage 数、Task 分布——「看执行」练习第一次。
4. 改 master 为 `local[1]` 重跑：UI 里 Task 串行化，wall-clock 变长——分区并行肉眼可见。
5. 退出并检查 `spark-warehouse/`、`metastore_db/` 残留：catalog 持久层的第一眼（→ 6 章）。

验收：能口述「一个 action 如何变成 N 个 task」；能在 UI 里指出 shuffle 前后两个 Stage。

## 10. 与前后章的接线（本目录章间导航）

- ← 01：本章把「主引擎」名词变成动词；01 的平台版图在此长出第一个进程。
- → 03：`spark.range` 换成 `spark.read`，入门即转生产语义；本章的 UI 功夫在 03 的小文件事故里立刻回本。
- → 14/15：`local[*]` 到集群的每一次参数迁移（master/deploy-mode）都是这两章的主题预演。
- → 10：`getOrCreate` 的 Session 生命周期问题在流查询里放大成「driver 长跑」运维问题。

## 11. 校读问答（五问五答，⚠️ 目录自问自答）

- **Q：入门章要不要讲 RDD？** A：2022 工程册共识是最少必要接触——本书大概率把 RDD 用作解释执行模型的化石（⚠️ 推定）；盘上系统展开在 TDG 07 号文（文件名含全角冒号，登记不链）。
- **Q：local[*] 和生产差多少？** A：差整个分布式层（网络序列化、槽位仲裁、失败域），不差计算语义——入门章的诚实写法应明说此点。
- **Q：为什么强调看 UI？** A：工程册与参考册的分界：参考册教你得到答案，工程册教你看见过程。
- **Q：Windows 用户怎么办？** A：WSL2/容器是 2024 后的现实答案；本书当年若走 winutils 路线，步骤已属考古 ⚠️。
- **Q：Spark 4.x 重学入门要重读什么？** A：JDK17+、Connect 客户端、Scala 2.13 三件事；其余心智可平移（§演进节）。

## 核心概念速览（中英对照）

- **SparkSession** — SparkSession：结构化 API 统一入口，封装上下文与配置。
- **本地模式** — Local Mode：单机多线程模拟集群，`local[*]` 按核数开线程。
- **惰性求值** — Lazy Evaluation：转换只建计划不执行，动作触发计算。
- **动作** — Action：count/show/write 等产生副作用或结果的算子。
- **阶段划分** — Stage：按 shuffle 边界切分的调度单元。
- **任务** — Task：分区粒度的最小执行单元。
- **Spark UI** — Spark UI：4040 端口的执行观测面，工程册的必修视图。
- **预编译发行包** — Pre-built Distribution：按 Hadoop 组合打包的官方二进制。
- **spark-submit** — spark-submit：应用提交入口，14/15 章部署的前身。
- **血缘** — Lineage：RDD 时代的容错叙事，DataFrame 时代部分让位于 checkpoint。

## 最新演进与工业实践

- **Spark 4.x 入门形态变化**：Connect 模式使「本地客户端 + 远端引擎」成为默认教学形态之一，`SparkSession.builder.remote("sc://host")` 替代部分 local[*] 场景 ⚠️（官方文档 ✅ https://spark.apache.org/docs/latest/ 下的 client-server 教程，本波未逐一展开 URL）。
- **版本实查** ✅（2026-10，downloads 页）：最新 4.2.0；维护线 3.5.9/4.0.4/4.1.3——本书 3.2 代码片段与 4.x 存在 Scala 2.13/Java 17+ 默认、ANSI SQL 默认开启等代差。
- **JDK 基线**：Spark 4.x 要求 Java 17+（3.5 仍兼容 Java 8/11/17），⚠️ 转述 + 官方发行说明校核。
- **发行渠道**：除 apache.org 外，conda-forge `pyspark`、Databricks Runtime、Amazon EMR 托管版本并存；工业上「本地装 Apache Spark 学习、生产用托管」成为成本主流（⚠️ 观察性陈述）。
- **不可实测降级**：本目录所在机器无法运行 Spark/JVM 全栈（波6 #215 实证 pyspark 不可装），本章所有 Spark 运行时细节均为「官方文档转述 + ⚠️」；入口 ✅ https://spark.apache.org/docs/latest/rdd-programming-guide.html（含最经典的 WordCount 教程节）。
