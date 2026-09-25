# CMU 15-779：Advanced Topics in Machine Learning Systems (LLM Edition)（机器学习系统专题·LLM 版）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CMU 15-779: Advanced Topics in Machine Learning Systems (LLM Edition) |
| 学校 | Carnegie Mellon University |
| 主讲 | Zhihao Jia（周智尧，CMU Portal 实验室） |
| 教材 | 以课程 slides + 每周指定论文为主（无固定教材） |
| csdiy 路径 | 深度生成模型 → 大语言模型 → CMU 15-779: Advanced Topics in ML Systems (LLM Edition) |
| 最新期次 | 2026 春季更新（csdiy 页面更新至 2026-02-21） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | https://www.cs.cmu.edu/~zhihaoj2/15-779/ |
| 语言/难度/学时 | Python（涉及 CUDA/硬件概念）；难度 4/5；80-120 学时 |

## 为什么学

- 从系统视角回答核心问题：**PyTorch 高层模型如何被分解为底层 kernel，并在 GPU/TPU 与分布式环境中高效执行**——把"框架层经验"打通到"算子/编译/硬件/集群"。
- 强系统导向且紧跟 2024-2026 前沿：FlashAttention、Triton、Ansor/TASO、Mirage 超优化、Alpa 自动并行、PagedAttention/RadixAttention、推测解码、MoE kernel 全覆盖。
- 训练方式好：每周课前论文 review + 期末小组系统项目（proposal/presentation/report），可当作"按周推进的系统训练营"自学。
- 与 11-868 互为犄角：15-779 更偏"算子与编译+前沿论文精读"，11-868 更偏"全流程工程作业"。

## 先修与知识联系

- 先修：无硬性要求；建议具备机器学习入门与深度学习训练经验、熟悉 PyTorch；了解 CUDA/GPU 基础会显著提升效率。
- 联系：
  - 上游：CS229/11-785（ML/DL）、CS149/15-418（并行计算）、CSAPP/6.S081（系统基础）。
  - 平行：机器学习系统分类（15-442、10-414、6.5940、MLC）、大语言模型/CMU11-868。
  - 下游：MLSys 方向科研；vLLM/TensorRT-LLM/DeepSpeed 等基础设施研发岗。

## 讲义章节目录（最新期，按官网 schedule 主题整理，以官网 schedule.html 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | ML 系统导论：以 TensorFlow/PyTorch 看计算图、执行模型与系统抽象 | TF 论文；PyTorch 论文；课程 intro slides |
| L2 | GPU 架构与 CUDA 编程模型 | PMPP 章节；CUDA C++ Programming Guide 关键节 |
| L3 | Transformer 与 Attention 案例：IO-aware 优化 | FlashAttention 1/2/3 论文 |
| L4 | 高级 CUDA：warp specialization、mega kernel、低延迟优化 | FlashInfer/MEGALAND 类论文；KernelCat 资料 |
| L5 | ML 编译器 I：tile 级 DSL（Triton、TileLang） | Triton 论文/文档；TileLang |
| L6 | ML 编译器 II：内核自动调优（Ansor、AutoTVM） | Ansor 论文 |
| L7 | ML 编译器 III：图级优化（TASO/PET）与超优化（Mirage） | TASO、PET、Mirage 论文 |
| L8 | 数据并行与显存优化：DDP、ZeRO/FSDP | DDP/ZeRO 论文 |
| L9 | 模型并行与流水线并行：Megatron-LM、GPipe | Megatron-LM；GPipe/PipeDream |
| L10 | 自动并行化（Alpa 等）与 3D 并行 | Alpa；GSPMD |
| L11 | 长序列与上下文并行 | Ring Attention；序列并行论文 |
| L12 | LLM 推理与服务：连续批处理、PagedAttention、RadixAttention | vLLM；Orca；SGLang |
| L13 | 推理加速：推测解码、KV 压缩、prefill/decode 分离 | Speculative Decoding；Medusa/EAGLE；DistServe |
| L14 | 后训练系统：PEFT（LoRA/QLoRA）与 RLHF 训练栈 | LoRA/QLoRA；veRL/HybridEngine 论文 |
| L15 | MoE 系统：架构、kernel 与并行化 | Switch/GShard；MegaBlocks；DeepSeek-V3 MoE 基础设施 |
| L16 | 前沿专题与项目展示（推理模型系统、多模态系统等当期主题） | 当期 paper list；学生项目报告 |

> 注：课程规则见 logistics.html（Grading、Paper Review、Course Project）；预备材料见 materials.html。
