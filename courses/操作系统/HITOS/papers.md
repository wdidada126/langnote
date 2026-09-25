# HITOS 论文与前沿清单（papers.md）

> 骨架级清单，正文由后续专人展开。关联讲次对应 notes/outline.md。

## 经典文献（本课以书与源码为主）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The UNIX Time-Sharing System (Ritchie & Thompson, CACM) | 1974 | Unix 抽象的原点，理解 0.11 设计动机的钥匙 | L3/L8/L10 |
| The Design and Implementation of the 4.3BSD UNIX Operating System (Rosenblum & Ousterhout) | 1992 | 同期内核设计全景参照，弥补 0.11 简化细节 | L6–L9 |
| The Design of the UNIX Operating System (Lions, Bach) | 1983/1986 | V6 逐行剖析范式，《Linux 内核完全注释》的榜样 | L1–L11 |
| Linux 0.11 源码本身（Linus Torvalds, 1991） | 1991 | 两万行读懂 OS 全机制的最小标本 | 全课程 |
| Exokernel (Engler & Kaashoek, SOSP) | 1995 | 与 0.11 式「小而全」形成设计光谱两端 | L11 |
| Virtual Memory (Denning, ACM Computing Surveys) | 1970 | 置换与工作集理论，为 L7 提供正式框架 | L7 |

## 近五年论文/动态（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Linux 6.x 调度器演进（EEVDF 替换 CFS 的内核文档与论文） | 2023–2024 | 公平调度最新形态，与 0.11 goodness 对照读 | L4 |
| io_uring 持续演进与内核安全边界讨论 | 2021–2024 | 系统调用接口 30 年最大变更 | L9 |
| Rust for Linux（内核内存安全新范式） | 2021–2024 | 从 C 源码课迈向现代内核开发的语言过渡 | L1–L2 |
| 侧信道与内核缓解（Spectre/Meltdown 后续缓解开销优化） | 2021–2023 | L9/L2 特权级机制的现实安全约束 | L2/L9 |
| 微型教学内核生态（xv6-riscv 更新、MizuKi 等） | 2021–2024 | 0.11 之后新一代教学内核选型参照 | L11 |

## 知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 说明 |
| --- | --- | --- |
| 引导与保护模式 | SeaBIOS、grub legacy 源码 | bootsect/setup 的现代对应物 |
| 进程与 fork | Linux kernel kernel/fork.c | 写时复制机制三十年演化对照 |
| 调度 | Linux EEVDF、FreeRTOS | 从 goodness 到生产调度器 |
| 内存管理 | Linux mm/、uCLinux | 页表/伙伴/置换的工程化 |
| 文件系统 | ext2（e2fsprogs）、minix fs | 0.11 FS 的直系后代 |
| 中断与 syscall | Linux arch/x86/entry、musl libc | int 0x80→syscall 快速路径 |
| 驱动与 tty | Linux tty 子系统 | 行规程概念至今未变 |
