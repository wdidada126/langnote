# Stanford CS149 并行计算（Parallel Computing）

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | Stanford CS149: Parallel Computing（姊妹课 CMU 15-418） |
| 学校 | Stanford University（课程源于 CMU 15-418） |
| 主讲 | Kayvon Fatahalian（+ Pedro Lopez 等助教，作业版配合 Cesare Mantovani） |
| 教材 | 无指定教材，以讲义 + 阅读材料为主 |
| csdiy 路径 | `并行与分布式系统/CS149`（csdiy 页面：CMU 15-418/Stanford CS149） |
| 最新期次 | CS149 Fall 2021（gfxcourses 公开作业版）；CMU 15-418 有完整录影 |
| 状态 | 骨架（README + outline + papers + projects 计划） |

- 课程网站：https://cs149.github.io/ 、作业版 https://gfxcourses.stanford.edu/cs149/fall21
- CMU 15-418 录影：http://www.cs.cmu.edu/~dga/15-418/Fall20.html
- csdiy 资源汇总：PKUFlyingPig/CS149-parallel-computing

## 为什么学

- 深入理解现代并行硬件（多核 CPU、GPU、集群）的设计原则与权衡，是打通「体系结构 → 系统软件 → 分布式」的关键一环。
- 学会用 CUDA、MPI、OpenMP、Threading Building Blocks、Spark 等框架编写高性能并行程序，5 个编程作业覆盖性能分析、多线程同步、GPU 编程、分布式框架，理论实践并重。
- 为后续 6.5840/6.824（分布式）、ML Systems（15-442、10-414）、GPGPU 推理优化（vLLM/FlashAttention 类工作）打下直接基础。

## 先修与知识联系

- 先修：计算机体系结构（CS61C / DDCA / CSAPP 之缓存与流水线）、熟练 C++、操作系统基础（虚拟内存、调度）。
- 联系：
  - 上游：CS61C/CSAPP（缓存层次、局部性）→ 本课的内存层级与 false sharing；
  - 平行：CMU 15-418（内容更丰富，含录影，可与本课讲义互为补充）；
  - 下游：MIT 6.5840/6.824（从单机并行走向跨机分布式）、KAIST CS431（并发编程细节）、MLC/10-414（把并行原语用到深度学习系统）。

## 讲义章节目录（按 CS149 Fall 2021 / 15-418 主题整理）

| 讲次 | 标题 | 阅读材料 |
|---|---|---|
| L1 | 课程导入：并行性的层次与本课程地图 | 讲义；Patterson & Hennessy 并行章节导言 |
| L2 | 并行硬件：多核 CPU、缓存层级、GPU | 讲义；Intel/AMD 多核架构白皮书 |
| L3 | 程序的表示与执行：ILP、SIMD、乱序执行 | 讲义；Agner Fog《Instruction Sets》选读 |
| L4 | 数据并行：map/reduce/scan 与原语抽象 | 讲义；MapReduce (OSDI'04) |
| L5 | 任务并行：fork-join、任务图、工作窃取 | 讲义；Cilk 相关论文节选 |
| L6 | 同步：锁、原子操作、无锁结构与内存模型 | 讲义；Hazy: "The Churn"（C++ 内存模型） |
| L7 | 顺序与结合律：prefix sum、并行归约的正确性 | 讲义；Blelloch 1990（prefix sum 经典） |
| L8 | 通信与数据搬移：NUMA、PCIe、网络、局部性优化 | 讲义；MPI 标准入门章节 |
| L9 | 并行模式与自动并行化 | "Patterns for Graph Processing" / TBB 手册节选 |
| L10 | GPU 编程：CUDA 执行模型、共享内存优化 | CUDA C Programming Guide 节选 |
| L11 | 集合通信：broadcast、reduce-scatter、all-to-all 与带宽模型 | 讲义；NCCL 文档 |
| L12 | 分布式并行框架：Spark 与数据并行系统 | RDD (NSDI'12)；Spark 论文/文档 |
| L13 | 端到端案例：图处理 / 深度学习中的并行 | PowerGraph / 深度学习并行策略论文节选 |
| L14 | 性能度量与评测：强/弱扩展、roofline、Amdahl | Williams "Roofline" (SC'09)；课程作业回顾 |

> 注：以当期官网 schedule 为准；本表为骨架级整理，用于逐讲填充 notes/。

## 作业与项目（概览）

5 个编程作业：① 图像 pipeline 性能分析（PIL 风格）② 多线程任务/同步（C++ threads）③ CUDA 粒子模拟/mandelbrot ④ 分布式（MPI/Socket）数据并行 ⑤ Spark/框架实战。详见 `projects/README.md` 的配套复刻计划。
