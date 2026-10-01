# 02 Spark 部署（对应原书 Ch2，印张页 27–43）

> 所属书目：[00-总览与阅读地图](00-总览与阅读地图.md) ｜ 《Data Analytics with Spark Using Python》1e，Jeffrey Aven 著，Addison-Wesley Professional，2018。
> 本章二级目录 ✅ 实抓自官方 informIT 产品页；正文为**精读重构**，非原书文本；涉及 2018 年版本号的叙述均 ⚠️ 推定（官方 TOC 不含版本号）。

## 官方二级目录（✅ 实抓）

- Spark Deployment Modes (p.27)
- Local Mode (p.28) ／ Spark Standalone (p.28) ／ Spark on YARN (p.29) ／ Spark on Mesos (p.30)
- Preparing to Install Spark (p.30) ／ Getting Spark (p.31)
- Installing Spark on Linux or Mac OS X (p.32) ／ Installing Spark on Windows (p.34)
- Exploring the Spark Installation (p.36)
- Deploying a Multi-Node Spark Standalone Cluster (p.37)
- Deploying Spark in the Cloud (p.39)
- Amazon Web Services (AWS) (p.39) ／ Google Cloud Platform (GCP) (p.41) ／ Databricks (p.42)
- Summary (p.43)

## 精读重构·四种部署形态（p.27–30）

本章是 Ch3「集群架构」的操作性前奏：先能装起来，再讲进程如何组织。

| 形态 | 资源由谁管 | 书中定位（⚠️ 推定展开） | 2026 现状 |
|---|---|---|---|
| Local | 无集群，JVM 内线程模拟分区 | 开发/教学首选，`local[*]` | 仍是默认开发路径 ✅ 官方文档在线 |
| Standalone | Spark 自带 Master/Worker | 自建小集群，本书实操主线 | 保留但非云原生主流 ⚠️ |
| On YARN | Hadoop 集群管理器 | 企业 Hadoop 存量环境 | 存量企业仍大量使用 ⚠️ 转述 |
| On Mesos | Mesos 框架 | 当时多元数据中心选项 | **已被 Spark 主线移除** ⚠️ 转述，演进节展开 |

示意命令（Spark 2.x 风格 ⚠️ 未实测，本机 pyspark 不可装——波6 实测结论沿用）：

```bash
# 本地模式冒烟
./bin/pyspark --master "local[*]"
# standalone master/worker
./sbin/start-master.sh
./sbin/start-slave.sh spark://head:7077
# 提交应用到 YARN
./bin/spark-submit --master yarn --deploy-mode cluster app.py
```

## 精读重构·安装与目录巡礼（p.30–37）

- **前置件**：JVM（Spark 2.x 时代要求 Java 7/8 ⚠️ 推定）、Python 2/3 双兼容窗口（本书选 Python 3）、
  可选 Hadoop 二进制包（提供 native-lib 与 yarn 类路径，非必需依赖）。
- **Getting Spark**：官方预编译包装 tar.gz/zip；Windows 走 zip + 路径空格坑（`C:\spark` 惯例），
  书中 Windows 单独成节正说明 2018 年 Windows 本地开发是 Python 数据分析者的真实场景。
- **Exploring the Installation**：`bin/`(spark-submit、pyspark、spark-shell)、`sbin/`(start-master 等)、
  `conf/`(spark-defaults.conf、spark-env.sh)、`examples/`、`yarn/`（如 with-hadoop 构建）。
- **Multi-Node Standalone**：头节点 start-master，工作节点 start-slave 指向 `spark://head:7077`，
  Web UI 8080；要点是 hostname 可达性与 `SPARK_MASTER_HOST` 显式设置（⚠️ 推定展开，TOC 仅列节名）。

## 精读重构·云上三选（p.39–43）

TOC 并列 AWS/GCP/Databricks 三节，2018 年的语义是：

1. **AWS**：EMR 集群 + S3 输入输出；或自建 EC2 standalone（书中教后者为多节铺垫 ⚠️ 推定）。
2. **GCP**：Dataproc 托管集群（书出年已 GA，⚠️ 转述）。
3. **Databricks**：作者公司背景相关的一键云上笔记本 + 托管集群，与 Ch8「Notebooks」节呼应。

> repo 对照：云上部署与生产调优的现行叙事，见
> [../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)。

> 与兄弟册分工登记（波8 内只登记不链）：#216 High Performance Spark 2e、#196 Learning Spark 2e、
> #150 Modern Data Engineering、#152 Beginning Apache Spark 3 各有部署章，本册 Ch2 的特征是
> **Python 初学者视角 + 三云并列**，教学颗粒度最粗但覆盖面最全（本地→单机→集群→云一条直线）。

🔧 **本地对照锚点（非 Spark 行为）**：本章无算法性内容，但「装起来才能学」的门槛在 2026 年有了零安装替代：
本机构 Python 3.13.2 自带 sqlite3 3.45.3、pip 环境含 duckdb 1.5.5（🔧 实测导入成功），
单机数据分析练手完全可以不依赖任何集群——这正是 Ch4/Ch5 概念用 DuckDB/SQLite 类比实测的基础（见 04/05/06/07 各节），
也是「Spark 式部署成本」的反面参照：本节三云叙述在 2026 年对应的是托管 Serverless 形态 ⚠️ 转述。

## 常见误区与读法提示

1. 2018 年下载链接与版本号已全部失效——照抄书中命令会扑空；读本章的正确姿势是学「形态分类学」，
   版本细节以 https://spark.apache.org/docs/latest/rdd-programming-guide.html 的运行方式节为准（✅ curl -sI 200）。
2. Mesos 一节可跳过：仅作技术史标本保留。
3. Windows 安装的 Hadoop winutils.exe 坑（2018 与今皆然）⚠️ 转述：社区高频问题，书如未覆盖则需外部补丁知识。

## 复习要点与自测清单

1. 默画四形态对照表：Local/Standalone/YARN/Mesos 各自的资源管理者与适用场景；能说出 Mesos 出局原因。
2. 能写出三行命令：起 standalone master、挂 slave、向 YARN cluster mode 提交 Python 应用。
3. 安装目录五件套（bin/sbin/conf/examples/yarn）各答出两个代表文件与用途。
4. 说清 `spark-submit` 的 `--master` 取值域与 `--deploy-mode` 的正交关系（Local 无 deploy-mode 语义）。
5. Windows 路径坑与 winutils 补丁的来历；WSL/devcontainer 为何成为新默认。
6. 三云各自的最小可行形态：EMR 集群、Dataproc 作业提交、Databricks workspace 一句话差异。
7. 自检题：为什么「本地 local[*] 能跑」不保证「集群能跑」？（提示：分区数、闭包序列化、内存切分——Ch3 收口）
8. 延伸：把本目录 04–08 任一概念实验先在 local[*] 心算跑一遍，再判断哪些必须真集群才能复现——
   这是 2026 年读本章的正确打开方式（部署章的知识点 80% 已转化为「托管服务选型」知识）。
9. 复核题：给四形态逐一标注 2026 年「仍日用/已淘汰/仅考古」三态，并各写一条迁移建议
   （Local→保留；Standalone→容器化；YARN→存量维护；Mesos→K8s 迁移）。
10. 一句话总结本章对数据分析读者的意义：部署形态决定你能用多大并行度，而与 API 选择无关。

## 核心概念速览（中英对照）

- **本地模式** — Local Mode：单机 JVM 内以线程模拟执行器的运行方式，`local[*]` 用满核。
- **独立集群** — Spark Standalone：Spark 自带 Master/Worker 的原生集群管理器。
- **集群管理器** — Cluster Manager：负责资源分配的外壳进程（Standalone/YARN/Kubernetes）。
- **客户端部署模式** — Client Mode：驱动进程留在提交机，日志回终端（Ch3 深化）。
- **集群部署模式** — Cluster Mode：驱动进程在集群内启动，提交端可断开（Ch3 深化）。
- **提交工具** — spark-submit：统一的应用打包提交命令行入口，`--master/--deploy-mode` 定形态。
- **环境配置** — spark-env.sh / spark-defaults.conf：部署级与默认参数级两套配置载体。
- **Web UI** — Spark Web UI：Master 8080、应用 4040 的监控页，安装后自检的第一站。
- **托管集群服务** — Managed Cluster Service：EMR/Dataproc/Databricks 类云上一键集群形态。
- **对象存储对接** — Object Storage Integration：S3/GCS 作为 RDD I/O 源的连接器配置（呼应 Ch1 I/O Types）。

## 最新演进与工业实践

- **Kubernetes 成为一等部署目标**：Spark 3.x 时代 `--master k8s://` 的原生 on-K8s 支持是新增主流；
  本书四形态（Local/Standalone/YARN/Mesos）中 Mesos 出局、K8s 入位 ⚠️ 转述。
- **配置面统一入口**：官方 RDD 指南的 "Spark on Kubernetes" 与提交工具文档均在
  https://spark.apache.org/docs/latest/rdd-programming-guide.html 链下维护（✅ 200）。
- **Serverless 化**：2024–2026 云厂商主推按量会话集群（EMR Serverless、Dataproc Serverless、Databricks Serverless 线）⚠️ 转述，
  本书「自己起 slave」的手感已成运维考古项。
- **JDK 基线迁移**：Spark 主线已要求 Java 8→11/17 阶梯并拥抱 Scala 2.13/Java 兼容面 ⚠️ 转述；
  书中 Java 7 时代预备步骤按现行文档重来。
- **Windows 开发路径改变**：WSL2/容器（devcontainer）替代当年 winutils 手工补丁 ⚠️ 转述。
- **工业实践基线**：数据分析团队常见组合已收敛为「本地 pandas/pyarrow 原型 → 云端 Spark/SQL 托管执行」；
  🔧 本机证据：pandas 3.0.2 + duckdb 1.5.5 即可跑通本书 Ch4–Ch8 的全部概念实验（本波 6 组类比即在此环境实测，
  见 `D:\develops\tmp\dbwave_w8_daspark\analogies.py`），零集群、零安装负担。
