# Cambridge Semantics — 配套项目计划（本轮只列计划，不写代码）

> 语言统一 OCaml（dune 工程，与课程 ML 背景一致）。本课程无官方公开作业，项目按"把每条语义规则变成可运行代码 + 可检验证明笔记"设计。**本轮只写不编译**，集中编译验证稍后由用户执行。

## 章节 → 项目映射表

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1-L3 大步语义 | OCaml | 简单命令式语言（Imp）解释器：BNF→AST→`eval` 关系 | dune build/test |
| L4 小步语义 | OCaml | 单步归约机 + `→*` 收敛/发散可视化（输出 trace） | dune test |
| L5-L6 类型安全 | OCaml | Imp 子集类型检查器 + progress/preservation 笔记证明（附反例测试） | dune + 证明 md |
| L7 λ 演算 | OCaml | 纯 λ 正规化器（CBV/CBN/正全规三模式）与 α 转换 | dune test |
| L8 子类型 | OCaml | 记录微语言 + 宽度子类型检查 | dune test |
| L9-L10 指称语义 | OCaml/Python | while 语言到"状态变换算子"的翻译，数值迭代逼近最小不动点 | dune / pytest |
| L11 语义等价 | OCaml | 观察等价判定玩具（穷举小上下文）对照指称相等 | dune test |
| L12 并发互模拟 | OCaml | 有限 CCS 进程互模拟判定器（分区细化算法） | dune test |
| L13 总结 | — | "三范式对照表" 笔记 + 用 Lean 复证 L6 定理的探索报告（可选） | 无 |

## 里程碑验收标准

- 每个解释器/判定器：README 先贴语义规则（分数式排版），再贴代码，测试即规则用例。
- 证明笔记：每定理给出结构归纳的完整推导树骨架。
- 与 `notes/outline.md` 双向链接。
