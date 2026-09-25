# CMU 10-414 配套项目计划

> 原则：按 5 个 Homework 的增量脉络，每章一个可运行小项目；本轮只规划代码与 build 方式、不写代码。语言：Python（autograd/optim/nn）+ C++/CUDA（HW5 GPU）。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L4 前向/反向 AD（HW1） | Python (numpy) | 实现 forward-mode 与 backward-mode autodiff，训练 MLP 做回归/分类 | `pytest homework1/test_*.py`；`python homework1/main_mlp.py` |
| L5-L7 backend+optim（HW2） | Python (numpy) | 构建 tensor backend + autograd + 损失/优化器/数据加载器 | `pytest homework2/test_backend.py` |
| L8 CNN（HW3） | Python (needle/C++) | 用 needle 框架训练 CNN 跑 MNIST/FashionMNIST | `python homework3/cnn/train.py`；`build.sh` 编译 cpp backend |
| L9 RNN/Transformer（HW4） | Python (numpy/C++) | 手写 LSTM/Transformer 层并做语言建模 | `python homework4/language_model/train.py` |
| L10 GPU（HW5） | CUDA/C++ | 接入 cuDNN/GEMM 后端，对比 CPU/GPU 吞吐 | `nvcc backend/src/cuda/*.cu`；`pytest test_cuda.py`（GPU） |
| L11 混合精度 | Python (PyTorch/needle) | FP16/loss-scaling 改造 needle 训练，对比收敛 | `python mp/run_fp16.py` |
| L12 性能建模 | Python/CUDA | 对 GEMM/conv 测算术强度画 Roofline | `python perf/roofline.py` |
| L13 分布式概览 | Python | 数据并行 mini-DDP（梯度 all-reduce）玩具 | `mpirun -np 2 python ddp/ring.py` |
| 综合 | Python/C++ | needle 全库整合：跑通 Transformer 端到端 | `python needle_e2e/run.py` |
