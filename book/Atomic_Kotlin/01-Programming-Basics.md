# 《Atomic Kotlin》第Ⅰ部 Programming Basics（第 1–15 章）——语言地基快跑

> 三态标注：✅ 书中内容（凭 leanpub 官方目录条目级事实）/ ⚠️ 记忆或技术归纳 / 🔧 自写示意代码（未实测，本机无 kotlinc 环境验证记录前不得声称实测）
> 本部 15 章逐字章名核实自 leanpub 官方页 ✅；下文"每章一句话"为基于章名的技术性归纳 ⚠️，不冒充书中原文。

## 一、本段覆盖章目（逐字英文章名）

| 章 | 逐字章名 ✅ | 一句话（⚠️ 归纳） |
|---|---|---|
| 1 | Introduction | 全书路线：以"原子"节奏自底向上建 Kotlin 心智模型 |
| 2 | Why Kotlin? | 对 Java/C++ 老手的卖点：更少的样板、空安全、函数式设施 |
| 3 | Hello World! | 第一个程序与 main 函数入口形态 |
| 4 | var & val | 可变/不可变变量声明，不可变优先 |
| 5 | Data Types | 基本类型与 Any/Unit 等顶层类型的鸟瞰 |
| 6 | Functions | fun 定义、参数、返回类型、表达式函数体 |
| 7 | if Expressions | if 作为表达式带值返回 |
| 8 | String Templates | 字符串内 `$name`/`${expr}` 插值 |
| 9 | Number Types | Int/Long/Float/Double 与显式转换 |
| 10 | Booleans | 布尔类型与严格条件表达式 |
| 11 | Repetition with while | while/do-while 循环 |
| 12 | Looping & Ranges | for 循环与区间（range）语法 |
| 13 | The in Keyword | in 的区间包含与成员测试语义 |
| 14 | Expressions & Statements | 表达式/语句之辨：Kotlin 以表达式优先 |
| 15 | Summary 1 | 第一部收束与练习 |

## 二、机制讲解（对老手：Java/C++ 对照）

### 1. var/val ↔ final / const（第 4 章）

- `val` ≈ Java 的 `final` 局部变量/字段：**引用不可变**，不是对象深不可变（`val list = mutableListOf<A>()` 后仍可 `list.add(...)`）。
- C++ 对照：`val` ≈ `const`（顶层），但 Kotlin 没有 C++ 那种 `const`/`constexpr` 编译期求值分界；也没有 `&` 引用语义。
- `var` ≈ C++ 普通变量 / Java 非 final 变量。语言的默认姿态是"先写 val，需要改再升 var"⚠️（惯用法裁决，非书中逐字）。
- 类型声明后置：`var x: Int = 5`。对照 C++ 前置 `int x = 5;`、Java `int x = 5;`。类型可推导时省略冒号部分是惯用写法。

### 2. 数据类型映射（第 5、9、10 章）

- Kotlin 的 `Int/Long/Float/Double/Short/Byte/Boolean/Char` 在 JVM 上编译为**原生 primitive**，不是装箱对象（性能路径与 Java `int` 相同；泛型位置才自动装箱）⚠️。
- 宽度纪律与 C++ 不同：Kotlin 不承诺 `Int` 之外类型的跨平台宽度像 C++ 那样依赖实现——它直接钉死为 JVM 语义（Int 恒 32 位）⚠️。C++ `int/long` 随平台变，Kotlin 无此问题。
- **没有隐式加宽**：Java/C++ 的 `int → long` 自动提升在 Kotlin 中不存在，必须 `i.toLong()`。转换是成员函数风格（`toDouble()`、`toString()`），不是构造式 `long(i)` ⚠️ 这是与 C++ 函数式转换语法 `long(i)` 的直观差异。
- `Char` 不是整数类型：C++ 里 `char + 1` 合法且提升为 int，Kotlin 里不行，需显式 `c.code` / `'a'.code`（较旧写法 `.toInt()`）⚠️。
- `Boolean` 严格：条件位置不接受 `Int`/指针/可空值。C++ 的 `if (ptr)`、Java 圈内"真值"文化在 Kotlin 无对应物；`if (x != null)` 必须写全。
- 顶层类型三件套：`Any`（≈ C++ `std::variant`?? 不，≈ Java `Object`）、`Unit`（≈ C++ `void`，但是真实单例类型，可写进泛型实参——`void` 做不到）、`Nothing`（≈ C++ `[[noreturn]]` 的类型化版本，空类型）。

### 3. 函数（第 6 章）

- `fun f(a: Int, b: Int): Int = a + b`：表达式函数体省大括号与 return，对应 C++ 单返回表达式 `auto f(int a,int int b){return a+b;}` 的压缩形态。
- Kotlin 有**顶层函数**：一个 `.kt` 文件不必先包一个类。对照 Java"一切皆在类中"，回到 C++ 的自由函数手感；编译后仍生成一个类（互见附录 B，第 08 篇）。
- `main` 形态：`fun main() { }` 顶层函数（可带 `args: Array<String>` 重载）；对应 Java 的 `public static void main(String[])`、C++ 的 `int main()` ⚠️。
- 默认参数在本部未讲、在第Ⅲ部 Named & Default Arguments（第 31 章）登场，此处只钉一句：它是 Java 重载脚手架大半消失的原因。

### 4. if 作为表达式（第 7 章）

- `val s = if (x > 0) "pos" else "neg"`：if 有值。对照：
  - Java/C++：靠三元 `? :`（表达式）与 if 语句两套语法分裂；
  - Kotlin：**没有三元运算符**，if-else 表达式统一取代，多行时仍需 else 分支齐备才有值 ⚠️（"else 缺失时值为 Unit"是归纳表述）。
- C++ 里赋值也是表达式（`if ((p = q))` 经典坑），Kotlin 赋值是**语句**、无值，从语法上封杀这类错误 ⚠️。

### 5. 字符串模板（第 8 章）

- `"$name has ${a + b}"`：`$` 简单名、`${}` 任意表达式。对照：
  - Java：`+` 拼接时代官能差；JDK 15+ text blocks（`"""`）解决多行但不解决插值小表达式；
  - C++20 仍无字符串插值标准语法（要靠 `std::format` 的 `{}` 占位，编译期格式化）。
- Kotlin 字符串不可变同 Java；`+` 拼接会走 StringBuilder 优化 ⚠️。本部只讲 `+` 与模板，`trimIndent()` 等多行设施书中后置出现 ⚠️。

### 6. 循环与区间（第 11–13 章）

- `while`/`do-while` 与 Java/C++ 同形，无 `for(;;)` 三段式——Kotlin 的 for 只有一种：**for-each**（对可迭代对象），C 风格索引循环要写 `for (i in 0..n-1)` 或 `for (i in 0 until n)`。
- 区间语法是本部的 Kotlin 特色：
  - `0..9` → `IntRange`，闭区间，含 9；
  - `0 until 10` → 开区间（避开端点差一错误的惯用武器）；
  - `9 downTo 0`、`step 2`：降序与步长。
  - 对照 C++23 `std::views::iota` 与 range-v3：概念对应，但 Kotlin 的 range 是**语言级+标准库双修的语法糖**，零开销展开为普通计数循环 ⚠️。
- `in` 关键字（第 13 章）一身两用：
  - 循环的 `for (x in collection)`；
  - 包含测试的表达式 `x in 1..10`、`s in stringSet`，返回 Boolean；反义 `!in`。
  - 对照：C++20 `std::ranges::contains`（且仍非中缀）、Java 的 `contains()` 方法调用——Kotlin 把它做成**中缀运算符**，这是后文 operator conventions（第Ⅶ部）的第一次预告。
- `in` 还可用于 when 分支与 sealed 匹配（Ⅲ/Ⅴ部回收），本部先埋线 ⚠️。

### 7. 表达式 vs 语句（第 14 章）

- 分类标准：有值参与更大的表达式 = expression；只产生副作用 = statement。
- Kotlin 中 `if`/`when`/`try`/`throw` 都是表达式（赋值除外）。设计后果：**能写表达式体的场合就别写语句块**，代码密度上升。
- 对照 C++：两者光谱不同——C++ 几乎一切皆表达式（连 `try` 不是），Java 几乎一切皆语句（只剩三元与赋值表达式）。Kotlin 取中间：分支有值、赋值无值。
- 对照 Java 21 模式匹配 switch 表达式（JEP 441）：Java 正在向 Kotlin 的 `when` 表达式靠拢，方向本身即是证词 ⚠️。

## 三、易错点与惯用法裁决（⚠️ 立场标注）

1. **C++/Java 直觉第一坑：无隐式数值提升**。`val l: Long = 10` 编译不过（字面量类型不匹配时看情况），`i + l` 在 Kotlin 里直接报错而非悄悄提升。立场：这是特性不是障碍——所有加宽处显式 `toLong()`，消灭 C++ 整型提升类 bug ⚠️。
2. **`1..N` 是闭区间**。从 Java `for (i = 0; i < n; i++)` 迁移的人写 `0..list.size` 必越界。惯用法裁决：遍历下标一律 `indices` 或 `0 until size` ⚠️。
3. **`val` ≠ 深不可变**。见第 4 章对照；与 Java `final List` 同款认知负担，Kotlin 的类型级解法（read-only 接口）要到第Ⅱ部 Lists 章才出现，届时再裁决 ⚠️。
4. **Int 溢出静默回绕**：与 Java/C++（有符号 UB 但实践回绕）一致，Kotlin 算术默认不检查。要检查用 `Math.addExact`/`toInt().let{}`?? 裁决：标准库提供 `+` 不检查是性能立场，教材对本部练习不涉及溢出，别过度解读 ⚠️。
5. **`Char` 参与算术**、**`Boolean` 用 `&&`/`||`**（Java 风格短路）而非 C++ 的 `and/or` 别名；位运算名字是 `and`/`or`/`inv` **函数**（中缀），不是 `&`/`|` 运算符——跨 Ⅲ 部 operator 章回收 ⚠️。
6. 惯用法：本部阶段就该养成的两条——声明一律 `val` 优先；能用 `until` 就不用 `..size-1` ⚠️。

## 四、🔧 微实验设计（kotlinc 单文件，只写设计与预期，未实测）

1. **`types.kt`：转换纪律**。写 `fun main() { val i = 42; val l: Long = i }` 预期编译失败；改为 `i.toLong()` 通过。再加 `val c: Char = 'a'; val n = c + 1` 预期失败，`c.code` 通过。**目的**：钉死"无隐式提升、Char 非数值"两条。
2. **`ranges.kt`：区间四件套**。同一目标（打印 0..8 的偶数降序）用四种写法：`8 downTo 0 step 2`、`0..8` 内 filter、`until` 版、`in` 测试断言版。预期输出一致；对照生成码可 `kotlinc -Xemit-jvm-type-annotations`?? 简化为：只观察 `until` 与 `..` 端点差一。**目的**：差一错误的语法级免疫。
3. **`expr.kt`：if 表达式与赋值语句**。`val s = if (true) { "a" } else { "b" }` 通过；`val t = (x = 5)` 预期编译失败（赋值无值）。**目的**：亲手验证第 14 章的表达式/语句分界。
4. **`template.kt`：插值边界**。测试 `"$2 + ${2}"`、`"${"nested ${1}" }"`、`$` 后跟非标识符（`"cost: 5$"`）是否需要 `${'$'}`。预期：字面 `$` 需转义或写成表达式。**目的**：模板解析规则。
5. **`mainargs.kt`：入口形态**。`fun main(args: Array<String>)` 与无参 `main` 同文件共存，预期编译告警/二义或合法重载通过（⚠️ 预期不确定，正是实验要裁决的点）。

## 核心概念速览

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 不可变引用 | val | 引用一经绑定不可改，对象本身可不可变另论 |
| 可变变量 | var | Java/C++ 常规变量对应物 |
| 单元类型 | Unit | 无值返回的单例类型，比 C++ void 更"有类型" |
| 顶层类型 | Any | 非空万物之源，≈ Java Object |
| 表达式 | expression | 有值、可参与更大表达式 |
| 语句 | statement | 只有副作用、无值（Kotlin 中赋值属此类） |
| 字符串模板 | string template | `$name`/`${expr}` 内嵌插值 |
| 闭区间 | range (`..`) | 含双端点的整数区间，for/in 的基础 |
| 开区间惯用 | until | `0 until n` 排除 n，防差一 |
| 包含测试 | in | 中缀运算符，测区间/集合成员，返回 Boolean |
| 显式转换 | toLong()/toDouble() | 唯一合法的数值加宽通道 |
| 原生类型映射 | primitive mapping | Int/Long 等编译为 JVM 原生类型 ⚠️ |
