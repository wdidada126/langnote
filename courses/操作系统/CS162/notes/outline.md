# CS162 讲义骨架（notes/outline.md）

> 每讲 3–5 条要点，骨架级。

## L1 导论：什么是 OS
- OS = 资源管理器（时间/空间复用）+ 虚拟机（提供更好接口）。
- 抽象三件套：进程、地址空间、文件。
- 内核态/用户态双模式与特权级切换开销。
- 课程地图与 Pintos 环境部署。

## L2 内核体系结构
- 宏内核 vs 微内核：性能与隔离的权衡。
- 中断向量表、异常与系统调用是三条入核路径。
- 模块化设计与可加载内核模块。
- Pintos 源码树导读（threads/vm/files 三层）。

## L3 线程与上下文切换 I
- 线程 = 执行流 + 寄存器组 + 栈；内核线程 vs 用户线程。
- 上下文切换保存/恢复的最小状态集（PC/SP/寄存器）。
- 栈与帧布局：切换实现（Pintos switch.S）。
- Project1/Threads 的第一步：thread_create/thread_start。

## L4 调度
- 指标：周转时间、响应时间、公平性；FCFS/SJF/MLFQ 谱系。
- 多级反馈队列的启发式与病态案例。
- 实时调度 EDF 导览。
- Pintos 要求严格优先级调度器（Homework+Project）。

## L5 系统调用与边界
- syscall 指令、参数传递与 errno 约定。
- 内核如何拷贝并校验用户指针（copy_from_user 思想）。
- 经典案例：fork/exec/wait 语义（25 年 Project 新增 fork）。
- 用户/内核栈切换与重入问题。

## L6 同步 I：互斥与条件变量
- 临界区问题：互斥、前进、有限等待。
- 关中断/spinlock→mutex 的实现层级。
- 条件变量 + 谓词循环的标准模式。
- Pintos 阻塞式 timer_sleep 的定时器中断驱动。

## L7 同步 II：信号量与死锁
- 信号量计数语义；用信号量构造 mutex 与栅栏。
- 死锁四条件与破坏策略（锁序、超时、检测）。
- 优先级反转：优先级继承（Pintos 调度器关键考点）。
- 原子指令 CAS/LL-SC 与无锁结构简介。

## L8 内存布局与地址空间
- 代码/数据/堆/栈五段布局与增长方向。
- 地址翻译启动：加载器如何建立初始内存映像。
- malloc/sbrk：实现内存分配器（Memory Homework）。
- 碎片：内部/外部与分配策略。

## L9 虚拟内存 I
- 机制/策略分离：页表提供机制，OS 决定策略。
- 多级页表、TLB 与地址翻译快路径。
- 缺页异常处理流程（demand paging）。
- Pintos vm 层：从 userprog 到 mmap 的演进。

## L10 虚拟内存 II
- 局部性与工作集；置换算法 FIFO/Clock/LRU 近似。
- 抖动与 thrashing 防治。
- 写时复制支撑 fork（呼应 CSAPP Ch.9）。
- Project 考点：页面回收与 swap。

## L11 I/O 设备与中断
- 轮询→中断→DMA 三级演进。
- 中断处理上半部/下半部分工。
- 设备驱动抽象与中断风暴应对。

## L12 磁盘与 SSD
- 磁调度：SCAN/CSCAN 与请求合并。
- SSD：擦除块、FTL、写放大与 TRIM。
- 磁盘可靠性：坏块重映射与 SMART。

## L13 文件系统 I：接口
- 统一接口 open/read/write/close/stat 的设计哲学。
- 目录即特殊文件；路径解析与硬链接/符号链接。
- Shell Homework：管道/重定向/路径解析全用上。

## L14 文件系统 II：实现
- inode、间接块与索引结构；位图分配空间。
- Buffer cache 与写回策略（File Systems Project 考点）。
- 日志（WAL）：redo/undo 与检查点。
- 可扩容文件与稀疏文件实现。

## L15 崩溃一致性
- fsync 语义与「崩溃后必须什么是对的」。
- 日志顺序依赖与屏障指令。
- fsck 修复与一致性检查（呼应 6.S081 log fs）。
- 子目录与目录树一致性维护。

## L16 网络
- TCP/IP 栈在 OS 中的分层与 socket API。
- 阻塞 send/recv 与事件驱动的两种服务模型。
- HTTP Homework：GET 服务器实现。

## L17 RPC 与分布式文件
- 调用语义：at-least-once/at-most-once。
- 序列化与桩代码（RPC Lab/Homework 子任务）。
- NFS/AFS 的设计教训。

## L18 MapReduce 与容错
- 分片、shuffle、规约的分布式骨架。
- 慢任务兜底（backup task）与失败重试。
- MapReduce Homework：可容忍错误的简易实现（可与 6.824 作业互换）。

## L19 安全与隔离
- 最小特权、完全中介、开放设计原则。
- 地址空间隔离与安全边界：Spectre 类侧信道导览。

## L20 虚拟化与容器
- 虚拟机监控器类型 I/II 与 Trap-and-Emulate。
- 影子页表/EPT 硬件辅助翻译。
- 容器 = 命名空间 + cgroup 的轻量隔离。

## L21 论文研讨 I
- Exokernel：应用级资源管理的设计空间（精读+讨论）。
- 微内核回潮（Fuchsia/Sel4 相关论文）。

## L22 论文研讨 II 与复习
- 当期指定 OSDI/SOSP 论文（每年更新，如异步持久内存、tail fences 等）。
- 全课程串讲：抽象-机制-策略-权衡一张图。
- 与 6.824/15445 的知识接口自查。
