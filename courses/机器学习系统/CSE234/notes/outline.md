# UCSD CSE234 提纲

> 骨架级要点，正文笔记待逐讲展开。

## L1 现代 DL 与计算图
- 框架三层：张量库 / 计算图 / 高层 API；eager vs graph 模式。
- 计算图即数据流：算子节点 + 张量边，调度与优化的基础。

## L2 Autodiff 与系统架构
- 反向模式 AD 与 tape 实现；micrograd → PyTorch autograd。
- ML 系统栈：API → 图 → 算子库 → 运行时 → 硬件。

## L3 张量与硬件加速器
- 张量格式（layout/NCHW vs NHWC）对内核效率的影响。
- MatMul 是性能基石：GEMM 与 roofline；GPU/TPU 加速器谱系。

## L4 GPU 与 CUDA
- 线程层级（grid/block/warp）与存储层级（寄存器/共享/HBM）。
- 基本性能模型：占用率、合并访存、kernel 启动开销。

## L5 GPU MatMul 与算子编译
- 分块 GEMM 与双缓冲；cuBLAS/CUTLASS 设计。
- 算子编译：从调度到代码生成。

## L6 Triton 编程
- 块级编程模型：program_id/掩码/自动内存优化。
- 用 Triton 写 fused softmax 与 attention kernel。

## L7 图优化与编译
- 算子融合（垂直/水平）、布局变换、常量折叠。
- torch.compile / TVM 的图-算子联合优化。

## L8 内存
- 训练内存大头：激活/梯度/优化器状态；重计算与 offload。
- 推理内存：KV cache 管理与碎片；PagedAttention 动机。

## L9 量化
- PTQ/QAT、权重/激活/权激联合；INT8/INT4/FP8。
- LLM 场景：AWQ/GPTQ/SmoothQuant 与系统落地路径。

## L10 并行 I
- 集合通信原语：all-reduce/all-gather/broadcast；环与树。
- 张量并行：列/行切分与通信模式；3D 并行组合。

## L11 并行 II
- 数据并行（DDP/ZeRO）+ 流水线并行（1F1B）。
- 自动并行：搜索策略空间（Alpa 思路）。

## L12 LLM 基础
- Transformer 前向的算力/访存剖析；注意力二次成本。
- MoE：专家并行与路由；推理显存-带宽权衡。

## L13 LLM 训练优化
- FlashAttention：IO 感知精确注意力与重计算。
- 训练稳定性：梯度裁剪、混合精度、checkpoint。

## L14 LLM 推理系统
- 批处理调度：静态 vs 连续；PagedAttention 显存分页。
- 分离式 prefill/decode（DistServe/Splitwise）与投机解码。

## L15 Scaling Law
- 损失 ~ 算力/参数/数据的幂律；Chinchilla 最优配比。
- 推理 scaling 与 overthinking 等 2024+ 新观察。

## L16-L19 Guest 专题
- ML compiler 前沿；LLM 预训练与开放科学。
- 快速推理（量化/稀疏/缓存）；tool use & agents 系统。
