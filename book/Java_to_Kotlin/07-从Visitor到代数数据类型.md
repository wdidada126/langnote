# 07 · 从Visitor到代数数据类型（sealed class 位；章位推定第 7–12 或 16–18 区间，⚠️ 自拟映射）

> 三态标注：✅ = 目次级事实（23 章全目录已取得；01–05 档逐字章名可资对照）；⚠️ = **本档章名按 [00 档](00-总览与阅读地图.md) 骨架"设计重构段：visitor→密封类+when"条目自拟映射，中文版 23 章逐字对应留欠账，勿引为原文**；🔧 = 未实测代码（本机无 kotlinc，对照示例自写，非原书代码）。
> 书目：*Java to Kotlin: A Refactoring Guidebook*，McGregor & Pryce，O'Reilly 2023；中文版机工 ISBN 978-7-111-73703-2 ✅。

## 覆盖章目（⚠️ 推定位）

| 本档主题 | 推定原书位置 | 依据 |
|---|---|---|
| Visitor 双分派 → sealed 层级 + when 穷尽 | visitor 章 ⚠️ 编号未核；与第 18 章（02 档曾引"继承/sealed"）联动 | 00 档骨架明列 "visitor→密封类+when" ✅ |

## 机制：Java 原形 → Kotlin 翻法 → 重构步序

**Java 原形（GoF Visitor 表达式树）** 🔧：

```java
interface Expression { <R> R accept(Visitor<R> v); }
interface Visitor<R> {
    R visitMoney(Money m);  R visitAdd(Add a);  R visitNegate(Negate n);
}
final class Money implements Expression {
    private final long cents; private final String currency;
    public <R> R accept(Visitor<R> v) { return v.visitMoney(this); }
}
final class Add implements Expression {
    private final Expression left, right;
    public <R> R accept(Visitor<R> v) { return v.visitAdd(this); }
}
final class Negate implements Expression { /* 同构省略 */ }
// 加"新操作"= 写个新 Visitor 实现（易）；加"新节点"= 改接口+全部 accept+全部 visitor（难）。
```

**中间态（IDE 转换产物）** 🔧：类与接口直译成 Kotlin，`accept`/`visit` 双分派骨架原样存活——泛型 `<R>` 变 `<R>`，行数没少，穷尽性仍靠人肉纪律。

**终态（代数数据类型）** 🔧：

```kotlin
sealed interface Expression {
    data class Money(val cents: Long, val currency: String) : Expression
    data class Add(val left: Expression, val right: Expression) : Expression
    data class Negate(val value: Expression) : Expression
    data object Zero : Expression            // data object 需 Kotlin 1.9 系语法 ⚠️ 版本口径待核
}

fun eval(e: Expression): Long = when (e) {
    is Expression.Money  -> e.cents
    is Expression.Add    -> eval(e.left) + eval(e.right)
    is Expression.Negate -> -eval(e.value)
    Expression.Zero      -> 0L
}   // when 作表达式：编译器强制穷尽，漏分支=编译错误，无需 else
```

**重构步序**（⚠️ 归纳，每步可编译）：① 封闭继承——节点层级加 `sealed`（约束范围随版本放宽：同文件→同模块同包 ⚠️）→ ② 每个 Visitor 实现改写成一个顶层 `when` 函数 → ③ 节点 data class 化（免费 equals/copy，联动 [04 档](04-从Bean到值.md)）→ ④ 无字段节点转 `data object`/`object` → ⑤ 全部 visitor 函数化后删 `Visitor` 接口与 `accept` → ⑥ 仍有 Java 侧继承者/调用方时，visitor 门面保留在边界层（第 18 章继承主题联动，🔧 实验 3）。

迁移对照表（⚠️ 归纳）：

| Visitor 概念 | sealed + when 对位 |
|---|---|
| 双分派（accept→visit） | `is` 类型检测 + 智能 cast |
| 节点集合"事实上封闭" | `sealed` 编译期封闭（编译器知道全集） |
| 新增 Visitor 实现 = 新操作 | 新增顶层函数/扩展函数 |
| 加节点→轰炸所有 visitor（人肉） | 加子类→编译器**标记所有漏 branch 的 when** |
| visitor 默认分支抛 UnsupportedOperation | 不需要 else（穷尽由编译器担保） |
| `void` visit 收集返回值 | `when` 表达式直接产出值 |

## 老手易错点与批判读法（画像：Java/C++ 经验者）

- **可拓展方向反转**：visitor 的本意是"允许（含第三方的）开放加操作"；sealed 把层级对模块外锁死——操作好加、节点也好加（编译器护航），但**只限本模块**。先问：有没有合法的外部节点贡献者？有，则 sealed 是过度封闭，保留 open 接口 + visitor 或"sealed 接口 + 边界适配"是正解（表达问题 trade-off，书选封闭集一侧 ⚠️ 归纳）。
- **穷尽是编译期定理，不是运行期保证**：Java 类继承、反序列化、RPC 都能送进"第五个成员"——与 TS 判别联合同一漏洞：对照 [../TypeScript_Cookbook/04-判别联合与状态建模食谱.md](../TypeScript_Cookbook/04-判别联合与状态建模食谱.md) 问题 5（bogus `kind` 静默落空实测 ✅）；跨界输入要有自己的白名单解析器。
- **C++ 对位**：`std::variant + std::visit + overloaded` 是同一思想的类型侧实现；sealed+when 省去 vtable 与 `bad_variant_access`，穷尽性检查在模式侧而非类型别名表——两边 trade-off 讨论可直接搬运。
- **智能 cast 依赖封闭**：when 分支里 `e is Add -> e.left` 之所以可用，是 `is` 收窄的功劳；把 `eval` 拆成回调传递时收窄会丢失——用 `when` 一处判、局部 val 绑定。
- **别只盯 visitor**：枚举驱动的状态机（`enum + switch`）也是 ADT 化的常客——每状态带载荷时 enum 立刻破产，sealed 接住（00 档"sealed class 状态机化"）。

## 🔧 微实验设计（未执行，方案自写）

1. **穷尽性见证**：给 sealed 层级新增一个节点，收集所有无 `else` 的 when 报错点清单——这就是"编译器帮你做维护"的账单。
2. **sealed 作用域三态**：跨文件同包、跨包同 module、跨 module 各写一个子类，记录编译器报错措辞（版本相关 ⚠️）。
3. **密封是编译器视图**：`javap` 看 sealed 类字节码（`PermittedSubclasses` 属性，JVM 17+ ⚠️），Java 侧 `extends` 报错的归属方验证。
4. **when(is) vs 双分派**：同一表达式树两种实现各跑 10^6 次求值 + 代码行数对比 ⚠️ 预期无性能卖点，行数差才是卖点。
5. **handler map 对位**：用 `Map<KClass<E>, (E)->R>` 复刻 visitor 开放加操作，演示丢失穷尽检查后必须补 default 抛错——呼应 TS 档 handler map 问题 6。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| 访问者模式 | visitor pattern | 操作与对象结构分离的双分派 GoF 模式 |
| 双分派 | double dispatch | accept(v) → v.visit(this) 两次动态绑定 |
| 代数数据类型 | algebraic data type (ADT) | 和类型（sealed 分支）× 积类型（data class 字段） |
| 密封类/接口 | sealed class/interface | 编译期已知全员的受限继承 |
| 穷尽 when | exhaustive when | 作表达式时缺分支即编译错误 |
| 智能类型转换 | smart cast | `is` 检测后分支内自动收窄 |
| 数据对象 | data object | 无载荷单例分支的相等性友好形态 |
| 表达问题 | expression problem | "加操作 vs 加类型"两个方向难以两全 |

## 盘谱互链

- TS 对照主链：[../TypeScript_Cookbook/04-判别联合与状态建模食谱.md](../TypeScript_Cookbook/04-判别联合与状态建模食谱.md)（判别联合/穷尽哨兵/运行时护栏三题直读 ✅ 在架）。
- 兄弟：[../Kotlin_Cookbook/02-面向对象与data-value类选型.md](../Kotlin_Cookbook/02-面向对象与data-value类选型.md) ✅ 在架；[../Kotlin_in_Action_2e/01-语言基础与结构.md](../Kotlin_in_Action_2e/01-语言基础与结构.md)（when/类型系统地基 ✅）。
- 本系：[04-从Bean到值.md](04-从Bean到值.md)（节点 data class 化）、[02-从Java类到Kotlin类.md](02-从Java类到Kotlin类.md)（第 18 章继承/sealed 锚点）、[00 档](00-总览与阅读地图.md)。

## ⚠️ 欠账

- visitor 章与第 18 章的逐字章名、章号及其互指关系。
- sealed 作用域放宽、`data object`、`PermittedSubclasses` 字节码的版本口径（kotlinc/JDK 本机无，全部未实测）。
- "书中示例是否即表达式树题材"——本档示例为自写典型，非原书还原。
