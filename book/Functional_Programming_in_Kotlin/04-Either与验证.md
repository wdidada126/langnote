# 04 · Either 与验证（Validated 式累积）

> 章目凭主题推定，购书后销账 ⚠️（完整章目录未获；对应 [00 总览](00-总览与阅读地图.md)
> "错误处理段"后半：Either/Validated → sealed class 惯用法衔接）。
> 目标书 *Functional Programming in Kotlin*，Apress 2021；⚠️ 作者/ISBN 未直证。
>
> **三态标注**：✅ Kotlin 语言事实（官方文档口径）｜⚠️ 书中位置推定｜🔧 自写代码未实测。

## 概念与机制

**Either 的动机**：[03](03-Option与错误处理.md) 的 Option/`A?` 只说"没有"，不说"为什么"。
`Either<E, A>` 把失败原因 `E` 也装进类型：左（Left）惯例为错误，右（Right）惯例为成功。
⚠️ 推定书中自建：

```kotlin
sealed class Either<out E, out A> {
    data class Left<out E>(val value: E) : Either<E, Nothing>()
    data class Right<out A>(val value: A) : Either<Nothing, A>()
}
```

Kotlin **没有内建 Either**✅（最接近的是 `kotlin.Result<T>`——但它的错误类型被固定为
`Throwable`✅，丢失了"错误也是领域数据"的自由度；这正是 Either 存在的理由⚠️推定书中
会这样论证）。

**Either vs Validated——错误处理的两条轴**（本档核心区分）：

| 轴 | Either 链（短路） | Validated（累积） |
| --- | --- | --- |
| 语义 | 第一个错即返回 | 跑完全部校验、错误打包返回 |
| 组合结构 | Monad（flatMap） | Applicative（mapN/zip），非 Monad |
| 场景 | 解析→依赖前步结果的流程 | 表单多字段独立校验 |
| Kotlin 现状 | 无内建✅，自建或用 Arrow ⚠️ 本书是否引 Arrow 未证 | 无内建✅，`NonEmptyList` 需自建 |

⚠️ 推定书中 Validated 会配 `Nel<E>`（非空列表）做错误半，用 zip/ap 组合——这是
FP in Scala 谱系（Validated 概念源自 scalaz/cats）的讲法；**谱系映射未直证**。
Kotlin 工程口径✅：实际项目要么 sealed class + when 手写，要么 Arrow；学院派类型体操
不与工程规范混背（00 档对 Effective Kotlin 的裁决延续适用）。

**右投影/双射约定**✅口径：`map` 只作用于 Right，`mapLeft` 作用于 Left；`flatMap` 的
错误类型需可协变合并（`Either<out E, out A>` 中 `Nothing` 子类型技巧承担，见下代码）。

## 成对代码：命令式 → 函数式改写

🔧 自写未实测。场景：注册表单三字段校验。

```kotlin
data class User(val name: String, val age: Int, val email: String)
sealed class FieldError { object BadName : FieldError(); object BadAge : FieldError(); object BadEmail : FieldError() }
```

```kotlin
// 命令式：错误塞布尔/字符串，第一个错后其余检查可能被跳过（或混乱地拼串）
fun validateImperative(name: String, age: String, email: String): String? {
    if (name.isBlank()) return "bad name"           // 只报第一个错
    if (age.toIntOrNull() == null || age.toInt() < 0) return "bad age"
    if (!email.contains("@")) return "bad email"
    return null                                      // null=成功：双重编码，反模式
}
```

```kotlin
// Either 版：短路语义（任一错即返）
fun <E, A, B> Either<E, A>.flatMap(f: (A) -> Either<E, B>): Either<E, B> =
    when (this) { is Either.Left -> this; is Either.Right -> f(value) }
fun <E, A, B> Either<E, A>.map(f: (A) -> B): Either<E, B> =
    when (this) { is Either.Left -> this; is Either.Right -> Either.Right(f(value)) }

fun checkName(s: String): Either<FieldError, String> =
    if (s.isBlank()) Either.Left(FieldError.BadName) else Either.Right(s)
fun checkAge(s: String): Either<FieldError, Int> =
    s.toIntOrNull()?.let { if (it >= 0) Either.Right(it) else Either.Left(FieldError.BadAge) }
        ?: Either.Left(FieldError.BadAge)
fun checkEmail(s: String): Either<FieldError, String> =
    if (!s.contains("@")) Either.Left(FieldError.BadEmail) else Either.Right(s)

fun signupEither(name: String, age: String, email: String): Either<FieldError, User> =
    checkName(name).flatMap { n ->
        checkAge(age).flatMap { a ->
            checkEmail(email).map { e -> User(n, a, e) }
        }
    }                                              // 三错齐犯也只报第一个

// Validated 版：错误累积（Applicative 手搓 zip）
data class Nel<A>(val head: A, val tail: List<A> = emptyList()) {
    val all get() = listOf(head) + tail
    fun combine(o: Nel<A>) = Nel(head, tail + o.all)
}
sealed class Validated<out E, out A> { data class Invalid<out E>(val e: E) : Validated<E, Nothing>()
                                        data class Valid<out A>(val a: A) : Validated<Nothing, A>() }
fun <E, A, B, R> zip(v1: Validated<E, A>, v2: Validated<E, B>,
                     c: (E, E) -> E, f: (A, B) -> R): Validated<E, R> = when {
    v1 is Valid && v2 is Valid -> Valid(f(v1.a, v2.a))
    v1 is Invalid && v2 is Invalid -> Invalid(c(v1.e, v2.e))
    v1 is Invalid -> v1
    else -> v2 as Invalid<E>
}
fun signupValidated(name: String, age: String, email: String)
    : Validated<Nel<FieldError>, User> =            // 三错齐犯报全部 ✅ 语义差所在
    zip(zip(checkName(name).toV(), checkAge(age).toV()) { e1, e2 -> e1.combine(e2) }
            to2 { n, a -> n to a },
        checkEmail(email).toV()) { e1, e2 -> e1.combine(e2) }
        { (n, a), e -> User(n, a, e) }
private fun <A> Either<FieldError, A>.toV(): Validated<Nel<FieldError>, A> =
    when (this) { is Either.Left -> Invalid(Nel(value)); is Either.Right -> Valid(value) }
private fun <A, B, C> Validated<A, Pair<B, C>>.to2() = this // 占位：实际需第二 zip 支持 Pair
```

（Validated 末段为演示骨架，🔧 编译未过可能性存在——微实验第 3 项即为把它跑通并改掉
`to2` 占位；Either 段结构完整可直接跑。）

## Java / C++ 对照

| 主题 | Kotlin ✅ | Java ✅ | C++ ✅ |
| --- | --- | --- | --- |
| 二选一类型 | 无内建✅，sealed 自建 | 无（库：vavr `Either`） | `std::variant<E, A>`（值语义、`std::get/get_if`） |
| 错误携带 | `A?`（无原因）/`Result`（仅 Throwable） | 异常（控制流代价）/ `Optional` 无错误位 | 异常 / 错误码 / `std::expected<E,T>`（C++23） |
| 短路 vs 累积 | 需自建两轨道✅ | 无标准支持 | `expected` 有 `and_then` 链（短路）；无累积内建 |
| 穷尽检查 | sealed + when 编译器强制✅ | 无（visitor 模式手写） | `std::visit` 全分支 overload 集漏则编译错 |

C++ 对照要点：`variant<Error, User>` 在**表示**上等价 Either，但**组合子文化**
（map/flatMap/zip 一套代数）完全缺席；这正是 Kotlin 用接口+扩展能补、C++ 用模板
概念难补的地带（对读 [C++20 概念章](../C++20模板元编程/06-概念和约束.md)）。

## 🔧 微实验设计

单文件 `ch04.kt`：

1. **Either 短路实测**：跑 `signupEither("", "-1", "x")`，断言只回 `BadName`。
2. **Monad 律检验**：Either 的 left identity / right identity / associativity 三条 `check`。
3. **Validated 累积跑通**：补全上文 Pair 版 zip（写 `zip3` 更直白），断言三错输入返回
   `Nel` 含 3 元素——这是"Applicative ≠ Monad"的**可执行**分界（flatMap 若给 Validated
   会丢失累积，写出该证明注释）。
4. **Result vs Either**：同一解析逻辑分别用 `runCatching` 与自建 Either 写，并排打印，
   记录错误类型自由度（Throwable vs 领域类型）差异✅。

## 核心概念中英对照

| 英文 | 中文 | 一句话 |
| --- | --- | --- |
| Either |  Either 类型 | 左错右成的二选一容器 |
| short-circuit | 短路 | 首个失败终止后续计算 |
| error accumulation | 错误累积 | 收集全部失败再返回 |
| Validated / Applicative | 验证态 / 应用函子 | 可并行合并上下文的组合结构 |
| NonEmptyList (Nel) | 非空列表 | 至少一元素的列表，累积错误载体 |
| left-biased | 左投影 | 组合子默认只作用于某一侧的约定 |
| domain error | 领域错误 | 失败原因作为业务数据建模 |
| sealed class | 密封类 | 分支集合编译期封闭，when 穷尽✅ |
| `kotlin.Result` | 结果类型 | 值-or-Throwable 的内建封装✅ |
