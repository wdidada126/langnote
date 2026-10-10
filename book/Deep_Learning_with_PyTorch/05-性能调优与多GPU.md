# 《Deep Learning with PyTorch》章笔记 05 · 性能调优与多 GPU

> ⚠️ 题注：对应书中「性能与扩展」章方向（约 ch9），章名与页码凭记忆，逐字目录待购电子版销账。
> 三态标注：✅ = pytorch.org 官方文档级常识口径（多 GPU 语义以 Distributed communication 文档为准）；⚠️ = 书中位置推定；🔧 = 未实测：本机未装 torch，更无多卡环境。
> 承接 [04 册](04-序列数据与RNN.md)：模型能跑了，本章回答「为什么这么慢、怎么喂饱 GPU」。

## 核心机制

### DataLoader 流水线：用进程躲 GIL

- 预取 + 多 worker 进程把「解码/增广」放到 CPU 侧与 GPU 计算重叠；`pin_memory=True` 锁页内存加速 H2D 拷贝，配 `non_blocking` 异步搬运（✅ 官方口径）。
- 对照 CPython：数据预处理是 Python 代码，多线程受 GIL  serialization（库内 [../CPythonInternals.md](../CPythonInternals.md) 一线），故 torch 选 **multiprocessing** 而非 threading——与 [../PythonParallelProgrammingCookbook.md](../PythonParallelProgrammingCookbook.md) 的「CPU 密集上进程」结论同构；对照 Java：JVM 无 GIL，线程池即可重叠，这是 Python 生态独有的结构性税。
- 2020 书中 `num_workers` 建议值 ⚠️ 凭记忆，平台差异大，以实测为准。

### 显存分配器：缓存式 malloc

- torch 的 CUDA caching allocator 不每次 cudaMalloc，而是持有已释放块的缓存池复用；`empty_cache()` 只清缓存不动活张量，碎片化时 `max_memory_allocated` 与 `memory_allocated` 分叉（✅ 官方文档口径）。
- 对照 JVM：与「堆 + GC 回收 vs 缓存池 + 显式语义」的取舍同型（库内 [../深入理解Java虚拟机3.md](../深入理解Java虚拟机3.md) 可借心智模型）：分配器快但会把「物理占用」与「逻辑占用」分成两条曲线，OOM 报的是池账不是显卡账 ✅。

### 多 GPU：DP 与 DDP 的代际断层

- `nn.DataParallel`：单进程多线程切 batch，Python 线程 GIL 序列化 + 主卡聚集，官方自认瓶颈（✅ 文档明语）。`nn.parallel.DistributedDataParallel`：每卡一进程，反向时梯度 all-reduce 同步，官方推荐路线（✅）。
- 对照 Java 分布式：DDP 的「多对等进程 + 集合通信原语」像多线程共享内存改造成消息传递；all-reduce 语义对照 MPI 概念（文本提及，本仓无 MPI 档）。
- AMP 混合精度（`torch.cuda.amp` ✅ 2020 新件，书中若未收则 ⚠️ 缺口）与 `torch.backends.cudnn.benchmark` 属同章现代兵器，读时补官方文档。

## 批判读法（易错与存疑）

1. **先量后调**：没有 `torch.cuda.synchronize` 校正的计时全是假数（异步队列让 CPU 侧计时严重低估 ✅）；书中性能方法论的位置 ⚠️ 凭记忆。
2. **DP 教学价值已尽**：读 DP 只为理解 DDP 为何不同；2026 新项目直接 DDP/`torchrun` 口径 ⚠️ 与现行文档核对。
3. **num_workers 玄学**：Windows/容器下 worker 启动开销与死锁是平台坑，书中数字勿照抄。
4. **pin_memory 非万能**：小 batch 高延迟场景收益近零；对照 [../性能之巅.md](../性能之巅.md) 方法学（本仓在盘），先建基线再谈优化。
5. 2020 后 `torch.compile`/FSDP 等重写了本章半壁江山（✅ 后续版本事实），本书该章是「地基课」不是「现行手册」。

## 🔧 微实验位（未实测：本机未装 torch，仅为设计；多卡项待有卡环境）

- 实验 A：`num_workers=0/2/8` 三档 dataloader 吞吐计时（前后加 synchronize），看流水线重叠收益与饱和点。
- 实验 B：训练循环前后对比 `memory_allocated` vs `max_memory_allocated` 曲线，观察缓存池锯齿。
- 实验 C（需双卡）：DP vs DDP 同 batch 等效训练时长对照，复现 IPC 瓶颈结论 ⚠️ 预期依据官方文档。

## 盘谱互链

- 上一章 [04-序列数据与RNN.md](04-序列数据与RNN.md)；下一章 [06-项目实战与生态延伸.md](06-项目实战与生态延伸.md)。
- GIL 与并行：[../CPythonInternals.md](../CPythonInternals.md)、[../PythonParallelProgrammingCookbook.md](../PythonParallelProgrammingCookbook.md)；方法学：[../性能之巅.md](../性能之巅.md)；JVM 对照：[../深入理解Java虚拟机3.md](../深入理解Java虚拟机3.md)。
- 全景对照：[../MachineLearningWithPyTorchAndScikitLearn.md](../MachineLearningWithPyTorchAndScikitLearn.md)；入口：[../DeepLearningWithPyTorch.md](../DeepLearningWithPyTorch.md)、[../Python系列·总索引.md](../Python系列·总索引.md)。

## 核心概念中英对照

- **数据装载器** — `DataLoader`：批取样 + 多进程预取的流水线器。
- **锁页内存** — pinned memory：不换出页，加速异步 H2D 拷贝。
- **缓存分配器** — caching allocator：复用显存块的分配策略。
- **数据并行** — data parallelism：切 batch 不切模型，各卡算各自梯度。
- **梯度聚合** — all-reduce：多进程梯度求和的集合通信原语。
- **混合精度** — AMP：fp16 前向 + fp32 主权重/梯度的加速法。
- **同步计时** — synchronized timing：GPU 队列排空后的真实耗时口径。

> ⚠️ 欠账：ch9 章名与页码凭记忆；AMP/benchmark 是否入书未核；DP→DDP 迁移细节与 torchrun 现行口径待官方文档销账；全部实验未实测（本机无 torch、无 GPU 环境）。
