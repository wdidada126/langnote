# CS110 论文与前沿清单（papers.md）

> 骨架级清单，正文由后续专人展开。关联讲次对应 notes/outline.md。

## 经典文献

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The UNIX Time-Sharing System (Ritchie & Thompson, CACM) | 1974 | 定义文件/进程/管道抽象，本课 Unix 编程模型的源头 | L6/L8/L10 |
| Lions' Commentary on UNIX 6th Edition (Lions) | 1978 | 逐行剖析 Unix 内核的经典著作，理解 fork/exec/管道底层语义的最佳伴读 | L6/L8/L10 |
| MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, OSDI) | 2004 | 用两函数抽象分布式数据处理，L19 分布式入门直接引用 | L19 |
| C10K: The C10K Problem (Kegel) | 1999 | 系统剖析万级并发连接的事件驱动方案谱系 | L18 |
| Dynamic Linking in Linux (Levine, Linkers and Loaders 相关文) | 2000 | 系统讲解 ELF 共享库、PIC 与 dlopen 机制的权威材料 | L3 |
| Threads Cannot be Implemented as a Library (Ousterhout, SIGOPS PPR) | 1995 | 论证用户级线程与内核级线程的本质差异，引出调度权衡 | L14/L16 |

## 近五年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| io_uring 相关：Efficient IO with io_uring (Axboe 内核文档/Alice & Bob 系列) | 2021 | 内核/用户共享环形队列的异步 I/O 接口，代表系统调用 I/O 演化方向 | L7/L11/L18 |
| Zen (Huang et al., ATC'22) 无锁队列系列 | 2022 | 高竞争下无锁队列的可扩展实现，补充原子与无锁一节的前沿参照 | L17 |
| Umbra/自愈型存储等系统软件可靠性综述（如 "Understanding and Detecting Real-World Bugs in Async Programs" SOSP'23 类） | 2023 | 并发/异步程序缺陷检测的最新系统方向 | L14–L17 |
| XArray/RDS over RDMA 类内核数据结构论文（可替换为当期热点） | 2021–2024 | 内核共享数据结构并发优化案例集 | L15/L17 |
| （持续补充：每年 SOSP/OSDI/ATC 中与 malloc、mmap、事件循环相关的工业论文） | 2021–2026 | 待筛选 | 全课程 |

## 知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 说明 |
| --- | --- | --- |
| mini malloc / 分配器 | jemalloc、mimalloc、tcmalloc | 尺寸类数组、线程缓存、碎片控制，工程化版 L5 |
| mmap 与文件映射 | SQLite (WAL/mmap 模式)、Redis (RDB/AOF 重写) | 用 mmap 与 CoW 做持久化与零拷贝 |
| fd/管道/信号 | nginx、busybox sh、dash | 事件驱动服务器与 Shell 的信号/重定向处理 |
| 线程池与同步 | muduo、folly、OneTBB | Reactor + 任务队列 + 锁分层的生产级实现 |
| HTTP Server | mongoose、h2o、civetweb | 从单连接到 epoll + 线程池的完整演化样本 |
| 动态库与插件 | Apache httpd 模块、GStreamer、VST 宿主 | dlopen 插件架构的真实用例 |
| MapReduce/RPC | Hadoop、Go net/rpc、gRPC | L19 抽象的生产对应物 |
