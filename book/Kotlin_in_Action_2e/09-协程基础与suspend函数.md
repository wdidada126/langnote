# 《Kotlin in Action 2e》章笔记 09 · 协程基础与 suspend 函数

> 三态标注：✅ = 语言事实（kotlinlang.org / kotlinx.coroutines 文档口径可证）；
> ⚠️ = 书中位置推定（2e 协程章群章号凭 00 册所载 Manning 页结论 ⚠️，未逐字
> 核实）；🔧 = 未实测（kotlinc 未装、本机无协程依赖仓）。本册是 2e 增量核心。

## 核心机制

### suspend：编译进函数类型的挂起-恢复

- `suspend fun load(): Data` 编译后多一个隐藏 `Continuation` 尾参（✅ CPS 变换口径），调用点可在挂起点让出**当前线程**而不**阻塞线程**。对照 Java：`Future.get()` 占线程、回调地狱、CompletableFuture 链=手工 CPS；对照 C++20：`co_await` 生成状态机+promise type，Kotlin 同属"编译器重写函数为状态机"路线，但 promise 协议被 kotlinx.coroutines 库吸收，语言侧只留 `suspend` 一个修饰符。C++ 侧协程状态机/generator 对照切片见 ../C++20模板元编程/09-范围库.md（co_yield/generator 汇流点，✅ 在盘档有登记）与 ../C++20设计模式/01-导论-模式体系与C++20惯用法.md（co_yield/co_await 改写 Observer/Iterator 异步形态，✅ 在盘档原句级）。
- `suspend` 进**类型系统**：`suspend () -> T` 与普通函数类型不兼容（✅，[02 册](02-函数与Lambda.md)"同层类型构造子"兑现），只有挂起上下文可调用。TS 对照：`async () => Promise<T>` 形似神异——Promise 是**运行时对象**、await 只是 thenable 语法糖；Kotlin 挂起编译期进类型、运行期 Continuation 状态机。两种 async 的"运行时留不留痕迹"恰落在 ../TypeScript系列·Runtime_vs_Type_System专题.md 的擦除坐标系上（✅ 该档实测 TS 侧）。
- JS 单线程事件循环 vs Kotlin 协程**可跨线程续跑**（✅）：恢复可能换线程，共享可变状态纪律照常——线程基本功在 ../C++并发编程实战2/03-线程间共享数据.md（✅ 在盘）。

### 启动、调度与阻塞边界

- `runBlocking {}` 桥接阻塞↔挂起世界，**阻塞当前线程**直到完成（✅）；生产代码只在 main/测试。`GlobalScope.launch` 是逃逸结构化并发的全局火种，书与官方口径一致劝退（✅；1e 无此章，2e 立场 ⚠️ 推定）。
- Dispatchers：`Default`（CPU 池）、`IO`（弹性阻塞池）、`Main`（UI）、`Unconfined`（不主动切换，✅）——对位 Java ExecutorService 选型，但下沉为**上下文元素**而非手交 executor；C++20 无标准执行器（P2300 未入，✅），协程调度全凭 promise type 自接——Kotlin 用库补完，C++ 留白。
- `delay(1000)` 挂起而非 `Thread.sleep`（✅）；`withContext(IO) { jdbc() }` 是阻塞调用圈养的合法入口（✅）。
- 组合子：`coroutineScope { async { f() } }` + `awaitAll` 对位 CompletableFuture.allOf，但取消/异常传播由层级结构决定而非手工拼装（✅，10 册深讲）。
- suspend 对 Java 不可见：产物方法带 Continuation 尾参（✅），Java 侧只能借 kotlinx-coroutines 的 future 桥接消费（模块/函数名凭记忆 ⚠️，00 册已挂账）。

## 批判读法（易错与存疑）

1. **"协程=轻量线程"话术**：调度器与线程池仍有限；Dispatcher 配错（IO 跑 CPU 活/Default 跑 JDBC）性能塌方——书中是否给吞吐曲线是 2e 质检点 ⚠️。
2. **挂起传染**：API 一半 suspend 后测试/回调接口全链改造；Main 里嵌 `runBlocking` 即死锁候选（✅ 机理）。
3. **suspend≠无并发**：状态机换线程续跑，共享 var 照旧要原子/锁——"单线程感"脑补成"线程安全"是初读头号事故。
4. **异常走 CPS 通道**：挂起点异常经 resumeWithException 上抛（✅），栈信息截断；书中是否讲调试栈合成（CoroutineExceptionHandler 之前那层）⚠️ 记忆存疑。
5. **Unconfined 误读**：常被当"就在当前线程跑完"——实际是事件循环语义，嵌套启动顺序反直觉（✅ 文档口径）。
6. 2e 协程群章数/章名（Coroutine basics 拆几册、是否含调试章）⚠️ 仅凭 Manning 页结论。

## 🔧 微实验（未实测：kotlinc 未装且协程实验需 kotlinx-coroutines 依赖，仅为设计）

- 实验 A：`runBlocking { launch { delay… } }` 打印前后线程名，验证 runBlocking 阻塞宿主但 launch 体走事件循环续跑。
- 实验 B：withContext(IO)/Default 切换打 `Thread.currentThread().name`，对照换不换线程两谱系。
- 实验 C：suspend 函数编译后 `javap -p`，肉眼确认 Continuation 尾参与返回 Object 哨兵，实证 CPS。

## 盘谱互链

- 上一章 [08-DSL构建.md](08-DSL构建.md)（scope 接收者语法同源）；下一章 [10-协程高级与Flow.md](10-协程高级与Flow.md)。
- TS await/Promise 与擦除坐标：../TypeScript系列·Runtime_vs_Type_System专题.md（✅ 在盘）。
- C++20 co_await/co_yield 状态机：../C++20模板元编程/09-范围库.md、../C++20设计模式/01-导论-模式体系与C++20惯用法.md。
- 线程基本功：../C++并发编程实战2/02-线程管控.md、../C++并发编程实战2/03-线程间共享数据.md。

## 核心概念中英对照

- **挂起函数** — suspend function：可让出线程的函数类型。
- **续体** — Continuation：挂起恢复回调句柄，CPS 显形。
- **CPS 变换** — continuation-passing style：编译器重写出状态机。
- **调度器** — Dispatcher：协程→线程投递策略（Default/IO/Main）。
- **运行阻塞桥** — runBlocking：两世界的适配器。
- **挂起而非阻塞** — suspend, don't block：delay≠sleep 军规。
- **圈养阻塞** — withContext(IO)：阻塞调用关进 IO 池的合法围栏。

> ⚠️ 欠账：2e 协程诸章逐字章名与切分；future 桥模块名、调试特性收录深度；本机零实测（无 kotlinc/依赖仓）——购书+搭环境后销账。
