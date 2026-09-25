# CS162 论文与前沿清单（papers.md）

> 骨架级清单，正文由后续专人展开。关联讲次对应 notes/outline.md。

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The UNIX Time-Sharing System (Ritchie & Thompson, CACM) | 1974 | 确立文件/进程/管道统一抽象，OS 设计的原点 | L1/L5/L13 |
| Exokernel: An OS Architecture for Application-Level Resource Management (Engler & Kaashoek, SOSP) | 1995 | 把资源保护与抽象分离，让应用自管策略，论文研讨常驻篇目 | L2/L21 |
| The Design and Implementation of the 4.3BSD UNIX Operating System (Rosenblum & Ousterhout, TOCS) | 1992 | 缓冲缓存/虚拟内存/文件系统一体化设计的经典叙述 | L8–L15 |
| A Log-Structured File System (Rosenblum & Ousterhout, SOSP) | 1991 | 用顺序日志把随机写变顺序写，现代 WAL 源头 | L14–L15 |
| Implementing Remote Procedure Calls (Birrell & Nelson, TOCS) | 1984 | RPC 语义与实现的奠基之作 | L17 |
| MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, OSDI) | 2004 | 分布式数据处理两函数抽象，课程作业蓝本 | L18 |
| Seawind: Streams in the Kernel (Ousterhout, SOSP) | 1982 | 内核流与同步机制的优雅设计范本 | L6–L7/L11 |

> 注：正式研读名单每期更新（常见还有 µTP、Plan 9、Sprite、Firecracker 等篇目），正文阶段以当期 syllabus 为准补全。

## 近五年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Tail Fences：内核态切换软屏障新机制（近年顶会热点，具体篇目待核） | 2023 | 大幅削减内核异步转换与中断处理开销 | L3/L5–L7 |
| io_uring 方向系统论文集（内核/用户共享环形队列） | 2021–2023 | 重塑用户/内核 I/O 边界 | L5/L11 |
| seL4/Fuchsia 微内核复兴系列（形式化验证与能力模型新篇） | 2021–2024 | 可验证内核与最小特权持续进展 | L2/L19 |
| CXL 内存池化与解耦式系统栈论文集 | 2022–2024 | 新互连改变虚拟内存与分层策略 | L9–L10/L16 |
| 轻量虚拟化与 Serverless（Firecracker NSDI'20 及后续工作） | 2021–2024 | microVM 隔离与冷启动优化 | L20 |
| 持久内存/文件系统一致性新篇（CrossLog、ZenFS 生态） | 2021–2023 | 面向 NVMe/PMEM 的日志与写放大优化 | L14–L15 |

## 知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 说明 |
| --- | --- | --- |
| Pintos 教学内核 | pintos（多校 fork 与中文实验文档） | 课程原生项目，可对照实现 |
| 调度器/优先级 | Linux EEVDF 调度器、PREEMPT_RT | 优先级反转与公平调度的生产实现 |
| 虚拟内存 | Linux mm 子系统、mmap/madvise | 页面回收、CoW、透明大页 |
| 文件系统与日志 | ext4 journal、ZFS、RocksDB WAL | 崩溃一致性与日志结构化 |
| io_uring/异步 I/O | liburing、ScyllaDB | L11 I/O 演化方向的落地 |
| RPC/MapReduce | gRPC、Hadoop/Spark | L17–L18 作业的生产对照 |
| 内存分配 | jemalloc/mimalloc | Memory Homework 的工程化对照 |
