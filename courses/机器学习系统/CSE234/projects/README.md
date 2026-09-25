# UCSD CSE234 配套项目计划

> 原则：按课程"Part1 基础 → Part2 系统 → Part3 LLM"递进，每章一个可运行小项目，动手对齐 nanoGPT/nano-vllm 生态；本轮只规划代码与 build 方式、不写代码。语言：Python + Triton（课程原生），无 GPU 时提供 CPU 等价实现。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L2 计算图与 AD | Python (numpy) | 手写 mini-autograd 并训练 MLP（对照 micrograd） | `pytest miniad/test_grad.py`；`python miniad/train.py` |
| L3 张量与 GEMM | Python (numpy/CUDA) | 分块 GEMM vs 朴素实现性能对比，画 roofline | `python gemm/bench.py`；`nvcc tiled_gemm.cu`（可选） |
| L4-L5 GPU/CUDA MatMul | CUDA/Triton | Triton 写 tiled matmul，与 cuBLAS 对比 TFLOPS | `triton_compile matmul.py && python bench.py` |
| L6 Triton 算子 | Python (Triton) | fused softmax + fused layernorm kernel | `python triton_ops/test_fused.py` |
| L7 图优化 | Python | torch.compile 前后 kernel 数与延迟对比分析 | `python graphopt/compile_bench.py` |
| L8 内存 | Python (PyTorch) | 激活重计算与 ZeRO 风格分片模拟，测峰值显存 | `python mem/recompute.py --model gpt2` |
| L9 量化 | Python (PyTorch/HF) | INT8 PTQ + AWQ 量化 1.5B 模型并测 ppl/吞吐 | `python quant/run_awq.py` |
| L10-L11 并行 | Python (PyTorch) | 列/行切分张量并行线性层 + DDP 对比；1F1B 调度模拟 | `torchrun --nproc_per_node=2 tp_linear.py` |
| L12-L13 LLM 训练 | Python (PyTorch/Triton) | nanoGPT 骨架 + 手写 FlashAttention 前反向（小尺寸） | `python flashattn/minifat.py --check` |
| L14 LLM 推理 | Python | 迷你 vLLM：连续批处理 + PagedAttention KV 管理（对齐 nano-vllm） | `python minivllm/serve.py --model 0.5B` |
| L15 Scaling | Python | 小 GPT 做 compute-optimal 实验（多组 N-D 配比画幂律） | `python scaling/run_grid.py` |
| L16-L19 Guest | Python | agents/tool-use 小系统：检索 + 工具调用 demo | `python agents/run_tool.py` |
