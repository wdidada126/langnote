# 07 · 从Visitor到代数数据类型（sealed class 位；推定位于第 7–12 或 16–18 区间，⚠️ 自拟映射）

> 三态标注：✅ = 目次级事实（23 章全目录已取得）；⚠️ = **本档章名按 [00 档](00-总览与阅读地图.md) 骨架"设计重构：visitor→密封类+when"条目自拟映射，中文版 23 章逐字对应留欠账，勿引为原文**；🔧 = 未实测（本机无 kotlinc，代码自写非原书示例）。书目：*Java to Kotlin: A Refactoring Guidebook*，McGregor & Pryce，O'Reilly 2023；中文版机工 ISBN 978-7-111-73703-2 ✅。

## 覆盖章目：visitor 章 ⚠️ 编号未核——00 档骨架明列 "visitor→密封类+when" ✅；与第 18 章（02 档所引继承/sealed 锚点）联动

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
// Negate 同构。加"操作"= 新 Visitor 实现（易）；加"节点"= 改接口+全部 accept+全部 visitor（难）。
```

**中间态（IDE 转换产物）** 🔧：类与接口直译 Kotlin，`accept`/`visit` 双分派骨架原样存活——行数没少，穷尽性仍靠人肉纪律。

**终态（代数数据类型）** 🔧：

```kotlin
sealed interface Expression {
    data class Money(val cents: Long, val currency: String) : Expression
    data class Add(val left: Expression, val right: Expression) : Expression
    data class Negate(val value: Expression) : Expression
    data object Zero : Expression            // data object 语法版本口径 ⚠️ 待核
}
fun eval(e: Expression): Long = when (e) {
    is Expression.Money  -> e.cents
    is Expression.Add    -> eval(e.left) + eval(e.right)
    is Expression.Negate -> -eval(e.value)
    Expression.Zero      -> 0L
}   // when 作表达式：编译器强制穷尽，漏分支=编译错误，无需 else
```

**重构步序**（⚠️ 归纳，每步可编译）：① 节点层级加 `sealed`（作用域随版本放宽：同文件→同模块同包 ⚠️）；② 每个 Visitor 实现改写成一个顶层 `when` 函数；③ 节点 data class 化（免费 equals/copy，联动 [04 档](04-从Bean到值.md)）；④ 无字段节点转 `data object`；⑤ 全部 visitor 函数化后删 `Visitor` 接口与 `accept`；⑥ Java 侧仍有继承者/调用方则 visitor 门面留边界层（🔧 实验 3）。

迁移对照表（⚠️ 归纳）：

| Visitor 概念 | sealed + when 对位 |
|---|---|
| 双分派（accept→visit） | `is` 检测 + 智能 cast 的 `when` |
| 节点集合"事实上封闭" | `sealed` 编译期封闭（编译器知道全集） |
| 新 Visitor 实现 = 新操作 | 新顶层函数/扩展函数 |
| 加节点→轰炸所有 visitor（人肉） | 加子类→**编译器标记所有漏 branch 的 when** |
| visitor 默认分支抛 UnsupportedOperation | 无需 else（穷尽由编译器担保） |

## 老手易错点与批判读法（画像：Java/C++ 经验者）

- **可拓展方向反转**：visitor 本意是"（含第三方）开放加操作"；sealed 把层级对模块外锁死——操作好加、节点也好加（编译器护航），**但只限本模块**。先问：有合法的外部节点贡献者吗？有则保留 open+visitor 或 sealed+边界适配——表达问题 trade-off，书选封闭集一侧（⚠️ 归纳）。
- **穷尽是编译期定理非运行期保证**：Java 继承、反序列化、RPC 都能送进"第五个成员"——与 TS 判别联合同洞：对照 [../TypeScript_Cookbook/04-判别联合与状态建模食谱.md](../TypeScript_Cookbook/04-判别联合与状态建模食谱.md) 问题 5（bogus `kind` 静默落空，该档已实测 ✅）；跨界输入要自带白名单解析器。
- **C++ 对位**：`std::variant + std::visit + overloaded` 是同一思想的类型侧实现；sealed+when 省 vtable 与 `bad_variant_access`，穷尽检查在模式侧——两边 trade-off 讨论可直接搬运。
- **别只盯 visitor**：`enum + switch` 状态机也是 ADT 化常客——状态一带载荷 enum 立刻破产，sealed 接住（00 档"sealed class 状态机化"）。

## 🔧 微实验设计（未执行，方案自写）

1. **穷尽性见证**：新增一个 sealed 节点，收集所有无 `else` 的 when 报错清单——"编译器代做维护"的账单。
2. **sealed 作用域三态**：跨文件同包/跨包同 module/跨 module 各写子类，记录报错措辞（版本相关 ⚠️）。
3. **密封是编译器视图**：`javap` 看 `PermittedSubclasses` 字节码属性（JVM 17+ ⚠️）；handler map（`Map<KClass, (E)->R>`）复刻开放 visitor，体验穷尽检查丢失后必须补 default 抛错——呼应 TS 档问题 6。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| 访问者模式 | visitor pattern | 操作与结构分离的双分派 GoF 模式 |
| 双分派 | double dispatch | accept(v)→v.visit(this) 两次动态绑定 |
| 代数数据类型 | algebraic data type (ADT) | 和类型（sealed 分支）× 积类型（data class 字段） |
| 密封类/接口 | sealed class/interface | 编译期已知全员的受限继承 |
| 穷尽 when / 智能 cast | exhaustive when / smart cast | 缺分支即编译错误；`is` 后自动收窄 |
| 表达问题 | expression problem | "加操作 vs 加类型"难两全 |

## 盘谱互链

- TS 对照主链：[../TypeScript_Cookbook/04-判别联合与状态建模食谱.md](../TypeScript_Cookbook/04-判别联合与状态建模食谱.md) ✅ 在架（判别联合/穷尽哨兵/运行时护栏三题直读）。
- 兄弟：[../Kotlin_Cookbook/02-面向对象与data-value类选型.md](../Kotlin_Cookbook/02-面向对象与data-value类选型.md) ✅、[../Kotlin_in_Action_2e/01-语言基础与结构.md](../Kotlin_in_Action_2e/01-语言基础与结构.md) ✅；本系 [04-从Bean到值.md](04-从Bean到值.md)、[02-从Java类到Kotlin类.md](02-从Java类到Kotlin类.md)（第 18 章锚点）。

## ⚠️ 欠账

- visitor 章与第 18 章的逐字章名/章号及互指关系。
- sealed 作用域放宽、`data object`、`PermittedSubclasses` 的版本口径全部 🔧 未实测（本机无 kotlinc）。
