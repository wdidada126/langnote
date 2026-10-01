# 06 Synapse Spark — Synapse Spark（原书第 6 章，pp.119–150）

> 章题与页区间 ✅ Crossref 存款记录实抓（DOI 后缀 `_6`，pp.119–150）；章内小节 ⚠️ 推定（无公开样章），
> 按 learn.microsoft.com Spark 文档域主题组织。托管 Spark 不可本机实测，机制一律「⚠️ 转述 + ✅ URL
> （2026-10-02 验 200）」；本章无 🔧 组（本册 🔧 五组分布于 02/05/09 章，见
> [00](00-总览与阅读地图.md) §6）。

## 6.1 本章在全书中的位置

第 6 章（全书最长章之一，32 页）处理「湖上工程算力」：Synapse 的 Spark 不是外挂服务，而是被官方表述为
**原生集成（natively integrated）**的运行时——共享工作区存储、身份与监控 ✅
`spark/apache-spark-overview`。它与 05 章共同兑现 02 章的「一个湖两种算力」承诺，也是 09 章 Delta
分析的发动机。

## 6.2 池形态：从小型到专有的执行选项

- **小型/中型/大型固定尺寸池**：会话复用、秒级启动，适合交互式笔记本 ⚠️ ✅
  `spark/apache-spark-pool-configurations`；
- **自定义（专有）配置**：指定节点 SKU+executor  cores/内存档位，作业独占——重 ETL 的容量纪律同页 ⚠️；
- 关键工程账：会话复用省冷启动但共享内存池易被邻居作业挤压；专有池隔离但要自付启动时间——
  与 05 章 DWU 的「常驻 vs 拉起」同构 ⚠️。

## 6.3 笔记本与开发面

- Synapse Studio 内置 Jupyter 式笔记本 ✅ `spark/apache-spark-development-using-notebooks`：多语言核
  （PySpark/SparkSQL/Scala/C#/PySQL），**synapseutils 内置库与 %%spark 魔法**为 Synapse 方言 ⚠️；
- Apache SynapsePy（纯 Python 作业提交路径）与笔记本互为镜像——CI 里跑 .py、探索期跑 .ipynb
  ⚠️ 推定组织；
- 上游语言/运行时机理（RDD/DataFrame/shuffle/tungsten）不在此书纵深，盘上深读（在盘 ✅ 实名已验）：
  [../Beginning_Apache_Spark_3/00-总览与阅读地图.md](../Beginning_Apache_Spark_3/00-总览与阅读地图.md)、
  [../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md](../Advanced_Analytics_with_Spark_2e/00-总览与阅读地图.md)。

## 6.4 存储与表：湖目录即表目录

- 默认文件系统=工作区 ADLS Gen2 ✅ `spark/apache-spark-overview`（abfss 方案+托管身份鉴权）；
- **Delta Lake 一等公民** ✅ `spark/apache-spark-what-is-delta-lake`、`spark/apache-spark-delta-lake-overview`：
  ACID、时间旅行、模式演化——02 章表格式三角中 Delta 的产品落点；Iceberg/Hudi 经连接器可用
  （Hudi 教程页在文档域存在；盘上 Hudi/Iceberg 四册为格式纵深 ⚠️ 对位登记）；
- 库表元数据三层（内置/外部 metastore/DW 映射）：同一份 Delta 可被专用池以外部表、Serverless 以
  OPENROWSET 共读——**「一数据三引擎」的体验差主要在类型与方言**（DECIMAL 刻度/时区/二进制字面量 ⚠️
  `sql/query-delta-lake-format` 存在性引用）。

## 6.5 作业化与运维

- **Spark 作业定义（job definitions）**：把笔记本编译为可编排作业，由管道 Execute Spark Job 活动触发 ✅
  `spark/apache-spark-job-definitions`（07 章对接点）；
- **池级监控**：Spark UI 代理端点、Application 视图、指标导出 ✅
  `monitoring/how-to-monitor-spark-applications`；**Spark Advisor**（自动调参建议）✅
  `monitoring/apache-spark-advisor`；
- 包管理：workspace 级 pip/maven 包 ✅ `spark/apache-spark-manage-workspace-packages`；
  **文件挂载 API**（免拷贝访问外部容器）✅ `spark/synapse-file-mount-api`。

## 6.6 ML 面（书中 SynapseML 段落 ⚠️ 组织）

- SynapseML（开源项目线，文档旧称 MMLSpark）提供深度学习的 Spark 规模化接口 ✅
  `machine-learning/what-is-machine-learning`；
- 与 Azure ML 工作区打通（环境/注册/部署在 AML 侧）同页；本书仅点到「特征在仓、训练在池、服务在
  外部」的三段论 ⚠️ 转述；
- 认知服务连接器（文本分析/翻译等 REST 的 Spark 化）在该文档域存在 ✅ `spark/apache-spark-overview`
  的 ML 链接位（2026 年该能力面逐步收编到 Fabric/Foundry 语境，见演进节）。

## 6.7 常见误区

1. **「Spark 池=HDInsight 换皮」**——共享存储/身份/监控的集成深度完全不同，运维对象是「池+会话」
   而非集群 ⚠️。
2. **「笔记本作业可直接当生产管道」**——会话语义与重试语义不同；生产走作业定义+管道编排（6.5）⚠️。
3. **「有 Delta 就不需要仓表」**——高并发 BI 点查/严格 T-SQL 语义仍在专用池更强（05 章账本）⚠️。
4. **「Advisor 建议=真理」**——自适应建议基于样本作业形态，负载漂移时反向劣化；灰度验证后再固化 ⚠️。

## 6.8 SQL 面 vs Spark 面能力对照表（跨章索引 ⚠️ 推定组织，文档口径 ✅ 见 6.2–6.5 各引用页）

| 能力位 | SQL 面（专用/Serverless） | Spark 面 |
| --- | --- | --- |
| 交互探索 | TDS+SSMS/Studio 脚本 | 笔记本 cell 级反馈 |
| 复杂控制流 | T-SQL 过程化（弱） | DataFrame/UDF 原生 |
| ML 训练 | 受限（评分/向导） | SynapseML/MLlib 主场 |
| 格式广度 | Parquet/Delta/CSV/Json | 全 Hadoop 生态格式 |
| 语义严格度 | T-SQL 类型系统强 | Catalyst 类型宽松面 |
| BI 并发 | DirectQuery/导入均顺 | 经仓表或直读（性能面窄） |
| 成本形态 | DWU 或按处理量 | 核心时（池尺寸×时长） |

- 一句话裁决：**方言与类型系统的冲突点集中在 DECIMAL/时间戳/二进制字面量**——「一数据三引擎」
  共享文件不共享解释，跨面验数是迁移工程的固定工序 ⚠️（对位 02 章 §2.6 过渡三态）。
- 池尺寸档位、作业定义、Advisor 等运维工件只存在于 Spark 面（6.2/6.5），SQL 面的对应物是
  资源类/工作负载组（05 章 §5.8）——两套治理词表不要互抄 ⚠️。

## 核心概念速览（中英对照）

- **Spark 池** — Apache Spark Pool：工作区内托管的原生 Spark 运行时 ✅ apache-spark-overview。
- **会话复用** — Session Reuse：同尺寸池复用 JVM 省冷启动，交互式笔记本的吞吐来源 ⚠️。
- **专有配置** — Dedicated Size：自定义节点/executor 的独占形态，重 ETL 的隔离手段 ✅ pool-configurations。
- **SynapsePy** — Apache SynapsePy：笔记本之外的纯 Python 作业开发形态 ⚠️。
- **作业定义** — Spark Job Definition：笔记本→可编排批产物的编译路径 ✅ job-definitions。
- **abfss** — Azure Blob File System secure scheme：Spark 直读写 ADLS Gen2 的方案前缀 ✅。
- **Delta 一等公民** — Delta as native format：ACID/时间旅行/模式演化的湖表默认 ⚠️ ✅ what-is-delta。
- **SynapseML** — 深度学习规模化库：Spark 上的认知/ML 连接器族 ✅ machine-learning 文档域。
- **Spark Advisor** — 自动调参器：采样运行给配置建议的运维助手 ✅ apache-spark-advisor。
- **文件挂载 API** — File Mount API：将外部容器挂载到 driver/executor 免拷贝访问 ✅ synapse-file-mount-api。

## 最新演进与工业实践

2021→2026（URL 均 2026-10-02 验证 ✅ 200；描述 ⚠️ 转述）：

- **Fabric Spark 为现役形态**：Synapse Spark 的概念（池/会话/小-中-大尺寸/Delta 绑定）被 Fabric Spark
  原样承接并挂到 OneLake；旧 slug `spark/synapse-spark-pool` 已 404，现役概览为
  https://learn.microsoft.com/en-us/azure/synapse-analytics/spark/apache-spark-overview ✅（本册引用面
  全部重新验真）。
- **Azure Databricks 的分流位**：https://learn.microsoft.com/en-us/azure/databricks/introduction/ ✅——
  微软官方双栈口径下「Databricks=独立一线产品、Fabric/Synapse=平台内嵌引擎」；工业实践按治理边界选型 ⚠️。
- **表格式再平衡**：Delta 仍是 Synapse/Fabric 默认，但 Iceberg 的跨引擎中立性（Fabric OneLake 亦提供
  Iceberg 化选项 ⚠️ 转述）让 6.4 节「一数据三引擎」的兼容性叙事在 2026 偏向 Iceberg；盘上纵深：
  [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)、
  [../Architecting_an_Apache_Iceberg_Lakehouse/00-总览与阅读地图.md](../Architecting_an_Apache_Iceberg_Lakehouse/00-总览与阅读地图.md)、
  [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)（流式湖仓补角，均在盘 ✅）。
- **ML 面迁移**：SynapseML 的连接器能力在 2026 微软叙事中归入 Foundry/Fabric 语义线 ✅
  https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview（事件侧）与 Azure ML/Foundry
  文档域 ⚠️；本书该节按「历史形态」读。
- **Spark 理论根基**：shuffle/分区/执行计划的经典文献经 [../../db/db.md](../../db/db.md) 论文索引回溯
  ✅ 在盘。
- **Fabric 侧对位（波9 收束升实链）**：本章专用 Spark 池叙事在 Fabric 侧对应 Lakehouse 内嵌
  Spark runtime——兄弟册 [00](../Learn_Microsoft_Fabric/00-总览与阅读地图.md) 08 章与 [00](../Data_Engineers_Guide_to_Microsoft_Fabric/00-总览与阅读地图.md) 04 章有对位 ⚠️ 转述。
