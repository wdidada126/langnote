# CSAPP 论文与延伸读物清单

> 配套 notes/L01–L20。经典表按讲次收录**真实存在**的论文/标准/权威长文；
> 近五年表收录 2020 后的论文、标准与工程文章；末尾为"知识点 ↔ 开源项目"映射表。
> 链接优先给官方/作者主页；个别老论文需自行搜题名（标注"检索"）。

## 一、经典论文 / 标准（按讲次）

| 讲次 | 文献 | 作者/出处 | 年份 | 与 CSAPP 的关系 | 链接 |
| --- | --- | --- | --- | --- | --- |
| L1 | The UNIX Time-Sharing System | Ritchie & Thompson, CACM 17(4) | 1974 | "一切皆文件/进程抽象"两大主题的源头 | dl.acm.org/doi/10.1145/361011.361067 |
| L3 | What Every Computer Scientist Should Know About Floating-Point Arithmetic | Goldberg, ACM Computing Surveys 23(1) | 1991 | 浮点全章的最佳外传，误差/舍入/NaN 语义 | docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html |
| L3 | Lecture Notes on the Status of IEEE 754 | Kahan, UCB Tech Report | 1996 | IEEE 754 之父亲述标准设计动机（检索标题） | 检索 "Kahan IEEE 754 status" |
| L3 | IEEE Std 754-2019, Standard for Floating-Point Arithmetic | IEEE | 2019 | 现行标准正文（bf16 等新格式） | standards.ieee.org |
| L7 | Smashing the Stack for Fun and Profit | Aleph One, Phrack 49 | 1996 | 栈溢出攻击开山文，ret2text/注入 shellcode 原始形态 | phrack.org/archives/issues/49 |
| L8 | A Survey of Microprocessor Pipelining Techniques / 教材级：Patterson & Hennessy | Smith; P&H CAQA | 1989/2017 | 流水线冒险与分支预测系统综述（教材 Ch.4/5） | 检索 "Patterson Hennessy" |
| L10 | Cache Memories | A. J. Smith, ACM Computing Surveys 13(3) | 1981 | 缓存映射/替换/写策略研究的开山综述 | doi.org/10.1145/356914.356920 |
| L10 | What Every Programmer Should Know About Memory | Drepper, Red Hat | 2007 | 本讲同名的"圣经级"长文（TLB/预取/优化） | 检索 "cpumemory drepper pdf" |
| L12/13 | Linkers for Large-Scale Multilanguage Development | M. Levine, Science of Computer Programming 32 | 1998 | 链接器问题的经典工程视角 | sciencedirect.com/science/article/pii/S0167642396000244 |
| L13 | How To Write Shared Libraries | Drepper, Red Hat | 2011 | GOT/PLT/TLS/版本脚本最权威实现指南 | sourceware.org/~drepper/how-to-write-shared-libraries.pdf |
| L16 | Virtual Memory | P. Denning, ACM Computing Surveys 2(3) | 1970 | "VM 作为缓存"理论起点 | doi.org/10.1145/234313.204347 |
| L16 | Working Sets Past and Present | Denning, ACM TOCS 5(1) | 1987 | 工作集模型：抖动分析的工具 | doi.org/10.1145/236543.243578 |
| L17 | Dynamic Memory Allocation: A Survey and Critical Review | Wilson, OOPSLA Workshop | 1993 | 分配器分类学总纲 | dl.acm.org/doi/10.1145/157719.157720 |
| L17 | Dynamic Memory Allocation Using Segregated Fit | Wilson, Johnstone, Neely, Boles, CU-CS-664-93 / SIGMETRICS | 1993 | sg_malloc 论文，Malloc Lab 直接依据 | 检索 "sg_malloc segregated fit" |
| L17 | A New, General Purpose, Dynamic Memory Allocation Package | Magaziner (与 Antol), USENIX Summer 1994 | 1994 | Windows NT 堆分配器诞生记，工程史经典 | usenix.org/summaries-1994 |
| L19 | A Protocol for Packet Network Intercommunication | Cerf & Kahn, IEEE Trans. COM 22(5) | 1974 | TCP/IP 原始论文 | ieeexplore.ieee.org/document/1451868 |
| L19 | RFC 791: Internet Protocol / RFC 793: Transmission Control Protocol | Postel 等, IETF | 1981 | IP/TCP 规范原文 | rfc-editor.org/rfc/rfc791, /rfc793 |
| L19 | RFC 768: User Datagram Protocol | Postel, IETF | 1980 | UDP 规范 | rfc-editor.org/rfc/rfc768 |
| L19 | RFC 9112: HTTP/1.1 Message Syntax and Routing | IETF | 2022 | Proxy Lab 协议依据（原 2616 拆分后继） | rfc-editor.org/rfc/rfc9112 |
| L20 | Cooperating Sequential Processes | Dijkstra, EWD123 | 1965 | 信号量原始文献 | cs.utexas.edu/users/mis/.../EWD123.pdf（检索 EWD123） |
| L20 | Why Threads Are a Bad Idea (for most purposes) | Ousterhout, USENIX Summer | 1995 | 事件驱动 vs 线程的永恒辩题 | usenix.org/conference/.../ousterhout |
| L20 | Implementing Remote Procedure Calls | Birrell & Nelson, ACM TOCS 2(1) | 1984 | RPC/消息传递：并发的另一条路（6.824 源头） | doi.org/10.1145/236543.243574 |

## 二、近五年（2020 起）论文 / 标准 / 工程文章

| 主题(讲) | 文献 | 出处 | 年份 | 看点 |
| --- | --- | --- | --- | --- |
| 分配器仿真(L17) | Simulation of High-Performance Memory Allocators: A Modular Framework and Benchmark (jemalloc/SGIMalloc/mimalloc) | arXiv:2406.15776 | 2024 | 现代分配器的统一评测框架 |
| 分配器(L17) | Mimalloc: Free List Sharding in Action | Leijen, MSR-TR-2019-29 | 2019(背景) | mimalloc 设计文档，与上条对照读 |
| 分配器(L17) | Exgen-Malloc: Optimizing Single-threaded Applications with Exgen-Malloc | arXiv:2510.10219 | 2025 | 面向单线程场景的新分配器研究 |
| 网络(L19) | RFC 9000: QUIC: A UDP-Based Multiplexed and Secure Transport | IETF | 2021 | "可靠字节流"的现代重定义，HTTP/3 之底 |
| 网络(L19) | RFC 9114: HTTP/3 | IETF | 2022 | 应用层协议如何摆脱 TCP 队头阻塞 |
| I/O(L18) | io_uring design guide（内核官方文档） | docs.kernel.org (Documentation/io_uring/io_uring-design-guide) | 2020 起持续 | 批量提交/完成队列如何消灭系统调用开销 |
| I/O(L18) | Efficient IO with io_uring (LSFMM 演讲材料) | Axboe, lsfmm.org | 2019+ | 作者自述设计动机（演讲 PDF） |
| 缓存(L10) | TinyLFU: A Highly Efficient Cache Admission Policy | Einziger, Friedman, Manes, ACM TOS | 2017(背景) | LFU 复兴：Redis/Alluxio 缓存策略来源 |
| 安全(L7) | Stack Clash: the "right" kind of wrong | Qualys advisories | 2017(背景) | 堆栈碰撞攻击：对齐/guard page 的反面教材 |
| 并发(L20) | eBPF 与内核旁路（kernel.org/bpf docs + Cilium 材料） | docs.kernel.org/bpf | 2020+ | "事件驱动+共享内存"在内核侧的当代形态 |
| 编译(L9) | LLVM New Pass Manager / PassBuilder 官方文档（licm/unroll/vectorize） | LLVM docs | 持续 | -O2/-O3 流水线各 pass 对应 L9/L11 技术 |

## 三、知识点 ↔ 开源项目映射

| CSAPP 知识点(讲) | 代表项目 | 代码/资料入口 |
| --- | --- | --- |
| 位级整数/溢出 (L2) | Linux 内核 `check_*_overflow` (include/linux/overflow.h) | torvalds/linux |
| 浮点 (L3) | NumPy/PyTorch 半精度、LLVM fast-math flag | numpy / llvm/llvm-project |
| 汇编与 ABI (L4–L7) | Linux `arch/x86/entry/entry_64.S`、System V ABI 文档 | torvalds/linux |
| 处理器/流水线 (L8) | gem5、RISC-V Spike、PicoRV32、香山 | gem5.org / riscv-software-src |
| 循环优化 (L9/L11) | LLVM (licm/unroll/vectorize passes)、xsimd/highway | llvm.org / google/highway |
| 缓存/局部性 (L10) | cachegrind(valgrind)、OpenBLAS GEMM 分块、perf | valgrind.org / xianyi/OpenBLAS |
| 链接/符号解析 (L12) | GNU binutils ld、LLVM lld、内核链接脚本 | sourceware.org / llvm lld |
| 共享库/装载 (L13) | glibc `elf/dl-*.c`(ld-linux)、musl | sourceware.org/glibc |
| 进程/系统调用 (L14) | Linux `kernel/fork.c`、`kernel/exit.c` | torvalds/linux |
| 信号/ECF (L15) | Nginx `src/core/ngx_cycle.c`、Redis 自签信号、systemd | nginx/nginx, redis/redis |
| 虚拟内存 (L16) | Linux `mm/`(mmap.c/page_alloc)、xv6 vm.c | torvalds/linux, MIT-PDOS/xv6-riscv |
| 分配器 (L17) | glibc ptmalloc、jemalloc、tcmalloc、mimalloc | jemalloc / google/tcmalloc / microsoft/mimalloc |
| 系统 I/O (L18) | libuv(跨平台 fd 抽象)、curl `lib/transfer.c` | libuv/libuv, curl/curl |
| 网络 sockets (L19) | Nginx `ngx_event*.c`、HAProxy、libevent | haproxy.org / libevent/libevent |
| 线程/同步 (L20) | glibc NPTL、xv6 锁实现、15-445 LockManager、Go runtime sched | mit-pdos/xv6-riscv, cmu-db |

## 四、使用说明

- 经典表以"读原著 + 对回 CSAPP 小节"为原则；近五年表用于把 1980s 的
  API 语义映射到 2020s 的工程现场（如 read/write → io_uring 批处理）。
- 建议配读顺序：L3↔Goldberg；L10↔Drepper 内存长文；L12/13↔Drepper 共享库+《自我修养》；
  L17↔Magaziner + sg_malloc + mimalloc TR；L20↔Ousterhout + EWD123。
