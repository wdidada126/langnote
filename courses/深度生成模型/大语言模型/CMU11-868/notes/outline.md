# CMU 11-868 讲义骨架（outline）

> 骨架级要点，填充时对照官网每讲 slide 与指定论文展开。

## L1 LLM 系统总览
- LLM 生命周期：数据 → 预训练 → 对齐 → 推理服务 → 运维，系统问题在每个环节的形态
- 算法视角与系统视角的交汇：同样模型，吞吐/成本差 10x 的来源
- 课程项目地图：miniTorch 从 Python 到 CUDA 到分布式的演进路线
- 衡量指标：MFU、tokens/s、$/token、TTFT/TPOT 等术语表

## L2 LLM 基础：Transformer 与预训练
- Encoder/Decoder、causal self-attention、FFN 的参数量与 FLOPs 计算
- 预训练目标：next-token 交叉熵；缩放律初步
- KV Cache 的由来：自回归解码的内存-带宽瓶颈（贯穿全课）
- 分词器、上下文窗口、采样策略（温度/top-p）基础

## L3 GPU 架构与并行编程模型
- SM、warp、寄存器/共享内存/全局内存层级与带宽数字
- 内存合并访问、占用率（occupancy）、算术强度与 roofline 模型
- 为何 attention/elementwise 操作大多是 memory-bound
- PMPP 章节配合：thread/block/grid 映射思维

## L4 CUDA kernel 编程与算子实现
- kernel 启动、索引计算、边界处理；归约与 scan 模式
- 手写矩阵乘 tiled SGEMM：从 naive 到共享内存分块
- 在 miniTorch 中为 matmul/softmax 添加 CUDA 后端
- 性能剖析：nsight/Nsight Compute 指标解读

## L5 自动微分与框架设计
- 前向模式 vs 反向模式；tape/动态图实现
- 算子-梯度注册、autograd 引擎、内存换计算（gradient checkpointing）
- 二阶梯度与对齐训练的需求（RLHF 中 actor-critic 同时反传）
- 框架抽象：Tensor/Function/Module 的最小设计

## L6 模型编译与执行优化
- 图捕获、算子融合、layout 变换、内存规划
- XLA/HLO、TorchInductor、Triton（tile 级 DSL）三层对比
- CUDA Graph 与 kernel launch 开销
- 编译视角看 FlashAttention：为何通用编译器做不出

## L7 训练数据与 tokenizer 系统
- 数据管线：抓取、去重（MinHash）、质量过滤、混合配比
- tokenizer 训练（BPE）与词表设计对下游的影响
- 数据加载 I/O 瓶颈：packed sequence、mmap、WebDataset
- 数据治理与合规（与 11-667 伦理章节呼应）

## L8 高效训练：长序列与注意力优化
- FlashAttention：tiling + 重计算，在线 softmax 精确求和
- 长上下文：Ring Attention / Ulysses 序列并行；RoPE 外推
- 注意力的 IO 复杂度分析（HBM↔SRAM 搬运次数）
- A3 作业核心：手写 CUDA softmax/LayerNorm 融合提速

## L9 数据并行与 ZeRO/FSDP
- DDP：梯度 all-reduce、bucket 与通信-计算重叠
- ZeRO 阶段 1/2/3：优化器状态/梯度/参数分片与通信代价
- FSDP 实现细节：ShardedGradHook、reshard 策略
- A4 作业：多卡分布式训练搭建与吞吐测量

## L10 张量并行与流水线并行
- Megatron 列/行切分：一次 all-reduce 的注意力与 MLP 并行
- 1F1B 流水线调度与 micro-batch 气泡权衡
- 通信拓扑意识：机内 NVLink vs 机间网络
- 3D 并行组合的显存/吞吐账本

## L11 自动并行化
- 计算图切分搜索：算子级并行策略（Alpa SPMD/OP 并行）
- 代价模型与 ILP/启发式求解
- 手工 3D 并行 vs 自动并行化的工程取舍
- 大规模故障与弹性训练：checkpoint/重启成本

## L12 MoE 稀疏化
- 路由（top-k gating）、负载均衡损失、专家并行通信（all-to-all）
- Switch/Mixtral/Megablocks 结构对比；共享专家方案
- 推理侧 MoE：专家缓存、offloading、批量效应
- 稀疏激活对显存带宽与并行策略的改变

## L13 量化与压缩
- 权重量化（GPTQ/AWQ/SmoothQuant）：对称/非对称、per-group
- KV Cache 量化；激活量化难点（outlier）
- 量化 kernel：INT8/INT4 GEMM、dequant 融合
- 质量评估：perplexity 退化与下游任务回归测试

## L14 PEFT 与蒸馏
- LoRA 低秩更新的显存账与合并部署；QLoRA 4bit 基座 + LoRA
- Adapter/prefix tuning/全参微调的选择谱
- 蒸馏：logit/特征蒸馏，小模型继承能力边界
- 多 LoRA 服务化：批量热切换（S-LoRA 类系统）

## L15 对齐系统（RLHF）
- 三阶段：SFT → 奖励模型 → PPO；数据与算力规模感受
- PPO 系统难处：四个模型共存、rollout 与训练引擎异构
- DPO/GRPO 简化路径：从系统角度省掉了什么
- veRL/TRL/OpenRLHF 框架架构剖析

## L16 LLM 推理服务
- vLLM：PagedAttention 虚拟内存式 KV 管理、continuous batching
- 调度器设计：prefill/decode 混合、抢占与重计算
- 指标：TTFT 与 TPOT 的延迟分解
- 与 TensorRT-LLM、SGLang（RadixAttention）对比

## L17 推理加速
- 投机解码：draft 模型、验证、接受率；Medusa/EAGLE 多头方案
- 长上下文 KV 传输与压缩（CacheGen 思路）
- 前缀缓存复用；多轮对话的缓存管理
- 解码并行化：chunked/parallel decoding 与局限

## L18 RAG 系统
- 检索栈：嵌入模型、ANN 索引（HNSW/IVF）、混合检索
- 分块、重排序、生成侧融合；端到端延迟预算
- 向量数据库选型与规模成本
- 与长上下文模型的竞争与组合

## L19 多模态 LLM 系统
- 视觉编码器 + 投影层 + LLM 主干的组装方式
- 视觉 token 的序列长度爆炸与压缩/池化
- 训练数据管线与交错模态打包
- 推理侧：图像缓存与流式生成

## L20 Agent 与工具调用运行时
- ReAct 循环、工具 schema、上下文管理与剪枝
- 运行时系统：并行工具调用、沙箱、状态持久化
- 长任务可靠性：重试、检查点、评测基准
- 与 RL 后训练（推理模型）的联系

## L21 在线维护与部署
- 金丝雀发布、A/B、评测回归在 LLM 服务中的形态
- 可观测性：请求级 trace、GPU 指标、成本归因
- 故障模式：NaN 训练崩溃、慢节点、网络抖动
- 工业嘉宾案例笔记占位

## L22 期末项目与前沿回顾
- 项目提案/展示/报告要求（课程 logistics）
- 全课知识地图：训练-压缩-服务一条链的决策点
- 2025 前沿：推理模型系统需求（长思维链对 batching 的冲击）
- 下一步学习路径：15-779、MLSys 论文生态
