# CMU 11-868 配套项目计划

> 本轮只登记计划，不写代码；每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一跑。课程作业（miniTorch A1-A5）为主线参照。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L2 总览与 Transformer | Python | 迷你 GPT：从零训练字符级 Transformer 并测 tokens/s 基线 | `python train_gpt.py --steps 1000` |
| L3-L4 GPU/CUDA | CUDA C++ + Python | 手写 tiled matmul 与 softmax kernel，对比 PyTorch 吞吐 | `nvcc -O3 matmul.cu -o matmul && python bench.py` |
| L5 自动微分 | Python | miniTorch 风格反向模式 autograd 引擎（A1 简化版） | `pytest -q`（纯 Python） |
| L6 编译 | Python + Triton | Triton 重写 LayerNorm/attention，测 CUDA Graph 前后 launch 开销 | `python triton_bench.py` |
| L7 数据 | Python | 语料清洗+去重+LLaMA 风格 tokenizer 打包管线 | `python data_pipeline.py --raw ./corpus` |
| L8 注意力优化 | CUDA/Triton | 复现 naive vs flash 的 attention 内存搬运计数与耗时 | `python attn_ablate.py` |
| L9-L10 分布式 | Python + PyTorch (torchrun) | 2 卡复现 DDP+ZeRO-1 分片；手写列/行张量并行 MLP | `torchrun --nproc_per_node=2 ddp_zero.py` |
| L11 自动并行 | Python | 小图代价模型：枚举切分方案选最优（Alpa 玩具版） | `python parallel_search.py` |
| L12 MoE | Python | top-k 路由 + 负载均衡损失的小型 MoE 训练；all-to-all 模拟 | `python train_moe.py` |
| L13 量化 | Python + C/C++ | INT8/INT4 per-group 权重量化 GEMM 与困惑度回归 | `python quant_eval.py` / C++ 版 `make && ./qgemm` |
| L14 PEFT | Python | LoRA 微调小模型 + 多 LoRA 热切换服务演示 | `python lora_ft.py && python serve_multi_lora.py` |
| L15 对齐 | Python | 玩具 RLHF：SFT→RM→PPO/DPO 对比训练曲线（A5 方向） | `python rlhf_mini.py --algo {ppo,dpo}` |
| L16-L17 服务与加速 | Python (C++ 可选) | 极简 vLLM：PagedAttention 块表 + 连续批处理调度器；草稿-验证投机解码 | `python mini_serve.py` |
| L18 RAG | Python | 本地嵌入 + HNSW 检索 + 重排序的端到端问答与延迟画像 | `python rag_pipeline.py` |
| L19 多模态 | Python | 视觉投影层拼接 LLM 的最小 VLM 训练与服务 demo | `python mini_vlm.py` |
| L20 Agent | Python/TS | 工具调用运行时：并行工具执行 + 上下文管理沙箱 | `python agent_runtime.py` / TS 版 `npm i && npm run dev` |
| L21 运维 | Python/Go | 推理网关：金丝雀路由、请求级 trace 与成本归因看板 | `python gateway.py` |
| L22 期末大项目 | Python+CUDA | 端到端：自训小 LLM → LoRA/DPO → 量化 → 服务并压测报告 | `bash build_all.sh`（本轮不执行） |
