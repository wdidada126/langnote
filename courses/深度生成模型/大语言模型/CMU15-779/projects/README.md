# CMU 15-779 配套项目计划

> 本轮只登记计划，不写代码；每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一执行。可对齐课程"每周 paper review + 期末系统项目"节奏。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1 框架抽象 | Python | 用 TorchFX 抓取计算图、统计融合机会并可视化 | `python graph_probe.py` |
| L2 GPU/CUDA | CUDA C++ | tiled matmul 三版演进 + occupancy 调参报告 | `nvcc -O3 mm.cu -o mm && ./mm` |
| L3-L4 Attention/CUDA 进阶 | CUDA/Triton | naive vs flash attention 复现；warp-specialized 小实验 | `python attn_bench.py`（含 .cu 扩展 `pip install .`） |
| L5 Triton DSL | Python + Triton | Triton 写 softmax/LayerNorm/QKV-proj 融合并测速 | `python triton_ops.py` |
| L6 自动调优 | Python | TVM/Ansor 跑一个 conv 调优或与 cuBLAS 对比 | `python ansor_tune.py` |
| L7 图/超优化 | Python | TASO/Mirage 玩具图等价搜索；Inductor pattern match 实验 | `python graph_opt.py` |
| L8-L9 并行训练 | Python (torchrun) | 2-4 卡 ZeRO-2 vs FSDP vs 手写 TP 的吞吐矩阵 | `torchrun --nproc_per_node=4 parallel_bench.py` |
| L10 自动并行 | Python | 小 MLP 切分搜索：枚举 vs Alpa 思路代价模型 | `python stage_search.py` |
| L11 长上下文 | Python | Ring Attention 模拟（多卡序列并行）显存/通信曲线 | `torchrun ... ring_attn.py` |
| L12 服务系统 | Python (C++ 可选) | mini-vLLM：块表 KV + continuous batching 调度器 | `python mini_serve.py` |
| L13 推理加速 | Python | 草稿-验证投机解码复现（接受率与加速比测量） | `python spec_decode.py` |
| L14 后训练 | Python | 多 LoRA 热切换服务 demo；mini GRPO 训练循环 | `python lora_switch.py` / `python grpo_mini.py` |
| L15 MoE | Python | top-k 路由 grouped-GEMM kernel（Triton）+ all-to-all 模拟 | `python moe_kernel.py` |
| L16 期末项目 | Python+CUDA | 选题示例：prefill/decode 分离调度器 / MLA 复现 / MoE 专家放置 | `bash build_all.sh`（本轮不执行） |
