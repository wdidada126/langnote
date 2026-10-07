# 02 · 面向对象：类、接口、委托与 data/value 选型（Recipe 档）

> 对应 *Kotlin Cookbook*（Ken Kousen，O'Reilly，2022；⚠️ ISBN 未直证）OOP 章带
> （类/接口/委托，高价值方向"data vs value class 选型"，见 [00 总览](00-总览与阅读地图.md)）。
> ⚠️ 章目录 403 墙未获：不冒充原书 recipe 编号/英文原标题，标题为中文推定归属。
> 三态头例：`[✅ 官方文档可证语言事实 | ⚠️ recipe 归属推定 | 🔧 未实测]`。
> 仲裁口径延续 00：**条目规范从 [Effective_Kotlin](../Effective_Kotlin/00-总览与阅读地图.md)，
> 即查即用食谱从本书**。

## 核心概念速览（中英对照见尾表）

本章是两本书重叠最重的地带：Moskala 给"该怎么选"的条目裁决，Kousen 给"怎么写出来"的
可抄片段。**选型结论一句话版**：有标识实体用 class、纯字段载体用 data class、
单字段包装用 value class、限定封闭层次用 sealed——每条下面都有代码证据。

---

## R1 · "sealed class 替策略 switch，when 怎么强制我覆盖新分支？"
`[✅ | ⚠️ 归属推定：OOP 章 sealed/多态惯用法 | 🔧]`

**Problem.** Java 加枚举常量要全文搜 switch；Kotlin 有编译器兜底吗？

**Solution.** 🔧

```kotlin
sealed interface Expr {                          // 1.5+ sealed 可修饰 interface ✅
    data class Num(val v: Double) : Expr
    data class Sum(val l: Expr, val r: Expr) : Expr
    object Pi : Expr
}
fun eval(e: Expr): Double = when (e) {           // 表达式 + 全覆盖：无 else ✅
    is Expr.Num -> e.v                           // 智能转换直接给字段 ✅
    is Expr.Sum -> eval(e.l) + eval(e.r)
    Expr.Pi -> Math.PI
}                                                // 新增分支未处理 = 编译错误（无 else 时）
```

```kotlin
fun bad(e: Expr): Int = when (e) {               // 反例：写 else 会把"漏分支"兜掉
    is Expr.Num -> 1
    else -> 0                                    // 规范（Effective）：能用穷尽就别写 else ⚠️ 条目号未核
}
```

**Discussion.** sealed 穷尽性只在**同一编译单元/模块内可见的子类型**上成立 ✅；
sealed interface 允许外部分子实现时不算封闭（规则细节以版本实测为准 🔧）。
`object` 分支在 `is`/`==` 两种写法下语义相同。递归求值这型"数据即树 + when 即解释器"
是本书 OOP 档最典型的口味 ⚠️ 归属推定。

## R2 · "接口默认方法会不会有菱形冲突？"
`[✅ | ⚠️ | 🔧]`

**Problem.** Java 8 default method 的菱形要靠 `Outer.super.method()`，Kotlin？

**Solution.** 🔧

```kotlin
interface A { fun log() { println("A") } }
interface B { fun log() { println("B") } }
class C : A, B {
    override fun log() {                // 必须显式重写 ✅，无继承即无冲突
        A.super.log()                   // Kotlin 语法：InterfaceName.super ✅
        B.super.log()
    }
}
```

```kotlin
class D : A by AImpl()                  // 见 R3，委托后连重写都不用写
object AImpl : A
```

**Discussion.** Kotlin 接口实现默认方法是**运行期特性**（1.4+ 目标 JVM 8 直接映射 Java
default method，旧版本生成 `DefaultImpls` 桥 ✅ 字节码形态以实测为准 🔧）。
"必须重写"这条比 Java 严：Java 遇菱形直接编译错误，Kotlin 允许你重写并自选转发目标 ✅。

## R3 · "组合代替继承具体怎么写？by 委托有什么代价？"
`[✅ | ⚠️ 归属推定：委托章 | 🔧]`

**Problem.** 类越来越像"上帝"，想抽能力出去，装饰器样板代码太多。

**Solution.** 🔧

```kotlin
interface Repository { fun find(id: Long): String; fun save(id: Long, v: String) }
class CachedRepo(val delegate: Repository) : Repository by delegate {   // 全量转发 ✅
    override fun find(id: Long) = delegate.find(id).also { println("hit $id") }
}
```

```kotlin
class Audit : Repository {                      // 手写装饰器：by 表达不了的"环绕"
    private val base = ...                       // 略
    override fun save(id: Long, v: String) { /* 前置校验 */ }
}
```

**Discussion.** `by` 生成的转发方法是**public 虚调用**：委托对象生命周期长于被委托接口引用
没问题，但**改 delegate 指向不会生效**（转发绑的是构造时那个对象）✅ 细节以实测为准 🔧。
规范仲裁：Effective Kotlin 主张"优先表达式委托/属性委托，接口实现委托警惕过深包装" ⚠️。
属性委托 `by lazy` 归 [03 章](03-函数Lambda与内联.md) R6。

## R4 · "data class 和 value class 都当包装类型，选哪个？"
`[✅ | ⚠️ 归属推定：OOP 章选型 Recipe（本档主打） | 🔧]`

**Problem.** `UserId(String)` 这种单字段包装，data class 一行搞定，为什么要 value class？

**Solution.** 🔧

```kotlin
@JvmInline
value class UserId(val raw: String)             // 1.5+ 稳定 ✅；须显式 @JvmInline（1.9 规则）✅
fun render(u: UserId) = "#${u.raw}"

data class Money(val cents: Long, val currency: String)  // 多字段 → 仍然 data class
```

```kotlin
// 反例：value class 约束
@JvmInline value class Bad(val a: Int, val b: Int)  // ❌ 编译错：主构造只能一个 val ✅
// value class 不能：被继承、有 init 块、var 属性、可空数组底层类型特例等 ✅（清单以版本为准 🔧）
```

**Discussion.** 选型表 ⚠️ 口径综合两书 + 官方文档：

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 单字段防"把 Name 传给 Id"的类型包装 | value class | 运行期擦除为底层类型，零装箱 ✅ |
| 多字段值载体、要 equals/copy/解构 | data class | componentN 与结构相等 ✅ |
| 有标识、实体随时间变、要引用相等 | 普通 class（手写 equals 或干脆不写） | data class 的 equals 按字段 ⚠️ Effective 反对实体用 data |
| 需要继承层次 | 都不是（data 不能开 class；value 不能继承） | ✅ |

value class 的代价要讲透：**函数签名在 JVM 上被 mangle**（参数名带后缀、返回类型可能是底层
类型或装箱），Java 侧调用混乱见 [06 章](06-IO序列化与JVM混编.md)；可空 `UserId?` 时又装箱 ✅。
"data vs value"是 00 骨架表点名的本档主打方向 ⚠️。

## R5 · "data class 能继承吗？我想给密封层次加点共享行为"
`[✅ | ⚠️ | 🔧]`

**Problem.** `data class Foo : Bar()` 报错，怎么办？

**Solution.** 🔧

```kotlin
abstract class Base { abstract val id: Long }
data class Row(override val id: Long, val name: String) : Base()   // data 可继承抽象类 ✅
// data class D2 : D1(...)                                          // ❌ data 不能继承普通类 ✅
sealed interface Ev { data class Click(val x: Int) : Ev }           // 常规解法：接口承接 ✅
```

```kotlin
// "复制时保留子类类型"的补丁惯用法 🔧
interface Copyable<T> { fun withId(id: Long): T }
data class User2(val id: Long, val name: String) : Copyable<User2> {
    override fun withId(id: Long) = copy(id = id)                   // 返回静态类型，够用
}
```

**Discussion.** 规则：data class 可实现接口、可继承抽象类（1.2 起 ✅），**不能继承具体类** ✅；
`copy()` 返回类型永远是本类，不做多态 copy——这是"协变 copy"语言的普遍缺口 ⚠️。
规范仲裁：Effective Kotlin 明确"别指望 data class 参与继承树的结构相等" ⚠️ 条目号未核。

## R6 · "伴生对象到底是不是 static？"
`[✅ | ⚠️ | 🔧]`

**Problem.** `companion object { val DEFAULT = ... }` 在 Java 里怎么拿到？和 object 单例区别？

**Solution.** 🔧

```kotlin
class Config {
    companion object Factory {                    // 可命名 ✅
        const val MAX = 100                       // const：真 static field，仅编译期常量 ✅
        @JvmStatic fun load() = Config()          // @JvmStatic：Java 见 Config.load() ✅
        @JvmField val GLOBAL = java.util.concurrent.atomic.AtomicInteger() // 避免 .INSTANCE ✅
    }
}
// Java 侧默认形态：Config.Factory.INSTANCE.load() / Config.Factory.Companion（无名字时）✅ 细节 🔧
```

**Discussion.** companion 是**单例对象实例**（有状态、可实现接口、可作接收者），`const`/`@JvmStatic`
才是静态视图 ✅。与顶层 `object` 的区别只在作用域归属；两者都可 `by` 实现接口 ✅。
Java 互操作注解三件套（`@JvmStatic/@JvmField/@JvmName`）完整速查在 [06 章](06-IO序列化与JVM混编.md) R5。

## R7 · "扩展函数能覆盖成员吗？为什么我的 toString 扩展没生效？"
`[✅ | ⚠️ | 🔧]`

**Problem.** 给第三方类加 `fun Any.describe()`，有同名成员时被静默忽略？

**Solution.** 🔧

```kotlin
fun Any.describe() = "ext:${hashCode()}"
class Named { fun describe() = "member" }
val s = Named().describe()          // "member"：成员永远赢 ✅
// 扩展是静态解析（按声明类型分派），没有虚语义 ✅
fun <T> List<T>.secondSafe(): T? = getOrNull(1)   // 泛型接收者 + 可空返回，扩展的正用
```

**Discussion.** 扩展=编译期 `ExtensionsKt.describe(list)` 静态调用 ✅，这带来两个后果：
可空接收者扩展（`fun String?.orBlank()`）内部要自己判 null ✅；写库时别用扩展"伪造多态"，
封闭层次用 sealed+when、开放体系用接口——规范位从 Effective ⚠️。

## R8 · "object、companion、顶层函数……Kotlin 里没有 static 怎么组织工具类？"
`[✅ | ⚠️ | 🔧]`

**Problem.** Java `public final class Utils { private Utils(){} static ... }` 的 Kotlin 等价？

**Solution.** 🔧

```kotlin
// 方案 A：文件级顶层函数（Kotlin 社区首选 ⚠️ 规范从 Effective）
// StringUtils.kt
fun slugify(s: String) = s.lowercase().replace(Regex("[^a-z0-9]+"), "-")

// 方案 B：无状态单例
object Slugger { fun of(s: String) = slugify(s) }        // 可实现接口、可作 lazy 委托目标 ✅
```

```kotlin
// Java 消费方看到的类名：StringUtilsKt.slugify(...)（文件+"Kt"）✅ → @file:JvmName 见 06 章 R3
```

**Discussion.** 三种"静态感"载体的分工：顶层函数（最惯用）、`object`（需要命名空间/接口身份）、
companion（依附某类型的成员）。选型 ⚠️ 是口味问题，官方文档只陈述机制 ✅。

## R9 · "委托属性由 lazy 起家，还能干嘛？"
`[✅ | ⚠️ 归属推定：委托章属性委托 | 🔧]`

**Problem.** 除了 `by lazy`，委托属性是不是玩具？

**Solution.** 🔧

```kotlin
class Session(val id: String) {
    var name: String by NameStore()                // 属性存取被接管 ✅
}
class NameStore {
    private val map = mutableMapOf<String, String>()
    operator fun getValue(thisRef: Any?, prop: kotlin.reflect.KProperty<*>) =
        map[prop.name] ?: ""
    operator fun setValue(thisRef: Any?, prop: kotlin.reflect.KProperty<*>, v: String) {
        map[prop.name] = v
    }
}
val heavy: List<String> by lazy { readLines() }    // 线程安全默认 SAFE 模式 ✅
```

**Discussion.** `getValue/setValue` 是 `operator` 约定 ✅；标准库另有
`Delegates.observable/vetoable` ✅。`by lazy` 的锁模式（`LazyThreadSafetyMode`）与
"可空 var 不能用 lateinit、初始化一次用 lazy"是高频口诀——`lateinit` 陷阱在
[05 章](05-空安全与异常Result.md) R3。

## R10 · "init 块、属性初始化器、构造参数默认值，执行顺序是什么？"
`[✅ | ⚠️ | 🔧]`

**Problem.** 排查 NPE 时需要确切顺序，Java 直觉对吗？

**Solution.** 🔧

```kotlin
open class Base { init { println(1) } }            // 父类 init 先跑
class Derived(val v: Int) : Base() {
    val calc = v * 2                               // 子类属性初始化在父 init 之后
    init { println(3) }                            // 整体顺序：1 → 2(属性隐式) → 3 ✅ 逐字输出 🔧
}
```

**Discussion.** 规则可证：主构造参数 → 父类初始化（含父 init）→ 子类属性与 init **按书写顺序** ✅。
坑：父类 init 调用被子类重写的方法时，子类属性还没初始化（Java 同款病，final 处方也同款）✅。
这条是"规范从 Effective"覆盖最严的条目（别在构造期调用可重写成员）⚠️。

---

## 本档核心概念中英对照表

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 密封层次 | sealed class/interface | 编译期封闭的类型和，配穷尽 when |
| 智能转换 | smart cast | is 检查后同表达式免强转 |
| 接口实现委托 | interface implementation by | `class C : I by d` 全量转发 |
| 属性委托 | property delegation | getValue/setValue operator 约定 |
| 数据类 | data class | 结构相等/copy/componentN 自动生成 |
| 值类（内联类） | value (inline) class | 单字段包装，JVM 上擦除为底层类型 |
| 伴生对象 | companion object | 单例语义，非 static；@JvmStatic 才像 |
| 扩展函数 | extension function | 静态解析，成员永远优先 |
| 延迟初始化 | lazy initialization | by lazy（线程安全默认）vs lateinit |
| 构造初始化顺序 | initialization order | 父先于子，属性与 init 按书写序 |

衔接：lambda/高阶函数侧去 [03](03-函数Lambda与内联.md)；value class 的 JVM 表征与互操作补丁去
[06](06-IO序列化与JVM混编.md)；错误建模的 sealed 用法去 [05](05-空安全与异常Result.md) R9。
