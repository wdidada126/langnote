# 《Kotlin in Action 2e》章笔记 10 · 协程高级：结构化并发与 Flow

> 三态标注：✅ = 语言事实（kotlinlang.org / kotlinx.coroutines 文档口径可证）；
> ⚠️ = 书中位置推定（2e「Structured Concurrency」「Flow 及其操作符」一线章群，
> 章号章名凭 00 册所载 Manning 页结论 ⚠️ 未逐字核实）；🔧 = 未实测
> （kotlinc 未装、无协程依赖仓）。承接 [09 册](09-协程基础与suspend函数.md)。

## 核心机制

### 结构化并发：作用域即父子树

- `coroutineScope { launch { } }`/`supervisorScope { }` 建立**父子 Job 树**：子协程失败默认取消兄弟并上抛（✅），父等待全部子完成（✅）——"泄漏任务"在类型上无处可去；supervisor 策略只截断失败分支不殃及兄弟（✅）。
- 对照 Java：ExecutorService 提交即散养，Future 忘 get 无人追责；CompletableFuture 异常链要手工 whenComplete 缝合。对照 C++：thread 脱离即 std::terminate，20 无 scope 执行器（P2300 未入，✅）——结构化并发是 kotlinx.coroutines 把并发问题改写成**词法作用域问题**的关键一手（✅ 机制），Elizarov 设计口径见官方 guide（⚠️ 篇名不写死）。
- `cancel()` 沿 Job 树传播、协程取消靠挂起点检查（✅）：不可挂起的长循环要么插 `yield()` 要么吃 `CancellationException` 规则（✅）；NonCancellable 清理段（✅）。
- `join/CompletableDeferred` 是显式会合点；withTimeout 用异常做控制流（✅）——异常语义与取消语义在 JVM 共享 CancellationException 通道，读代码先分清"超时"还是"被杀"。

### Flow：挂起函数版冷流

- `Flow<T> = suspend (FlowCollector<T>) -> Unit`（✅  typealias 口径）：发射端是挂起函数，`emit` 天然可背压——慢消费自动拖慢生产，与 RxJava 需要显式 backpressure 策略（✅）分野。冷流：每次 collect 重跑上游（✅），对位 TS async generator / C++23 std::generator（../C++20模板元编程/09-范围库.md co_yield 汇流点，✅ 在盘）。
- 操作符两层命名（✅）：中间流式 `map/filter/zip/merge`（返回新 Flow，可自由组合）vs 终端挂起 `toList/collect/reduce`（只能在挂起上下文调）——终结函数把"要不要阻塞点"写进类型，Java Stream 的惰性终端无此约束。
- 上下文切换唯一合法口 `flowOn(dispatcher)`（✅）：只影响**上游**发射，不影响下游 collect（✅）——`asFlow().flowOn(IO).map{}.collect{}` 的方向读错是头号理解事故。异常穿透：操作符 try/catch 包住 emit 非法（✅ 约束：挂起函数不能在 crossinline/try 里随意调），书给 `catch/takeWhile` 型操作符（凭记忆 ⚠️ 收录位置）。
- StateFlow/SharedFlow（✅）：热流转接 UI 状态，distinctUntilChanged 语义、replay/buffer 策略；与 Rx BehaviorSubject/Relay 同族但类型层区分"有初值必在"（StateFlow T 非空）与"可空无初值"（SharedFlow? T）。Java 对位是 9 版 Flow API（✅ 仅 Reactive-Streams 接口，无组合子）——kotlinx Flow 完整度高出一截。

## 批判读法（易错与存疑）

1. **"取消=异常"心智**：CancellationException 不该被业务 catch-all 吞掉（✅ 官方警告）；`try { collect } catch (e: Exception)` 顺手写就破坏协作取消——代码评审红线。
2. **flow 里的 emit 约束**：自定义 flow{} 内不能在非协程上下文（回调里）emit，除非 callbackFlow+channel 桥（✅）；书中对 callbackFlow/producer 演化的取舍凭记忆 ⚠️。
3. **flowOn 不是万能开关**：下游 collect 仍跑在调用者线程；把"切线程"理解成管道整体搬迁就错（✅ 机理）。
4. **热流的泄漏面**：SharedFlow 无限 collect 不结束，Android 生命周期绑定时机=泄漏时机——与 RxJava 同款事故（✅ 机理）；10 册若只讲 API 不讲取消纪律即残缺 ⚠️。
5. **supervisor 的双刃**：子失败静默只落 CoroutineExceptionHandler（✅），忘装 handler 即异常黑洞——与 Actor 模型监督树对照阅读。
6. 2e Flow 章是否覆盖 Flow 与 Structured Concurrency 库（runScheduledTask 类 2.x 新 API）⚠️ 未核。

## 🔧 微实验（未实测：kotlinc 未装、协程实验需 kotlinx-coroutines 依赖，仅为设计）

- 实验 A：coroutineScope 内一子抛异常，打印兄弟取消日志与异常上抛路径；换 supervisorScope 对照只伤一枝。
- 实验 B：flow{ while(true){emit; delay} }.flowOn(IO).collect{ delay(慢) }，线程名+时序表验证背压与"flowOn 只搬上游"。
- 实验 C：catch{} 包住下游 map 异常 vs try/catch 包 collect，看操作符链异常的位置语义差异。

## 盘谱互链

- 上一章 [09-协程基础与suspend函数.md](09-协程基础与suspend函数.md)；回主干 [00-总览与阅读地图.md](00-总览与阅读地图.md)——十册骨架至此闭合。
- TS async/Promise vs 运行时留痕坐标：../TypeScript系列·Runtime_vs_Type_System专题.md（✅ 在盘）。
- C++20 co_await 状态机/C++23 generator 对照：../C++20模板元编程/09-范围库.md、../C++20设计模式/01-导论-模式体系与C++20惯用法.md。
- 线程世界基本功（Job 树 vs 线程池）：../C++并发编程实战2/02-线程管控.md、../C++并发编程实战2/09-高级线程管理.md。
- 协程 API 命名/用法惯例补读：[../Effective_Kotlin/00-总览与阅读地图.md](../Effective_Kotlin/00-总览与阅读地图.md)。

## 核心概念中英对照

- **结构化并发** — structured concurrency：并发任务树随词法作用域生灭。
- **监督作用域** — supervisorScope：子失败不连坐兄弟的策略位。
- **协作取消** — cooperative cancellation：挂起点检查的自愿让出制。
- **冷流** — cold flow：每次 collect 重跑的惰性序列。
- **背压** — backpressure：emit 挂起实现的生产被消费拖慢。
- **流操作符** — flow operators：中间层可组合 + 终端层挂起二分。
- **热流** — StateFlow/SharedFlow：多播带缓存的状态载体。

> ⚠️ 欠账：2e Structured Concurrency/Flow 各章逐字章名与切分（14–18 部的章序凭 Manning 页结论 ⚠️）；catch/callbackFlow 讲解位置；本机零实测——购书+搭 gradle 环境后销账；另 01/02 册前向旧链名待总索引统一。
