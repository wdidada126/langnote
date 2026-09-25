# CMU 11-785 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Learning Representations by Back-propagating Errors | 1986 | L3 | 反向传播开山 |
| LeNet | 1998 | L4 | 卷积网络文档识别 |
| AlexNet | 2012 | L4 | 深度学习引爆 ImageNet |
| word2vec (Efficient Estimation of Word Representations) | 2013 | L5 | skip-gram 词嵌入 |
| Batch Normalization | 2015 | L6 | 中间层分布稳定 |
| ResNet | 2015 | L6 | 残差连接使百层可训 |
| LSTM / GRU (原始与 The Learning Long Short-Term Memory) | 1997/2014 | L7 | 门控循环与长期依赖 |
| Attention Is All You Need | 2017 | L8 | Transformer |
| An Image is Worth 16x16 Words (ViT) | 2020 | L9 | Transformer 迁移视觉 |
| wav2vec 2.0 | 2020 | L9 | 自监督语音表征 |
| Auto-Encoding Variational Bayes (VAE) | 2013 | L10 | 重参数化与 ELBO |
| GAN | 2014 | L11 | 对抗生成 |
| Denoising Diffusion Probabilistic Models (DDPM) | 2020 | L11 | 扩散模型范式 |
| Semi-Supervised Classification with GCN | 2016 | L14 | 谱卷积简化版 GNN |
| SimCLR | 2020 | L14 | 对比学习框架 |
| Adam | 2014 | L3/L12 | 自适应优化默认选择 |
| Dropout | 2014 | L13 | 随机失活正则 |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| A ConvNet for the 2020s (ConvNeXt) | 2022 | L4/L6 CNN 现代化 |
| Scaling Language Models (Chinchilla) | 2022 | L16 缩放定律 |
| Mamba (Linear-Time Sequence Modeling) | 2023 | L7/L8 替代循环的新架构 |
| Stable Diffusion / latent diffusion | 2022 | L11 扩散工程化 |
| Flamingo / LLaVA | 2022-2023 | L9 多模态对齐 |
| Theorem 1? — Understanding Double Descent 综述 | 2021 | L13 泛化新图景 |
| GraphGPS (Benchmarking GNNs) | 2022 | L14 GNN 基准 |
| Direct Preference Optimization | 2023 | L15 RL 与对齐交汇 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 反向传播（L3） | PyTorch autograd / micrograd | 计算图与自动微分内核 |
| CNN/ResNet（L4/L6） | torchvision / timm | backbone 与预训练权重 |
| Transformer（L8） | HuggingFace transformers | 事实标准实现 |
| ASR（L9） | ESPnet / WeNet / whisper | CTC/attention 语音栈 |
| VAE/GAN/扩散（L10-11） | diffusers / StyleGAN3 官方实现 | 生成管线与采样器 |
| GNN（L14） | PyTorch Geometric / DGL | 消息传递算子库 |
| 优化/泛化（L12-13） | DeepSpeed / bitsandbytes | 大规模训练与隐式正则工程 |
| RL（L15） | stable-baselines3 / Tianshou | 策略梯度与 AC 实现 |
