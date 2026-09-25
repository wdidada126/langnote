# 03 Apache Flink 架构（原书第 3 章）

> 对应原版第 3 章（中文版「Apache Flink 架构」）。小节范围按已核实中文目录：
> 系统架构、搭建 Flink 所需组件、应用部署、任务执行、高可用性设置、Flink 中的数据传输、
> 基于信用值的流量控制、任务链接、事件时间处理（时间戳/水位线/水位线传播/时间戳分配与生成）、
> 状态管理（算子状态/键值分区状态/状态后端/有状态算子扩缩容）、
> 检查点/保存点及状态恢复（一致性检查点/Flink 检查点算法/性能影响/保存点）。
> 正文逐字内容未获取，下文按该范围重写（见 [00 总览](00-总览与阅读地图.md) 核实说明）。

## 核心概念速览（中英对照）

- **作业管理器** — JobManager：负责构图、调度、协调检查点与故障恢复的主控进程（master）。
- **任务管理器** — TaskManager：真正执行子任务的 worker 进程，提供任务槽与网络/内存资源（Client 提交后不在数据路径上）。
- **作业图 / 执行图** — JobGraph / ExecutionGraph：逻辑图（算子 + 边）与按并行度展开、含调度状态的物理图。
- **应用部署 vs 会话部署** — application mode / session mode：前者每作业独占集群（jar 在集群侧），后者共享一个长驻集群。
- **基于信用值的流量控制** — credit-based flow control：接收方向发送方通告可接收缓冲数（信用），实现无阻塞式反压传导。
- **任务链接** — task chaining：把可合并的相邻算子装进同一个任务线程，省掉序列化与网络。
- **水位线传播** — watermark propagation：算子输出水位线 = 各输入通道水位线的最小值，保证「所有上游都没越过」才推进。
- **时间戳分配器与水位线生成器** — timestamp assigner & watermark generator：从记录抽取时间戳并按乱序界发出水位线。
- **键控状态** — keyed state：只在 `KeyedStream` 上可用、按当前记录所属键自动路由的状态。
- **算子状态** — operator state：属于算子实例本身的状态，跨重启靠分配策略（even/split/union）重分布。
- **状态后端** — state backend：状态的物理存放与快照实现（堆内 vs 磁盘 RocksDB；快照写到哪里）。
- **键组** — key group：键控状态分片的逻辑单位，决定「哪个子任务持有哪些键」，是有状态算子扩缩容的基础 ⚠️（术语出处以官方文档为准）。
- **一致性检查点** — consistent checkpoint：所有算子快照构成的全局状态恰好等于某个「逻辑时刻」的快照，无悬挂消息。
- **屏障对齐** — barrier alignment：多输入算子必须等所有输入通道的同一次检查点屏障到齐才快照，否则重放会出现消息重复/丢失。
- **保存点** — savepoint：由人主动触发的、带目录与元数据格式的检查点，用于版本升级、A/B、迁移与重缩放。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 | 系统组件 | Client 提交、JobManager 编排、TaskManager 执行，三者可独立扩缩 |
| 3.2 | 应用部署 | 图从 API 到 JobGraph 到 ExecutionGraph，部署单位是 subtask |
| 3.3 | 任务执行 | slot = 资源容器；slot sharing 让不同算子共槽，吞吐靠并行度而非槽数 |
| 3.4 | 高可用 | ZooKeeper 做 leader 选举与元数据持久化，JobManager 挂了能恢复作业 |
| 3.5 | 数据传输与反压 | Netty + 固定网络缓冲 + 信用通告；反压是特性不是故障 |
| 3.6 | 任务链接 | 1:1、同并行度、非链外分区 → 合成一个任务；调试时要会关掉 |
| 3.7 | 事件时间处理 | 时间戳在 source/assigner 处打，水位线按最小值跨图传播 |
| 3.8 | 状态管理 | keyed state 按键、operator state 按实例；状态后端决定性能与容量 |
| 3.9 | 检查点与保存点 | 屏障 + 异步快照 + 全局确认 + 回滚；保存点是其「人为触发、可移植」版 |

## 核心精讲

### 3.1 三个进程，一条控制链

```
Client ──(JobGraph + jar 引用)──▶ JobManager ──(部署 subtask)──▶ TaskManager ×N
                                      │                              │
                              CheckpointCoordinator                状态读写 / 网络 shuffle
                                      └──── 快照写入 ───▶ HDFS / S3（state.checkpoints.dir）
```

- **Client** 不在数据路径上：提交完就退出（`-d` 分离模式）；`rest.port: 8081` 提供 Web UI/REST。
- **JobManager** 内含 SchedulerNG（⚠️ 组件命名随版本变化）、`CheckpointCoordinator`、HA 元数据；它决定检查点何时触发、谁完成、失败是否回滚。
- **TaskManager** 提供 `taskmanager.numberOfTaskSlots`；一个 slot 理论上可跑任意 subtask，靠 slot sharing 混装。

### 3.2 部署与执行的粒度

| 层次 | 单位 | 决定因素 |
| --- | --- | --- |
| 用户代码 | 转换（`map`/`process`/`window`） | 你的写法 |
| JobGraph | 节点 + 边 | 转换拓扑 |
| ExecutionGraph | `ExecutionJobVertex` × subtask | 并行度 |
| 部署 | subtask → slot → TM 线程 | slot 请求与资源 |
| 状态 | key group 分片 → subtask | `maxParallelism` + key hash |

**为什么粒度重要**：检查点、监控、失败重启都发生在 subtask 级别；调优（改并行度、加内存、拆链）也都在这一级生效。

### 3.3 数据传输：缓冲、通道与信用

- 每条 shuffle 边展开为「上游 subtask × 下游 subtask」的 channel 矩阵；channel 用固定数量网络缓冲（memory segment）收发。
- **信用机制**：接收端按已消费的空闲缓冲数向发送端发「信用」；发送端只有在有信用时才写。
  好处：不需要 TCP 那种会阻塞 Netty 线程的流控，反压可以在应用层精确表达并能区分不同 channel。
- 后果：`taskmanager.network.memory.fraction` / `buffers-per-channel` 配小 → 吞吐受限；配大 → 内存挤占堆内状态（09 章调优）。

### 3.4 事件时间的机器学：时间戳与水位线传播

🔧 Scala（Flink 1.7 风格；教学示意）

```scala
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)

val stream = env.addSource(kafkaSource)
  .assignTimestampsAndWatermarks(
    new AscendingTimestampAssigner[Event] {                     // 升序假设：乱序界 5s
      override def extractTimestamp(e: Event, prev: Long): Long = e.ts
      override def onPeriodicEmit(wm: WatermarkOutput) =
        wm.emitWatermark(new Watermark(currentMaxTs - 5000))    // 水位线 = 见过的最大时间戳 - 乱序界
    })
```

架构层的三条规则（本目录后文反复引用）：

1. **水位线是「单调的猜测」**：算子内部对每条记录更新最大时间戳，周期性发出 `maxTs - lag`。
2. **多输入取最小值**：`out = min(in₁, in₂, …)`；这就是为什么一个卡住的分区会拖住整个作业的时间推进（06 章的 idle source 问题）。
3. **水位线穿过图**：下游算子看到的水位线已经受上游所有分区影响，因此窗口结束条件是全局一致而非局部。

### 3.5 状态的两套抽象与三种后端

| 维度 | 键控状态 keyed state | 算子状态 operator state |
| --- | --- | --- |
| 可用前提 | 必须在 `KeyedStream` 之后 | 任意算子 |
| 归属 | 键 → key group → subtask | 算子实例 |
| 恢复时的分配 | 按 key group 重分片（并行度可变） | 按 list state 分配策略：even_split /（union 用于广播类） |
| 典型用途 | 每用户计数、会话缓存、去重集合 | source 的分区 offset（07/08 章） |
| 接口 | `ValueState/ListState/MapState/ReducingState/AggregatingState` | `ListState`（`CheckpointedFunction`）或 `ListCheckpointed`（旧） |

状态后端（Flink 1.7 时代的名字，⚠️ 现代版本已改名，见「版本与兼容性」）：

- **Memory/HashMap 型**：状态在 JVM 堆，快、受内存限制，快照是全量序列化。
- **RocksDB 型**：状态在 RocksDB（堆外 + 本地磁盘），容量大、有序列化代价，支持**增量检查点**（只写变化 SST）。
- **持久化位置**：`state.backend` + `state.checkpoints.dir`（作业容错）与 `state.savepoints.dir`（人工）分离配置。

### 3.6 检查点：Flink 算法与 Chandy-Lamport 的关系（架构视角）

原书在此给出的是机制轮廓，本目录把它整理成六步：

1. JobManager 的 `CheckpointCoordinator` 按周期（如 10s）**向所有 source 注入屏障**（barrier，标记为 `n`）。
2. 屏障随数据流走，**不做插队**：屏障前的事件先被处理并进状态。
3. 算子收到某输入的屏障后**对齐**（等所有输入的屏障 n 到齐；期间收到的其它输入数据先缓冲或直接处理但不计入本次快照）。
4. 对齐完成 → 把状态**异步**快照到持久存储，同时**放行屏障**继续向下游。
5. 所有算子快照成功 → JobManager 记 `n` 为「完成的最小水位」，并向算子发 `notifyCheckpointComplete`（08 章的事务提交钩子）。
6. 任一算子失败/超时 → 丢弃 `n`，作业回滚到**上一个完成的检查点**，并从 source 重放到该位置。

与原始论文的差别（细节见 [12 补编](12-补编-检查点机制与分布式快照.md)）：用数据流内屏障代替独立的控制消息广播，
快照是**异步**的（论文隐含同步语义），并且要额外处理**源与汇**（外部系统不在图内 → 需要重放/幂等/事务）。

### 3.7 检查点的性能账单

| 代价项 | 触发条件 | 缓解 |
| --- | --- | --- |
| 对齐等待 | 反压 + 多输入算子（keyBy/window 之后） | 加长间隔、提高并行度、（1.11+）非对齐检查点 ⚠️ |
| 快照序列化 | 大状态 + 全量快照 | RocksDB 增量检查点、预定义序列化器 |
| 上传带宽 | 状态写到远端对象存储 | 提高 `state.checkpoints.num-retained` 前先算容量、本地恢复 ⚠️（后版本特性） |
| 屏障放大 | 并行度高、channel 多 | 控制 `maxParallelism`、拆作业 |

## 版本与兼容性

- **状态后端改名**：`MemoryStateBackend`/`FsStateBackend`/`RocksDBStateBackend`（本书时代）→
  `HashMapStateBackend`/`EmbeddedRocksDBStateBackend` + `state.checkpoints.dir` 决定持久化（1.13 起）⚠️ 以官方文档为准。
- **时间戳 API 换代**：`assignTimestampsAndWatermarks(Assigner...)`（1.7）→ `WatermarkStrategy`（1.11+）。
- **`ListCheckpointed` 已废弃移除**（1.13 起不推荐，2.0 移除）⚠️：本书用它讲算子状态，现在一律写 `CheckpointedFunction`。
- **可查询状态（Queryable State）**在本书第 7 章有整节，但 1.10 起废弃、后续版本移除 ⚠️（07 章说明替代方案）。
- 本书部署章节的 Kubernetes 支持是 1.7 时代的形态（非 native K8s；native 支持 1.10 起）⚠️（09 章说明）。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「JobManager 挂了作业就丢」 | 配了 ZooKeeper HA + 持久化 storageDir 才能恢复；没配就是单点（09 章） |
| 「slot 数 = 并行度上限」 | 每个 slot 可承载多个 subtask（slot sharing）；总槽位需求 ≈ 最大并行度（同作业内不同算子共槽） |
| 「水位线是消息，随便插队」 | 水位线在通道里按序推进，与数据同序，这正是它「表示进度」的原因 |
| 「检查点越频繁越安全」 | 频繁检查点会挤占 CPU/带宽并放大对齐等待，反而降低吞吐；间隔要与可容忍恢复时间一起定 |
| 「RocksDB 一定比堆内快」 | RocksDB 省内存但有 (反)序列化与磁盘代价；小状态高吞吐场景堆内更快 |
| 「保存点就是检查点」 | 触发者（人 vs 调度器）、格式（可移植的规范路径 vs 作业内部引用）、用途（升级/重缩放 vs 容错）都不同 |
| 「对齐等待是 bug」 | 它是正确性要求；想「不对齐」得用非对齐检查点或改用处理时间语义，不能只调参数 |

## 与其他章 / 其他书的联系

- 3.2 的图与并行在代码层如何表达 → [05-DataStreamAPI.md](05-DataStreamAPI.md)。
- 3.4 的水位线在窗口/计时器上的可见后果 → [06-时间与窗口算子.md](06-时间与窗口算子.md)。
- 3.5 的两套状态接口写法与扩缩容实操 → [07-有状态函数与状态管理.md](07-有状态函数与状态管理.md)。
- 3.6 第 5 步的提交钩子与端到端一致性 → [08-读写外部系统.md](08-读写外部系统.md)。
- 3.4/3.6 的运行期配置（HA、检查点目录、状态后端）落地 → [09-集群部署与配置.md](09-集群部署与配置.md)、
  [10-运维监控与调优.md](10-运维监控与调优.md)。
- 仓库互链：检查点/屏障的通用叙述与论文登记见 [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)
  第 91 行与第 209 行（Chandy & Lamport, ACM TOCS 1985）；快照算法本身见 [12-补编-检查点机制与分布式快照.md](12-补编-检查点机制与分布式快照.md)。
