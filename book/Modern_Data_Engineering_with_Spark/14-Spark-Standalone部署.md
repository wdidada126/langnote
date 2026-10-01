# 14 — Spark Standalone 关键任务部署（Deploying Mission-Critical Spark Applications on Spark Standalone）

> 《Modern Data Engineering with Apache Spark》第 14 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_14` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 Spark 集群管理官方文档主题域反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

deployment 双线之一（Standalone 篇）：把 2–13 章在 local 模式里打磨的「关键任务应用」放上多机集群。选 Standalone 而非 YARN/Mesos 的动机与本书气质一致——**依赖最少、机制最透明**：不用先装 Hadoop 全家桶就能看懂资源协商、driver/executor 生命周期与容错全貌。它是 15 章 K8s 对照实验的「基线组」。

## 2. Standalone 架构件（⚠️ 按章题域重构，官方校核）

- **Master**：集群大脑，管 worker 注册、应用排队、资源分配；HA 走 ZooKeeper leader 选举或（3.4+/4.x 线）内部单节点元存储 ⚠️ 版本相关。
- **Worker**：每机一个，按 `SPARK_WORKER_CORES/MEMORY/INSTANCES` 切资源槽。
- **Driver/Executor**：`--deploy-mode cluster` 时 driver 落在 worker 槽内（集群托管 vs client 模式的本章分野）；executor 数/核/内存三参数组是资源规划的全部旋钮（Spark 4.x 的 `--properties-file`/内存模型细节以文档为准）。
- **提交链路**：spark-submit → REST/CLI → Master 调度 → worker 拉起容器——一条可背诵的时序线。
- ✅ 校核：集群总览 https://spark.apache.org/docs/latest/cluster-overview.html 与调度 https://spark.apache.org/docs/latest/job-scheduling.html（Standalone 节，2026-10 实测均 200）。

## 3. mission-critical 的集群侧清单（本章的工程灵魂，⚠️ 重构）

1. **应用 HA**：Master leader 切换不丢应用状态；driver 失败重启策略（`spark.restart.on.user.class.error` 类细节 ⚠️ 以文档为准）。
2. **队列与公平**：`--queue`/权重配置，多团队共享集群的隔离雏形。
3. **动态回收**：`spark.dynamicAllocation`（Shuffle Tracking 支持线）与 Standalone 的适配度——历史上有版本限制，需校核 ⚠️。
4. **观测面**：Master/Worker Web UI(8080/8081)、Application UI(4040)、History Server(event log 集中读)——长跑流的仪表盘前件（接 13 章监控）。
5. **依赖分发**：`--jars/--py-files` 与 worker 侧的 Python 环境一致性——Standalone 的经典运维痛点（容器化在 15 章正是为治它）。
6. **存储挂载**：各 worker 同路径可见的检查点目录——NFS/对象存储的部署假设要在本章显形（与 3/10 章 checkpoint 线会师）。

## 4. 资源规划算术（工程册给得出公式的部分，⚠️ 重构）

- executor 数 = 集群空闲槽 ÷ 单 executor 槽；cores 与并行度（任务数、`shuffle.partitions`）的配比原则。
- 内存三分：executor 堆内（计算+存储）/ 堆外开销（`memoryOverhead`）/ 集群预留——一条容量线三个敌人。
- shuffle 局部性：`spark.local.dir` 落点与 SSD 的关系；RSS 合并模式（MRS）的磁盘预算 ⚠️ 以文档为准。
- 与 7 章管道互动：并发管道数 × 峰值资源 = 集群规模——「容量规划=乘法口诀」的工程诚实。
- 🔧 概念类比注：分区并行收益可用本机 DuckDB/SQLite 观测「单线程 vs 并行聚合」的粗略差异，但 Standalone 的**槽位仲裁/排队行为**不可在单机复现，本波不做数字类比（登记于 00 §7 之外的降级说明；Spark 数值一律 ⚠️ 转述）。

## 5. 版本现场：3.3–3.5 移除线 → 4.x（⚠️ 转述 + 官方校核）

- **Mesos/YARN 之外的调度器收敛**：Standalone 幸存且持续演进（REST 提交、内部元数据存储替代部分 ZK 依赖）——本书的 ZK-HA 步骤在 Spark 4.x 可能整体过时，部署前查 ✅ https://spark.apache.org/docs/latest/job-scheduling.html。
- **Scala 2.12→2.13 / Java 8→17 基线迁移**：集群侧 JVM 版本统一成为部署前置任务（与 2 章 JDK 坑呼应）。
- **历史服务器形态**：单节点 History Server 与事件日志滚动策略文档化。
- 对位权威展开（性能线）：[../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)；调优纵深在波8兄弟 #216 High Performance Spark 2e（登记不链，见 00 §4.1）。

## 6. 流作业的部署特殊性（副题在此章的落点，⚠️ 重构）

- 长跑 `awaitTermination` 进程 = 集群里「不会自己死的 driver」——重启策略、优雅停机（`stop()` 前的水位收尾）都要专门设计。
- checkpoint 目录=集群共享存储的强依赖（10 章）；恢复演练应入验收清单：kill driver → 同 checkpointLocation 重提 → 验证 offset 续读（Kafka 场景接 11 章）。
- 升级路径 = 新查询 + 元数据迁移（plan 不兼容），与 K8s 蓝绿发布在 15 章续谈。
- Airflow（8 章）视角：编排器对 Standalone 提交是「点火器」，HA 由集群层负责——职责分界线的画法是本章的组织贡献。

## 7. 校读清单

- 作者搭了几台「伪分布式」（单机多 worker）？——hands-on 册的常见折中。
- History Server 是否配置？——观测面的成熟度试纸。
- 动态分配在本章是否被尝试并被限制劝退？——2022 语境高频剧情（⚠️）。

## 8. 配置文件骨架（概念导引，⚠️ 非原书清单，参数名以文档为终裁）

```text
# conf/spark-defaults.conf（集群级默认，提交侧可覆盖）
spark.master            spark://h1:7077
spark.eventLog.enabled  true
spark.eventLog.dir      nfs://mount/spark-logs        # History Server 的读源
spark.history.fs.logDirectory  nfs://mount/spark-logs
# conf/spark-env.sh（每机进程环境）
SPARK_LOCAL_IP=...  SPARK_WORKER_CORES=8  SPARK_WORKER_MEMORY=16g
SPARK_WORKER_INSTANCES=2                     # 单机多 executor 的槽位切分
# sbin/start-or-stop-all.sh 拓扑：h1=master+history, w1..w3=workers
```

- 审计点一：默认值放集群还是放提交脚本？——「mission-critical 应用自带配置、集群只给地板」的分工原则（⚠️ 目录立场）。
- 审计点二：事件日志目录的保留策略与轮转——History Server 考古线的运维债利息（§3 清单 4）。

## 9. 恢复演练脚本卡（§6 的落地台本，⚠️ 转述设计，本机不可执行）

1. 布景：3 worker、一长跑 SS 查询（Kafka 源、JDBC sink、NFS 上的 checkpoint）。
2. 断言基线：记录当前 offset、sink 表行数与 `max(ver)`。
3. 杀 driver（`kill -9`）→ Master 重启策略拉起/人工重提 → 断言 offset 单调续进、无重复键。
4. 升级剧本：改查询定义 → 新 checkpointLocation 冷启 → 双跑对账一周 → 切换/回滚预案（10 章兼容性线的集群版）。
5. 演练频率：季度列入 oncall 日历——「没演练过的 HA 等于没有」的工程宪法（⚠️ 目录观点）。

## 10. 校读问答（五问五答）

- **Q：2022 还教 Standalone 是不是落伍？** A：恰是本书优点——把调度抽象的裸架构看一遍，K8s/YARN 的隐喻学起来才有底片（15 章对照组）。
- **Q：MESOS/YARN 在本书位置？** A：⚠️ 预期仅目录级提及；本波云仓/托管诸册（#214/#158 登记不链）承担另一侧现实。
- **Q：动态分配到底开不开？** A：版本适配 + shuffle 服务依赖决定；Standalone 上保守不开、K8s 上原生自然（§5/15 章对照，⚠️ 以文档终裁）。
- **Q：本章与 8 章重叠吗？** A：不——Airflow 管「何时点火」，本章管「火塘怎么搭」；提交参数是唯一交界面（§6 第 4 条）。
- **Q：资源算术的下一步？** A：压测校准——§4 公式给初值，实测反馈调 `shuffle.partitions` 与 executor 尺寸（调优纵深：波8 #216 登记不链）。

## 11. 章末锚点卡（速记三线，⚠️ 目录制）

- 一条主线：Standalone 的透明性=教学红利——槽位/排队/仲裁三件事在 8080 页面上一眼见底，K8s 学完才懂它省掉了什么。
- 一条警戒线：依赖分发与环境一致性（§3 清单 5）——本章半数事故在此；「镜像治百病」的判断留给 15 章兑现。
- 一条接口线：checkpoint 走 NFS（3/10 章）、提交走 Airflow（8 章）、长跑监控走 13 章三指标——本章是全书平台的「地面真值」层。
- 记忆钩：恢复演练台本（§9）五步——没演练的 HA 等于没有；容量乘法（§4）——规划是口诀不是玄学。
- 历史位：Mesos 消亡/YARN 存量化的时代（✅ job-scheduling 文档口径），Standalone 反而成了「最后一个自建集群」的活标本。

## 观读三复（复核小记）

- 复核点一：§8 配置块刻意用「概念骨架」措辞——参数级考古需对照当期 ✅ job-scheduling/cluster-overview 双文档。
- 复核点二：流作业「不会自己死的 driver」是本章与 10 章的接口句——重启策略与优雅收尾的设计母题。
- 复核点三：ZK-HA→内部元存储的路线变化（§5）让本书部署节部分过时——⚠️ 迁移前先查文档再动手。
- 教学位vs生产位：全章立场「无菌标本优先」——读 15 章前保持此心态，别拿 Standalone 直接对标生产平台。
- 台账：本章无 🔧 实验（集群行为单机不可复现），类比仅 §4 注一条——口径合规（00 §7 四组无 Spark 数字冒充）。

## 核心概念速览（中英对照）

- **Standalone Master/Worker** — Standalone Cluster：Spark 原生集群管理器，透明资源仲裁的教学首选。
- **deploy-mode cluster/client** — Deploy Mode：driver 落集群内还是提交机上的分野。
- **资源槽** — Resource Slot：worker 按核/内存切分、可多实例化 executor 的容器额度。
- **动态分配** — Dynamic Allocation：按积压伸缩 executor，受 shuffle 追踪支持牵制。
- **History Server** — History Server：集中读事件日志的观测面，UI 过期后的考古层。
- **事件日志** — Event Log：UI/审计/排错的元数据源（3/10 章 checkpoint 的兄弟件）。
- **队列权重** — Scheduling Queue/Fairness：多应用共享的仲裁策略雏形。
- **依赖分发** — Dependency Distribution：jars/py-files 与 worker 环境一致性之痛。
- **恢复演练** — Recovery Drill：kill driver 验证 offset×checkpoint 续读的验收动作（§6）。
- **容量乘法** — Capacity Arithmetic：管道并发×峰值槽位的朴素规划法（§4）。

## 最新演进与工业实践

- **Spark 4.x 的 Standalone 现状** ✅ https://spark.apache.org/docs/latest/：仍是官方一等调度器且持续修复增强；但工业新增部署明显向 K8s/云托管倾斜，Standalone 的主场退守「自建、透明、教学与中小规模」（⚠️ 观察性陈述）。
- **ZK 依赖松动**：内部元数据存储替代部分 ZooKeeper 场景（版本线细节以 job-scheduling 文档为终裁 ⚠️），本书 ZK-HA 配方按需替换。
- **云托管对照**：EMR/Dataproc 的 Spark 运行时 + K8s 原生（见 15 章）是 2026 多数团队的 mission-critical 现实；本章价值转为「理解调度抽象的无菌标本」（⚠️ 目录判断）。
- **观测栈升级**：History Server + Prometheus/OTel 指标抓取（spark-exporter 类）替代纯 UI 巡检（⚠️ 观察性陈述）。
- **不可实测声明**：本目录环境无 JVM/Spark（波6 实证），本章所有集群行为均为官方文档转述 + ⚠️；类比实验仅限单机可复现的语义投影（00 §7 四组，无 Spark 数字冒充）。
