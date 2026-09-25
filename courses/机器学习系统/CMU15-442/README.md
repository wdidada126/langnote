# CMU 15-442/642: Machine Learning Systems 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 15-442/642: Machine Learning Systems |
| 学校 | CMU（卡内基梅隆大学） |
| 主讲 | Tianqi Chen（陈天奇）、Zhihao Jia |
| 教材 | 无单一教材；官方 assignment 仓库 + MLSys 论文清单 |
| csdiy 路径 | `机器学习系统/CMU 15-442/642: Machine Learning Systems`（页面更新：2026-07-21） |
| 最新期次 | 2026 Spring（csdiy 收录版；官网 mlsyscourse.org） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 100+ 小时；先修：系统入门(如 15-213)、深度学习入门、基本数学；语言 Python/C++/CUDA(PTX)/TIRx |

## 为什么学

- LLM 时代最核心的工程问题就是"高效训练与部署"：这门课由陈天奇与 Zhihao Jia 讲授，是探究 vLLM、SGLang 等顶尖推理框架底层原理、亲手编写榨干现代 GPU 算子的算子的最佳入门。
- "模型、数据、系统、硬件"全栈协同视角：从自动微分等框架基石 → GPU（Blackwell B200）底层加速 → 分布式训练（ZeRO、张量/流水线并行）→ LLM 推理（连续批处理、PagedAttention、投机解码）→ ML 编译抽象与 Mega-Kernel。
- 三个硬核且与工业前沿接轨的作业：①扩展图自动微分框架；②用 MPI+NumPy 实现 ZeRO Stage 3 参数分片与张量并行通信；③用 TIRx DSL 针对 B200 从零手写 FP16 GEMM，处理 128B Swizzle、TMA 异步搬运、Warp Specialization、2-CTA 集群调度，把算力从 0.02 TFLOP/s 提到媲美 cuBLAS 的 1300+ TFLOP/s。

## 先修与知识联系

- 先修：15-213/CSAPP（系统）、深度学习入门（CS230/10-414）、线代/概率基础。
- 前导/平级：CMU10-414（DL Systems 本科-研究生版，15-442 可视为其 MLSys 进阶与 LLM 化重写）、EML/TinyML（算法侧效率技术互补）、MLC（编译专题）。
- 后续：CMU11-868/15-779 等大模型系统课；工业界 LLM Infra（vLLM/SGLang/TensorRT-LLM 源码阅读）。
- 知识输出：自动微分作业 → autograd 引擎；分布式作业 → DeepSpeed/FSDP；GEMM 作业 → cuBLAS/CUTLASS/Triton 内核开发。

## 讲义章节目录（对应 2026 Spring 课程模块，官网 mlsyscourse.org）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：MLSys 与"模型-数据-系统-硬件"全栈 | 课程 slides；AlexNet 2012 |
| L2 | 自动微分：前向/反向模式、扩展计算图 | Baydin et al. 2018；Assignment 1 |
| L3 | 深度学习框架架构：算子、调度器、运行时 | TensorFlow OSDI 2017；PyTorch 设计文档 |
| L4 | 现代 GPU 硬件：SM、存储层级、Tensor Core | NVIDIA Blackwell 架构白皮书；Roofline Williams 2009 |
| L5 | GPU 编程：CUDA/PTX/Triton/TIRx 与内存访问模式 | Triton PLDI 2019；TIRx 文档；Assignment 3 |
| L6 | 高性能 GEMM：Swizzle、TMA 异步拷贝、Warp Specialization、集群调度 | CUTLASS 文档；Assignment 3 |
| L7 | 机器学习编译：图级/算子级抽象、自动调度 | TVM OSDI 2018；Ansor ASPLOS 2020；MLC 课程选读 |
| L8 | 分布式训练 I：数据并行、All-Reduce、通信隐藏 | Ring All-Reduce (Shaojie 2017); Horovod 1710 |
| L9 | 分布式训练 II：ZeRO 冗余优化器、参数分片 | Rajbhandari et al. ZeRO 2020；Assignment 2 |
| L10 | 分布式训练 III：张量并行、流水线并行、自动并行 | Megatron-LM 2019；GPipe 2019；Alpa 2022 |
| L11 | LLM 推理 I：服务系统、连续批处理、PagedAttention | Kwon et al. vLLM SOSP 2023；SGLang 2024 |
| L12 | LLM 推理 II：KV cache 管理、投机解码、prefill/decode 分离 | Leviathan et al. Speculative Decoding 2023；DistServe 2024 |
| L13 | 量化与低精度：FP8/INT8/INT4 与训练推理落地 | Micikevicius 2018；GPTQ/AWQ 2022-23；FP8 白皮书 |
| L14 | 前沿：Mega-Kernel、异构系统、MLSys 开放问题 | MegaKernel 相关论文（2024-25）；MLSys 会议精选 |

> 注：三个作业（Assignment 1/2/3 对应 L2/L9-10/L5-6）为课程核心，官方仓库 mlsyscourse/assignment*；具体周次以 2026 Spring 官网为准。

## 课程资源（摘自 csdiy）

- 课程网站：https://mlsyscourse.org/
- 课程视频：无（以 slides + 作业驱动）
- 课程作业：assignment1（自动微分）、assignment-distributed-training（ZeRO-3+TP）、assignment-tirx-gemm（B200 手写 GEMM）
- 资源汇总：RisingUppercut/CMU_15442_2026Spring（GitHub）
