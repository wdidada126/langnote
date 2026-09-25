# CMU 15-442 配套项目计划

> 原则：与课程三大作业对齐 + 每模块一个可运行小项目；本轮只规划代码与 build 方式、不写代码。语言混合：Python（AD/分布式）、C++/CUDA/Triton/TIRx（GPU 算子）。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2 自动微分（作业1） | Python (numpy) | 扩展图 AD（控制流 + 自定义算子），梯度检查对齐 finite-diff | `pytest tests/test_ad.py`；`python example/train_mlp.py` |
| L3 框架 | Python | 手写 mini-tensor + dispatcher，支持 eager/lazy | `python minitent/test_ops.py` |
| L4-6 GPU GEMM（作业3） | CUDA/Triton/TIRx | 从 naive 到 Swizzle+TMA+WarpSpec 的 FP16 GEMM，对标 cuBLAS | `nvcc gemm.cu -arch=sm_100a`；`python bench.py`（需 B200，可 CPU 仿真验证正确性） |
| L7 ML 编译 | Python (TVM) | 用 TensorIR 手写并 auto-tune 一个 conv 算子 | `python tvm_tune.py --target cuda` |
| L8 数据并行 | Python (MPI/NumPy) | Ring All-Reduce 实现并测带宽扩展 | `mpirun -np 4 python allreduce.py` |
| L9 ZeRO（作业2） | Python (MPI/NumPy) | ZeRO-3 参数分片 + 梯度 all-gather 训练 MLP | `mpirun -np 4 python zero3_train.py` |
| L10 模型并行 | Python (PyTorch) | 张量并行线性层 + 流水线 1F1B 调度模拟 | `torchrun --nproc_per_node=2 tp_linear.py` |
| L11 LLM 推理 | Python | 迷你 continuous-batching 调度器 + PagedAttention KV 管理（对齐 nano-vllm） | `python minivllm/serve.py`；CPU 可跑 |
| L12 投机解码 | Python | 草稿模型 + 验证的投机解码 demo，测加速比 | `python spec_decode/run.py` |
| L13 量化 | Python (PyTorch) | INT8 对称/非对称量化感知训练 + PTQ 对比 | `python quant/qat.py` |
| L14 Mega-Kernel | Python/Triton | 把 mini-Transformer 融合为单 kernel（研究性） | `python megakernel/fused_attn.py` |
