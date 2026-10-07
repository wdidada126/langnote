# 《Atomic Kotlin》课带 07 Lambda 与函数式风格（第 70–79 课）——函数升为一等公民的完整账

> 三态标注：✅ 本仓已核实条目 / ⚠️ 课名与课号系凭 leanpub/booksource 官方站体例记忆拟题（带界自拟，逐字题名与部界待销账）/ 🔧 自写示意实验，未实测（本机无 kotlinc，验证前不得声称实测）
> 画像裁定前提：Java/C++ 后端老手。Lambda 概念与 Stream 风格已通（Java 8 / C++11 起），本带算 Kotlin 在其上的四件增量：函数类型、引用统一、inline 零开销、接收者 lambda。

## 一、课带地图（第 70–79 课，共 10 课）

| 课 | 拟题（⚠️ 待逐字销账） | 一行要点 |
|---|---|---|
| 70 | Lambdas | `{ x: Int -> x * 2 }` 匿名函数值 |
| 71 | Lambda Syntax & it | 单参隐名 `it`、尾置 lambda 括号外语法 |
| 72 | Function Types | `(Int, Int) -> Int` 是类型，箭头可读作"映到" |
| 73 | Higher-Order Functions | 函数作参/作返回值，操作注入的主通道 |
| 74 | Function References | `::max` 引用统一顶层/方法/构造器三种地址 |
| 75 | Captures & Closures | 捕获环境；可捕获 var（与 Java 反差最大）⚠️ |
| 76 | Lambda with Receiver | `with(sb) { ... }` 型：this 移进 lambda |
| 77 | Inline Functions | `inline` 抹平高阶调用开销，noinline/crossinline ⚠️ |
| 78 | Scope Functions | let/apply/run/with/also 五件套选型 |
| 79 | Summary | 部练习与收束（⚠️ 归属部界待对齐） |

## 二、画像裁定（Java/C++ 后端视角）

- **已通，略**：lambda 语法手感（两者都有 `->`）；函数作参数的理念（Comparator、回调）；`forEach`/`removeIf` 风格。
- **增量 1——函数类型实名分（72）**：Java 要靠 `IntBinaryOperator/Function<A,B>` 接口族与类型擦除桥接，SAM 转换只在接口位生效；Kotlin `(A) -> B` 是**真类型**，可赋值、入泛型、当返回。C++ 对照 `std::function<Sig>`——Kotlin 语法几乎即 C++ 期望的"直接用签名当类型" ⚠️。
- **增量 2——捕获纪律反转（75）**：Java lambda 只能捕获 effectively final 变量；Kotlin **可捕获 var** 并在闭包内改写（C++ 引用捕获 `[&]` 同族但 Kotlin 无生命周期悬垂问题——全堆对象）⚠️。裁决：这是便利也是逃逸口，循环变量捕获要留心回环语义。
- **增量 3——引用大一统（74）**：`::print`（顶层）、`p::name`（绑定方法引用≈C++ 成员指针而可调）、`::Person`（构造器引用，C++ 无直接对应）——一个 `::` 语法四两拨千斤 ⚠️。
- **增量 4——inline 零开销抽象（77）**：高阶函数默认有对象/lambda 调用开销，`inline` 让编译器展开代码——对标 C++ 模板/`always_inline` 的地位，Java 无等价物（Stream 管分配照单全收）。副作用细节：非局部返回（lambda 里 `return` 跳出外层函数）仅 inline 合法 ⚠️。
- **增量 5——接收者 lambda 与 DSL（76/78）**：类型化 `this` 进 lambda 是 type-safe builder/HTML DSL 的引擎；C++ 用链式调用+CRTP 苦修，Java 用 Builder 样板。五件套选型口诀 ⚠️ 惯用裁决：变换结果用 let/also，配置对象用 apply，语句块用 with/run。

## 三、🔧 微实验设计（未实测）

1. **`funtype.kt`**：`val op: (Int, Int) -> Int = ::max; op(1, 2)` 与 `op = { a, b -> a + b }` 双赋值。**目的**：函数类型是一等公民的三点验证（变量/传参/返回）。
2. **`captvar.kt`**：lambda 存进列表后改写外部 `var counter`，回调触发观察累加；同型 Java 代码 mental diff（effectively final 报错对照）。
3. **`tailcall.kt`**：`list.filter { it > 0 }.map { it * 2 }` 尾置括号省略一级 `()` 的可读性；再传 `::isPositive` 方法引用进 filter。**目的**：语法糖密度。
4. **`receiver.kt`**：`fun build(sb: StringBuilder, block: StringBuilder.() -> Unit)` 内 `append` 免点名调用；对照 `with(sb) { ... }` 等价形态。**目的**：DSL 最小骨架。
5. **`scopefn.kt`**：同一对象分别过 let/apply/run/also/with 五关，打印各函数返回值（对象自身 vs 表达式结果）差异表。**目的**：五件套不是玄学，返回物不同。

## 四、盘谱互链（磁盘 ls 实测 ✅）

- 主对位：[../Learning_TypeScript/03-函数签名与this.md](../Learning_TypeScript/03-函数签名与this.md)——TS 箭头函数词法 `this` vs Kotlin 接收者 lambda 的 `this` 重绑定，方向恰好相反；TS 上下文类型推导 lambda 参数 ≈ Kotlin 省略参数类型惯法；`::max` vs TS 无成员引用语法。
- 泛型函数位参照：[../Learning_TypeScript/06-泛型与tsconfig入门.md](../Learning_TypeScript/06-泛型与tsconfig入门.md)（`(A)->B` 入泛型 vs `Callable`/`Function` 接口位）。
- 兄弟带：上一带 [06-Nullable-Types-and-Errors.md](06-Nullable-Types-and-Errors.md)，下一带 [08-Advanced-Topics-and-Appendices.md](08-Advanced-Topics-and-Appendices.md)。

## 五、核心概念中英对照

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 函面量 | lambda expression | 匿名函数值 `{ params -> body }` |
| 隐式单参 | it | 单参 lambda 的免名参数 |
| 函数类型 | function type | `(A, B) -> C` 形式的真类型 |
| 高阶函数 | higher-order function | 以函数为参/返回的函数 |
| 引用表达式 | callable reference (`::`) | 顶层/绑定/构造器统一寻址 |
| 闭包捕获 | closure capture | lambda 持有外部变量引用 |
| 接收者 lambda | lambda with receiver | this 被指定为某类型接收者 |
| 内联函数 | inline function | 调用点展开以消除抽象开销 |
| 非局部返回 | non-local return | 从被调 lambda 跳出调用方 |
| 作用域函数 | scope functions | let/run/with/apply/also 族 |
| 尾置调用 | trailing lambda | 末参为 lambda 时移出括号 |

## 六、⚠️ 欠账

- 70–79 逐字题名待销；inline/noinline/crossinline 是否入本书正文（还是仅Ⅶ部后段）未定——若缺席，77 全课降级为 ⚠️ 补充注记。
- 五件套官方是否给专章命名"Scope Functions"未核；01 带埋线"operator conventions Ⅶ部"与本带无冲突但 08 带要回收。
- 捕获 var 在并发下可见性语义（无 volatile 承诺）未做纪律裁决，挂账。
