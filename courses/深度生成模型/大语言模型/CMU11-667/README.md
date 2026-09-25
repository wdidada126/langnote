# CMU 11-667：Large Language Models: Methods and Applications（大语言模型：方法与应用）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CMU 11-667: Large Language Models: Methods and Applications |
| 学校 | Carnegie Mellon University（LTI） |
| 主讲 | Graham Neubig、Zaid Bazyana 等（Neubig 组，近年持续开课） |
| 教材 | 精选论文与资料（阅读列表见课程网站）；辅以《Practical Deep Learning for Coders》类工程材料 |
| csdiy 路径 | 深度生成模型 → 大语言模型 → CMU 11-667: Large Language Models: Methods and Applications |
| 最新期次 | 2025（csdiy 页面更新至 2025-06-08） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | https://cmu-llms.org/ |
| 语言/难度/学时 | Python；🌟🌟🌟🌟；100 学时以上 |

## 为什么学

- LLM **方法侧**最系统的研究生课之一：从架构、预训练、微调、对齐到解释性、涌现、推理、评测、伦理全覆盖。
- 由 CMU LTI 的 Graham Neubig 主讲，研究前沿与教学体系兼备，阅读材料即领域论文地图。
- 六次作业覆盖预训练数据准备、Transformer 实现、RAG、模型比较与偏见缓解、训练效率提升——是"懂原理也能动手"的完整闭环。
- 与 11-868（系统侧）互补：本课回答"LLM 怎么训出来、为什么有效、如何用好"，11-868 回答"怎么跑得动跑得快"。

## 先修与知识联系

- 先修：机器学习基础（相当于 CMU 10-301/10-601）、NLP 基础（11-411/11-611）；熟练 Python 与 PyTorch。
- 联系：
  - 上游：CS229/10-601（ML）、CS224n/11-711（NLP 与神经网络）。
  - 平行：大语言模型/CMU11-711（ANLP，方法重叠更多）、CMU11-868/15-779（系统侧）。
  - 下游：深度生成模型/MIT6.S184（扩散路线对照）、研究选题（对齐/解释性/推理方向）。

## 讲义章节目录（最新期 2025，按官网 syllabus 主题整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：语言模型简史与 LLM 定义 | Neubig 博客/课程 slides；Chomsky→统计→神经脉络 |
| L2 | 架构：Transformer、Encoder/Decoder、MoE | Vaswani 2017；LLaMA/GPT 架构章节 |
| L3 | 预训练 I：目标函数、数据与 tokenizer | GPT-3；C4/The Pile 数据论文 |
| L4 | 预训练 II：缩放律与计算最优训练 | Kaplan/Chinchilla scaling laws |
| L5 | 微调与适配：SFT、PEFT、领域适应 | LoRA/QLoRA；FLAN 指令微调 |
| L6 | 对齐：RLHF、DPO 与偏好优化 | InstructGPT；DPO；Constitutional AI |
| L7 | 涌现能力与上下文学习 | Wei emergent abilities；Brown GPT-3 ICL；Pet ICL 解析 |
| L8 | 提示工程与推理：CoT、自洽性、搜索 | Chain-of-Thought；Self-Consistency；ToT；o1 类推理模型 |
| L9 | 解码与可控生成 | 采样策略；DoLa/对比解码；约束生成 |
| L10 | 检索增强与非参数化知识 | RAG（Lewis et al.）；RETRO；记忆机制 |
| L11 | 评测：基准、人工评估与统计有效性 | HELM；LMSYS Arena；评测批判论文 |
| L12 | 效率：训练与推理的高效方法（方法视角） | FlashAttention/量化概览；蒸馏；与 11-868 分工 |
| L13 | 解释性：探针、机制可解释性 | Elhage math of transformers；induction heads；SAE |
| L14 | 偏见、安全与攻击 | 毒性/偏见度量；越狱与提示注入；red-teaming |
| L15 | 多模态与非文本应用 | CLIP；LLaVA；科学/代码应用（AlphaCode 类） |
| L16 | Agent、工具使用与社会影响展望 | ReAct；WebGPT；部署治理与法律议题 |

> 注：作业 https://cmu-llms.org/assignments/ 共六次：预训练数据准备、Transformer 实现、RAG、模型比较与偏见缓解、训练效率提升等。
