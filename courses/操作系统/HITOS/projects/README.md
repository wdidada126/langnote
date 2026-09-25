# HITOS 配套项目计划（projects/README.md）

> 对齐官方 8 小实验 + 4 大实验（蓝桥云课/HIT 实验手册），本地化到可复现环境。本轮只列计划不写代码。
> 注意：Linux 0.11 需老工具链（bochs + 32 位 gcc），统一用 Docker 镜像 `hdw1998/hitos-os:0.11` 风格环境；小项目部分用现代 Linux 复现等价机制。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L2 引导与地址 | 汇编 (NASM) + C | bootloader：写 512 字节引导扇区打印字符串进保护模式；地址换算小工具 | `nasm -f bin boot.asm && qemu-system-i386 -drive format=raw,file=boot.bin`；换算器 `gcc -O2 addr.c` |
| L3 进程创建 | C | fork-tracer：观测 fork/CoW（页表共享）并用 /proc 验证 | `gcc -O2 -static`（0.11 实验版用 bochs 镜像内工具链） |
| L4 调度 | C | sched-sim：复现 0.11 goodness 调度 vs CFS/EEVDF 行为对比模拟器 | `gcc -O2`，`./sched_sim --traces traces/` 输出甘特图数据 |
| L5 切换与终止 | C + x86 汇编 | ctx-switch：手写 swap_context(a,b) 双切换演示；僵尸回收 demo | `gcc -Og -g -m32`（或 0.11 镜像内 `-m32`） |
| L6–L7 内存管理 | C | pgtable-walk：用户态自建两级页表模型 + 页面置换（FIFO/Clock/LRU）模拟器 | `gcc -O2`；0.11 大实验一：内核加 printk 观察物理内存分配 |
| L8 文件系统 | C | minix-lite：解析 0.11 镜像中 minix 超级块/inode/目录项并 ls | `gcc -O2`；bochs 挂载 0.11 根文件系统镜像读取 |
| L9 中断与系统调用 | C + 汇编 | mysyscall：现代 Linux 添加一个自定义 syscall（或 ptrace 观测 int 0x80 路径） | 内核模块：`make -C /lib/modules/$(uname -r)/build M=$PWD modules` |
| L10 I/O 与 tty | C | term-raw：cfmakeraw 复刻键盘→tty→read 链路，统计中断次数 | `gcc -O2`，`strace -c ./term_raw` |
| 大实验（综合） | C/asm (0.11) | 四大实验：内核编译启动、进程实验、内存实验、文件系统实验（按官方手册逐步） | Docker 内 `make all && bochs -f bochs.cfg` |
