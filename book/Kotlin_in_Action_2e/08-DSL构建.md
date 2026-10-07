# 《Kotlin in Action 2e》章笔记 08 · DSL 构建

> 三态标注：✅ = 语言事实（kotlinlang.org 口径可证）；⚠️ = 书中位置推定
> （章名凭记忆；1e「Creating DSLs / Type-safe domain-specific languages」是
> 招牌章，2e 未逐字核实）；🔧 = 未实测（kotlinc 未装）。02（接收者 lambda）
> + 07（invoke/约定）的汇流终点，也是 09 `scope.launch {}` 的同款机器。

## 核心机制

### 类型安全构建器：把 lambda 当作用域

- 范式：`html { table { tr { } } }`——外层函数收 `block: HTML.() -> Unit`，lambda 体内以 HTML 实例为**隐式接收者**（✅），逐层嵌套建对象树；声明式外形、编译期类型检查、无字符串无反射。1e 的 HTML/SQL 双例（位置凭记忆 ⚠️）是这条线的教科书展开。
- 三块地基在盘：尾随 lambda（[02 册](02-函数与Lambda.md)）、带接收者函数类型 `A.() -> R`（02）、invoke 与 get/set 糖（[07 册](07-运算符重载与语言细节.md)）；`"route" { handle }` 式 Web DSL = `operator fun String.invoke(block: Route.() -> Unit)`（✅）。
- Java 对照：Builder 是**运行时**模式（方法返回 this，无作用域概念）；Kotlin 默认参数（02）已干掉大半 telescoping，DSL 再把平铺参数升级成层级语言。GoF Builder 的 C++ 形态见 ../C++20设计模式/02-建造器模式.md（✅ 在盘）——天花板同样是线性链式、无语法级作用域。
- TS/JS 对照：JSX 是语法级特例（要编译器插件），Kotlin DSL 全由标准语言构造拼出——"库即语言"路线，且类型报错兜住拼写。

### @DslMarker：给嵌套作用域装围栏

- 无注解时内层 lambda 同时看见**所有外层接收者**：`html { table { tr() } }` 里跨层误调外层成员照样编译（✅ 隐式接收者解析规则）。
- `@DslMarker annotation class HtmlDSL` 标到接收者类后，同标签的外层接收者被屏蔽、只留最近一层（✅）——作用域泄漏从运行时 bug 前移为编译错误，Kotlin DSL 区别于一切手写 Builder 生态的关键一手。
- 局限（✅ 机理）：只屏蔽**同标签**外层，不同标签/显式参数照穿；是嵌套卫生，不是权限系统。

### scope functions 五件套：let/apply/run/with/also

- 两轴分类（✅ 官方口径）：传引用（it：let/also）还是当接收者（this：apply/run/with）；返回 lambda 结果还是对象自身（apply/also 惯例）。
- 选择纪律（书中立场凭记忆 ⚠️，与 Effective Kotlin 同调）：apply 配置、also 旁路校验/日志、let 可空链转换、with 对已就位对象分组、run≈with+作用域限定。`also` 1.1 加入（✅）正是补"it 版 apply"空位。
- `apply` 永远返回接收者（✅）：`val n = obj.apply { 42 }` 拿回 obj 不是 42——高频误读。
- 协程 `CoroutineScope.() -> Unit`（[09 册](09-协程基础与suspend函数.md)）复用同一机器：DSL 章读深度直接决定协程 API 是自然还是玄学。

## 批判读法（易错与存疑）

1. **深嵌套隐式 this**：三层以上不配 DslMarker 靠 IDE 高亮救命；书中对"何时退回显式命名参数"着墨多少是 2e 检验点 ⚠️。
2. **DSL≠语言扩展**：报错是普通类型错误（"Unit 不能赋给 TR"式天书），无 parser 级提示；与 TS 模板类型报错同级别难。
3. **run/with 滥用成匿名变量块**：无关联语句塞进 with 只为省前缀，diff 与栈可读性双输。
4. **围栏不防 Java**：DslMarker 只在 Kotlin 侧生效，Java 调用方仍乱序调 builder（✅ 机理）——互操作护栏缺口。
5. **构建器对象生命周期**：lambda 里存了接收者引用逃逸出作用域，树建完对象还被持有——DSL 与内存泄漏的隐秘接口（✅ 机理）。
6. 2e 例库换血情况（HTML 之外是否 kotlinx 新库/@BuilderInference 收录）⚠️ 未核。

## 🔧 微实验（未实测：kotlinc 未装，仅为设计）

- 实验 A：手搓 mini-HTML（html/table/tr 三层）打印标签树；table 层误调 `html()`，先证无注解编译通过，加 @DslMarker 复编译看围栏报错。
- 实验 B：同一对象配置分别 apply/also/let，`javap` 对照闭包类捕获差异与返回值。
- 实验 C：双参数 invoke 路由 DSL 雏形 `"/" { }`，验证 07 册与本册语法咬合。

## 盘谱互链

- 上一章 [07-运算符重载与语言细节.md](07-运算符重载与语言细节.md)；下一章 [09-协程基础与suspend函数.md](09-协程基础与suspend函数.md)。
- 命名/可读性：[../Effective_Kotlin/01-命名与注释.md](../Effective_Kotlin/01-命名与注释.md)；GoF Builder 对照：../C++20设计模式/02-建造器模式.md。
- TS 系列索引（报错可读性同族）：../TypeScript系列·总索引.md（✅ 在盘）。

## 核心概念中英对照

- **类型安全 DSL** — type-safe DSL：类型系统校验的领域语言。
- **构建器** — builder：接收者 lambda 逐层建对象树。
- **隐式接收者** — implicit receiver：省略 this 的成员访问源。
- **作用域标记** — @DslMarker：屏蔽同标签外层接收者。
- **作用域函数** — scope functions：let/apply/run/with/also。
- **调用约定 DSL** — invoke-based DSL：`obj(args){}` 形态地基。

> ⚠️ 欠账：2e DSL 章逐字章名与例库；DslMarker 细则展开深度凭记忆——购书后销账。
