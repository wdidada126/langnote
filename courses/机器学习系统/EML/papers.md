# MIT 6.5940 (EML) 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Deep Compression: Squeezing NNs with Pruning, Distilled Training and Quantized Training (Han et al., ICLR) | 2016 | L2/L4 | 剪枝+量化+蒸馏三件套，TinyML 开山 |
| Learning both Weights and Connections for Efficient NNs (Han et al., NIPS) | 2015 | L2 | 迭代幅度剪枝 |
| Distilling the Knowledge in a Neural Network (Hinton et al.) | 2015 | L2/L10 | 知识蒸馏原始论文 |
| The Lottery Ticket Hypothesis (Frankle & Carlini, ICLR) | 2019 | L2 | 稀疏子网存在性 |
| Neural Architecture Search with Reinforcement Learning (Zoph & Le) | 2017 | L3 | RL 搜索架构 |
| MobileNets / ShuffleNet / EfficientNet | 2018-2019 | L3 | 轻量架构三部曲 |
| DARTS: Differentiable Architecture Search (Liu et al.) | 2019 | L3 | 可微 NAS |
| Quantization for Deep Learning: A Survey (Jacob et al.) | 2018 | L4 | 量化方法学综述 |
| Eyeriss: An Energy-Efficient Reusable Accelerator (JSSC) | 2016 | L6 | 数据流加速器 |
| A Functional Taxonomy of Deep Learning Accelerators (Jouppi TPU 延伸 / Molchanov 剪枝) | — | L6 | 加速器谱系 |
| Sparse Winograd / — 替代：Inference Efficiency for DL (Han et al., IEEE Micro) | 2017 | L2 | 稀疏推理 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| AWQ: Activation-aware Weight Quantization for LLM (MLSys) | 2023 | L8 权重量化 |
| GPTQ: Accurate Post-Training Quantization for GPT | 2022 | L8 PTQ |
| SmoothQuant: Accurate and Efficient Post-Training Quantization (ICML) | 2022 | L8 离群值迁移 |
| LLM.int8(): 8-bit Matrix Multiplication for Transformers (NeurIPS) | 2022 | L8 混合精度分解 |
| LLM in a flash: Efficient LLM Inference using Windowed Near-flash (Microsoft) | 2023 | L9 权重存放 |
| vLLM: Efficient Memory Management for LLM Serving (SOSP) | 2023 | L9 PagedAttention |
| Fast Inference from Transformers via Speculative Decoding (ICML) | 2023 | L9 投机解码 |
| SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot | 2023 | L2 大模型剪枝 |
| Wanda: Pruning by Weights and Activations | 2023 | L2 剪枝准则 |
| Once-for-All: Train One Network and Specialize it (Tenzer et al.) | 2020 | L3 |
| Mixtral of Experts (MoE 高效 LLM) | 2023 | L13 MoE |
| A Survey on Efficient Training of Transformers (MLSys) | 2023 | L12-L13 |
| Mamba: Linear-Time Sequence Modeling | 2023 | L7 线性时间序列 |
| StreamingLLM / 长上下文高效注意力 | 2023 | L7 长上下文 |
| Consistency Models / 扩散加速 (Song et al.) | 2023 | L11 扩散加速 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 剪枝/稀疏（L2） | TorchSparse / NVIDIA Sparse Tensor Core / SparseML | 稀疏权重存储与计算 |
| NAS（L3） | MNN / NNI / Once-for-All / PP-TinyNAS | 搜索框架与端侧模型生成 |
| 量化（L4/L8） | llama.cpp / bitsandbytes / AutoGPTQ / TensorRT / GPTQ-for-LLaMa | INT8/INT4/NF4 推理 |
| TinyML（L5） | TFLite Micro / ExecuTorch / Edge Impulse / ml-cpp | MCU 部署运行时 |
| 高效芯片（L6） | Vitis AI / NVDLA / 端侧加速器 | 数据流编译栈 |
| 高效注意力（L7/L9） | FlashAttention / vLLM / HuggingFace attn implementations | IO 感知与 KV 管理 |
| MoE 训练（L13） | MegaBlocks / Tutel / vLLM MoE | 稀疏激活与专家并行 |
| 蒸馏/对齐（L11） | DistillKit / TRL / NeMo | 后训练加速 |
