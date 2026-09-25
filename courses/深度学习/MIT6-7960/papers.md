# MIT 6.7960 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Learning Representations by Back-propagating Errors | 1986 | L3 | 反向传播奠基 |
| Automatic Differentiation in Machine Learning: a Survey | 2015 | L3 | autograd 系统综述 |
| Adam | 2014 | L4 | 自适应优化默认选择 |
| Dropout | 2014 | L5 | 集成式随机正则 |
| AlexNet | 2012 | L6 | CNN 引爆点 |
| ResNet | 2015 | L6 | 残差连接深度可训练 |
| LSTM | 1997 | L7 | 门控长期记忆 |
| Seq2Seq + Attention (Bahdanau) | 2014 | L7/L8 | 注意力起源 |
| Attention Is All You Need | 2017 | L8 | Transformer |
| BERT | 2018 | L9 | 双向预训练 |
| GPT-3 (Few-Shot Learners) | 2020 | L9 | in-context learning |
| VAE | 2013 | L10 | 变分生成框架 |
| GAN | 2014 | L10 | 对抗生成 |
| DDPM | 2020 | L10 | 扩散模型范式 |
| GCN (Kipf & Welling) | 2016 | L11 | 谱卷积 GNN |
| DQN (Playing Atari with Deep RL) | 2013 | L12 | 深度 RL 起点 |
| InstructGPT (RLHF) | 2022 | L12 | 语言模型对齐 |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| Chinchilla: Training Compute-Optimal LMs | 2022 | L9 缩放定律修正 |
| Scaling Vision Transformers (ViT-G) | 2021 | L6/L9 视觉缩放 |
| Latent Diffusion (Stable Diffusion) | 2022 | L10 扩散工程化 |
| Mamba: Selective State Spaces | 2023 | L7/L8 线性时间序列建模 |
| FlashAttention 1/2 | 2022-2023 | L13 IO 感知注意力 |
| GPTQ / AWQ | 2022-2023 | L13 权重量化 |
| DPO | 2023 | L12 免 RM 对齐 |
| DeepSeek-V3 Tech Report | 2024 | L9/L13 MoE 与训练配方 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| autograd（L3） | PyTorch / JAX | 反向模式微分内核 |
| CNN/Transformer（L6/L8） | torchvision / timm / HF transformers | 标准实现与权重库 |
| 扩散（L10） | HuggingFace diffusers | 调度器/UNet/DiT 组件库 |
| GNN（L11） | PyTorch Geometric / DGL | 消息传递算子 |
| RL/RLHF（L12） | stable-baselines3 / TRL / veRL | 策略优化与对齐训练 |
| 高效部署（L13） | vLLM / llama.cpp / TensorRT-LLM | PagedAttention、量化、图优化 |
| 分布式训练（L13） | DeepSpeed / FSDP | 切分与混合精度 |
