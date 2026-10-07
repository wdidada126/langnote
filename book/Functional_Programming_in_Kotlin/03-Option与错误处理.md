# 03 · Option 与错误处理

> 章目凭主题推定，购书后销账 ⚠️（完整章目录未获；对应 [00 总览](00-总览与阅读地图.md)
> "错误处理段"前半：Option → 衔接 Kotlin `Result` 与 sealed 惯用法）。
> 目标书 *Functional Programming in Kotlin*，Apress 2021；⚠️ 作者/ISBN 未直证。
>
> **三态标注**：✅ Kotlin 语言事实（官方文档口径）｜⚠️ 书中位置推定｜🔧 自写代码未实测。

## 概念与机制

**Option 的本质**：把"可能没有值"编码进**类型**，替代 null 哨兵。⚠️ 推定书中会自定义
`Option<A>`（sealed class：`Some(a)` / `None`）并配 map/flatMap/getOrElse——因为
Kotlin 语言本身**没有 Option 类型**✅，标准库对应物是**可空类型 `A?`** 加上作用域函数。

Kotlin 可空体系的✅事实口径：

- `A? = A or null`：null 是类型系统的成员而非任意引用的隐式成员；非空引用赋 null 编译失败。
- 安全调用 `?.`、Elvis `?:`、非空断言 `!!`（后者是把检查交还运行期的逃生舱）、
  智能转换（`if (x != null)` 分支内 x 收窄为 `A`）。
- `let/run/with/also/apply`✅：`x?.let { f(it) }` 就是 Option 的 map 惯用形态。

**`A?` 与 Option 的表达力差**（本档核心观察点⚠️书中立场推定）：

| 维度 | `A?` | Option/Either 风格 |
| --- | --- | --- |
| 缺失原因 | 无（null 单值，原因丢失） | 需另配 Either 类承载（见 [04](04-Either与验证.md)） |
| 可组合性 | `?.` 链在深嵌套时可读性塌 | map/flatMap 显式、可换 Monad 律推理 |
| 与 Java 互操作 | null 双向流动，类型边界撒谎风险✅ | 包一层即隔离 |
| 工程惯例 | Kotlin 官方推荐直接可空✅ | 学院派类型体操，00 档裁决：**不与工程规范混背** |

✅ `kotlin.Result<T>`：runCatching 产出的"值或异常"封装，`isSuccess/isFailure`、
`getOrNull`。注意它曾是@ExperimentalStdlibApi（✅ 1.5 起稳定），且**不能用作普通函数返回
类型之外的多种位置**——历史上有一批使用限制✅，工程口径仍以 try/catch + 可空为主。

## 成对代码：命令式 → 函数式改写

🔧 自写未实测。场景：配置查询链，任一缺失即无结果。

```kotlin
// 命令式（Java 风）：层层判空，NPE 阴影
fun hostImperative(m: Map<String, Map<String, String>>): String {
    val net = m["server"]
    if (net == null) return "localhost"
    val h = net["host"]
    if (h == null) return "localhost"
    return h
}
```

```kotlin
// Kotlin 惯用可空链（工程口径 ✅ 推荐形态）
fun host(cfg: Map<String, Map<String, String>>): String =
    cfg["server"]?.get("host") ?: "localhost"

// 学院派 Option（⚠️ 推定书中形态，自建以对接 04 的 Either）
sealed class Option<out A> {
    data class Some<out A>(val value: A) : Option<A>()
    object None : Option<Nothing>()
}
fun <A> optionOf(a: A?): Option<A> = if (a == null) Option.None else Option.Some(a)
fun <A, B> Option<A>.map(f: (A) -> B): Option<B> =
    when (this) { is Option.Some -> Option.Some(f(value)); is Option.None -> Option.None }
fun <A, B> Option<A>.flatMap(f: (A) -> Option<B>): Option<B> =
    when (this) { is Option.Some -> f(value); is Option.None -> Option.None }
fun <A> Option<A>.getOrElse(d: () -> A): A =
    when (this) { is Option.Some -> value; is Option.None -> d() }

fun hostO(cfg: Map<String, Map<String, String>>): String =
    optionOf(cfg["server"]).flatMap { s -> optionOf(s["host"]) }.getOrElse { "localhost" }
```

两版结果等价；可空链短，Option 链**把"缺失"升为可推理的代数对象**，为后续接 Either
铺路⚠️（推定书中以此为进入 04 的动机）。

## Java / C++ 对照

| 主题 | Kotlin ✅ | Java ✅ | C++ ✅ |
| --- | --- | --- | --- |
| 缺失值编码 | `A?`（语言级） | `Optional<A>`（库级， java.util） | `std::optional<A>`（C++17，值语义） |
| map/flatMap | 无内建，`?.let` 手写 | `Optional.map/flatMap/orElseGet` | 无标准 map；`transform`(C++23) 仅一元 |
| 缺失原因 | 不区分 | 不区分（Optional 无错误位） | `nullopt` 同样无原因 |
| 空指针错 | 编译期挡非空赋值 | 运行期 NPE / Optional 违规抛 `NoSuchElementException` | `*空optional` 未定义行为 |
| 原型出处 | — | Scala `Option` 影响下的 2014 设计 | `optional` 设计文档常引 Scala 谱系 |

对 C++20 档读者：`std::variant<std::monostate, A>` ↔ `Option<A>` 的编码等价、
`std::optional` ↔ `Some/None` 更贴；差别在于 C++ 拿不到 `match+when 穷尽`✅ 的语言级
编译器助力（`std::visit` 手写 overload 集）。

## 🔧 微实验设计

单文件 `ch03.kt`：

1. **律检验**：对自建 Option 验证 `flatMap(m)(f).map(g) == flatMap(m)(f andThen g)` 与
   left/right identity——三行 `check` 断言，坐实 Option 是 Monad 的最小样本。
2. **可空链 vs Option 断链对比**：构造三级缺失的 Map，分别跑两版，打印等价结果。
3. **runCatching 现场**：`runCatching { "x".toInt() }.getOrElse { -1 }` 与
   `toIntOrNull()` 对比，记录 `Result` 与 Option 的定位差（异常携带 vs 值携带✅）。
4. **逃生舱代价**：故意写 `!!` 于可空链末端，观察 NPE 栈，作为"非空断言=把编译期问题
   退货给运行期"的实测注脚。

## 核心概念中英对照

| 英文 | 中文 | 一句话 |
| --- | --- | --- |
| Option type | 选项类型 | "有值/无值"二态的代数编码 |
| nullable type | 可空类型 | Kotlin 的 `A?`，null 入类型 |
| safe call operator | 安全调用 | `?.`，接收者空则整链短路 |
| elvis operator | Elvis 运算符 | `?:`，空值兜底 |
| smart cast | 智能转换 | 判空分支内类型自动收窄 |
| scope functions | 作用域函数 | let/run/with/also/apply |
| sentinel value | 哨兵值 | 用特殊值（-1/null）代指"没有"的反模式 |
| failure encoding | 失败编码 | 把失败信息放进类型系统的做法 |
| `kotlin.Result` | 结果类型 | runCatching 的 值-or-异常 封装✅ |
