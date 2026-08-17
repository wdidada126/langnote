# Iris：高阶并发分离逻辑

## 它是什么

Iris 是在 Coq/Rocq 中实现并被机器验证的高阶并发分离逻辑框架。它的目标不是取代 Rocq，而是在 Rocq 之上提供适合证明共享可变状态、细粒度并发、抽象数据类型和程序 refinement 的逻辑语言与 proof mode。

传统 Hoare logic 常写为 `{P} c {Q}`：若执行前满足 `P`，程序 `c` 结束后满足 `Q`。当多个线程共享堆、锁和回调时，关键问题变成“谁拥有哪个资源、资源何时转移、哪些状态可共享”。分离逻辑把命题解释为对资源的断言，Iris 再加入高阶谓词、不变式、模态、ghost state 和逻辑原子性，使这些推理能模块化组合。

## 最重要的直觉

| 符号/概念 | 直觉 | 用途 |
| --- | --- | --- |
| `l ↦ v` | 独占拥有位置 `l`，其中保存 `v` | 防止两个线程同时以可写方式声称拥有同一内存。 |
| `P ∗ Q` | `P` 与 `Q` 分别占有互不重叠的资源 | 将两个独立模块或线程的证明拼接起来。 |
| frame rule | 程序未触及的资源可从证明中“框住”保留 | 局部推理：证明函数时不用展开全局堆。 |
| invariant | 长期共享状态必须始终满足的约束，按规则短暂打开/关闭 | 描述“锁保护的 map 始终满足 key 唯一”等共享不变量。 |
| weakest precondition（WP） | 为使程序得到后置条件所需的最弱前置条件 | 以组合式规则从语句推导程序规格。 |
| ghost state | 仅存在于证明中的抽象资源 | 记录逻辑版本号、权限、历史、事务状态，不进入生产二进制。 |
| logically atomic triple | 把多步骤并发实现暴露为客户端看来一次发生的原子操作 | 为无锁栈、事务 `Run`、并发 map 提供好用的抽象规格。 |

`P ∗ Q` 不是普通逻辑的 `P ∧ Q`。后者允许同一资源同时被两边引用；前者要求资源可分离，因此天然适合表达独占堆所有权。对于共享只读资源、锁或协议状态，Iris 使用持久断言、不变式、权限 token 等机制，而不是放弃所有权约束。

## 一个锁的证明心智模型

```text
共享计数器 n，要求 n >= 0

锁未持有：invariant 中保存 counter ↦ n 与 n >= 0
线程 acquire(lock)：按 Iris 规则打开 invariant，取得 counter ↦ n
线程修改：将 n 改为 n + 1，证明新状态仍满足 n + 1 >= 0
线程 release(lock)：把 counter ↦ (n + 1) 放回 invariant，重新关闭 invariant
```

这里的“打开 invariant”是证明规则，不表示运行时关闭整个系统；它约束证明者只能在原子步骤附近以受控方式访问共享资源。由此可以证明实现不破坏共享状态，但仍需单独定义想要的抽象语义，例如计数器 `inc` 是否线性化、队列是否 FIFO、事务是否可串行化。

## Iris 适合解决的问题

- 细粒度并发数据结构：无锁队列、栈、哈希表、内存回收与 helping。
- 锁、条件变量、通道、会话协议和资源生命周期的模块化规格。
- 逻辑原子性：实现需要多步 CAS/重试循环，客户端仍可像调用原子 ADT 一样推理。
- 程序 refinement：证明优化实现、并发实现与更简单抽象规范等价或细化。
- 作为其他逻辑的基础：Perennial（Go/崩溃安全）、Aneris（分布式系统）、Actris（会话类型）、RefinedRust 等。

## Iris 在 vMVCC 中的作用

vMVCC 的物理实现包含 tuple 版本链、每 tuple 锁、活动事务集合、时间戳 site 和后台 GC。Iris 用不变式和 ghost state 将这些物理结构关联到抽象数据库历史；逻辑原子规格使客户端可把一次事务看成原子状态转换。

难点在于事务的抽象效果不必出现在该事务自己的某一行代码上。vMVCC 使用 Iris 的 prophecy variables 表达未来非确定性结果与逻辑状态演化的关系，再用 logically atomic triples 连接客户端事务体、读写结果和提交/中止语义。预言变量与 ghost state 只在证明中存在，不会影响 Go 实现的运行时性能。

## 它不是什么

- Iris 不是编程语言、Go 编译器或数据库；它是嵌入 Rocq 的逻辑和证明库。
- Iris 不会从任意源码自动推导业务规格。人必须定义抽象状态、线性化语义、资源不变式和信任边界。
- Iris 的安全性证明不自动给出活性、性能、无死锁、实时期限或分布式可用性；这些需要对应扩展逻辑、调度/公平性假设或独立证明。
- “使用了 Iris”不等于生产代码无 bug。结论只覆盖已建模、已翻译和已完成证明的部分。

## 学习路线

1. 先会写 Rocq 的递归函数和归纳证明，理解命题、类型和 proof state。
2. 学普通 separation logic：heap ownership、`∗`、frame rule、Hoare triple。
3. 完成 Iris 官方 Lecture Notes 或 Iris Tutorial in Rocq 的基础章节，再练习 HeapLang 的引用、CAS、fork 和锁。
4. 学 invariant、WP、persistent assertion、ghost state 和 logical atomicity；每个概念都配一个并发容器例子。
5. 最后读 Perennial/vMVCC。面对大证明时先找抽象规格与不变式，后看 tactic；不要从几千行 proof script 的末尾开始阅读。

## 参考资料

- Iris 项目、Rocq 实现、教程与论文：<https://iris-project.org/>
- Iris Lecture Notes：<https://iris-project.org/tutorial-pdfs/iris-lecture-notes.pdf>
- Iris Tutorial（Rocq）：<https://github.com/logsem/iris-tutorial>
- 《Iris from the Ground Up》：<https://iris-project.org/pdfs/2017-esop-iris3-final.pdf>
