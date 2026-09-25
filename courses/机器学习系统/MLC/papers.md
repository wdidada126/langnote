# MLC（机器学习编译）论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| TVM: An Automated End-to-End Optimizing Compiler for Deep Learning (Chen et al., OSDI) | 2018 | L1-L5 | ML 编译奠基：算子调度 + 自动调优 |
| Learning to Optimize Tensor Programs (AutoTVM, NeurIPS) | 2018 | L6 | 代价模型引导的调度搜索 |
| Ansor: Generating High-Performance Tensor Programs for Deep Learning (OSDI) | 2020 | L6 | 无模板自动调度 |
| Halide: Decoupling Scheduling from Semantics (Mullapudi 等 CGO/OSDI) | 2013 | L5 | schedule 与计算分离的思想源头 |
| XLA: Optimizing Compiler of Computation Graphs of TensorFlow（技术报告） | 2017 | L1 | 图编译另一路线 |
| Relay: A Functional IR for Deep Learning Optimization（TVM Relay 论文/文档） | 2019 | L3/L7 | 函数式中端 IR |
| TVM's MicroTVM: towards compiling DL models for MCU (技术报告) | 2020 | L4 | 嵌入式代码生成 |
| MetaSchedule: 自动调度与迁移学习（TVM 演进） | 2022 | L6 | schedule 迁移 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| MLC-LLM: Universal LLM Inference Engine（技术博客 + MLSys/arXiv 系列） | 2023-2024 | L7/L8 LLM 编译部署 |
| WebLLM / MLCEngine: Browser-native LLM inference (web) | 2023-2024 | L8 端侧/浏览器 |
| Relax: A Composable Compiler for Deep Learning on Heterogeneous Devices (arXiv) | 2022 | L7 |
| TensorIR: An Abstraction for Automatic Tensorized Program Optimization (ASPLOS) | 2023 | L5 |
| FlashInfer: Efficient Attention Engine with block-sparse & JIT | 2024 | L8 注意力编译 |
| torch.compile / TorchInductor 技术报告 | 2022-2023 | L1 图编译现代代表 |
| TVM + Triton 协同（异构 codegen 讨论，延伸） | 2023 | L4 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| Relay/前端导入（L2-L3） | Apache TVM (relay.frontend) | Keras/ONNX/TorchScript 导入 |
| 整图优化（L3/L7） | TVM Relax / PyTorch Inductor / XLA | 融合、布局、形状特化 |
| TensorIR 调度（L5） | TVM TIR / TVMScript | 循环变换与向量化 |
| 自动调优（L6） | AutoTVM / Ansor / MetaSchedule / GAMMA | 搜索代价模型 |
| 端侧部署（L4） | microTVM / TVMC / ExecuTorch（对照） | MCU 运行时与 codegen |
| 异构后端（L4） | TVM LLVM/CUDA/OpenCL/Vulkan/Metal 后端 | 统一 codegen |
| LLM 编译（L8） | MLC-LLM / WebLLM / MLCEngine | 统一 LLM 推理栈 |
