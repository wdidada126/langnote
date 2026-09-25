# NJUOS 论文与前沿清单（papers.md）

> 骨架级清单，正文由后续专人展开。关联讲次对应 notes/outline.md。

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The UNIX Time-Sharing System (Ritchie & Thompson, CACM) | 1974 | 文件/进程/管道三大抽象的原始定义 | L6/L9/L17 |
| Exokernel (Engler & Kaashoek, SOSP) | 1995 | 「OS 应只提供复用与保护」——对象+API 视角的极端化 | L8 |
| Threads Cannot be Implemented as a Library (Ousterhout, SIGOPS PPR) | 1995 | 用户级/内核级线程之争的经典论证 | L9 |
| What Every Programmer Should Know About Memory (Drepper) | 2007 | 存储器层次与虚拟内存的权威长文，内存讲次主读物 | L13–L15 |
| A Log-Structured File System (Rosenblum & Ousterhout, SOSP) | 1991 | 日志结构化存储思想源头 | L17 |
| Virtual Memory (Denning, ACM Computing Surveys) | 1970 | 局部性与工作集模型奠基，置换策略理论根基 | L15 |

## 近五年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Rust for Linux：安全语言进入内核（社区白皮书与配套论文） | 2021–2024 | 用所有权系统消除内存安全类内核缺陷 | L2/L11/L19 |
| io_uring 与内核旁路 I/O 系列 | 2021–2023 | 系统调用边界重构：从 trap 到共享环形队列 | L7/L18 |
| seL4 与内核形式化验证更新篇 | 2021–2024 | 迷你内核正确性可证明的现代路径，OSLab 的理想参照 | L19 |
| 分层内存/CXL 页放置论文（如 TPP/Memtis） | 2021–2023 | 新硬件让经典虚拟内存研究重新升温 | L14–L15 |
| 持久内存文件系统与崩溃一致性（CrossLog、ZenFS 等） | 2021–2023 | 日志与文件系统协同设计新范式 | L17 |

## 知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 说明 |
| --- | --- | --- |
| 状态机式 shell | busybox sh、dash | MiniLab shell 的生产对照 |
| 动态链接 | glibc ld.so、musl | LD_PRELOAD/PIC 机制的权威实现 |
| 协程 | libco、Boost.Context、Go runtime | 百行协程实验的工程放大版 |
| 调度器 | Linux EEVDF 调度器、BFS | 公平性与实时策略落地 |
| 内存管理 | Linux mm 子系统、xv6 | 页表/置换/回收逐层对照 |
| FAT/文件系统 | FatFs (elm-chan)、dosfstools | MiniLab myfat 的工业版 |
| 迷你内核 | xv6、ToaruOS、MizuKi | OSLab 毕业后的自然延伸 |
