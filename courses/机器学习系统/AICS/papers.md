# 智能计算系统（AICS）论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| ImageNet Classification with Deep CNNs (AlexNet) | 2012 | L2 | GPU 训练引爆深度学习，算法-硬件协同起点 |
| Very Deep Convolutional Networks (VGG) | 2014 | L2 | 堆叠 3x3 卷积 |
| Deep Residual Learning (ResNet) | 2015 | L2 | 残差连接，训练栈可运行的代表作 |
| Adam: A Method for Stochastic Optimization | 2015 | L2/L3 | 框架默认优化器 |
| Automatic Differentiation of Algorithms (Linn) / AD 综述 (Baydin) | 1970/2018 | L3 | 自动微分理论 |
| TensorFlow: A System for Large-Scale ML (OSDI) | 2016 | L3 | 工业框架设计范本 |
| Programming Patterns for GPU Computing (CUDA C Programming Guide 对应文献) | 2010+ | L5 | SIMT 编程模型 |
| Cambricon: An Instruction Set Architecture for Neural Networks (ISCA) | 2016 | L4 | 寒武纪 DianNao 系指令集，MLU 前史 |
| Eyeriss: An Energy-Efficient Reusable Accelerator (ISSCC/JSSC) | 2016 | L4 | 数据流驱动的 DNN 加速器 |
| TPU: A Domain-Specific Architecture (ISCA) | 2017 | L4 | 脉动阵列与推理加速 |
| BCL/CNRTL 相关：寒武纪编译器技术报告（延伸为 TVM, OSDI 2018） | 2018 | L5 | 算子编译与融合 |
| MLPerf: Benchmarking for Deep Learning (MICRO) | 2019 | L6 | AI 系统基准方法学 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| Merlion / 国产 AI 芯片系列（寒武纪 MLU 架构演进白皮书/论文） | 2021+ | L4 国产 NPU 路线 |
| MLPerf Inference v3.x+ 报告 | 2021-2025 | L6 评估演进 |
| AWQ: Activation-aware Weight Quantization (MLSys) | 2023 | L7 大模型压缩 |
| vLLM: Efficient Memory Management (SOSP) | 2023 | L7 大模型推理 |
| LLaMA 系列 | 2023-2024 | L7 开源大模型基座 |
| Qwen 技术报告 | 2023-2024 | L7 模型-系统协同 |
| 端侧大模型部署（MobileLLM / llama.cpp 生态论文/技术报告） | 2024 | L7 端侧全栈 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 计算图与 autograd（L3） | PyTorch / miniDL / cs231n 风格自研框架 | 算子注册、反向 tape |
| 卷积算子实现（L5） | cuDNN / MNN / ncnn / 寒武纪 CNNL | im2col/Winograd/直接卷积 |
| 自定义算子扩展（L5） | PyTorch CustomOp / TVM relay.op | forward/backward 集成 |
| BCL/GPU 编程（L5） | CUDA / Triton / HIP | SIMT 内核开发 |
| NPU 体系结构（L4） | 寒武纪 MLUarch / 昇腾 Da Vinci / NVDLA | 数据流加速器 |
| 模型压缩与部署（L7） | ONNX Runtime / TensorRT / MLC-LLM / llama.cpp | 量化/图优化/端侧运行时 |
| 评估基准（L6） | MLPerf / AI-Benchmark / 寒武纪 benchmark | 端到端性能评估 |
