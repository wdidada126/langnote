# PKU 编译原理实践 — 论文与延伸阅读骨架

> 本课程为实践课，无官方论文清单；下表为与课程各阶段对应的经典/前沿文献与开源应用，供填充笔记时引用。

## 经典论文

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Aho et al., *Compilers: Principles, Techniques, and Tools*（龙书） | 2006 | 各阶段理论总纲（配合 L3-L10） |
| Appel, *An Implementation of the Pop Stack Reference Machine* / Tiger 系列 | 1998 | 增量式编译器实现方法论参照 |
| Cytron et al., Efficiently Computing SSA | 1991 | Koopa IR 的 SSA 形式与支配树理论 |
| Chaitin et al., Register Allocation via Coloring | 1981 | L7/L10 寄存器分配思想的源头 |
| Preston Briggs et al., Practical Register Allocation (SSA 上) | 2003 | 现代 RA 路线，性能挑战方向 |
| Boehm, A Garbage Collector for C and C++ (libgc) | 1988/2011 | 若做运行时库/内存管理扩展时的参考 |
| Kerrison & Eker, JIT compilation techniques survey | 2015 | 对比：静态编译器 vs JIT，理解本课程取舍 |

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| CompCert / KKWM 后端验证后续（C--{} 相关） | POPL/PLDI 2021-2024 | 后端翻译正确性验证，对照"输出汇编正确性测试" |
| Stacker: Verify the Stack Layout in a Verified Compiler | ICFP 2022 | 栈帧布局形式化，对应 L7 |
| RegAlloCA / 图着色 RA 的 ILP/SMT 新解法 | CGO 2022-2024 | 寄存器分配自动化求解 |
| MLIR 生态论文（Lattner et al. 后续）与 Triton 编译栈 | PLDI/OSDI 2021-2024 | 简化 IR 设计的当代延伸（Koopa→MLIR 视角） |
| SysY/“系统能力大赛” 相关教学论文 | 国内教学会议 2021-2024 | 课程背景与评测体系 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| Koopa IR（LLVM IR 子集） | LLVM | IR/SSA/phi、pass 管线的原型 |
| 词法/语法工具生成 | tree-sitter、flex/bison | 增量词法与 GLR 解析，现代编辑器基础设施 |
| RISC-V 指令选择 | GCC / LLVM RISC-V 后端 | TableGen 模式匹配 vs 本课程手工映射 |
| 栈帧与调用约定 | RISC-V ELF psABI + glibc | 帧布局、ra 保存策略 |
| 常量折叠/CSE/内存提升 | Rustc MIR optimizer | MIR 层面的同族简化 pass |
| 自动测试/差分测试 | csmith、fuzzing 工具 | L9 之后自测编译器正确性 |
| SysY 评测 | 全国大学生计算机系统能力大赛（SysY 赛题仓库） | 课程成果直接参赛 |
