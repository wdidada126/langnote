# 15 — Kubernetes 关键任务部署（Deploying Mission-Critical Spark Applications on Kubernetes）

> 《Modern Data Engineering with Apache Spark》第 15 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_15` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 Spark on K8s 官方文档主题域反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

全书终点：把 mission-critical 应用放上 Kubernetes——与 14 章 Standalone 互为对照组，回答「云原生时代 Spark 进程如何被编排」。K8s 带来的三件大礼：镜像统一依赖（治 14 章分发之痛）、声明式 API 与 operator 托管（治提交/升级之痛）、弹性调度与现有平台合流（治容量孤岛之痛）。本书以此章收束「本地平台 → 可投产平台」的弧线。

## 2. 部署机制栈（⚠️ 按章题域重构，官方校核）

- **镜像**：`bin/build-image.sh` 产出含 Spark 发行版的 driver/executor 基础镜像；业务依赖再叠一层——两镜像策略是工程册惯例（⚠️ 推定书中如此）。
- **提交形态**：`--master k8s://https://<api-server>` 的 spark-submit；`driver/podTemplate` YAML 声明资源、节点亲和、污点容忍。
- **executor 生命周期**：driver 直接向 K8s API 申请 executor pod（Spark 原生线），**无需常驻集群管理器**——与 Standalone 的本质架构差。
- **动态分配**：`spark.dynamicAllocation.enabled` + shuffle 追踪（3.x+ 支持 EC 驱逐安全线，细节 ⚠️ 以文档为准）。
- **历史服务器**：事件日志写持久卷/对象存储，History Server 独立部署续读（14 章观测线的 K8s 化）。
- ✅ 校核：https://spark.apache.org/docs/latest/running-on-kubernetes.html（2026-10 实测 200）。

## 3. Spark Operator：从脚本到声明式 CRD

- **Kubeflow Spark Operator**（社区主线路）：`SparkApplication` CRD 把提交参数变成 YAML 对象——GitOps 可版本化的前提；✅ 项目入口 https://github.com/kubeflow/spark-operator（实测 200）、K8s operator 概念 ✅ https://kubernetes.io/docs/concepts/extend-kubernetes/operator/。
- **作业形态**：批=Job 语义（跑完即散）、流=Deployment/长跑 CRD + 重启策略——副题「关键任务流」在 K8s 的落点。
- **升级发布**：镜像 tag 滚动=蓝绿/金丝雀的可能；对比 14 章「手改提交脚本」的原始感。
- **DAG 视角回看 8 章**：Airflow 可经 operator/K8s 原生 API 提交 Spark——编排层与运行层的云原生接缝（⚠️ 书中是否串线未知）。

## 4. 资源与治理的现实面（工程册责任段，⚠️ 重构）

- requests/limits 与 Spark 内存模型的**双层语义陷阱**：JVM 堆配了不等于 pod 给够——`memoryOverhead` 进 limits 的换算表（14 章容量算术的 K8s 续篇）。
- executor 驱逐防护：priorityClass、PDB、spot 节点容忍——长跑流作业的生存学。
- 命名空间配额与多团队：`batch`/`streaming` 分池，水位线/新鲜度 SLA 映射到资源池策略（09–13 章语义的平台化）。
- Shuffle：K8s 上临时卷→远端服务化 shuffle（ celeborn/Magpie 类）的选项 ⚠️ 观察性补充，非本书。
- 🔧 概念类比（登记不实测）：pod 重启≈微批重放，二者都要求「应用自身幂等+状态外置」——10/11 章语义的平台侧回声；K8s 编排行为本机不可跑，本组不做实验、维持 ⚠️（口径同 00 §7）。

## 5. 与 repo/生态对位

- 盘上湖仓×K8s 语境：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)（平台合流章）、[../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)（表格式与 K8s 作业解耦）。
- TDG 部署对照（YARN 时代叙事）：[../Spark_The_Definitive_Guide/10-生产部署与性能调优.md](../Spark_The_Definitive_Guide/10-生产部署与性能调优.md)。
- 编排器侧：Airflow 的 KubernetesPodOperator 生态（8 章演进线，官方 ✅ https://airflow.apache.org/docs/）。

## 6. 校读清单

- 作者用什么本地 K8s（minikube/kind/Docker Desktop）？——决定步骤的今日可复现性（2026 多已换版本）。
- 是否部署了 operator 还是仅原生提交？——CRD 化的深度试纸。
- 检查点/事件日志持久卷怎么挂？——10/14 章存储线在 K8s 的兑现处。

## 8. SparkApplication CRD 骨架（概念导引，⚠️ 字段以 operator 版本文档为终裁）

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata: {name: agg-stream, namespace: spark}
spec:
  type: Scala
  mode: cluster
  image: registry.local/spark-app:1.2.0        # §2 两级镜像的第二级
  mainApplicationFile: s3a://jobs/agg.jar
  sparkVersion: "3.2.1"
  restartPolicy: {onFailureCount: 3}           # mission-critical 的声明式落点
  scheduler: {schedulingPolicy: {queues: [prod-stream]}}
  driver: {cores: 1, memory: 2g, serviceAccount: spark}
  executor: {cores: 2, instances: 4, memory: 4g}
  dynamicAllocation: {enabled: true, maxExecutors: 16}
```

- 读法：每一块都能映射回前章——image→依赖分发（14 章痛点终结处）、restartPolicy→§6 长跑容错、动态分配→§4 双层内存语义、队列→多团队治理。
- GitOps 注：此 YAML 进 Git 即获得 14 章提交脚本永远没有的评审/回滚能力（§3 声明式价值实证）。

## 9. Standalone ⇄ K8s 对照表（两章合订的收束件，⚠️ 目录提炼）

| 维度 | Standalone（14 章） | K8s（本章） |
|------|---------------------|-------------|
| 资源仲裁者 | Master 常驻进程 | kubelet/apiserver 平台全体 |
|  executor 生命周期 | worker 槽内拉起容器 | driver 直申 pod，用毕即焚 |
| 依赖一致性 | jars/py-files + 环境自觉 | 镜像=唯一事实 ✅ 治痛点 |
| 提交面 | spark-submit/REST | CRD/GitOps 声明对象 |
| 弹性 | 静态 worker 池 | 节点/调度器层自动伸缩 |
| 观测 | 8080/4040 + History | 上述 + kubectl/事件/Prom 全家 |
| 学习曲线 | 一小时看懂全部机制 | 要先养一个集群 🐾 |
| 教学定位 | 无菌标本 | 手术现场 |

- 收束判断：两章并置本身就是本书的部署观——**先透明后抽象**；顺序倒过来学，读者会把 K8s 当黑魔法（⚠️ 目录解读立场）。

## 10. 校读问答（五问五答）

- **Q：本地 K8s 玩具环境还值得搭吗？** A：为「跑通声明流」值得（kind/minikube 半天）；为生产学习不值得——参数面与托管集群差异大（⚠️）。
- **Q：operator 与原生提交谁先学？** A：先原生理清 pod 生成机制，再 operator 学声明式封装——与 14→15 章同理的分层（§3）。
- **Q：Connect 会取代本章提交面吗？** A：客户端-服务器化让「作业常驻远端、笔记本瘦提交」成为新形态；本章的 pod 机制仍是服务端基础（⚠️ 演进观察）。
- **Q：shuffle 持久化在 K8s 怎么办？** A：临时卷→Celeborn 类远端服务（§4 注），这是与 Standalone「worker 本地盘」最大的体验差（⚠️ 转述）。
- **Q：全书读完后部署线带走的三件事？** A：幂等的应用（7/10/11）+ 版本化的配置与镜像（8/14/15）+ 演练过的恢复（13/14）——mission-critical 的三角定义（⚠️ 目录总结）。

## 11. 章末锚点卡（速记三线，⚠️ 目录制）

- 一条主线：K8s 化=把「集群管理」外包给一个你已经在运维的东西——Spark 特有的只剩镜像与 CRD 两块。
- 一条警戒线：双层内存语义（§4 条 1）——JVM 配平不等于 pod 配平，limits 杀 driver 的日志 2026 仍刷屏。
- 一条接口线：CRD 的 restartPolicy 是 13 章状态恢复的平台侧镜像；事件日志进 S3 是 14 章 History 线的托管版；YAML 入 Git 是 8 章声明观的终点。
- 记忆钩：对照表（§9）八行——「14 章赢在理解、15 章赢在生产」一句收束全书部署线。
- 全书收束：五环（可重复/可编排/可容错/可靠消息/可部署）至此闭锁——01 章画的圈在最后一章画上句点，mission-critical 不是形容词而是清单。

## 观读三复（复核小记）

- 复核点一：YAML 骨架字段以 ✅ kubeflow/spark-operator 当期 CRD 文档为终裁（GitHub 实测 200）——版本漂移区，抄写前核对。
- 复核点二：「executor pod 用毕即焚」与 13 章 RocksDB 状态的「本地目录易失」构成 K8s 流作业的核心矛盾——远端 shuffle/状态后端为其解，演进节已登记。
- 复核点三：对照表 §9 是全波 14 本中「部署双章」的唯一成对样本——兄弟册 #216/#196 诸书未给此结构（登记）。
- 收束自检：五环（01 §4）→ 14/15 章两章合卷即闭环——副题 mission-critical 在结构上兑现，本书完成度最高点。
- 全书最后一读：15 章之后回翻 09——「流=无界表」的隐喻此时应当读出它的全部价格。

## 核心概念速览（中英对照）

- **SparkApplication CRD** — SparkApplication CRD：operator 的声明式作业对象，GitOps 单元。
- **podTemplate** — Pod Template：driver/executor pod 的 YAML 细配（资源/亲和/容忍）。
- **executor pod** — Executor Pod：由 driver 动态申请的执行容器，无常驻集群管理器。
- **镜像分层** — Image Layering：Spark 基础镜像+业务依赖镜像的两级构建。
- **动态分配（K8s）** — Dynamic Allocation on K8s：executor pod 随积压伸缩的弹性线。
- **驱逐防护** — Eviction Guard：priorityClass/PDB 对长跑作业的保命配置。
- **滚动发布** — Rolling Upgrade：以镜像 tag 为单位的蓝绿/金丝雀路径。
- **持久卷日志** — Persistent Event Log：History Server 续读的存储前提。
- **GitOps** — GitOps：声明式对象入 Git 的部署流水线形态（→ 演进）。
- **平台合流** — Platform Convergence：Spark 作业与 K8s 原生工作负载同池调度（§4）。

## 最新演进与工业实践

- **Spark 4.x on K8s**：资源/绑定 API 与镜像构建持续打磨，Java 17 基线、Connect 客户端使「K8s 服务端 + 瘦客户端」形态更顺（⚠️ 转述；✅ https://spark.apache.org/docs/latest/running-on-kubernetes.html 实测 200）。
- **operator 生态收敛**：Kubeflow Spark Operator 为社区主线（✅ GitHub 实测 200）；云厂商各出托管版（Databricks on K8s、EMR on EKS 类）——本书自建路径的教学价值高于生产复制价值（⚠️ 观察性陈述）。
- **2024–2026 生产主流**：新增 Spark 流批负载普遍落在 K8s 或云托管运行时；Standalone 维持自建/边缘场景——14/15 章对照的今日答案是「15 章赢在生产，14 章赢在理解」（⚠️ 目录判断）。
- **远端 shuffle 服务化**：Celeborn 类项目解决 K8s 上 executor 易失与 shuffle 持久的矛盾，进入增量计算/湖仓写入链路（⚠️ 观察性陈述，术语以项目文档为终裁）。
- **平台工程合流**：Spark 作业纳入通用平台工程流水线（模板库、策略即代码、成本观测），本书「为 Spark 建集群」的叙事被「平台吃下 Spark」取代——data engineer 的部署技能转向「会声明、会观测、会预算」（⚠️ 观察性陈述）。
