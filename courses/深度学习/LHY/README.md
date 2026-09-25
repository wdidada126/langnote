# 国立台湾大学：李宏毅机器学习（Machine Learning 2025 Spring）学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 國立台灣大學 機器學習（Machine Learning, NTU） |
| 学校 | 国立台湾大学 |
| 主讲 | 李宏毅（Hung-yi Lee） |
| 教材 | 无指定教材；讲义与作业均公开（自建 Jupyter Lab 作业体系） |
| csdiy 路径 | `深度学习/LHY`（页面更新：2025-06-08） |
| 最新期次 | Spring 2025（大改版：以 RAG / AI Agent / LLM 为主线，与 2023 及之前差异极大） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 80 小时；先修：熟练掌握 Python |

## 为什么学

- 中文世界影响力最大的机器学习课，李宏毅老师风趣幽默（宝可梦 PPT），自学资料完全公开。
- 2025 改版后直接对准当下最热主线：LLM 原理、RAG、AI Agent，作业全部围绕 LLM 实战。
- 作业提供助教示例代码，改代码即入门，同时也是学习优质工程代码/水课程大作业的好来源。
- 旧版（2023 及之前）15 个 Lab 覆盖 CNN/自注意力/GAN/BERT/异常检测/可解释 AI/攻击/域适应/压缩/终身学习/元学习等，可作为进阶专题图书馆。

## 先修与知识联系

- 先修：Python、基础微积分与线代；有 CS230/CS229 概念更佳。
- 后续/衔接：LLM 主线与 CS224n、CMU 11-868 互补；传统深度学习部分可衔接 CS231n、CS285。
- 横向：2025 版 RAG/Agent 作业与开源 LangChain/LlamaIndex/DSPy 生态直接对应。

## 讲义章节目录（Spring 2025 主线，以官网课表为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L0 | 课程说明与自学章节（回归/分类/梯度下降/深层网络训练） | 2021-2023 版对应讲义（自学） |
| L1 | 生成式 AI 与 ChatGPT 原理（预训练/指令微调/RLHF） | ChatGPT 讲义 |
| L2 | 提示工程与思维链（Prompt / CoT / 自洽性） | Prompting 讲义 |
| L3 | Transformer 架构复习（Attention/自注意力/位置编码） | 自注意力讲义（旧版保留） |
| L4 | 解码策略与生成（greedy/beam/采样、温度） | Decoding 讲义 |
| L5 | 工具使用与函数调用（Tool Use / Function Calling） | Toolformer 等论文 |
| L6 | RAG 检索增强生成（检索器/重排/分块/评估） | RAG (Lewis 2020) 讲义 |
| L7 | AI Agent（规划/反思/多智能体，ReAct 范式） | ReAct 论文 |
| L8 | 模型微调与高效适配（LoRA/QLoRA/蒸馏） | LoRA 讲义 |
| L9 | 长上下文与效率（KV cache、量化、稀疏注意力） | 效率综述 |
| L10 | 多模态模型（视觉-语言，CLIP/LLaVA） | CLIP/LLaVA 论文 |
| L11 | LLM 评估（benchmark/LLM-as-a-judge） | 评估讲义 |
| L12 | 安全与对齐（越狱、防御、RLHF/DPO） | 安全讲义 |
| L13 | 研究前沿专题（推理模型、o1/R1 式 RL 训练） | DeepSeek-R1 论文 |

> 作业线（2025）：约 6 个 Jupyter 作业，覆盖 训练分类器 → BERT Masked LM → LLM 微调 → RAG 问答 → Agent → 安全攻击，随课表推进。
