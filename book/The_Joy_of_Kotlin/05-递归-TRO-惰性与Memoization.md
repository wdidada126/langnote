# 05 · 递归、TRO、惰性与 Memoization（本仓专题划分，非原书章名 ⚠️）

> **三态头**
> - ✅ 已证书目事实：*The Joy of Kotlin*，Pierre-Yves Saumont，Manning，2019-04，
>   ISBN 9781617295362；本档服务于 ✅ 焦点"functional programming approaches"的
>   递归/惰性支柱（非 Manning 四焦点独立项，归属 ⚠️ 推定）。
> - ⚠️ 章节推定：主题带（循环↔递归互换 → 栈溢出 → 尾递归/@tailrec → 蹦床(TRO) →
>   Sequence 惰性 → memoization 缓存）按记忆推定；原书是否自造 `TailCalls` 蹦床类型
>   还是仅用 `@tailrec`，**待证**——本档两者都写。
> - 🔧 微实验：全部代码未经 kotlinc 实测，标 🔧。
>
> 上一档 [04-状态变更控制与不可变性.md](04-状态变更控制与不可变性.md)；
> 下一档 [06-结构与测试(Lenses-并行概览).md](06-结构与测试(Lenses-并行概览).md)。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话定义 |
|---|---|---|
| 尾递归 | tail recursion | 递归调用是函数**最后**一个动作、结果不再参与运算的形态 |
| 尾调用优化 | tail call optimization (TCO) | 编译器把尾递归改写成循环，栈帧复用；JVM 无通用 TCO |
| `@tailrec` | tailrec annotation | Kotlin 编译器的"此函数必须可优化，否则报错"契约——TRO 的语法位 |
| 蹦床 | trampoline / TailCalls | 返回"下一步该跳还是停"的 suspension 对象，由驱动循环逐一执行——把栈搬到堆 |
| 累加器风格 | accumulator-passing style (CPS 前身) | `f(n, acc)` 化非尾递归为尾递归的标准手术 |
| 惰性求值 | lazy / call-by-name / by-need | 表达式推迟到需要时求值；`by lazy` 属性、`Sequence` 惰性集合 |
| 记忆化 | memoization | 纯函数结果按实参缓存——**只有纯函数才配安全记忆化**（引用透明的红利） |

## 复演：渐进重构叙事（本档演进链）

同一段"列表求和/深度递归"，从朴素递归改到蹦床再改到惰性管道（⚠️ 情节复演，非逐字引书）：

**第 0 态——朴素递归**（坏在：栈深 O(n)，大输入 StackOverflowError）：

```kotlin
fun sum(xs: List<Int>): Int =
    if (xs.isEmpty()) 0 else xs.head() + sum(xs.tail())   // 加法在递归**之后**：非尾
```

**第 1 态——累加器改尾**（尾调用出现，但 JVM 不保证 TCO——直到用 `@tailrec` 逼编译器兑现）：

```kotlin
tailrec fun sumT(xs: List<Int>, acc: Int = 0): Int =
    if (xs.isEmpty()) acc else sumT(xs.tail(), acc + xs.head())
// @tailrec = 编译期契约：改不成循环就报错，栈深 O(1)
```

**第 2 态——不能尾化的递归怎么办：蹦床**（互相递归/树折叠等，把栈搬到堆）：

```kotlin
sealed class TailCalls<out A> {
    data class Done<out A>(val get: A) : TailCalls<A>()
    data class More(val next: () -> TailCalls<A>) : TailCalls<Nothing>()
}
fun drive(t: TailCalls<Int>): Int = when (t) {          // 驱动循环：堆上"续延"逐个跳
    is TailCalls.Done -> t.get
    is TailCalls.More -> drive(t.next())                 // 这本身是尾调用，由 @tailrec 保障
}
// isEven/isOdd 互递归改蹦床：每个函数返回 More{...} 而非直接调用对方
```

**第 3 态——惰性与记忆化合流**（递归只在需要处展开、算过处不重算）：

```kotlin
val memo = mutableMapOf<Int, Long>()                     // 边界处的一次可变态（04 档第 3 态口径）
fun fib(n: Int): Long = memo.getOrPut(n) {
    if (n < 2) n.toLong() else fib(n - 1) + fib(n - 2)
}                                                        // 指数→线性：纯函数才敢这样缓存
fun main() = (1..10).asSequence()
    .map { it * it }
    .filter { it % 2 == 0 }
    .forEach(::println)                                  // Sequence：逐元素拉取，无中间集合
```

链条收束为一句话：**递归给结构、尾化给深度、惰性给按需、记忆化给重复**——
四件武器都在捍卫引用透明，而非替代循环。

## Java / C++ 对照

- **Java**：无 `@tailrec` 等价物，无语言层 TCO；函数式风格递归在 Java 里常年输给 for 循环，
  直到 Virtual Threads/Stream 时代才有中间路线。蹦床需自造（`Supplier` 链）。
- **C++**：标准只保证**强制**情形（析构、`[[noreturn]]` 尾调用可优化），TCO 非义务——
  递归深树同样爆栈；惯用解是 `-foptimize-sibling-calls`（GCC 尽力而为）或直接手写循环。
  `constexpr` 递归求值在编译期**有配额**（`-fconstexpr-depth`），是另一种"栈"故事。
- **Kotlin**：`@tailrec` 仅限直接自递归（互递归/lambda 内不可标），限制条款是 Saumont
  引蹦床的理由（⚠️ 推定因果）；`lazy`/`by lazy` 是 stdlib 标配，线程安全模式可选。

## 🔧 微实验（未实测）

```kotlin
fun main() {
    val big = List(100_000) { 1 }
    // println(sum(big))    // 期望 StackOverflowError 🔧（非尾递归，深度 10 万）
    println(sumT(big))      // 期望 100000：@tailrec 改写后深度 O(1) 🔧
    println(fib(40))       // 期望 102334155：无 memo 时同 n 重算次数肉眼可见慢
    // 实验 B：给 sumT 塞一个中间乘法 `2 * sumT(...)` 使其非尾，观察 @tailrec 编译错误——
    //   编译器拒绝"撒谎的优化承诺"，这是比运行期爆栈更早的防线。
    // 运行：kotlinc rec.kt -include-runtime -d rec.jar && java -jar rec.jar -Xss256k
}
```

预期观察：同一算法三种命运（第 0 态崩、第 1 态过、第 2 态把崩溃搬到堆上换表达力）。🔧

## 权衡

- **蹦床成本**：每步一个 `More` 闭包对象+驱动循环——常数开销大，换来"任意递归形态"的安全；
  热点路径仍该回 `@tailrec` 或循环。
- **惰性成本**：`Sequence` 迭代器分配与调试黑箱（断点难打）；`by lazy` 的线程安全模式
  选错会有双重初始化故事。
- **memoization 红线**：只对纯函数成立——缓存一个读时钟的函数=把 bug 焊进堆。

## 互链与自测

- 上一级：[00-总览与阅读地图.md](00-总览与阅读地图.md)；上一档 04；下一档 06。
- 04 档"变更搬家"口径在本档第 3 态 `memo` 处复用——两处可变都在受控边界。
- **读完自测**：① 为何 `2 * sumT(xs, acc)` 形态让 `@tailrec` 失效？② 蹦床与 `@tailrec`
  各自把栈放在哪里（寄存器/堆/无）？③ fib 记忆化对非纯函数为什么是错的，举一个反例。

## 中英对照表（本档回收）

| 中文 | 英文 | 备注 |
|---|---|---|
| 续延传递风格 | CPS (continuation-passing style) | 蹦床是其入门形态；KiA2e `suspend` 是工业形态 |
| 按需计算 | call-by-need / by-need | `by lazy` 即 memoized thunk |
| 拉取式集合 | pull-based (Sequence/Iterator) | 对照 List 的推送/物化 |
| 驱动循环 | driver loop | 蹦床的执行引擎 |
