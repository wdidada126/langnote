# CMU 11-711：Advanced Natural Language Processing（高级自然语言处理 / ANLP）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CMU 11-711: Advanced Natural Language Processing (ANLP) |
| 学校 | Carnegie Mellon University（LTI） |
| 主讲 | Graham Neubig |
| 教材 | 经典与前沿论文合集 + Goldberg《A Primer on Neural Network Models for Natural Language Processing》章节 |
| csdiy 路径 | 深度生成模型 → 大语言模型 → CMU 11-711: Advanced Natural Language Processing |
| 最新期次 | Fall 2024（csdiy 页面更新至 2025-06-08） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | https://www.phontron.com/class/anlp-fall2024/ |
| 语言/难度/学时 | Python；🌟🌟🌟🌟；约 100 学时 |

## 为什么学

- 研究生级 NLP 主线课：**从词表征、序列建模、注意力/Transformer 一路讲到 LLM 预训练、指令微调、复杂推理、多模态与安全**，是理解现代 NLP 演进逻辑的最佳脉络。
- 紧跟最新研究：LLaMA、GPT-4 等大模型方法直接进入课堂材料，而非只讲经典。
- 实践性强：每次课配套代码演示与在线小测；期末项目要求**复现并改进一篇前沿论文**，训练科研级动手能力。
- 作为 11-667（LLM 专题）的前置/平行课，补齐传统 NLP 到 LLM 的过渡知识；Neubig 的教学与论文选读质量高。

## 先修与知识联系

- 先修：无硬性要求，但需 Python 编程经验、概率论与线性代数基础；有神经网络使用经验更佳（11-785 或 CS224n 水平）。
- 联系：
  - 上游：CS224n / 11-785（深度学习+NLP 入门）、CS229/10-301（机器学习）。
  - 平行：大语言模型/CMU11-667（LLM 方法专题，深度更大）、深度学习/CS224n。
  - 下游：CMU11-868/15-779（系统方向）、生成模型方向（MIT6.S184）。

## 讲义章节目录（Fall 2024，按官网 schedule 整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：NLP 的挑战与神经网络方法变迁 | Goldberg 第 1 章；课程 slides |
| L2 | 词表征与子词模型（Word2Vec/GloVe/BPE） | Mikolov 2013；Pennington GloVe；Sennrich BPE |
| L3 | 序列建模与循环网络语言模型 | Elman 1990；Grave 2013 RNNLM；Goldberg 第 5 章 |
| L4 | 注意力机制与编码器-解码器模型 | Bahdanau 2014；Luong 2015 |
| L5 | Transformer 架构详解 | Vaswani 2017；The Annotated Transformer |
| L6 | 上下文表征与预训练（ELMo/BERT） | Peters ELMo；Devlin BERT；CLM vs MLM 目标 |
| L7 | 自回归大模型与缩放（GPT 系列） | GPT-2/GPT-3；Chinchilla |
| L8 | LLM 训练细节：tokenizer、数据、架构演进 | LLaMA 报告；GQA/RoPE/SwiGLU 论文 |
| L9 | 指令微调与对齐（RLHF/DPO） | FLAN；InstructGPT；DPO |
| L10 | 上下文学习与提示 | Brown ICL；CoT；提示Survey |
| L11 | 复杂推理与规划 | ToT；Self-Consistency；推理模型（o1 前置材料） |
| L12 | 生成解码策略与可控性 | 采样/beam search；DoLa；NEURIPS 约束生成 |
| L13 | NLP 任务专题：机器翻译/摘要/QA/信息抽取 | T5；PEGASUS；RAG；抽取式方法 |
| L14 | 评测与统计：基准、显著性、LLM-as-judge | HELM；评测批判论文 |
| L15 | 多模态与跨语言 | CLIP；mBERT/XLM；LLaVA |
| L16 | 效率、解释性与安全 | LoRA/量化概览；机制可解释性；越狱与偏见 |
| L17 | 前沿讲座与项目展示周 | 学生论文复现报告 |

> 注：课程含每次课在线小测与代码演示；期末项目为复现并改进一篇前沿论文（assignments 页 https://www.phontron.com/class/anlp-fall2024/assignments/ ）。
