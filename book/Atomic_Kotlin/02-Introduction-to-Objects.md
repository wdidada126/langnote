# 《Atomic Kotlin》第Ⅱ部 Introduction to Objects（第 16–29 章）——从类骨架到集合三兄弟

> 三态标注：✅ 书中内容（凭 leanpub 官方目录条目级事实）/ ⚠️ 记忆或技术归纳 / 🔧 自写示意代码（未实测，本机无 kotlinc 环境验证记录前不得声称实测）
> 本部 14 章逐字章名核实自 leanpub 官方页 ✅；"每章一句话"为 ⚠️ 归纳。

## 一、本段覆盖章目（逐字英文章名）

| 章 | 逐字章名 ✅ | 一句话（⚠️ 归纳） |
|---|---|---|
| 16 | Objects Everywhere | Kotlin 里一切都是对象/类型有值 |
| 17 | Creating Classes | class 声明与主构造器语法 |
| 18 | Properties | 属性抽象：字段+访问器的统一体 |
| 19 | Constructors | 构造过程与 init 块 |
| 20 | Constraining Visibility | public/private/protected/internal 可见性 |
| 21 | Packages | 包声明与文件组织 |
| 22 | Testing | 用 AtomicTest 库做行内小测试 |
| 23 | Exceptions | 抛出与传播异常 |
| 24 | Lists | List 只读/可变双面孔 |
| 25 | Variable Argument Lists | vararg 形参 |
| 26 | Sets | Set 与成员测试惯用法 |
| 27 | Maps | Map 键值与 `[]` 访问 |
| 28 | Property Accessors | 自定义 get/set |
| 29 | Summary 2 | 第二部收束与练习 |

## 二、机制讲解（对老手：Java/C++ 对照）

### 1. 类骨架与主构造器（第 16–17、19 章）

```kotlin
// 🔧 自写示意（未实测）
class Person(val name: String, var age: Int) {
    init { require(name.isNotEmpty()) }
}
```

- 参数位直接声明 `val/var` = **属性**，这一步同时消灭 Java 的"字段+构造赋值+getter/setter"五件套样板，也消灭 C++ 的"成员+初始化列表"配对（C++17 CTAD 只解决类型推导，不解决样板）。
- 主构造器写在类头；构造体内逻辑放 `init` 块。C++ 对照：`init` ≈ 构造函数体内语句，Kotlin 也允许属性声明处直接初始化（≈ C++ NSDMI 非静态成员初始化器）。
- 实例化不写 `new`：`Person("A", 3)`。对照 Java `new Person(...)`（同一表达式两种语言不再区分"栈/堆"心智——Kotlin 对象一律堆语义 ⚠️），C++ 则同时有值语义对象与 `new`，Kotlin **没有值语义对象**，`==`/`equals` 与"对象同一性"的区分压力因此不同。

### 2. 属性 vs 字段（第 18、28 章）

- Kotlin 类里没有公开的"字段"概念：属性 = 存储 + getter (+ setter)，声明 `var age: Int` 即自动生成了 Java 要手写的访问器。Java 老手要记住：**你面对的是属性系统，不是字段系统**。
- 自定义访问器（第 28 章）：`val fullName get() = ...` 计算属性；C++ 要写成员函数或重载 `operator`，Java 要 record + 方法，Kotlin 用 `get()` 保留字内联。
- 背后字段 `field` 关键字解决"在访问器里读写自己"的递归问题；无初始值的属性声明必须给值或由构造器给值（对照 C++ 默认构造自由度过大导致的未初始化 UB——Kotlin 编译期就拒绝未初始化路径 ⚠️）。
- `lateinit`（Ⅶ部回收）与"属性必须有定义好的初值"这条纪律的和解方式。

### 3. 可见性（第 20 章）

- 四档：`private`（类内/文件内顶层）、`protected`（继承链，**接口里也不给用**⚠️ 规则细节）、`internal`（module）、`public`。默认 **public**——与 Java 默认 package-private 正好相反，从 Java 迁移的人不设防就全裸奔，写习惯是"默认不写，越窄越好"⚠️。
- `internal` ≈ "同一编译单元可见"，对应物是 Java 模块系统（JPMS）的 module-internal 但 JPMS 是包级+打包策略，Kotlin 是语言级；C++ 无直接对应（近似匿名命名空间的链接隔离，粒度不同）。
- 文件级顶层声明的 `private` = 仅本 `.kt` 文件可见——≈ C++ 静态自由函数的 TU 隔离，Java 没有这个档位。

### 4. 包与文件（第 21 章）

- `package` 声明、目录不必强制匹配包名（C++ namespace 与目录、Java 包与目录的强一致纪律在此放松 ⚠️ 惯用上仍建议匹配）。
- Kotlin **没有 `import ... static`**：顶层函数/属性与普通 import 同一条通道。

### 5. 测试先行（第 22 章）

- 本书用自制 AtomicTest 库（附录 A 专章 ✅）在教材前半段就建立"每个练习带断言"的纪律 ⚠️。对照：Java 教学书默认 JUnit；Kotlin 生产环境也是 JUnit/kotest，AtomicTest 是**教学最小闭环**，不是工业库。

### 6. 异常（第 23 章）

- Kotlin **没有受检异常（checked exception）**：所有异常都运行时、编译器不强制 catch/声明。对照：
  - Java：`throws IOException` 传染链是 Java 一大样板源；
  - C++：同样无受检（exception specification 已废弃），Kotlin 立场≈C++；
  - 代价：调用 `readFile()` 你得自己记得它会炸。惯用法裁决：受检异常本来就在消亡（Java 8 Stream 里都得绕），Kotlin 的"全无"路线与生态趋势一致 ⚠️。
- 异常是**表达式**（与第Ⅰ部 if 同构）：`val x = try { ... } catch (e: E) { fallback }`；`throw` 的类型是 `Nothing`（Ⅵ部专章回收）。

### 7. 集合三兄弟：只读/可变双面孔（第 24、26、27 章）

- Kotlin 标准库把 Java 的 `java.util.List/Set/Map` 在**类型层**劈成两半：
  - `List<T>`（只读接口）与 `MutableList<T>`（可变，继承只读）；`listOf()` 产出前者、`mutableListOf()` 产出后者。
  - Java 对照：`Collections.unmodifiableList()` 是**运行期装饰器**，类型仍是 List，`add` 要到抛 `UnsupportedOperationException` 才暴露；Kotlin 是编译期拒绝——**把纪律从文档搬到类型系统**，这是 Kotlin 集合设计的第一卖点 ⚠️。
  - C++ 对照：`const std::vector&` 表达只读视图≈只读接口，`std::span`/`const` 限定语义混合，Kotlin 的双接口相当于把 `const` 正确性做进标准库类型谱系。
- `in` 对 Set/List 的惯用（第 13 章埋线的回收）：`if (k in map)`。
- Map 访问：`m[key]` 索引语法（operator conventions 首秀），只读 Map 上 `m[k]` 对缺失键返回 **null**（`getOrDefault` 对应 `getOrDefault`/`?:` 惯用）⚠️——可空性在第Ⅲ部才正式讲，这里先记"Map 取值可能给你 null"。
- 默认工厂 `mapOf("a" to 1)` 里的 `to` 是中缀函数造 `Pair` ⚠️（若书中用 `Pair` 构造则以此为准，`to` 属常见惯用补充）。

### 8. vararg（第 25 章）

- `fun f(vararg xs: Int)` ≈ C++20 `std::initializer_list` 参数 / Java `int... xs`（Java 语法几乎同形，语义同：函数体内是 `IntArray` 视图）。
- 传现成数组：Kotlin 用**展开** `f(*arr)`（≈ C++ `std::to_array`?? 不，更贴切类比是 Python `*args`；Java 直接传数组即可，无展开语法）。C++ variadic template 是同族但机制完全不同（编译期展开 vs 运行期数组）。

## 三、易错点与惯用法裁决（⚠️ 立场标注）

1. **默认 public 陷阱**：Java  reflex "不写就是包内"的肌肉记忆在这里会让你 API 面失控。裁决：公共类的一切实现细节都要主动 `private`/`internal` ⚠️。
2. **只读 ≠ 线程安全**：`List<T>` 只是"接口层面不能改"，背后若交给别人持有 `MutableList` 引用仍会并发改。Java `CopyOnWriteArrayList` 语义同理。别把 `val listOf` 读成快照 ⚠️。
3. **vararg 与重载决议**：`f(vararg Int)` 与 `f(Int, vararg Int)` 之类共存时调用点歧义要警惕；Java 同坑。裁决：vararg 尽量只做单一入口 ⚠️。
4. **init 块顺序**：属性初始化器与 init 块按**源码顺序**交错执行，乱序引用未初始化属性会被编译期拦住但可读性已差。对照 C++：成员初始化列表严格声明序——Kotlin 的顺序规则更直白也更该守 ⚠️（执行序规则系语言标准归纳，是否书中逐字未核）。
5. **无受检 ≠ 不抛**：`listOf(idx)` 越界、除零都照常炸。C++ 除零是 UB、Kotlin 整数除零直接 `ArithmeticException`——比 C++ 可预期 ⚠️。
6. **Map 索引取值的 null**：`m[k]` 缺键返回 null 在Ⅲ部 Nullable 之前是"看不见的地雷"。裁决：本部先养成"缺键必有默认值"写法 `m[k] ?: default` 的占位习惯 ⚠️。

## 四、🔧 微实验设计（kotlinc 单文件，只写设计与预期，未实测）

1. **`accessors.kt`：属性黑盒**。类内声明 `var suspicious: Int`，主函数用 `obj.suspicious = 1` 赋值（语法像字段）。自定义 `set` 里夹打印，观察每次赋值走访问器。**目的**：建立"Kotlin 无 public 字段，全是访问器"的认知。
2. **`visibility.kt`：internal 边界**。同文件顶层函数 A `internal` 调 B `private`；再放到两个不同"module"模拟（两个 kotlinc 调用产出两份 jar）后跨引用，预期 `internal` 跨 module 不可见。**目的**：摸到 Java 没有的那一档。
3. **`rolist.kt`：只读/可变双面孔**。`val rl: List<Int> = mutableListOf(1,2)` 合法上转型；再试 `val ml: MutableList<Int> = listOf(1,2)` 预期编译失败；把 `rl` 强转回 `MutableList` 运行期居然成功（共享对象）——观察只读只是类型层合约。**目的**：只读接口的能与不能。
4. **`varexp.kt`：异常即表达式**。`val v = try { 10 / 0 } catch (e: ArithmeticException) { -1 }`；再写 `fun f(b: Boolean): Int = if (b) 1 else throw IllegalStateException()` 观察 Nothing 参与类型兼容。**目的**：为Ⅵ部 Nothing 章预热。
5. **`vararg.kt`：展开与装箱**。`fun sum(vararg xs: Int)` 分别用 `sum(1,2,3)`、`sum(*intArrayOf(1,2,3))` 调用；再传 `IntArray` 不展开，预期类型不匹配报错。**目的**：展开运算符 `*` 的存在理由。

## 核心概念速览

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 主构造器 | primary constructor | 写在类头的参数表，同时声明属性 |
| 属性 | property | 存储+访问器的统一抽象，消灭字段样板 |
| 初始化块 | init block | 构造体内的自由语句区，按源码序执行 ⚠️ |
| 模块可见 | internal | 同一编译单元内可见，介于 public 与 private 之间的新档 |
| 非受检异常 | unchecked exception | Kotlin 全员运行时异常，无 throws 传染 |
| 只读列表 | List (read-only) | 类型层禁止修改的列表接口 |
| 可变列表 | MutableList | 继承只读并解锁修改操作 |
| 可变参数 | vararg | 零或多个同类型实参，体内为数组 |
| 展开运算符 | spread `*arr` | 把数组作为 vararg 实参铺开的语法 |
| 计算属性 | custom getter | 每次读取现算的属性，无独立存储 |
| 背后字段 | backing field (`field`) | 访问器内部真正存值的位置，自动或按需生成 |
| 配对构造 | to/Pair | Map 字面量的元素形态 ⚠️ |
