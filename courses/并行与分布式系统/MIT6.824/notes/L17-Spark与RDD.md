# L17 Spark：弹性分布式数据集（RDD）

> 阅读：Zaharia et al., *Resilient Distributed Datasets: A Fault-Tolerant Abstract for
> Distributed Memory Computing*, NSDI 2012
> 主线：修复 L02 MapReduce 的最大短板——每步落盘、只有两层——用内存 + 血缘重算。

## 1. 核心问题

- MapReduce（L02）的痛点：
  1. **迭代算法极慢**（机器学习/图计算每轮都要把中间结果写 HDFS 再读回）；
  2. **表达受限**（只有 map+reduce 两层，稍复杂的 DAG 要串几十个作业）；
  3. **交互式查询**（每次全量落盘）。
- 前人的内存集群系统（HaNeP/Ptylee）用"把数据常驻内存 + 更新传播"，
  但**编程模型不通用 / 容错靠日志代价高**。
- Spark 的问题：**能否有一个通用的内存分布式抽象，容错成本近乎为零？**

## 2. RDD：设计核心

### 2.1 定义
RDD = **只读（read-only）、可分区（partitioned）、可并行操作**的元素集合。
"只读 + 血缘（lineage）"是全讲的钥匙：
- 只读 → 不可变 → 无需锁、可随意多读；
- 血缘（记录它是从哪个稳定存储经哪些变换来的）→ **丢失就沿血缘重算（recompute）**
  ——容错从"复制/日志"换成"重算"，几乎零成本（与 L02 MapReduce 重做、
  L08 checkpoint 对照：三种容错策略——重算 vs 复制 vs 检查点）。

### 2.2 转换与行动
- **Transformation（惰性）**：`map/filter/union`（窄依赖：每父分区 → 常数个子分区，
  可流水线）与 `join/groupBy`（宽依赖：需 shuffle，物化屏障，对应 BSP 超步）。
- **Action**：`count/collect/save` 才触发计算。
- **窄依赖可全程流水线**是相对 MapReduce（每作业物化）的性能来源之一；
  DAG 调度器把 Stage 切在宽依赖边界（对照 L02 的"只有两层"→ 任意深度 DAG）。
- `persist()` 显式把热数据钉进内存；存储级别决定溢出策略
  （MEMORY_ONLY / MEMORY_AND_DISK / 序列化副本）。

### 2.3 与共享内存模型的哲学对照
Spark 论文专门对比 active memory（内存数据库）：
- 内存数据库：数据可变 + 更新传播 + 复制日志容错 → 细粒度操作但贵；
- RDD：粗粒度变换 + 血缘重算 → 粒度受限（不能随机更新）但简单且容错免费。
**取舍：牺牲细粒度可变性，换容错简洁性与吞吐**——"one abstraction fits most"。

## 3. 性能与后续

- 论文数据：逻辑回归比 Hadoop 快 30×（迭代复用内存）、
  交互式查询快 100×+。
- Shuffle 仍保留 MapReduce 式"sort-based shuffle"（后续 Adaptive Query Execution、
  push-based shuffle 才改善）。
- 谱系扩展：DataFrame/Dataset（带 Catalyst 优化器的逻辑计划，走向 L18 的
  专用 DAG）、Structured Streaming（微批 = RDD 上的流）、GraphX（带 Pregel API
  的图专用 RDD）、MLlib。

## 4. 论文间脉络

- 直接回答 L02 的遗留问题（中间结果落盘）。
- 与 L18 衔接：Spark 是"通用 DAG"，Millipipe/Piccolo 进一步做"流水线化 + 专用化"，
  GraphX/Lightning 做图特化——数据并行三部曲。
- 与 L16 衔接：批（Spark core）与流（Structured Streaming）的"批流一体"，
  Kafka 供数据、Spark 供引擎。
- 血缘重算 = 分布式快照/检查点（L07 Chandy-Lamport、Flink）的"惰性对偶"。

## 5. 跨课程联系

- **CS149**：窄依赖流水线 = 数据并行 + 任务并行混合调度；Stage 边界 = 全局栅栏；
  RDD 分区 ↔ 并行数组（parallel array）与 gather/scatter。
- **15-445/15-721**：Catalyst 优化器 = 编译式查询优化；惰性求值 ↔ 向量化执行。
- **MLC/15-442**：数据并行训练（每分区一份 mini-batch）≈ 分布式 RDD 变换；
  梯度压缩 ↔ shuffle 优化。Spark 曾是参数服务器的载体（GraphX 的 PowerGraph 血统）。
- **6.S081**：`persist` 的内存管理 ↔ page cache 换入换出策略。

## 6. 开源项目中的应用

- **Apache Spark**：ETL/数仓（Delta Lake = Spark + 事务日志，L14 血统）、
  特征工程（Databricks）。
- **Databricks Photon / Gluon**：向量化/加速器实现（本讲论文的工业延长线）。
- **Ray（L 官网讲义有 Ray 讲）**：Actor + 对象存储模型，是"可变状态 + 细粒度"
  对 RDD"不可变 + 粗粒度"的反命题（对照阅读）。
- **Flink**：走"流为一等 + checkpoint 容错"另一路线，与 Spark"批为一等 + 重算"对照。

## 7. 延伸阅读

- *Resilient Distributed Datasets* 原论文 + Spark 论文后续 *An Imperative Style, More Efficiently*（DataFrame）。
- *Millipipe* (OSDI 2020)（下一讲）——理解"流水线化数据并行"如何吃掉 Spark 的启动开销。
- CARMA/"The Dataflow Model"（Google, MillWheel）——批流一体的另一理论框架。
- 精读 Spark 源码 `DAGScheduler`/`ShuffleManager`，对照本讲 Stage 切分规则。
