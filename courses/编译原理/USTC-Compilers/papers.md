# USTC 编译原理与技术 — 论文与延伸阅读骨架

## 经典论文（龙书配套 + LightIR/后端/RA 专题）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Aho et al. — 龙书（配套讲义主干） | 2006 | 全课程理论总纲 |
| Johnson — Yacc — A Parser Generator | 1975 | L3/L5 Bison 一系 |
| Lesk & Weinreb — Lex: A Lexical Analyzer Generator | 1975 | L2/L5 Flex 一系 |
| Cocke & Allen — A Machine Program for Analysis | 1969 | 数据流/全局优化源头（L10/L12） |
| Cytron et al. — Efficiently Computing SSA | 1991 | LightIR 的 SSA 语义基础 |
| Chaitin — Register Allocation via Coloring | 1981 | L14/L15 图着色 |
| Preston Briggs — Register Allocation via Graph Coloring PhD | 1992 | RA 工程化改进 |
| Lattner & Adve — LLVM 论文 | 2004 | LightIR 的母体设计 |
| Appel & Jim — Runtime / Typed FlINT 系列 | 1997 | 现代教学编译器对照（虎书系） |

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| LoongArch ISA 体系相关白皮书与工具链论文 | 龙芯/学术出版 2021-2023 | L8-L9 国产 ISA 后端语境 |
| CompCert 后端验证（C--{}） | POPL 2021 | 后端正确性对照 |
| 学习驱动寄存器分配（RegAllocAI 及后续 CGO/MLSys 工作） | 2021-2024 | L15 现代 RA |
| MLIR / Triton 编译栈 | PLDI/OSDI 2021-2024 | IR 分层设计延伸 |
| 开源教材建设 + 自动化评测的编译教学改革 | 国内教学会议 2021-2024 | 课程方法论 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| Flex/Bison 前端 | GCC（ Bison 生成）、tree-sitter | L1 同源技术栈 |
| LightIR（LLVM 子集） | LLVM IR / Clang | L2/L4 直接对接 `opt`/`llc` 验证 |
| LoongArch 后端 | GCC/LLVM loongarch 后端、Loongnix 工具链 | L3 的现实工业对应 |
| 数据流/GVN | LLVM Pass（GVN、SCCP） | L4/L5 优化管线 |
| 寄存器分配 | GCC LRA、LLVM FastRA | L6 的工业实现对照 |
| 自动化评测 | 官方 testcases + CI 脚本 | 课程与 SysY/大赛评测同构 |
