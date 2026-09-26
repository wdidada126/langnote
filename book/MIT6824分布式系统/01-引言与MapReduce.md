# 第 01 讲 Introduction：为什么分布式，以及 MapReduce

> 官方标题：**Introduction**（LEC 1，主讲 rtm）
> 指定必读：**MapReduce (2004)**
> 布置：**Lab 1: MapReduce**

## 本章地图

本讲是整门课的「立论」，回答两个问题：**为什么要有分布式系统**、**为什么它难**。
Morris 给出的动机是四条——并行换性能、副本换容错、物理上本来就分离、隔离换安全；
困难也是四条——并发、局部失效（partial failure）、性能不随机器线性增长、以及由此带来的复杂度。
后半讲用 MapReduce 当第一个案例：它是「把困难收敛到一个框架里」的范本——
程序员只写 `map` / `reduce`，框架负责分发、容错、straggler 处理。

主线：动机 → 困难 → 课程三大主题（性能 / 容错 / 一致性）→ 基础设施（RPC、线程、并发控制）→ MapReduce 案例。

## 核心精讲

### 1.1 为什么要构建分布式系统

| 动机 | 含义 | 代价 |
| --- | --- | --- |
| 并行（parallelism） | 多台机器同时干活，吞吐随机器数增长 | 需要可切分的任务 + 可聚合的结果 |
| 冗余（replication） | 一份数据多份副本，坏一台不掉数据 | 副本之间必须保持一致 |
| 物理分布（physical） | 业务本身就跨地域（如跨行转账） | 网络延迟不再是可忽略项 |
| 隔离（isolation） | 互不信任的域之间需要边界 | 需要认证/授权，不能靠共享内存 |

### 1.2 为什么难：三条核心困难

1. **并发（concurrency）**：多个节点同时做事，交互顺序不可预测；
2. **局部失效（partial failure）**：一部分坏了、一部分还活着——这是分布式独有的、最折磨人的失败形态；
   单机程序要么全崩要么全对，分布式系统必须能「带伤运行」；
3. **性能不线性**：加机器不会线性提速，Amdahl 定律 + 协调开销 + 网络瓶颈共同起作用。

### 1.3 课程三大主题（贯穿 21 讲）

- **性能（performance）**：可扩展性——加 N 倍机器要拿到接近 N 倍的吞吐；
- **容错（fault tolerance）**：可用性 + 可恢复性 + **一致性**（副本必须看起来像一份）；
- **一致性（consistency）**：理想是「对外表现得跟没复制一样」，但实际要在强弱之间做取舍。

课程用的三件基础设施：**RPC**（跨节点通信）、**线程**（节点内并发）、**并发控制**（锁/通道/原子操作）。

### 1.4 MapReduce：把困难收进框架

执行流程：

```
输入（GFS 上的大文件，切成 M 个 split）
  → M 个 map worker：产出中间 key/value，按 R 个 reduce 分区落本地盘
  → shuffle：reducer 从各 mapper 拉取自己那一片
  → R 个 reduce worker：归并同 key 的值，输出到 R 个文件
  → 结果通常再喂给下一个 MapReduce
```

框架要做的事（程序员不写）：任务调度、位置感知（让 map 读本地副本）、
worker 失效重做、**straggler 的备份任务（backup task）**、combiner 优化、中间数据分区。

关键设计取舍：

- **重做是安全的，因为 map/reduce 必须是纯函数（deterministic）**——
  同样的输入重跑得到同样的输出，所以「不确定就重跑」不会污染结果；
- **reduce 的输出是原子的**：靠底层文件系统（GFS）的原子 rename 保证，所以 reduce 重做不会留下半成品；
- **map 的中间结果写在 mapper 本地盘**，而不是 GFS——失败就重跑，省掉复制开销；
- **straggler 不是故障，但比故障更伤**：收尾阶段额外启动备份任务，谁先完成算谁的。

### 1.5 教学示意：一个极简 MapReduce 调度器骨架

> **教学示意，不参与构建**，只表达「任务状态机 + 重做」的形状，不是可跑的实现。

```go
// 教学示意：任务状态机（不参与构建）
type TaskState int

const (
    Idle TaskState = iota
    InProgress
    Completed
)

type Task struct {
    ID     int
    Kind   string // "map" | "reduce"
    Input  string
    State  TaskState
    Worker string   // 派给了谁
    DoneAt time.Time
}

// 调度循环的核心判断：一个 InProgress 的任务超过阈值没完成，就重新标记 Idle
func (c *Coordinator) sweep(threshold time.Duration) {
    now := time.Now()
    for i := range c.tasks {
        t := &c.tasks[i]
        if t.State == InProgress && now.Sub(t.DoneAt) > threshold {
            // 关键点1：重做必须幂等 —— 依赖于 map/reduce 是确定性的
            // 关键点2：旧 worker 可能还活着，它写出的输出必须能被丢弃
            //          （实践中靠「先写临时文件、完成后原子 rename」实现）
            t.State, t.Worker = Idle, ""
        }
    }
}
```

> 这个骨架刻意省掉了：RPC 定义、worker 注册、输出文件的原子提交、以及 straggler 备份任务的触发时机。
> 正因为它省掉了这些，它**不能**被当成 Lab 1 的答案——它只是把「为什么需要超时重做」讲清楚。

### 1.6 MapReduce 的局限（也是后续课程的伏笔）

- **只有 map 和 reduce 两步**，任何需要迭代/多轮 join 的计算都要串成 DAG，中间结果反复落盘；
- **不擅长流式**：输入是有界数据集，来一条算一条的场景要靠别的系统；
- **不解决一致性问题**：它依赖底层文件系统已经把存储问题解决了。

## 版本演进

- **2004（论文当年）**：MapReduce 解决的是「几千台廉价机器 + 每天 TB 级数据 + 程序员不想管并行」的矛盾。
- **2010 前后**：Hadoop 把 MapReduce 开源化，成为大数据的事实标准；
  但社区很快发现「所有计算都套 map-reduce」既慢又难写。
- **2012–2015**：Spark（弹性分布式数据集 RDD + 内存计算 + DAG 调度）在实践中大面积取代 MapReduce；
  Flink 走真正的流式（事件驱动 + 有状态算子）。
- **2020（本讲）**：课程已把 Spark 独立成 L15 一讲，MapReduce 在本讲的定位是
  「**第一个可理解的大规模并行抽象**」，而不是「推荐的现代方案」。
- **2026**：批处理的主流是 Spark / Flink / 各类 SQL 引擎（以及 Ray 这类通用分布式执行框架，
  6.5840 在 2026 已把 **Ray** 单列一讲）。MapReduce 本身基本退居教学与面试概念，
  但它的三个思想——**确定性重做、位置感知调度、straggler 备份任务**——被完整继承下来。

## 经典论文与原始文献

| 论文 | 出处 | 本讲为何读它 |
| --- | --- | --- |
| Dean & Ghemawat《MapReduce: Simplified Data Processing on Large Clusters》 | **OSDI 2004** | L1 指定必读。示范「用受限的编程模型换取自动并行与自动容错」 |
| （配套，非本讲指定）Ghemawat, Gobioff & Leung《The Google File System》 | SOSP 2003 | MapReduce 的输入/输出与 reduce 的原子 rename 依赖 GFS；L3 的必读 |

> 课程站点上的文件名：`mapreduce.pdf`。本目录不保证长链有效，以官方 2020 schedule 页的链接为准。

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **straggler 与降速（degradation）调度**：Google 的 *Effective Straggler Mitigation*（EuroSys 2013 之后持续研究）
    把「备份任务」升级为「预测性复制 + 资源感知调度」；
  - **Serverless 数据分析**（Lambada、Starling、Cackle 等方向）把 shuffle 搬到对象存储上，
    代价是失去本地性、换来弹性；
  - **确定性执行**重新成为热点（确定性数据库 Calvin，SIGMOD 2012）：
    「先定序、再执行」的思想与 MapReduce 的「确定性重做」同源。
- **工业界开源（star 数 2026-09-26 `gh api` 实测）**：
  - `apache/hadoop`（**15669★**）：MapReduce 的开源实现仍在（Hadoop MapReduce 模块），
    但实际生产中基本由 YARN + Spark/Flink 承担计算，HDFS 仍有大量存量部署。
  - `apache/spark`（**44055★**）：RDD/DAG/内存计算，事实上的批处理主流；
    与 MapReduce 的关键差别是**中间结果尽量留在内存**，失败靠 **lineage（血缘）重算**而不是重跑整个 stage。
  - `apache/flink`（**26367★**）：真正的流处理（有状态算子 + checkpoint），批被视作有界流。
  - `ray-project/ray`（**43929★**）：通用分布式执行框架（任务 + actor），
    6.5840 2026 schedule 已把它单列一讲（LEC 18，读 Ray 2021 论文）。
  - `minio/minio`（**61350★**）：对象存储；2026 年大数据栈的输入输出越来越多地直接落在对象存储上，
    而不是 HDFS——这是 MapReduce 「本地性」前提在云上失效的直接后果。

## 常见误区与本课程需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「MapReduce 快」 | 它 2004 年快在「能跑起来」，不在「跑得快」；多轮 job 的中间落盘是主要瓶颈，Spark/Flink 正是为解决它而生 |
| 2 | 「mapper 失败重跑就够了」 | 还要处理 **straggler**（没坏但极慢），否则长尾决定总时长；备份任务是必须的 |
| 3 | 「重做随便做」 | 重做合法的前提是 **map/reduce 确定性**；若 reduce 依赖外部时钟/随机数，重做会产生不一致结果 |
| 4 | 「输出写一半被读到」 | reduce 输出必须原子发布（临时文件 + 原子 rename），这是「重做安全」的另一半 |
| 5 | 🔧 2020 课程未覆盖 | 云上**存算分离**使「位置感知调度」失去意义：对象存储的带宽不再是本地盘语义，调度目标从「靠近数据」变成「靠近缓存/靠近网络出口」 |
| 6 | 🔧 2020 课程未覆盖 | **Serverless / 弹性执行**：worker 池不再固定，故障不再是「机器坏了」而是「实例被回收/被限流」，重试语义要重新设计（幂等键成为一等公民） |
| 7 | 🔧 2020 课程未覆盖 | **数据倾斜**在 2020 只作为调优话题带过；2026 的 SQL 引擎普遍内建 adaptive query execution（AQE）自动拆分倾斜分区 |
| 8 | 🔧 2020 课程未覆盖 | Lab 1 的骨架在 6.5840 已迭代（2026 为 Lab 1 MapReduce，另新增 Lab 2 Key/Value Server）；按同一份旧资料照抄会与新 lab 的接口不一致 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - [02-RPC与线程.md](02-RPC与线程.md)——Lab 1 的 worker 与 coordinator 之间就是 RPC，下一讲讲它的失败语义；
  - [03-GFS.md](03-GFS.md)——MapReduce 的输入输出与原子 rename 都建立在 GFS 上；
  - [13-Labs总结与2026视角.md](13-Labs总结与2026视角.md)——Lab 1 的设计要点与调试方法，以及 L15 Spark 讲的一句话索引。
- **跨书**：
  - [../设计数据密集型应用/10-批处理.md](../设计数据密集型应用/10-批处理.md)——DDIA 对 MapReduce 及其后继（数据流引擎）的取舍分析，与本讲互补；
  - [../分布式系统/01-引论.md](../分布式系统/01-引论.md)——教材口径的「分布式系统动机与设计目标」，可用于把本讲的四条动机系统化；
  - [../2020-10_DistSys_lectures/00-索引与阅读地图.md](../2020-10_DistSys_lectures/00-索引与阅读地图.md)——剑桥课程没有对应的批处理讲（它的 8 讲偏模型），本讲是 MIT 独有的工程案例。

> **Lab 提示（思路，不给代码）**：Lab 1 的成败在于「任务状态机 + 超时重做 + 输出原子发布」三件事；
> 先想清楚「一个任务从 Idle 到 Completed 有哪些中间态、在哪个态超时」，再动手。
> 本目录不提供、也不链接任何公开解答仓库。
