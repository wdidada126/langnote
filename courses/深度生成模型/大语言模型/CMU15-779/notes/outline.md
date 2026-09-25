# CMU 15-779 讲义骨架（outline）

> 骨架级要点；填充时对照官网每讲 slides 与阅读列表，并把每周 paper review 笔记挂到对应讲次下。

## L1 ML 系统导论
- 核心问题：高层模型 → kernel → 异构硬件 → 集群执行的完整分解链
- 计算图抽象：静态图（TF1/XLA）vs 动态图（PyTorch）的系统含义
- 系统度量：延迟/吞吐/成本/MFU；roofline 心智模型
- 课程项目与论文 review 制度说明

## L2 GPU 架构与 CUDA
- SM/warp 执行模型；内存层级与合并访存
- occupancy、bank conflict、双缓冲；流与多流并发
- 矩阵乘分层：cuBLAS→CUTLASS→手写 tiling
- 性能计数器解读：SM busy、DRAM throughput

## L3 Attention 案例：IO-aware
- attention 的 HBM 搬运复杂度分析（为什么 naive 慢）
- FlashAttention：tiling + online softmax + 重计算
- FA2/FA3：序列维并行、warp 划分、异步 TMA/WGMMA（Hopper）
- 变体生态：varlen、paged KV 中 attention kernel 改动

## L4 高级 CUDA
- warp specialization：生产/消费角色分工隐藏同步
- persistent kernel 与 mega kernel：融合整层消除 launch 开销
- CUTLASS 3.x / CuTe 布局代数概览
- 低延迟服务场景：decode 单 token kernel 的极致优化

## L5 Tile 级 DSL
- Triton：block 编程模型、自动 layout/共享内存管理
- TileLang/其它 tile DSL：向 CUTLASS 表达能力靠拢
- DSL 表达力 vs 可优化性的光谱；何时仍需手写 CUDA
- 用 Triton 复现 softmax/LayerNorm/小 attention

## L6 内核自动调优
- AutoTVM→Ansor：从模板调参到无模板搜索（stage 分解）
- 代价模型：学习式性能预测与搜索空间剪枝
- 调优落地：kernel 库（mm/conv）自动生成为主
- 局限：对 transformer 新型算子的泛化问题

## L7 图级优化与超优化
- TASO/PET：等价变换搜索最优计算图（算子融合/layout）
- 超优化思路：Mirage 自动发现多 kernel 流水线与 pass 序列
- 编译器与算法协同：attention 模式自动匹配
- 与 TorchInductor/CUDA Graph 的工程对照

## L8 数据并行与 ZeRO
- DDP 梯度桶化与通信-计算重叠
- ZeRO 1/2/3 分片策略与通信量推导
- FSDP 实现：reshard、mixed precision、CPU offload
- 大规模训练的 all-reduce 拓扑：环/分层/网络感知

## L9 模型/流水线并行
- 张量并行切分：列/行并行、all-reduce 插入点
- 流水线 1F1B/interleaved 调度与气泡公式
- 显存-带宽-通信三角：并行策略选择的账本
- TP 的硬件耦合：NVLink 域内 vs 跨机

## L10 自动并行化
- 算子级并行（OP）vs 数据并行（SPMD）的统一搜索（Alpa）
-  inter-operator 图切分与 ILP 求解
- 工程现实：手工 3D 并行仍是主流，自动化的收益边界
- 弹性与容错：慢节点检测、检查点策略

## L11 长序列与上下文并行
- 序列并行：Ring/ Ulysses 的通信模式与显存收益
- 位置编码外推与稀疏注意力（NSA 类）
- KV cache 随上下文增长的显存压力（连接 L12/L13）
- 百万级上下文的系统工程案例

## L12 LLM 服务系统
- continuous batching；prefill/decode 的异质性调度
- PagedAttention 块表管理；RadixAttention 前缀树复用
- 分离式部署：prefill/decode 拆池（DistServe 类）
- 服务指标：TTFT/TPOT/goodput 与 SLO 设计

## L13 推理加速
- 投机解码：draft-verify、树状草稿（Medusa/EAGLE）、接受率数学
- KV 压缩：量化（KIVI）、驱逐（H2O/SnapKV）、MLA 低秩
- 加速对正确性无影响的原则（分布等价证明）
- 推理模型时代：长思维链对 batching 与调度的冲击

## L14 后训练系统
- PEFT 服务：多 LoRA 批量热切换（S-LoRA）
- RLHF 引擎：四模型放置、rollout 与训练异构引擎共享
- GRPO/PPO 的算力账；veRL HybridEngine 设计
- 数据侧：偏好/思维链数据生成的算力复用

## L15 MoE 系统
- top-k 路由的 all-to-all 通信与容量因子
- MoE kernel：grouped GEMM、expert 负载均衡的算子层技巧
- 专家并行 vs 数据/张量并行的组合策略
- DeepSeek-V3 类：FP8 训练与大规模 MoE 基础设施剖析

## L16 前沿专题与项目
- 当期主题：推理系统扩展、编译器新进展、新硬件（GB200/TPUv6）
- 项目流程：proposal → presentation → report 的评审标准
- 常见项目坑：baseline 复现、消融不足、测量噪声
- 结课知识地图：模型→kernel→集群全链决策表
