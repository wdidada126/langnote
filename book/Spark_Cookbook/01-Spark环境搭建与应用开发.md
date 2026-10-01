# 01 · Spark 环境搭建与应用开发（原书 Ch1 Getting Started with Apache Spark + Ch2 Developing Applications with Spark）

> 精读重构笔记，非原书文本。目录取证：微信读书官方电子版目录快照（✅ 实抓）；Spark 引擎行为本机不可实测 → 一律 ⚠️ 转述。
> 合并口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §3：Ch1/Ch2 同属「环境与工具链操作域」。

## 1. 章域定位

2015 年的 Spark 上手第一问不是 API，而是**怎么把集群跑起来、怎么把 IDE 配起来**。Rishi Yadav 把这两件事写成 13 个食谱，覆盖从单机玩具集群到 Mesos/YARN 生产编排的完整梯度。今天回看，这一章是「Spark 1.x 时代运维复杂度」的化石记录：Spark 1.6 之后 standalone 模式边缘化、Spark 2.4 后 Mesos 支持废弃、Spark 3.x 后 Mesos 移除，而 EC2 食谱的继任者是 EMR/Databricks，本地开发从「Eclipse+SBT 手工配置」进化到「`pip install pyspark` + Databricks Community Edition」——这些落差正是本目录 00 定位节强调的「先建 3.x 坐标系再考古」的原因。

## 2. 食谱地图（Ch1 + Ch2，题名为官方目录逐字转录）

| # | 食谱 | 问题域 | 2026 等价物 |
|---|---|---|---|
| 1.1 | Installing Spark from binaries | 二进制包解压即用 | `pip install pyspark` / 发行版镜像 ⚠️ |
| 1.2 | Building the Spark source code with Maven | 源码定制构建 | sbt/maven 仍在，多走 CI 出镜像 ⚠️ |
| 1.3 | Launching Spark on Amazon EC2 | 手工起云上集群 | EMR / Glue / Databricks 托管 ⚠️ |
| 1.4 | Deploying on a cluster in standalone mode | 自带 master/worker | 基本淘汰 ⚠️ |
| 1.5 | Deploying on a cluster with Mesos | Mesos 细粒度/粗粒度 | 官方已移除支持 ⚠️ |
| 1.6 | Deploying on a cluster with YARN | Hadoop 生态主路径 | 仍是存量大头 ⚠️ |
| 1.7 | Using Tachyon as an off-heap storage layer | 跨应用内存共享层 | Tachyon 更名 Alluxio，转向云原生缓存 ⚠️ |
| 2.1 | Exploring the Spark shell | spark-shell/scala REPL 试错 | pyspark shell / Scala REPL 同构 ⚠️ |
| 2.2-2.5 | Eclipse/IntelliJ × Maven/SBT 四组合 | 工程骨架与依赖管理 | IDE 收敛到 IntelliJ/VSCode，SBT 仅 Scala 工程 ⚠️ |

## 3. 精读块一：部署模式的选择树（Ch1 的隐含主线）

**问题**：单机、云上、集群三档怎么升？
**配方骨架**：binary 解压 → `spark-env.sh` 配 master/worker → `spark-submit` 打 standalone；要复用 Hadoop 资源就 `--master yarn`；要跨租户编排才上 Mesos。
**评注 ⚠️**：食谱把三种集群管理器并列是 1.x 世界观；2.x 起 YARN/K8s 二分，Mesos 出局。Tachyon 食谱是本书最有「时代切片」价值的一题——堆外共享 RDD 的诉求后来由「对象存储 + 湖仓格式」路线接走（本目录 02 章、[../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md) 展开）。
**坑**：standalone 的 web UI 端口、worker 内存与 `spark.executor.memory` 的账目关系，当年无数读者在 log4j 与 GC 抖动里打转——这类「配方没写的隐性成本」正是食谱体裁的通病，读书时要主动补。

## 4. 精读块二：IDE × 构建工具四象限（Ch2）

**问题**：从 spark-shell 原型到可提交 jar 的工程化一跃。
**配方骨架**：Eclipse/IntelliJ + Maven/SBT 各给一套最小工程：`provided` 作用域的 spark-core、`spark-submit --class` 指主类。
**评注 ⚠️**：Maven vs SBT 之争当年是 Scala 社区身份政治；Python 用户 2015 年只能走 `spark-submit` 脚本打包（本书默认 Scala 视角，Python 食谱占比极低——这是它与后来 Learning Spark 系教材的关键差异）。Scala 2.10/2.11 ABI 对配是当年第一大坑。
**与 repo 对照**：Scala 语言底座见 [../bigdata/06-Scala函数式与集合编程.md](../bigdata/06-Scala函数式与集合编程.md)；执行域概念预演见 [../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md)。

## 5. 🔧 类比实验说明

本章食谱全部是「起集群/配 IDE」类操作，SQL 引擎无可类比面（DuckDB/SQLite 单机嵌入式，不存在集群编排语义），故本章不设 🔧 组；Spark 引擎行为按 00 §7 声明一律 ⚠️ 转述。类比实验 8 组的完整口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §7。

## 6. 互链清单

- 上行主参照：[../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md](../Spark_The_Definitive_Guide/01-Spark入门与架构巡礼.md)、[../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)
- 中文底座：[../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md)、[../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)
- 同题教材防混：[../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)（传智教材含环境章，教学型叙述 vs 本章食谱型）
- 系列索引：[../分布式系列·总索引.md](../分布式系列·总索引.md)

## 7. 配方骨架速查（考古重构，⚠️ 转述，语法按 1.x 惯例）

- **1.1 二进制安装**：下载 spark-1.5.x-bin-hadoop2.4 → 解压 → `conf/spark-env.sh.template` 复制为 spark-env.sh → `./sbin/start-master.sh` 与 `start-slave.sh <master-URL>` 起 standalone ⚠️。
- **1.2 Maven 源码构建**：`mvn -Pyarn -Phadoop-2.4 -DskipTests package` 后 `make-distribution.sh` 出自定义发行包 ⚠️。
- **1.3 EC2**：官方 spark-ec2 脚本一键拉起 master+worker 组，安全组放行 8080/4040 类端口后提交任务 ⚠️。
- **1.4-1.6 部署三谱系**：提交入口统一 `spark-submit --class <MainClass> --master <standalone-URL | mesos://... | yarn> <app.jar>`；YARN 下 `--deploy-mode cluster` 决定 driver 上节点 ⚠️。
- **1.7 Tachyon**：Tachyon master/worker 起停后跑示例类验证 RDD 跨应用共享，off-heap 配置联动 ⚠️（Alluxio 前身谱系）。
- **2.1 spark-shell**：`spark-shell --master local[4]` 里 sc 已就绪，try 完再落工程 ⚠️。
- **2.2-2.5 工程骨架**：Maven 依赖 spark-core 标 provided；SBT 同思路加 `libraryDependencies` + assembly 插件出提交 jar；IDE 侧导入即普通 JVM 工程 ⚠️。

## 8. 自测卡（合卷作答，8 问）

1. 为什么本地文件在 local 模式读得通、集群模式读不通？（答案要点见 §3：executor 侧路径可见性）
2. YARN 的 client 与 cluster 两种 deploy-mode 差在哪？（driver 落位与日志去向）
3. Mesos 谱系为何出局？（编排层被 K8s 接管，粗/细粒度模式双维护成本）
4. provided 作用域在 spark-submit 链条里防什么事故？（fat-jar 与集群自带库的版本冲突）
5. Tachyon 食谱解决什么问题？职责后来被谁接管？（跨应用共享 RDD 内存；对象存储+湖仓格式+云原生缓存）
6. Scala 2.10 工程连 2.11 构建的 Spark 会看到什么报错形态？（运行期 NoClassDefFound/序列化不匹配爆炸，提交不报错）
7. spark-shell 与工程化提交的边界在哪？（原型验证 vs 可复现产物）
8. 本章 7 个部署食谱的共同缺失是什么？（没有监控/日志/安全面，食谱体裁通病）

## 9. 小练习

1. 为 1.3-1.6 各写三行迁移笔记：2015 写法 / 2026 等价 / 消亡或存活原因。
2. 按 2.2-2.5 画出你团队的 IDE×构建工具四象限现状，标注哪一格已被 CI 吞并。
3. 用 1.7 素材给新人文档写一段：为什么中间数据现在落湖而不是塞共享缓存。

## 10. 延伸索引

- 部署模式历史落差：[../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)
- 资源与运维中文口径：[../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)
- Scala 语言底座：[../bigdata/06-Scala函数式与集合编程.md](../bigdata/06-Scala函数式与集合编程.md)
- 现代部署对照：[../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)

## 11. 易混点辟谣（快问快答）

- **误区：standalone 是 Spark 原生调度所以最快**——它只有调度没有隔离与多租户，生产早被 YARN/K8s 接管 ⚠️。
- **误区：装 Spark 等于装 Python 包**——`pip install pyspark` 的壳里跑的仍是 JVM 引擎，1.x 时代连壳都没有。
- **误区：EC2 拉起成功等于理解云部署**——安全组/凭证/弹性伸缩三件事食谱各只碰了一个角。
- **误区：SBT 更 Scala 所以选它**——构建工具是工程问题不是立场问题，选型由 CI 与仓库形态决定 ⚠️。
- **误区：Mesos 细粒度利用率高所以该活着**——编排层竞争是生态整体胜负，K8s 带着调度器外置+CRD 通吃 ⚠️。
- **误区：Tachyon 失败了**——它改名 Alluxio 转型湖缓存，产品存活、在计算栈的位置下移 ⚠️。
- **误区：源码构建是性能路线**——1.2 的真实动机是接私有 Hadoop patch；性能路线属于 12 章（本目录 08）。
- **误区：会 spark-submit 等于会部署**——提交只是最后一厘米，凭证/依赖/回滚三件事食谱都不写。

## 12. 读后行动清单

1. 把你当前项目翻译成 2015 写法（三 master 选一）并标注 2026 等价形态。
2. 用最熟 IDE 搭一个 provided 作用域最小骨架的伪流程（十行内），体会当年工程化门槛。
3. 整理一张 `spark-submit` 常用参数 1.x→3.x 对照表（--master/--deploy-mode/资源三族）⚠️。
4. 合卷复述：standalone/Mesos/YARN 三谱系淘汰路径与时间点，各一句话。
5. 写三行「本书 01 章 vs 传智教材环境章」差异卡片，练同题异书辨析眼力（对位 [../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)）。

## 核心概念速览（中英对照）

- **Spark 二进制发行版** — Spark binary distribution：预编译的发行包，解压配置即用，区别于源码构建。
- **集群管理器** — cluster manager：Spark 之上的资源编排层，1.x 三选项 standalone/Mesos/YARN。
- **spark-submit** — spark-submit：应用提交入口，携带 master URL、主类、依赖 jar 与资源配置。
- **provided 作用域** — provided scope：构建期编译依赖 spark 而运行期由集群提供的 Maven/SBT 依赖声明方式。
- **堆外存储层** — off-heap storage layer：把 RDD 数据放 JVM 堆外共享内存的中间层，Tachyon（后更名 Alluxio）是 2015 年代表方案。
- **宽/窄依赖** — wide/narrow dependency：本章尚未展开但 spark-shell 食谱已触及的执行图概念，详见本目录 03/08 章链接目标。
- **spark-shell** — Spark shell：交互式 REPL 原型环境，学习 Spark 的第一现场。
- **ABI 兼容** — binary compatibility：Scala 主次版本与 Spark 构建版本必须严格匹配，当年高频坑。
- **细粒度/粗粒度模式** — fine-grained/coarse-grained mode：Mesos 部署食谱给出的两种任务与资源耦合方式。
- **托管服务化** — managed service（本目录归纳词）：EC2 手工集群食谱在 2026 年的等价迁移方向（EMR/Glue/Databricks）。

## 最新演进与工业实践

- **部署面**：Spark 4.x 时代的集群管理只剩 YARN（存量）、Kubernetes（增量原生 `--master k8s://`）与托管平台三极；Mesos 支持自 3.0 移除，standalone 仅作开发用途——官方文档入口 ✅ https://spark.apache.org/docs/latest/index.html （2026-10-01 curl -sI 200）。
- **安装面**：`pip install pyspark` 使「装 Spark」从集群运维题降格为包管理题；本书 1.1-1.2 两食谱的日常价值随之归零，仅考古与私有 patch 场景保留。
- **Alluxio 线**：Tachyon→Alluxio 的演化验证了「计算侧缓存层」路线，2020s 被「存算分离 + 湖仓格式」吸收——Iceberg/Delta 目录快照缓存与对象存储加速承担了同等职责，对位可读 [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)。
- **IDE 面**：Databricks Repos/Git 集成与本地 devcontainers 取代了 Eclipse/SBT 手工四象限；Scala 侧 IntelliJ 一统，本书 2.2-2.5 四题合并为「一个 git 仓库 + CI」的当代形态。
- **工业实践**：2026 年新建 Spark 工作负载的事实标准是「云托管 + 容器化 + IaC 模板」，把本章 7 个部署食谱的决策树整体外包给了平台团队；个人开发者侧则退化为三行命令。此判断基于官方文档与主流云厂商公开文档 ⚠️（本波不可达源清单见 00 §2 声明，未逐条 curl 的厂商 URL 一律不引）。
