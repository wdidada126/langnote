# 《Atomic Kotlin》课带 06 可空类型与错误处理（第 60–69 课）——把 NPE 编进类型系统

> 三态标注：✅ 本仓已核实条目 / ⚠️ 课名与课号系凭 leanpub/booksource 官方站体例记忆拟题（带界自拟，逐字题名与部界待销账）/ 🔧 自写示意实验，未实测（本机无 kotlinc，验证前不得声称实测）
> 画像裁定前提：Java/C++ 后端老手。null 的存在与 try/catch 语法零增量（02 带异常✅），本带核心是**类型层空安全**这套 Java/C++ 都没有完整对应物的机制。

## 一、课带地图（第 60–69 课，共 10 课）

| 课 | 拟题（⚠️ 待逐字销账） | 一行要点 |
|---|---|---|
| 60 | Null & Nullable Types | `T?` 是类型不是约定，非空 T 拒收 null |
| 61 | Safe Call `?.` | 链式取用：任一环节为 null 整链短路 |
| 62 | Elvis `?:` | 缺省值通道，与 `?.` 配成对 |
| 63 | Not-null Assertion `!!` | 手动解除空检查，炸点自负 ⚠️ 官方称呼待核 |
| 64 | Smart Casts | `if (x != null)` 后 x 按 T 看，无需强转 |
| 65 | Handling Null from Maps | 回收 02 带 `m[k]` 地雷终账 |
| 66 | The Nothing Type | 永不返回值的空类型：throw/exit 的类型化 |
| 67 | Common Exceptions | 异常谱系与自定义异常类 |
| 68 | Checking Requirements | require/check/IllegalArgumentException 惯用法 ⚠️ 是否专课待核 |
| 69 | Summary | 部练习与收束（⚠️ 归属部界待对齐） |

## 二、画像裁定（Java/C++ 后端视角）

- **已通，略**：null/空指针的**问题意识**（Tony Hoare "十亿美元 mistake"）；try/catch/finally 流程控制；"异常不该做控制流"的老纪律。
- **增量 1——可空是类型（60）**：Java 引用天然可空、靠文档/Optional 补救；C++ 裸指针可空但 `int` 不可空是另一维度，`std::optional<T>` 才对标 `T?`——而 Kotlin 是**语言内建**且互操作层自动生成平台类型（`T!`，附录 B 细账，08 带）⚠️。裁决：`T?` 与 `T` 不兼容是编译器铁面，老手别急着 `!!` 糊弄。
- **增量 2——三通道取用（61–63）**：`?.`/`?:`/`!!` 对应 C++ 手写判空三连与 Java Optional 的 map/orElseGet 链；`?:` 右值惰性求值（与 `||` 短路同族）。立场：`!!` 只该出现在"逻辑上不可能为 null 而类型系统不知道"处——即互操作与 lateinit 交界 ⚠️。
- **增量 3——智能转换（64）**：判空后变量自动收窄为 T，**前提是 var 在检查后不可变路径**（跨函数可变属性不转换）；对照 TS 类型守卫（互链）、C++ 无此机制、Java preview 模式匹配在路上。边界坑：`var` 可空属性智能转换失败是本书高频易错点 ⚠️。
- **增量 4——Nothing（66）**：`throw` 表达式类型是 Nothing，可参与 `val x = if (ok) 1 else throw(E())` 的类型兼容——≈ C++ `[[noreturn]]` 但进了类型代数（Any 之底）。02 带实验 4 已预热 ✅。
- **增量 5——require/check（68）**：前置条件函数族，语义分工 require=参数合法、check=状态合法，异常类型自动配套；C++20 contract 至今未产，Java 靠 Preconditions(Guava) 第三方 ⚠️。

## 三、🔧 微实验设计（未实测）

1. **`nullable.kt`**：`fun f(s: String)` 传 null 预期**编译错误**；改 `String?` 后体内 `s.length` 预期编译错误、`s?.length` 通过。**目的**：可空检查发生在编译期。
2. **`chain.kt`**：`company?.dept?.name ?: "N/A"` 三级链，逐级置 null 观察短路；同文件用嵌套 if 判空复写对照行数。**目的**：Optional 链 vs 语言语法。
3. **`smartcast.kt`**：`val s: String? = ...` 智能转换成功；换 `var` + 另一函数改值场景观察转换失败（⚠️ 预期报错，正是实验裁决点）。
4. **`nothing.kt`**：`fun fail(): Nothing = throw E()`；`val x = if (c) read() else fail()` 编译通过——Nothing 使 x 非空。**目的**：空类型参与并类型。
5. **`reqchk.kt`**：`require(n >= 0)` 与 `check(state)` 各触发一次，捕获确认异常类型分别是 IllegalArgumentException/IllegalStateException ⚠️。

## 四、盘谱互链（磁盘 ls 实测 ✅）

- 主对位：[../Learning_TypeScript/05-联合类型与收窄.md](../Learning_TypeScript/05-联合类型与收窄.md)——TS `T | null` + 类型守卫收窄与 Kotlin `T?` + 智能转换同题异构：**名义类型系统**（Kotlin：判空后静态换类型）vs **结构推断**（TS：守卫函数+控制流分析）。strictNullChecks 开关史≈Kotlin 设计立场的社区补课。
- 注解对照：[../Learning_TypeScript/01-类型注解与原始类型.md](../Learning_TypeScript/01-类型注解与原始类型.md)（`?` 后缀 vs `: T | null` 的写法经济）。
- 兄弟带：上一带 [05-Inheritance-and-Polymorphism.md](05-Inheritance-and-Polymorphism.md)，下一带 [07-Lambdas-and-Functional-Style.md](07-Lambdas-and-Functional-Style.md)。

## 五、核心概念中英对照

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 可空类型 | nullable type (T?) | 显式把 null 纳入类型域 |
| 安全调用 | safe call (?.) | 接收者 null 时短路返回 null |
| 猫王运算符 | elvis (?:) | 左 null 则取右值，右侧惰性 |
| 非空断言 | not-null assertion (!!) | 人工背书、运行期炸穿 |
| 智能转换 | smart cast | 判空/判型后编译器静默收窄 |
| 空类型 | Nothing | 无值的底类型，throw 的类型 |
| 平台类型 | platform type (T!) | Java 互操作时空性未知的豁免态 |
| 前置要求 | require/check | 参数/状态契约的标准函数族 |
| 短路求值 | short-circuit | 运算符左值定局即止 |
| 穷空检查 | null safety | 编译期禁 NPE 的整套体系 |

## 六、⚠️ 欠账

- 60–69 逐字题名待销；require/check 若官方设在Ⅶ部专章需从本带迁账。
- 智能转换对 `var`/跨模块属性的失败矩阵未逐条核官方例。
- `lateinit` 与可空性的和解位（02 带挂账"Ⅶ部回收"）归属未定，暂列本带欠账。
- 平台类型 `T!` 写法是社区称呼，官方是否用该记号待附录 B 核验。
