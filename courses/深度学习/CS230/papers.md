# CS230 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| LeNet: Gradient-Based Learning Applied to Document Recognition | 1998 | C4W1 | 卷积+池化+全能的手写识别奠基结构 |
| AlexNet (ImageNet Classification with Deep CNNs) | 2012 | C4W2 | ReLU/Dropout/GPU 训练引爆深度学习 |
| Network in Network（1x1 卷积） | 2013 | C4W1 | 点卷积与 MLP 卷积核思想 |
| VGG (Very Deep Convolutional Networks) | 2014 | C4W2 | 重复 3x3 卷积堆叠到 16-19 层 |
| GoogLeNet / Inception v1 | 2014 | C4W2 | 多尺度并行分支 + 1x1 瓶颈 |
| Batch Normalization | 2015 | C2W3 | 中间层分布稳定，加速收敛 |
| ResNet (Deep Residual Learning) | 2015 | C4W2 | 恒等快捷连接解决退化，百层可训 |
| Adam: A Method for Stochastic Optimization | 2014 | C2W2 | 动量+自适应步长默认优化器 |
| Dropout | 2014 | C2W1 | 随机失活作为集成正则 |
| FaceNet (Joint Embedding CNN) | 2015 | C4W3 | triplet loss 人脸识别 |
| Neural Style Transfer (Gatys et al.) | 2015 | C4W3 | 预训练 VGG 特征上做风格优化 |
| Sequence to Sequence Learning | 2014 | C5W2 | encoder-decoder 机器翻译范式 |
| Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau Attention) | 2014 | C5W3 | 注意力机制起源 |
| LSTM | 1997 | C5W1 | 门控解决长期依赖 |
| GloVe: Global Vectors for Word Representation | 2014 | C5W2 | 全局共现矩阵分解词向量 |
| Attention Is All You Need (Transformer) | 2017 | C5W3 | 自注意力+位置编码，终结循环 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| ConvNeXt: A ConvNet for the 2020s | 2022 | CNN 现代化的 Transformer 化改造 |
| Scaling Language Models: Methods, Analysis (Gopher) | 2021 | C1W1 规模驱动的量化版 |
| Chinchilla (Training Compute-Optimal LLMs) | 2022 | 数据量/参数量最优配比 |
| Segment Anything (SAM) | 2023 | C4W3 分割/检测的基座模型化 |
| LLaMA 系列 (1/2/3) | 2023-2024 | C5W3 Transformer 解码器开源复现 |
| LoRA: Low-Rank Adaptation | 2021 | C2W3/C5 微调参数高效化 |
| FlashAttention / v2 | 2022-2023 | C5W3 注意力工程优化 |
| Diffusion Models Beat GANs on ImageSynthesis (ADM) | 2021 | C4W3 生成方向演进 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 自动微分/BP（C1W4） | PyTorch / JAX | autograd 计算图与反向模式微分 |
| CNN 经典架构（C4W2） | torchvision / timm | 内置 ResNet/ConvNeXt 等 backbone |
| Adam/BN（C2W2-3） | PyTorch `optim` / `nn.BatchNorm` | 训练管线默认组件 |
| Transformer（C5W3） | HuggingFace transformers | Encoder/Decoder 实现的事实标准 |
| GPT 解码器 | llama.cpp / vLLM | Transformer 推理栈（KV cache、量化） |
| 风格迁移（C4W3） | fast-style-transfer / diffusers 前身 | 优化式与前馈式风格迁移 |
| 序列生成（C5W2） | HF transformers generate | beam search/top-k/top-p 采样实现 |
