# CMU 10-414 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Automatic Differentiation: From Machine Learning to Optimization? / AD 综述 (Griewank & Walther) | 2008 | L2-L3 | AD 前向/反向模式的理论经典 |
| Efficiency of Backpropagation (Rumelhart/Hinton/Williams) | 1986 | L3 | 反向传播 = 反向模式 AD |
| Adam: A Method for Stochastic Optimization | 2015 | L5 | 优化器标准实现 |
| Delving Deep into Rectifiers / He 初始化 | 2015 | L8 | 深层网络初始化 |
| Long Short-Term Memory (Hochreiter & Schmidhuber) | 1997 | L9 | LSTM 门控单元 |
| Attention Is All You Need | 2017 | L9 | Transformer |
| cuDNN: Efficient Primitives for Deep Learning | 2014 | L10 | GPU 深度学习基元库 |
| Mixed Precision Training (Micikevicius et al.) | 2018 | L11 | FP16 与 loss scaling |
| Roofline: An Insightful Visual Performance Model (Williams et al.) | 2009 | L12 | 性能建模 |
| Large Scale Distributed Deep Networks (Dean et al., NIPS) | 2012 | L13 | 分布式训练范式 |
| TVM: An Automated End-to-End Optimizing Compiler (OSDI) | 2018 | L13 | DL 编译（延伸） |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| FlashAttention: Fast and Memory-Efficient Exact Attention | 2022 | L12 访存感知 kernel |
| PyTorch 2.0 / torch.compile 技术报告 | 2022-2023 | L6/L13 编译栈 |
| FP8 Formats for Deep Learning (OCP Microformats) | 2022 | L11 低精度格式 |
| Megatron-LM / ZeRO（分布式训练现代化，作延伸） | 2021 | L13 |
| BitNet / 二值化推理（LLM 量化新方向） | 2023-2024 | L11 量化演进 |
| Mamba: Linear-Time Sequence Modeling | 2023 | L9 序列模型新架构 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 前向/反向 AD（L2-L4） | micrograd / PyTorch autograd / JAX | grad tape 与 vmap/jit |
| 框架 backend 分层（L6） | needle / PyTorch aten / TVM | 算子与调度解耦 |
| CNN/RNN 实现（L8-L9） | PyTorch / TensorFlow / Keras | nn 层与损失函数 |
| cuDNN 集成（L10） | PyTorch CUDA backend / cuDNN | 卷积/GEMM 加速 |
| 混合精度（L11） | PyTorch AMP / DeepSpeed | autocast + GradScaler |
| 性能建模（L12） | Nsight Compute / Roofline 工具 / Triton | 内核瓶颈定位 |
| 分布式（L13） | PyTorch DDP / DeepSpeed / Horovod | 梯度 all-reduce |
