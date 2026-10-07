# 《TypeScript in 50 Lessons》课带 04 · 部Ⅳ 工具链与 tsconfig

> 题注 ⚠️：课号与逐课原名以版权页为准（Manning 页本波 404 未破墙）；本档是按 TS 通行机制写的「课带地图」，不冒充书中原文。
> 证据三态：✅ = 本机 node v22.14.0 真跑（/tmp/t50/，2026-10-07）｜⚠️ = 通行机制归纳/预期形态｜🔧 = 待实测位。**本机无独立 tsc、本波禁 npm install——下方「开关→报错形态表」全部为预期形态，一律不得引用为实测。**

## 一、课带地图（部Ⅳ · 约 13 课位）

- 课位 Ⅳ-1 · tsconfig.json 定位与输入面：`files/include/exclude` 决定工程边界；无 config 裸 tsc = 目录扫 ts——一切配置讨论的场地定义。
- 课位 Ⅳ-2 · target：产物 JS 的语法下限（ES3→ESNext）；只影响降级产码不影响类型检查，`async`/可选链等按 target 决定是否拍平。
- 课位 Ⅳ-3 · lib：类型可见面与 target 解耦——「运行时能力」和「类型声明里有什么」是两本账，DOM/node 混配错位的根源。
- 课位 Ⅳ-4 · module 与 moduleResolution：ESM/CJS 产物形态 × 查找算法（node/node16/bundler）双旋钮；exports map 时代的包边界由此对齐——book 出 2022（TS 4.x 时代），bundler 档覆盖与否 ⚠️。
- 课位 Ⅳ-5 · strict 伞开关：一键拉齐 noImplicitAny/strictNullChecks/strictFunctionTypes/strictBindCallApply/strictPropertyInitialization/noImplicitThis/useUnknownInCatchVariables/alwaysStrict——「开了 strict 还报错」的答案永远是查家族展开。
- 课位 Ⅳ-6 · strictNullChecks 单点：null/undefined 从「所有类型都含」变为「独立成员」——本系列最大报错增量来源，Kotlin `?` 的开关化形态。
- 课位 Ⅳ-7 · noImplicitAny 单点：推不出类型的参数/属性报隐式 any——迁移老 JS 时第一波报错红潮的主凶。
- 课位 Ⅳ-8 · strict 家族外的进阶项：`exactOptionalPropertyTypes`（`?:` 不再自动并 undefined）、`noUncheckedIndexedAccess`（`a[i]` 类型并 undefined）——strict 伞不含它们，本表独立行。
- 课位 Ⅳ-9 · declaration 与 sourceMap：`.d.ts` 是类型的 ABI 产物面；`declarationMap` 补跳转——库作者课位。
- 课位 Ⅳ-10 · 手写声明：`declare`/ambient module/全局泄漏——第三方无类型包的接入与「声明即谎言契约」。
- 课位 Ⅳ-11 · @types 谱系：DefinitelyTyped 命名规约 `@types/pkg`、`types`/`typeRoots` 圈可见性、`typesVersions` 包内多版声明。
- 课位 Ⅳ-12 · allowJs/checkJs 渐进迁移：JS 文件入编译单元 → 只查不标 → JSDoc 当类型 → 逐文件改后缀——本书「allowJs/checkJs 渐进迁移课」课向（00 骨架钉），与用户 Java→Kotlin 迁移同题。
- 课位 Ⅳ-13 · isolatedModules/verbatimModuleSyntax 与工程化：转译器（Babel/esbuild/node strip）兼容纪律、`import type` 显式化、project references/incremental 大工程提速——收束到「编译器分工」总图。

## 二、本书特色处：tsconfig 开关→报错形态表（本系列最细配置线，主档）

| 开关 | 管什么 | 预期报错形态（⚠️ 未实测，待 tsc） | 盘谱对位 |
|---|---|---|---|
| noImplicitAny | 隐式 any 禁令 | `Parameter 'x' implicitly has an 'any' type` | Learning_TypeScript Ⅳ 段 |
| strictNullChecks | 可空独立成员 | `Object is possibly 'null'` | 对照 Kotlin `?`：Java_to_Kotlin/03 |
| strictFunctionTypes | 参数逆变检查 | 赋值处 `Types of parameters ... are incompatible` | 本册 02 band Ⅱ-11 |
| strictPropertyInitialization | 构造后必初始化 | `Property 'x' has no initializer ...` | 对照 Kotlin lateinit 剧情 |
| noImplicitThis | this 类型落地 | `The 'this' context of type ... is implicitly 'any'` | — |
| useUnknownInCatchVariables | catch 参改 unknown | 直接用 `e.message` 报 `'e' is of type 'unknown'` | 本册 02 band Ⅱ-10 |
| exactOptionalPropertyTypes | `?:` 不并 undefined | 显式赋 undefined 报 `Type 'undefined' is not assignable` | 本表独立行（伞外） |
| noUncheckedIndexedAccess | 索引读并 undefined | `a[i]` 直用报 possibly undefined 族 | 伞外进阶 |
| checkJs（配 allowJs） | JS 文件也查 | 无注解 JS 内的隐式错，形态同上数条 | 课位 Ⅳ-12 主料 |
| isolatedModules | 每文件可独立转译 | 重导出类型报 `Re-exporting a type when 'isolatedModules' ...`（须 `export type`） | strip-types 边界同款动机 ✅ |

表纪律：每行=固定样例触发一条最小报错；「预期形态」按通行报错文案记忆写 ⚠️，实跑销账后逐格改 ✅ 并回写总索引「实测基线」。

## 三、🔧 实验

✅ 实测（node v22.14.0，strip-only vs transform-types 边界矩阵，本档 4 跑；连同课带 01/02/03 共 9 跑）：

| 语法 | `--experimental-strip-types` | `--experimental-transform-types` |
|---|---|---|
| 纯擦除（type/interface/satisfies/泛型） | ✅ 跑通 exit=0 | ✅ |
| `enum` | ✅ 拒：`enum is not supported in strip-only mode` | ✅ 跑通（输出 `never 0`，enum 被**产码**成对象） |
| `namespace` | ✅ 拒：`namespace declaration is not supported in strip-only mode` | ✅ 跑通（输出 `1`，产码为 IIFE 式赋值） |
| 参数属性 `constructor(private x: number)` | ✅ 拒：`parameter property is not supported in strip-only mode` | （本波未单独跑 ⚠️） |

解读：node 两种 flag 的分工正是 Ⅳ-13 课的活教材——strip 只「删」、transform 会「造」；凡类型层语法需要运行时生成代码（enum 对象、namespace 对象、参数属性的 `this.x = x`）就跨过 strip 的界。专题档第 5 条「enum/参数属性/装饰器产码语法」由此销账两格 ✅。

🔧 待测方案（本档主案，**未实测**——需独立 tsc，本机未装 ⚠️，禁 npm install，待用户授权安装口径）：
1. 固定样例集（每开关一个最小触发文件，含隐式 any/可空/索引/可选精确/catch 参各一）；
2. 基线 `tsc --noEmit`（全默认）录报错集；3. 逐开关单开 → diff 报错增量回填第二节表；4. `strict` 伞开 → 验证家族展开=逐条并集。`allowJs+checkJs` 迁移演练追加：一个裸 JS 目录三级推进（allowJs→+checkJs→JSDoc 消错）——对位用户 Java→Kotlin 手感。

## 四、盘谱互链

- 本册骨架：[./00-总览与阅读地图.md](./00-总览与阅读地图.md)（「Ⅳ 部配置课并入总索引实测基线」读法裁决处）。
- 配置字典 heavier 版：[../Essential_TypeScript_5/00-总览与阅读地图.md](../Essential_TypeScript_5/00-总览与阅读地图.md)（其 Ⅴ 部 tsconfig 字典章与本表互证轻重）。
- 配置背后的实现语义：[../TypeScript_Compiler_Notes/00-总览与阅读地图.md](../TypeScript_Compiler_Notes/00-总览与阅读地图.md)；速查化下游：[../TypeScript_Cookbook/00-总览与阅读地图.md](../TypeScript_Cookbook/00-总览与阅读地图.md)。
- 迁移同题：[../Java_to_Kotlin/01-引言与项目迁移.md](../Java_to_Kotlin/01-引言与项目迁移.md)（课位 Ⅳ-12 的跨语言镜像）；入口书配置段：[../Learning_TypeScript/00-总览与阅读地图.md](../Learning_TypeScript/00-总览与阅读地图.md)。
- 擦除边界总账：[../TypeScript系列·Runtime_vs_Type_System专题.md](../TypeScript系列·Runtime_vs_Type_System专题.md)；本表销账回写：[../TypeScript系列·总索引.md](../TypeScript系列·总索引.md)。

## 五、中英对照

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 编译配置文件 | tsconfig.json | tsc 的输入边界+开关总集 |
| 目标版本 | target | 产物 JS 的语法下限 |
| 类型库 | lib | 类型可见面，与 target 解耦 |
| 模块解析 | module resolution | 按说明符找类型文件的算法 |
| 严格模式伞 | strict | 一揽子严格开关的总闸 |
| 严格空检查 | strictNullChecks | null/undefined 独立成成员 |
| 隐式 any 禁令 | noImplicitAny | 推不出即报，不默认放行 |
| 精确可选属性 | exactOptionalPropertyTypes | `?:` 与赋 undefined 分家 |
| 声明产物 | declaration (.d.ts) | 库对外类型的 ABI 面 |
| 环境声明 | ambient declaration | declare 起的「外部世界契约」 |
| 渐进迁移 | gradual migration | allowJs/checkJs 三级推进 |
| 独立转译纪律 | isolatedModules | 每文件可脱离全工程转译 |
| 项目引用 | project references | 跨 tsconfig 增量构建图 |

## 六、⚠️ 欠账

- Ⅳ 部逐字课名/课界未销（Manning 404）；书覆盖 TS 版本止于 4.6/4.7 还是追至 5.0 ⚠️——bundler 解析模式（TS 5.0 新项）等配置在书中存无待目录核。
- 报错形态表 10 行全为预期形态：待 tsc 授权安装后按第三节方案一次跑齐逐格销 ✅，并同步总索引「实测基线」。
- `--experimental-transform-types` 对参数属性的处理本波未跑（表内标 ⚠️）；装饰器两制（实验 vs Stage-3）边界留待有样例再测。
- 版次注记（或有 2/e，TS 5 时代）：若 2/e 实存，本 band Ⅳ-4/Ⅳ-13 需按新解析档重写半表。
