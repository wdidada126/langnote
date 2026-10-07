# TypeScript 系列·总索引

> 2026-10-07 开波。本文件是 `book/` 下 TypeScript 系列的总索引，收录用户书目表内 **10 本**主流英文书 + 社区文档线。
> 元数据状态标注：✅ 已核实（含本会话联网/本机实测出处）｜⚠️ 待核验（凭记忆或二手，不写死）｜📄 来自既有笔记｜⛔ 时效警戒。
> 使用约定：只做导航与元数据归档，不改动各书正文笔记；新增书目按分表追加并同步「收录统计」。

## 读者画像与路线（本系列定位）

本系列面向**已有 Java/C++/Kotlin 后端经验**的工程师：重点不是"学语法"，而是把 **结构类型系统 + 类型擦除运行时** 这两条与 JVM/C++ 根本不同的公理装进已有心智模型，再分型别体操、工程规范、编译器实现三条专项线推进。

阅读顺序（采纳用户粘贴的第三方建议，含本仓校正）：

1. **入门**：Learning TypeScript（结构类型心智建模最快）。
2. **主干**：Programming TypeScript（类型系统纵深）→ Effective TypeScript 2e（工程规范，条目式，对位 Effective Java/Kotlin）。
3. **实战**：TypeScript Cookbook（问题驱动）↔ TypeScript in 50 Lessons（体系化短课）。
4. **专项·类型体操**：Type-Level TypeScript——与本仓 `C++20模板元编程/` 合读（条件类型/映射类型 ≈ 模板特化/SFINA/概念约束的类型级对偶）。
5. **专项·实现线**：TypeScript Compiler Notes（社区档）+ 官方 `microsoft/TypeScript` 源码与 spec。
6. ⛔ **校正**：Pro TypeScript（2012，TS 0.8 时代）不进主线，仅作「前类型注解时代」考古；Essential TypeScript 5 定位为大而全参考书，按需查章不线性读。

## 本系列独有的两条专项线

- **核心概念清单**（各书分章档按此互链）：结构类型（structural typing）、联合/交叉类型、控制流收窄（narrowing）、条件类型、映射类型、`keyof`/索引访问、模板字面量类型、`infer`、分发式条件类型。
- **Runtime vs Type System 专题**（type erasure，TS 与 Java/Kotlin/C++ 的根本分歧点）：
  - 本波已本机实测 ✅（见下「实测基线」），分章档中该专题以实测为准、书目说法为辅。

## 一、书目主表

| 书 | 目录 | 出版社·年份 | ISBN | 优先级 | 状态 |
|---|---|---|---|---|---|
| Learning TypeScript | [Learning_TypeScript/](Learning_TypeScript/00-总览与阅读地图.md) | O'Reilly·2022 | ⚠️待核验 | ★★★ 入口 | ✅ 作者 Goldberg 双源佐证 |
| Programming TypeScript | [Programming_TypeScript/](Programming_TypeScript/00-总览与阅读地图.md) | O'Reilly·2020 | ⚠️9781492052187 | ★★★ 主干 | ⚠️（403 墙） |
| Effective TypeScript 2e | [Effective_TypeScript_2e/](Effective_TypeScript_2e/00-总览与阅读地图.md) | O'Reilly·2024 前后 | ⚠️待核验 | ★★★ 规范 | ✅ 2e 条目数 83（中文版书名直证 1e=62 → 2e=83） |
| TypeScript Cookbook | [TypeScript_Cookbook/](TypeScript_Cookbook/00-总览与阅读地图.md) | O'Reilly·2024 | 9781098136659（题名强匹配）| ★★ | ⚠️ 作者归属待核（第三方称 Baumgartner） |
| TypeScript in 50 Lessons | [TypeScript_in_50_Lessons/](TypeScript_in_50_Lessons/00-总览与阅读地图.md) | Manning·2022 | ⚠️9781617298561 | ★★ | ⚠️（Manning 本波 404，未破墙） |
| Tackling TypeScript | [Tackling_TypeScript/](Tackling_TypeScript/00-总览与阅读地图.md) | 自出版·2021 | ⚠️ | ★★ | ⚠️（免费在线版归属 exploringjs 待核） |
| Type-Level TypeScript | [Type_Level_TypeScript/](Type_Level_TypeScript/00-总览与阅读地图.md) | 独立出版·2023 前后 | ⚠️ | ★★ 专项 | ⚠️ 作者 Vergnaud（第三方名录，未见官方页直证） |
| Essential TypeScript 5 | [Essential_TypeScript_5/](Essential_TypeScript_5/00-总览与阅读地图.md) | Apress·2023 前后 | ⚠️ | ★ 参考书 | ⚠️（图书馆藏记录仅证 "Essential TypeScript" 存在） |
| Pro TypeScript | [Pro_TypeScript/](Pro_TypeScript/00-总览与阅读地图.md) | Apress·2012 | ⚠️ | ⛔ 仅考古 | ⚠️ TS 0.8 时代，内容大面积失效 |
| TypeScript Compiler Notes | [TypeScript_Compiler_Notes/](TypeScript_Compiler_Notes/00-总览与阅读地图.md) | GitHub 社区 | — | ★ 实现线 | ⚠️ 仓库 URL/作者本波未定位，档案为占位警示档 |

## 二、第三方书目清单核对结果（2026-10-07）

- 十本**书名-作者配对全部真实存在** ✅（无 Kotlin 波遇到的 "DeVore" 型硬伤）；但三处需按本仓证据修正口径：
  - **Effective TypeScript 第二版=83 条**：1e 中文版《精进TypeScript代码的62个实践方法》ISBN 9787519859381，2e 中文版书名即《…83个实践方法（第二版）》——第三方未给条目数，本仓记 ✅ 83。
  - **Learning TypeScript 有中文版**《学习 TypeScript》（机工系寄藏书号 979-8341-658196 线），作者 Josh Goldberg 双源（孔夫子书目+O'Reilly 中文库页面）佐证 ✅。
  - **Pro TypeScript 时效 ⛔**：2012 年基于 TS 0.8 写作，早于泛型推断、收窄、映射类型等一切现代机制——第三方把它排进推荐序列属于**过时书单**，本仓降为考古位。
- 未破墙（403/404/噪音）维持 ⚠️：Programming TS、50 Lessons、Cookbook 作者、Tackling、Type-Level、Essential、Compiler Notes 的 ISBN/逐字目录——购电子版或换网段后销账。

## 三、实测基线（本机 node v22.14，`--experimental-strip-types`）✅

- 类型注解/interface/`implements` 运行时**整体擦除**：`type`、`interface` 声明的绑定在运行时不存在（与 Java 泛型擦除同族，但 TS 是**全类型层擦除**）。
- TS `private` 是**纯类型层**修饰符：字段运行时仍在（`"secret" in new A()` → true），与 JS 原生 `#field`（真私有，不出现在 `getOwnPropertyNames`）**语义层级不同**。
- 类型**不参与**任何运行时形状：`f.length`（元数）等 JS 反射事实不因类型注解改变。
- `--experimental-strip-types` **只删注解不做检查**：`const n: number = "x"` 照常运行——校验是 `tsc`/编辑器（编译期）的职责，运行时零保护。这是「Runtime vs Type System」专题的第一手证据。
- ✅ 边界（第 2 波已销）：`enum`/`namespace` 等非纯擦除语法（需转译产码）strip 模式实测**拒载**（exit=1），`--experimental-transform-types` 实测**放行**（exit=0）——两制边界均有本机复演记录，见专题档第五节；`tsc` 报错矩阵仍 ⚠️（本机无独立 tsc，留购装后销账）。

## 四、与既有系列的衔接

- **结构类型 vs 名义类型**：对照 Java 名义泛型、Kotlin `data class`——`Java_to_Kotlin/`、`Spring系列·总索引.md` 互链；类型兼容判定树是本系列与 JVM 系最大分歧档案。
- **类型擦除对照**：Java 泛型擦除（桥方法/ClassCastException 位点）↔ TS 全类型擦除 ↔ C++ 模板单态化（类型生成代码，运行时无类型层）——`C++语言的设计与演化.md`、`C++20模板元编程/` 谱系位。
- **类型级计算**：条件类型/映射类型/`infer` ↔ C++20 concepts/SFINA/模板特化——与 `C++20模板元编程/` 分章档对读（Type-Level TS 是本仓第二本「类型即程序」档）。
- **Kotlin 对照**：可空类型（`?`/strictNullChecks）↔ Kotlin `?`/平台类型；联合类型 ↔ sealed class；narrowing ↔ 智能转换（`Effective_Kotlin/` Ⅱ 部对位）。

## 收录统计

- 2026-10-07 第 1 波：10 本书目全部建档（各 1 枚 00-总览与阅读地图）+ 本总索引 + 本机 type-erasure 实测基线 4 条 ✅。全系列 11 枚档案。
- 2026-10-07 第 2 波收束 ✅：9 路泳群 46 枚分章档全落盘（Learning 6/Programming 6/Effective 6/Cookbook 6/50Lessons 4/Tackling 5/Essential 5/Pro 3/Type-Level 5；Compiler Notes 按「先销账后读」纪律不展开）——**全系列 56 枚档案、断链扫描 0**。泳群合计真跑复演 ~70 次（全部 node v22.14 strip/transform 双制），实测基线新增：
  - 非纯擦除语法拒载面由 enum/namespace 扩至**参数属性、`import = require()`、装饰器**（装饰器 legacy/Stage-3 双写法 × strip/transform 双模式四组合**全判负**＝Node 不译装饰器且不读 tsconfig，主代理已独立复现）；
  - `as const` **不产生 Object.freeze**、`const enum` 在 Node transform 下**不内联**（运行时留绑定）——`isolatedModules`/`erasableSyntaxOnly` 语义边界自此有了运行面代理实锤；
  - enum 转译产物=双向映射对象 `{"0":"Red","Red":0}`；`node:http` 服务端线**零 node_modules/零 @types 直跑全绿**——「运行时不做类型解析」一手证据。
- 待办：O'Reilly/Apress/Manning 各墙 ISBN·逐字目录联网销账；TypeScript Compiler Notes 仓库定位（销账失败按 Mobedi 先例转 ⛔ 注销档）；tsc 报错矩阵（待 typescript 安装授权口径）；各书分章档内 ⚠️ 欠账逐档滚动。
