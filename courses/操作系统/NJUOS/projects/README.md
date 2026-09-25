# NJUOS 配套项目计划（projects/README.md）

> 对齐官方 5 MiniLab + 4 OSLab 主线，本地化为可独立编译的小项目。本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L3–L4 二进制与链接 | C | mini-ld：解析 ELF 符号表，完成一次性静态链接；LD_PRELOAD 劫持计时器 | `gcc -O2 -no-pie`；ELF 解析用 `<elf.h>`，动态库实验 `-shared -fPIC -ldl` |
| L6 状态机与 shell | C | mshell：状态机驱动的 shell（管道/重定向/后台），即 MiniLab-1 风格 | `gcc -Wall -Wextra`，自带用例脚本 `make test` |
| L9 协程 | C | co-rtm：约百行有栈协程 + 调度器（swapcontext 与手写汇编两版） | `gcc -Og -g`；汇编版 `gcc -c co.S` 后链接 |
| L10–L12 调度与同步 | C | threadpool + 生产者消费者：MLFQ 模拟、死锁演示与 TSan 清零 | `gcc -O2 -pthread`；检测 `gcc -fsanitize=thread` |
| L13–L15 内存管理 | C | pager：用户态页表/TLB/缺页与 Clock 置换模拟器 | `gcc -O2`，`./pager --size 16 --frames 4 --trace t.txt` |
| L16–L17 存储与文件系统 | C | myfat：按微软 FAT 规范实现簇链读写 + 目录枚举（MiniLab-5 风格） | `gcc -O2`；镜像用 `dd`+自格式化脚本生成 |
| L19 OSLab 主线 | C + x86_64 汇编 | oskernel：四步走——boot(16→32→64位)/内存管理/进程调度/简易 FS，QEMU 启动 | `gcc -ffreestanding -nostdlib` + `ld -T link.ld`；运行 `qemu-system-x86_64 -kernel kernel.bin` 或 `make run` |
