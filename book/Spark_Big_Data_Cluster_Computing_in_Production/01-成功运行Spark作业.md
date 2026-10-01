# 01 成功运行Spark作业（豆瓣实抓章题：第1章 成功运行Spark job；原书英文章题未实证 ⚠️）

> 书目：Spark: Big Data Cluster Computing in Production（Wiley, 2016, ISBN 978-1-119-25401-0，Ilya Ganelin/Ema Orhian/Kai Sasasaki/Brennonn York 著）。
> 本文件为**精读重构**：章题与全书定位来自 DNB 著录+豆瓣目录栏 ✅ 实抓；章内小节为 ⚠️ 推定讲解域（依内容简介与 Spark 2.3 官方文档公开结构），非原书文本。总纲见 [00-总览与阅读地图](00-总览与阅读地图.md)。

## 1. 本章要回答的问题（✅ 依 DNB 题名语义 + 豆瓣内容简介）

「成功运行 Spark job」= 让一个作业**在生产集群上**跑起来并可重复。豆瓣内容简介实抓：本书「涵盖了开发及维护生产级Spark应用的各种方法、组件与有用实践」——第 1 章承担「各种方法」的起点：作业形态与提交链。

## 2. ⚠️ 推定小节 A：Spark 作业的四层拆解

任何 Spark 作业，生产视角下拆成四层（此拆法为本目录讲解框架，标 ⚠️ 非原书章结构）：

1. **应用层**：driver 程序本身（spark-submit 入口 / 由调度系统触发的一次进程）。
2. **计算层**：executor 里的 task 并行度 = RDD 分区数/DAG 阶段——引擎语义细节在 #215 TDG 的头名册里已建档，见 [Spark_The_Definitive_Guide·00总览](../Spark_The_Definitive_Guide/00-总览与阅读地图.md)，本章不重复。
3. **资源层**：谁给 executor 发容器/槽位——即集群管理器，本章铺垫、第 2 章（`02-集群管理.md`）全开。
4. **运维层**：日志、重试、依赖分发（`--jars`/`--py-files` 归档）——2016 年正是「作业从手动 spark-submit 过渡到编排系统（cron/Airflow/Oozie）」的时代 ⚠️。

**时代坐标**：本书写作于 Spark 1.6→2.0 过渡期（豆瓣/DNB 2016 年著录 ✅；Spark 2.0 发布于 2016-07，官方文档线可查 https://spark.apache.org/docs/2.3.0/ ✅ 本会话 200 预检）。2.0 前 DataFrame 实验特性、2.0 后成默认 API——本书叙事重心因此不在 API，而在「提交与集群」侧，这正是它与 #215 的分工线。

## 3. ⚠️ 推定小节 B：一次提交链的解剖（依官方文档公开结构 ⚠️ 非原书）

**本册 vs #215 TDG 同知识点覆盖对照（阅读路由表）**：

| 知识点 | 本册处理 | TDG 处理（在盘） |
|---|---|---|
| RDD/DataFrame 语义 | 不展开 | 主体（04-07 文件域） |
| spark-submit 参数 | 生产形态：依赖/名字/重试 | API 手册式罗列 |
| 分区与并行度 | 结构性因果（🔧 组 1） | 引擎机制细节 |
| driver 内存边界 | 事故视角（FAQ Q2） | 语义视角 |
| eventLog/History | 提交链留证据一环 | 特性简介 |
| shuffle | 仅类比因果，落盘规格归 03 | 机制权威 |

`spark-submit` 到作业可见，中间发生（提交语义基准=https://spark.apache.org/docs/latest/cluster-overview.html ✅ 200 预检）：

1. 提交机进程化出 driver，向集群管理器**申请资源**；
2. 集群管理器分配 executor 容器，driver 与 executor 建立 **RPC 双向通道**（2.0 时代默认 Akka/TCP 随机端口——第 4 章安全域伏笔：随机端口对防火墙与网络策略极不友好 ⚠️）；
3. 任务以分区为单位下发，shuffle 落本地盘；
4. driver 端事件日志（eventLog）是事后诊断的唯一集中工件——生产环境**必开** `spark.eventLog.enabled`，配置项名 ✅ 见 https://spark.apache.org/docs/latest/configuration.html ✅ 200 预检。

**生产检查单（本目录提炼 ⚠️ 讲解框架）**：依赖是否自包含（jar/py 归档齐全）；`--name`/队列/优先级是否按租户标注；eventLog 路径是否集中可读；失败重试策略是否与编排系统职责不重叠。

## 4. 🔧 实测（DuckDB/SQLite 类比·非本书 Spark 引擎行为）

**🔧 实测组 1（倾斜键聚合，SQLite 3.45.3）**：方法——`:memory:` 建表 t(k,v) 灌 200 万行，其中约 2.5% 行的 k 恒为 1（模拟倾斜分区键），跑 `SELECT k, COUNT(*), SUM(v) FROM t GROUP BY k ORDER BY 2 DESC LIMIT 3`，墙钟 **0.895s**；结果 top3=[(k=1, 51250), (k=63, 31250), (k=62, 31250)]（`D:\develops\tmp\dbwave_w8_spwiley\` 内脚本可复跑）。
观察：**倾斜键的分组行数约为均衡键的 1.6 倍**——单机 SQLite 无所谓（全表扫一次），但类比到 Spark 即「最热 reduce task 拖尾」的根因形态：分组基数决定并行度上限，热键把长尾集中到一个桶。
⚠️ 边界声明：SQLite 单进程串行执行，无 shuffle、无 executor 概念，本组仅类比「倾斜键→桶大小不均」这一因果，**非本书 Spark 引擎行为**。

**🔧 实测组 2（读型作业的一次提交多消费者，DuckDB 1.5.5，exp2.duckdb 30M 行物化表）**：同一物化文件分别以 threads=1/4/8 跑全表 GROUP BY，墙钟 **1.166s→0.324s→0.168s**，近线性（见 `03-性能调优.md` 同数据复用）。
类比：**作业一次「计算」、结果多次「消费」的模式下，算力追加换吞吐近线性**——对应 Spark 里「并行度不足时加核无用、分区够多时加核线性」的方向性直觉；DuckDB 线程≠Spark executor，⚠️ **非本书 Spark 引擎行为**。

## 5. 与盘上他册的分工（互链，均已验存）

- 提交语义/API 权威：[Spark_The_Definitive_Guide·00总览](../Spark_The_Definitive_Guide/00-总览与阅读地图.md)（TDG 头名册，勿与其争语义细节）。
- Iceberg catalog 下的提交栈后日谈：[Use_Iceberg_with_Spark·00总览](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)。
- 编排调度的同域中文教材登记：[Spark大数据分析与实战](../Spark大数据分析与实战.md)（主题域不同，不并档，见 00 §8）。

## 6. 本章在 2016→2026 的回看要点（详见文末演进节）

2016 年「怎么把 job 跑起来」的选择题（Standalone/YARN/Mesos/DC-OS），2026 年只剩两条主线：Kubernetes 原生 + 云托管；spark-submit 之外又长出了 spark-connect 的客户端-服务器提交形态 ⚠️（未见实证版本细节处不给版本号）。

## 7. 生产提交 FAQ（⚠️ 本目录提炼，非原书条文）

- **Q1 为什么在提交机跑得好、上集群就挂？**——依赖未自包含：executor 节点没有你的 jar/pip 环境；对策：`--jars/--py-files` 归档分发，或底座镜像内置环境。
- **Q2 driver OOM 但 executor 空闲？**——数据在 collect/toPandas 处回聚 driver；生产红线：driver 不拉大数据（语义详见 [Spark_The_Definitive_Guide·00总览](../Spark_The_Definitive_Guide/00-总览与阅读地图.md)）。
- **Q3 同一 jar 多版本冲突？**——`--jars` 与底座 classpath（YARN 时代 Hadoop 版本矩阵）打架；对策：shade 重定位或统一底座发行版。
- **Q4 端口开哪些？**——driver↔executor RPC 段（2.0 随机端口最麻烦）、4040 UI、eventLog 写入路径；此题即 `04-安全.md` 的前半。
- **Q5 重试配几层？**——底座重试（YARN AM）× Spark task 重试 × 编排系统重试三层职责必须收敛，否则故障时雪崩式重复提交 ⚠️。
- **Q6 怎么给作业「留证据」？**——eventLog + History Server + `--name` 规范（队列/负责人/SLA 入名）：可观测三件套的前身（见 `03-性能调优.md` §5）。

## 8. 常见误区五条（⚠️ 讲解框架）

1. 把「会 spark-submit」当「能生产运行」——四层拆解（§2）缺任一层都会半夜接告警。
2. 用开发集群的默认并行度直觉上生产——分区数与底座配额是两件事（`02-集群管理.md`/`03-性能调优.md`）。
3. 以为引擎自带安全——2016 的默认是 fail open（`04-安全.md` 🔧 组 7/8 的类比结论）。
4. 以为升级 Spark 就免掉运维——AQE 等引擎演进吃掉的是参数调优，不吃掉「提交链解剖」。
5. 把本书当 API 书读——API 向需求请转 [Spark_The_Definitive_Guide·00总览](../Spark_The_Definitive_Guide/00-总览与阅读地图.md)（三角分工见 00 §8）。

## 9. 章末自测（读后应能口答）

- 画出 spark-submit 到 executor 可见的四步链（§3）。
- 说出倾斜键→桶行数不均的实测数字（🔧 组 1：约 1.6 倍）。
- 回答「为什么本书不细讲 DataFrame API」。
- 默写生产提交检查单四项（§3 末）。
- 说出「重试三层」各层名称与收敛原则（FAQ Q5）。
- 指出本册与 TDG 的分工线在路由表的哪两行（§3 表）。

## 10. 「一次提交」二十年形制小史（⚠️ 讲解框架，供定位本书坐标）

- 2010–2013：手敲 spark-submit（1.x API 未稳），单机脚本+cron 即「生产」。
- 2014–2016：**本书坐标**——提交进 YARN/Mesos 队列，编排系统（Oozie/Airflow）接管 cron，History Server 成为标配。
- 2017–2020：云托管集群（EMR 类）把底座退化为 SKU；提交参数由平台模板下发 ⚠️。
- 2021–2023：K8s Operator 化：作业即 CRD 清单（spark-operator 标题级 ⚠️，链接未过预检不引 URL）。
- 2024–2026：spark-connect 客户端/服务器分离提交；「提交机」概念开始消解（官方文档线 ✅ https://spark.apache.org/docs/latest/）。
- 读法：本书第 1 章的所有「常识」都停在第 2 行时间点上——对照本表逐条自问「今天还成立吗」。

---

## 核心概念速览（中英对照）

- **驱动** — Driver Program：持有 SparkContext、把 DAG 拆成阶段并调度任务的主进程；生产上它本身也是「一个需要被看护的服务」。
- **执行器** — Executor：常驻工作进程，按分区领任务、缓存数据、向 driver 汇报。
- **提交工具** — spark-submit：生产入口脚本，统一应用/资源/集群管理器三类参数。
- **集群管理器** — Cluster Manager：分配容器与槽位的底座（Standalone/YARN/Mesos/K8s），本书第 2 章主题。
- **部署模式** — Deploy Mode（client/cluster）：driver 落在提交机还是容器内，决定故障归属与网络暴露面 ⚠️ 术语通用、非原书小节。
- **依赖归档** — Application Archives/Jars：`--jars`/`--py-files` 把闭源依赖分发到每个 executor。
- **事件日志** — Event Log：driver 侧集中记录任务时间线，History Server 的数据源。
- **历史服务器** — History Server：离线回放已完成作业的唯一 UI，生产必配常驻服务 ⚠️。
- **分区** — Partition：并行度单位；分组基数=可并行上限（🔧 组 1 的倾斜类比锚点）。
- **DAG 阶段** — DAG Stage：以 shuffle 为界的执行单元。
- **检查点** — Checkpoint：长 lineage 作业的中间物化手段，2.x 时代生产惯例 ⚠️。
- **编排系统** — Scheduler/Orchestrator（Airflow/Oozie 等）：把「一次提交」变成「每天可重复的流水线」。

## 最新演进与工业实践

- **版本线**：Spark 4.0（2025 官宣发布，Apache 官方线）；4.x 默认 Java 17/Scala 2.13、新 UI 等细节**未在本书 2016 语境中**，本会话未逐条实证 → 一律 ⚠️。官方文档入口：https://spark.apache.org/docs/latest/（✅ 本会话 200 预检）。
- **提交形态**：`cluster-overview.html`（✅ 200 预检）描述的 manager 插件式提交框架沿用至今；Kubernetes 成为一等公民部署目标（官方 docs 内 K8s 运行模式章节，URL 未单独预检 ⚠️）。
- **spark-connect（⚠️ 标题级）**：客户端-服务器化提交/交互（Python 薄客户端）是 3.5/4.x 时代最重要的提交侧演进，方向上终结了「driver 必须与代码同进程」的 2016 假设；本节按纪律只给概念名与官方文档域，不引未验 URL、不引 DOI（Crossref 通道本会话可达但候选 DOI 皆 404，见 00 §2）。
- **工业实践**：托管化（云 EMR/Dataproc 类服务）把「跑起来」压缩成配置项，本册 01+02 的自建集群叙事在 2024–2026 主要存活于**私有合规域**（金融/政务自建 YARN→K8s 迁移长尾 ⚠️ 推断级，无引用支撑故仅作方向陈述）。
- **回看方法**：读本书第 1 章时，把它当作「提交链解剖学」而非版本手册——分区/倾斜/依赖分发三件套的因果在 4.x 时代仍然成立（🔧 组 1/2 即本机可复跑的因果佐证，均标非 Spark 行为）。
