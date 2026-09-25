# UCSD CSE234: Data Systems for Machine Learning 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CSE234: Data Systems for Machine Learning（高效 LLM 系统导论） |
| 学校 | UCSD（加州大学圣地亚哥分校） |
| 主讲 | Hao Wang（Hao AI Lab）等 |
| 教材 | 无单一教材；课程网站 resources 页论文清单 + 配套文档 |
| csdiy 路径 | `机器学习系统/UCSD CSE234: Data Systems for Machine Learning`（页面更新：2026-02-01） |
| 最新期次 | Winter 2025（hao-ai-lab.github.io/cse234-w25，全部开源） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟，约 120 小时；先修：线性代数、深度学习、操作系统、计算机网络、分布式系统；语言 Python/Triton |

## 为什么学

- 以 LLM 系统为核心应用场景的高效系统设计入门课，强调真实系统中的取舍与工程约束，而非停留在算法或 API 层面。
- 三大部分递进：①现代 DL 与计算表示（计算图/Autodiff/张量格式/硬件加速器）→ ②系统与性能优化（GPU Kernel/算子编译/Triton/图优化/内存/量化）→ ③LLM 系统（并行策略/Transformer/FlashAttention/连续批处理/PagedAttention/分离式 prefill/decode/Scaling law）。
- 作业直面真实性能瓶颈（内存带宽、通信开销、kernel fusion），用 Triton 与系统级优化解决，对理解"为什么某些 LLM 系统长这样"极有帮助。
- csdiy 给出最佳食用路线：基础部分配 micrograd，系统部分配 nanoGPT/nano-vllm 动手实现。

## 先修与知识联系

- 先修：线性代数、深度学习、OS、网络、分布式系统；自学建议先补 CUDA/并行编程，否则 Part 2/3 曲线陡峭。
- 前导：CMU10-414（框架与 autograd）、MLC（编译视角）、EML（模型效率视角）。
- 平级：CMU15-442（同为 LLM 时代系统课，CSE234 更重 Triton 动手与分布式视角）。
- 后续：CMU11-868 等大模型系统课；工业 LLM Infra（vLLM/SGLang/TensorRT-LLM）。
- 知识输出：kernel 作业 → Triton/CUTLASS 开发；推理作业 → nano-vllm 级调度器；并行 → Megatron/DeepSpeed。

## 讲义章节目录（对应 cse234-w25 三大部分 + Guest）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | Part1 导论：现代深度学习与计算图/框架基础 | 课程 slides；micrograd 对照 |
| L2 | Autodiff 与 ML 系统架构概览 | Baydin 2018；框架论文 |
| L3 | Tensor 格式、MatMul 深入与硬件加速器 | 加速器综述；Roofline |
| L4 | Part2 GPU 与 CUDA：基本性能模型 | CUDA 文档；GPU Glossary |
| L5 | GPU MatMul 与算子编译 | Triton 矩阵乘教程；CUTLASS |
| L6 | Triton 编程 | Tillet et al. 2019 |
| L7 | 图优化与编译 | TVM/Inductor 资料 |
| L8 | 内存：训练/推理内存问题与技巧（重计算/offload/碎片） | ZeRO/Checkpointing 论文 |
| L9 | 量化：方法与系统落地 | GPTQ/AWQ/SmoothQuant |
| L10 | Part3 并行 I：模型并行与 collective communication | Megatron-LM；NCCL 文档 |
| L11 | 并行 II：intra/inter-op 与自动并行化 | Alpa；自动并行论文 |
| L12 | LLM 基础：Transformer、Attention、MoE | Vaswani 2017；Mixtral |
| L13 | LLM 训练优化：FlashAttention 等 | Dao et al. 2022/2023 |
| L14 | LLM 推理：连续批处理、PagedAttention、分离式 prefill/decode | vLLM 2023；DistServe/Splitwise 2024 |
| L15 | Scaling law | Kaplan 2020；Chinchilla 2022 |
| L16 | Guest：ML compiler | 延伸嘉宾讲义 |
| L17 | Guest：LLM pretraining / open science | 延伸嘉宾讲义 |
| L18 | Guest：fast inference | 延伸嘉宾讲义 |
| L19 | Guest：tool use & agents | 延伸嘉宾讲义 |

> 注：以 w25 官网 syllabus 为准，guest 讲次名称可能调整。

## 课程资源（摘自 csdiy）

- 课程网站/视频/教材/作业：https://hao-ai-lab.github.io/cse234-w25/（resources 与 assignments 子页）
- 资源汇总：内容全开源；在线测评与参考答案未开源
- 延伸：GPUMode（GPU Kernel/System 深度讲解，覆盖 DistServe/FlashAttention/Triton）
