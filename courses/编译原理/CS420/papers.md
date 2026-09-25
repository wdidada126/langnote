# KAIST CS420 — 论文与延伸阅读骨架

## 经典论文（编译课：SSA/优化/RA/验证编译）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Cytron et al. — Efficiently Computing Static Single Assignment Form and the Control Dependence Graph | 1991 | L5-L6：SSA 与支配树的圣经 |
| Lattner & Adve — LLVM: A Compilation Framework for Multiphase Optimization | 2004 | 本课程 IR 设计的现实原型 |
| Chaitin et al. — Register Allocation via Spilling and Coloring | 1981 | L12：图着色 RA 源头 |
| Briggs, Cooper, Torczon — Practical Improvements to the Coalescing and SSA Register Allocation | 1994/2003 | L12：现代 RA 工程化 |
| Click — Engineering a Simple, Efficient Code Optimizer（太虚博士论文） | 1995 | L8：GVN/值编号的现代实现范式 |
| Ramsey & Davidson — Encapsulating Linkage with Frame Structures（虎书框架模块出处） | 1998 | L11：栈帧抽象设计参照 |
| Leroy — The CompCert Verified Compiler | 2006 | L14：全验证编译对照组 |
| Lee et al. — Vellvm: Efficient Reasoning about the Design and Semantics of LLVM IR（POPL） | 2015 | L14：kaist-cp 组对 LLVM IR 的形式化 |
| Yang et al. — Finding and Understanding Bugs in C Compilers（csmith 论文，PLDI） | 2011 | L13：差分测试方法学出处 |

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| Leroy et al. — CompCert 后端 C--{} 算术后端验证 | POPL 2021 | 后端翻译正确性 |
| 学习驱动寄存器分配（RegAllocAI 及后续演进） | CGO/MLSys 2021-2024 | L12：RL 优化 RA |
| Lattner et al. — MLIR 生态与 Triton 编译栈后续 | PLDI/OSDI 2021-2024 | IR/管线设计的当代延伸 |
| Granite（学习驱动 GVN 代价模型）及同类工作 | arXiv/CGO 2023-2024 | L8-L9：优化决策自动化 |
| kaist-cp 组编译教学改革与 KECC 经验报告 | KSE/SIGCSE 2022-2024 | 课程本身的教学研究 |

> 个别条目以"方向+代表作"形式给出，填充笔记时核对确切标题与作者全名。

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| SSA IR 设计 | LLVM IR、Rustc MIR | phi/支配前沿与课程 LIR 一一对应 |
| CFG 简化/GVN | LLVM NewPM（SimplifyCFG、GVN、Mem2Reg） | 直接可对照阅读的实现 |
| 循环优化 | GCC（LICM、unroll）、LLVM LoopPass | L9 工业实现 |
| RV64 代码生成 | LLVM RISC-V 后端、rustc（复用 LLVM） | L10-L12 指令选择与帧降低 |
| csmith 差分测试 | csmith、llvm-benchmarks、fuzztest | L13 方法学 |
| IR 形式语义 | Vellvm（Coq）、CompCert | L14 验证路线 |
