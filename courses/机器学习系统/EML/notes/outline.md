# MIT 6.5940 (EML) 提纲

> 骨架级要点，正文笔记待逐讲展开。

## L1 导论
- 深度学习的三堵墙：算力、内存、能耗；端侧/大模型两种极端场景。
- 效率指标：FLOPs、参数量、MAC、能耗/比特、延迟与吞吐。

## L2 剪枝
- 非结构化剪枝（幅度阈值+迭代重训）→ Deep Compression。
- 结构化剪枝（通道/头/层）与硬件友好性权衡。
- Lottery Ticket：稀疏子网络存在性假设。

## L3 NAS 与轻量架构
- 搜索空间/策略/评估三要素；可微分 DARTS。
- 代表架构：MobileNet(深度可分离卷积)、ShuffleNet(通道洗牌)、EfficientNet(复合缩放)。
- Once-for-All 与训练一次弹射多子网。

## L4 量化
- 权重量化/激活量化/权激联合；对称 vs 非对称、逐通道 vs 逐张量。
- PTQ vs QAT；量化误差与 MSE 最小化。
- 混合精度分配（敏感层保留高精度）。

## L5 TinyML：MCU 部署
- 模型到 MCU：内存/算力约束下的压缩-编译-调度流水线。
- 工具链：TFLite Micro / ExecuTorch / Edge Impulse。
- 案例：关键词唤醒、手势识别。

## L6 高效芯片与系统
- 数据流架构（Eyeriss/TPU）、脉动阵列、片上 SRAM 复用。
- 稀疏计算硬件与近存计算趋势。

## L7 高效 Transformer
- 自注意力 O(n²) 瓶颈；稀疏/低秩/核近似三类路线。
- 长上下文：滑窗、RoPE 外推、KV cache 压缩。

## L8 LLM 推理 I：量化
- LLM.int8 的混合精度分解；GPTQ 基于 Hessian 的逐层量化。
- AWQ 激活感知保护显著权重；SmoothQuant 离群值迁移。

## L9 LLM 推理 II：系统
- vLLM/PagedAttention 消除 KV 碎片；连续批处理。
- 投机解码（draft-verify）；LLM in a flash（NOR-FLASH 权重存放）。

## L10 多模态与视觉效率
- ViT 压缩与蒸馏；MLLM（LLaVA 系）推理成本剖析。
- 图像编码器小型化路线。

## L11 生成模型加速
- 扩散采样加速：蒸馏一致性模型、少步采样。
- GAN/VAE 推理优化的代表工作。

## L12 高效训练 I：并行
- DP/TP/PP/ZeRO 组合；流水线 1F1B bubble。
- 通信-计算重叠与拓扑感知。

## L13 高效训练 II：通信与 MoE
- 梯度压缩（top-k/量化）；All-Reduce 替代方案。
- MoE 系统：专家并行、路由负载不均衡、GShard/Switch。

## L14 端侧训练与前沿
- Split learning/联邦高效训练；片上微调。
- 总结：模型-算法-硬件协同设计方法论。
