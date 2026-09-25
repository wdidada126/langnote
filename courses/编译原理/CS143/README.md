# Stanford CS143: Compilers（编译原理）【CORE】

> 核心课程。本 README 为完整版（含全章节目录）；逐讲中文笔记见 `notes/`（L01-L19），论文清单见 `papers.md`，配套 C++ 实现见 `projects/`（MiniC 六阶段渐进编译器）。

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Stanford CS143: Compilers |
| 学校 | 斯坦福大学（Stanford University） |
| 主讲 | Alex Aiken（课程设计者） |
| 教材 | 龙书《编译原理》（Aho, Lam, Sethi, Ullman, *Compilers: Principles, Techniques, and Tools*, 2nd ed.） |
| csdiy 路径 | https://csdiy.wiki/编译原理/CS143/ （页面更新 2024-11-02） |
| 最新期次 | 公开授课 Fall 2018（课程网站含全部讲义/作业），课程语言 COOL |
| 状态 | ✅ 全量（2026-09）：README + 19 讲中文笔记 + papers.md + MiniC 六阶段配套项目 |
| 先修要求 | 计算机体系结构（建议先修 CS61C/CSAPP 一类课程） |
| 实现语言 | Java 或 C++ |
| 预计学时 | 约 150 小时（csdiy 难度 ★×5） |

## 课程定位

CS143 是经典"理论 + 完整编译器实现"课程：为面向对象的 COOL（Classroom-Object-Oriented-Language）语言实现一个编译器，编译到 MIPS 汇编并在 SPIM 模拟器上运行。理论覆盖词法分析、语法分析、语义分析、运行时环境、中间表示、寄存器分配、数据流分析与代码优化；实践分为词法、语法（AST）、语义检查、中间代码生成、后端代码生成五个递进的编程项目，优化部分留有大量自主设计空间。

## 为什么学

- 编译原理自学链条中的"学院派正统"：龙书作者之一亲自授课，理论与作业严格对应，是打牢前端/中端/后端完整知识框架的首选。
- 五个 Programming Projects 从零构建一个真实结构的编译器（含面向对象动态派发），完成后可与 NJU/USTC/SJTU 等国内课程互为印证。
- COOL 的 ClassTable、特征向量（feature table）与 dispatch 机制是理解"类型系统如何落到运行时"的极佳练习。
- 书面作业（5 个）覆盖龙书考研级知识点：LL(1)/LALR 构造、FIRST/FOLLOW、数据流框架、支配树、SSA——笔试能力与工程能力并重。

## 先修与知识联系

- **先修**：体系结构（MIPS 指令集、函数调用约定）、数据结构（树/图算法、哈希表）、Java 或 C++ 工程能力；建议先完成 CS61A（解释器）与 CSAPP。
- **后续/互练**：CS420/USTC/SJTU（现代 LLVM 风格中端与后端）、PKU-Compilers（SysY→RISC-V 实战）、CS242（类型理论侧写 COOL 的静态类型检查）。
- **知识映射**：COOL 语义分析 ↔ 龙书 ch5-6；ICG ↔ ch8；后端 ↔ ch9；寄存器分配 ↔ 图着色（Chaitin）；优化 ↔ ch10。

## 课程资源

- 课程网站：http://web.stanford.edu/class/cs143/
- 课程视频：Bilibili 搬运（BV17K4y147Bz）/ 原在线课程 Stanford Online (Fall 2018)
- 作业：5 个书面作业 + 5 个编程项目（PA1 Lexer / PA2 Parser+AST / PA3 Semantic Analyzer / PA4 Abstract Syntax Tree→COOL IR / PA5 Back End）
- 社区资源汇总：skyzluo/CS143-Compilers-Stanford（含笔记与参考实现）

## 讲义章节目录（最新公开期次，按课程网站 Schedule 与龙书整理）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | Introduction：编译器结构、翻译阶段总览 | 龙书 ch1 |
| L2 | COOL 语言与 Projects 总览 | 课程网站 Cool Manual |
| L3 | 词法分析 I：正则语言、有限自动词法器 | 龙书 ch2, ch3.1-3.6 |
| L4 | 词法分析 II：FA 实现与 lexer 生成器 | 龙书 ch3.7-3.9；Flex 文档 |
| L5 | 语法分析 I：上下文无关文法、推导与语法树 | 龙书 ch4.1-4.2 |
| L6 | 语法分析 II：Top-down 与 LL(1) | 龙书 ch4.3-4.4 |
| L7 | 语法分析 III：Bottom-up、LR/LALR 与冲突 | 龙书 ch4.5-4.7 |
| L8 | 语法分析 IV：解析器生成器（ yacc/bison） | 龙书 ch4.9 |
| L9 | 语义分析 I：语法制导翻译、属性文法 | 龙书 ch5.1-5.4 |
| L10 | 语义分析 II：类型检查、作用域与符号表 | 龙书 ch6.1-6.3, 6.5；ch5.6 |
| L11 | 运行时环境：激活记录、动态链、静态链、闭包 | 龙书 ch7.1-7.3, 7.10 |
| L12 | 中间表示：树、三地址码、DAG、SSA 引介 | 龙书 ch8.1-8.2 |
| L13 | 中间代码生成：表达式、控制流翻译 | 龙书 ch8.3-8.5 |
| L14 | 机器无关优化引论：数据流分析框架 | 龙书 ch9.1-9.2, 9.4 |
| L15 | 代码生成：目标机器模型、指令选择、调度 | 龙书 ch8 代码生成相关节；课程后端讲义 |
| L16 | 寄存器分配：活跃性、干涉图、图着色、合并 | 龙书 ch9.3, 9.6（另参 Chaitin 论文） |
| L17 | 高级优化：常量传播、归纳变量、循环优化、过程间分析 | 龙书 ch10.1-10.6 |
| L18 | 面向对象编译专题：dynamic dispatch、feature table、继承与多态的实现 | Cool Manual + 讲义 |
| L19 | GC 与运行时支持、课程总结 | 龙书 ch7.5（另参 Boehm 相关讲义） |

> 书面作业对应：HW1（词法/正则）、HW2（LL/LR 构造）、HW3（SDT/类型系统）、HW4（运行时/IR 翻译）、HW5（数据流/寄存器分配/优化）。

## 目录结构与学习路径

- `notes/L01..L19-*.md`：逐讲中文笔记（核心概念 + 算法伪码/例题 + 前后讲联系 + 跨课程联系 + 开源应用 + 延伸阅读）。
- `papers.md`：经典论文（按讲次）＋ 近五年条目（存疑处标"待核实"）＋ 知识点↔开源项目映射表。
- `projects/`：语言 C++17（仅标准库，本轮只写不编译）。
  `common/`（随阶段增长的编译器核心头）+ `01_lexer`～`06_optimizer` 六个独立可构建阶段 + `samples/`；
  每阶段自带 README 与 `build.sh`(g++) / `build.bat`(cl)。
  总表与 MiniC 语言规格见 `projects/README.md`。

建议顺序：读 L03-L04 → 做 projects/01；L05-L08 → 02；L09-L10 → 03；L11 → （配合 05 阅读）；
L12-L13 → 04；L15 → 05；L14+L17 → 06；L18-L19 为专题阅读（无对应代码，附伪码）。

## 状态与约定

- 状态：全量（2026-09）。笔记讲义以本 README 的 19 讲目录为准（对应 Fall 2018 公开期次 syllabus 与龙书章节）。
- 笔记语言：中文；项目代码本轮只写不编译（与全仓库约定一致），集中编译由用户自行执行。
