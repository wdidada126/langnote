# Cambridge Semantics — 论文与延伸阅读骨架

## 经典论文（语义学标准配置）

| 论文 | 年份 | 与课程知识点的关系 |
| --- | --- | --- |
| Church — A Set of Postulates for the Foundation of Logic (λ 演算) | 1932/1936 | L7 源头文献 |
| Scott — Data Types as Lattices (Comp. Lang.) 与域理论系列 | 1968-1972 | L9-L10 指称语义基石 |
| Milner — A Theory of Type Polymorphism in Programming (JCSS) | 1978 | L8 多类型经典 |
| Plotkin — A Structural Approach to Operational Semantics | 1981 | L3-L4 SOS 方法论 |
| Hoare — An Axiomatic Basis for Computer Programming (CACM) | 1969 | 公理化语义引介（L13 后续入口） |
| Park — Concurrency and Automata on Infinite Sequences（互模拟定义） | 1981 | L12 bisimulation |
| Winskel — The Formal Semantics of Programming Languages（教材） | 1993 | 全课程主干 |
| Pierce — Types and Programming Languages（教材） | 2002 | L5-L8 对照教材 |
| Milner — Communication and Concurrency（CCS 教材） | 1989 | L12 延伸阅读 |

## 近 5 年论文（2021–2026）

| 论文 | 出处/年份 | 方向 |
| --- | --- | --- |
| 语义的机器验证（Coq/Lean 中的 SOS 与 soundness 证明，如 Software Foundations 后续与 CompCert 教学线） | ITP/CICM/CACM 2021-2024 | L3-L6 形式化再证 |
| 并发语义与互模拟在新型语言（Rust 异步/GC 并发）中的应用研究 | POPL/CONCUR 2021-2024 | L12 前沿 |
| 域理论/概率语义（随机程序指称语义）进展 | LICS/POPL 2021-2024 | L9-L11 延伸 |
| 教学型语义工具（语义即代码：PLT Redex/Coq 微课） | JFP/TFP/SIGCSE 2021-2024 | 学习方法 |
| 全抽象与程序等价在验证编译器中的新案例 | POPL/PLDI 2021-2024 | L11 工程回响 |

## 知识点在开源项目中的应用

| 知识点（本课程） | 开源项目 | 具体应用 |
| --- | --- | --- |
| 操作语义（SOS） | K Framework、Oxide（Rust） | 语言规范的 executable/可复用语义 |
| 类型安全证明 | Coq（Software Foundations/VST）、Lean 4 | 教科书定理机械验证 |
| λ 演算/规范化 | Coq/Lean 内核（CIC/TTIP 路线） | 证明即计算 |
| 指称语义 | 概率程序语言（WebPPL/Church 语义研究）、qPL 系 | 随机程序推理 |
| 互模拟 | 模型检测工具（mCRL2、CADP） | 并发系统等价化简 |
| 语义等价 | 验证编译器（CompCert 的等价性证明） | 优化合法性 |

> 个别条目以"方向+代表作"给出，填充时精确化引用版本与年份。
