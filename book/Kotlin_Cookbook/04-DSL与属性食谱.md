# 04 · DSL 与属性食谱档

> 对应 *Kotlin Cookbook*（Ken Kousen，O'Reilly，2022；⚠️ 作者/ISBN 转称未直证不写死）DSL 与属性章带（type-safe builder/委托属性/访问器，见 [00 总览](00-总览与阅读地图.md)）。⚠️ 章目录 403 墙未获：本档「问题→解型」按 Kotlin 通行正解预建，Recipe 编号/逐字题名以版权页为准，不冒充书中原文。
> 三态头例：`[✅ 官方文档可证 | ⚠️ 归属推定/裁决 | 🔧 未实测]`（本机无 kotlinc）；仲裁延续 00：规范从 [Effective_Kotlin](../Effective_Kotlin/00-总览与阅读地图.md)，即查即用从本书。

## 问题清单（5 问）

1. 内部 DSL 三件套：接收者 lambda+工厂函数+@DslMarker 怎么搭？
2. 自定义 get/set：backing field 怎么引用才不递归？
3. 委托属性：map-backed / observable 两型怎么写？
4. `provideDelegate`：按属性名决定委托实例（Gradle 式配置位）？
5. `invoke` 与 `infix`：把"像自然语言"推到什么程度恰如其分？

## 采纳裁决

- DSL/属性属 Kotlin 类型系统层能力，[../TypeScript系列·Runtime_vs_Type_System专题.md](../TypeScript系列·Runtime_vs_Type_System专题.md) 未涉此域 → 本档无 ✅ 实测处可续引，除官方文档可证语言事实外一律 ⚠️。
- Gradle Kotlin DSL 等工程落地位归 [06](06-工程与互操作食谱.md) R5，本档只讲语言机制。

## R1 · 类型安全 builder 三件套
`[✅ | ⚠️ 归属推定：DSL 章主打 | 🔧]`

```kotlin
@DslMarker annotation class HtmlDsl()
@HtmlDsl class Tag(val name: String) { private val kids = mutableListOf<Tag>()
    fun add(c: Tag) { kids += c }
    fun render() = kids.joinToString("<$name>", "</$name>\n") { it.render() } }
fun html(block: Tag.() -> Unit) = Tag("html").apply(block)    // 工厂+接收者 lambda
fun Tag.body(b: Tag.() -> Unit = {}) = Tag("body").also { add(it); it.b() }
```

`@DslMarker` 屏蔽外层接收者、防上下文逃逸 ✅；标准库 `kotlin.html` 已移除（版本 ⚠️），自搭迷你 DSL 仍是教学/生产主力 ✅ 口径 ⚠️ 归属。

## R2 · 访问器与 backing field
`[✅ | ⚠️ | 🔧]`

```kotlin
class Temperature {
    var celsius: Double = 0.0
        set(v) { field = v.coerceIn(-273.15, 1000.0) }  // field=backing；写 celsius= 即递归 ✅
    val fahrenheit get() = celsius * 1.8 + 32           // 计算属性无 backing field ✅
}
```

访问器可见性可低于属性（`private set` ✅）；默认访问器映射 JavaBean getter/setter（→ [06](06-工程与互操作食谱.md) R2）。

## R3 · 委托属性两型
`[✅ | ⚠️ | 🔧]`

```kotlin
class Profile(val map: MutableMap<String, Any?>) {
    var name: String by map                 // 标准库 Map 委托：属性名即键 ✅
    var visits: Int by map
}
var logged: String by Delegates.observable("<init>") { _, o, n -> println("$o→$n") }
```

协议=`getValue/setValue(thisRef, property[, value])` operator 约定 ✅；[02](02-面向对象与data-value类选型.md) R9 讲"为什么"，本档给"载体"；`by lazy` 的 lambda 侧在 [03](03-函数与Lambda食谱.md)。

## R4 · provideDelegate 声明位
`[✅ 语言事实 | ⚠️ 是否书中 recipe 存疑 | 🔧]`

```kotlin
class Reading<T>(val qualified: String, val d: T)
class Key<T>(val name: String, val d: T)
operator fun <T> Key<T>.provideDelegate(r: Any?, p: kotlin.reflect.KProperty<*>): Reading<T>
    = Reading("${r}/${p.name}", d)          // 声明期拿到属性名 ✅
```

Gradle/声明式配置线（`val x by setting(...)` 模式）的机关 ✅ 官方文档可证；本书是否收录 ⚠️——可能越出 Cookbook 范围，按通行正解预建。

## R5 · invoke 与 infix
`[✅ | ⚠️ | 🔧]`

```kotlin
class Router(val base: String) { operator fun invoke(path: String) = "$base$path" }
val api = Router("https://x"); api("/users")        // 展开 api.invoke ✅
infix fun Int.pow(e: Int) = Math.pow(this.toDouble(), e.toDouble()).toInt()
val v = 2 pow 3                                     // infix=单参数、无默认 ✅
```

多接收者（`fun A.B.m(){}`）语法不存在、编译不过 ✅；invoke 重载超两个该退具名方法、DSL 语法感三件套=infix+by+接收者（口诀 ⚠️ 非书中引文）。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 类型安全 DSL | type-safe builder DSL | 接收者 lambda+工厂+@DslMarker |
| 支撑字段 | backing field | 访问器内以 `field` 引用 |
| 委托属性 | delegated property | getValue/setValue 协议接管存取 |
| 委托提供 | provideDelegate | 声明点按属性名产出委托实例 |
| 中缀函数 | infix function | `a op b`，单参数无默认值 |

## 盘谱互链与 ⚠️ 欠账

- 前档：[02](02-面向对象与data-value类选型.md) R9（属性委托机关）、[03](03-函数与Lambda食谱.md)（接收者 lambda 地基）；机制深讲从 [../Kotlin_in_Action_2e/00-总览与阅读地图.md](../Kotlin_in_Action_2e/00-总览与阅读地图.md) ✅ 磁盘实测（部Ⅱ"属性与委托/注解 DSL"带）；工程落地去 [06](06-工程与互操作食谱.md)。
- ⚠️ 欠账：作者归属（Kousen 转称）/ISBN/逐字目录购版权页销账义务；本书是否单列 DSL 章、@DslMarker/provideDelegate 是否入书未证（403 墙）；`kotlin.html` 移除版本与全部代码块 🔧 待 exp/ 落样。
