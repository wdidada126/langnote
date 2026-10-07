# 03 · 函数与 Lambda 食谱档

> 对应 *Kotlin Cookbook*（Ken Kousen，O'Reilly，2022；⚠️ 作者"Kousen"系第三方转称未直证，ISBN/逐字目录未核不写死）函数与 lambda 章带（高阶/内联，高价值方向"内联值语义 Recipe"，见 [00 总览](00-总览与阅读地图.md)）。⚠️ 章目录 403 墙未获：本档「问题→解型」按 Kotlin 通行正解预建，Recipe 编号/逐字题名以版权页为准，不冒充书中原文。
> 三态头例：`[✅ 官方文档可证语言事实 | ⚠️ recipe 归属推定/裁决 | 🔧 未实测]`（本机无 kotlinc）。
> 仲裁延续 00：条目规范从 [Effective_Kotlin](../Effective_Kotlin/00-总览与阅读地图.md)，即查即用食谱从本书。

## 问题清单（5 问）

1. 函数类型 `(A) -> B` / `A.() -> B` 与可调用引用 `::f` 怎么写？
2. 何时该 `inline`，代价（字节码膨胀/非局部返回/二进制兼容）？
3. `reified T`：内联函数为何能摸到实类型、逃逸擦除？
4. `let/apply/run/with/also` 五兄弟选型口诀？
5. Java SAM 接口 ↔ Kotlin lambda 双向怎么转（`fun interface`）？

## 采纳裁决

- 「lambda 擦除 ↔ inline 逃逸」与 [../TypeScript系列·Runtime_vs_Type_System专题.md](../TypeScript系列·Runtime_vs_Type_System专题.md) 四语言擦除对照表互证；但该表 Kotlin 列系 ⚠️ 书档归纳（仅 TS 列 ✅ 实测）→ 本档 inline/reified 结论同降 ⚠️，待 kotlinc 字节码输出复核 🔧。
- 「嵌套 lambda 显式命名参数优于裸 `it`」等口味条目从 Effective_Kotlin ⚠️ 条目号未核。

## R1 · 函数类型与引用
`[✅ | ⚠️ 归属推定 | 🔧]`

```kotlin
fun transform(s: String, f: (String) -> Int): Int = f(s)
val f: (String) -> Int = ::transform            // 可调用引用 ✅
listOf("a", "bb").maxBy { it.length }           // lambda 位即函数类型实参
```

JVM 落 `FunctionN`、不映射 Java `Function` 家族 ✅；`A.() -> B` 接收者型是 DSL 地基（→ [04](04-DSL与属性食谱.md) R1）。

## R2 · inline 何时值得
`[✅ | ⚠️ | 🔧]`

```kotlin
inline fun timed(block: () -> Unit): Long {
    val t0 = System.nanoTime(); block(); return System.nanoTime() - t0
}
fun caller(): Long { timed { return@caller } }  // 非局部返回靠 inline 才允许 ✅
```

判据口诀"高阶包装短、调用点热才 inline" ⚠️；代价=public inline API 的二进制兼容特殊规则 ✅（细节以版本为准 🔧）。

## R3 · reified：泛型逃逸擦除
`[✅ | ⚠️ | 🔧]`

```kotlin
inline fun <reified T> List<*>.countIs(): Int = count { it is T } // 非 reified 编译不过 ✅
inline fun <reified T : Any> typeName() = T::class.simpleName
```

对照 TS 专题表：TS"零留存"、Kotlin"可逃逸的擦除" ⚠️（该列未实测）；Java 用 `Class<T>` 令牌手工化同一件事 ✅。

## R4 · scope 函数五兄弟
`[⚠️ 主裁决位 | 🔧]`

```kotlin
val cfg = Config().apply { retries = 3 }     // 配置并返回自身
val msg = cfg.render()?.let { "[$it]" }      // 判空+转换，返回新值
val out = with(theme) { "$fg/$bg" }          // 接收者上下文多表达式
users.also { println(it.size) }              // 链中插副作用，返回原对象
```

一句判别：`let/run` 产新值、`apply/also` 还本、`with`=接收者块 ✅；嵌套 ≥2 层可读性回退 ⚠️（Effective 条目号未核）。

## R5 · Java SAM 双向门
`[✅ | ⚠️ | 🔧]`

```kotlin
val r = Runnable { println("ko") }              // Java 单抽象方法接口：lambda 直转 ✅
fun interface Check { fun ok(v: Int): Boolean } // 1.4+ ✅
val c = Check { it > 0 }                        // 自家接口须 fun interface 才 SAM ✅
```

SAM 字节码形态与 `-Xsam-conversions`（class/indy）版本差异 ⚠️🔧；互操作面续 [06](06-工程与互操作食谱.md)。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 函数类型 | function type | `(A)->B`/`A.() -> B`，JVM 落 FunctionN |
| 内联函数 | inline function | 展平 lambda：零对象+非局部返回 |
| 具化类型参数 | reified type parameter | 仅 inline 可用，泛型擦除的逃逸口 |
| 作用域函数 | scope function | let/run/with/apply/also 五兄弟 |
| SAM 转换 | SAM conversion | Java 单抽象方法接口 ↔ lambda |

## 盘谱互链与 ⚠️ 欠账

- 前档：[01](01-基础与字符串集合.md) R8（lambda 解构）、[02](02-面向对象与data-value类选型.md) R9（`by lazy`）；本带主教材 [../Kotlin_in_Action_2e/02-函数与Lambda.md](../Kotlin_in_Action_2e/02-函数与Lambda.md) ✅ 磁盘实测（闭包/inline 深讲从它，本档即查即用）；DSL 去 [04](04-DSL与属性食谱.md)，suspend 地基去 [05](05-协程食谱.md)。
- ⚠️ 欠账：作者归属"Kousen"转称购版权页销账义务（与 KiA2e 第 1 波口径同批）；ISBN/逐字目录、operator 约定是否单列一章未证；本机无 kotlinc → R1–R5 全 🔧，`-Xsam-conversions` 默认值待装链实测。
