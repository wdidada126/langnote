# UCSD CSE234 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Automatic Differentiation in Machine Learning: a Survey (Baydin et al.) | 2018 | L2 | AD 模式选择理论依据 |
| Roofline: An Insightful Visual Performance Model (Williams et al.) | 2009 | L3-L4 | 计算/访存瓶颈判定 |
| Tiled/Blocked GEMM 经典（Goto & Van de Geijn GEMM 设计） | 2008 | L5 | 分块 + 双缓冲的高性能 GEMM |
| Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations (Tillet et al., MAPL) | 2019 | L5-L6 | 块级 DSL 降低 GPU 门槛 |
| TVM: An Automated End-to-End Optimizing Compiler (OSDI) | 2018 | L7 | 图-算子联合编译 |
| Gradient Checkpointing (Chen et al.) | 2016 | L8 | 激活重计算省内存 |
| ZeRO: Memory Optimizations Toward Training Trillion Parameter Models | 2020 | L8/L11 | 优化器/梯度/参数分片 |
| Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism | 2019 | L10 | 张量模型并行 |
| GPipe: Efficient Scaling using Pipeline Parallelism | 2019 | L10-L11 | 流水线并行 |
| Attention Is All You Need (Vaswani et al.) | 2017 | L12 | Transformer 原始论文 |
| Outrageously Large Neural Networks: The Sparsely-Gated MoE (Shazeer et al.) | 2017 | L12 | MoE 奠基 |
| Scaling Laws for Neural Language Models (Kaplan et al.) | 2020 | L15 | 幂律 scaling 原始观察 |
| Horovod: distributed training framework (Shoeybi? 实为 Alexander Sergeev) | 2017 | L10 | 环形 all-reduce 数据并行 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| FlashAttention / v2 / v3 (Dao et al.) | 2022-2024 | L13 IO 感知注意力 |
| Alpa: Automating Inter- and Intra-Operator Parallelism (OSDI) | 2022 | L11 自动并行 |
| Mixtral of Experts | 2023 | L12 现代 MoE LLM |
| Efficient Memory Management for LLM Serving: PagedAttention (vLLM, SOSP) | 2023 | L14 KV cache 分页 |
| SGLang: RadixAttention 结构化程序执行 | 2024 | L14 前缀复用 |
| DistServe: Disaggregating Prefill and Decoding | 2024 | L14 分离式部署 |
| Splitwise: Efficient distributed LLM inference using phase splitting (ISCA) | 2023 | L14 |
| Chinchilla: Training Compute-Optimal LLMs | 2022 | L15 最优数据-参数配比 |
| GPTQ / AWQ / SmoothQuant | 2022-2023 | L9 LLM 量化 |
| Fast Inference from Transformers via Speculative Decoding (ICML) | 2023 | L14 投机解码 |
| MegaScale / 大规模训练系统实践类 | 2024 | L10-L11 训练系统 |
| DeepSeek-V3 Technical Report | 2024/25 | L9/L10/L13 训练与推理系统综合 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 计算图/AD（L1-L2） | micrograd / PyTorch autograd | 最小可运行 autograd |
| MatMul/Triton（L5-L6） | Triton 官方教程 / FlagGems / liger-kernel | fused attention/softmax kernel |
| 图编译（L7） | torch.compile (Inductor) / TVM | 融合与布局优化 |
| 内存优化（L8） | DeepSpeed ZeRO / PyTorch FSDP | 分片与 offload |
| 并行（L10-L11） | Megatron-LM / DeepSpeed / torchtitan / Alpa | 3D 并行与自动策略 |
| FlashAttention（L13） | FlashAttention 库 / HF transformers 集成 | IO 感知精确注意力 |
| LLM 推理（L14） | vLLM / SGLang / TensorRT-LLM / nano-vllm | 连续批处理/PagedAttention/分离式 |
| Scaling（L15） | nanogpt 训练配方 / llm.c | 训练配方的工程体现 |
