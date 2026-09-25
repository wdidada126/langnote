# Stanford CS224n: Natural Language Processing 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS224n: Natural Language Processing with Deep Learning |
| 学校 | Stanford University |
| 主讲 | Christopher Manning（NLP 领域巨佬，Stanford AI Lab / SudoLab） |
| 教材 | 无指定教材；Speech and Language Processing（Jurafsky & Martin，第三版公开）为最佳伴读 |
| csdiy 路径 | `深度学习/CS224n`（页面更新：2025-06-07） |
| 最新期次 | 2025（课程官网最新一期；B 站有历届完整视频） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 80 小时；先修：深度学习基础 + Python |

## 为什么学

- NLP 深度学习最权威公开课程：从词向量一路讲到 Transformer、GPT 与对齐，正好横跨"前大模型"与"大模型"两个时代。
- 5 个编程作业循序渐进（词向量→word2vec→依存句法→机器翻译→Transformer 微调），大作业在 SQuAD 上训 QA 模型，历届有学生作业直接发顶会。
- Manning 的讲解是"把语言学直觉注入深度学习"的独一份体验，理解 LLM 为何有效的重要拼图。
- 资源汇总：@PKUFlyingPig 的全部资源与作业实现在 PKUFlyingPig/CS224n 仓库。

## 先修与知识联系

- 先修：CS230/CS231n 级别 DL 基础 + Python/PyTorch。
- 纵向：与 CS231n 共享 Transformer/视觉语言章节；向上衔接 CMU 11-711/11-667、LHY 2025 主线。
- 横向：词向量与嵌入章节和 CS224w（图嵌入）呼应；对齐（RLHF/DPO）章节是 CS285 的应用侧。

## 讲义章节目录（按 2025 公开课表整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | NLP 与深度学习导论 | Jurafsky&Martin ch.1-3（自学） |
| L2 | 词向量：word2vec 与负采样 | word2vec、GloVe 论文 |
| L3 | 依存句法与动态规划 | 早期神经网络句法分析论文 |
| L4 | vanilla 序列到序列机器翻译 | Seq2Seq (Sutskever) 论文 |
| L5 | 注意力机制（加性/乘性） | Bahdanau 论文 |
| L6 | Transformer：自注意力与多头 | Attention Is All You Need |
| L7 | Transformer 实践与作业讲解 | 课程 notes（transformers 部分） |
| L8 | 掩码语言模型：BERT 与 GPT 对比 | BERT、GPT-2/GPT-3 论文 |
| L9 | 上下文向量表示（ELMo 及其后继） | ELMo 论文 |
| L10 | 神经生成与解码策略 | Nucleus Sampling 论文 |
| L11 | 大语言模型：GPT-3、few-shot 与缩放定律 | Chinchilla |
| L12 | 提示、思维链与工具使用 | CoT、Toolformer |
| L13 | 指令微调与人类反馈对齐 | InstructGPT、DPO |
| L14 | 参数高效微调（LoRA/Adapter） | LoRA 论文 |
| L15 | 多模态：视觉-语言模型 | CLIP、Flamingo |
| L16 | 可解释性、偏差与评估 | probing/评估讲义 |
| L17 | 前沿嘉宾讲座（智能体/推理模型等） | 当季 reading list |

> 作业线：A1 词向量分析 → A2 word2vec 实现 → A3 依存句法 → A4 NMT（Transformer+BPE）→ A5 Transformer 微调 → Final Project：SQuAD 问答系统。
