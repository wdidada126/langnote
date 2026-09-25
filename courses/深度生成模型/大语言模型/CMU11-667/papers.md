# CMU 11-667 论文清单

## 经典论文（LLM 方法与涌现基础）

| 主题 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| Transformer | Attention Is All You Need | 2017 | L2 |
| 预训练 | BERT | 2018 | 双向预训练范式 |
| GPT 系列 | GPT / GPT-2 / GPT-3 | 2018/2019/2020 | L3-L7 主线，GPT-3 引出 ICL |
| 缩放律 | Scaling Laws for Neural LMs (Kaplan) | 2020 | L4 |
| 缩放律 | Chinchilla | 2022 | L4 修正 |
| 涌现 | Emergent Abilities of LLMs (Wei et al.) | 2022 | L7 |
| 涌现批判 | Are Emergent Abilities A Mirage? (Schaeffer) | 2023 | L7 争议 |
| ICL | Why Can GPT Perform In-Context Learning (von Moltke/Dai 等) | 2022-23 | L7 机制 |
| 指令微调 | Finetuned LMs are Zero-Shot Reasoners (FLAN) | 2021 | L5 |
| RLHF | InstructGPT | 2022 | L6 |
| DPO | Direct Preference Optimization | 2023 | L6 |
| CoT | Chain-of-Thought Prompting (Wei et al.) | 2022 | L8 |
| 自洽 | Self-Consistency | 2022 | L8 |
| ToT | Tree of Thoughts | 2023 | L8 |
| RAG | Retrieval-Augmented Generation (Lewis) | 2022 | L10 |
| 幻觉 | 事实性与幻觉综述类 | 2023-24 | L10 |
| 多模态 | CLIP / LLaVA | 2021/2023 | L15 |
| 解释性 | A Mathematical Framework for Transformer Circuits (Elhage) | 2021 | L13 |
| 解释性 | Induction Heads | 2022 | L13 |
| 评测 | HELM / Chatbot Arena | 2022/2023 | L11 |
| 偏见 | StereoSet / 反事实偏见框架 | 2020 | L14 |
| 安全 | Training the Underlying Model to be Robust / 越狱综述 | 2023 | L14 |
| Agent | ReAct / Reflexion | 2022-23 | L16 |
| LLaMA | LLaMA / Llama 2 / Llama 3 报告 | 2023-24 | 全课开源基线 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| GPT-4 技术报告 | 2023 | 多模态、能力跃迁与可控性 |
| Llama 2 / Llama 3 | 2023-24 | 开源可复现的对齐配方 |
| Qwen / Mistral 系列 | 2023-25 | 开源竞争与架构多样性 |
| Mixtral 8x7B | 2024 | 开源稀疏 MoE |
| DeepSeek-V3 / R1 | 2024-25 | 高效 MoE 训练 + GRPO 长思维链推理模型 |
| OpenAI o1 | 2024 | 测试时计算缩放范式确立 |
| Sora（视频生成） | 2024 | 扩散/流匹配生成，跨模态生成能力参照 |
| Flow Matching / Rectified Flow 在生成侧普及 | 2023-25 | 与 LLM 统一的生成视角（连接 MIT6.S184） |
| Sparse Autoencoders 大规模应用（Anthropic/OpenAI） | 2024-25 | 机制可解释性工程化 |
| 越狱与提示注入攻防 | 2023-25 | 安全对齐的持续对抗 |
| SWE-bench / GAIA 等长任务评测 | 2023-25 | Agent 能力量化 |
| 推理模型评测（AIME、GPQA、LiveBench） | 2024-25 | L8 前沿延伸 |
| 蒸馏小模型继承推理能力（DeepSeek-R1-Distill） | 2025 | L5/L12 交叉 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| Transformer/微调 | Hugging Face transformers、TRL、PEFT | L2/L5 复现 |
| 预训练数据 | dolma、Data-Juicer、NeMo-Curator | L3 数据管线 |
| 缩放律与训练 | nanotron、torchtitan、Megatron-LM | L4 训练配方 |
| 指令微调/对齐 | trl（SFT/DPO/PPO）、OpenRLHF、LLaMA-Factory | L5/L6 |
| CoT/推理 | LangChain、DSPy、STaR 实现 | L8 |
| RAG | LlamaIndex、LangChain、Haystack、FAISS | L10（A3 作业） |
| 评测 | lm-evaluation-harness、OpenCompass、HELM、promptfoo | L11 |
| 效率/蒸馏 | bitsandbytes、TensorRT-LLM、LLM-Blender 蒸馏工具 | L12 |
| 解释性 | TransformerLens、SAELens、NN-Surge | L13 |
| 安全 | promptfoo、Rebuff、 Lakera/Gandalf 类红队工具 | L14 |
| 偏见缓解 | Fairlearn、stereoset 工具、A4 作业栈 | L14 |
| 多模态 | LLaVA、Qwen-VL、CLIP 生态 | L15 |
| Agent | AutoGen、OpenHands、LangGraph、MCP | L16 |
