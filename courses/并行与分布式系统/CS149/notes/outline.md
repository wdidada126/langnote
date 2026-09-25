# CS149 讲义要点提纲（骨架）

> 每讲 3–5 条要点级提纲，正文笔记后续按讲填充 `notes/Lxx-*.md`。

## L1 课程导入：并行性的层次
- 并行性来源：指令级（ILP/SIMD）、线程级、硬件线程、数据并行、任务并行、跨机分布式。
- 「性能 = 算法 × 数据结构 × 硬件行为」：并行的核心矛盾是分解与协调。
- 正确性 vs 性能：并行程序的 bug 往往来自不确定的调度顺序。
- 本课程主线：硬件能力 → 编程模型 → 抽象原语 → 框架与系统。

## L2 并行硬件
- 多核 CPU：每核私有 L1/L2 + 共享 LLC，缓存一致性协议（MESI 家族）。
- false sharing：同一缓存行被多线程写入导致性能崩塌，需按行对齐/填充。
- GPU：海量简单核 + warp 锁步执行，吞吐优先于延迟；内存层级与 CPU 迥异。
- 带宽与延迟数量级表：寄存器→L1→LLC→DRAM→PCIe→网络，指导数据放置决策。

## L3 程序表示与执行
- 编译器中间表示与依赖图：可并行性的静态判定。
- ILP 与乱序执行掩盖延迟；SIMD（AVX/NEON）用宽指令实现数据并行。
- 分支预测失败在并行 kernel 中的代价；向量化条件掩码。
- 性能分析工具（perf/VTune/ncu）：先看瓶颈再动手。

## L4 数据并行
- map / filter / reduce 原语：无依赖的逐元素操作天然并行。
- 以数据为中心（data-parallel）vs 以线程为中心两种编程观。
- 局部性：分块（tiling）+ 融合（fusion）减少中间数组与内存往返。
- 案例：图像滤波 pipeline 的分块并行与 GPU kernel 对照。

## L5 任务并行
- fork-join 模型：递归任务分解、工作窃取调度器。
- 任务图 DAG：依赖决定调度，粒度决定开销（细粒度任务的调度成本）。
- 负载不均衡问题：不规则计算（如光线追踪）需要动态调度。
- 与数据并行的组合：任务并行管结构，数据并行管内核。

## L6 同步
- 锁的实现：原子指令（CAS/LL-SC）→ 自旋锁 → 队列锁；锁粒度设计。
- 无锁栈/队列：ABA 问题、内存回收（hazard pointers）。
- 内存模型：relaxed/atomic、happens-before；仅靠 volatile 不够。
- 避免同步的三板斧：局部累加、分区、原语化（reduction）。

## L7 顺序与结合律
- 并行归约的正确性条件：结合律；浮点加法不满足 → 结果随调度变化。
- prefix sum（scan）是数据并行的万能胶：计数排序、流压缩、字符串处理。
- Blelloch work-efficient scan：up-sweep/down-sweep，工作量与顺序算法同阶。
- 关联算子与单位元抽象（monoid）在框架中的体现。

## L8 通信与数据搬移
- NUMA：远端内存访问代价，线程/数据绑定策略。
- CPU↔GPU 传输走 PCIe：overlap 计算与传输、统一内存的真实代价。
- 网络：带宽延迟积、incast、all-to-all 的链路利用（bisection bandwidth）。
- 通信复杂度优化：数据布局、消息合并、拓扑感知调度。

## L9 并行模式与自动并行化
- 模式目录：map、stencil、reduction、graph traversal、backtrack 等及其并行策略。
- 自动向量化/自动并行化的能力边界（依赖分析、别名问题）。
- TBB / Cilk / std::execution / OpenMP 各自的抽象层次与适用场景。
- 用模式语言沟通：同一问题在不同硬件上的映射方法。

## L10 GPU 编程
- CUDA 执行模型：grid/block/thread、warp 调度、occupancy。
- 共享内存手动分块 + bank conflict 规避；coalesced global memory 访问。
- warp 级原语（shuffle）做无内存参与的规约。
- 案例：matrix multiply / mandelbrot 的逐级优化曲线。

## L11 集合通信
- broadcast、scatter、gather、all-gather、reduce、all-reduce、all-to-all 语义。
- all-reduce 实现：ring vs tree/halving-doubling，延迟与带宽权衡。
- 模型并行中的通信模式：数据并行=all-reduce 梯度，张量并行=all-gather。
- MPI/NCCL/Gloo/Gloo 后端对照。

## L12 分布式并行框架
- MapReduce 模型：容错靠重算而非检查点；shuffle 是代价中心。
- Spark RDD：用不可变弹性数据集 + lineage 把迭代计算留在内存。
- 数据并行 DSL/框架的调度：任务划分、倾斜（skew）处理。
- 单机原语 vs 集群原语的映射关系（scan→部分和重分布）。

## L13 端到端案例
- 图处理并行：PowerGraph/GAS 模型、顶点切分（flock）与幂等更新。
- 深度学习训练的并行策略：数据/算子/流水线/专家并行组合。
- 一个完整应用从算法选择到部署的并行化决策记录。
- 度量：扩展效率、加速比、每样本吞吐。

## L14 性能度量与评测
- Amdahl 定律与 Gustafson 视角：固定时间 vs 固定问题。
- 强弱扩展实验设计与报告规范（baseline、方差、饱和点）。
- Roofline：算术强度决定 compute-bound / memory-bound。
- 课程总结：并行系统设计是一条「分解—通信—协调—度量」的闭环。
