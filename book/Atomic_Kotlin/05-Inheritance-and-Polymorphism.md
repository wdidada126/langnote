# 《Atomic Kotlin》课带 05 继承与多态（第 50–59 课）——被收紧的 OOP 老刀

> 三态标注：✅ 本仓已核实条目 / ⚠️ 课名与课号系凭 leanpub/booksource 官方站体例记忆拟题（带界自拟，逐字题名与部界待销账）/ 🔧 自写示意实验，未实测（本机无 kotlinc，验证前不得声称实测）
> 画像裁定前提：Java/C++ 后端老手。继承/多态概念零起点部分一律标已通，本带只算 Kotlin 对老 OOP 纪律的三处收紧。

## 一、课带地图（第 50–59 课，共 10 课）

| 课 | 拟题（⚠️ 待逐字销账） | 一行要点 |
|---|---|---|
| 50 | Inheritance Basics | `open` 才可继承：默认 final 的立场反转 |
| 51 | Superclass & Any | 万物之源 Any（≈ Object），无根类义务 |
| 52 | Overriding | `override` 必写；方法/属性均可覆写 |
| 53 | Polymorphism | 上转型自由、按对象实际类型分派 |
| 54 | Abstract Classes | abstract 成员隐式 open ⚠️ 细节待核 |
| 55 | Interfaces | 可带默认实现；属性只能抽象/计算，无状态 ⚠️ |
| 56 | Multiple Inheritance via Interfaces | 多接口实现与冲突消解 `X.super.y()` |
| 57 | Type Tests: is / as | instanceof 与 downcast，`is` 后自动收窄 |
| 58 | Sealed Hierarchies Revisited | 回收 03 带 sealed：封闭继承树+穷尽 when |
| 59 | Summary | 部练习与收束（⚠️ 归属部界待对齐） |

## 二、画像裁定（Java/C++ 后端视角）

- **已通，略**：里氏替换、虚分派、纯虚函数=abstract、接口默认实现（Java 8 / C++ 抽象类惯用法）——概念层零增量。
- **增量 1——默认 final（50）**：C++ 类默认开放继承、Java 默认开放，Kotlin **类与成员都默认 final**，继承要点两次火（`open class` + `open fun`）。裁决：这正是 Effective Java "design for inheritance or forbid it" 的语言化，C++ 老手要放弃"随手派生"肌肉记忆 ⚠️。
- **增量 2——override 必写（52）**：C++11 `override` 是可选保险，Kotlin 是强制关键字；同时 **Kotlin 无协变返回之外的 C++ 签名分叉坑**，也没有名字遮蔽（non-virtual shadowing）问题——因为默认不可隐式覆写 ⚠️。
- **增量 3——无状态接口（55）**：接口属性只能 `val x get() = ...` 或抽象，不允许像 C++ 那样在"接口类"塞数据成员；构造初始化列表文化整体缺席。裁决：要状态就 abstract class，Java 程序员会觉面熟（≈interface 字段只能 static final）⚠️。
- **增量 4——is/as 与安全收窄（57）**：`if (x is Dog)` 分支内 x 自动按 Dog 看（智能转换，机制细账在 06 带）；对照 C++ `dynamic_cast` 判空二连与 Java instanceof 强转两行半。`as` 失败抛 ClassCastException ≈ dynamic_cast 引用版；`as?` 给 null 不抛 ⚠️ 是否有专课待核。
- **增量 5——多继承冲突消解（56）**：`interface A { fun f() = 1 }; class C : A, B, { override fun f() = super<A>.f() }` 语法与 Java 8 菱形默认冲突同题，Kotlin 强制显式择源 ⚠️。C++ 虚基类机制整体不需要。

## 三、🔧 微实验设计（未实测）

1. **`openfinal.kt`**：继承非 open 类预期编译错误；成员不加 open 则子类 override 预期编译错误。**目的**：两级开关亲手碰。
2. **`shape.kt`**：abstract Shape + area()，List<Shape> 多态遍历断言总面积。**目的**：快跑老概念，验证语法手感。
3. **`diamond.kt`**：两接口同名默认方法，类不覆写预期编译错误；`super<A>.f()` 消解通过。**目的**：菱形冲突的强制显式。
4. **`isas.kt`**：`val d = a as? Dog ?: return`，与 `is` 分支智能转换对照输出；错误 `as` 观察异常。**目的**：downcast 三通道。
5. **`sealed_tree.kt`**：sealed Expr（Num/Add/Neg）+ evaluate 用 when 穷尽，删一支预期编译错误。**目的**：表达式代数的解释器惯用法。

## 四、盘谱互链（磁盘 ls 实测 ✅）

- 主对位：[../Learning_TypeScript/04-接口与结构类型.md](../Learning_TypeScript/04-接口与结构类型.md)——TS interface 是**结构类型**：形状吻合即兼容，无 `implements` 声明也成立；Kotlin 名义继承必须显式 `: Shape`，跨库类型形状全同也不互认。两条路线的取舍（演化宽松 vs 意图明确）在 TS 档内有裁决文，本带所有"接口"实验都值得各跑一遍双证。
- 联合收窄参照：[../Learning_TypeScript/05-联合类型与收窄.md](../Learning_TypeScript/05-联合类型与收窄.md)——`is` 收窄 ≈ TS `typeof/in` 类型守卫。
- 兄弟带：上一带 [04-Collections-and-Loops.md](04-Collections-and-Loops.md)，下一带 [06-Nullable-Types-and-Errors.md](06-Nullable-Types-and-Errors.md)。

## 五、核心概念中英对照

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 开放修饰 | open | 显式解锁继承/覆写的开关 |
| 覆写标记 | override | 强制声明"我在替换父成员" |
| 上转型 | upcast | 子到父隐式安全转换 |
| 向下转型 | downcast (as) | 父到子需运行时校验 |
| 类型测试 | is (type check) |  instanceof 的中缀化，触发收窄 |
| 可空转换 | as? | 失败返回 null 而非抛出 |
| 抽象类 | abstract class | 可带状态与实现的不可实例化类 |
| 菱形冲突 | diamond problem | 多接口默认实现的来源歧义 |
| 封闭继承树 | sealed hierarchy | 子集编译期已知，支持穷尽 |
| 超源限定 | super<T>.m() | 指名取哪条继承链的默认实现 |

## 六、⚠️ 欠账

- 50–59 逐字题名待销；sealed/智能转换可能在官方目录属 Nullable 部，本带 57/58 或要搬家。
- 泛型方差（in/out）刻意押到 08 带，官方若以专章置于Ⅴ部 Abstract Data Types，部界对照表要重做。
- 接口可有初始化器（`val x get()=...` 依赖构造序）细节未核。
