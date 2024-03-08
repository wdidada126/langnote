# xv6

github.com/mit-pdos/xv6-public

### [【操作系统学习 01】MIT xv6操作系统环境配置及编译](https://blog.csdn.net/ALOmiya0/article/details/79673702)



[操作系统学习 02】xv6操作系统实现反向输出命令echo_reversal](https://blog.csdn.net/ALOmiya0/article/details/79675554)

xv6源码分析（一）：BootLoader

https://blog.csdn.net/qq_25426415/article/details/54583835

关注实验

`git clone git://github.com/mit-pdos/xv6-public.git`

xv6 borrows code from the following sources:
    JOS (asm.h, elf.h, mmu.h, bootasm.S, ide.c, console.c, and others)
    Plan 9 (entryother.S, mp.h, mp.c, lapic.c)
    FreeBSD (ioapic.c)
    NetBSD (console.c)


To build xv6 on an x86 ELF machine (like Linux or FreeBSD), run
"make"
Now install the QEMU PC
simulator and run "make qemu".


