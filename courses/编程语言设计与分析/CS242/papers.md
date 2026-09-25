# Stanford CS242 — 论文与延伸阅读骨架

## 经典论文（PL 课标准配置：类型理论 + 语言实战 + Caml Cases）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Church — An Unsolvable Problem of Elementary Number Theory（λ 演算） | 1936 | L3 的源头 |
| Milner — A Theory of Type Polymorphism in Programming | 1978 | 类型推断与安全性经典（L5） |
| Wright & Felleisen — A Syntactic Approach to Type Soundness | 1994 | progress/preservation 范式（L5） |
| Leroy — Caml Cases（OCaml 工业落地案例集） | 2009/2020 修订 | L4/L5/L11 函数式编程现实价值总证据 |
| Rossberg et al. — WebAssembly 规范论文（Bringing the World Together） | 2017 | L6 主文献 |
| Lehmann & Tan — Where's the Soundness of WebAssembly? | 2019 | L6 批判性阅读 |
| Walker — Substructural Type Systems（博士论文，线性/相关类型） | 2000 | L7 线性/相关类型理论 |
| Jung et al. — RustBelt: Securing the Foundations of the Rust Programming Language | 2018 | L7 Rust 所有权的语义根基 |
| Honda — Types for Dyadic Interaction（会话类型） | 1993 | L9 会话类型开山 |
| Blackwood et al. — stakette: Session Types as a Library（OOPSLA 2021） | 2021 | L9 typestate 会话类型 TCP 库 |
| Pierce — TAPL 教材 | 2002 | 前半课程主干 |

> 两处"待核对"仅作提示，正式填充时替换为准确条目（线性类型博士论文年份、会话类型 Rust 库论文）。

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| Crichton — From Theory to Systems: A Grounded Approach to Programming Language Education | POPL 2024 | 本课程教学法本身 |
| RustBelt Meets Refinement / 所有权扩展（如 RustBelt 后续、statiq） | POPL/ICFP 2021-2024 | L7 前沿 |
| 会话类型 Rust 库与验证（stakette 后续、rusty_hoop 等） | OOPSLA/ICFP 2021-2024 | L9-L10 |
| Lean/Mathlib 自动化与验证（如 Lean 4 生态论文） | ITP/CICM/CACM 2021-2024 | L10 定理证明线 |
| 函数式自动微分与 ML 框架（如 Enzyme、Maluuba 等 PL 系 AD 工作） | PLDI/OOPSLA 2021-2024 | L11 深度学习框架线 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| λ 演算/类型检查 | rustc（类型系统）、OCaml 编译器 | L5 检查器的工业放大 |
| OCaml 工程 | opam/dune、tree-sitter OCaml binding、FFI | L4 生态 |
| WebAssembly | Wasmtime、V8、wasm-bindgen | L6 运行时与工具链 |
| 线性类型/所有权 | Rustc borrow checker（NLL/Polonius 方向） | L7 直接对应 |
| 异步 | tokio、smol、Futures 库 | L8 executor 实现 |
| 会话类型 | stakette、rusty_hoop（作者含课程助教线） | L9 HW 参考实现 |
| 定理证明/验证 | Lean 4、Coq、F*、Verus | L10-L11 大作业工具 |
| 函数式 AD/ML | OCaml 版小型框架（如 owl、gll 系）；对比 PyTorch autograd | L11 深度学习框架作业 |
