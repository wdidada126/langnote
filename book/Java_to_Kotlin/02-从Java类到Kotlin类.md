# 02 · 从Java类到Kotlin类（第 3 章）

> 三态标注：✅ = 目次级事实；⚠️ = 归纳/推定（小节切分、书中实际示例类名不可逐字对照；`final class` 语法版本相关表述见内注）；🔧 = 未实测代码（以下三段对照均为本档自写的典型 Java 类风格示例，非原书代码）。

## 覆盖章目

| 产出档内主题 | 原书章号与逐字章名 |
|---|---|
| 类的惯用化 | 第 3 章 从Java类到Kotlin类 ✅ |

英文章名推定为 "From Java Classes to Kotlin Classes" 一类 ⚠️（回译）。本章是"逐章惯用化"的第一站：IDE 转换出一个 Java 味的 Kotlin 类之后，逐刀削掉。

## 机制：一个类的六刀

Java 类的身份证特征：显式构造器重载、字段+getter/setter、`equals/hashCode/toString` 手写或 IDE 生成、类默认 open 可继承、包装类型 `Integer`。第 3 章的工序逐个消解它们（⚠️ 归纳为下表工序序）。

**重构前（Java 原形）** 🔧：

```java
public class Money {
    private final long amount;
    private final String currency;

    public Money(long amount) { this(amount, "EUR"); }
    public Money(long amount, String currency) {
        if (amount < 0) throw new IllegalArgumentException("negative");
        this.amount = amount;
        this.currency = currency;
    }
    public long getAmount() { return amount; }
    public String getCurrency() { return currency; }
    // + 手写/IDE 生成的 equals、hashCode、toString（约 30 行）
}
```

**中间态（IDE 一键转换的产物——能编译、仍是 Java 味）** 🔧：

```kotlin
class Money {
    private val amount: Long
    private val currency: String

    constructor(amount: Long) {
        this.amount = amount
        this.currency = "EUR"
    }
    constructor(amount: Long, currency: String) {
        require(amount >= 0) { "negative" }
        this.amount = amount
        this.currency = currency
    }
    fun getAmount(): Long = amount
    fun getCurrency(): String = currency
    // 转换工具保留的 equals/hashCode/toString 显式覆盖
}
```

**终态（惯用 Kotlin）** 🔧：

```kotlin
@JvmInline
value class Money(private val cents: Long) {          // 单位类型：币种入域则用
    // value class 需 Kotlin 1.5+；@JvmInline 语法 1.7+ ⚠️ 版本口径以所用编译器为准
}

data class Money(                                     // 或：值语义路线，见 04 档"从Bean到值"
    val cents: Long,
    val currency: Currency = Currency.EUR,
) {
    init { require(cents >= 0) }
}
```

六刀清单（每刀都是独立可提交的一小步，⚠️ 归纳）：

| 刀 | 动作 | 章节联动 |
|---|---|---|
| 1 | 字段+构造参数 → 主构造器 `val` 属性 | 11 章（方法→属性） |
| 2 | getter 消失，`money.amount` 直接访问 | 第 11 章 |
| 3 | `equals/hashCode/toString/copy` → `data class` | 第 5 章 |
| 4 | 构造重载 → 默认参数 + 具名实参 | 第 5 章 |
| 5 | 包装类型 `Long`/`Int` → 原始类型属性；单字段包装 → value class | — |
| 6 | 隐式 `open` 心态 → Kotlin 类默认 `final`；确需继承时显式 `open` 或转 sealed | 第 18 章 |

## 老手易错点（画像：Java/C++ 经验者）

- **默认 final 是特性不是限制**：Java 人第一反应是给每个类补 `open`。判据与 C++ 一致：无虚分派需求就别付 vtable 的钱——Kotlin 默认 final 正是"零开销"的类层级版本；要开放扩展点时，优先想 sealed（封闭集，编译期穷尽）而不是 open（开放集，运行期未知）。
- **data class 滥用**：`data` 生成的是**结构相等**。实体类（有身份证相等，如数据库行）不该用 data class——两行金额相同却代表不同订单时，`==` 会撒谎。C++ 类比：`operator==` 按成员比 vs 按 handle 比。
- **`equals` 双跳**：Java 惯用的 `instanceof + getClass() == other.getClass()` 之争在 Kotlin 里由 data class 统一裁决（用 `javaClass == other.javaClass`）⚠️ 生成细节未逐字核实，建议实测（见 🔧 3）。
- **主构造器副作用**：把逻辑塞进 `init { }` 做 I/O 是坏味道——校验可以，取数不行（联动第 20 章"从执行I/O到传递数据"）。
- **`@JvmOverloads` 依赖症**：为了 Java 侧调用保留构造重载而大量加注解，是把迁移成本反向摊还；只在真正的互操作边界加。

## 🔧 微实验设计（未执行，方案自写）

1. **转换质量复测**：对同一 Java 类做 IntelliJ 转换，统计中间态→终态删除的行数（预期 equals/hashCode/toString/getter 四项占 60%+ 体积）。
2. **默认 final 实验**：Kotlin 类不加 `open`，Java 子类继承 → 观察编译错误归属方（预期：kotlinc 生成的 class 文件无 final 修饰差异需 javap 确认 ⚠️）。
3. **data class 相等语义**：子类实例与父类实例字段全同，`a == b` 与 `b == a` 是否对称？写出断言再用 `javap -c` 看 equals 里的 `javaClass` 比较。
4. **value class 互操作**：`@JvmInline value class` 作参数时 Java 侧看到的签名（预期被擦为底层类型），验证"类型安全只活在 Kotlin 侧"。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| 主构造器 | primary constructor | 与类声明同体的参数表，参数即属性 |
| 具名实参 | named arguments | 调用处写 `currency = "EUR"`，替代重载/布尔参数 |
| 默认参数 | default arguments | `val currency: String = "EUR"`，一个构造器顶八个 |
| 数据类 | data class | 生成 equals/hashCode/toString/copy/componentN |
| 解构声明 | destructuring declaration | `val (cents, _) = money`，依赖 `componentN` |
| 单位类型 | unit type / wrapper type | 用单字段类给原始类型起名（C++ strong typedef 的 Kotlin 版） |
| 值类 | value class (`@JvmInline`) | 编译期包装、运行期擦除的单位类型 |
| 结构相等 | structural equality (`==`) | Kotlin 的 `==` 调 equals，非 Java 引用相等 |
