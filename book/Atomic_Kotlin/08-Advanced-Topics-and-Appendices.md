# 《Atomic Kotlin》课带 08 进阶主题与附录（第 80–87 课 + 附录 A/B）——表达式力、方差与互操作还账

> 三态标注：✅ 本仓已核实条目 / ⚠️ 课名与课号系凭 leanpub/booksource 官方站体例记忆拟题（带界自拟，逐字题名与部界待销账）/ 🔧 自写示意实验，未实测（本机无 kotlinc，验证前不得声称实测）
> 画像裁定前提：Java/C++ 后端老手。本带收全书最后增量与前七带挂账：operator conventions（01 带埋线 ✅）、`to`/Pair（02 带埋线 ✅）、平台类型 `T!`（06 带埋线 ✅）、方差专账（00 带公评 ✅）。

## 一、课带地图（第 80–87 课 + 附录两枚，共 10 行）

| 课 | 拟题（⚠️ 待逐字销账） | 一行要点 |
|---|---|---|
| 80 | Extension Functions | 给既有类型外挂成员函数，静态帮助类文化的终结 |
| 81 | Operator Conventions | `operator fun plus/get/contains`：+ 与 [] 背后的命名约定 |
| 82 | Infix Functions | `infix fun` 中缀调用，`a to b`/`step`/`downTo` 全族还账 |
| 83 | Generics | `<T>` 型参与 reified 缺口 ⚠️ 是否涉及时另核 |
| 84 | Variance: in & out | 声明位协变逆变：out=产出位、in=消费位 |
| 85 | Delegated Properties | `by lazy/by map` 属性级委托（区别于 03 带类委托） |
| 86 | DSLs / Type-Safe Builders | 接收者 lambda+invoke 约定拼小型内部 DSL ⚠️ 待核 |
| 87 | Summary | 全书收束与最终练习 |
| App A | AtomicTest 库 | 教学断言库 API 全目录：`test/check/expect` ⚠️ 逐字待核 |
| App B | Kotlin and Java | 互操作：平台类型、@JvmStatic/@JvmOverloads、FileKt 命名 |

## 二、画像裁定（Java/C++ 后端视角）

- **已通，略**：泛型/模板基本概念（两门老语言皆熟）；"运算符重载"的语义设计直觉（C++ 老本行）；单测概念与 JUnit 生态。
- **增量 1——扩展函数（80）**：`fun String.shout() = uppercase()+"!"` 编译为静态工具方法但语法如成员——对标 C++ 自由函数+ADL 的组合，但**可空接收者**扩展（`T?.orEmpty()`）是 C++/Java 都没有的档位；与 Java 静态 helper（StringUtils）同物不同皮。注意：**不可覆写、解析优先级低于真成员**⚠️。
- **增量 2——运算符约定（81）**：C++ 可造任意 operator 语义；Kotlin 只发放**固定名单**（plus/times/get/iterator/contains…）且优先级全固定（同为左结合、优先级由语言钦定）——裁决：这是刻意的反 C++ 立场，消灭自定义 `%` 类野语法 ⚠️。01 带"位运算是函数名 and/or/inv"的挂账在此结清 ⚠️ 结论待核。
- **增量 3——声明位方差（84）**：Java 通配符是用位（`List<? extends T>`），Kotlin `interface Iterable<out T>` 一劳永逸写在声明上；C++ 模板无方差概念（靠约定）。00 带评"本仓公认强段"✅ 立场保留：读熟 out/in 再回头看 Java PEES 会退化成肌肉厌恶 ⚠️。
- **增量 4——属性委托（85）**：`val config by lazy { ... }` 惰性初始化+`Delegates.observable`；Java 要靠供应商模式 Supplier 缓存手写，C++ mutable+std::call_once 苦修。与 03 带**类委托**（by 转发接口实现）是同一 `by` 关键字的两次分身 ⚠️。
- **增量 5——附录 B（互操作）**：混合工程日常：Java 集合在 Kotlin 眼里的可空豁免（平台类型 `T!` 终账）、顶层函数编译成 `文件名Kt` 类（01 带埋线 ✅ 兑现）、`@JvmOverloads` 生成重载供 Java 调用方看全默认参数、SAM 双向转换。**这是本画像全带最高价值段**——其余多为语言内政 ⚠️。

## 三、🔧 微实验设计（未实测）

1. **`ext.kt`**：给 `Int` 挂扩展 `fun Int.isEven()`；同类型挂**同名真成员**观察成员优先解析；再写 `String?.orEmpty()` 风格可空扩展。**目的**：扩展=静态解析不是虚分派。
2. **`oper.kt`**：自定义 `class Vec` 实现 `operator fun plus/minus/unaryMinus/get`，验证 `+`、`-v`、`v[0]` 语法可用；试造 `operator fun "%"` 预期**不存在该名单**编译失败。**目的**：固定名单纪律。
3. **`variance.kt`**：`fun f(list: List<Any>)` 传 `listOf(1,2)` 通过（List 声明 out）；换 `MutableList<Any>` 传 `mutableListOf(1)` 预期编译错误。**目的**：可变异方差的危险与语言把关。
4. **`lazydel.kt`**：`val x by lazy { println("init"); 42 }` 两次读取观察只算一次；对照 `by Delegates.observable` 记录写序。
5. **`jvmshape.kt`**：kotlinc 产出 jar 后 `javap` 看顶层函数落成的 `FileKt` 类与 companion 的静态字段形态（javap 属 JDK 工具，本机有 JDK ⚠️ 亦未实测本轮）。**目的**：附录 B 的字节码真相。

## 四、盘谱互链（磁盘 ls 实测 ✅）

- 主对位：[../Learning_TypeScript/06-泛型与tsconfig入门.md](../Learning_TypeScript/06-泛型与tsconfig入门.md)——TS 泛型**只有结构型兼容**（协变到处放行、缺 in/out 声明位控制），Kotlin 名义谱系里方差必须显式声明；两侧"数组协变安全性"议题可对照清算。
- 互操作镜像：[../Learning_TypeScript/04-接口与结构类型.md](../Learning_TypeScript/04-接口与结构类型.md)——TS 与 JS 生态"类型即形状、互操作零成本"vs Kotlin/Java"名义类+专用注解桥接"，附录 B 是本仓 JVM 线的互操作主账本。
- 系列挂账：[../Kotlin系列·总索引.md](../Kotlin系列·总索引.md)、KiA2e 方差章冲突裁决以 [../Kotlin_in_Action_2e/00-总览与阅读地图.md](../Kotlin_in_Action_2e/00-总览与阅读地图.md) 为准（00 带立场 ✅）。
- 兄弟带：上一带 [07-Lambdas-and-Functional-Style.md](07-Lambdas-and-Functional-Style.md)；全带总览 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 五、核心概念中英对照

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 扩展函数 | extension function | 外挂载于既有类型的函数 |
| 可空接收者 | nullable receiver | 扩展可声明在 T? 上 |
| 运算符约定 | operator conventions | 符号与 operator fun 名字的映射表 |
| 中缀函数 | infix function | `a op b` 式双参调用约定 |
| 协变 | covariance (out) | 子型实参可替换的产出位方差 |
| 逆变 | contravariance (in) | 反方向的消费位方差 |
| 站点方差 | declaration/use-site variance | Kotlin 声明位 vs Java 用位通配 |
| 属性委托 | delegated property | get/set 转发给委托对象的 by 机制 |
| 惰性求值属性 | by lazy | 首读才算、线程安全默认 ⚠️ |
| 平台类型 | platform type (T!) | Java 值入 Kotlin 的可空豁免态 |
| 互操作注解 | @JvmStatic/@JvmOverloads | 面向 Java 调用方的形态整形 |

## 六、⚠️ 欠账

- 80–87 逐字题名待销；DSL/reified/invoke 约定可能不在官方正文，届时本带缩为 6–7 课+补充注记。
- 附录 A AtomicTest 的逐字 API（test/expectTrue 等命名）未核——前七带全部 🔧 实验的断言写法依赖此账，销账后统一回改。
- 附录 B 是否含 build tool/模块映射细节未核；`kotlinc -classpath` 与 javap 实验待有网/有 JDK 环境实测。
- 00 带Ⅴ段"并发入门/协程引子"在本 87 课目录中无处安放——待逐字目录核实后决定并入 86 课注记或另开补带。
