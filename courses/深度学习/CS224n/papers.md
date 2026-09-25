# CS224n 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| A Neural Probabilistic Language Model (Bengio) | 2003 | L1 | 分布式表示语言模型起点 |
| word2vec | 2013 | L2 | 预测式词向量 |
| GloVe | 2014 | L2 | 全局共现词向量 |
| Seq2Seq Learning with Deep NNs | 2014 | L4 | encoder-decoder 翻译 |
| Effective Approaches to Attention (Luong) | 2015 | L5 | 注意力变体系统研究 |
| Bahdanau Attention | 2014 | L5 | 软对齐解决瓶颈 |
| Attention Is All You Need | 2017 | L6 | Transformer |
| BERT | 2018 | L8 | MLM 预训练+微调 |
| ELMo | 2018 | L9 | 上下文化词向量 |
| The Curious Case of Neural Text Degeneration (Nucleus) | 2019 | L10 | top-p 采样 |
| GPT-3 | 2020 | L11 | few-shot in-context |
| Neural Machine Translation of Rare Words with Subword Units (BPE) | 2015 | L4 | 子词切分标配 |
| Training LMs with Human Feedback (InstructGPT) | 2022 | L13 | RLHF 范式 |
| LoRA | 2021 | L14 | 低秩微调 |
| CLIP | 2021 | L15 | 图文对比学习 |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| Chain-of-Thought Prompting | 2022 | L12 推理提示 |
| Chinchilla (Compute-Optimal Training) | 2022 | L11 缩放定律 |
| FlashAttention | 2022 | L6/L11 训练效率 |
| DPO | 2023 | L13 直接偏好优化 |
| LLaMA 1/2/3 | 2023-2024 | L11 开源 LLM 主干 |
| Mixtral (Sparse MoE) | 2024 | L11 稀疏专家 |
| DeepSeek-R1 | 2025 | L12 RL 训练推理 |
| Qwen2.5 / GPT-4o 技术报告 | 2024-2025 | L15 多模态现役 |
| SGLang/Continuum 类 agent 记忆研究 | 2024-2025 | L17 前沿：智能体 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 词向量（L2） | gensim / GloVe 官方 C 实现 | 计数/预测嵌入库 |
| Transformer/NMT（L4-L7） | HuggingFace transformers / OpenNMT-py | encoder-decoder 标准件 |
| BERT 微调（L8） | HF transformers Trainer / sentence-transformers | 微调与句向量生态 |
| 解码（L10） | transformers generate / vLLM sampling | 采样/束搜索/约束解码 |
| GPT 推理（L11） | vLLM / llama.cpp / SGLang | 高吞吐自回归服务 |
| 对齐（L13） | TRL / OpenRLHF / veRL | SFT/RM/PPO/DPO 训练环 |
| PEFT（L14） | PEFT 库 / QLoRA | LoRA 即插即用 |
| 多模态（L15） | LLaVA / Qwen2-VL / open_clip | 视觉投影+LLM |
