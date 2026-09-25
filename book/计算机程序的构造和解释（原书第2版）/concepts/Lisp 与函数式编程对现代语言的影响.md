# 专篇：Lisp 与函数式编程对现代语言的影响（1996 → 2026）

> **一句话**：Lisp 在 1960 年提出的所有 idea，到 2026 年基本都被主流语言吸收了——**区别只在于有的写了出来，有的藏在了标准库之后**。

---

## 1. 一张对照表：Lisp 的想法今天在哪

| Lisp / 函数式思想 | 出现于 | 2026 年的现状 |
| --- | --- | --- |
| 表达式即数据（S 表达式） | 1960 | 基本被放弃：JS/Python 用 JSON；只有 Lisp 系保留 |
| 一等函数（higher-order function） | 1975 | **已成标配**：JS 箭头函数、Python `lambda`、C++11 lambda、Java 8 lambda |
| 闭包（capture environment） | 1975 | 已成标配（JS/Go/Rust `Fn` trait） |
| 柯里化 / 部分应用 | 1936（lambda 演算） | Scala 3、Kotlin、TypeScript 支持；C++20 借 `lambda` + `bind_front` 部分实现 |
| 尾调用优化 | 1975 | **仍是最难推广的一块**：OCaml/Haskell/Racket 有；Java/Python/JS 无 |
| 惰性求值 | 1974 | 以**迭代器/生成器**形式落地（Rust `Iterator`、Python generator、JS 异步生成器） |
| 不可变数据 | 1975 | 已成共识：C++ `const`、Java record、C# `readonly`、Rust 默认不可变 |
| 高阶列表操作（`map/filter/fold`） | 1970s | 已成标配：SRFI-1、JS `Array`、Python `functools`、Rust `Iterator` |
| 代数数据类型与模式匹配 | 1980s ML | **已大规模普及**：Rust enum、Kotlin sealed、C# 模式匹配、Java 21 的模式匹配 |
| 数据导向（可加性） | 1978 | Rust trait、C++20 concept、Go 泛型 |
| 消息传递 / Actor | 1970s Smalltalk / 1986 Actors | Akka、`tokio` channel、Erlang/OTP |
| 宏系统 | 1978 | LISP 系独有；Rust 的 `macro_rules!` 是主流语言里最接近的 |
| 垃圾回收 | 1959 | 已成标配（C/C++ 仍靠 RAII/手动） |
|  continuations | 1970s | CPS 用于编译器与异步：`async/await`、生成器、Rust `async fn` |

> **这张表说明一件事**：SICP 讲的东西没有一样是「过时的古董」，它们的**实现方式变了，但思想被完整继承**。

---

## 2. 三条彼此竞争的技术路线

```
              ┌──────────────── 纯函数式（Haskell/OCaml/Racket）
              │   默认不可变 + 惰性求值 + 静态类型
              │
   Lisp ──────┼──── 混合式主流（Rust/Scala/Kotlin/Java/C++）
              │   不可变默认 + 命令式混合 + 静态类型
              │
              └──── 命令式 + 库（C/Go/Python/JS）
                  及早求值 + 可变默认 + 高阶函数当工具
```

> 2026 年的现实是**第三条路线占了绝大多数工业代码**，但第一条路的很多 idea 被塞进第三条的库里。
> **SICP 站在第一条路线**，这既让它深刻，也让它与日常工程有距离——这个距离值得显式说明。

---

## 3. 逐条对照 SICP 的章节与今天的语言

| SICP 章 | 2026 年的对应物 |
| --- | --- |
| 1.1 表达式与环境 | 任意语言；JS 的 `let` 块级作用域就是环境帧 |
| 1.2 递归 vs 迭代 | Java/Python 依然是坑；Rust/Scala 用 `tailrec`/循环 |
| 1.3 高阶函数 | JS `map/filter/reduce`、C++11 lambda、Python `functools.partial` |
| 2.1 数据抽象 | Rust `struct` + `impl`；Java `record`；Go struct + 接口 |
| 2.2 列表与高阶操作 | `Iterator` / generator / Streams |
| 2.4 数据导向 | trait / concept / 泛型约束（编译期版） |
| 3.1 赋值与对象 | 字段赋值；Rust 的 `&mut` 是它的类型化版本 |
| 3.2 环境模型 | V8 的 hidden class、JVM 的对象布局 |
| 3.4 并发 | Go channel、Rust `Send/Sync`、Clojure `ref` |
| 3.5 流 | 迭代器、响应式流（RxJS）、异步生成器 |
| 4.1 元循环求值器 | V8 Ignition、JVM 解释器、Rust 写的前端 |
| 5.x 寄存器机 | LLVM IR、WASM、Crawlift |

> 读完这张表会得到一个印象：**SICP 描述的不是一门过期语言，而是现代程序设计的底层结构图谱**。

---

## 4. 哪些 Lisp 的 idea 没有被吸收

诚实地说，有三样至今仍是 Lisp 独有：

| 特性 | 为什么没被吸收 |
| --- | --- |
| **宏系统**（代码即数据，可改写语法） | 调试困难、错误信息差、工具链支持弱；Rust 的宏是折中 |
| **真正的 `eval`**（任意环境求值任意表达式） | 安全问题（eval injection）；今天只在沙箱与 REPL 里用 |
| **默认惰性求值** | 性能和可推理性代价太大，工业界选择显式迭代器 |

> 这一条很重要：**SICP 不主张你改用 Lisp，它主张你理解这些抽象**。2026 年的最佳姿势是「用 Rust/Go/Java 解决工程问题，用 SICP 的思维模型控制复杂度」。

---

## 5. 2026 年反 Lisp 的几股力量

| 力量 | 表现 |
| --- | --- |
| **类型系统复兴** | Rust/Scala 让「静态类型」比「动态 + 高阶」更受欢迎 |
| **推理成本被重新计价** | 大型代码库里，不可控的动态行为代价极高 |
| **调试与可观测性优先** | 栈回溯、断点、profiler 成为基础设施，宏与 TCO 都与之冲突 |
| **AI 辅助编程** | 机器学习写代码时，显式语法比宏更容易被生成和检查 |
| **WASM 的兴起** | 目标平台从物理 CPU 变成字节码 VM，寄存器机思想再次中心化 |

---

## 6. 建议的阅读路径（想补齐 SICP 缺的那块）

| 想补什么 | 读什么 |
| --- | --- |
| SICP 没有的类型系统 | *Types and Programming Languages*（Pierce） |
| SICP 没有的模块与包 | Racket 的 `provide/require`；Rust 的模块系统 |
| SICP 没有的并发安全 | Rust 的所有权与 `Send/Sync` |
| SICP 没有的工程实践 | *Continuous Delivery* / *Clean Code* / *重构* |
| SICP 的编译器部分怎么落地上生产 | *Engineering a Compiler*（Appel）/ *Crafting Interpreters*（Nystrom, 2021） |
| 想看 Lisp 的完整表达力 | *On Lisp*（Graham 1993）/ *Practical Common Lisp*（Seibel 2005） |

---

## 7. 延伸文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| *The Roots of Lisp* | Abelson, 2002（在线文章） | 用 30 行讲清 Lisp 的所有基础，是理解本篇的最佳起点 |
| *On Lisp* | Paul Graham, 1993 | 函数式抽象的完整表达力 |
| *The Art of the Interpreter* | Abelson, Sussman, Sussman, AI Memo 505, 1982 | 本篇的思想源头 |
| *结构解释与计算机程序*（第 2 版） | Abelson 等, MIT Press 1996 | 原书 |
| *Functional Programming in Scala*（第 3 版） | 2020 | 函数式思想在主流语言里的完整落地 |
| *Crafting Interpreters*（在线书 + 仓库） | Bob Nystrom, 2021 | 用 Java/JS 从零写解释器，是 4/5 章的现代替代 |
| *The Concise Encyclopedia of Programming Languages* | Reynolds, 在线版 2020 | 语言谱系的横向对照 |
