# 《Learning TypeScript》章笔记 03 · 函数签名与 this

> 对应 [00-总览与阅读地图.md](00-总览与阅读地图.md) 骨架 **Ⅱ 函数与对象段（前半）**。
> ⚠️ 章名「函数签名与 this」为按书记忆的主题带命名（原书函数章含参数/返回/重载/this），非逐字章名。
> 三态：**✅** = 本机实测（node v22.14 strip-types，脚本 `/tmp/lts_exp/exp03.ts`）；**⚠️** = 凭记忆；**🔧** = 未实测。

## 核心机制

- **签名=注解化的形状登记**：`(a: number, b?: string) => number` 里除 JS 本体（参数表、
  返回值）外全是编译期契约。✅ 实测：`(a: number, b?: string, ...rest: unknown[]) => a`
  的 `f.length = 2`——`b?` 与 `...rest` 在类型层的花样不改变 JS  arity 事实，运行时的
  `b` 就是个普通缺省为 `undefined` 的槽位。
- **`this` 伪参数是纯类型层发明**：`function g(this: { name: string }) {...}` 的 `this:`
  参数被 strip-types 整个剥除。✅ 实测：`g.call({ name: "erased-this-param" })` 正常返回
  ——TS 允许你给 `this` 立字面契约，但执行时没有任何东西核对它。
- **箭头函数 this 是 JS 语义不是 TS 语义**：✅ 实测：类字段 `incArrowSelf = () => this.n`
  用 `.call(999)` 强行换 this 无效（返回仍是实例的 `0`），词法绑定运行时硬核；而
  `incNormal()` 返回的普通函数一换就飞。TS 的 `noImplicitThis` 只是在编译期给这条
  JS 地形补路标 ⚠️（编译器面未实测，无 tsc）。
- **与名义类型系对照**：Java 方法签名绑定在类上、虚分派看运行时类型；Kotlin 的接收者
  lambda（`fun Foo.block()`）里 this 有编译期真身。TS 的 `this` 与函数完全解耦——它是
  **调用方式决定的隐式首参**，重载签名（overload signatures）也只是给检查器看的候选列表，
  运行时永远是单个实现 ⚠️（实现体签名+校验要手写）。

## 批判读法

- 入口书把「函数即值」讲得顺，但 `this` 一章本质是在给你打 JS 补丁而不是教 TS——
  Java/C++ 读者最省力路径是：**先按 JS 规则理解 this，再看 TS 注解面**，顺序反了会
  把 `this: void` 之类的写法当成运行时约束。⚠️ 教学口径印象。
- 原书对参数属性（constructor 简化术）与函数重载的边界警告较弱；实测确认参数属性是
  **会产码的混合语法**：✅ strip-only 直接拒跑（`ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX:
  TypeScript parameter property is not supported in strip-only mode`），这条界碑专题档
  原标 ⚠️ 待补实测，本会话已销账 ✅。
- 默认参数与可选参数 `?` 混用时 arity 的诡异（见上实验 `length=2`）原书未必点破，
  属自建判词位。⚠️。

## 🔧 微实验

- ✅ 已实测（exp03.ts，exit=0）：arity 不受类型注解影响、`this:` 伪参数剥除后可调用、
  箭头 this 词法硬绑定、类方法落 `Counter.prototype`。
- ✅ 已实测边界（boundary_pp.ts，拒跑 exit=1）：参数属性非纯擦除语法，strip-only 拒绝。
- 🔧（未实测）`strictFunctionTypes` 下逆变参数报错矩阵；重载回退选错的报错文案——均需 tsc。

## 盘谱互链

- 参数属性界碑销账对象：[../TypeScript系列·Runtime_vs_Type_System专题.md](../TypeScript系列·Runtime_vs_Type_System专题.md)（第五节待补清单）。
- 骨架档：[00-总览与阅读地图.md](00-总览与阅读地图.md)。
- Kotlin 函数面对照（具名函数类型/接收者 lambda）：[../Kotlin_in_Action_2e/02-函数与Lambda.md](../Kotlin_in_Action_2e/02-函数与Lambda.md)。
- 工程条目回看：[../Effective_TypeScript_2e/00-总览与阅读地图.md](../Effective_TypeScript_2e/00-总览与阅读地图.md)（重载/`this` 相关 Item 谱系 ⚠️）。

## 中英对照表

| 中文 | 英文 | 一句定义 |
| --- | --- | --- |
| 函数签名 | function signature | 参数表+返回类型构成的可赋值形状，纯编译期 ✅。 |
| 返回类型注解 | return type annotation | `=> T`；不写则推断，写了即登记期望。 |
| 可选参数 | optional parameter | `b?: T`；运行时只是可为 undefined 的普通槽位 ✅。 |
| 默认参数 | default parameter | JS 本体语法，真产码；与 `?` 语义重叠需二选一 ⚠️。 |
| this 伪参数 | this parameter | 首置的 `this: T` 契约，strip 后整个消失 ✅实测。 |
| 词法 this | lexical this | 箭头函数捕获定义处 this，运行时硬墙 ✅实测。 |
| 函数重载 | overload signatures | 多签名一实现，仅供检查器挑选，无运行时分派 ⚠️。 |
| 参数属性 | parameter property | `constructor(public v: T)` 型语法；会产码，strip-only 拒 ✅实测。 |

⚠️ 欠账：逐字章名；重载/`strictFunctionTypes` 报错矩阵待 tsc；原书是否单列 `this` 节次凭记忆。
