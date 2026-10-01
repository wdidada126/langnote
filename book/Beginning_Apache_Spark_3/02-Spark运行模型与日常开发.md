# 02 Working with Apache Spark（Spark 运行模型与日常开发）

> 原书 Ch2，pp.17–49。这一章把「跑起来」拆成两半：运行时（driver/executor/cluster manager 的进程拓扑）与编程时（RDD 的最小必要知识 + DataFrame 日常操作）。二级小节未实抓 ⚠️，主题簇依章题页幅与同谱系册推定重构；属**精读重构**，非原书文本。

## 2.1 运行时拓扑：一个 Spark 应用的解剖 ⚠️（转述官方文档口径）

- 三角色：**Driver**（持有 SparkSession，翻译并调度你的代码）→ **Cluster Manager**（分配资源：Standalone/YARN/Kubernetes）→ **Executor**（工作 JVM，跑任务、持缓存）。
- 四级工作单元：Application（一次提交）⊃ Job（一个行动作触发一次）⊃ Stage（按 shuffle 边界切分）⊃ Task（一个分区一次执行）。这套名词是本册后面所有优化讨论（`05`）的语言基础。
- 官方锚点：架构文档 https://spark.apache.org/docs/latest/（✅ 主页 200，逐页路径以 latest 为准；本目录不逐一开链接防 404）。
- 教学顺序辨析：#196 Learning Spark 系（波8 兄弟，仅登记）同样从拓扑讲起，但配 cluster 部署实操；本册 Ch2 只要求「看懂 Web UI 上的 job/stage」，部署推给云上托管——2021 年入门册的典型取舍 ⚠️。

## 2.2 RDD：入门册的最小必要知识 ⚠️

- 原书给 RDD 的篇幅极短（章内约一节）——定位是「看得懂遗留代码」而非「用它写新代码」。
- 五个必留概念（重构表述）：① 弹性分布式数据集=带分区的不可变对象集合；② transformation/action 二分与惰性；③ 窄依赖（stages 内流水线）vs 宽依赖（shuffle 断点）；④ 持久化 `persist()`；⑤ 共享变量 broadcast/accumulator（详见 TDG 专章）。
- 对照盘上：RDD 的中文教材展开在 [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)，共享变量在 [../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md](../Spark_The_Definitive_Guide/07-底层API：RDD与共享变量.md)。本册的价值是告诉你**可以不学**，本目录的职责是把「不学」的边界画清楚。
- 宽依赖=shuffle=代价——这个直觉在 Ch5/Ch6 反复收费（DStream 微批本质就是一串带 shuffle 的小 RDD 作业）。

## 2.3 PySpark 与 Scala：API 对称性与坑 ⚠️

- Spark 2.x 起 DataFrame/SQL API 在 Scala/Python/Java/R 间对齐，3.x 继续补 Python 缺口（窗口函数、pandas 转换 API）。入门建议按本册口径：**Python 主线，Scala 会读**。
- PySpark 的两个性能真相（转述 ⚠️，非本机可测）：① Python 代码在 executor 上仍是逐行解释执行，跨 JVM/Python 进程序列化开销真实存在；② `pandas_udf`（Arrow 批量）比 row-at-a-time UDF 快一个量级——这是「UDF 是黑箱」的工程解法，呼应 `04` 的 🔧 E2。
- 类型面：Scala 有 Dataset[T] 强类型编译期检查；Python 只有 DataFrame（无类型）——本册 Ch4 讲 typed/untyped 区分时主要在 Scala 语境 ⚠️。

## 2.4 日常开发回路：REPL、notebook、spark-submit ⚠️

- `spark-shell` / `pyspark` 交互验证小逻辑 → 固化为脚本 → `spark-submit --master yarn --deploy-mode cluster ...` 交付；中间参数面（`--executor-memory`、`--conf`）在 Ch5 优化语境才有意义，Ch2 只建立「提交=申请资源+广播代码」的意象。
- 依赖分发：`--py-files/--jars/packages`——Spark 3.3 起 pip 环境自动分发（conda 式痛点缓解 ⚠️ 版本后话，见演进节）。
- 🔧 概念类比（**非本书 Spark 引擎行为**，环境 DuckDB 1.5.5/SQLite 3.45.3）：本地 REPL 回路 ≈ `duckdb` Python 进程内即时查询；「提交到集群」≈ 把同一 SQL 文本交给远程引擎。本机没有分布式层，故一切与分区/任务数量有关的行为在类比中**缺席**——缺席本身要登记：入门者最容易把 local 模式的「快」错当成引擎的「快」。

## 2.5 Web UI 与可观测的最小面 ⚠️

- 原书本章带 Spark UI 巡礼（Stages/Storage/Environment 页签）⚠️ 推定；要点：看 DAG 可视化找宽依赖、看 stage 时长找倾斜、看 spill 找内存不足。
- 2026 现状修正：Spark UI 信息密度低是社区长期痛点，事件日志 + 外部可观测栈（History Server、OpenLineage、云厂商托管 UI）才是工业面 ⚠️；对照盘上 [../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)。

## repo 视角

| 对照点 | 链接 |
| --- | --- |
| 执行模型权威章 | [../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md](../Spark_The_Definitive_Guide/02-Spark架构与执行模型.md) |
| Shuffle 与宽依赖的中文教材展开 | [../bigdata/03-Shuffle与宽依赖.md](../bigdata/03-Shuffle与宽依赖.md) |
| 表格式/存储层（Spark 不拥有数据） | [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md) |

## 2.7 运行模型问答（重构 ⚠️）

- Q：Driver 挂了作业还在吗？
  A：不在——driver 是调度大脑，client 模式下它甚至是你的 shell 进程；生产要靠集群侧恢复机制（YARN/K8s 重启 driver）或流式 checkpoint（`07`）。
- Q：一个 task 失败会拖垮整个作业吗？
  A：不会，task 级重试是默认行为；但 stage 的 shuffle 输出丢失会引发父 stage 重算——「失败代价」取决于血缘与缓存/检查点，这是 Ch5 埋的线。
- Q：executor 数量、分区数、核数怎么配？
  A：入门期记住一个经验位：先保证「分区数 ≫ executor 核数总和」，让并行度有余量；细调留给 `05` 与 AQE。
- Q：PySpark 作业为什么比 Scala 慢？慢在哪？
  A：慢在 Python↔JVM 边界与逐行执行面；DataFrame API 下大部分工作在 JVM 内完成，差距收窄，UDF 才重新拉开（`04` E2 的单机标本）。
- Q：local 模式能验证分布式语义吗？
  A：语义层（惰性、stage 切分、依赖）可验证；物理层（网络 shuffle、节点失效）不可——本目录 🔧 类比全部处于「语义层可类比」这一档。

## 2.8 日常开发清单（可抄走的 10 条 ⚠️ 重构）

1. 起手：`SparkSession.builder.appName(任务名).master("local[2]")`（本机）→ 上线换 cluster。
2. 一切调试从 `df.printSchema()` 与 `df.show(5, truncate=False)` 开始。
3. 任何 `collect()` 前先 `count()`——driver OOM 的第一道闸门。
4. REPL 里验证过的片段，固化时包成函数，别整段搬。
5. `spark-submit` 参数三段记：资源（executor 数/内存）、代码（主文件/py-files）、配置（--conf）。
6. 依赖管理：镜像/环境交给平台（云托管/容器），不要往作业包里塞 300MB 依赖（3.3+ pip 分发是另一条路）。
7. 命名：给每个 DataFrame 起「物理含义名」而非 df1/df2——计划树排查时的生命线。
8. 看一次 Web UI 的 DAG 可视化，胜过读十遍拓扑图。
9. 遗留 RDD 代码：只改不扩，新逻辑一律 DataFrame。
10. 提交前 `df.explain()` 一眼：出现意料外的 `Exchange` 就该停下来想想。

## 2.9 与前后章的接线表（本册内部导航）

| 本章概念 | 在哪收费 |
| --- | --- |
| stage/宽依赖 | `04` join 策略、`05` shuffle 调参、`06` DStream=一串小作业 |
| 惰性求值 | `04` explain 读计划、`06` 流查询的 trigger 执行 |
| 持久化 | `05` 缓存判断标准、`07` state store 对照 |
| broadcast/accumulator | `04` BroadcastHashJoin、`05` 倾斜热点键处理 |
| PySpark 边界 | `04` E2 UDF 惩罚标本、8.3 特征管道性能面 |

## 2.10 术语卡（中英）

- 应用（Application）：一次 spark-submit 的全部内容，含所有 Job。
- 作业（Job）：每个 action 触发一次调度执行单位。
- 阶段（Stage）：task 集合，shuffle 为其边界。
- 任务（Task）：单分区的一次执行，最小调度粒度。
- 血缘（Lineage）：RDD/DataFrame 的依赖历史，重算的依据。
- Shuffle 落盘：宽依赖中间物化，磁盘 IO 的重灾区。

## 2.11 速自检（口令式，答案在上文）

1. 说出四级工作单元及其切分依据。
2. 宽依赖=____，它在哪里显形（UI 层）。
3. Driver 与 Executor 各自持有什么状态？
4. client 与 cluster 部署模式差在哪一进程的落点？
5. PySpark 慢的三处边界（进程/序列化/逐行）。
6. `--py-files` 时代与 pip 分发时代的分界版本？
7. broadcast 与 accumulator 的读写方向各是什么？
8. 「本地 REPL 快」为什么不证明「引擎快」？

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 驱动器 | Driver | 持有 SparkSession、翻译代码并调度任务的主进程 |
| 执行器 | Executor | 集群工作进程，执行 task 并提供内存缓存 |
| 集群管理器 | Cluster Manager | Standalone/YARN/K8s，负责资源分配的角色 |
| 应用/作业/阶段/任务 | Application/Job/Stage/Task | 四级工作单元，stage 以 shuffle 为边界 |
| 窄依赖 | Narrow Dependency | 子分区只依赖有限父分区，可流水线执行 |
| 宽依赖 | Wide Dependency (Shuffle) | 重分区依赖，物化中间结果的代价点 |
| 持久化 | Persistence/Caching | RDD/DataFrame 跨复用点保存计算结果 |
| 广播变量 | Broadcast Variable | 只读大变量免逐行网络复制 |
| 累加器 | Accumulator | 单向聚合的写侧共享变量 |
| pandas API UDF | Vectorized UDF | Arrow 批量替代逐行 Python，缩小 UDF 惩罚 |
| 提交模式 | spark-submit | 生产交付形态：资源申请+代码分发 |
| Spark UI | Application Web UI | 入门者的第一可观测面：DAG/stage/时长 |

## 最新演进与工业实践

- **运行时面（2021→2026）**：Kubernetes 原生调度成为一线（`spark-submit` on K8s 从实验转正）；**Spark Connect**（4.0 一等公民）把 driver 逻辑从「和你的 executor 挤在一个 JVM」拆成协议化远程会话，入门图里的经典拓扑正在变成「瘦客户端⇄服务」⚠️（官方文档口径）。锚点：https://spark.apache.org/docs/latest/（✅ 200）。
- **PySpark 面**：pandas API on Spark（`pandas_on_spark` 并入主线）让 pandas 语法直通分布式执行；pip 依赖分发（3.3+）缓解「--py-files 手工艺」⚠️。
- **RDD 退场进度**：本册 2021 年已只给 RDD 一节；3.x 后期 MLlib RDD API 进入维护、GraphX 边缘化，2026 视角下「先 RDD 后 SQL」的教学路径正式归档——盘上仍以该路径写的中文单文件群（`../Spark大数据分析与实战.md`、[../bigdata/](../bigdata/00-总览与阅读地图.md) 谱系）读时需要这层时代修正。
- **工业实践**：入门练习的主流载体从自建 local Spark 转向 Databricks Community/云托管免费档 ⚠️；本目录因 Spark 不可装（沿用波6 实测结论），教学验证一律走「DuckDB/SQLite 概念类比 + 官方文档实证」双轨，且类比数字不外推。
