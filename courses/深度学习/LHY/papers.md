# 李宏毅机器学习 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Attention Is All You Need | 2017 | L3 | Transformer 奠基，本课一切的地基 |
| BERT | 2018 | L3/L8 作业 | Masked LM 双向预训练 |
| Language Models are Few-Shot Learners (GPT-3) | 2020 | L1/L2 | in-context learning 涌现 |
| Training LMs to Follow Instructions with Human Feedback (InstructGPT) | 2022 | L1/L12 | RLHF 三件套范式 |
| Chain-of-Thought Prompting (Wei et al.) | 2022 | L2 | 思维链提示显著提推理 |
| RAG: Retrieval-Augmented Generation (Lewis et al.) | 2020 | L6 | 检索器+生成器联合框架 |
| ReAct: Synergizing Reasoning and Acting | 2022 | L7 | 推理-行动交替的 Agent 原型 |
| Toolformer | 2023 | L5 | 自监督学会调用外部 API |
| LoRA: Low-Rank Adaptation | 2021 | L8 | 低秩增量微调，PEFT 事实标准 |
| CLIP | 2021 | L10 | 图文对比学习零样本分类 |
| An Image is Worth 16x16 Words (ViT) | 2020 | L10 | Transformer 通吃视觉 |
| GAN | 2014 | 旧版 Lab | 对抗训练生成（旧版作业） |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| QLoRA | 2023 | 4bit 基座 + LoRA 单卡微调 |
| LLaMA 1/2/3 | 2023-2024 | 开源可复现 LLM 主线 |
| FlashAttention 1/2/3 | 2022-2024 | 注意力 IO 感知优化 |
| GraphRAG (Microsoft) | 2024 | 图结构增强检索 |
| Self-Instruct | 2022 | 指令数据自动构造 |
| Direct Preference Optimization (DPO) | 2023 | 免奖励模型的偏好优化 |
| DeepSeek-V3 Technical Report | 2024 | MoE/MLA 工程与训练配方 |
| DeepSeek-R1 | 2025 | 纯 RL 涌现长思维链（GRPO） |
| Qwen2-VL / InternVL | 2024 | 开源多模态主力 |
| SWE-bench / AgentBench | 2023-2024 | Agent 程序化评估基准 |
| DSPy | 2023 | 把提示编译成可优化程序 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| RAG（L6） | LangChain / LlamaIndex / RAGFlow | 检索-重排-生成管线标准件 |
| Agent（L7） | AutoGPT / OpenManus / LangGraph | ReAct 循环与图编排 |
| 微调（L8） | HuggingFace TRL / LLaMA-Factory / PEFT | SFT/DPO/LoRA 全家桶 |
| KV cache 效率（L9） | vLLM / SGLang / llama.cpp | PagedAttention、量化、投机解码 |
| Function Calling（L5） | OpenAI/Anthropic tool API、MCP | 模型输出到执行的协议 |
| 多模态（L10） | Qwen2-VL、LLaVA 仓库 | 视觉投影 + LLM 主干实现 |
| RL 训练（L13） | veRL / OpenRLHF / TRL GRPOTrainer | 推理模型 RL 后训练 |
