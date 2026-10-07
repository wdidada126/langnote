# 02 · 函数与 Lambda

> 三态标注：✅ = 语言事实，以 kotlinlang.org 官方文档口径可证；⚠️ = 书中位置推定
> （目录凭记忆与版次对照推定，购书后销账）；🔧 = 未实测示意代码。
> 书中位置（⚠️ 推定）：1e 约第 5 章 Functions、第 6 章 Working with collections 中
> 的 vararg/infix/局部函数素材、第 8 章 Higher-order functions（lambdas and function
> references）；2e 章号未核实。本册把"函数一等公民 + lambda/闭包 + inline/reified"
> 合并成一条线，协程对 suspend lambda 的依赖（见 [09](09-协程基础与suspend函数.md)）
> 以此为地基。

## 主题机制讲解

### 声明侧：默认参数、命名实参、单表达式函数

- 默认参数值 + 调用点命名实参（`f(x = 1)`），一次消灭 Java 的 telescoping
  overload 金字塔（✅）。对 C++：默认实参 C++ 也有，但 C++ **没有命名实参**
  （提案多年未进）；Kotlin 的命名实参在布尔尾巴 `f(true, true, false)` 可读性上
  是质变。
- 默认参数按声明顺序求值，后面的默认值可引用前面的参数（✅）。与 Java 无对位；
  与 C++ 同（C++ 也顺序求值）。
- 单表达式函数省略大括号与返回类型：`fun abs(x: Int) = if (x < 0) -x else x`（✅）。
- 函数是类型化值：`Int.() -> String`、`(A, B) -> C`；suspend 版本 `suspend (A) -> B`
  是同层的类型构造子（✅，见 08 册）。Java 需 `Function/IntFunction/...` 家族 +
  原始类型特化避装箱；Kotlin 一切皆对象但 `Int` 在泛型位会装箱——这是与 C++ 模板
  零成本抽象的正面对照点（Kotlin JVM 靠 `@JvmName`/专门化部分缓解，Native 后端
  按实参类型单态化 ✅）。

### 调用侧：lambda 语法糖与闭包

- lambda 是 `{ 参数 -> 体 }`；单参数默认名 `it`（✅）。尾随 lambda 移到圆括号外，
  多 lambda 时**只有一个**能外置（✅）——这是 Kotlin "把语句感的块参数放在最后"
  的 DSL 地基，直接对位 C++ 无、Java 无（Java lambda 必须留在括号内）。
- 闭包捕获：可捕获可变局部变量（lambda 内可改写外层 `var`，✅）。语义等价 Java 的
  effectively-final 限制的**解除**；JVM 实现上靠 Ref.ObjectRef 盒子（非 Indy 时代）
  或 `invokedynamic + LambdaMetafactory`（1.5+ 默认，✅）。C++ 的 `&`/`=` 捕获选择
  在 Kotlin 不存在——一律引用捕获，悬垂引用问题改由 GC 消解。
- 非局部返回（non-local return）：`return` 直接退出**定义该 lambda 的外层函数**
  （✅）——只对 inline 调用的 lambda 合法（下文），普通 lambda 用 `return@label`。
  这是 Kotlin 与 Java/C++ lambda 的最大语义差：Java lambda 内不能 `return` 外层值，
  C++ lambda 里 return 只出 lambda 自身。
- 函数引用：`::funName`、`obj::method`、`String::toInt`、构造器引用 `::Person`（✅）。
  Java 方法引用语法近似但类型系统不同：Java 引用只在函数式接口位上适配（SAM 转换），
  Kotlin 函数引用直接是函数类型值。Kotlin 侧 Java SAM 转换亦存在，但**只认 Java 的
  SAM**；Kotlin 自己要用 `fun interface`（1.4+，✅）显式声明可 SAM 转换的接口——
  C++ 无对位（std::function 从任意可调用构造，无接口概念）。

### inline：性能与 reified 的双重理由

- 高次函数的固有成本是对象分配 + 间接调用；`inline` 让编译器把函数体与 lambda 体
  内联进调用点，lambda 不再产生类（✅）。`noinline` 标记个别不外联的参数、
  `crossinline` 允许内联但禁止非局部返回（✅）。
- 由此解锁 **reified 类型实参**：普通泛型函数在 JVM 上被擦除（与 Java 同），
  但 inline 函数调用被展开时按具体实参重新生成代码，`T` 在运行期"真实化"，
  可写 `is T`、`javaClass`（✅）。C++ 模板天然 reified（每实参单态化）；
  Kotlin 用 inline 借来的这条路是**语法位受限的特例**，而 C++ 是默认——
  两门语言在"泛型=擦除复用 还是 模板=展开复制"上的根本取舍在此摊牌，
  详见 [06-泛型.md](06-泛型.md)。

```kotlin
// 🔧 示意：inline + reified 的过滤器
inline fun <reified T> List<*>.filterIsInstanceTo() = filterIsInstance(T::class.java)
```

- 非局部返回只与 inline 共生（✅）：`fun findFirst(xs: List<Int>) = run { xs.forEach { if (it>0) return it }; null }`
  之所以能直接 `return it`，正因为 `forEach` 是 inline 函数——控制流被"摊平"进
  findFirst 的帧里，return 有确定的宿主帧。普通（非 inline）lambda 里 return
  没有外层帧可退，编译失败。

### 扩展函数：静态派发的"伪成员"

- `fun String.lastChar(): Char = this[length-1]` 声明为扩展但**编译为静态函数**
  `StringsKt.lastChar(String)`，按声明类型（接收者的静态类型）派发，不参与虚表
  （✅）。对照 C++：成员扩展（ADL + free function 惯例）语义相同——都是静态派发；
  对照 Java：无对位（只能工具类 `StringUtils` 手传 self）。
- 扩展与同名成员冲突时成员优先（✅）；扩展可被接口"虚假重写"埋坑：基类引用调用
  扩展时选的仍是基类接收者版本。
- 可空接收者扩展：`fun String?.isNullOrBlank()`——这是标准库大量判空助手的语法基础
  （✅）；成员扩展在可空接收者上访问成员要先判空，智能转换可用。

```kotlin
// 🔧 示意：静态派发陷阱
open class Base; class Derived : Base()
fun Base.name() = "base ext"; fun Derived.name() = "derived ext"
// val b: Base = Derived(); b.name() == "base ext"   ← 按静态类型选扩展
```

## 易错点

1. **非局部返回的泄漏**：inline 高阶函数里 lambda 提前 return 会跳过函数体内
   return 之后的代码——`forEach { return }` 绕过"收尾"逻辑；收尾若必须执行，
   要么改 `crossinline` 调用方约束，要么重构为显式 for 循环。
2. **`::` 引用与重载决议**：`::print` 在重载集上歧义，需靠期望函数类型或显式
   类型标注消歧（✅），报错信息对 Java 方法引用用户不直观。
3. **默认参数 + 函数引用**：不能把带默认参数的函数直接引用成少一个参数的函数类型
   （无部分应用糖，✅），需手写 `{ x -> f(x, default) }`；`bind` 扩展
   （`operator fun A.bind(b: B)`，1.1+）可做参数前置绑定但少有人知。
4. **inline 的滥用税**：内联复制放大字节码体积；库函数标 inline 是 ABI 承诺——
   改动内联体在严格意义上影响所有调用点生成物；`noinline`/局部内联是刹车片（✅）。
5. **扩展属性没有 backing field**（✅）：`val String.quotes get() = ...` 只能计算，
   不能有字段——想"加存储"必须走委托（Map 委托、类设计重构），见
   [04 册](04-类与接口与对象表达式.md)。
6. **it 的不可读连锁**：嵌套两层 lambda 都含 `it` 时，`it` 绑定最近 lambda 参数——
   外层遮蔽只能靠显式命名参数或标签；代码评审惯犯。
7. **suspend 转换 lambda 尾随语法**：`scope.launch { ... }` 里 lambda 类型是
   `suspend CoroutineScope.() -> Unit`，接收者 + suspend 修饰都在 lambda 类型上
   （✅）；把 lambda 存成普通 val 再传给 launch 需要 `suspend { ... }` 显式标注，
   漏写 suspend 编译失败。

## 🔧 kotlinc 微实验设计

```bash
kotlinc ch02.kt -include-runtime -d ch02.jar && java -jar ch02.jar
```

- 实验 A（非局部返回的边界）：同一 `forEach` 分别写 `return@forEach`（局部）与
  `return`（非局部），观察后者能提前终止外层函数；再把 `forEach` 换成自定义
  非 inline 高阶函数 `forEachNB`，`return` 立刻编译失败——实证"inline 是
  非局部返回的许可证"。
- 实验 B（reified 对照擦除）：写泛型 `fun <T> cast(o: Any): T? = o as? T`，
  观察 `cast<String>(1)` 返回 null（unchecked 警告），改 `inline fun <reified T>`
  后 `o as? T` 按实参真实判定——两版输出对照即"擦除 vs 具体化"的活体切片。
- 实验 C（扩展静态派发）：用上面 Base/Derived 代码打印派发结果，再用
  `kotlinc -Xemit-jvm-type-annotations`（或反编译 `javap -p`）观察生成物是
  顶层静态方法——证实"扩展=带接收者的静态函数"。
- 实验 D（捕获可变变量）：`var counter=0; repeat(3){ counter++ }`；再启线程
  捕获 `var` 演示跨线程可见性问题（引出 @Volatile 与协程语境下的原子类，
  衔接 [10 册](10-协程高级与Flow.md)）。

## 核心概念中英对照

- **命名实参** — named arguments：调用点以参数名定位实参。
- **尾随 lambda** — trailing lambda：最后一个 lambda 实参移到括号外。
- **闭包** — closure：捕获外层变量的 lambda；Kotlin 一律引用捕获。
- **非局部返回** — non-local return：从 inline lambda 退出的外层函数。
- **函数引用** — function reference (`::name`)：函数值化，含构造器引用。
- **SAM 转换** — Single Abstract Method conversion：lambda ↔ 函数式接口适配；
  Kotlin 侧需 `fun interface` 显式授权。
- **内联函数** — inline function：调用点复制函数体，lambda 免对象化。
- **具体化类型** — reified type parameter：仅 inline 可用的运行期实参类型。
- **扩展函数** — extension function：带接收者的顶层静态派发函数。
- **局部函数** — local function：函数体内声明的函数，可捕获外层变量。

互链：上级 [00 总览](00-总览与阅读地图.md)；上一章
[01-语言基础与结构.md](01-语言基础与结构.md)；下一章
[03-集合与标准库.md](03-集合与标准库.md)。inline/reified 的泛型全貌见
[06-泛型.md](06-泛型.md)。
