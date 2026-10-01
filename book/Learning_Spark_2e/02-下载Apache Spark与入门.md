# 02 · 下载 Apache Spark 与入门

> 原书第 2 章（Downloading Apache Spark and Getting Started）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原；正文为精读重构，Spark 命令与行为 = ⚠️ 转述（本机不可装 Spark），文档实链见文末。对位：[TDG 02 架构与执行模型](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md)、[bigdata 11 调度资源与运维](../bigdata/11-调度资源与运维.md)。

## 2.1 本章定位

全书唯一"装机章"，但重心不在装：三步下载/shell 流程只占四分之一篇幅，四分之三给了**执行词表的建立**（SparkSession/Job/Stage/Task、窄宽转换、Spark UI）与**第一个独立应用**。2e 把"概念安装"放在"软件安装"之前，是明确的教学法选择——后面第 7 章调优全靠这里建立的词表。

## 2.2 下载与环境（⚠️ 转述，按官方文档口径）

- 从 https://spark.apache.org/downloads 取预编译包（"Build type: Maven" 的 tar.gz；历史版本按"Hadoop 2.7/3.2+ 预构建"选择）。
- 依赖：JDK 8/11（本书时代 JDK 1.8 为默认口径）；纯 Python 用户可 `pip install pyspark`（本书原话级口径：3.0 时代 pip 安装已是官方推荐路径之一；⚠️ 本环境实测 pyspark **不可安装运行**——沿用波 6 #215 结论，故本章全部命令为零执行转述）。
- 目录结构：`bin/`（spark-shell、pyspark、spark-sql、spark-submit）、`sbin/`（start/stop-master|worker）、`conf/`（spark-defaults.conf、spark-env.sh 模板）、`jars/`、`examples/`、`data/`（自带 sample 数据，本章 M&M 计数即用之）。

## 2.3 两个 Shell 与 spark-submit

- **spark-shell**（Scala REPL）/ **pyspark**（Python REPL）：本地模式一条命令起，`spark.read.text(...)` 即可试跑；`--master local[*]` 语义：单机多线程模拟。
- **spark-submit**：生产入口。关键参数词表（⚠️ 官方文档口径，https://spark.apache.org/docs/latest/submitting-applications.html 同族页）：`--master`（yarn/k8s/spark://）、`--deploy-mode client|cluster`、`--num-executors/--executor-memory/--executor-cores`（YARN 系）、`--conf` 任意键。Driver 是否随容器进集群是 client/cluster 的唯一本质差别。
- **Databricks Community Edition**：本章给出的"零装机"路径——免费集群 + notebook + 样例数据；2026 回看：CE 仍在线但已非推荐教学件（⚠️ 平台政策变动频繁，不展开）。

## 2.4 应用概念词表（本章的真正主干）

| 概念 | ⚠️ 转述口径 | 与数据库世界的类比 |
| --- | --- | --- |
| SparkSession | 唯一入口对象，封装上下文/配置/catalog；`SparkSession.builder.appName(...).getOrCreate()` | 连接 + 目录 + 会话变量三合一 |
| Spark Job | 一次 action 触发的执行单元 | 一条查询 |
| Spark Stage | 按 shuffle 边界切分的阶段 | 执行计划的分段物化点 |
| Spark Task | Stage 内每分区一个 | 并行 worker 单位 |
| 转换/动作 | transform 惰性登记，action 物化触发 | SQL 的"解析不执行" vs "执行" |
| 窄/宽转换 | narrow 一分区进一分区出；wide 跨分区重分布（shuffle） | 类比：无 barrier 算子 vs 带 barrier 算子 |

🔧 **概念类比（非本书 Spark 引擎行为）**：用 SQLite 3.45.3 观察"视图惰性 vs 物化"——`CREATE VIEW v AS SELECT k, sum(id) FROM base GROUP BY k` 后对 v 做 `EXPLAIN QUERY PLAN`，得到 `CO-ROUTINE v → SCAN base → USE TEMP B-TREE FOR GROUP BY`：视图定义只在读取时展开（惰性），而 `CREATE TABLE m AS ...`（CTAS）立即物化。这精确类比 Spark "transform=登记计划、action=真正干活"的两段式；300 万行 DuckDB 侧实测：建视图 ~0.3s、首读 ~18ms vs CTAS ~391ms、复读 ~0.6ms（`meas.txt` G6 组）。**这是 SQLite/DuckDB 单机行为，不是 Spark。**

## 2.5 Spark UI（章节标题："Spark UI"）

- 本地模式默认 `http://localhost:4040`，作业运行期间可见：Jobs→Stages→Storage→Environment→Executors 五页签（词表 ⚠️ 转述）。
- 本章教学动作：跑 M&M 计数后打开 UI，认三个东西——Job 数、每 Stage Task 数（=分区数）、shuffle read/write 量。**2e 把 UI 前置到第 2 章**，1e 没有这个安排——调优是默认技能而非进阶选项，是本书方法论信号。
- History Server（`spark.history.fs.logDirectory` + eventLog 开启）在生产侧取代临场 UI；本册不展开，第 7 章回马枪。

## 2.6 第一个独立应用（"为 Cookie Monster 数 M&M"）

- 样例数据：`data/mllib/almuch.txt` 形态的"一袋袋 M&M 颜色清单"（⚠️ 具体文件名以发行包为准）；任务：按颜色计数。
- Scala 版给出 build.sbt/maven 两条打包路线 + `spark-submit --class ... target/...jar`；PySpark 版免打包（`--py-files` 或直接单文件）。
- 教学点： RDD→DataFrame 两写法同屏对比（`sc.textFile(...).flatMap(...).countByKey()` vs `spark.read...groupBy("color").count()`），在第一个程序里就宣告"本书主 API 是 DataFrame"。

## 2.7 常见坑（社区共识 + ⚠️ 转述）

1. Windows 本机跑 Spark 需要 winutils/hadoop home 补丁（本书时代即存在，社区长期痛点）；2020 前后 Hadoop 3.5+ winutils 分支可解——**这是"教学册默认你在 Linux/CE"的隐式假设**。
2. `local[*]` 与真集群的分区默认值差异（本地看线程数，集群看 minPartitions/文件切片）导致复现不出性能行为。
3. JDK 版本与 `--add-opens` 模块系统冲突（Java 17 起才爆发，书未涉及——演进节补）。

## 2.8 小结

装机的琐碎被刻意压缩，本章真正的产出是**词表 + UI 习惯 + 第一 jar**：此后所有章节的作业都在"SparkSession→惰性图→action→UI 看执行"这条回路上进行。

## 2.9 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| 第 1 步：下载 Apache Spark | 2.2 |
| Spark 的目录和文件（bin/sbin/conf/jars/examples/data） | 2.2 末条 |
| 第 2 步：使用 Scala/PySpark Shell（本地机器） | 2.3 |
| 步骤 3：理解 Spark 应用概念（App 与 SparkSession/Jobs/Stages/Tasks） | 2.4 表前四行 |
| 转换、动作和惰性评估；窄转换和宽转换 | 2.4 表后两行 |
| Spark UI | 2.5 |
| Databricks Community Edition | 2.3 末条 |
| 您的第一个独立应用程序（本地机器） | 2.6 |
| 为 Cookie Monster 计算 M&M 的数量 | 2.6 |
| 在 Scala 中构建独立应用程序（build.sbt/Maven 打包） | 2.6 |
| Summary | 2.8 |

## 2.10 重建示例：三条入口命令（⚠️ 语义转述自官方文档线，本目录未执行）

```bash
# 入口一：本地教学壳（Scala）
./bin/spark-shell --master "local[*]"
scala> val df = spark.read.text("data/mllib/almuch.txt")   # 惰性：只登记
scala> df.count()                                          # 动作：真算

# 入口二：Python 壳（pip 路线，本书时代已官方背书）
pip install pyspark && pyspark --master "local[*]"

# 入口三：生产提交（client vs cluster 只挪 Driver 的位置）
./bin/spark-submit --class com.example.MMCount \
  --master yarn --deploy-mode cluster \
  --num-executors 4 --executor-memory 4g --executor-cores 2 \
  target/scala-app_2.12-0.1.jar s3a://bucket/in/
（jar 名/参数按发行包实际为准——⚠️ 零执行，命令仅存档语义）
```

## 2.11 课堂问题（答不出回本文件）

1. SparkSession 与旧 SparkContext 的关系一句话？
2. 一个 Action、一个 Job、若干 Stage、若干 Task 的触发链是什么？
3. 窄/宽转换的判别标准（一句话版）？给一个宽转换的 SQL 对应物。
4. client 与 cluster 部署模式下，`--files`/日志去向有何不同？
5. UI 的 4040 只能"临场"，事后取证靠哪两件套？
6. 为什么 `local[*]` 下复现不出集群的分区行为（2.7 第 2 条）？

## 核心概念速览（中英对照）

- **SparkSession** — 会话总入口：上下文、配置、Catalog 的持有者。
- **spark-submit** — 生产提交工具：master/deploy-mode/资源参数一揽。
- **client / cluster 部署模式** — 两种模式：Driver 在提交机 / 在集群容器内。
- **local[*]** — 本地全核模拟：教学与单测专用。
- **Spark Job / Stage / Task** — 作业/阶段/任务：action 级、shuffle 边界级、分区级三层粒度。
- **窄转换/宽转换** — Narrow/Wide Transformation：是否跨分区重分布（shuffle barrier）。
- **Spark UI** — 4040 临场观测台：Jobs/Stages/Storage/Executors。
- **History Server** — 事后观测台：eventLog 回放。
- **REPL（spark-shell/pyspark）** — 交互式壳：Scala/Python 两条即时通路。
- **Databricks Community Edition** — 社区版托管：免装机的教学集群。
- **winutils** — Windows 本地补丁：非官方支持的装机坑。

## 最新演进与工业实践

- **版本线**：Spark 3.0（2020）→ 3.5（2023/24）→ **4.0（已发布，官方页 ✅ curl 200：https://spark.apache.org/releases/spark-release-4-0-0.html）**；4.0 起 Java 17 为编译基线（⚠️ 转述），本章 JDK 1.8 口径整体作废。
- **Spark Connect**：4.0 的标志性变化——轻量 Python 客户端 `pyspark-client`（官方 release note 实抓：仅 1.5MB）、默认开启 Connect 的发行包、`spark.api.mode` 开关（✅ 同上 URL）。教学含义：本章"下载 tarball 起 shell"的入门叙事正在被"pip 装瘦客户端连远端"替代。
- **容器化装机**：官方镜像 `apache/spark` 与 K8s Operator 成为部署主流（⚠️ 转述，spark.apache.org/docs/latest/running-on-kubernetes.html 同族文档线）；YARN 进入维护期叙事。
- **Databricks CE 现状**：⚠️ 政策多次调整，2026 年教学场景更多转向本地 DuckDB/Polars 预教学 + 云上免费层，本册装机章的"社区版"小节整体老化。
- **工业实践**：CI 里跑 Spark 单测的标准件是 `spark-testing-base`/`pytest-spark`（⚠️ 转述未逐仓核验）；本目录纪律下零执行，全部命令仅存档语义。
- **对照阅读**：中文环境的 Windows 装机血泪与国产发行版差异见 [../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)；执行模型的纵深推导见 [../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md)。
