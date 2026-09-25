# CSAPP 配套项目汇总

语言：**C**（POSIX / Windows 可移植子集；本轮只写不编译，代码完整自洽）。
每个项目独立目录：源码 + README（关联讲次）+ `build.bat`（cl，需
`vcvarsall.bat x64` 环境）+ `build.sh`（gcc）或 `Makefile`。

## 讲次 → 项目 → 知识点

| 讲次 | 项目目录 | 语言 | 知识点 ↔ 内容 |
| --- | --- | --- | --- |
| L02–L03 (Ch.2) | `ch02-bits-float/` | C | 位运算、补码/溢出、IEEE 754：Data Lab 式位级函数 + 自检测试 |
| L04–L07 (Ch.3) | `ch03-asm/` | C | x86-64 操作数/控制流/栈帧/结构对齐：小函数集 + 预期汇编要点注释 + objdump/dumpbin 对照 |
| L08–L11 (Ch.4/5/6) | `ch04-05-perf/` | C | 存储层次与优化：行/列遍历、分块矩阵乘、步长冲突扫描 + 跨平台计时脚手架 |
| L12–L13 (Ch.7) | `ch07-linking/` | C | 链接：多目标文件、ar 静态库与顺序敏感性、强弱符号、-fPIC/.so 与 dlopen / LoadLibrary 双版 |
| L14–L15, L18 (Ch.8/10) | `ch08-09-ecf-io/` | C | 异常控制流与系统 I/O：mini-shell 骨架（fork/exec/wait/SIGCHLD/进程组）、健壮 cp、epoll 与 IOCP 设计说明 |
| L19–L20 (Ch.11/12) | `ch10-11-net-conc/` | C | 网络与并发：双平台 echo 服务器/客户端（线程版）、有界缓冲生产者-消费者（mutex+cond / SRWLOCK+CV） |

## 与官方 11 个 Lab 的对应关系

| 官方 Lab | 本仓库替代品 | 说明 |
| --- | --- | --- |
| Data Lab | `ch02-bits-float` | 同款位级约束与浮点位操作 |
| Bomb Lab | `ch03-asm` + L04–L06 笔记读图清单 | 正向写 C→预测汇编，等价于逆向训练 |
| Attack Lab | L06/L07 笔记 + papers.md Smashing the Stack | 攻击实验建议用官方框架（需真 x86-64 Linux） |
| Architecture Lab | L08 笔记 | HCL/Y86 需官方 SIM 工具链 |
| Cache Lab | `ch04-05-perf` | 用真实计时替代 trace 模拟，结论一致 |
| Shell Lab | `ch08-09-ecf-io/mini_shell` | 骨架 + README"未完成清单"即 Lab 要求 |
| Malloc Lab | L17 笔记 + papers.md 分配器材料 | 完整实现请上官方框架 |
| Proxy Lab | `ch10-11-net-conc` | HTTP 解析与 epoll/IOCP 路线见其 README |

## 通用构建说明

```sh
# 所有 build.sh 假定 gcc；Windows 两种等价方式：
# 1) "x64 Native Tools Command Prompt for VS 2022" 里直接跑 build.bat
# 2) cmd 中先: call "...\vcvarsall.bat" x64   再跑 build.bat
```

- 网络示例端口默认 8000，冲突时改参数；服务器需与客户端在同一平台族测试
  （Windows↔Linux 互通亦可，TCP 不挑 OS）。
- 本轮**只写不编译**；若集中编译发现问题，优先检查各 README 的"观察点"。
