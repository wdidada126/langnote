# CMU 11-868：Large Language Model System（大语言模型系统）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CMU 11-868/768: Large Language Model Systems（原 11-868 系列前身含 10-414 深潜之后） |
| 学校 | Carnegie Mellon University |
| 主讲 | Tianqi Chen、Zhenyu Zhang 等（LLMSystem 教学团队，工业嘉宾客座讲座） |
| 教材 | 精选论文 + *Programming Massively Parallel Processors, 4th Ed* 部分章节 |
| csdiy 路径 | 深度生成模型 → 大语言模型 → CMU 11-868: Large Language Model System |
| 最新期次 | 2025 Spring（csdiy 页面更新至 2025-06-08） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | https://llmsystem.github.io/llmsystem2025spring/ |
| 语言/难度/学时 | Python（含 CUDA）；🌟🌟🌟🌟；约 120 学时 |

## 为什么学

- 聚焦**"从算法到工程"**的 LLM 系统构建全过程：GPU 编程、自动微分、分布式训练、压缩量化、推理服务一条线打通。
- 项目驱动：五次编程作业 + 期末大项目，把 miniTorch 框架从纯 Python 一路拓展到真实 CUDA 内核，是少数能"手写出来"的 LLM 系统课。
- 紧密结合最新论文与开源实现（FlashAttention、ZeRO、vLLM、GPTQ、MoE、RLHF 系统），工业嘉宾讲座呈现真实工程挑战。
- 与 15-442/10-414/15-779 形成互补：本课以 LLM 全流程为主线，适合想进入 LLM 训练/推理基础设施方向的人。

## 先修与知识联系

- 先修：强烈建议已修 Deep Learning（11-785）或 Advanced NLP（11-611/11-711）；熟悉 Python/PyTorch；复习并行计算与自动微分；需 NVIDIA GPU + CUDA Toolkit 环境。
- 联系：
  - 上游：CS229/11-785（深度学习）、CS149/15-418（并行计算）、6.S081/CSAPP（系统基础）。
  - 平行：机器学习系统/15-442、10-414（DL Systems）、深度生成模型/CMU15-779（ML Systems LLM 专题，主题高度重叠、互为深化）。
  - 下游：大语言模型/CMU11-667（方法侧）、CMU11-711（NLP 侧）。

## 讲义章节目录（2025 Spring，按官网 syllabus/schedule 整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | LLM 系统总览：算法与系统双视角 | 课程 Syllabus；LLM 训练流水线综述 |
| L2 | LLM 基础：Transformer 与预训练目标 | Vaswani et al. Attention is All You Need；GPT-2/GPT-3 |
| L3 | GPU 架构与并行编程模型 | PMPP 4e 第 1-3 章 |
| L4 | CUDA kernel 编程与算子实现 | PMPP 4e 第 4-6 章；miniTorch 算子作业 |
| L5 | 自动微分与深度学习框架设计 | Autograd 论文；PyTorch 实现解析 |
| L6 | 模型编译与执行优化（JAX/XLA、Triton、TVM） | JAX/XLA 论文；Triton 文档 |
| L7 | 训练数据处理与 tokenizer 系统 | LLaMA 数据论文；BPE/SentencePiece |
| L8 | 高效训练：长序列与注意力优化 | FlashAttention 1/2；Ring Attention |
| L9 | 数据并行、梯度同步与 ZeRO/FSDP | DDP 论文；ZeRO 三部曲 |
| L10 | 张量并行与流水线并行 | Megatron-LM；GPipe/PipeDream |
| L11 | 自动并行化与 3D 并行 | Alpa/GSPMD；大规模训练案例 |
| L12 | MoE 稀疏化训练与推理 | Switch Transformer；Mixtral/Megablocks |
| L13 | 模型压缩：量化（GPTQ/AWQ/SmoothQuant） | GPTQ、LLM.int8() 论文 |
| L14 | 参数高效微调与蒸馏 | LoRA/QLoRA；蒸馏方法 |
| L15 | 对齐系统：RLHF/PPO/DPO 的工程实现 | InstructGPT；TRL/veRL 框架剖析 |
| L16 | LLM 推理服务：连续批处理与 PagedAttention | vLLM 论文；Orca |
| L17 | 推理加速：投机解码与缓存优化 | Medusa/EAGLE；CacheGen |
| L18 | 检索增强生成（RAG）系统与向量检索 | RAG 论文；向量数据库综述 |
| L19 | 多模态 LLM 系统 | LLaVA/Qwen-VL 类论文 |
| L20 | Agent 与工具调用运行时 | ReAct；开源 agent 框架剖析 |
| L21 | 在线维护、监控与部署（MLSys 工程实践） | 工业嘉宾讲座材料 |
| L22 | 期末项目展示与前沿回顾 | 学生项目报告 |

> 注：作业体系为 Assignment 1-5 + 期末大项目；A1 自动微分+CUDA 手写算子，A2 GPT-2 构建，A3 手写 Softmax/LayerNorm 提速，A4 分布式训练，A5 见官网。
