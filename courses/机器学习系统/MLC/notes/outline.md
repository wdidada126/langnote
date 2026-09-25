# MLC（机器学习编译）提纲

> 骨架级要点，正文笔记待逐讲展开。

## L1 导论
- 碎片化的模型格式 × 碎片化的硬件 = 编译而非手工移植的必然性。
- 开发模式（eager）vs 部署模式（静态优化）；MLC 的抽象分层：前端图 → 中端 IR → 后端代码生成。
- TVM 在编译栈中的位置（对比 XLA/Inductor）。

## L2 模型开发者编译 I：Keras+TVM
- 前端导入：Keras/TFLite → Relay IR；`relay.frontend`。
- 整图优化 pass：融合、常量折叠、布局转换。
- 部署：graph runtime 在 CPU/GPU/移动端跑通同一模型。

## L3 模型开发者编译 II：PyTorch 接入
- TorchScript / ONNX / torch.compile 多种导入路径对比。
- 自动调优（autotune）流程：搜索 → 代价模型 → 选择 kernel。
- 跨硬件：x86/ARM/CUDA/OpenCL/Vulkan 后端统一 API。

## L4 硬件后端编译
- 从线性回归/矩阵乘的小算子看端到端 lowering：tensor op → schedule → 目标码。
- target 描述与 codegen 接口（LLVM/自定义后端）。
- 运行时（Runtime）设计：packed function、VM。

## L5 Tensor 表达式与 TIR
- TensorIR 抽象：块（block）/迭代变量/存储缓冲。
- 循环变换原语：split/fuse/reorder/pattern；向量化与并行标注。
- TVMScript 可读语法；与 Halide/ISPC 抽象对照。

## L6 自动优化
- AutoTVM：模板 + 树模型学习代价。
- Ansor：以 sketch 搜索自动 schedule，无需手写模板。
- 搜索代价建模与迁移学习（MetaSchedule）。

## L7 整图编译与 Relax
- 函数式 IR 处理控制流/动态形状；Relax 设计动机。
- 图级-算子级联合优化：whole-graph 调度。
- 部署栈：MLC-LLM/统一运行时。

## L8 前沿
- LLM 编译：KV cache 感知融合、连续批处理与编译的结合。
- 端侧/异构/浏览器（WebLLM）部署前沿；开放问题总结。
