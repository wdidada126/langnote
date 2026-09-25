# NeuralNets-ZeroToHero 提纲

> 骨架级要点，正文笔记待逐讲展开。

## L1 反向传播入门与 micrograd（上）
- 梯度下降的心智模型：把损失看作高维碗形曲面，沿负梯度小步走。
- 计算图视角：任何复杂模型都是标量运算（加/乘/激活）的 DAG。
- 链式法则的两种模式：前向模式 vs 反向模式；标量输出时反向模式 O(节点数) 算完所有梯度。

## L2 micrograd（下）
- Value 类：同时携带 data 与 grad，`__add__/__mul__` 时悄悄记录 parent 与局部导。
- backward()：拓扑排序 + 从输出往回逐节点 `grad += child_grad * local_grad`（`__backprop__`）。
- 与 PyTorch 对照：micrograd 就是 autograd 的最小可运行内核；Troubleshooting 梯度（可视化、梯度检查）。

## L3 makemore Part 1：Bigram 语言模型
- 把"下一个字符预测"形式化为多类分类；名字数据集、one-hot 表示。
- 统计法：数 co-occurrence 频率得到 bigram 概率表。
- 采样生成：按概率分布抽 token，评估用 NLL（交叉熵）。

## L4 makemore Part 2：MLP 语言模型
- 参数化概率分布：logits → softmax → 概率；为什么用 log 概率相加代替概率连乘。
- 交叉熵 = -log p(正确类)，与 NLL 等价。
- torch 版训练循环：前向、损失、backward、更新，mini-batch 的意义。

## L5 makemore Part 3：手动反向传播
- C = sum(B * A) 型矩阵乘的反向：dA = Bᵀ·dC、dB = dC·Aᵀ 的推导模板。
- 前向缓存 → 反向复用：每个算子自己会求导（局部反向）。
- 用自己写的 backward 替代 torch autograd，逐算子核对梯度。

## L6 makemore Part 4：调参与结构
- Embedding/查表层：one-hot × 矩阵 = 查表，可学习的连续表示。
- 宽度/深度、学习率、初始化对收敛的影响；随机搜索。
- Bengio 上下文特征连接：MLP 语言模型的原始形态。

## L7 Let's build GPT
- Self-attention：Q/K/V 与"可微分哈希表"直觉；单头 → 多头。
- Causal mask 与 Transformer block 堆叠：MLP + LayerNorm + 残差。
- 位置编码、权重共享（embedding 与输出头）、生成循环；与 nanoGPT 对齐。

## L8 GPT Tokenizer（BPE）
- 为什么按字节/字符切分低效：词表 vs 序列长度权衡。
- BPE 训练：从单字节出发迭代合并高频对；encode/decode 全流程。
- 特殊 token、上下文窗口拼接与 padding 的工程细节。

## L9 nanoGPT 与训练实践
- 预训练：数据管道、scaling、评估 loss；AdamW、weight decay、grad clipping。
- 监督微调 SFT 与"格式对齐"；采样策略（temperature / top-k / top-p）。
- GPU 训练实操：混合精度、checkpoint、多卡启动（torch.distributed 概览）。

## L10 复现 GPT-2 (124M)（2024 新增）
- 从论文与官方 checkpoint 出发核对每一处实现差异（初始化、LayerNorm 位置等）。
- 用 WebText 子集复现 loss 曲线；理解"逐 bit 对齐"式复现方法论。
- 延伸：llm.c / nanochat 把训练栈下推到 C/CUDA 的思路。

## L11 Deep Dive into LLMs
- LLM 训练的三段式：预训练 → SFT → RLHF/偏好对齐的全景图。
- 幻觉、上下文窗口、工具调用等能力边界的形成原因。
- 与 nanoGPT 知识点对应：ChatGPT 并不神秘，是同一骨架 + 数据 + 对齐。

## L12 How I use LLMs
- 提示工程与任务分解：把 LLM 当"实习生"使用的工作流。
- 检索/工具/代理（agent）模式的实际收益与局限。
- 个人实践：llm.c、nanochat 等项目的持续演进方向。
