# 06 · 结构与测试：Lenses、并行概览与类型类封顶（本仓专题划分，非原书章名 ⚠️）

> **三态头**
> - ✅ 已证书目事实：*The Joy of Kotlin*，Pierre-Yves Saumont，Manning，2019-04，
>   ISBN 9781617295362；本档横跨 ✅ 焦点"controlling state mutations"的结构侧延伸
>   与全书收束段。
> - ⚠️ 章节推定：主题带（函数式数据结构 → 深不可变更新/Lenses → Future 并行概览 →
>   纯函数测试 → Functor/Monad 封顶）按 00 档"Ⅲ 进阶/Ⅳ 类型类线"记忆推定；
>   原书是否讲 Lens、讲到何种深度，**待证**——本档内容以通行知识复演，非逐字引书。
> - 🔧 微实验：未经 kotlinc 实测，标 🔧；`kotlin.lenses` KEEP 状态为 00 档登记的待查项 ⚠️。
>
> 上一档 [05-递归-TRO-惰性与Memoization.md](05-递归-TRO-惰性与Memoization.md)；本档为目录末档。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话定义 |
|---|---|---|
| 焦点/透镜 | Lens | "读一个深字段 + 以更新该字段的方式写回新副本"的一对本原操作 |
| 深拷贝更新 | immutable deep update | `a.copy(b = a.b.copy(c = ...))` 链——data class `copy` 只到一层的痛 |
| 组合 | lens composition (`l1 + l2` / `andThen`) | 小透镜拼大透镜，与 01 档函数组合同一代数 |
| 持久化结构 | persistent data structure | 04 档概念的结构化展开：cons List/树，版本共享存储 |
| 未来 | Future / Promise | 异步结果的容器；`map/flatMap` 使其可组合——本书年代线（⚠️ 以 KiA2e 协程为准绳降权） |
| 属性测试 | property-based testing | 纯函数的红利：随机输入验证恒等式，无需 mock 世界 |
|  functor / monad | Functor / Monad | "可 map 的结构"/"可 andThen 的结构"的统一接口——全书各档类型的封顶（Kotlin 无 typeclass，只能接口化模拟 🔧⚠️） |

## 复演：渐进重构叙事（本档演进链：深不可变更新之痛）

同一棵"公司→部门→员工→薪资"嵌套树，从手写拷贝链改到 Lens 代数（⚠️ 情节复演，非逐字引书）：

**第 0 态——可变直达**（04 档第 0 态病灶的嵌套放大版）：

```kotlin
company.departments[2].employees[5].salary += 1000.0
// 五层可变共享：谁还引用着旧 employee？无人知晓，无处审计
```

**第 1 态——copy 俄罗斯套娃**（消灭原地改写，新增可读性灾难）：

```kotlin
val e = company.departments[2].employees[5]
val e2 = e.copy(salary = e.salary + 1000.0)
val d = company.departments[2].copy(employees =
    company.departments[2].employees.replaceAt(5, e2))
val c2 = company.copy(departments = company.departments.replaceAt(2, d))
// 每深一层，表达式长度近乎翻倍——04 档预告的痛点正式现身
```

**第 2 态——Lens 抽象：把"读写对"升格为值**：

```kotlin
data class Lens<A, B>(
    val get: (A) -> B,
    val put: (A, B) -> A,
) {
    fun <C> andThen(l: Lens<B, C>): Lens<A, C> =                 // 组合即代数
        Lens({ a -> l.get(get(a)) }, { a, c -> put(a, l.put(get(a), c)) })
    fun modify(f: (B) -> B): (A) -> A = { a -> put(a, f(get(a))) }
}
val employees = Lens<Company, List<Employee>>({ it.departments }, { c, d -> c.copy(departments = d) })
val raise: (Company) -> Company = idx(2).andThen(emp(5)).andThen(salary).modify { it + 1000.0 }
// 读写各写一次，此后无限复用——与 02/03 档"组合子齐套"同一节奏
```

**第 3 态——现实核查**：手写 Lens 在 Kotlin 无类型类、无操作符之舞的语境下样板仍重；
Arrow `optics` 是工业替代；Kotlin 官方 `kotlin.lenses` KEEP 状态 ⚠️（00 档登记待查，
本仓不写死）；索引/存在性修饰（`idx`、`filter`）超出纯 Lens 表达力，属 Traversal 领地——
Saumont 式叙事在此停步是诚实而非缺陷。

## 并行段概览（⚠️ 年代早，按 00 档降权）

- 本书 Future 线：`Future<A>` ≈ `() -> Either<Throwable, A>` 的惰性/异步对偶，
  `map/flatMap` 组合子与 02/03 档同型；`recover/fallback` 与 Either 线同型——
  **读法：把它当 Either 叙事的时间维_extension_，而非并发教程**。
- 2019 前的 `java.util.concurrent` 口径（线程池/回调地狱规避） today 应整体让位于
  structured concurrency（KiA2e / kotlinx.coroutines 为准绳 ⚠️ 本仓预设立场，见 00）。
- 不可变数据在并行的红利（04 档）在本档回收：无共享可变 ⇒ 组合子链天然可交错执行。

## 纯函数测试段（封顶视角）

- 纯函数=输入→输出的表：无需 mock、无需环境搭建，**表格驱动+属性测试**双打法；
  Option/Either/Try 线让"失败"也在表内（断言 `Left(InsufficientFunds(...))` 即可）。
- Functor/Monad 封顶：02 Option、03 Either、05 TailCalls、本档 Future 共享同一对操作
  （`map` + `andThen`）——统一命名的收益=一条律（结合律/幺元律）四处通用；
  Kotlin 只能以接口+扩展函数模拟 typeclass，天花板观察位（00 档Ⅳ）。

## Java / C++ 对照

- **Java**：`Optional/CompletableFuture` 各自有 map/flatMap，但无统一 Functor 抽象
  （泛型高种类问题 HKT 缺席）；Lens 对应物是 AutoValue/RecordBuilder 的 wither——
  生成代码换类型安全。
- **C++**：`std::optional::transform`（C++23）、`std::expected` 同理，各家各自为政；
  Lens 文化在 C++ 几乎不存在——值语义+`const` 让"原地改局部"反而合规，
  FP 动机（共享可变之痛）在 C++ 以 RAII/所有权另解。
- **测试**：JUnit5 `@ParameterizedTest` 对表格驱动；Catch2 的 `GENERATE` 是属性测试雏形。

## 🔧 微实验（未实测）

```kotlin
fun main() {
    // 实验 A：证明第 2 态与第 1 态等价：
    val c3 = raise(company)
    println(c3.departments[2].employees[5].salary == company.departments[2].employees[5].salary + 1000.0) // true 🔧
    println(company.departments[2].employees[5].salary)   // 旧版本纹丝不动——04 档断言的嵌套版
    // 实验 B： Lens 律检查：andThen 满足结合律（构造三镜两路复合比对 get/put 行为一致）
    // 运行：kotlinc lens.kt -include-runtime -d lens.jar && java -jar lens.jar
}
```

预期观察：`copy` 套娃可机械化生成（故工业界交给注解处理器/Arrow），手写 FP 在 Kotlin
的"教学成本/工程成本"剪刀差正是本档结论。🔧

## 权衡与本仓裁决预告

- **优点**：深更新可组合、可复用、可测试；Future/Either/Option 同型操作=封顶统一。
- **缺点**：Lens 样板在 Kotlin 无语法加持；并行段已过时（降权 ⚠️）；Monad 讲完也改变不了
  Kotlin 缺 HKT 的事实。
- 00 档"理论步子更大"的判词在本档兑现场：读完 01–06，若 Functor/Monad 段读感好于
  FPIK 对应章，则"讲解手感取本书"成立，回写 00 裁决。

## 互链与自测

- 上一级：[00-总览与阅读地图.md](00-总览与阅读地图.md)；上一档 05；本目录末档。
- 跨书：Lens 痛点 ↔ [../Effective_Kotlin/](../Effective_Kotlin/) 数据类条款；
  Future 降权依据 ↔ KiA2e 协程线。
- **读完自测**：① `andThen` 的组合方向与函数组合 `andThen` 一致吗，为什么？
  ② 第 1 态为何不可接受而第 2 态可读——指出表达式长度的渐近差异；
  ③ 说出 Option/Either/TailCalls/Future 共享的操作子对与需满足的律。

## 中英对照表（本档回收）

| 中文 | 英文 | 备注 |
|---|---|---|
| 读写对 | getter/setter pair（纯函数版） | Lens 的 put 不改原物，返回新副本 |
| 遍游 | traversal | Lens 的推广：0..n 焦点，超本档范围 |
| 结构化并发 | structured concurrency | 本档并行段的当代替代口径 |
| 高种类类型 | higher-kinded type (HKT) | Kotlin 缺席=Functor 接口化的天花板根因 |
