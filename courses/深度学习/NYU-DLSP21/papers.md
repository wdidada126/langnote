# NYU DLSP21 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Backpropagation Through Time (Werbos 溯源) | 1990 | L3 | 反向传播与循环展开 |
| Gradient-Based Learning (LeNet) | 1998 | L4 | CNN 训练范式定型 |
| ImageNet Classification (AlexNet) | 2012 | L4 | 现代深度学习点火 |
| Efficient Estimation of Word Representations (word2vec) | 2013 | L5 | 分布式语义可学习 |
| LSTM | 1997 | L6 | 门控解决长期依赖 |
| Learning Phrase Representations (Cho GRU/Seq2Seq) | 2014 | L6 | GRU 编码器-解码器 |
| Neural Machine Translation by Jointly Learning to Align (Bahdanau) | 2014 | L7 | 注意力机制诞生 |
| Attention Is All You Need | 2017 | L7 | Transformer |
| BERT | 2018 | L8 | 双向预训练微调 |
| Improving Language Models by Generative Pre-training (GPT) | 2018 | L8 | 自回归生成预训练 |
| Playing Atari with Deep RL (DQN) | 2013 | L9 | 深度值函数 RL |
| Language Models are Few-Shot Learners (GPT-3) | 2020 | L10 | 大模型 in-context 时代 |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| A New Path to Unsupervised Learning: JEPA（LeCun 立场文） | 2022-2023 | L5 非生成式自监督路线 |
| I-JEPA / V-JEPA | 2023-2024 | L5 预测嵌入空间表征 |
| RoFormer (RoPE) | 2021 | L7 旋转位置编码成为标配 |
| GPTNeoX / Pythia（训练解剖） | 2023 | L10 开源复现 GPT 细节 |
| NanoGPT/speedrun（How to Train Your Own GPT-2 类实践报告） | 2023-2024 | L10 期末项目现代对照 |
| Mamba | 2023 | L6-L7 循环思想以状态空间回归 |
| LLaMA 系列 | 2023-2024 | L8 开源 decoder-only 主线 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| autograd（L3） | PyTorch / TinyAutoGrad（karpathy） | tape 式反向模式微分 |
| CNN（L4） | torchvision / timm | 经典 backbone 库 |
| 嵌入检索（L5） | FAISS | 向量近邻与倒排索引工业实现 |
| 语言模型（L6-L8） | HuggingFace transformers | BERT/GPT 标准实现 |
| Build GPT-2 Mini（L10） | karpathy/nanoGPT、llama2.c | 期末项目的当代最简参照 |
| RL（L9） | CleanRL / stable-baselines3 | 单文件 DQN/PPO 实现 |
| 课程作业框架 | NYU DL GitHub（atcold/NYU-DLSP21） | slides+assignment 官方仓库 |
