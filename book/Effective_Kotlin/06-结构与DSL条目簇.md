# 06 · 结构与 DSL 条目簇

> **部名/Item 编号/逐字题名以版权页目录为准** ⚠️。本簇编号接 05 簇续排（⚠️47–54），
> 仅作检索锚点，**条旨为本仓自概括**，不声称逐字来自原书。总览见
> [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 三态：**✅** 语言事实；**⚠️** 编号/归属推定；**🔧** 未实测（本机无 kotlinc）。

## 本簇条目地图（⚠️ 推定 8 条）

| 编号 | 条旨（本仓自概括） | 一句话裁决 |
| --- | --- | --- |
| ⚠️47 | 作用域函数按两轴选型：返回值是谁 + 上下文体叫什么 | ✅ let/also 回块结果、体名 `it`；run/with/apply 体名 `this`；run/with/let 回块结果，apply/also 回接收者 |
| ⚠️48 | 别连续链作用域函数，别为用而用 | ✅ 两层 `this` 嵌套必遮蔽、`it` 失效（呼应 ⚠️5）；判据：省掉它是否更清楚 |
| ⚠️49 | 声明处方差 in/out 取代通配符 | ✅ `interface Out<out T>`：T 只出；`compareBy` 类消费位用 `in`；比 Java `? extends` 可声明在接口上一劳永逸 |
| ⚠️50 | 使用处方差与星投影：调用点才知角色时用 | ✅ `fun copy(src: List<out T>, dst: MutableList<T>)`；`List<*>` = 只读未知元，写入即 ❌ |
| ⚠️51 | ADT 主组合拳：sealed + data + 穷尽 when | ✅ 分支即类型、编译器查漏；错误处理可退 Option/Either 模式（见 FP in Kotlin 盘谱） |
| ⚠️52 | 类型安全 DSL = 带接收者 lambda + `@DslScope` | ✅ `@DslScope` 禁止隐式接收者越层逃逸（外块函数在内块误调直接编译失败） |
| ⚠️53 | 名义类型系统里要"结构近似"用接口，不要字面量祈祷 | ✅ Kotlin 无结构化类型：鸭子类型靠 interface/泛型上界表达 |
| ⚠️54 | 型参默认上界 `Any?`：先声明 `<T : Any>` 再谈可空 | ✅ 非空型参让 `!!` 与平台类型噪音出局；`Nothing` 是"永不到来"的返回类型 |

## 条目特写

### ⚠️47｜作用域函数选型规范（本仓落码口径）

- 判空并变换 → `?.let { }`；对结果做副作用且继续原对象 → `also`；
- 构造期配置对象（"build 感"）→ `apply`；函数体内造局部作用域计算 → `run`；
- 已有接收者、块长且以它为主语 → `with`。裁决：选型是**可读性函数不是风格教条**；
  同一段代码 `let/run/also` 全能编译过，选错只是读者付账。

### ⚠️49/50｜泛型方差

🔧 坏味道：`fun printAll(list: List<Any>)` 收不下 `List<String>`（✅ List 协变但形参写死）。
🔧 修正：
```kotlin
fun printAll(list: List<out Any>) = list.forEach(::println) // 生产位：out
fun <T> fill(list: MutableList<in T>, item: T) { list += item } // 消费位：in
```
**跨语言裁决**：Effective Java Item 26–29"PECL：producer-extends, consumer-super"
（⚠️ 编号凭记忆；本仓暂无 EJ 分章档互链）在 Kotlin 的判词是"能声明在声明处就
别写在使用处"——✅ 协变接口（`List<out E>` 出厂即带）让调用点免写通配符，这是
Kotlin 相对 Java 的真实减负。C++ 模板无声明处方差概念（每个实例独立类型），
约束靠 concepts 表达（见 [../C++20模板元编程/06-概念和约束.md](../C++20模板元编程/06-概念和约束.md)）。
TypeScript 是另一种世界：结构化+双向协变默认**不健全**（soundness 让位于易用），
判例见 [../Effective_TypeScript_2e/01-类型基础条目簇.md](../Effective_TypeScript_2e/01-类型基础条目簇.md)
与 [../Effective_TypeScript_2e/03-对象与结构关系条目簇.md](../Effective_TypeScript_2e/03-对象与结构关系条目簇.md)，
系列索引 [../TypeScript系列·总索引.md](../TypeScript系列·总索引.md)。

## 🔧 微实验（全部未实测，本机无 kotlinc）

1. DSL 嵌套不带/带 `@DslScope`，在外层函数内层误调，记录报错差异。
2. `List<String>` 传给 `List<Any>`（预期 ✅ 通过）与 `MutableList<String>` 传给
   `MutableList<Any>`（预期 ❌），留方差教学反例。
3. `when` 穷尽 sealed 漏一分支，记录 1.7+ 由警告升级错误的口径变化 ⚠️。

## 盘谱互链

- [../The_Joy_of_Kotlin/01-函数式方法入门.md](../The_Joy_of_Kotlin/01-函数式方法入门.md)、
  [../Functional_Programming_in_Kotlin/03-Option与错误处理.md](../Functional_Programming_in_Kotlin/03-Option与错误处理.md)（ADT 替代路线）。
- [../Programming_Kotlin/01-Kotlin哲学与类型基础.md](../Programming_Kotlin/01-Kotlin哲学与类型基础.md)、
  [../Atomic_Kotlin/00-总览与阅读地图.md](../Atomic_Kotlin/00-总览与阅读地图.md)。
- DSL 实作练习可挂 [../Kotlin_Cookbook/00-总览与阅读地图.md](../Kotlin_Cookbook/00-总览与阅读地图.md)。

## 中英对照

| 中文 | 英文 | 一句定义 |
| --- | --- | --- |
| 作用域函数 | scope functions | let/run/with/apply/also：临时给对象开块作用域。 |
| 带接收者 lambda | lambda with receiver | 块内 `this` 绑定外部对象，DSL 的引擎件。 |
| 声明处方差 | declaration-site variance | `out/in` 写在类型参数声明上，一次生效全部调用点。 |
| 使用处方差 | use-site variance | 调用点 `out T/in T`，对应 Java 通配符。 |
| 星投影 | star projection | `List<*>`：只读未知元素类型。 |
| DSL 作用域限制 | `@DslScope` | 编译期禁隐式接收者跨层访问。 |

## ⚠️ 欠账

- 原书 DSL 是否独立成部待目录销账；`@DslScope` 细则条目归属未定。
- TS 结构化类型 vs Kotlin 名义类型的"迁移期望管理"专题未立项（候选新档）。
