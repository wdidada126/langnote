# KAIST CS420 — 逐讲要点骨架

> 骨架级要点；填充时对照 kaist-cp/cs420 textbook 与实验讲义展开。

## L1 课程总览：C→RISC-V 与 KECC 架构
- KECC = KAIST Educational C Compiler：框架已给前端，学生在其上补齐各阶段核心。
- 管线：C 源码→AST→HIR→LIR(SSA)→优化→RV64 汇编。
- 真实 C + csmith Fuzzing：正确性以"差分测试通过"为准绳。
- Rust 所有权/借用与编译器数据结构（Arena、Rc）实践语境。

## L2 前端速览与 AST 遍历
- 语法树、符号信息与 C 类型系统要点（数组/指针退化）。
- 不要求手写前端：理解"框架边界"，把精力留给 IR 与后端。
- AST 遍历模式：fold/visit 在 Rust 中的惯用写法。

## L3 Lab1：AST 打印
- 用括号化约定打印 AST：最小可视化反馈回路。
- 遍历 + 格式化 = 后续所有"打印 IR"技能的地基。
- 测试驱动：每实现一个节点类型跑对应测试。

## L4 HIR 与 CFG 构建
- HIR：表达式语句混合的高层 IR，贴近 AST 但已去掉文法噪音。
- 基本块划分与 CFG 边（br/cond）构造。
- 短路求值、循环在 HIR 层的规范化。

## L5 LIR 与 SSA/phi
- LIR：寄存器级三地址 + 显式栈操作（mov/getp/putp）。
- SSA 约束：每变量单一定义；phi 在 join 点合并。
- 从 HIR 降 LIR：临时寄存器分配与 spill 雏形。

## L6 数据流分析与支配树、use-def 链
- 支配/必支配前沿（dominance frontier）→ phi 放置位置。
- use-def 链：后续 GVN、死代码删除的基础设施。
- 可达定义/活跃区间在 SSA 上的平凡化。

## L7 优化 I：CFG 简化
- 不可达块删除、单前驱/单后继块合并、空块跳转压缩。
- 保持 SSA 不变量的简化条件。
- 实验形式：给简化函数补全，通过属性测试。

## L8 优化 II：GVN
- 值编号：同表达式只求值一次；哈希-cons 实现。
- 与支配树协作：只在定义支配处复用值。
- memory-to-register promotion：可提升局部变量消 load/store。

## L9 优化 III：循环与内联
- LICM、强度削弱、循环展开的收益与代码膨胀权衡。
- 内联启发式与调用图。
- pass 排序与管线设计哲学（对照 LLVM PassBuilder）。

## L10 后端 I：RV64 指令选择
- LIR→机器指令映射：立即数范围、寻址模式约束。
- RV64I/M/A/F/D 基线；伪指令展开。
- 指令调度初探（延迟槽在 RISC-V 不存在，但依赖仍要排）。

## L11 后端 II：栈帧与调用约定
- RV 调用约定：ra/sp/a0-a7/s0-s11，谁保存谁恢复。
- 帧布局：参数溢出区、保存区、局部区对齐。
- 叶子函数优化与 ra 省略。

## L12 后端 III：寄存器分配与 peephole
- Live range 计算→干涉图→着色/拆分；spill 代价启发。
- KECC 采用相对朴素但正确的 RA：先保证通过测试再谈质量。
- peephole：立即数合并、冗余 mv 删除。

## L13 csmith Fuzzing 与差分测试
- 随机 C 程序生成→gcc/clang vs KECC 结果比对。
- 测试化归（test-case reduction）与最小复现。
- 用 fuzzing 思维审视每个优化 pass 的合法性。

## L14 前沿：Verified Compilation 与总结
- Vellvm：用 Coq 验证 LLVM IR 语义（课程实验室方向）。
- CompCert 对照：全验证 vs 测试驱动的取舍。
- 结课复盘：C→RISC-V 每一跳"为什么这样做，还能怎么做"。
