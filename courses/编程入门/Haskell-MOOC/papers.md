# Haskell MOOC 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| Why Functional Programming Matters | J. Hughes, 1984 | 全课 | FP 价值最著名的论述文章 |
| Notions of Computation and Monads | E. Moggi, 1991 | L10 | Monad 进入程序语义的源头 |
| Monads for Functional Programming | P. Wadler, 1995 | L9/L10 | 面向使用者的 monad 讲解经典 |
| Tackling the Awkward Squad: Monadic Input/Output, Concurrency, Exceptions, and Non-Determinism | P. Peyton Jones, 2001 | L9/L14 | 纯函数语言如何处理"脏问题" |
| Implementing Lazy Functional Languages on Stock Hardware: The STG Machine | S. Peyton Jones, 1992 | L14 | 惰性求值实现机制 |
| How to Make Ad-Hoc Polymorphism Less Ad Hoc | P. Wadler & S. Blott, POPL 1989 | L8 | typeclass 原始论文 |

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| Haskell 2022 语言报告发布 | 2023 | 全课 | 语言标准化的最新基线 |
| Linear Types in GHC (GHC 9.x LinearTypes 扩展稳定化) | 2021+ | L9/L14 | 资源使用监控：FP 抽象的现代延伸 |
| GHC Proposed Extensions 文档持续更新 | 2021–2025 | L11–L13 | typeclass 体系演进风向标 |
| moocfi/haskell-mooc 仓库修订 | 持续 | 全课 | 课程官方作业最新形态 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 纯函数/不可变 (L2–L5) | React/Redux (reducer) | FP 思想在前端主流化的样本 |
| Promise/then ≅ Monad (L10) | fp-ts (TypeScript) | 把 Haskell 抽象移植到 TS 的完整库 |
| Java Optional/Stream ≅ Functor/Applicative (L11–L12) | JDK java.util.stream | 课程动机章节的直接对应物 |
| Monad: IO/解析 (L9–L10) | Pandoc | Haskell 编写的通用文档转换引擎 |
| Applicative 组合 (L12) | Cardano (PLC/Haskell 智能合约) | 生产级 Haskell 形式化验证栈 |
| FRP (L15 Fraxp) | reactive-banana / Elm | 课程项目概念族谱 |
| 惰性求值 (L14) | Scala LazyList / GHC RTS | 惰性集合的跨语言回声 |
