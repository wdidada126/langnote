# 03 · 从Optional到nullable（第 4 章）

> 三态标注：✅ = 目次级事实；⚠️ = 归纳/推定（英文章名回译、小节切分、"书中示例类名"不可逐字对照）；🔧 = 未实测代码（三段对照为本档自写的典型风格示例，非原书代码）。

## 覆盖章目

| 产出档内主题 | 原书章号与逐字章名 |
|---|---|
| 空值建模 | 第 4 章 从Optional到nullable ✅ |

英文章名推定为 "From Optional to Nullable" 一类 ⚠️（回译）。本章是全书"类型系统接管空安全"的枢纽章：Java 用 `Optional` 把"可能没有"编码进**容器类型**，Kotlin 把它编码进**类型本身的可空标记**。

## 机制：Optional 的每一种用法都有 nullable 对应物

**重构前（Java，Optional 链）** 🔧：

```java
public String cityOf(Customer customer) {
    return findOrders(customer)                        // List<Order>
        .stream()
        .findFirst()
        .flatMap(o -> o.getDeliveryAddress())          // Optional<Address>
        .map(Address::getCity)                         // Optional<String>
        .orElse("unknown");
}
```

**中间态（IDE 转换产物——Optional 原样保留，类型满屏）** 🔧：

```kotlin
fun cityOf(customer: Customer): String {
    return findOrders(customer)
        .stream().findFirst()
        .flatMap { it.deliveryAddress }
        .map { it.city }
        .orElse("unknown")
}
// 痛点：Customer?、Optional<Address>、platform type 混杂；
// 可空性与"集合可能空"两种语义被挤在一个容器里。
```

**终态（nullable + 安全调用 + Elvis）** 🔧：

```kotlin
fun cityOf(customer: Customer): String =
    customer.lastOrder?.deliveryAddress?.city ?: "unknown"

// API 边界上的签名变化：
//   Java:  Optional<Address> getDeliveryAddress()
//   Kotlin: val deliveryAddress: Address?
```

对照表（⚠️ 归纳，逐条可作 review checklist）：

| Java Optional idiom | Kotlin nullable idiom |
|---|---|
| `Optional<T>` 字段/返回值 | `T?` |
| `.map(f)` | `?.let(f)` 或直接属性链 `a?.b` |
| `.flatMap(f)` | `f(a)?.b` 组合 |
| `.orElse(d)` / `.orElseGet` | `?: d`（Elvis） |
| `.ifPresent(r)` | `?.also(r)` 或 `?.let { }` |
| `optional.filter(p)` | `?.takeIf(p)` |
| `Optional.empty()` | `null`（在表达式里通常由 `?.` 自动产生） |
| 方法参数 `Optional<T>`（Guava 式"可缺省参数"） | 默认参数 `t: T? = null` |

关键语义点：`?.` 链在任一环节遇到 `null` 即短路，与 Optional 链等价；但 Kotlin 不强制包裹——**"可能没有"是类型的属性，不是容器的属性**。平台类型 `T!` 是迁移期特例：Java 侧无注解时 Kotlin 编译器不敢判空，惯用化推进时应逐步补 `@Nullable/@NonNull`（JSpecify/`org.jspecify` 注解 ⚠️ 具体注解包名以项目为准），把 `!` 收敛成 `?` 或 `T`。

## 老手易错点（画像：Java/C++ 经验者）

- **`!!` 是写给自己的断言**：等价于 C++ 的 UB 前置条件——编译器不帮你查，错了当场炸。review 红线：新增 `!!` 必须给出"此处 null 不可能"的注释级论据；转换工具产出的 `!!` 要逐个消灭。
- **`?.` 与 `?:` 的优先级坑** 🔧：`a?.b ?: c.foo()` 里 `?:` 右侧表达式仅在左侧为 null 时求值（Elvis 短路），但 `?.` 返回的是"链尾类型或 null"——`x?.list?.size ?: 0` 里 `size` 为 0 不是 null，不会误落 Elvis。Java 人流于 `orElse` 总求值的直觉，Kotlin 的 `?:` 右侧是惰性的，`orElseGet` 的对应物。
- **C++ 直觉直通**：`T?` ≈ `std::optional<T>`（值语义、无空指针特权），`?.` ≈ 手写 `if (opt) ... else ...` 的语法糖；差别在 Kotlin 把可空性做进了类型系统底座，任何引用类型都能带 `?`，无需包装。
- **别把 Optional 当文档**：有人迁移后仍用 `Optional` 只为"显式表达可空"——双重系统（`T?` 与 `Optional<T>` 并存）是本书点名的坏味道 ⚠️ 归纳。
- **泛型可空上下界**：`T : Any?` 才是"默认不限"，Java 人写 `<T>` 对应 Kotlin `<T>` 时若忘写 `Any?` 约束会得到 `T : Any`，把调用方的可空实参拒之门外 🔧（版本行为，建议实测）。

## 🔧 微实验设计（未执行，方案自写）

1. **短路语义验证**：`fun probe(): String? { println("called"); return null }`，测 `probe()?.length ?: error("x")` 与 Optional 版 `orElse(probe())` 的求值次数差。
2. **平台类型收敛**：同一 Java getter，分别在无注解、`@Nullable`、`@NonNull` 三种状态下被 Kotlin 调用，记录编译器给出的类型显示（`String!`/`String?`/`String`）与错误时机。
3. **`!!` 爆破点**：把转换工具自动插入的 `!!` 全部替换为显式 `?: 默认值` 或抛业务异常，diff 行为差异并跑测试。
4. **`takeIf`/`let` 等价性**：对 `optional.filter(p).map(f)` 与 `?.takeIf(p)?.let(f)` 各写 10 个用例断言同值 ⚠️ 预期等价，未实测。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| 可空类型 | nullable type (`T?`) | 类型层显式标记"可能为 null" |
| 非空类型 | non-null type (`T`) | 默认即非空，空安全是缺省而非奢求 |
| 平台类型 | platform type (`T!`) | 未标注 Java 类型的可空性未知态 |
| 安全调用 | safe call (`?.`) | null 则整链短路为 null |
| Elvis 操作符 | elvis operator (`?:`) | 左值为 null 则取右值，右值惰性 |
| 非空断言 | non-null assertion (`!!`) | 把检查责任揽回运行期 |
| 作用域函数 | scope functions (`let/also/run/with/apply`) | 围绕lambda的惯用法家族，本章主用 `?.let` |
| 条件保留 | `takeIf` | 谓词为假则整表达式为 null |
