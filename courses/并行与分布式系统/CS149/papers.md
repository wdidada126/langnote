# CS149 论文与开源应用映射

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities (Amdahl) | 1967 | 给出串行占比决定加速比上界的经典定律 | L1, L14 |
| Reevaluating Amdahl's Law (Gustafson) | 1988 | 固定时间视角下大规模并行近线性扩展 | L14 |
| Vector Models for Data-Parallel Computing (Blelloch) | 1990 | prefix sum/scan 的工作高效并行算法，数据并行理论基础 | L4, L7 |
| A Message-Passing Interface (Grope & Lusk, MPI 前身) | 1994 | 标准化跨节点消息传递语义，集群编程基石 | L8, L11 |
| The Landscape of Parallel Computing Research: A View from Berkeley (patterns 报告) | 2006 | 用 13 个应用 + DAG 抽象归纳并行计算模式 | L9, L13 |
| MapReduce: Simplified Data Processing on Large Clusters (Dean & Barroso) | 2004 | 以 map/reduce 抽象 + 重算容错支撑大规模数据并行 | L4, L12 |
| Resilient Distributed Datasets (Zaharia et al.) | 2012 | lineage 机制让迭代式数据并行计算驻留内存 | L12 |
| Roofline: An Insightful Visual Performance Model (Williams et al.) | 2009 | 用算术强度可视化内存带宽/算力瓶颈 | L14 |
| Scaling the OpenMP Way 系列 / OpenMP Architecture Review Board 规范 | 2000+ | 共享内存循环级并行指令标准的演进 | L5, L9 |
| PowerGraph: Distributed Graph-Parallel Computation (Gonzalez et al.) | 2011 | 顶点切分 + GAS 模型解决幂律图并行 | L13 |

## 近 5 年论文（2021–2026）

| 标题 | 年份/出处 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| Alpa: Automating Inter- and Intra-Worker Parallelism for DNNs | OSDI 2022 | 编译器自动搜索数据/算子/流水线并行组合 | L12, L13 |
| Orca: A Distributed Serving System for Transformer-Based Generative Models | OSDI 2022 | iteration-level 调度把 LLM 推理吞吐提升一个量级 | L5, L13 |
| FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness | NeurIPS 2022 | IO 感知分块将注意力 kernel 逼近 GPU 带宽上限 | L10, L14 |
| vLLM: Efficient Memory Management for LLM Serving with PagedAttention | SOSP 2023 | 类虚拟内存的 KV cache 分页管理提升批处理率 | L5, L10, L13 |
| MPK: MegaKernel 系（Persistent Whole-Program GPU Kernels, 如 Mirages） | arXiv 2024–2025 | 把整个程序编译为单张 GPU 巨核，消除 kernel launch 与中间写回 | L10 |

> 持续跟踪 OSDI/SOSP/SC/PPoPP/MLSys 近 5 年并行相关论文，笔记按讲次回填。

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 应用方式 |
|---|---|---|
| 数据并行原语（L4/L7） | Apache Spark、Dask | RDD/DataFrame 上的 map/reduce/scan 家族 API |
| GPU 编程模型（L10） | CUDA Toolchain、Triton、Taichi | Triton 用类 Python tile 编程抽象 warp/block 管理 |
| 多核共享内存并行（L5/L6/L9） | oneTBB、OpenMP (LLVM libomp)、Intel TBB | 任务窃取调度器、parallel_for/reduction |
| 集合通信（L8/L11） | NCCL、MPI (OpenMPI/MVAPICH)、Gloo | all-reduce 环实现驱动多卡训练 |
| 分布式训练并行（L12/L13） | DeepSpeed、Megatron-LM、PyTorch FSDP | 数据/张量/流水线并行的工程化拆分与通信调度 |
| 性能评测（L14） | nvbench、Google Benchmark | 统计化基准测试框架，防抖动误判 |
