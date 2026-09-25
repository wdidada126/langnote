# CMU 15-442 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Automatic Differentiation in Machine Learning: a Survey (Baydin et al.) | 2018 | L2 | AD 前向/反向模式系统综述 |
| TensorFlow: A System for Large-Scale ML (ABADI et al., OSDI) | 2016 | L3 | 数据流图与分布式训练框架 |
| PyTorch: An Imperative Style, High-Performance DL Library | 2019 | L3 | 动态图 autograd 主流实现 |
| Distributed Deep Learning with Objective Communication / —（Ring All-Reduce via Baidu/sergeev 1710） | 2017 | L8 | Ring-AllReduce 带宽最优 |
| Scaling Distributed Deep Learning with SGC / —（Megatron-LM, Shoeybi et al.） | 2019 | L10 | 张量模型并行 3D 并行 |
| GPipe: Efficient Scaling of Gradient-Based ML with Pipeline Parallelism (Huang et al.) | 2019 | L10 | 流水线并行与 micro-batch |
| ZeRO: Memory Optimizations Toward Training Trillion Parameter Models (Rajbhandari et al.) | 2020 | L9 | 三级参数/梯度/优化器分片 |
| TVM: An Automated End-to-End Optimizing Compiler (Chen et al., OSDI) | 2018 | L7 | 算子调度 + 自动调优编译 |
| Ansor: Generating High-Performance Tensor Programs (Zheng et al., ASPLOS) | 2020 | L7 | 自动调度搜索 |
| Roofline: An Insightful Visual Performance Model (Williams et al.) | 2009 | L4/L6 | 计算/访存瓶颈判定 |
| Addresing the Memory Wall / —（cuBLAS/CUTLASS 技术文档） | — | L6 | GEMM 与 TMA/Warp-Specialization |
| Mixed Precision Training (Micikevicius et al.) | 2018 | L13 | FP16 训练与 loss scaling |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| Efficient Memory Management for LLM Serving: PagedAttention (vLLM, Kwon et al., SOSP) | 2023 | L11 连续批处理/KV cache 分页 |
| FlashAttention / v2 / v3 (Dao et al.) | 2022-2024 | L6/L12 IO 感知精确注意力 |
| SGLang: Efficient Execution of Structured LM Programs (RadixAttention) | 2024 | L11 前缀复用与程序级调度 |
| DistServe / Splitwise: Disaggregating Prefill and Decoding | 2024 | L12 prefill/decode 分离 |
| Accelerating LM Generation with Speculative Decoding (Leviathan et al., ICML) | 2023 | L12 投机解码 |
| Alpa: Automating Inter- and Intra-Operator Parallelism (OSDI) | 2022 | L10 自动并行 |
| GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers | 2022 | L13 权重量化 |
| AWQ: Activation-aware Weight Quantization (MLSys) | 2023 | L13 量化 |
| MegaScale / —（Mega-Kernel 类工作，如 "Low-Latency... MegaKernel"） | 2024-2025 | L14 整网单 kernel |
| DeepSeek-V3 Technical Report (FP8/MoE) | 2024 | L9/L13/L14 训练系统 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 自动微分（L2） | PyTorch / JAX / tinygrad | autograd 引擎与 vmap/jit |
| 框架运行时（L3） | PyTorch C10 / MLX / ExecuTorch | dispatcher 与多后端 |
| GEMM / TIRx（L5-6） | CUTLASS / cuBLAS / Triton / TVM | GPU 算子生成与调优 |
| ML 编译（L7） | Apache TVM / torch.compile (Inductor) | 图与算子联合优化 |
| 数据并行（L8） | DeepSpeed / PyTorch DDP / Horovod | All-Reduce 重叠与分桶 |
| ZeRO/FSDP（L9） | DeepSpeed ZeRO / PyTorch FSDP | 参数分片与 offload |
| 张量/流水线并行（L10） | Megatron-LM / DeepSpeed / Alpa | 3D 并行与调度 |
| LLM 推理（L11-12） | vLLM / SGLang / TensorRT-LLM / MLC-LLM | PagedAttention、连续批处理、投机解码 |
| 量化（L13） | GPTQ-for-LLaMa / AWQ / TensorRT / bitsandbytes | INT4/FP8 部署 |
| Mega-Kernel（L14） | FlashInfer / 研究性 kernel 引擎 | 融合解码内核 |
