# CMU 15-442 提纲

> 骨架级要点，正文笔记待逐讲展开。

## L1 导论
- MLSys = 算法 × 系统 × 硬件的交叉学科；瓶颈常在 IO 与通信而非算力。
- 全栈协同设计（co-design）视角贯穿课程。

## L2 自动微分
- 前向模式（雅可比-向量积）vs 反向模式（向量-雅可比积，标量输出 O(n)）。
- 计算图 tape 机制；高阶 AD 与双数。
- 作业1：扩展图 AD 支持控制流/自定义算子。

## L3 框架架构
- 张量抽象、算子注册、惰性 vs 即时执行、运行时调度。
- PyTorch dispatcher / torch.compile 分层；XLA 图编译。

## L4 GPU 硬件
- SM、warp、寄存器文件/共享内存/HBM 层级与带宽。
- Tensor Core 与 MMA 指令；Roofline 判定计算/访存受限。

## L5 GPU 编程
- CUDA 线程模型、合并访存、bank conflict；PTX 与编译链。
- Triton/TIRx DSL：以块级编程替代手工 warp。

## L6 高性能 GEMM
- 分块 tiling + 双缓冲；128B Swizzle 消除 bank conflict。
- TMA 异步搬运、Warp Specialization 软流水线、2-CTA 集群；对标 cuBLAS。

## L7 ML 编译
- 图优化（算子融合/布局）+ 算子调度（循环变换）。
- AutoTVM/Ansor 自动搜索；TIR 抽象。

## L8 数据并行与通信
- All-Reduce 原语、ring 算法带宽最优。
- 梯度分桶与计算/通信重叠。

## L9 ZeRO
- 优化器状态/梯度/参数三级分片消除冗余。
- 通信量分析；offload。作业2 用 MPI+NumPy 实现 ZeRO-3。

## L10 模型并行
- 张量并行（TP，列/行切分 + all-reduce）；流水线并行（GPipe/1F1B bubble）。
- 自动并行（Alpa）搜索策略空间。

## L11 LLM 推理 I
- 自回归解码的访存瓶颈；连续批处理（iteration-level scheduling）。
- PagedAttention 管理 KV cache；RadixAttention 前缀复用（SGLang）。

## L12 LLM 推理 II
- KV cache 量化/分页；投机解码用小草稿验证大模型。
- prefill/decode 分离（DistServe/Splitwise）与 chunked prefill。

## L13 量化
- 训练后量化 vs 量化感知训练；FP8/INT8/INT4 与 GPTQ/AWQ。
- 离群值处理与校准数据集。

## L14 前沿
- Mega-Kernel：整模型单 kernel 消除启动/同步开销。
- 异构、Chiplet、开放问题讨论。
