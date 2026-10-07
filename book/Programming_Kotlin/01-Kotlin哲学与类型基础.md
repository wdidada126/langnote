# 01 · Kotlin 哲学与类型基础

> 三态口径：✅ 语言事实以 kotlinlang.org 官方文档为口径；⚠️ 本章覆盖范围是**推定**的
> 主题切分（原书页目录 403 墙未获，不冒充原书章名；对应 [00 总览](00-总览与阅读地图.md)
> 骨架表"基础与惯用：类型/不可变/空安全叙事"段）；🔧 本章所有代码为凭记忆重敲，
> 本环境无 kotlinc（仅 JDK 17），未实测，修复实测后再升格。
> 延续 00 的 2018 时效降权裁决：**语言动机叙事照读**，具体语义细节一律以现行官方文档为准。

## 核心概念速览（中英对照）

- **表达式导向** — expression-oriented：`if`/`when`/`try` 皆有值，语句与表达式的界线在 Kotlin 里大幅软化。
- **不可变优先** — prefer immutability：`val` 默认心智（引用不可变，非对象冻结），Venkat 全书动机的根 ✅。
- **空安全类型系统** — null safety：`T` 与 `T?` 是两个类型，可空性进入类型签名，NPE 从运行期事故前移为编译期违例。
- **平台类型** — platform type：Java 来的声明可空性未知，编译器记作 `T!`，放行但埋雷（互操作专属）。
- **智能转换** — smart cast：对 `val`/局部变量在类型检查后自动窄化，免去手写强转；稳定性是前提。
- **结构相等** — structural equality：`==` 调 `equals()`，`===` 才是引用同一；Java 老手第一天的坑。
- **Nothing / Unit**：`Unit` 是"有返回但无信息"（≈ void 但可当值）；`Nothing` 是"绝不正常返回"，空类型、协变底端。

## 机制：写给老手写 Java/C++ 的人

Kotlin 的类型层选择，逐条对照旧世界：

1. **`val` vs `final`**：Java 的 `final` 是可选的纪律，Kotlin 把默认方向反转——先 `val`，
   要 `var` 需自觉。这决定后文一切：不可变使 smart cast 成立（03 章 sealed+when 的穷尽性
   依赖它）、使并发共享少一层防御。C++ 的 `const`/`constexpr` 走的是另一条路（值语义+
   编译期求值），Kotlin 只管引用不可变，不做深度不可变承诺。
2. **没有基元类型的表层**：`Int`/`Long` 是类型系统的公民（可为泛型实参前的表面一致），
   但编译器对集合等场景做特化字节码——表层统一、底层高效，对照 C++ 模板为 `vector<int>`
   与 `vector<shared_ptr>` 各生成一份的旧账。
3. **`T?` 进入签名**：Java 用 `Optional`/注解（`@Nullable`）打补丁，Kotlin 把可空性做成
   类型的一部分。安全阀三件套：`?.`（安全调用，短路返回 null）、`?:`（elvis 给默认值）、
   `!!`（显式引爆，等于"我接管 NPE 责任"）。✅ 官方口径：`!!` 抛的是 `KotlinNullPointerException`
   （注：现行文档与源码对具体异常类的表述有演变，🔧 不咬死）。
4. **表达式导向**：`val size = if (list.isEmpty()) 0 else list.size`；`when` 是"带模式匹配的
   switch 超集"——分支可不连续、可比对象、可无Subject（`when { x < 0 -> ... }`），且作表达式时
   分支必须全覆盖或带 `else`，否则编译错。对照 C++ 需要 `std::optional`+三元链的等价物。
5. **平台类型是唯一的"类型系统后门"**：Kotlin 互操作读不到 Java 注解历史，故 `String!`
   默认放行、不做检查——这是**编译器有意放弃的一段空安全**，不是 bug。防御写法：接 Java
   入参立刻落到显式声明的可空类型上。

## 易错点

- **`==` 与 `java` 直觉相反**：Java 里 `==` 是引用比较，Kotlin 里 `==` 是 `equals()` 调用
  （对可空左侧有 null 处理）。包装类 `Integer.valueOf` 缓存 [-128,127] 造成的 Java 经典题
  在 Kotlin 里根本不发生——但 `===` 误用（比引用）仍是新经典事故源。
- **`!!` 当 `?.` 用**：见空即 `!!` 等于把编译期保障改回运行期赌博。判据：只有"此处为 null
  即程序不变量已破坏、崩了活该"的语义才配 `!!`。
- **smart cast 对 `var` 失效**：局部 `var` 在跨线程/可被其他位置修改时不保证检查与使用之间
  类型不变，✅ 官方规则：smart cast 仅对**确定稳定**的标识符生效（局部不变量、`val`、
  同类内 private 且无自定义 getter 的属性等）。老手常在此处吃"明明判了 is 还让我转"的火。
- **`when` 忘了 `else` 的两种后果**：作语句时不强制覆盖（类型安全网在 sealed 才收口，见 03 章）；
  作表达式时必须穷尽。Java `switch` 的 fall-through 心智在这里没有对应物，也没有 `break`。
- **把 `Unit` 当 `void` 的残留**：`fun f(): Unit` 可省略；但lambda 末行表达式即返回值，
  期望 `Unit` 的lambda里"最后一行恰好是个有值的表达式"不会造成类型意外——这是与 C++
  "末表达式靠返回类型推导" 相反方向的心结，需清空。

## 🔧 微实验（未实测，kotlinc 可用后逐条回填）

1. **平台类型引爆炸点定位**：Java 侧 `public static String ret(String s) { return s; }`，
   Kotlin 侧 `val x: String = JavaLib.ret(null)` 观察是否编译通过、NPE 落在哪一行——
   预期：声明处赋值即抛，证明"信任 Java 的代价由声明者预付" ⚠️ 预期基于官方平台类型文档。
2. **`!!` vs `?. ?: ` 三路对比**：
   ```kotlin
   // 🔧 凭记忆，未编译
   val a: String? = readMaybeNull()
   println(a?.length)          // null 短路 → 打印 null，不抛
   println(a?.length ?: -1)    // elvis 兜底 → -1
   println(a!!.length)         // 引爆 → KNE，栈顶即此行
   ```
3. **smart cast 稳定性的边界**：把 03 章要用的模式先在本章试探——
   ```kotlin
   // 🔧
   var x: Any = "s"
   if (x is String) { println(x.length) }   // 预期编译错：var 可能被并发修改
   val y: Any = "s"
   if (y is String) { println(y.length) }   // 预期通过
   ```
4. **`when` 作表达式的穷尽要求**：
   ```kotlin
   // 🔧
   val n = 1
   val s = when (n) { 1 -> "one"; 2 -> "two" }   // 预期编译错：无 else，非穷尽
   ```

## 中英对照表

| 英文 | 中文 | 一句注 |
| --- | --- | --- |
| nullable type | 可空类型 | `T?`，与 `T` 无子型关系 |
| platform type | 平台类型 | Java 来的 `T!`，空安全豁免区 |
| safe call operator | 安全调用 | `?.`，链式空短路 |
| elvis operator | elvis 运算符 | `?:`，命名来自 Elvis 侧头发型 |
| smart cast | 智能转换 | 类型检查后自动窄化，依赖稳定性 |
| structural equality | 结构相等 | `==`，走 `equals()` |
| referential equality | 引用相等 | `===` |
| expression-oriented | 表达式导向 | if/when/try 皆有值 |
| immutable by default | 默认不可变 | `val` 优先的动机叙事 |
| Nothing / Unit | 空类型/单位类型 | 底类型 / 可当值的 "void" |

## 互链

- 上：[00-总览与阅读地图.md](00-总览与阅读地图.md)；下：[02-集合与函数式操作.md](02-集合与函数式操作.md)。
- 现代语义回源：✅ Kotlin language 官方文档（null-safety / basic types / control flow 各页）；
  本仓兄弟目录 [../Kotlin_in_Action_2e/](../Kotlin_in_Action_2e/00-总览与阅读地图.md)、
  [../Atomic_Kotlin/](../Atomic_Kotlin/00-总览与阅读地图.md)。
- 读完自测：① 平台类型为何存在、防御写法是什么；② `==`/`===` 与 Java 直觉的错位在哪；
  ③ smart cast 对什么形态的变量失效、为什么。
