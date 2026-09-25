# 智能计算系统（AICS）配套项目计划

> 原则：与 2024 新版实验线对齐，每章一个可运行小项目；本轮只规划代码与 build 方式、不写代码。语言：Python（框架/训练）、C++/CUDA（算子）；BCL 实验用寒武纪平台，无硬件时以 CUDA/CPU 等价实现替代并标注。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2 算法基础（实验1） | Python (PyTorch) | PyTorch 复现 CNN/RNN/Transformer 小任务（MNIST→TinyShakespeare） | `python ch2/train.py --model cnn` |
| L3 框架原理（实验2） | Python (numpy) | 手写 mini 框架：Value 计算图 + autograd + 3 个算子 | `pytest ch3/test_autograd.py` |
| L5 卷积算子（实验3/4） | C++/CUDA（CPU 回退） | 手写 forward/backward 卷积，im2col 优化，对齐 torch | `nvcc conv.cu -o conv` / `g++ -O3 conv.cpp`；`./run_tests.sh` |
| L5 算子融合（实验5） | CUDA/Python | 手写 Conv+ReLU 融合，对比未融合耗时 | `python fusion/bench.py`（GPU） |
| L4 硬件设计（实验6） | Verilog/Python 仿真 | mini 数据流加速器 RTL 或行为级仿真 | `iverilog mlu_sim.v` 或 `python sim/df_model.py` |
| L6 评估（实验7） | Python | 对同一模型做 CPU/GPU/端侧延迟-吞吐-能效 benchmark 报告 | `python bench/run.py --device all` |
| L7 大模型（新版实验） | Python (PyTorch/HF) | 小 GPT 训练 + INT8 量化 + 部署推理一条龙 | `python llm/train.py`；`python llm/quant.py --int8` |
| L8 综合设计（实验8） | Python/C++ | 自选端侧模型全栈优化：算子+量化+profiling | `python final/run_all.py` |
