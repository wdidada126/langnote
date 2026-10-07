# 02 · 处理可选数据：Option 线（本仓专题划分，非原书章名 ⚠️）

> **三态头**
> - ✅ 已证书目事实：*The Joy of Kotlin*，Pierre-Yves Saumont，Manning，2019-04，
>   ISBN 9781617295362；Manning 页四焦点之 "**handling optional data**" 对应本档。
> - ⚠️ 章节推定：本档主题带（空值之坑 → 自造 Option → map/flatMap/andThen → 与可空类型对照）
>   按 Manning 描述+记忆推定；Saumont 大概率**手写 sealed Option** 以教学而非用库（⚠️ 推定），
>   不冒充原书章名与小节号。
> - 🔧 微实验：未经 kotlinc 实测，标 🔧。
>
> 上一档 [01-函数式方法入门.md](01-函数式方法入门.md)；下一档 [03-安全错误处理(Either-Try线).md](03-安全错误处理(Either-Try线).md)。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话定义 |
|---|---|---|
| 十亿美元的错误 | The Billion Dollar Mistake | Hoare 对 null 的著名忏悔；本档全链的动机 |
| 可空类型 | nullable type (`T?`) | Kotlin 语言层的 null 安全：编译期检查，但组合性差 |
| 选项类型 | Option / Optional | 用**类型**而非特殊值表达"可能没有"：`Some(a)` 或 `None` |
| 映射 | map | 有值则变换，无值则原样传播 `None`——免写 if 的第一件套 |
| 平铺/链式 | flatMap / andThen（Saumont 命名 ⚠️） | 变换函数本身返回 Option 时的组合，防 `Option<Option<A>>` 套娃 |
| 兜底 | getOrElse / getOrElseLazy | 把 Option 落回默认值的安全出口 |
| 偏函数 | Partial Function（`A -> Option<B>`） | Saumont 的定义：定义域不覆盖全部输入的函数；与 03 档 Either 线交汇 |

## 复演：渐进重构叙事（本档演进链）

同一段"从用户档案取邮编拼运费"的坏代码，逐格推进（⚠️ 情节复演，非逐字引书）：

**第 0 态——null 接力**（坏在：每层都可能爆 NPE，且类型不说真话）：

```kotlin
fun zipCode(u: User): String? = u.address?.zip          // 就算用 ?. 也仍是 String?
fun postage(u: User): Double {
    val z = zipCode(u)
    if (z == null) return 0.0                            // 每加一层可空，if 翻倍
    return rate(z) * weight(u)
}
```

**第 1 态——把"没有"升格为类型**（自造教学版 Option，Saumont 风）：

```kotlin
sealed class Option<out A> {
    object None : Option<Nothing>()                       // 注意：None 复用 Nothing 协变
    data class Some<out A>(val get: A) : Option<A>()
}
fun <A, B> Option<A>.map(f: (A) -> B): Option<B> =
    when (this) { is None -> None; is Some -> Some(f(get)) }
```

**第 2 态——链式组合**（邮编→费率→金额，全在 Option 语境里）：

```kotlin
fun <A, B> Option<A>.andThen(f: (A) -> Option<B>): Option<B> =   // 即 flatMap
    when (this) { is None -> None; is Some -> f(get) }
fun postage(u: User): Option<Double> =
    zipOption(u)                                   // Option<String>
        .andThen { z -> rateOption(z) }            // Option<Double>
        .map { r -> r * weight(u) }
// 无值时全程静默传播，一个 if 都没写
```

**第 3 态——偏函数视角**（本档与 03 档的桥）：`rateOption: String -> Option<Double>`
就是 Saumont 所谓偏函数——用 `Option` 把"可能无定义"**写进签名**。
运费链就此成为"偏函数的合法复合"：偏函数复合偏函数，仍是纯函数。

## Java / C++ 对照

- **Java `Optional`**（`java.util.Optional`，2016 起主流）：`map/flatMap/orElse` 一一对应
  第 2 态；但 Java 社区长期滥用 `Optional.get()` 当解包锤，效果等于 `!!`。
  Kotlin 可空类型 + `?.`/`?:` 提供的语法糖是 Java 没有的——Saumont 仍教手写 Option，
  意在**类型构造与函数组合**的心智模型而非日常写法（⚠️ 推定）。
- **C++ `std::optional`**（C++17）：值语义、无堆分配，`and_then/or_else` 到 C++23 才补上
  单体操作；对照点：C++ 用 `has_value()/value()`，爆错路径是 `bad_optional_access` 异常——
  等于"Option 退回到异常世界"。
- **Kotlin 原生 `T?`**：与 Option 是**同一问题的两套代数**——`T?` 走语言内建（零装箱、
  智能转换），Option 走类型系统（可 `map` 组合、可放进泛型管线）。老手裁决：业务代码用 `T?`，
  需要高阶组合/偏函数建模时借 Option 视角。

## 🔧 微实验（未实测）

```kotlin
fun main() {
    val xs = listOf("1", "abc", "3")
    val opts = xs.map { it.toIntOrNull().toSomeOption() }      // 教学版转换
    println(opts.filterIsInstance<Option.Some<Int>>().size)    // 期望 2 🔧
    // 实验 B：给 map 传一个抛异常的 f，观察 Option 不捕获异常——
    // "无值"≠"出错"，这正是 03 档 Either/Try 补位的裂缝。
}
```

预期观察：Option 只传播"缺失"，不传播"失败原因"——缺失是无因的，失败必须留话。🔧

## 权衡与本仓预设立场

- **优点**：把 null 检查变成类型系统责任；`andThen` 链让"可空数据流"可测试、可组合。
- **缺点**：每个值多一层对象（`Some` 装箱）；与 Kotlin 内建可空类型**双轨并存**是认知税；
  只带 `None` 不带原因——错误处理力不从心（→ 03 档）。
- **反方立场**：Dreyfus 学派批评 `Maybe`  monadic 化会让代码变成"管道涂鸦"；Saumont 的
  渐进叙事恰好在第 2→3 态展示了边界——链一长就该问"这是缺失还是错误？"

## 互链与自测

- 上一级：[00-总览与阅读地图.md](00-总览与阅读地图.md)；上一档 01；下一档 03。
- 姊妹书对照：FPIK 的 `Option` 讲法走库化（Arrow），本档走手写教学——同一代数两条路。
- **读完自测**：① 为什么 `None` 可以声明成 `Option<Nothing>`？（协变 + 无值）
  ② `map.andThen` 与 `andThen.andThen` 哪个能压掉一层 Option？③ 举一个"该用 Either 而非
  Option"的场景（提示：校验失败要回显原因）。

## 中英对照表（本档回收）

| 中文 | 英文 | 备注 |
|---|---|---|
| .some / 无 | Some / None | Arrow 用 `some()/none()`，Kotlin 惯用 `T?` |
| 平铺 | flatMap | 本书语境 Saumont 常名 `andThen` ⚠️ |
| 兜底默认值 | getOrElse / orElse | Java 名为 orElse/orElseGet |
| 空安全传播 | null-safe propagation (`?.`) | Kotlin 语法层，Option 的类型层替身 |
