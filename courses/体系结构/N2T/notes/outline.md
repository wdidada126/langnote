# Nand2Tetris 讲义骨架（notes/outline.md）

> 每讲 3–5 条要点，骨架级。Part I = 硬件线（Ch.1–6），Part II = 软件线（Ch.7–12）。

## L1 布尔逻辑与 HDL（Ch.1）
- 只用 Nand 一种门可表达全部布尔函数（功能完备性）。
- 课程自研 HDL：以芯片为单位，输入/输出位、内部连线、Part 组合。
- 由 Nand 造 Not/And/Or/Xor/Mux，建立「门层级」抽象。
- Project 1：实现基本门与多路复用器族。

## L2 组合逻辑（Ch.2）
- 组合电路无状态：输出只由当前输入决定。
- 半加→全加→16 位加法器；有符号补码加法。
- ALU：由选择位控制运算，输出 z/n 标志。
- Project 2：Inc、Add、ALU。

## L3 时序逻辑与内存（Ch.3）
- 引入时钟与时序：Latch→D-Flip-Flop→Register。
- 程序计数器 PC（带 load/reset/increment 控制）。
- 寄存器组 RAM 与 ROM（数组式存储，地址译码）。
- Project 3：PC、RAM16K、ROM 等。

## L4 机器语言（Ch.4）
- Hack 机 16 位指令：C-指令（a=0）与 A-指令（a=1）。
- 目的寄存器、计算表 comp、跳转 dest/j 字段编码。
- 用机器码写第一个程序（求和、最大公约数）。
- Project 4：手写机器码填充 ROM 并运行。

## L5 计算机体系结构（Ch.5）
- 把 CPU 组件接成整机：指令寄存器 IR、ALU、寄存器组、PC、地址多路。
- 取指-译码-执行的指令周期。
- 内存映射 I/O：SCREEN、KEYBOARD、RAM 共用地址空间。
- Project 5：组装完整 CPU（有屏/键盘）。

## L6 汇编器（Ch.6）
- 两段式：先收集符号（变量/label），再翻译指令。
- A-指令符号解析、C-指令查表编码。
- .hack/.asm 输出与符号表。
- Project 6：Hack 汇编器（Python/C++/Java 任选）。

## L7 虚拟机 I（Ch.7）
- Jack VM：栈范式，`push/pop/add/sub` 等 15 条命令。
- 参数/局部变量经 RAM[0]/SP/LCL 指针管理。
- 算术、比较、访问函数命令翻译为 Hack 汇编。
- Project 7：翻译算术与内存访问命令。

## L8 虚拟机 II（Ch.8）
- 程序控制：if-goto/goto 翻译成跳转指令。
- 函数调用：call 压栈建立新栈帧，return 恢复调用者。
- caller/callee 帧协议与参数、返回值传递。
- Project 8：翻译控制流与函数调用。

## L9 高级语言导论（Ch.9）
- Jack 语言：类、方法/函数/构造器、字段与静态变量、基本类型与数组。
- 语法 vs 语义；到 VM 指令的映射策略。
- 标准库：String、Array、Math、Sys。
- 为编译做准备：不写代码，理解语言规范。

## L10 编译器（Ch.10）
- 编译前后端：词法/语法分析→符号表→代码生成。
- 表达式编译（优先级递归下降）与语句编译。
- 子程序调用、字段/静态变量映射到 RAM。
- Project 10：完整 Jack 编译器。

## L11 操作系统（Ch.11）
- OS 提供内存、图形、键盘、时钟、数学服务 API。
- 内存分配（heap 段 free/alloc）与字符串对象管理。
- 图形输出双缓冲、键盘输入轮询、线程与等待。
- Project 11：编写 Jack OS（内存、屏幕、键盘、数学）。

## L12 终局与全栈回顾（Ch.12）
- Jack 游戏 → Jack 编译器 → VM → 汇编器 → 机器码 → 硬件 CPU → OS 交互。
- 抽象层与接口契约如何隔离复杂度（课程核心思想）。
- 与现代真实栈（C→LLVM→x86/RISC-V→OS）的对应关系。
- 完成俄罗斯方块上机运行，形成完整计算机系统心智模型。
