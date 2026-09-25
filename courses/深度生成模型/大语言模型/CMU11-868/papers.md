# CMU 11-868 论文清单

## 经典论文

| 主题 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| Transformer | Attention Is All You Need (Vaswani et al.) | 2017 | L2 架构起点 |
| GPT 系列 | Language Models are Unsupervised Multitask Learners (GPT-2) | 2019 | A2 复现对象 |
| GPT 系列 | Language Models are Few-Shot Learners (GPT-3) | 2020 | 缩放与 ICL |
| GPT 系列 | InstructGPT (Training LMs to Follow Instructions, Ouyang et al.) | 2022 | RLHF 三阶段范式 |
| RLHF | Training language models to follow instructions with human feedback | 2022 | L15 对齐系统蓝本 |
| RLHF | Deep RL from Human Preferences (Christiano et al.) | 2017 | 奖励建模源头 |
| LLaMA | LLaMA / Llama 2 / Llama 3 技术报告 | 2023-24 | 开源基线与数据配方 |
| 缩放律 | Chinchilla (Training Compute-Optimal LMs, Hoffmann et al.) | 2022 | 训练算力分配 |
| 注意力 | FlashAttention / FlashAttention-2 | 2022-23 | L8 IO-aware 优化 |
| 分布式 | ZeRO / ZeRO-2 / ZeRO-3 | 2019-20 | L9 数据并行分片 |
| 分布式 | Megatron-LM (Tensor Parallelism) | 2019 | L10 张量并行 |
| 流水线 | GPipe / PipeDream | 2018-19 | L10 流水线调度 |
| 编译器 | TorchInductor/JAX-XLA 相关论文；Triton (Google) | 2021-24 | L6 编译优化 |
| MoE | Switch Transformers / GShard | 2021-22 | L12 稀疏化 |
| 量化 | GPTQ / SmoothQuant / LLM.int8() | 2022-23 | L13 压缩 |
| PEFT | LoRA / QLoRA | 2021-23 | L14 高效微调 |
| 推理系统 | vLLM: Efficient Memory Management for LLM Serving (PagedAttention) | 2023 | L16 服务化核心 |
| 推理系统 | Orca (OSDI'22) | 2022 | 连续批处理先声 |
| 投机解码 | Speculative Decoding (Leviathan et al.) | 2023 | L17 |
| 并行化 | Alpa / GSPMD | 2022 | L11 自动并行 |
| 梯度检查点 | Training Deep Nets with Sublinear Memory Cost (Chen et al.) | 2016 | 长上下文显存利器 |
| 位置编码 | RoFormer (RoPE) | 2021 | 长上下文外推 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| Mixtral of Experts | 2024 | 开源 MoE 标杆，稀疏服务成本账 |
| DeepSeek-V2/V3 | 2024-25 | MLA 低秩 KV、FP8 训练、大规模 MoE 基础设施 |
| DeepSeek-R1 / o1 类推理模型 | 2024-25 | GRPO 后训练；长思维链对推理系统的冲击 |
| Sora 技术报告（视频生成） | 2024 | 扩散/流匹配系统栈，跨模态基础设施参照 |
| Flux / SD3（整流流） | 2024 | 生成模型系统化的工程实现 |
| Medusa / EAGLE-2/3 | 2024-25 | 多草稿头投机解码主流方案 |
| SGLang / RadixAttention | 2024 | 前缀树 KV 复用与程序化 LLM 服务 |
| Sarathi-Serve / chunked prefill | 2023-24 | prefill/decode 混批调度 |
| MegaScale / 万卡训练实践 | 2024 | 超大规模训练故障与网络工程 |
| veRL / OpenRLHF | 2024-25 | HybridEngine 共卡放置的 RLHF 训练栈 |
| 长上下文系统（Ring Attention、Infini-attention） | 2023-25 | 百万 token 上下文的并行与缓存 |
| KV Cache 压缩（H2O、SnapKV、KIVI） | 2023-25 | 服务侧显存治理 |
| 多模态服务与交错推理（LLaVA-One 类） | 2024-25 | 视觉 token 压缩 |
| TensorRT-LLM / 编译化推理 | 2023-25 | 图编译 + 量化 kernel 全栈 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| CUDA 算子/融合 kernel | FlashAttention、CUTLASS、Triton 教程 | fused attention、Triton 版 softmax/LN |
| 自动微分与框架 | miniTorch（课程自用）、PyTorch ATen | A1/A3 作业直接对应 |
| 模型编译 | TorchInductor、XLA、TVM、MLC-LLM | 图融合与 kernel 生成 |
| 分布式训练 | DeepSpeed（ZeRO）、Megatron-LM、torchtitan | L9-L11 全部主线 |
| 自动并行 | Alpa、GSPMD/JAX | L11 |
| MoE | Megatron-Core MoE、Mixtral/megablocks、vLLM MoE | L12 |
| 量化 | AutoGPTQ、AWQ、TensorRT-LLM quantization、llama.cpp | L13 |
| PEFT | PEFT (HuggingFace)、QLoRA 实现 | L14 |
| RLHF 系统 | veRL、OpenRLHF、TRL、Distributed Fused Agent | L15 |
| LLM 服务 | vLLM、SGLang、TensorRT-LLM、CacheGen、llama.cpp | L16-L17 |
| RAG | LangChain/LlamaIndex、FAISS/Milvus | L18 |
| 多模态 | LLaVA、Qwen2-VL、vLLM 多模态支持 | L19 |
| Agent 运行时 | OpenHands、SWE-agent、MCP 生态 | L20 |
| 生成侧（对照） | diffusers（扩散服务的 batching 特殊性） | L16/L19 延伸 |
