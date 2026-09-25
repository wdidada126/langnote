# MLC（机器学习编译）配套项目计划

> 原则：每讲一个可运行 notebook/小项目，对齐官方作业（mlc-ai/notebooks/assignment）；本轮只规划代码与 build 方式、不写代码。语言 Python（TVM/PyTorch），部分性能实验需 GPU。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L2 端到端编译 | Python (TVM) | Keras MobileNet 导入 TVM → 自动调优 → 目标设备跑通并对齐输出 | `python ch2_compile/keras_tvm.py --target llvm` |
| L3 PyTorch 接入 | Python (TVM) | TorchScript/ONNX 两路导入 ResNet，图优化后精度/性能对比 | `python ch3/torch_import.py`；`pytest test_parity.py` |
| L4 算子编译 | Python (TVM) | 手写矩阵乘 tensor program 并 lowering 到 CUDA/LLVM | `python ch4/matmul_tvm.py --target cuda` |
| L5 TensorIR | Python (TVM/TVMScript) | TVMScript 重写 conv schedule：split/fuse/reorder 优化 | `python ch5/tir_conv.py`；`tvm.script` 校验 |
| L6 自动优化 | Python (TVM) | AutoTVM vs Ansor 在同一模型上对比调优时间与性能 | `python ch6/autotune.py --task ansor` |
| L7 Relax 整图 | Python (TVM Relax) | 用 Relax 做整图融合与动态形状实验 | `python ch7/relax_graph.py` |
| L8 LLM 编译 | Python (MLC-LLM) | MLC-LLM 编译 7B 模型到多平台（CUDA/Web）并测吞吐 | `python -m mlc_llm.build --model ...`；`mlc_chat benchmark` |
| 综合 | Python | 自定模型全链路：PyTorch → Relax → 目标硬件 → benchmark 报告 | `python final/run_all.py --report` |
