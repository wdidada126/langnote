# CS3110 配套项目计划（骨架，本轮不写代码）

语言统一 OCaml（dune 构建），呼应课程 PSet 风格（库实现 + 规格 + 测试）。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2–L4 列表/ADT | OCaml | 表达式计算器：手写 AST + 求值 + pretty printer | `dune build && dune exec` |
| L5–L6 Option/测试 | OCaml | 带性质的随机测试套件（qcheck 风格 mini 实现） | `dune runtest` |
| L7 ADT | OCaml | Set/Map 两种实现（有序列表 vs BST）共享同一签名 | `dune build`，接口一致性测试 |
| L8 效率 | OCaml | 摊还分析实验：two-stack queue 计时 vs 渐近预测 | `dune build --profile release` |
| L9 可变性 | OCaml | 备忘录/缓存函数库 + GC 行为观察 | `dune exec` + perf 采样（可选） |
| L10 模块/函子 | OCaml | 用 functor 把 Set 复用进图算法（Dijkstra） | `dune build` |
| L11 类型检查 | OCaml | 微语言类型推理器 (HM 算法 W 简化版) | `dune test`（坏程序必须被拒） |
| L12–L13 解释器 | OCaml | 课程 "Caml Light"式微语言：env 模型→惰性/异常/对象扩展 | `dune exec --repl` REPL |
| L14 证明 | Markdown/OCaml | 为核心库写形式化规格与归纳证明笔记 | 文档形式，无需编译 |

约定：本轮只列计划；所有项目 dune 单仓多包结构预留。
