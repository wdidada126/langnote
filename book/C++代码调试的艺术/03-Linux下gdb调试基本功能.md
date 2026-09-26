# 03 Linux系统gdb调试基本功能（对应原书第 3 章）

> 对应原书第 3 章「Linux系统gdb调试基本功能」（✅ 章名双源核实）。节级目录（⚠️ 据豆瓣阅读电子书页 TOC）：
> 3.1 Linux C/C++编程基本知识、3.2 gdb简介、3.3 调试执行、3.4 断点管理、3.5 程序执行、
> 3.6 查看当前函数参数、3.7 查看/修改变量的值、3.8 自动显示、3.9 显示源代码、3.10 查看内存、
> 3.11 查看寄存器、3.12 查看调用栈、3.13 线程管理、3.14 其他（观察点/捕获点等）。
> **本章是本目录实测密度最高的一章**：所有 🔧 命令均在 Windows 上的 GNU gdb (GDB) 17.1（MinGW 构建）
> 实测通过——gdb 命令面跨平台稳定，Linux 上除标注 Windows 差异外行为一致；差异处逐条 ⚠️ 说明。

## 核心概念速览（中英对照）

- **启动与附加** — `gdb prog` / `gdb -p PID` / `attach PID`：三种入场方式；attach 会冻结目标。
- **断点族** — `break`/`hbreak`/`watch`/`rwatch`/`awatch`/`tbreak`：软件/硬件/观察/临时四种断点。
- **执行控制** — `run`/`continue(c)`/`next(n)`/`step(s)`/`finish`/`until`/`skip`：粒度从语句到函数。
- **查看三件套** — `print(p)` 表达式求值、`display` 命中即显、`x` 裸内存检查（格式串 `x/3i $pc` 看指令）。
- **栈操作** — `bt`/`frame N`/`up`/`down`/`info args`/`info locals`：切帧改变表达式求值的上下文。
- **线程命令** — `info threads`/`thread N`/`thread apply all BT`/`set schedule-multiple`：gdb 的线程视角。
- **捕获点** — catchpoint：`catch throw`/`catch syscall` 等「事件断点」，Linux 独有 `catch syscall`。
- **gdb 脚本化** — `commands`/`define`/`-batch -x file.gdb`/Python API：gdb 区别于 IDE 的杀手锏。
- **观察点即硬件断点** — watchpoint 由 DR0–DR3 实现：4 个槽位、只能监视已解析地址的内存（10 章原理）。
- **`set debug`/`show`** — 自省命令族：`show conventions`、`set print pretty on` 等偏好开关。

## 动机：为什么 gdb 值得单独一整章（以及为什么本书 2026 年仍成立）

gdb 是「命令行调试器」的最大公约数：lldb 刻意仿它、IDA 的调试面板语义来自它、
IDE（CLion/VSCode）的底层后端在 Linux/MinGW 上就是它。操作面之外，gdb 提供三件 IDE 给不了的：

1. **可脚本化的现场**——`commands` 让断点命中后自动打印并继续（无暂停的「活探针」），批量回归时用 `-batch -x`；
2. **对机器状态的直达通道**——`x`/`p $rsp`/`disassemble /m`，在符号不可信时回到第一性现场；
3. **任何地方都能跑**——SSH 之后、容器里、gdbserver 另一端、core 文件上（第 7/8 章）。

## 机制与实测：一条主线走完本章全部小节

主线样本 🔧（仓库外 `D:\develops\tmp\cppsnippets_debug\wp.c`）：

```c
#include <stdio.h>
int main(void) {
    int arr[4] = {1, 2, 3, 4};
    int sum = 0;
    for (int i = 0; i < 4; i++) {
        sum += arr[i];
        printf("i=%d sum=%d\n", i, sum);
    }
    return 0;
}
```

🔧 `g++ -g -O0 -o wp.exe wp.c`，然后 `gdb -batch -x cmd1.gdb ./wp.exe`
（**已实测坑**：Git Bash 下 `-ex 'info breakpoints'` 的引号会被拆散导致 gdb 把位置参数当可执行文件，
统一用命令文件驱动；Linux bash 无此问题 ⚠️）。cmd1.gdb 节选与真实输出：

```text
🔧 start / watch sum / continue / continue / info breakpoints

Temporary breakpoint 1 at 0x14000144d: file wp.c, line 3.
Thread 1 hit Temporary breakpoint 1, main () at wp.c:3
3	    int arr[4] = {1, 2, 3, 4};
Hardware watchpoint 2: sum
Thread 1 hit Hardware watchpoint 2: sum
Old value = 32759        ← 未初始化栈内存的「垃圾值」也是现场信息
New value = 0
Thread 1 hit Hardware watchpoint 2: sum
Old value = 0
New value = 1
main () at wp.c:7
7	        printf("i=%d sum=%d\n", i, sum);
Num  Type         Disp Enb Address        What
2    hw watchpoint keep y                 sum
	breakpoint already hit 2 times
```

要点逐条对上小节：

- **3.3/3.5 调试执行**：`start` = 「main 入口临时软断点 + run」，避免 `break main` 在 ASLR 下的地址问题；
  `next/step/finish` 与 VS 的 F10/F11/Shift+F11 一一对应。
- **3.4 断点管理**：`info breakpoints` 表格里 `hw watchpoint` 字样直接暴露机制——gdb 替你占用了 DR 寄存器；
  `disable/enable/delete/clear`、`ignore N 5`（跳过 5 次命中）、条件断点 `b wp.c:7, i==3`。
- **3.6/3.7 参数与变量**：`p sum`、`p/x`（十六进制）、`p *arr@4`（数组段， gdb 私有语法）、
  `print elements` 控制截断；改值 `set var sum = 0`。C++ 对象：`p obj` 走 gdb 类型打印机
  （libstdc++ 的 pretty printer 由 `info pretty-printer` 列出——STL 调试的前置知识）。
- **3.8 自动显示**：`display sum` 之后每次停都自动打印，等价 VS 的 Watch 钉住。
- **3.9/3.10/3.11**：`list`、`x/16xb &arr`（16 字节裸看）、`x/3i $pc`（当前指令流）、
  `info registers`（**已实测差异**：Windows 构建的 gdb 17.1 不暴露 DR 寄存器值，`p $dr0` 返回 `void`；
  Linux 上经 `ptrace(PTRACE_PEEKUSER)` 可读 DR6/DR7——这是第 10 章两套 OS 调试 API 差异的直接可观测后果）。
- **3.12 调用栈**：见下面栈溢出实验。
- **3.13 线程管理**：见 04 章（本章实测的 `info threads` 输出也贴在 04）。

### 栈溢出实验（3.12 的硬核版）🔧 已实测

```c
int deep(int n) { return deep(n + 1) + n; }   /* 无终点递归 */
```

```text
Thread 1 received signal SIGSEGV, Segmentation fault.
0x00007ff77a7b1453 in deep (n=43340) at so.c:2
#0  deep (n=43340) at so.c:2
#1  deep (n=43339) at so.c:2
...
(gdb) info frame
Stack level 0, frame at 0x404020:
 rip = 0x7ff77a7b1453 in deep (so.c:2); saved rip = 0x7ff77a7b1458
 Saved registers: rbp at 0x404010, rip at 0x404018
```

机制注脚：栈底守卫页（Windows guard page / Linux `MAP_GROWSDOWN`+rlimit）被踩中 → 页错误 → SIGSEGV。
`n=43340` 就是「递归已经四万三千层」的量化现场；`bt` 能走通全靠 `-O0` 保留的 rbp 帧链——
第 9 章 Release 下这条链会断（frame pointer omitted）。实用开关：`set backtrace limit 20`（防四万帧刷屏）、
`bt full`、`frame 100` 跳帧。

### 异常与库层断点（3.14 其他/捕获点）🔧 已实测

```text
🔧 catch throw / run
Catchpoint 1 (throw)
Thread 1 hit Catchpoint 1 (exception thrown), 0x... in __cxa_throw ()
```

`catch throw` 让你停在「抛出点」而非「catch 点」——unwinding 之前的黄金现场。
**已实测坑**：紧随其后在 `c` 到「exception caught」停点打 `bt` 会报 `No stack`——
MinGW SEH 展开期间帧信息不可信，这是 Windows 上 gdb 的已知薄弱环节（Linux 上 Itanium ABI 的
`.eh_frame` 回溯正常 ⚠️ 平台差异）。对策：在 throw 停点直接 `bt`（上面实验即在 throw 处取栈）。
Linux 独有：`catch syscall read`、`catch fork`；`catch syscall`+`info functions^read` 组合是「谁读了我的 fd」类问题的正解。

## 权衡：gdb 的语法债务与替代位置

- gdb 命令面 40 年沉积：缩写歧义（已实测：`c` 在批量脚本语境可被解析为 help 缩写而报错，**显式写 `continue` 最稳**）、
  `print` 与 `x` 的格式系统彼此不兼容——学习曲线陡是真实成本；
- 但它**没有 UI 可骗你**：`disassemble /m`（源码/汇编交错，第 9 章主武器）与 `x` 的裸内存视角
  让「我以为程序是这样」当场对质；
- lldb 命令更现代（`p`/`frame variable` 与表达式系统统一），概念与 gdb 一一对应，本章所有实验在 lldb
  有直接翻译——**学机制不学咒语**的人可把 lldb 当本章的第二投影（⚠️ 原书未讲 lldb）。

## 相邻概念对比

| 命令 | gdb | lldb | VS 对应 |
| --- | --- | --- | --- |
| 条件断点 | `b file:line, cond` | `breakpoint mod -c cond` | 断点属性 Condition |
| 数据断点 | `watch var` | `watchpoint set var` | 数据断点(2.13 ⚠️) |
| 命中后动作 | `commands ... end` | `breakpoint command add` | Actions |
| 反汇编视图 | `disassemble /m` | `disassemble -m` | Disassembly 窗口 |
| 脚本化 | Python API | Python API | DTE/无 |
| 事后 core | `gdb exe core` | `lldb -c core` | 打开 .dmp |

## 最新演进与工业实践

- **GDB 现状**（sourceware.org/gdb 仓库）：17.x 系列（2025）主升级点是 **DWARF5 完整支持、index 加速、
  Python 3 强制、`maintenance` 族清理**；本机 17.1 实测 `start`/watch/threads 全部正常。
  sourceware/gdb 仓库即原书所讲 gdb 的同源延续。
- **lldb 对位**：llvm/llvm-project（lldb 子目录）命令面持续向「可脚本、可分离符号」演进；macOS/iOS 唯一选择。
- **rr (mozilla/rr)**：`rr record ./prog; rr replay` 后在 gdb/lldb 里获得**无限回退**（`continue -1`）；
  数据断点式「找谁写坏 sum」的问题从 watchpoint 的「4 槽位+慢」变成随便倒带重查。Linux-only（需 VM 支持），
  Windows 对位是 WinDbg TTD（第 11 章）。
- **pwndbg 生态**：GEF/pwndbg（github: pwndbg/pwndbg）给 gdb 补安全研究视角的 UI
  （堆块解析、寄存器侧栏）——「内存查看」小节在逆向语境的延伸。
- **发行版符号服务化**：debuginfod 后，`gdb /usr/bin/foo` 自动拉符号已是
  Fedora/Ubuntu 的默认体验——对应第 9 章符号剥离的工业答案。

## 互链

- 断点/观察点底层机制（INT3、DR 寄存器、ptrace）：[10-调试高级话题.md](10-调试高级话题.md)
- Release 下本章命令的失效面：[09-Release版调试.md](09-Release版调试.md)
- 线程命令的完整战场：[04-多线程死锁调试.md](04-多线程死锁调试.md)
- gdb 操作面的微软镜像：[02-VisualC++调试基本功能.md](02-VisualC++调试基本功能.md)
- 远程 gdb（gdbserver/RSP）：[07-远程调试.md](07-远程调试.md)
- core 文件即「静态的本章现场」：[08-转储文件调试分析.md](08-转储文件调试分析.md)
- DWARF/堆机理的另册纵深：[../高效CC++调试.md](../高效CC++调试.md)
- gdb Python  scripting 的自动化语境：[../C++编程惯用法.md](../C++编程惯用法.md)
- C++ 系列总索引：[../C++系列·总索引.md](../C++系列·总索引.md)
