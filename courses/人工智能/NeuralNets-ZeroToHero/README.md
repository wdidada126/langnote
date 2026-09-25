# Neural Networks: Zero to Hero（Karpathy 神经网络从零实现）学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Neural Networks: Zero to Hero（神经网络：从零到英雄） |
| 学校 | 无（Andrej Karpathy 独立开设，Eureka Labs / YouTube） |
| 主讲 | Andrej Karpathy（前 Tesla AI 总监、OpenAI 创始成员，斯坦福博士，CS231n 创建者） |
| 教材 | 无；以课程配套代码（micrograd / makemore / nanoGPT 系列仓库）为教材 |
| csdiy 路径 | `人工智能/Neural Networks：Zero to Hero`（页面更新：2025-06-24） |
| 最新期次 | 2024-2025 持续活跃：2024-12 新增 "Let's reproduce GPT-2 (124M)"、两门 LLM 科普篇；2025 年持续更新 |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 19 小时；先修：基本 Python 编程 + 对深度学习概念有所了解；语言 Python |

## 为什么学

- Karpathy 招牌式的"逐行手敲"教学：从反向传播第一性原理出发，一步步搭出 micrograd → makemore → GPT，全程不藏步骤。
- 是理解 PyTorch autograd、Transformer 与 LLM 训练细节的最短路径，学完对 `loss.backward()` 背后发生的事再无黑盒。
- 配套开源项目（micrograd、nanoGPT、llm.c 等）本身就是工业界与教育界引用最多的参考实现。
- 2024-2025 新内容（复现 GPT-2 124M、Deep Dive into LLMs）与 LLM 时代前沿保持同步，2025-06 csdiy 仍在更新收录。

## 先修与知识联系

- 先修：Python 基础、少量微积分/概率直觉；不需要预先会深度学习。
- 前导：CS50P / MIT-Missing-Semester（工具与编程）、Coursera ML / CS230（概念地图）。
- 后续/横向：CS231n、CS224n（Karpathy 在斯坦福的正式课程）、CMU10-414 与 15-442（把 micrograd 升级为真正的反向模式 AD 与系统实现）、CS285（RL 视角的 policy gradient 与本课程语言模型技巧同源）。
- 知识输出：micrograd → PyTorch autograd 心智模型；makemore/nanoGPT → 一切 LLM 训练/推理框架（vLLM、llama.cpp）的最小骨架。

## 讲义章节目录（YouTube 播放列表"Zero to Hero"，按学习顺序，2024-2025 最新态）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 反向传播入门与 micrograd（上）：标量自动求导 | Karpathy "The spelled-out intro to neural networks and backpropagation: building micrograd"；chain rule 讲义 |
| L2 | micrograd（下）：Value 计算图与梯度回传 | 同上视频后半；karpathy/micrograd 源码 |
| L3 | 语言模型第一步：makemore Part 1（Bigram 统计模型） | makemore Part 1；字符级 n-gram 直觉 |
| L4 | makemore Part 2：MLP 语言模型与交叉熵 | makemore Part 2；Bengio 2003 神经语言模型 |
| L5 | makemore Part 3：手推反向传播（Manual Backprop Wizard） | makemore Part 3；Baydin et al. 2018 自动微分综述（选读） |
| L6 | makemore Part 4：超参搜索、Bengio 特征与查表 | makemore Part 4 |
| L7 | Let's build GPT：从零手搓 Transformer（注意力/多头/Causal mask） | 视频 "Let's build GPT: from scratch, in code, spelled out"；Vaswani 2017（必读） |
| L8 | Let's build the GPT Tokenizer：BPE 分词器从零实现 | 视频；Sennrich et al. 2016 BPE 论文（选读） |
| L9 | nanoGPT 总览与训练实践：预训练 + SFT + 采样策略 | 视频 "The spelled-out intro to LLMs and generation: building nanoGPT"；karpathy/nanoGPT README |
| L10 | Let's reproduce GPT-2 (124M)（2024-12 新增） | 对应视频；Radford et al. 2019 "Language Models are Unsupervised Multitask Learners" |
| L11 | 延伸篇：Deep Dive into LLMs like ChatGPT（2025） | 视频；Karpathy 博客与训练 pipeline 讲稿 |
| L12 | 延伸篇：How I use LLMs（2025） | 视频；nanochat/llm.c 仓库（选做） |

> 注：视频上线时间与播放顺序有交叉（micrograd/nanoGPT 视频在前，makemore 系列在后），本表按 csdiy 建议的"由浅入深"学习顺序编排，骨架阶段允许微调。

## 课程资源（摘自 csdiy）

- 课程视频：YouTube 播放列表（Karpathy 频道）
- 作业：课程内代码实践与项目练习（无标准作业系统）
- 更多信息请访问 YouTube 观看完整课程视频
