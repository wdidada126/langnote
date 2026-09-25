# MIT 6.1810 / 6.S081 论文与阅读清单

> 与 notes/L01–L22 配套的论文表。凡本笔记未能从一手来源确认的题名/作者/年份，一律标"待核实"，
> 以当期官网 papers 页（pdos.csail.mit.edu/6.1810）为准。

## 1. 经典论文 / 专著表

| # | 文献 | 出处 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- | --- |
| 1 | Ritchie & Thompson, *The UNIX Time-Sharing System* | CACM 1974（1978 修订版） | L01/L02/L13 | 文件+进程两抽象的原点；fork/exec/wait、管道的设计现场 |
| 2 | Bach, *The Design of the UNIX Operating System* | Prentice Hall 1986 | L03–L07/L10–L11 | System V 内核逐层解剖教材：inode/缓冲/swap 的"前 xv6 时代"标准叙述 |
| 3 | Leffler et al., *An Advanced 4.3BSD Interprocess Communication Software Suite* 等（含 4.4BSD Lite 手册节选） | USENIX 1989/1993 | L20/L21 | socket API 与协议栈分层冻结为今日 POSIX 形状 |
| 4 | Popek & Goldberg, *Formal Requirements for Virtualizable Third Generation Architectures* | CACM 1974 | L16 | 可虚拟化判定：敏感指令 ⊆ 可陷入指令；x86 当年不满足的根因 |
| 5 | Denning, *Virtual Machines* | ACM Computing Surveys 1970 | L10 | 工作集/抖动理论，把"换页"从技巧变成学问 |
| 6 | Seltzer et al., *Software-Updated / Soft Updates*（题名与作者待核实，常见引作为 Soft Updates: Delayed Block Updates） | USENIX ATC 1993 | L07/L14 | 不写日志、靠依赖图延迟写也保崩溃一致的另类路线 |
| 7 | Mohan et al., *ARIES: A Transaction Recovery Method* | ACM TODS 1992 | L07/L09 | undo/redo + WAL + checkpoint 的完整形态，数据库侧标准 |
| 8 | Rosenblum & Ousterhout, *The Design and Implementation of a Log-Structured File System* | SOSP 1991 / ACM TOCS 1992 | L09/L14 | 一切皆顺序写 + 段清理：LSM 树与 F2FS 的祖父 |
| 9 | Engler & Kaashoek, *Exokernel: An Operating System Architecture for Application-Level Resource Management* | SOSP 1995 | L17 | 保护而非抽象；安全复用协议；libOS 思想源头 |
| 10 | Liedtke, *Improving IPC by Kernel Design* | CACM 1993 | L20 | 同步 IPC + 寄存器传小消息：快 IPC 的第一次系统论证 |
| 11 | Liedtke, *On μ-Kernel Structure*（及被常引为 "Splendid Isolation" 的相关讨论，具体篇目待核实） | SOSP 1993 | L17/L20 | 微内核必须小到能"隔离地思考"；maxims 写作法 |
| 12 | Accetta et al., *Mach: A New Kernel Foundation for UNIX Development* | USENIX 1986 | L20 | 端口/权利/虚拟内存对象：IPC 即一切的激进化与其性能教训 |
| 13 | Chew & Ma et al., *Message Processing in Modular Operating Systems*（作者全名单待核实） | SOSP 1999 | L20 | Mach IPC 成本微基准：cache/TLB 扰动才是大头 |
| 14 | McKenney, *Read-Copy Update*（US 专利 6,377,984, 2002）与 McKenney & Appavoo 等 *Read-Copy Update* 系列；McKenney, *What is RCU, Fundamentally?* | ACM Queue 2012 | L15 | 宽限期 + per-CPU 静默状态：读端零开销的数学与工程 |
| 15 | M. Michael, *Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects* | ASPLOS 2004 / IEEE TPDS 2004 | L15 | 读者显式声明"在看"，换 O(1) 安全回收 |
| 16 | Fraser, *Practical Lock-Freedom* | Cambridge Tech Report 2004（非会议论文，待核实） | L15 | 无锁数据结构与 EPAM 回收实操手册 |
| 17 | Eide et al., *FSCQ: A Synthesizable Specification for a File System*（作者/题名细节待核实） | OSDI 2013 | L09 | 把崩溃一致性写成可证明的规约：日志协议的定理化 |
| 18 | Jeitner et al., *Delegating Consistency to Hardware*（题名/出处待核实） | HotOS 2023 | L09/L14 | 让存储硬件提供顺序，文件系统协议因此可删 |
| 19 | Shapiro & Bernstein, *Designing a File System for the Non-Volatile Era* | HotOS 2021 / ACM TOCS 2023 | L09/L14 | 字节寻址非易失内存下，日志与拷贝是否都该消失 |
| 20 | Barham et al., *Xen and the Art of Virtualization* | SOSP 2003 | L16 | 半虚拟化（PV）路线宣言：改 guest 换性能 |
| 21 | Moritz & Zeldovich, *Dune: Safe User-level Access to the Memory Management Unit* | OSDI 2008 | L16/L18 | 给单个进程发 hypervisor：硬件隔离当沙箱 |
| 22 | Zhang et al., *DAGT: Effective Memory Management Across Heterogeneous CPUs*（作者待核实） | ISCA 2022（6.1810 2023 年起列入） | L19 | 页分配位置 = 异构 CPU 性能旋钮：分配器仍是活跃前沿 |
| 23 | Saltzer & Schroeder, *The Protection of Information in Computer Systems* | IEEE 1975 | L03/L17 | 最小特权/开放设计/经济性——全部安全讲次的宪法 |
| 24 | Marsh & Scott, *Crash-Only Software* | HotOS 2007 | L07/L09 | 恢复路径必须与崩溃路径同构，否则不可信 |
| 25 | Arpaci-Dusseau 夫妇, *Operating Systems: Three Easy Pieces*（OSTEP） | 免费在线书 | 全课 | 并发/虚拟化/持久化三分法，与本笔记结构互校 |

> 教材本体：*xv6: a simple, Unix-like teaching operating system*（book-rev2，RISC-V），
> Morris & Kaashoek 等；它不是论文，但每讲的"阅读材料"几乎都指向它。

## 2. 近五年（2021–2026）相关文献表

| 文献 | 出处/年份 | 关联讲次 | 备注 |
| --- | --- | --- | --- |
| Anglin & Sanchez, *Ink: Precise Version Ordering...*（精确题目待核实） | OSDI 2020 | L07/L14/L22 | 批量版本序降 fence/元数据开销 |
| Anglin & Sanchez, *Soil: Updating Sealed-Bid...*（精确题目待核实，主题=内存加密/唯一性） | SOSP 2021 | L22 | 唯一明文代替唯一密文，省新鲜度元数据 |
| *DRAM-SEC: In-DRAM Memory Integrity via SECDED...*（题目待核实） | ASPLOS 2021 | L22 | 用 ECC 冗余位承载截断 MAC |
| *Tail Fences: A simple and efficient whole-system defense against ROP/COP/JOP*（作者待核实） | SOSP 2021 | L18 | 内核返回路径加"看门返回"，不改编译器 |
| *Pebble: A Fully-Subjective Operating System*（题目待核实） | SOSP 2023 | L17/L22 | 直接执行路线的现代复兴 |
| *microOS: Intra-ms Latency and Throughput in the OS with a Microkernel-designed OS* | SOSP 2023（UIUC 组，作者待核实） | L17/L20 | 微内核+无锁分片做到 μs 级内核延迟 |
| *Lion: Block-level Versioning Abstraction for ML File Systems*（完整题名待核实） | SOSP 2023 | L07/L14 | ML 训练 I/O 模式倒逼 FS 版本语义 |
| *Tangram: Inter-Core Dependency Awareness...*（若与网络/核间调度相关，待核实） | OSDI 2024 | L21 | 多核数据面调度近年的代表作 |
| seL4 生态：*Formal verification of the seL4 microkernel* 后续工程文章（seL4 Foundation 技术博客/白皮书 2021–2024） | 非会议 | L16/L17 | 从"证明内核"到"证明系统"（CAmkES/数据流） |
| Unikernel/Serverless 线：*Catalyzer: Sub-millisecond Startup for Serverless Computing with Initialization-less Booting* | EuroSys 2021 | L10/L16 | 快照+CoW 恢复启动（与 L11/Firecracker 互读） |
| "红核"类国产内核/教学内核公开论文与报告 | —— | L17 | 具体所指与出处待核实：建议以官网当期 papers 与中文社区资料交叉确认 |
| io_uring/eBPF 在文件系统/网络的新测量与接口论文（如 FAST/ATC 近五年 fsync 与持久性测量系列） | 2021–2025 | L05/L14/L21 | 检索词："fsync", "crash consistency", "kernel bypass"；具体篇目待核实 |

## 3. 知识点 ↔ 开源项目映射表

| 知识点（讲次） | xv6 教学分支 | Linux | 教学/国产重写 | 其他工业项目 |
| --- | --- | --- | --- | --- |
| 锁与并发（L02） | `kernel/spinlock.c`、lab-lock | `kernel/spinlock.c`、locktorture | rCore/nCore 互斥量 | liburcu |
| sleep/wakeup 调度（L01/L02） | `proc.c: sleep/wake_up` | `wait_queue`、completion | rCore 阻塞队列 | FreeRTOS xQueue |
| 用户/内核地址空间（L03/L04） | `vm.c: walk/mappages` | `arch/riscv/mm`、swapper_pg_dir | rCore `MemorySet` | seL4 CNode/页表能力 |
| 系统调用（L05） | `syscall.c: syscallvec` | `sys_call_table`、vdso | nCore syscall | gVisor sentry |
| 文件系统：fd/inode/namei（L06） | `fs.c`、`bio.c` | VFS+ext4 | NJUOS tmpfs/fatfs | LittleFS（Zephyr） |
| 日志与崩溃一致性（L07/L09） | `log.c`、lab-fs | jbd2（ext4）、XFS log | —— | FSCQ/FizzBee、RocksDB WAL |
| 换页与缺页（L10） | xv6-mm 分支 `uvm.c` | `mm/vmscan.c`、page cache | rCore 换页实验 | zswap/zram |
| CoW fork（L11） | lab-cow | `do_wp_page`、userfaultfd | rCore CoW | Firecracker 快照 |
| virtio/块设备（L12） | `virtio_disk.c` | `drivers/virtio`、NVMe | rCore virtio-drivers | Cloud Hypervisor/Firecracker 设备栈 |
| 驱动复杂度/USB（L13） | （讲义）`usb.c` 片段 | `drivers/usb`、xhci | —— | tinyusb（设备侧） |
| 文件系统优化（L14） | lab-fs 性能测试 | ext4 fast commit、XFS、F2FS | —— | SPDK、Seastar |
| RCU（L15） | lab-thread（epoch 回收） | `kernel/rcu/tree.c` | —— | liburcu、Rust arc-swap |
| 虚拟化（L16） | lab-vm（RISC-V H 扩展） | KVM | NJUOS "Linux on 内核" 传统 | QEMU、Firecracker、Cloud Hypervisor |
| 隔离/微内核（L17） | （对照阅读） | namespaces/cgroups、eBPF | arceos/microOS 类 | seL4、Unikraft |
| 异常与攻击面（L18） | `trap.c` | KASLR/CFI/CET | —— | gVisor、浏览器沙箱 |
| 物理内存分配（L19） | `kalloc.c`、projects/alloc | buddy+slub | rCore buddy | jemalloc/mimalloc |
| IPC（L20） | `pipe.c`、socket | futex/io_uring | rCore pipe | seL4 CAmkES |
| 网络（L21） | `net.c`、lab-net | XDP/AF_XDP | —— | DPDK/VPP/F-Stack |
| 安全存储/直接执行（L22） | （论文课） | TDX/SEV-SNP、dm-integrity | —— | Kata Confidential Containers |

## 4. 使用说明

- 论文课讲次（L14–L22）的阅读材料以官网当期 papers 页为唯一权威；本表用于"知道去哪找 + 知道为什么读"。
- 标"待核实"的条目不影响概念理解，仅提示引用信息可能有出入，写论文综述/作业引用前请回查原始出处。
