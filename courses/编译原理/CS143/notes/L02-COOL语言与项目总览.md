# L2 COOL 语言与 Projects 总览

> 讲次：CS143 L2 ｜ 阅读：Cool Manual（课程网站）｜ 配套：projects/ 全链路以自研 MiniC 复刻 COOL 教学思想

## 核心概念

### COOL 语言速览
- Classroom Object-Oriented Language：面向教学的强类型面向对象语言，编译到 MIPS 汇编、SPIM 模拟器运行。
- 类型：Int、Bool、String、Object 及类类型；表达式均有静态类型。
- 特征表达式：`let x : T <- e in e`、`if e then e else e fi`、`while e loop e pool`、`isvoid e`、`e@C.f(e)`（静态派发覆盖）、`new T`、`dispatch` 动态绑定。
- 每个类隐式继承 Object；`type` 方法返回类型标签——运行时反射的最小内核。
- IO 约定：`out_string(String)`、`out_int(Int)`、`abort()`。

### 语法要点（Cool Manual）
- 标识符分大小写两类：小写开头是变量/方法，大写开头是类型（词法级区分！）。
- 字符串字面量不允许换行与制表符——词法器要专门检查，这是 PA1 的经典考点。
- `(* 注释 *)` 可嵌套——词法分析需要计数状态，纯正则仍然可表达（用自动机而非正则即可）。
- 文法有"悬挂 else"二义性，靠语法规约（shift 优先）解决。

### 五个 Programming Projects 的流水线
| PA | 阶段 | 产物 |
| --- | --- | --- |
| PA1 | 词法 | `abstract_module.cc` 中的 `string::tokenize()` |
| PA2 | 语法 | bison+flex 构建 AST（类层次化） |
| PA3 | 语义 | 符号表 + 类型检查 + 报错 |
| PA4 | ICG | AST → 抽象汇编树（COOL IR） |
| PA5 | 后端 | IR → MIPS：栈帧、特征表、动态派发、简单优化 |
书面作业 HW1-HW5 与 PA 对齐：正则/自动机、LL/LR、SDT/类型、运行时/IR、数据流/寄存器分配/优化。

### 本笔记项目的 MiniC 设计（映射 COOL）
- 保留：Int/Bool/String(仅字面量)、局部 let 风格声明、if/while、函数与形参类型标注、print（≈ out_*）。
- 简化：砍掉类与继承（OO 动态派发单独在 L18 笔记中用伪码演示，不进入 MiniC 实现）。
- 目标：五个阶段目录与本讲 PA 一一对应，最后接一个优化 pass。

## 与前后讲的联系
- 本讲定义"题目"，L3 起逐个阶段"答题"；PA 的提交顺序即讲次推进顺序。
- COOL 的每个语言决定几乎都对应龙书一节：type 标签↔运行时(L19)、静态链/闭包课程未用但龙书 ch7 有、`@C.f`↔L18 特征表。

## 跨课程联系
- **CS3110/CS242**：COOL 是"带子类型的名义类型系统"，与 OCaml 的结构类型、Java 的名义类型可做三方对比——静态语义决定符号表要存什么。
- **6.S081/CSAPP**：COOL 编译产物直接暴露 MIPS 调用约定，PA5 本质是"手写函数序言/尾声 + 手工栈管理"。
- **CS61C**：SPIM 上跑 COOL 程序 = 把 CS61C 的 ISA 知识变成编译器输出合同。

## 开源项目中的应用
- **rustc 教学版**：rust-analyzer / `min` 类玩具（如 "Writing a Compiler in Go" 系列）与 PA1-PA5 拆分同构。
- **RPython/RPython 系**：PyPy 的 "builder" 流程（词法→AST→rpython 流图→后端）是 COOL 流水线的工业放大版。
- **WASM 工具链**：若把 COOL 目标机从 MIPS 换成 wasm32，前端完全不动——体会"IR/目标机可替换"。

## 延伸阅读
- Cool Manual（Stanford 课程站）；skyzluo/CS143-Compilers-Stanford 仓库的讲义整理。
- 龙书 ch2.2（实现的组织结构）与附录 COOL 语法对照阅读。

## 自测问题
1. COOL 词法如何区分 `Foo` 与 `foo`？这对类型系统意味着什么（类型名也是标识符）？
2. `e@C.f(args)` 的 `@C` 改变了什么、没改变什么？（提示：静态类型 vs 运行时对象）
3. if 的分支类型不同时，结果类型是什么规则？该规则把活干在了哪个阶段？（答：语义层的 lub）
4. PA4 与 PA5 的分界线是什么？为什么课程要把"IR"与"MIPS"拆成两个 PA？
5. 本仓库 MiniC 为什么砍掉 OO？哪一讲笔记用伪码补上了这块？（答：L18）
6. `isvoid e` 与 `e = nothing` 为何不是一回事？void 在类型格中处于什么位置？
7. 五个 PA 中哪两个允许"错误信息质量"直接扣分？这对你的测试习惯意味着什么？
