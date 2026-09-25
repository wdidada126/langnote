# NeuralNets-ZeroToHero 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Learning representations by back-propagating errors (Rumelhart/Hinton/Williams) | 1986 | L1-L2 | 反向传播成为训练多层网络的标准方法 |
| A Neural Probabilistic Language Model (Bengio et al.) | 2003 | L4/L6 | 分布式词表示 + MLP 语言模型，embedding 思想源头 |
| Adam: A Method for Stochastic Optimization (Kingma & Ba) | 2015 | L9 | 动量+自适应步长，nanoGPT 默认优化器（AdamW） |
| Language Models are Unsupervised Multitask Learners (GPT-2) | 2019 | L10 | 零样本多任务能力，本课复现对象 |
| Attention Is All You Need (Vaswani et al.) | 2017 | L7 | Transformer 架构原始定义 |
| Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau) | 2014 | L7 | 注意力机制起源 |
| Layer Normalization (Ba/Kiros/Hinton) | 2016 | L7 | Transformer 内部标准归一化 |
| Improved Techniques for Training Consistent Networks (He et al., GELU/残差相关) | 2016 | L7 | 残差连接与预激活训练技巧 |
| Byte Pair Encoding: Neural Machine Translation of Rare Words with Subword Units (Sennrich et al.) | 2016 | L8 | BPE 分词算法原始论文 |
| Language Models are Few-Shot Learners (GPT-3) | 2020 | L9 | few-shot 范式，理解规模化的意义 |
| RoFormer: Enhanced Transformer with Rotary Position Embedding (Su et al.) | 2021 | L7 | 现代 LLM 普遍采用的旋转位置编码 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| Chinchilla: Training Compute-Optimal Large Language Models | 2022 | L9/L10 数据-参数最优配比 |
| LoRA: Low-Rank Adaptation of Large Language Models | 2021 | L9 参数高效微调 |
| InstructGPT: Training language models to follow instructions | 2022 | L9/L11 SFT+RLHF 三段式 |
| LLaMA 系列 (1/2/3) | 2023-2024 | L7/L10 开源复现主线 |
| FlashAttention / v2 / v3 | 2022-2024 | L7 注意力 IO 优化 |
| Mamba: Linear-Time Sequence Modeling with Selective State Spaces | 2023 | L7 Transformer 替代架构 |
| Direct Preference Optimization (DPO) | 2023 | L11 免 RM 对齐 |
| GPT-4 Technical Report | 2023 | L11 能力边界讨论 |
| DeepSeek-V3 Technical Report | 2024/25 | L9/L10 MoE+MLA 训练实践 |
| nanochat / llm.c（Karpathy 项目技术内容） | 2024-2025 | L12 全栈复现 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 标量自动微分（L1-L2） | PyTorch / micrograd / llm.c | autograd 引擎与 CUDA 反向核的最小模型 |
| 交叉熵与 softmax（L4） | scikit-learn / PyTorch | `nn.CrossEntropyLoss`、`log_softmax` 数值稳定实现 |
| Transformer 块（L7） | llama.cpp / vLLM / HuggingFace transformers | QKV 融合、KV cache、RoPE 生产实现 |
| BPE 分词（L8） | HuggingFace tokenizers / tiktoken | GPT 系列 tokenizer 训练与 Rust 加速 |
| 训练循环与 AdamW（L9） | nanoGPT / LitGPT / torchtitan | 混合精度、梯度裁剪、DDP 训练配方 |
| 复现与对齐（L10） | llm.c / Koroko / GPT-2 checkpoint 复刻 | 逐层对齐官方权重做行为验证 |
| 对齐与推理（L11） | OpenAI API / Ollama / LM Studio | SFT/RLHF 产物作为对话模型部署 |
