# CS143 配套项目：MiniC —— 一个渐进式迷你编译器（C++17，仅标准库）

复刻 CS143 五个 Programming Projects（COOL 编译器）的教学结构，但把目标语言换成更小的
**MiniC**（C 语法子集，去掉 OO 部分；面向对象派发专题见 `notes/L18`，用伪码演示），
并把 COOL 的 "bison+flex" 路线换成"手写为主 + 讲次对照"。

## MiniC 语言规格（摘要）

```
program := { func }                     函数定义若干（无全局变量）
func    := type IDENT '(' [params] ')' block
type    := 'int' | 'bool'
block   := '{' { decl | stmt } '}'     块级作用域，允许遮蔽（不允许同层重名）
decl    := type IDENT [ '=' expr ] ';'
stmt    := block | 'if' '(' expr ')' stmt [ 'else' stmt ]
         | 'while' '(' expr ')' stmt | 'return' expr ';'
         | 'print' expr ';' | IDENT '=' expr ';' | callExpr ';'
expr    := ||(1) >(2:&&) >(3:比较) >(4:+-) >(5:* / %) > 前缀(! -) > 原子
原子    := NUM | true | false | IDENT | IDENT '(' args ')' | '(' expr ')'
注释    := // 行注释；/* 块注释（可嵌套，带计数器）
```
类型规则：算术 `int`、序关系 `int→bool`、`==/!=` 同型、`&&/||/!` `bool`、
`if/while` 条件 `bool`、print 接受 `int|bool`、函数必须 `return expr`
（漏写路径由检查器 warning + IRGen 隐式 `return 0`）。

## 讲次 → 阶段 → 知识点 总表

| 阶段目录 | 对应讲次（notes/） | 交付物 | 核心知识点 |
| --- | --- | --- | --- |
| `01_lexer/` | L3, L4 | 手写 DFA 词法器 | 最长匹配、前瞻/回退、关键字表、嵌套注释计数器、行列号 |
| `02_parser/` | L5, L6, L8 | 递归下降分析器 + AST 打印 | 优先级爬升（Pratt）、panic-mode 错误恢复、文法↔过程同构 |
| `03_semantic/` | L9, L10 | 符号表 + 静态类型检查 | 作用域栈、两遍法（签名/函数体）、类型规则表、哨兵类型防刷屏 |
| `04_ir/` | L12, L13 | AST → 三地址码（每函数一份） | 翻译模式、短路 &&/|| 的跳转模板、while 回填、槽位改名（name@k） |
| `05_backend/` | L11, L15 | 三地址虚拟机（解释执行） | 帧=激活记录、$aX 全局参数箱≈调用约定、Ret 弹栈；README 附 x86 风格输出示例 |
| `06_optimizer/` | L14, L17 | 常量折叠 / 复制传播 / DCE | 块内格（lattice）、SSA 单赋值收益、读集反向删除、优化顺序敏感 |

编译器核心在 `common/`（头文件形式，逐阶段增长）：
`lexer.h → ast.h → parser.h → checker.h`；各阶段目录内的 `*.h` 是该阶段**新增**的
教学代码（`icode.h / interp.h / opt.h`），`main.cpp` 为驱动。

## 构建与运行

所有阶段只需编译**本目录的 main.cpp**（其余经 `#include "../common/xxx.h"` 相对路径引入，
quoted include 以包含者文件所在目录解析，无需 -I 参数）。**请在各阶段目录内执行**：

```sh
cd 04_ir && ./build.sh && ./minic04 ../samples/hello.minic
```
```bat
cd 05_backend && build.bat && minic05.exe ..\samples\hello.minic
```
`build.sh` 用 g++（Linux/macOS/MSYS2/WSL），`build.bat` 用 MSVC cl
（需在"x64 Native Tools Command Prompt"下运行，VS2017+ 支持 /std:c++17）。
默认样例：不带参数时自动读 `../samples/hello.minic`。

## 样例
- `samples/hello.minic`：全功能冒烟（gcd/isEven/累加循环）。
- `samples/bad.minic`：故意错 6 处，验证 stage 03 的报错质量。
- `samples/dead.minic`：stage 06 的折叠/传播/死码实验台。

## 与 CS143 官方 PA 的对应
| 官方 PA | 本项目阶段 | 差异说明 |
| --- | --- | --- |
| PA1 Lexer（C++ 手写） | 01 | 一致（路线同为手写） |
| PA2 Parser（flex+bison 构 AST） | 02 | 我们手写递归下降；L7-L8 讲 LR/bison 作对照 |
| PA3 语义检查 | 03 | COOL 有子类型/lub；MiniC 只有 int/bool |
| PA4 AST→抽象汇编 | 04 | MiniC 出三地址而非 COOL 的带约束汇编树 |
| PA5 后端（MIPS+SPIM） | 05/06 | MiniC 用解释器代替真汇编，另附 x86 文本示例 |

## 约定
本轮只写不编译（与全仓库一致）；代码为 C++17、仅标准库、单编译单元可独立构建。
若你动手编译遇到问题，那正是"从读代码到写代码"的第一步。
