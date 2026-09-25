# MIT 6.1810 (原 6.S081): Operating System Engineering（【CORE】）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Operating System Engineering（2022 秋起编号由 6.S081 变更为 6.1810，内容不变） |
| 所属学校 | 麻省理工学院（MIT PDOS 实验室） |
| 主讲 | Robert Morris、Frans Kaashoek（教材与 xv6 作者） |
| 教材 | 《xv6: a simple, Unix-like teaching operating system》(xv6-riscv, book rev2)，配合 OSTEP 作为理论补充 |
| csdiy 路径 | /操作系统/MIT6.S081/ |
| 最新期次 | 每年秋季开设，最新为 pdos.csail.mit.edu/6.1810/（csdiy 中文对照对应 2021 秋 schedule） |
| 先修要求 | 体系结构 + 扎实 C 语言 + RISC-V 汇编；语言 C/RISC-V；难度 🌟🌟🌟🌟🌟；预计学时 150 小时 |
| 状态 | 全量（2026-09）：notes/L01–L22 逐讲笔记 + papers.md 论文清单 + projects/ 六个 C 语言模拟项目 |

## 为什么学

- 公认最好的本科 OS 实践课：直接对着 xv6（MIT 教授专为教学重写、继承 JOS 衣钵的 RISC-V Unix）源码逐行理解内核机制。
- 11 个周更 Lab 全部带完善测试框架（部分测试超千行），从实现 shell、页表、系统调用到写日志文件系统与 CoW fork，全程在真内核里改代码。
- 后半程精读文件系统、安全、网络、虚拟化方向的领域经典论文，本科阶段即可触及学界前沿。
- RISC-V 干净现代，不必纠结 x86 历史包袱，可将精力集中于操作系统本身；学完对 CSAPP Ch.8/9/10 的理解产生质变。

## 先修与知识联系

| 方向 | 关联课程/知识 |
| --- | --- |
| 先修 | CSAPP（尤其第 3/8/9/10/12 章）、DDCA/CS61C（RISC-V/流水线背景） |
| 平级互补 | CS162/NJUOS/HITOS（理论框架与工业视角）、OSTEP 教材 |
| 后续 | 6.824（分布式）、15445（存储引擎复用日志/并发思想）、6.858（安全论文线） |
| 直接复用 | lab-log 的写前日志 → 数据库 WAL；RCU 论文 → Linux 内核与 15445 并发控制 |

## 讲义全章节目录（对应 notes/L01–L22；以 6.1810 最新一届 lecture list 组织）

| 讲次 | 标题 | 阅读材料 | 笔记 |
| --- | --- | --- | --- |
| L01 | 课程导论（Introduction：OS 抽象与 xv6 总览） | xv6 教材 Ch.1–2；课程 FAQ | [L01](notes/L01.md) |
| L02 | 锁与并发（Locking / Synchronization） | xv6 book Ch.8；locking 讲义 | [L02](notes/L02.md) |
| L03 | 隔离与地址空间（Space） | xv6 book Ch.3–4；附录 A/B | [L03](notes/L03.md) |
| L04 | 虚拟地址机制（va：页表 / TLB / malloc） | xv6 book Ch.6–7；RISC-V priv spec §3 | [L04](notes/L04.md) |
| L05 | 系统调用（System Calls：trap 机制） | xv6 book Ch.5；syscall.c、trap.c | [L05](notes/L05.md) |
| L06 | 文件系统（File System：fd/inode/namei） | xv6 book Ch.9；fs.c、bio.c | [L06](notes/L06.md) |
| L07 | 日志与崩溃一致性（Log） | xv6 log.c；Mohan ARIES 选读 | [L07](notes/L07.md) |
| L08 | 文件系统扩展（fs+：加功能与换设计） | lab-fs 材料；软更新/extent | [L08](notes/L08.md) |
| L09 | 日志式文件系统深化（Journal） | Shapiro & Bernstein(Non-Volatile Era)；FSCQ | [L09](notes/L09.md) |
| L10 | 虚拟内存 I：换页与缺页（vm1） | xv6 book Ch.6；Denning Virtual Memory | [L10](notes/L10.md) |
| L11 | 虚拟内存 II：写时复制 fork（vm2） | xv6 uvm.c；lab-cow；Ritchie & Thompson | [L11](notes/L11.md) |
| L12 | 磁盘与设备驱动（Disk Drivers / virtio） | xv6 virtio_disk.c、plic.c、uart.c | [L12](notes/L12.md) |
| L13 | USB 驱动（USB） | xv6 usb.c；USB 规范概览 | [L13](notes/L13.md) |
| L14 | 文件系统性能优化（Optimizing File Systems） | LFS 论文；fssched；flash 主题 | [L14](notes/L14.md) |
| L15 | RCU 与无锁读（RCU） | McKenney "What is RCU, Fundamentally?";lab-thread | [L15](notes/L15.md) |
| L16 | 虚拟化（Virtualization） | Xen/KVM 材料；RISC-V H 扩展 | [L16](notes/L16.md) |
| L17 | 隔离与内核最小化（Separation） | Engler Exokernel；seL4；Liedtke | [L17](notes/L17.md) |
| L18 | 异常即攻击面（Exceptions & Software Attacks） | tail fences；ROP/CWE；Dune | [L18](notes/L18.md) |
| L19 | 物理内存分配（Physical Memory Allocation） | buddy/slab；DAGT(Heterogeneous CPUs) | [L19](notes/L19.md) |
| L20 | IPC 与消息传递（Inter-Process Communication） | xv6 pipe.c；Liedtke；Mach 消息论文 | [L20](notes/L20.md) |
| L21 | 快速网络栈（Fast Network / kernel bypass） | xv6 net.c；DPDK/AF_XDP 材料 | [L21](notes/L21.md) |
| L22 | 直接执行与唯一加密存储（Direct Execution & Unique，合并） | Ink/Soil/DRAM-SEC/Pebble | [L22](notes/L22.md) |

> 配套论文表见 [papers.md](papers.md)；动手项目见 [projects/README.md](projects/README.md)。
> Lab 共 11 个：util（Unix 工具）、riscv（调试器）、shell（系统调用/管道）、pgtbl/mmap（页表）、traps（用户级中断/性能计数）、lock（多线程安全）、fs（日志重放简化 kv 存储）、cow（CoW fork）、net（virtio 网络）、vm（hypervisor）、thread（用户级线程库与 RCU 实验）。具体要求见当期官网 lab 页。

## 课程资源（摘自 csdiy）

- 课程网站：https://pdos.csail.mit.edu/6.828/2021/schedule.html（与中文视频文档对应）；最新 https://pdos.csail.mit.edu/6.1810/
- 课程视频：YouTube（每课链接见官网）；中文翻译文档 mit-public-courses-cn-translatio.gitbook.io
- 课程教材：https://pdos.csail.mit.edu/6.828/2021/xv6/book-riscv-rev2.pdf（中译 xv6-riscv-book-zh-cn）
- 资源汇总：KuangjuX lab 题解、xv6-rust 重实现
