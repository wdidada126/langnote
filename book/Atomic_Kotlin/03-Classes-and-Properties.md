# 《Atomic Kotlin》课带 03 类与属性（第 30–39 课）——从"能写类"到"写对类"

> 三态标注：✅ 本仓已核实条目 / ⚠️ 课名与课号系凭 leanpub/booksource 官方站体例记忆拟题（带界自拟，逐字题名与部界待销账）/ 🔧 自写示意实验，未实测（本机无 kotlinc，验证前不得声称实测）
> 画像裁定前提：读者为 Java/C++ 后端老手。第 30 课前的类语法已在第 02 带收账，本带只处理"类系统的增量"。

## 一、课带地图（第 30–39 课，共 10 课）

| 课 | 拟题（⚠️ 待逐字销账） | 一行要点 |
|---|---|---|
| 30 | Compound Objects | 组合优先：类持有其他类实例的协作形态 |
| 31 | Named & Default Arguments ✅（01 带已锚） | 具名实参+默认值，坍缩 Java 重载/Builder 脚手架 |
| 32 | Data Classes | `data class` 自动生成 equals/hashCode/toString/componentN |
| 33 | Copy and Immutable Update | `copy()` 带具名改动＝不可变对象的函数式更新惯用法 |
| 34 | Companion Object | 类内伴生单例：Java `static` 的 Kotlin 替身，但非真 static |
| 35 | Enumerated Types | 枚举可带属性/方法/逐常量类体，强于 Java enum 的惯用面 |
| 36 | Sealed Class | 代数数据类型：when 穷尽性检查的语言级支点 |
| 37 | Object Declaration | 顶层 `object` 单例声明，对照 Effective Java 枚举单例 |
| 38 | Class Delegation | `by` 委托实现：包装样板一行消解（装饰器/适配器减负） |
| 39 | Summary 3 | 部练习与收束（⚠️ 官方部界与本带不严格重合，销账时对齐） |

## 二、画像裁定（Java/C++ 后端视角）

- **已通，略**：类的声明与实例化、构造器与 init（第 02 带 ✅）；组合优于继承（C++/Java 常识）；枚举"可带方法"（Java enum 早就会）。
- **增量 1——具名/默认参数（31）**：Java 的 Builder 模式与 telescoping 构造器大半可删；C++20 designated initializers 是同族但只作用于聚合，Kotlin 作用于任何构造调用。裁决：布尔位参一律改写具名，`f(x = true, debug = false)` 消灭"trailing boolean 迷宫"⚠️。
- **增量 2——data class（32）**：≈ Java 16 record，但 record 是**不可变数据载体+访问器同名**，data class 属性可 var、且生成 `componentN()` 支持解构——record 无解构约定。C++ 对照：`operator==` 手写或 C++20 `= default`，toString 永远手写；Kotlin 一次 `data` 关键字全给 ⚠️。
- **增量 3——companion object（34）**：`companion object fun create()` ≈ Java static 工厂，但 companion 是**真对象**：能实现接口、能被引用（`Person.Companion`）、能加扩展。`@JvmStatic` 才降级为 JVM static（细节在 08 带附录课回收）⚠️。
- **增量 4——sealed（36）**：Java 21 的 sealed interface（JEP 410）是后补的，且穷尽检查靠 switch 模式匹配才完整；Kotlin 的 sealed + when 是教材级主食。C++ 无直接对应（variant+overload set 是苦行路线）⚠️。
- **增量 5——委托（38）**：`class LoggingList<T>(val src: List<T>) : List<T> by src` 一行顶 Java 手写 20 个转发方法；C++ 靠继承+转发构造，无语言级委托 ⚠️。

## 三、🔧 微实验设计（未实测）

1. **`dataclass.kt`**：`data class P(val x: Int)`；断言 `p == P(1)` 为真（record 语义对照：Java record 也等值，验证认知）；解构 `val (a) = p` 走 component1。**目的**：钉死 data=等值+解构双约定。
2. **`named.kt`**：四参构造器全部带默认值，调用点只写 `P(c = 5)`；对照删掉 `c =` 改位置传参的读感。**目的**：具名参的可读性红利。
3. **`sealed_when.kt`**：sealed 三子类，when 漏一支预期**编译错误**（穷尽性）；改 open 类后漏支只需 else。**目的**：sealed 是穷尽检查的开关。
4. **`deleg.kt`**：`by` 委托一个 MutableList 并只覆写 `add`，观察其余操作透传。**目的**：装饰器样板消失。
5. **`companion.kt`**：companion 实现接口 + 顶层扩展函数挂到 companion 上调用。**目的**：与 Java static 的本质分野。

## 四、盘谱互链（磁盘 ls 实测 ✅）

- 结构类型 vs 名义类对位：[../Learning_TypeScript/02-对象与数组类型构造.md](../Learning_TypeScript/02-对象与数组类型构造.md)——TS 对象字面量按**形状**匹配类型，Kotlin data class 仍是名义类：形状全同、类名不同即不兼容；解构/等值靠 componentN/生成的 equals 而非形状。
- 联合类型对照 sealed：[../Learning_TypeScript/05-联合类型与收窄.md](../Learning_TypeScript/05-联合类型与收窄.md)（06 带回收收窄机制）。
- 兄弟带：上一带 [02-Introduction-to-Objects.md](02-Introduction-to-Objects.md)，下一带 [04-Collections-and-Loops.md](04-Collections-and-Loops.md)。

## 五、核心概念中英对照

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 具名实参 | named argument | 调用点以 `参数名 =` 指定实参 |
| 默认参数 | default parameter | 形参自带缺省实参值 |
| 数据类 | data class | 自动合成等值/打印/解构/副本的类 |
| 副本更新 | copy() | 基于现有实例改部分属性造新实例 |
| 伴生对象 | companion object | 类级单例，static 的面向对象替身 |
| 密封类 | sealed class | 子类集合编译期封闭，when 可穷尽 |
| 单例声明 | object declaration | 声明即唯一实例 |
| 类委托 | class delegation (`by`) | 接口实现整体转发给被委托对象 |
| 解构约定 | componentN convention | data class 生成的位置访问函数 |
| 枚举类体 | enum class body | 逐常量定制成员 ⚠️ |

## 六、⚠️ 欠账

- 第 30/32–39 课逐字题名与官方部界对照表未销；33/37 可能并入他课。
- AtomicTest 断言形态待附录 A（08 带）核实后回改本带实验写法。
- `componentN` 与 Java record 访问器命名差异（`component1()` vs `x()`）未逐字核官方表述。
