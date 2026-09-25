# CMU 15-779 论文清单

## 经典论文（ML 系统主线）

| 主题 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| 计算图/框架 | TensorFlow / PyTorch（Automatic Differentiation in PyTorch） | 2016/2017 | L1 |
| GPU | Programming Massively Parallel Processors（教材）+ CUDA 指南 | - | L2 |
| Attention | FlashAttention / FA2 / FA3 | 2022/2023/2024 | L3 案例核心 |
| Tile DSL | Triton: Intermediate GPU Compiler | 2019 | L5 |
| 内核调优 | TVM / Ansor: Generating High-Performance Tensor Programs | 2018/2020 | L6 |
| 图优化 | TASO: Automating GPU Graph Transformations / PET | 2019/2021 | L7 |
| 超优化 | Mirage: A Superoptining Compiler for Datacentric DAGs | 2024-25 | L7 |
| 数据并行 | Large-Scale Distributed DNN Using Synchronized SGD / ZeRO 三部曲 | 2014/2019-20 | L8 |
| 张量并行 | Megatron-LM | 2019 | L9 |
| 流水线 | GPipe / PipeDream | 2018/2019 | L9 |
| 自动并行 | Alpa: Automating Inter/Intra-Operator Parallelism | 2022 | L10 |
| 服务 | Orca: Distributed Serving (OSDI'22) / vLLM (PagedAttention, SOSP'23) | 2022/2023 | L12 |
| 前缀缓存 | SGLang / RadixAttention | 2024 | L12 |
| 投机解码 | Speculative Decoding (Leviathan) / SpecInfer | 2022/2023 | L13 |
| 长上下文 | Ring Attention / LongNet | 2023 | L11 |
| MoE | GShard / Switch Transformer / MegaBlocks | 2020/2022 | L15 |
| PEFT | LoRA / QLoRA | 2021/2023 | L14 |
| RLHF 系统 | InstructGPT / veRL(HybridEngine) | 2022/2024 | L14 |
| 显存优化 | Gradient Checkpointing (Chen et al.) / Selective Recompute | 2016/2020 | L8-L9 |
| 多LoRA服务 | S-LoRA / Punica | 2023 | L14 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| DeepSeek-V2/V3（MLA、FP8、MoE 基础设施） | 2024-25 | KV 低秩压缩与超大规模训练系统样本 |
| DeepSeek-R1 / o1（推理模型） | 2024-25 | 长思维链对服务调度/批处理的新挑战 |
| Mixtral / 稀疏专家服务化 | 2024 | MoE kernel 与路由开销 |
| FA3 / FlashInfer | 2024-25 | Hopper 异步 kernel、服务级 attention 库 |
| TileLang | 2024-25 | 新一代 tile DSL |
| MegaScale / 万卡集群实践 | 2024 | 训练容错、网络与并行工程 |
| DistServe / Splitwise（prefill/decode 分离） | 2024 | 服务架构解耦 |
| EAGLE-2/3、Medusa | 2024-25 | 投机解码实用化 |
| Mooncake（Kimi 服务架构） | 2024-25 | PD 分离 + KV 池化 |
| Sarathi-Serve（chunked prefill） | 2024 | 调度混批 |
| 稀疏注意力（NSA、MInference） | 2025 | 长上下文推理加速 |
| Mirage/超优化进入 LLM kernel | 2025 | L7 前沿 |
| Sora/流匹配生成系统的服务化（对照 diffusers 栈） | 2024-25 | 非自回归生成的系统差异 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| 计算图与执行 | PyTorch 2/XLA、MLC-LLM | L1/L7 |
| CUDA kernel | FlashAttention、CUTLASS、flashinfer | L2-L4 |
| Triton 算子 | triton 官方 tutorials、vLLM kernels、TorchTune | L5 |
| 自动调优 | Ansor（TVM）、NVIDIA cutlass profiler | L6 |
| 图级优化 | TASO、MLC、Mirage | L7 |
| 分布式训练 | DeepSpeed、Megatron-LM、torchtitan、Megatron-Core | L8-L10 |
| 自动并行 | Alpa | L10 |
| 长上下文 | RingAttention 开源实现、flash-attn varlen | L11 |
| LLM 服务 | vLLM、SGLang、TensorRT-LLM、LMDeploy | L12 |
| 推理加速 | speculative-decoding 实现（vLLM spec decode）、KV 压缩库 | L13 |
| 后训练 | veRL、OpenRLHF、PEFT、FastDM/多 LoRA 服务 | L14 |
| MoE | Megatron-Core MoE、MegaBlocks、KTransformers 专家 offload | L15 |
| 全链路对照 | transformers（模型层）、diffusers（生成服务层） | 课程视角延伸 |
