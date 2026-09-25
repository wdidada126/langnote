# L02 MapReduce：大规模并行计算的抽象

> 阅读：Dean & Barroso, *MapReduce: Simplified Data Processing on Large Clusters*, OSDI 2004
> 对应 Lab：pg1（mapreduce）。本课"性能"支柱的第一块基石。

## 1. 核心问题

- 2003–2004 年 Google 每周要跑数千个 PB 级统计任务（URL 计数、倒排索引、
  click-through 分析）。写一个分布式并行程序需要：切分数据、调度机器、容错、
  网络拥塞控制……每个工程师都在重复造轮子且造得不好。
- 观察：**绝大多数任务可以写成"对每条记录做一个函数，再对结果按 key 归约"**。
  于是把编程模型收敛为两个用户函数：`Map(k1,v1) -> list(k2,v2)` 与
  `Reduce(k2, list(v2)) -> list(v3)`，其余全部由运行时接管。
- 与旧模型（SMP、MPI、共享内存锁）的根本差异：MapReduce 假设
  **粗粒度数据并行 + 无共享 + 记录间无顺序**，换来对"机器会死"的免疫力。

## 2. 设计与取舍

### 2.1 执行流程
输入按 64MB 块切分 → master 把 map 任务分给空闲 worker →
map 输出写到本地磁盘（分区环形缓冲， spills 时按 reduce 分区数哈希）→
reduce worker 拉取属于自己分区的中间文件 → 归约输出写 GFS。

### 2.2 容错：全论文最精彩的一节
- worker 心跳超时 → master 把它标记为空闲，**它在做的任务重新调度**；
  已完成的 map 任务也要重做（结果丢了）。
- **Map 是幂等的，Reduce 是"结果可见前原子提交"的**：
  reduce 输出先写临时文件，rename 成功才算发布；两个 reduce 实例同时跑
  也只产生一个最终结果。这就是 L01 RPC 论文"at-most-once 做不到，
  用幂等 + 去重凑"的直接落地。
- 无 check-point 的代价：整批重算。收益：运行时简单到可以信任。

### 2.3 性能优化（取舍的另一半）
- ** locality：map 任务优先调度到持有数据块的机器**（GFS 的 chunkserver
  列表告诉 master 数据在哪）——"移动计算而非数据"。
- **Combiner**：map 端本地聚合，把 shuffle 流量降一个数量级。
- **跳过坏机器**：跑得最慢的 5 个任务重排一遍，谁先完成取谁
  （backup execution，长尾效应对策，后来叫"straggler mitigation"）。
- 排序而非哈希传递中间值：reduce 端需要有序遍历，同时避免分区倾斜全压在哈希上。

### 2.4 局限（论文自己承认的）
- 中间结果全部落盘（可靠性/简单换性能）→ 迭代式作业极差 → 引出 L13 Spark；
- 不支持粗粒度 reduce（单 reducer 热点）、不支持图计算（Pregel 补位）、
  表达力受限（一切问题都得压进 map/reduce 两个框）。

## 3. 论文间脉络

- 承 L01：master/worker 通信用 RPC；容错语义 = RPC 论文的 at-most-once + 幂等。
- 启 L03：MapReduce 假设底下有一个"能存超大文件、可追加不可改写"的
  分布式文件系统——GFS 正是为它而生；两者互为动机。
- 启 L13/L14：Spark（内存 RDD）、Millipipe（DAG 流水线）全是对
  "每步落盘、只有两层"的修正——本课数据并行主线：MapReduce → Spark → Millipipe/GraphX/Lightning。

## 4. 跨课程联系

- **CS149**：MapReduce 是 bulk-synchronous parallel（BSP）的工业实例——
  map 阶段 = 超步计算，shuffle = 全局栅栏同步；对照 CS149 的 gather/scatter 抽象。
- **15-445/15-799**：分区聚合（partial aggregation + exchange）与并行 SQL
  的 hash aggregate / hash join 同构；MRR 可看作 select ... group by 的极简版。
- **MLC/15-442**：数据并行梯度下降 = map 算梯度、reduce 求和平均，
  是 PS（parameter server）架构的理论起点。
- **6.S081**：map 端"多进程共享一份只读代码段"的调度直觉，对应内核
  copy-on-write fork 与调度器负载均衡。

## 5. 开源项目中的应用

- **Hadoop MapReduce (Hadoop 1.x)**：论文的直接复刻，YARN 负责资源层。
- **Google 内部**：后来演进为 FlumeJava/MillWheel/Dataflow（论文作者自述
  几乎不再手写原始 MR）。
- **Spark 的 `mapGroups/reduceByKey`、Flink 的 keyed stream**：抽象血缘。
- **Kafka Streams / RocksDB compaction**：log-structured merge 的批量归并
  与 reduce 阶段"按 key 拉取归并"如出一辙。

## 6. 延伸阅读

- Cohen et al., *F1: A Distributed SQL Database*（讲 Google 内部如何用 MR 思路做后台维护）。
- Isard et al., *Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks*, EuroSys 2007——把两层 DAG 泛化成任意 DAG，读懂它就读懂了 Spark/Millipipe 的前史。
- 对照本目录 `projects/p1_mapreduce/`：单进程内用 goroutine 模拟 master/worker，复现超时重做与 backup execution。
