# SJTU 编译原理 — 论文与延伸阅读骨架

## 经典论文（虎书配套 + 逃逸分析/GC/RA 专题）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Appel — *Modern Compiler Implementation in C*（虎书本体） | 1998 | 全课程管线蓝本 |
| Toft — Type-Directed Partitioning for Automatic Memory Management | 1990 | 静态类型语言 GC 根基（L13） |
| Boehm & Weiser — Garbage Collection in an Uncooperative Language | 1988 | L13 保守式 GC 工程原型 |
| Cytron et al. — Efficiently Computing Static Single Assignment Form | 1991 | L9-L11 IR 与活跃分析基础 |
| Chaitin et al. — Register Allocation via Spilling and Coloring | 1981 | L12 图着色 RA 源头 |
| George & Appel — Iterated Register Coalescing | 1996 | L12 拷贝合并标准算法 |
| Ramsey & Fernandez — 在线/增量寄存器分配方向 | 1990s | 虎书在线 RA 章学术脉络 |
| Appel — 逃逸分析与束分配（虎书 ch7 引用的 Toft/Lassen 系） | 1989-1992 | L6 逃逸分析原始文献 |
| Aiken & Foster — 类型/流分析辅助 GC 与别名方向（虎书延伸阅读） | 1990s | L6/L13 理论支撑 |

> 个别行作者-年份为方向性概括，正式填充时按虎书参考文献列表核对确切出处。

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| 教学/生产编译器差分测试与验证（CompCert 派生、fuzzing 方法） | POPL/CGO 2021-2024 | Lab 验证方法 |
| MLIR/Triton 编译栈生态论文 | PLDI/OSDI 2021-2024 | L9 LLVM 路线的当代延伸 |
| 学习驱动 RA/调度（RegAllocAI 后续） | CGO/MLSys 2021-2024 | L12 自动化决策 |
| 国产平台后端与教学工具链适配（LoongArch/RISC-V） | 学术/工业白皮书 2021-2024 | 目标码生成现实语境 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| Flex/Bison 前端 | GCC、bash | L3-L4 同源工业栈 |
| Tiger→LLVM IR | Clang（C→IR 路径）、Rustc（MIR→LLVM） | L9 直译模板对照 |
| 帧抽象 Frame 接口 | LLVM CodeGen（MachineFrameInfo/TargetFrameLowering） | L7 的工业放大版 |
| 活跃分析/数据流 | LLVM LiveIntervals、CodeQL | L11 的库化实现 |
| 寄存器分配 | LLVM Greedy/FastRA、GCC LRA | L12 生产级对应 |
| GC 专题 | Boehm GC、WebKit JSC 分代 GC | L13 工程形态 |
| 闭包/curry | OCaml、Rust 闭包 lowering | L14 运行时表示 |
