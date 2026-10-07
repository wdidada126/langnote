# 05 · 函数与 Lambda 条目簇

> **部名/Item 编号/逐字题名以版权页目录为准** ⚠️。本簇编号接 04 簇续排（⚠️39–46），
> 仅作检索锚点，**条旨为本仓自概括**，不声称逐字来自原书。总览见
> [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 三态：**✅** 语言事实；**⚠️** 编号/归属推定；**🔧** 未实测（本机无 kotlinc）。

## 本簇条目地图（⚠️ 推定 8 条）

| 编号 | 条旨（本仓自概括） | 一句话裁决 |
| --- | --- | --- |
| ⚠️39 | 函数默认 final，open 只在确有多态时开 | ✅ 非 open 不可覆写、可静态派发；无继承意图就别留口子 |
| ⚠️40 | 单语句函数用表达式体 | ✅ `fun area() = w * h` 免写 return/返回类型声明位；与 ⚠️18（表达式优先）同根 |
| ⚠️41 | inline 三收益：免 lambda 对象、非局部返回、reified 型参 | ✅ 内联是语义特性不只是性能提示——`inline` 才谈得上跳出调用函数 |
| ⚠️42 | noinline：lambda 参数要"逃逸"（存字段/传出）时的豁免标记 | ✅ 被 noinline 的参数失去非局部返回权；逃逸是内联的天敌 |
| ⚠️43 | crossinline：允许在非内联嵌套上下文（object 表达式等）调用 | ✅ 比 noinline 更严：连对象引用都不留，故永远不能非局部返回 |
| ⚠️44 | inline 是"函数体进契约"：改体需调用方重编译（ABI 兴趣线接口） | ✅ 内联把实现烧进调用方字节码——公开 API 慎用 inline（详见特写） |
| ⚠️45 | 函数引用 `::name` 替等价的手包 lambda | ✅ `map(::sqrt)` 免一层无谓包装；可引用构造器/绑定成员 `user::name` |
| ⚠️46 | lambda 嵌套过两层就抽具名函数 | ✅ 嵌套里外层 `it` 不可见（同 ⚠️5），可读性与正确性双杀 |

## 条目特写

### ⚠️41–43｜inline / noinline / crossinline 的三值语义

🔧 典型三件套：
```kotlin
inline fun retry(times: Int, block: () -> Unit, cleanup: () -> Unit) {
    repeat(times) { try { block(); return } catch (e: Exception) { } }
    cleanup()                       // cleanup 若被存起来稍后调 → 要 noinline
}
// 调用方：block 里可直接 return@retry 之外再 return（非局部返回）——✅ 只有 inline 参数有权
```
裁决表：参数会被**存/传**→ `noinline`（保留 lambda 对象，禁非局部返回）；参数要进
**嵌套非内联上下文**（object/匿名函数）→ `crossinline`（不留对象引用，同样禁非局部
返回，且 `return@inlineFun` 局部标签也禁）。两者都是"我要逃逸，请别烧我进调用点"。

### ⚠️44｜inline 与 ABI（本仓兴趣线接口）

✅ 语义：库函数一旦 `inline`，其**函数体**就成了调用方字节码的一部分；库升级改体，
旧调用方不重编译就继续跑旧体——行为漂移但签名兼容，二进制兼容性检查器看不见它。
✅ 配套机制：`@PublishedApi internal` 允许内联体引用 internal 成员（否则编译失败）；
`reified` 型参只能活在 inline 函数上（✅ 这是 Kotlin 对 Java 擦除的最大反超点）。
**跨语言裁决**：C++ 的 `inline` 是链接期 ODR 许可（多 TU 定义合并），Kotlin 的
`inline` 更接近宏展开+闭包融合——两者同名不同德，迁移读者最易在此中招（对照
[../Effective_Modern_C++/06-lambda表达式.md](../Effective_Modern_C++/06-lambda表达式.md) 的捕获语义：C++ lambda 是带捕获列表的闭包对象，Kotlin 默认也是，唯 inline 把它变成"源码级"）。TS 无编译期内联条目，函数类型严格性判例见
[../Effective_TypeScript_2e/04-函数条目簇.md](../Effective_TypeScript_2e/04-函数条目簇.md)。

## 🔧 微实验（全部未实测，本机无 kotlinc）

1. 同一高阶函数加/去 `inline`，`javap -c` 对比：是否生成 `Function1` 匿名类、体是否进调用方。
2. `noinline` 参数里写非局部 `return`，留编译器报错文案归档（预计 "return" from noinline）。
3. `inline fun <reified T> List<*>.countOfType() = count { it is T }` vs 传 `KClass` 版，对比字节码与调用点。

## 盘谱互链

- [../Functional_Programming_in_Kotlin/01-函数式基础与引用透明.md](../Functional_Programming_in_Kotlin/01-函数式基础与引用透明.md)（高阶函数原理侧）。
- [../Kotlin_in_Action_2e/02-函数与Lambda.md](../Kotlin_in_Action_2e/02-函数与Lambda.md)（语言事实基线，先读它再读本书条目）。
- [../Java_to_Kotlin/00-总览与阅读地图.md](../Java_to_Kotlin/00-总览与阅读地图.md)（Java 函数式接口→Kotlin 函数类型迁移线）。

## 中英对照

| 中文 | 英文 | 一句定义 |
| --- | --- | --- |
| 内联函数 | inline function | 调用点展开函数体，lambda 参数免对象化，支持非局部返回。 |
| 非局部返回 | non-local return | 从 lambda 里直接 return  enclosing 函数，仅内联参数可用。 |
| 具化型参 | reified type parameter | inline 函数专属，运行期可 `is T`/`T::class`，对抗擦除。 |
| 逃逸参数 | noinline/crossinline | 分别允许"保留对象"与"仅允许调用的嵌套上下文"两种豁免。 |
| 函数引用 | function reference `::` | 按名字引用函数/构造器/属性访问器，可携带接收者绑定。 |

## ⚠️ 欠账

- 原书 inline 条目实际编号/拆合（可能"何时不该内联"单列一条）待销账。
- inline 与 Java `@InlineOnly` 历史包袱、Swift `@inlinable` 的 ABI 对照未展开（留 C++/Swift 兴趣线作业）。
