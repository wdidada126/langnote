# 李宏毅机器学习 2025 提纲

> 骨架级要点；旧版传统 DL 章节（Regression/CNN/GAN/BERT/攻击/元学习等）作为自学专题另行归档。

## L0 课程说明与自学章节
- 2025 版假设已自学基础章节：回归、分类、梯度下降、反向传播、卷积。
- 旧版 15 个 Lab 是知识索引：异常检测、可解释 AI、攻击、适应、压缩、终身学习、元学习。
- 作业均给助教范例代码，重点在"改"而非"搭"。

## L1 ChatGPT 原理
- 三阶段：预训练（生成下一个 token）→ 指令微调 → RLHF。
- 为什么 next-token prediction 涌现出对话与推理能力。
- GPT 是"只读"的：模型知识冻结在参数中。

## L2 提示工程与思维链
- zero-shot → few-shot → CoT → 自洽性（Self-Consistency）投票。
- 提示是"程序"，模型是"解释器"；提示注入攻击的雏形。
- 推理模型（o1/R1）把 CoT 内化进训练。

## L3 Transformer 架构
- 自注意力 QKV 与多头；因果掩码。
- 位置编码演进：绝对 → 相对 → RoPE → ALiBi。
- Encoder-only（BERT）vs Decoder-only（GPT）两种预训练目标。

## L4 解码与生成
- greedy/beam 在开放式生成中退化；温度、top-k、top-p。
- 重复问题与采样策略（min-p、repetition penalty）。
- 结构化输出：约束解码/JSON mode。

## L5 工具使用
- Toolformer：模型自学何时调用 API。
- Function Calling 作为"模型输出 → 程序执行"的协议。
- 检索也是一种工具。

## L6 RAG 检索增强生成
- 动机：知识更新、溯源、私有数据，绕开重训。
- 流水线：分块 → 向量化 → 召回 → 重排 → 注入生成 → 端到端评估。
- GraphRAG、HyDE 等变体；RAG vs 长上下文 vs 微调的取舍。

## L7 AI Agent
- ReAct：推理与行动交替循环。
- 规划（Plan-and-Solve）、反思（Reflexion）、记忆（短期/长期）。
- 多智能体协作与任务分解；Agent 评估（基准与真实收益）。

## L8 微调与高效适配
- LoRA 低秩假设；QLoRA 4bit 基座。
- 指令微调数据构造（Self-Instruct）。
- 蒸馏与更小模型路线。

## L9 长上下文与效率
- KV cache 显存瓶颈；PagedAttention（vLLM）。
- 稀疏/线性注意力、滑动窗口。
- 量化：GPTQ/AWQ/INT8；投机解码。

## L10 多模态
- CLIP 对比学习对齐图文；ViT 图像切块。
- LLaVA 式"视觉投影 + LLM 主干"。
- 视觉 tokenizer 与生成（扩散头）。

## L11 LLM 评估
- benchmark 污染与过拟合；MMLU/GSM8K/HumanEval。
- LLM-as-a-judge 的偏差（位置、冗长偏好）。
- 人工评估与 A/B 仍是金标准。

## L12 安全与对齐
- 越狱攻击（提示注入、编码绕过）与防御。
- RLHF 的奖励黑客；DPO 直接偏好优化。
- 水印与可追溯性。

## L13 前沿：推理模型
- RL + 可验证奖励（数学/代码）训练长思维链。
- GRPO（DeepSeek-R1）：去掉 critic 的组内相对基线。
- test-time compute 换性能的新 scaling 维度。
