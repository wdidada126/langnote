# 04 · 从Bean到值（第 5 章）

> 三态标注：✅ = 目次级事实；⚠️ = 归纳/推定（英文章名回译；"Bean"一词按 JavaBeans 规范义使用，书中定义表述为归纳）；🔧 = 未实测代码（对照示例自写）。

## 覆盖章目

| 产出档内主题 | 原书章号与逐字章名 |
|---|---|
| 值对象化 | 第 5 章 从Bean到值 ✅ |

英文章名推定为 "From Beans to Values" 一类 ⚠️（回译）。本章处理 Java 世界密度最高的类种群：Bean（私有字段 + 公开 getter/setter + 无参构造 + `equals/hashCode`），Kotlin 的对应解法是 **data class + copy 的不可变值**。

## 机制：Bean 的四项债务

Bean 模式的原始动机是框架反射（JavaBean 规范：可实例化、属性可读写、序列化友好）。代价（⚠️ 归纳）：

1. **中间态泛滥**：`new Foo()` 后处于"半初始化"，编译器无法保证字段齐全。
2. **可变别名**：set 随处可调，共享引用即共享突变（C++ 人熟悉的 reference aliasing 之痛）。
3. **相等性漂移**：作为 `HashMap` key 期间 set 一个参与 hashCode 的字段，条目永久失踪。
4. **样板税**：每个属性三行，N 个属性 3N 行只为表达 N 行事实。

**重构前（典型 Java Bean）** 🔧：

```java
public class Address {
    private String street;
    private String city;
    private String zip;

    public Address() {}                      // 框架要求的无参构造
    public String getStreet() { return street; }
    public void setStreet(String s) { this.street = s; }
    public String getCity() { return city; }
    public void setCity(String c) { this.city = c; }
    // zip 同理；equals/hashCode/toString 由 IDE 生成，再 40 行
}
```

**中间态（IDE 转换产物——可变属性化的 Java）** 🔧：

```kotlin
class Address {
    var street: String? = null
    var city: String? = null
    var zip: String? = null
    // 转换工具保留的 equals/hashCode/toString 覆盖
}
```

能编译，但仍是 Bean：全 `var`、全 `null` 起点、无不变式。

**终态（值对象）** 🔧：

```kotlin
data class Address(
    val street: String,
    val city: String,
    val zip: String,
)

val moved = home.copy(city = "Bonn")   // 变更 = 造新值，旧值不动
```

配套工序（⚠️ 归纳）：

| Bean 残留 | 值化动作 |
|---|---|
| 无参构造 + set 填充 | 全参主构造 + 默认参数；校验入 `init` |
| `var` 属性 | `val`；确有状态机才允许 `var` |
| 就地修改 | `copy(...)`，必要时抽私有"withX"函数表达合法迁移 |
| 深层共享突变 | 嵌套 data class 逐层 copy，或改用不可变集合（见 05 档） |
| 框架要求 Bean 形态 | 边界适配层保留一份浅 Bean，内部核心全值化 |

## 老手易错点（画像：Java/C++ 经验者）

- **这不是"Kotlin 特性"，是 C++ 早已回归的老地方**：Bean→值 ≈ C++ 从"指针语义+句柄满天飞"回到值语义（Stroustrup 的 value semantics、移动语义让值廉价）。同一判据两边通用：**能在寄存器/栈上表达的东西不要 new 到堆上让别人共享**。copy-on-change 就是 C++ copy-and-swap 的不可变近亲。
- **`copy()` 是浅拷贝**：嵌套可变成员（`var list: MutableList`）copy 后仍共享——值化必须与集合不可变化（05 档）配套，否则 data class 给你虚假的安全感。
- **`equals` 双刃**：值相等让 `a == b` 有意义，但也让"逻辑上不同、字段恰好相同"的两个实体撞车。实体（Entity）不 data class 化，判据：它有没有跨时间身份（id）。
- **`componentN` 泄密**：data class 自动解构，`val (street, city, zip) = a` 依赖**声明顺序**；重排字段是静默 breaking change（调用处不报错、结果错位）🔧 建议用实验 4 验证。
- **别用 `apply` 重建 Bean**：`Address().apply { set... }` 是 Kotlin 语法写 Java 模式；`apply` 的正当领地只在无法用构造器表达的 SDK 风格对象（如 `Intent`、线程池配置）上。
- **JPA/序列化框架的 Bean 引力**：转 Kotlin 后仍要 Bean 形态时，惯用做法是 core 层纯值 + adapter 层薄 Bean（映射一次 copy），而不是让 data class 迁就框架把 `val` 改回 `var` ⚠️ 归纳。

## 🔧 微实验设计（未执行，方案自写）

1. **hashCode 漂移复现**：Java 版 Bean 放进 `HashSet` 后 `setCity(...)`，再 `contains` → false；换 data class（不可编译 set 演示"病根在可变"）。
2. **浅拷贝陷阱**：data class 含 `val items: MutableList`，`b = a.copy()` 后改 `b.items`，断言 `a.items` 同步变化，然后改 `List`（只读接口 + `toList()`）复测。
3. **copy 成本**：JMH 或简单计时对比 `Bean 变异 10^6 次` vs `data class copy 10^6 次`（预期：GC 压力换线程安全与推理成本；数字未实测 ⚠️）。
4. **componentN 顺序敏感**：交换 data class 两字段声明顺序，旧解构代码零编译错误的实证（观察 javap 的 `component1/component2` 签名变化）。
5. **默认参数 vs 构造重载**：同一需求（3 必填 2 可选）分别用 Java 重载 5 个构造器与 Kotlin 默认参数实现，统计行数与 `@JvmOverloads` 需求。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| JavaBean | JavaBean | 无参构造+getter/setter+可序列化的规范对象 |
| 值对象 | value object / value type | 相等性由全部字段决定、不可变的对象 |
| 数据类 | data class | Kotlin 值对象的语法载体 |
| 副本变更 | copy-on-change (`copy`) | 不改旧值，造带差异的新值 |
| 函数式更新 | functional update | `copy(x = 新值)` 的同义学术名 |
| 浅拷贝 | shallow copy | `copy()` 的默认语义，嵌套可变成员仍共享 |
| 半初始化态 | half-initialized state | 无参构造+set 填充带来的非法中间窗口 |
| 边界适配层 | adapter / boundary layer | 为核心值对象兼容框架 Bean 要求的外圈 |
