# CS3110 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| Structure and Interpretation of Computer Programs (SICP) | Abelson & Sussman, 1985 | L12 | 课程前身 MIT 6.001 教材，"modern SICP" 称号的参照系 |
| A Theory of Type Polymorphism in Programming | R. Milner, 1978 | L11 | Hindley-Milner 类型推理源头 |
| The Zinc Experiment: An Efficient Machine-Coded Compiler for CAML | X. Leroy, 1990 | L13 | OCaml 编译器与函数式语言高效实现经典 |
| Purely Functional Data Structures | C. Okasaki, 1996 (博士论文/书) | L7–L8 | 不可变数据结构的系统文献 |
| Logical Foundations of Programming Methodology | M. Gries & F. B. Schneider, 1993 | L14 | 形式化规格与归纳证明的教材级参考 |

> 骨架注：以上为确定清单；正式填充时按讲次细化补充课程 textbook 内引用。

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| CS3110 Textbook 2e 修订（持续更新） | 2021–2024 | 全课 | 教材本身即最新一手材料 |
| OCaml 5.x 效果系统 (Effects) 发布 | 2023 | L13 | 并发原语的语言级新实现 |
| dune/odoc 工具链演进文档 | 持续 | L1/L6 | 现代 OCaml 工程实践 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| ADT/模式匹配 (L4) | Flow (Meta/Facebook) | 以 OCaml 编写的 JS 类型检查器 |
| 模块/函子 (L10) | Jane Street Core / Incr | 模块编程在金融交易系统的工业应用 |
| 解释器 (L12) | CS143/CS420 各项目 | 微语言解释经验直接迁移到编译器课 |
| 测试/性质验证 (L6) | qcheck / Crowbar | OCaml 生态性质测试库 |
| 数据结构 (L7–L8) | OPAM 依赖求解器 (mccs) / js_of_ocaml | 函子化数据结构 + 算法的落地 |
| GC (L9) | OCaml 运行时自身 | 分代/增量 GC 的教科书样本 |
