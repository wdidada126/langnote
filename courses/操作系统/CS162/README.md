# UCB CS162: Operating Systems and Systems Programming 操作系统

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | CS162: Operating Systems and Systems Programming |
| 所属学校 | 加州大学伯克利分校（UC Berkeley） |
| 主讲 | Tiem Liu（Fa25 现任；课程长期由 Arpaci-Dusseau 团队讲授，OSTEP 作者本人） |
| 教材 | Operating Systems: Principles and Practice, 2nd（Arpaci-Dusseau 亦为 OSTEP 作者，课程论文补充） |
| csdiy 路径 | /操作系统/CS162/ |
| 最新期次 | Fall 2025（csdiy 收录 Fa25 WayBack 站点；公开视频 2020Fa/2021Fa/22Sp 三届，自学推荐 22Sp） |
| 先修要求 | CS61C + CS61B；语言 C/C++/Rust；难度 🌟🌟🌟🌟🌟；预计学时 150 小时 |
| 状态 | 骨架已建，正文待填充 |

## 为什么学

- 「原理 + 实践」双轨：课堂讲通用抽象（进程/内存/文件），Project 用 Pintos 从零把线程、调度、虚存、文件系统亲手做出来。
- Pintos 本身仅约一万行，4 个 Project 几乎无框架代码，2000 行级设计自由度和完整本地测试，是本科阶段最接近真实内核开发的项目（Stanford/Berkeley/JHU 共同采用）。
- 25 年版作业重做：3 Project（User Programs/Threads/File Systems）+ 6 Homework（List/Shell/HTTP/Memory/MapReduce/RPC 子任务），C 与 Rust 双版本，与 6.824 有直通设计。
- 后程论文课覆盖 SOSP/OSDI 经典，理论实践与科研视野三线并进。

## 先修与知识联系

| 方向 | 关联 |
| --- | --- |
| 先修 | CS61C（硬件抽象）、CS61B（数据结构）、CSAPP Ch.8–9 强烈有益 |
| 平级 | 6.S081（同主题不同风格：xv6 读改 vs Pintos 自建）、NJUOS/HITOS |
| 后续 | 6.824（MapReduce/RPC 作业直接对应）、15445（文件系统/日志复用）、CS168/CS144（网络部分） |
| 教材复用 | OSTEP 电子书；Arpaci-Dusseau 课程视频（cs162.io） |

## 最新年份讲义章节目录表（Fa25 排课骨架，22 讲，对应 OSPP 2nd 五大部分）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：什么是 OS、虚拟机视角 | OSPP Ch.1 |
| L2 | 内核体系结构：单核/微核、模块与中断 | OSPP Ch.3 |
| L3 | 线程与上下文切换（一）：内核线程/用户线程 | OSPP Ch.4；Pintos 代码导读 |
| L4 | 线程与上下文切换（二）：调度 | OSPP Ch.4；sched 论文节选 |
| L5 | 系统调用与用户态/内核态边界 | OSPP Ch.3；Pintos syscall 实现 |
| L6 | 同步 I：互斥与条件变量 | OSTEP Ch.28–30 |
| L7 | 同步 II：信号量、死锁与原子操作 | OSTEP Ch.28/31 |
| L8 | 内存布局与地址空间 | OSTEP Ch.13–14 |
| L9 | 虚拟内存 I：机制、页表与 TLB | OSTEP Ch.17–20 |
| L10 | 虚拟内存 II：置换与换页策略 | OSTEP Ch.21–22 |
| L11 | I/O 设备与中断处理 | OSTEP Ch.35–36 |
| L12 | 磁盘与 SSD | OSTEP Ch.37 |
| L13 | 文件系统 I：接口与目录 | OSTEP Ch.38–39 |
| L14 | 文件系统 II：实现与日志 | OSTEP Ch.40–41；Miller "Pintos for Instructors" 类比材料 |
| L15 | 文件系统 III：崩溃一致性与 fsck | OSTEP Ch.41；ARIES 节选 |
| L16 | 网络协议栈与 socket | OSTEP Ch.44；RFC 791/793 节选 |
| L17 | 分布式系统 I：RPC 与文件 | Tanenbaum 分布式章节/RPC 讲义 |
| L18 | 分布式系统 II：MapReduce 与容错 | Dean & Ghemawat 004 |
| L19 | 安全与隔离初阶 | Saltzer & Schroeder 保护定理 |
| L20 | 虚拟化与容器 | Popek & Goldberg；KVM 论文节选 |
| L21 | 论文研讨（一）：Exokernel/Splinter 等当期指定 | SOSP/OSDI 论文（每期更新） |
| L22 | 论文研讨（二）+ 期末复习 | 当期指定论文 + 全课程回顾 |

## 课程资源（摘自 csdiy）

- 课程网站：Fa25（WayBack 备份见 csdiy 链接）
- 课程视频：22Sp（自学首选）/ 20Fa / 21Fa
- 课程作业：3 Pintos Project + 6 Homework（C/Rust 双版本）
- 资源汇总：RisingUppercut/CS162-fall25（含框架代码与设计文档）
