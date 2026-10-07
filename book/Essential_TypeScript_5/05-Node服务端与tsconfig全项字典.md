# 《Essential TypeScript 5》参考带 05 · Node 服务端与 tsconfig 全项字典（Ⅳ+Ⅴ 部）

> ⚠️ 部名「Ⅳ Node 与服务端」「Ⅴ 配置与部署」与章序凭 Freeman 体例记忆；本书是否讲 Express/Node 内置 http、tsconfig 章讲到哪一代开关（`erasableSyntaxOnly`？`verbatimModuleSyntax`？）**版次覆盖范围待销账**——00 档已标「tsconfig 字典章=本系列最全单点 ⚠️」。
> 三态纪律：✅=本会话 `node v22.14.0 --experimental-strip-types` 真跑（transform 面另注命令）｜⚠️=公共面记忆/书目说法。**本机无独立 tsc**（`which tsc` 空；全局仅有 @vue/cli 内嵌 typescript 4.1.6，不对位，按 ../TypeScript系列·总索引.md 三口径不作出处）⇒ 下表「编译期报错」列一律空，只给**运行面对位状态**。

## 一、查表地图（机制 → 本仓更深主干对位）

| 机制 | 对位档 | 本书角色 |
|---|---|---|
| tsconfig 全项字典 | ../TypeScript_in_50_Lessons/00-总览与阅读地图.md（⚠️ 其 `04-*.md` 未建，按 00 口径：本仓 tsconfig 语义最细的一本） | 全项清单来源 + 索引 |
| `strict` 家族语义 | ../Effective_TypeScript_2e/00-总览与阅读地图.md（规范裁决位） | 补「开关打开后的完整写法」样板 |
| 模块解析（Node/bundler） | ../TypeScript_Compiler_Notes/00-总览与阅读地图.md（实现线 ⚠️ 占位档） | 只做目录 |
| Node/Express 服务端类型接线 | ../TypeScript_Cookbook/00-总览与阅读地图.md | 本仓画像后端 ⇒ 本书 Ⅳ 部是唯一服务端位 |
| 擦除与运行时真相 | ../TypeScript系列·Runtime_vs_Type_System专题.md（✅ 一手记录） | 无 |
| 迁移期混合库（allowJs/checkJs） | ../Java_to_Kotlin/（渐进迁移同题）、../Kotlin系列·总索引.md | 对照 |

## 二、本书独有价值点：tsconfig 字典全项清单（33 行、合写后 40+ 个开关；每行标本仓实测状态）

图例：**✅运行面**=Node 直跑已给出一手对位证据；**⚠️待tsc**=纯编译期开关，本仓 0 实测；「一句话作用」列整体属**公共面记忆 ⚠️**（未与原文逐条对表）。

| # | compilerOptions 项 | 一句话作用（⚠️ 记忆/公共面） | 本仓实测状态 |
|---|---|---|---|
| 1 | `target` | 产物 JS 语言代际 | ✅运行面：node v22.14 对所测 ES2022 面语法全绿（static block/`#`private/Array.at/Object.hasOwn/structuredClone/fetch/WeakRef/TLA）——`esfeat.ts` |
| 2 | `lib` | 注入哪些全局声明 | ✅运行面：`esfeat.ts` 中 `fetch/structuredClone/Intl/Object.hasOwn` 在 node 22 真实存在；反向：`using d = new D()`（依赖 `esnext.disposable`）报 V8 `SyntaxError: Unexpected identifier 'd'` ✅（`us.ts`）⇒ lib 若写最新代，运行时仍可能无支撑 |
| 3 | `module` | 产物模块制 | ⚠️待tsc；✅运行面：Node 侧模块制由 `package.json type`/`.mts/.cts` 决定，与 tsconfig 无关（`m1/s.ts`、`c.cts`） |
| 4 | `moduleResolution` | 解析算法（node16/nodenext/bundler） | ⚠️待tsc；✅运行面：Node ESM 要求**带扩展名**——`noext.mts` → `ERR_MODULE_NOT_FOUND ... \b`（`a.mts` 带 `.mts` 则通过） |
| 5 | `types` / 6 `typeRoots` | 自动引入哪些全局声明包 | ⚠️待tsc；✅运行面：类型-only import 不解析包（`elide.ts`/`srv.mts` 无 `@types/node` 仍跑） |
| 7 | `strict` | 严格族总闸 | ⚠️待tsc（0 报错实测） |
| 8 | `noImplicitAny` | 隐式 any 报错 | ⚠️待tsc |
| 9 | `strictNullChecks` | null/undefined 进类型域 | ⚠️待tsc |
| 10 | `strictFunctionTypes` | 函数参数逆变检查 | ⚠️待tsc |
| 11 | `strictBindCallApply` | bind/call/apply 签名检查 | ⚠️待tsc |
| 12 | `strictPropertyInitialization` | 字段必须初始化 | ⚠️待tsc |
| 13 | `useUnknownInCatchVariables` | catch 变量为 unknown | ⚠️待tsc |
| 14 | `noUncheckedIndexedAccess` | 索引访问附加 undefined | ⚠️待tsc；✅运行面：`srv.mts` 用 `(...)[0]!` 非空断言，运行时零检查（擦除） |
| 15 | `exactOptionalPropertyTypes` | 可选属性不接受 undefined | ⚠️待tsc |
| 16 | `noImplicitOverride` | 覆写必须写 override | ⚠️待tsc；✅运行面：`ovr2.ts` → `override erased: 2`（`override` 不进产物） |
| 17 | `noUnusedLocals` / 18 `noUnusedParameters` | 未用声明报错 | ⚠️待tsc |
| 19 | `noFallthroughCasesInSwitch` / `noImplicitReturns` | 控制流纪律 | ⚠️待tsc |
| 20 | `allowJs` | 把 `.js` 纳入编译 | ⚠️待tsc；✅运行面：`mixjs.mts` 从 `./plain.js` 导入 `add(2,3)=5` —— Node 天然混合，无需开关 |
| 21 | `checkJs` | 对 `.js` 做类型检查 | ⚠️待tsc |
| 22 | `esModuleInterop` / `allowSyntheticDefaultImports` | CJS 默认导入兼容 | ⚠️待tsc；✅运行面：`import fs = require()` 在 strip 模式直接 `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`（`shim.ts`） |
| 23 | `isolatedModules` | 单文件转译安全子集 | ⚠️待tsc；✅运行面：Node 两模式都按**单文件**处理——`const enum` 未内联、仍留运行时绑定（`ce2.ts` → `{"5":"X","X":5}`） |
| 24 | `verbatimModuleSyntax` | 保真模块语法/禁隐式擦除 | ⚠️待tsc；✅运行面反向证据：`import type` 被**无条件整体删除**（含不存在的路径），Node 无「保真」概念（`elide.ts`） |
| 25 | `erasableSyntaxOnly` | 只允许可纯擦除语法 | ⚠️待tsc；✅运行面=**本带最强代理**：strip 模式对 `enum`/`namespace`/参数属性/`import =` 四类全部抛 `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`（`enum.ts`/`ns.ts`/`param.ts`/`shim.ts`），纯擦除面（`eo.ts`/`sat.ts`）全跑通 |
| 26 | `experimentalDecorators` / 27 `emitDecoratorMetadata` | 旧装饰器制 + 元数据发射 | ⚠️待tsc；✅运行面：Node **两模式均不译装饰器**（legacy 与标准写法同报 V8 `Invalid or unexpected token`），且同目录 tsconfig 存在不影响结果（`dec/`） |
| 28 | `useDefineForClassFields` | 字段用 define 还是 set 语义 | ⚠️待tsc；✅运行面：V8 原生 define 语义——`fieldkeys.ts` → own keys `[ 'b','s','priv','b2' ]`、`#hard` 不入 ownKeys |
| 29 | `declaration` / `declarationMap` / `composite` / `incremental` | 产出 .d.ts、项目引用、增量 | ⚠️待tsc（本仓无产物可查） |
| 30 | `outDir` / `rootDir` / `noEmit` / `removeComments` / `sourceMap` | 产物布局 | ⚠️待tsc；✅运行面：Node 直跑不落产物 ⇒ 本仓「noEmit 当 lint 用」路线依赖安装 tsc ⚠️ |
| 31 | `resolveJsonModule` | JSON 当模块导入 | ⚠️待tsc；✅运行面：`import ... with { type: "json" }` 与 `readFileSync` 双路皆通（`json.ts`，42/42） |
| 32 | `skipLibCheck` / `forceConsistentCasingInFileNames` | 库检查与大小写纪律 | ⚠️待tsc |
| 33 | `jsx` / `downlevelIteration` | JSX 与低代迭代降级 | ⚠️待tsc；✅运行面：`mixjs.mts` 原生 Set/Map 迭代、展开、generator 全绿 ⇒ node 22 不需降级 |

## 三、🔧 微实验（本波真跑摘录，脚本 `/tmp/et5/`）

1. **服务端面跑通**：`node --experimental-strip-types srv.mts` → `strip-types-server: 200 {"msg":"hi"} | routes keys: [ '/hi' ]` ✅ —— `node:http` + 泛型路由表 + `type` 说明符 + 非空断言 + 动态端口 `listen(0)` + `fetch` 自测，**纯擦除语法内零配置可跑**；Express 面本仓无依赖 ⚠️ 不可跑（禁 install）。
2. **开关→报错形态表（Node 侧代理）**：`enum.ts`/`ns.ts`/`param.ts` 三件在 strip 模式全部 `SyntaxError [ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX]`（逐条原文：`TypeScript enum is not supported in strip-only mode` 等 ✅），`--experimental-transform-types` 三件全跑（`never 0` / `1` / `ok P { q: 1 }` ✅）——「擦除 vs 转译」分界实测完成，`erasableSyntaxOnly` 的语义边界即此。
3. **模块解析面**：`a.mts` 带扩展名 import ✅ vs `noext.mts` 不带扩展名 `ERR_MODULE_NOT_FOUND` ✅。
4. 待补（依赖独立 tsc ⚠️）：固定样例集 × `strict` 族逐项单开 → diff 报错清单；`verbatimModuleSyntax` vs `importsNotUsedAsValues` 新旧口径对照。

## 四、盘谱互链

- 骨架权威：./00-总览与阅读地图.md（Ⅳ/Ⅴ 部定位、四、实测口径）。
- 配置轻量版互证：../TypeScript_in_50_Lessons/00-总览与阅读地图.md；前代考古：../Pro_TypeScript/00-总览与阅读地图.md（⛔ 2012 命令行时代配置面）。
- 主干/规范/实现线：../Programming_TypeScript/00-总览与阅读地图.md、../Effective_TypeScript_2e/00-总览与阅读地图.md、../TypeScript_Compiler_Notes/00-总览与阅读地图.md、../Type_Level_TypeScript/00-总览与阅读地图.md、../Learning_TypeScript/00-总览与阅读地图.md、../Tackling_TypeScript/00-总览与阅读地图.md、../TypeScript_Cookbook/00-总览与阅读地图.md。
- 同系列档：../TypeScript系列·Runtime_vs_Type_System专题.md、../TypeScript系列·总索引.md；本波其余带：./01、./02、./03、./04。

## 五、⚠️ 欠账

- **字典代次风险**：上表 40+ 开关（33 行）按 TS 5.x 公共面整理 ⚠️，与**本书实际列出项**的差集未核（书中是否含 `bundler` 解析、`erasableSyntaxOnly`、`customConditions`、`noCheck` 等）。
- 编译期报错面**全数 0 实测**：本机无独立 tsc；销账动作=获授权后装 typescript 5.x 并重跑「固定样例集 × 单开关」矩阵。
- Ⅳ 部逐字章名（Node/Express/Apollo？）、Ⅴ 部是否讲 CI/部署流——未核。
- 本带实验脚本仅存会话临时目录，未入库（`exp/` 固化待授权）。
