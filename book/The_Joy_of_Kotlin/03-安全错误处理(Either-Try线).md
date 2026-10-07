# 03 · 安全错误处理：Either / Try 线（本仓专题划分，非原书章名 ⚠️）

> **三态头**
> - ✅ 已证书目事实：*The Joy of Kotlin*，Pierre-Yves Saumont，Manning，2019-04，
>   ISBN 9781617295362；Manning 页四焦点之 "**safe error management**" 对应本档。
> - ⚠️ 章节推定：本档主题带（异常之弊 → Result/Either → Try → 偏函数+fallback 组合 →
>   验证/累加语义）按 Manning 描述+记忆推定，不冒充原书章名。Either 的左右约定
>   （`Either<E, A>` 左=错误、右=成功，right-biased）按通行惯例书写，原书是否同向 ⚠️ 待核。
> - 🔧 微实验：未经 kotlinc 实测，标 🔧。
>
> 上一档 [02-处理可选数据(Option线).md](02-处理可选数据(Option线).md)；下一档 [04-状态变更控制与不可变性.md](04-状态变更控制与不可变性.md)。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话定义 |
|---|---|---|
| 异常 | exception (checked/unchecked) | 用**非常规控制流**传播失败；签名不诚实（Saumont 主要批判点） |
| 结果类型 | Result / Either<E, A> | 把"成功或失败"编码进返回类型；失败成为**值**而非跳转 |
| 右偏 | right-biased | `map/flatMap` 只对 Right 生效、Left 原样穿透——Either 作为 Monad 的通行取向 ⚠️ |
| 尝试 | Try<A>（≈ `Either<Throwable, A>`） | 专装"异常型失败"的 Either 特化；捕获与传播合一 |
| 偏函数（复现） | partial function `A -> Either<E, B>` | 02 档的 Option 版在此升级为"带原因的偏函数" |
| 回退 | fallback / orElse / recover | 失败时用备选继续；Either 链的安全出口 |
| 验证累加 | applicative validation（对照位） | 收集**全部**错误而非短路第一个——Either 单体链的反面需求 |

## 复演：渐进重构叙事（本档演进链）

同一棵 JSON 解析树，从 `try/catch` 金字塔改到 Either 管道（⚠️ 情节复演，非逐字引书）：

**第 0 态——异常金字塔**（坏在：控制流分叉不可见、吞错容易、可组合性为零）：

```kotlin
fun parseAge(json: String): Int =
    try {
        try jsonJsonRoot(json).obj("user").num("age").toInt()   // 嵌套 try 只是缩影
        catch (e: NullPointerException) throw RuntimeException("missing user", e)
    } catch (e: NumberFormatException) { -1 }                    // -1 哨兵值：类型再次说谎
```

**第 1 态——异常收编为值：Try**（消灭的 effect：不受签名约束的控制流跳转）：

```kotlin
sealed class Try<out A> {
    data class Success<out A>(val get: A) : Try<A>()
    data class Failure(val exception: Throwable) : Try<Nothing>()
}
fun <A> attempt(f: () -> A): Try<A> =
    try { Try.Success(f()) } catch (e: Throwable) { Try.Failure(e) }
// 签名即事实：可能炸的函数返回 Try，catch 只在边界做一次
```

**第 2 态——失败也需要语义：Either**（Try 的失败只有 Throwable；业务错误想要自己的类型）：

```kotlin
sealed class Either<out E, out A> {
    data class Left<out E>(val get: E) : Either<E, Nothing>()
    data class Right<out A>(val get: A) : Either<Nothing, A>()
}
fun age(json: String): Either<ParseError, Int> =
    attempt { rawAge(json) }                    // Try<Raw>
        .toEither { ParseError.IO(it) }
        .andThen { parseInt(it) }               // Either<ParseError, Int> 继续链
```

**第 3 态——组合子齐套：map / andThen / fallback**：

```kotlin
fun <E, A, B> Either<E, A>.andThen(f: (A) -> Either<E, B>) = when (this) {
    is Left -> this; is Right -> f(get) }        // 短路传播，但留在类型里
fun <E, A> Either<E, A>.fallback(fb: () -> Either<E, A>) = when (this) {
    is Right -> this; is Left -> fb() }
// 解析链 = andThen 串接；默认值策略 = fallback 外挂——异常 handler 全部失业
```

**第 4 态——语义裂缝现身**：多字段校验时 Either 链只报**第一个**错；要全量错误清单，
需要"并行累加"的另一套组合（applicative/validate，⚠️ 原书推进到哪一步待证）。
本档在此立存照：单体链 ≠ 万能，认清表达力边界。

## Java / C++ 对照

- **Java**：checked exception 是"用签名说谎的反面极端"——它说了谎话之外的真话却毁掉
  组合性（泛型里塞不进 throws）；Java 8 `Optional` 后社区转向值语义错误处理，
  `CompletableFuture.exceptionally` 是 Try 的运行期表亲。
- **C++**：异常在嵌入式/游戏业长期被 `-fno-exceptions` 禁用；`std::error_code`（C++11）
  与 **`std::expected<T, E>`（C++23）** 是 Either 的标准化直系——`and_then/or_else/transform`
  组合子与本档第 2/3 态几乎同名，可作互证。
- **Kotlin**：语言层只有 unchecked 异常，等于"默认说谎"；因此 Saumont 式 Either 教学在
  Kotlin 的边际收益比 Java 更大（⚠️ 推定）。

## 🔧 微实验（未实测）

```kotlin
fun main() {
    val bad = age("{ not json")
    println(bad)                       // Left(...)：错误在场但程序未跳转 🔧
    println(bad.fallback { Right(18) })// Right(18)
    // 实验 B：在 andThen 链中间塞一个抛异常但未包 attempt 的 f，
    // 观察异常直接击穿——Either 不自动捕获，边界收编(attempt)是纪律不是魔法。
    // 运行：kotlinc either.kt -include-runtime -d either.jar && java -jar either.jar
}
```

预期观察：第 0 态改一行代码控制流就变形；第 3 态改的只是**值**——这就是"安全错误管理"
的全部含义：失败可被传递、存储、断言，而不再劫持程序。🔧

## 权衡

- **优点**：签名诚实、可测试（错误是返回值即可断言）、fallback/组合子可代数化推理。
- **缺点**：每个调用点多缩进一层组合子；与协程/`suspend` 的异常文化（CancellationException
  等）需要划界——KiA2e 协程时代用 `runCatching` 的读者注意口径（见 00 的降权 ⚠️）。
- **与 Try 的分工**：外部世界（IO/第三方库）用 Try 收编；内部业务规则用 Either 自定义
  错误代数——两条线在 Saumont 叙事里是**同一演进的两个切面**（⚠️ 概括口径）。

## 互链与自测

- 上一级：[00-总览与阅读地图.md](00-总览与阅读地图.md)；上一档 02；下一档 04。
- 00 档"偏函数+Either 链是本仓最实用段"即指本档第 2→4 态。
- **读完自测**：① `Try` 为什么可以视为 `Either<Throwable, A>` 的特化，反过来为何不行？
  ② 写出"校验 email+age 并返回全部错误"与 Either 链的差异需求说明；
  ③ Java checked exception 与 Either 谁更"签名诚实"，给出论据。

## 中英对照表（本档回收）

| 中文 | 英文 | 备注 |
|---|---|---|
| 左/右 | Left / Right | 错误/成功之约定 ⚠️ 原书同向待证 |
| 收编异常 | attempt / catching / runCatching | Kotlin stdlib 2.6+ 名 `runCatching`，返回 `Result` |
| 短路 | short-circuit | Either 链的失败传播 |
| 回退 | fallback / recover / orElse | 命名各家不同，语义同一 |
