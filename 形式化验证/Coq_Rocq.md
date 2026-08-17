# Coq / Rocq：交互式定理证明器

> 本文件中的 Coq 与 Rocq 指同一证明器生态。项目已更名为 Rocq Prover；阅读旧论文、旧仓库和 opam 包时仍会大量看到 Coq 名称。

## 它是什么

Rocq 是带依赖类型的函数式语言和交互式定理证明器。开发者把数据结构、程序、规格和定理写成精确定义，再用 tactic 逐步构造证明；最后由可信内核检查生成的证明项。它适合需要“机器可检查的正确性保证”的领域，例如编译器、密码协议、操作系统、并发算法、数学定理和关键基础设施。

核心观念是 Curry-Howard 对应：命题可视为类型，证明可视为该类型的程序/值。`Theorem` 提出待证明目标，`Proof` 进入交互证明，`Qed` 只会在所有子目标完成且证明项通过内核检查后结束。tactic 用于提高书写效率，但最终可信的不是 tactic 的“结论提示”，而是内核检查的证明项。

```coq
From Stdlib Require Import Arith.

Theorem plus_zero_r : forall n : nat, n + 0 = n.
Proof.
  intro n.
  induction n as [| n ih].
  - reflexivity.
  - simpl. rewrite ih. reflexivity.
Qed.
```

这段例子表达的不是“跑了几个测试后认为成立”，而是对任意自然数 `n` 构造归纳证明。证明器会显示当前未完成目标；每一步都必须把目标化简、拆分或归约到已知事实。

## 能做什么

| 用途 | 说明 | 代表性问题 |
| --- | --- | --- |
| 规格与证明 | 将函数前置条件、后置条件、不变式和抽象模型写成定理 | 排序结果有序且是原数组的排列；事务提交满足原子性。 |
| 并发/系统验证 | 配合 Iris、Perennial、VST、Aneris 等程序逻辑库 | 锁没有数据竞争；日志恢复后状态满足不变式。 |
| 程序提取 | 从一部分构造性定义中抽取 OCaml/Haskell 程序 | 从经过证明的算法定义生成可执行实现。 |
| 数学形式化 | 表达代数、数论、图论和分析中的定义与定理 | 将论文证明转为可复查的机器证明。 |
| 证明自动化 | 使用 `lia`、`ring`、`auto`、Ltac/Ltac2 等辅助完成规则化子目标 | 线性整数算术、等式归一化、重复性证明步骤。 |

## 它不保证什么

Rocq 证明的是“**在写下的模型、规格、公理和已验证依赖成立时**，结论成立”。因此正确性边界仍包括：

- 规格可能写错或遗漏业务属性。证明“实现满足错误规格”不会得到正确产品。
- 未建模的 FFI、操作系统、网络、硬件、编译器、密码假设和人工引入公理都不自动获得保证。
- 证明通常侧重安全性（safety），例如不违反不变量；终止性、性能、实时性、侧信道安全和可用性需要额外模型与证明。
- 将已证明的模型抽取或连接到生产二进制时，仍需说明编译器、运行时和接口的可信基础。

因此，Rocq 不是“比测试更强的单元测试工具”，而是要求先把要保证的性质精确定义的工程方法。

## 基本工作流

```text
非形式化需求
    -> 数据模型与抽象状态机
    -> 函数/模块规格、前置条件和不变式
    -> Rocq 定义与引理
    -> 交互证明和自动化 tactic
    -> 内核检查 .vo 编译产物
    -> 与实现、测试、代码审查和部署保障共同构成系统可信边界
```

实际项目会将证明拆为小引理：先证明数据结构表示关系，再证明单个操作维持不变式，最后组合为模块级定理。不要一开始试图证明完整数据库或分布式系统；先用有限状态机、列表、映射和顺序算法理解归纳、量词和等式重写。

## 与 MVCC、Iris、Perennial 的关系

- MVCC 是待验证的数据库并发控制算法，Rocq 不实现 MVCC，而是承载其形式化规格和证明。
- Iris 是在 Rocq 中实现的高阶并发分离逻辑，提供所有权、不变式、ghost state 等更适合并发程序的推理语言。
- Perennial 在 Iris 之上面向 Go 并发/崩溃安全系统；Goose 将受支持的 Go 代码转为可在 Rocq 中证明的语义表示。

在 vMVCC 中，Rocq 内核最终检查 Perennial/Iris 写出的证明，结论是该研究原型在其形式化模型下满足事务库规格，而不是“Rocq 运行了 vMVCC 的压力测试”。

## 学习路线

1. 用 Rocq Platform 或 opam 建立隔离环境，学会编辑器显示 proof state、编译 `.v` 文件和阅读错误目标。
2. 阅读 Software Foundations 的 Logical Foundations，掌握归纳类型、递归函数、`induction`、`rewrite`、`inversion`、存在量词和关系。
3. 写小型规格：列表反转保持长度、二叉树查找保持 BST 不变式、简单状态机的安全性。
4. 再进入程序逻辑或并发：先学 Hoare logic 与 separation logic，然后学习 Iris。
5. 只有在能读懂基本 proof state 后，才尝试 Perennial、vMVCC 等大型仓库；固定仓库的 opam lock/版本，不要将教程代码与最新 master 随意混用。

## 参考资料

- Rocq 官方首页、名称演进与发行信息：<https://rocq-prover.org/>
- Rocq 官方学习与安装入口：<https://rocq-prover.org/docs>
- Rocq Reference Manual：<https://rocq-prover.org/doc/master/refman/index.html>
- Software Foundations：<https://softwarefoundations.cis.upenn.edu/>
