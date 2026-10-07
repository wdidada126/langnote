# 《Learning TypeScript》章笔记 06 · 泛型与 tsconfig 入门

> 对应 [00-总览与阅读地图.md](00-总览与阅读地图.md) 骨架 **Ⅳ 泛型与配置段**（Ⅴ 工程段另立欠账）。
> ⚠️ 章名「泛型与 tsconfig 入门」为按书记忆的主题带命名（generics 章 + tsconfig 相关内容），非逐字章名。
> 三态：**✅** = 本机实测（node v22.14 strip-types，脚本 `/tmp/lts_exp/exp06.ts` 及三个 boundary_*.ts）；**⚠️** = 凭记忆；**🔧** = 未实测。

## 核心机制

- **泛型是四语言里擦得最狠的一档**：✅ 实测：`function first<T>(xs: readonly T[])` 的
  `first.toString()` 打印 `function first (xs ) { return xs[0]; }`——类型参数原地变空白，
  `first.length = 1`，对 `[7,8]` 与 `["a","b"]` 同一份机器码服务；`class Box<T>` 实例自身
  属性只有 `['v']`，无任何型参留存。对照专题档第二节总表：**Java 桥方法+Class 元数据尚存、
  Kotlin reified 可内联逃逸、C++ 单态化直接生成多份真码，TS 是零留存**。
- **约束 `extends` 是给检查器的下界**，运行时不生成任何形状验证；默认型参 `T = string`
  同样纯编译期 ⚠️。Java 有类型擦除后的桥接与反射残骸可捞，Kotlin 可在 inline 函数里
  `reified T` 真问 `x is T`——TS 里想要「运行时知道 T」只能把 T 的 schema 当值传参
  （专题档推论 3 再现）。
- **tsconfig 是编译器的行为合同不是运行时开关**：`strict` 是家族开关（内含
  `strictNullChecks`、`noImplicitAny`、`strictFunctionTypes` 等 ⚠️ 名单凭记忆，以官方文档
  为准），全部只影响「你写代码时红不红波浪线」，改任何一项产物 JS 一字不变。⚠️ 机制推论
  （由零留存公理直接得出；逐开关 diff 产物未实测 🔧）。
- **混合带语法会产码——三条界碑本会话实测销账**：✅ `enum`、`namespace`、参数属性
  （`constructor(public v: T)`）均被 strip-only 拒跑，报
  `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`（原文含 "enum is not supported in strip-only mode" 等），
  exit=1——因为这三者编译后要**生成真 JS**（枚举对象/IIFE/赋值语句），违背纯擦除，
  故成迁移工具兼容地雷（专题档推论 4 由此从 ⚠️ 升 ✅）。

## 批判读法

- 入口书的 tsconfig 是「认字级」：只教最小可用集，strict 家族逐开关语义要留给
  50 Lessons/Effective 谱系回补；别把本书配置面当全貌。⚠️ 口径归纳。
- 泛型章通常止于函数/类型参与约束；变型标注（`in`/`out`）、高阶泛型推断的坑都在本书
  边界外——读到「`extends` 完事」别停在这里 satisfies/推断失败才是工程常态。⚠️。
- 若你从 Java 泛型来：`List<T>` 的协变直觉（`List<Integer>` 不是 `List<Number>`）在 TS
  数组上表现不同（不变 ⚠️ 记忆），而函数参数双变更反直觉——配置章与泛型章连读才能校准。

## 🔧 微实验

- ✅ 已实测（exp06.ts，exit=0）：泛型函数 toString 见裸 JS、`Box` 实例零型参痕迹、
  深层 type 别名（`ReadonlyArray<Record<string, Box<number>>>`）值面就是 `[]`。
- ✅ 已实测（boundary_enum/boundary_ns/boundary_pp.ts，均 exit=1 拒跑）：产码语法三条
  界碑确认，专题档第五节「enum 转译产物阅读」欠账的部分前置销账。
- 🔧（未实测）`tsc --strict` 与逐项开关（strictNullChecks/noImplicitAny 等）的报错矩阵、
  enum 编译产物 JS 阅读——本机无独立 tsc，见 00 档第四节，禁止引用报错文案为实测。

## 盘谱互链

- 擦除总表与推论 3/4 出处：[../TypeScript系列·Runtime_vs_Type_System专题.md](../TypeScript系列·Runtime_vs_Type_System专题.md)。
- 骨架档 Ⅳ/Ⅴ 段与实测口径：[00-总览与阅读地图.md](00-总览与阅读地图.md)。
- Java 擦除对照（桥方法/反射残骸）：[../深入解析Java虚拟机HotSpot.md](../深入解析Java虚拟机HotSpot.md)、
  [../Java_to_Kotlin/02-从Java类到Kotlin类.md](../Java_to_Kotlin/02-从Java类到Kotlin类.md)。
- Kotlin reified 谱系位置：[../Kotlin系列·总索引.md](../Kotlin系列·总索引.md)。
- C++ 单态化对照：[../C++语言的设计与演化.md](../C++语言的设计与演化.md)；配置深水区下游：
  [../TypeScript_in_50_Lessons/00-总览与阅读地图.md](../TypeScript_in_50_Lessons/00-总览与阅读地图.md)、
  [../TypeScript_Cookbook/00-总览与阅读地图.md](../TypeScript_Cookbook/00-总览与阅读地图.md)、
  [../TypeScript_Compiler_Notes/00-总览与阅读地图.md](../TypeScript_Compiler_Notes/00-总览与阅读地图.md)。

## 中英对照表

| 中文 | 英文 | 一句定义 |
| --- | --- | --- |
| 类型参数 | type parameter | `<T>` 占位符；TS 中运行时零留存 ✅实测。 |
| 泛型约束 | generic constraint | `T extends U` 下界登记，仅编译期生效 ⚠️。 |
| 类型子参 | type argument | 调用处填实 `<number>`；显式或推断而来。 |
| 可具化 | reified | 类型参数留存为运行时信息；Kotlin 可，TS 永不可 ✅机理。 |
| 单态化 | monomorphization | C++ 对照物：每型参实例化生成真实代码，非擦除。 |
| 严格模式族 | strict family | tsconfig 开关组，只改编译期红线不改产物行为 ⚠️名单待核。 |
| 产码语法 | emit-producing syntax | enum/namespace/参数属性：违背纯擦除，strip-only 拒 ✅实测。 |

⚠️ 欠账：逐字章名；strict 家族开关全名单与语义（待官方文档+tsc 实测）；变型/推断深坑
超出本书范围确认；`--experimental-transform-types` 对三界碑的转译面未测。
