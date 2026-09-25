# ASU CSE466 系统安全（Computer Systems Security）

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | Arizona State University CSE466 / CSE546: Computer Systems Security |
| 学校 | Arizona State University |
| 主讲 | Trevor Pounds 等（pwn.college 创始教研组） |
| 教材 | 无；pwn.college dojo 讲义 + Challenge 即教材 |
| csdiy 路径 | `系统安全/CSE466` |
| 最新期次 |  dojo 常驻：https://dojo.pwn.college/cse466/ （随学期滚动更新） |
| 状态 | 骨架 |

- 课程网站：https://dojo.pwn.college/cse466/
- 视频：YouTube @pwncollege；直播 Twitch @pwncollege；Discord 答疑
- 作业：13 个模块、共 358 个 challenges（CTF 形式，难度递增，内核模块最难）
- 注意：官方不鼓励上传题解（每模块前两题与逆向部分 16 题除外），笔记只写概念与方法论。

## 为什么学

- 系统安全的「肌肉课」：shellcode 注入、ROP、堆利用、内核提权全部要求亲手打穿，而非纸上谈兵。
- 逆向与二进制分析的沉浸式训练：函数帧、静态/动态工具链在关卡中自然上手。
- CSE365 的直接续作、6.858/工业漏洞研究的跳板：学完具备打 pwn 类 CTF 与读漏洞研究论文的完整能力。

## 先修与知识联系

- 先修：CSE365 或等价基础（Linux 命令行、汇编入门、Web 基础）；CSAPP 级别内存模型。
- 联系：与 6.858 的 L5–L7（利用与缓解）互为「讲义版/实战版」；内核模块与 Syzkaller/kAFL 生态直接对接；沙箱/竞态模块与 OS 课（6.S081/CS162）共享概念。

## 讲义章节目录（13 模块整理，按 dojo 页面滚动更新）

| 讲次 | 标题 | 阅读材料 |
|---|---|---|
| M1/L1 | Program Misuse（Linux 程序滥用进阶） | pwn.college 模块讲义 |
| L2 | Program Interaction（进程交互/IPC 滥用） | 同上 |
| M2/L3 | Shellcoding：shellcode 注入与执行 | 讲义 |
| L4 | Shellcode 防御（NX 前后语境） | 同上 |
| M3/L5 | 汇编与逆向基础：函数帧、栈布局 | 讲义 |
| L6 | 静态逆向工具（Ghidra/IDA 向） | 工具文档 |
| L7 | 动态逆向工具（gdb/pwndbg/strace 向） | 工具文档 |
| M4/L8 | 控制流劫持：ret2syscall/ret2lib | 讲义 |
| L9 | ROP 与栈迁移（pivoting） | 同上 |
| M5/L10 | 格式化字符串与内存错误（UAF/堆） | 讲义 |
| L11 | JIT/现代执行体攻击（JIT spray 等杂项） | 同上 |
| M6/L12 | 内核安全：内核模块与提权 | 讲义（Linux 内核文档） |
| L13 | System Exploitation 综合与竞态条件（race condition） | 讲义 |
| M7/L14 | Sandboxing 与课程综合（期末 CTF） | 讲义 |

> 注：官方以 13 模块组织（358 题），本表按知识域拆成 14 讲骨架，最终以 dojo 当期模块列表对齐。

## 作业与项目（概览）

全在线 challenge；本地配套见 `projects/README.md`（自建靶题 + 利用/防御双向工程）。
