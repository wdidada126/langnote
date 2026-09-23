# CompletableFuture 与异步编排

> 定位：《Java并发编程之美》第 4 章讲线程池与 `Future` 时指出 `Future.get()` 只能阻塞等待、无法回调；本篇讲 JDK 8 引入的 `CompletableFuture`——它同时实现了 `Future`（拉）与 `CompletionStage`（推），是 Java 在虚拟线程之前唯一的官方异步组合方案。

## 一、是什么（最小示例）

`CompletableFuture<T>` 是一个**可被手动完成（complete）的 Future**，并且支持把后续动作以回调形式挂上去。三类编排：串行（`thenApply`/`thenCompose`）、并行汇聚（`thenCombine`/`allOf`/`anyOf`）、异常与超时（`exceptionally`/`handle`）。

```java
ExecutorService biz = Executors.newFixedThreadPool(8);   // ① 务必传自定义池，见第六节

CompletableFuture<Integer> stock  = CompletableFuture.supplyAsync(() -> queryStock(id), biz);
CompletableFuture<Integer> price  = CompletableFuture.supplyAsync(() -> queryPrice(id), biz);

CompletableFuture<String> render = stock
        .thenCombine(price, (s, p) -> s > 0 ? "price=" + p : "sold out")   // ② 两个都完成才触发
        .thenApplyAsync(String::toUpperCase, biz)                          // ③ Async 后缀 = 换线程执行
        .thenCompose(txt -> CompletableFuture.supplyAsync(() -> translate(txt), biz)) // ④ 扁平化，避免 Future<Future<>>
        .exceptionally(ex -> "fallback:" + ex.getMessage())                // ⑤ 只吃异常，无异常则透传
        .orTimeout(2, TimeUnit.SECONDS);                                   // ⑥ JDK 9+，超时抛 CompletionException

String result = render.join();        // join() 与 get() 的区别：不抛受检异常
CompletableFuture.allOf(stock, price).join();   // 等待全部；anyOf 则是任一完成即返回
```

- **方法后缀的三条规则**：`thenApply` 沿用上一步的线程；`thenApplyAsync` 提交到线程池；带 `Executor` 的重载指定线程池。不带 `Async` 的版本在上一步已完成的线程（可能是**调用方线程**）上直接跑，这是最常见的性能陷阱。
- **`thenApply` vs `thenCompose`**：前者是 `map`（`T -> U`），后者是 `flatMap`（`T -> CompletionStage<U>`）。在 lambda 里返回 `CompletableFuture` 却用了 `thenApply`，会得到嵌套的 `CompletableFuture<CompletableFuture<T>>`，且外层立刻完成——**内层异常不再向外传播**。
- **异常传播**：`supplyAsync` 里抛出的异常被捕获进 `AltResult`，只有调用 `get/join` 或下游 `handle/whenComplete/exceptionally` 时才以 `CompletionException`（`join` 则是 `CompletionException`，`get` 是 `ExecutionException`）形式重新抛出。不写 `exceptionally` 也不 `join`，异常会被**静默吞掉**。

## 二、实现原理（源码级）

```java
// JDK 8 CompletableFuture 的核心：一个 volatile 结果字段 + 一个"完成动作"栈（Treiber stack）
volatile Object result;      // 正常结果，或 AltResult（异常/null 包裹）
volatile Completion stack;   // 无锁压栈的依赖动作链表

// 完成时的核心循环（简化，去掉了 CAS 细节）：
final void postComplete() {
    CompletableFuture<?> f = this; Completion h;
    while ((h = f.stack) != null || (f != this && (h = (f = this).stack) != null)) {
        CompletableFuture<?> d; Completion t;
        if (f.casStack(h, t = h.next)) {     // ① 弹出一个依赖
            if (t != null) { if (f != this) { pushStack(h); continue; } h.next = null; }
            f = (d = h.tryFire(NESTED)) == null ? this : d;   // ② 触发它，可能返回新的下游
        }
    }
}
```

- **数据结构**：`result` 用 CAS 写入（或 `UNSAFE.compareAndSwapObject`），保证只完成一次（重复 `complete` 返回 false）；`stack` 是 **Treiber 栈**（Michael-Scott 式无锁结构，见本书《Michael-Scott 无锁队列》一篇），回调以后进先出压入。因为是栈而非队列，`thenApply` 的注册顺序**不保证**触发顺序。
- **依赖爆炸问题**：每个 `thenXXX` 都 new 出至少一个 `UniApply`/`BiApply` 对象挂在栈上，长链会产生大量短命对象；`postComplete` 用循环而非递归触发下游，正是为了避免长链时栈溢出（源码注释明确写了 "to avoid recursion"）。
- **`allOf` 的怪癖**：返回 `CompletableFuture<Void>`，丢弃全部结果，需要自己再 `thenApply` 回各个 future 上取；且**任一子任务失败，其余任务不会被取消**，仍在后台跑完。
- **`orTimeout` 的实现（JDK 9+）**：

```java
public CompletableFuture<T> orTimeout(long timeout, TimeUnit unit) {
    if (result == null)
        whenComplete(new Canceller(Delayer.delay(new Timeout(this), timeout, unit)));
    return this;
}
// Delayer 内部是一个只有 1 个线程的 ScheduledThreadPoolExecutor（daemon），
// 惰性初始化；因此大量短超时任务会在这个单线程上排队，超时精度受限。
```

- **`ForkJoinPool.commonPool()` 陷阱**（第六节详述）：不传 `Executor` 的 `*Async` 方法走 `ForkJoinPool.commonPool()`；若任务里有阻塞 IO，会把公共池拖死，而 `parallelStream` 也用同一个池，于是**整个 JVM 的并行流一起变慢**。

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 5 | `java.util.concurrent.Future` + `FutureTask`：只能 `get()` 阻塞拿结果或轮询 `isDone()`，无法组合 |
| JDK 6-7 | 生态靠 Guava `ListenableFuture` / `SettableFuture`（`addListener` + `Futures.transform`）补位 |
| JDK 8 | 🔴 **本书基线**：`CompletableFuture` 加入（作者 Doug Lea），实现 `Future` + `CompletionStage`，50+ 个组合方法；`thenApply/thenCompose/thenCombine/allOf/anyOf/exceptionally/handle/whenComplete` 齐备 |
| JDK 9 | 🔴 `orTimeout` / `completeOnTimeout` / `completeAsync` / `copy` / `defaultExecutor` / `newIncompleteFuture` / `minimalCompletionStage`；内部改用 `VarHandle` 替代 `Unsafe` |
| JDK 12 | `exceptionallyAsync`、`exceptionallyCompose`（让异常恢复也能异步/返回新的 stage） |
| JDK 19-21 | 虚拟线程时代：`CompletableFuture` 仍可用，但**推荐直接写同步代码**；`StructuredTaskScope`（JEP 453/464/480）提供"结构化并发"替代方案，子任务随作用域退出自动取消 |
| JDK 21+ | 迁移建议：IO 密集编排优先虚拟线程 + `StructuredTaskScope`；`CompletableFuture` 保留给"需要把结果暴露给外部、生命周期跨越方法边界"的场景（如缓存加载、批量 RPC 扇出） |

**与同类 API 的对照**：

| API | 取消传播 | 背压 | 组合能力 | 适合场景 |
| --- | --- | --- | --- | --- |
| `FutureTask` | 支持 `cancel` | 无 | 无 | 单次任务的简单结果获取 |
| Guava `ListenableFuture` | 支持 | 无 | `transform`/`allAsList` | JDK 8 之前的历史代码 |
| `CompletableFuture` | 弱（无父子关系，`cancel` 不传导上游） | 无 | 强（50+ 方法） | 扇出编排、缓存异步加载 |
| Reactor `Mono`/`Flux` | 通过订阅链传导 | ✅ Reactive Streams 背压 | 极强（数百操作符） | 流式、限流、消息驱动 |
| `StructuredTaskScope` | ✅ 作用域退出自动取消全部子任务 | 无 | 弱（偏命令式） | 虚拟线程下的"多任务等齐" |

## 四、经典论文

| 论文 | 作者 | 会议 / 期刊 | 年份 | 与本篇的关系 |
| --- | --- | --- | --- | --- |
| *Promises: Linguistic Support for Efficient Asynchronous Procedure Calls in Distributed Systems* | Barbara Liskov, Liuba Shrira | SIGPLAN Notices | 1988 | Promise/Future 的正式起源，提出 promise 作为"尚未完成计算的占位符"，`then` 式回调的思想源头 |
| *A Universal Modular Actor Formalism for Artificial Intelligence* | Carl Hewitt, Peter Bishop, Richard Steiger | IJCAI | 1973 | Actor 模型：消息传递与异步语义的另一条路线（Akka/Erlang），与 Future 形成对照 |
| *Subject/Observer 与反应式编程的形式化*（Rx 代表作 *Your Mouse Is a Database*） | Erik Meijer 等 | SIGMOD | 2012 | 把事件流对偶于数据库查询，奠定了 Rx 与后续 Reactive Streams 的理论表述 |
| *Reactive Streams Specification*（规范文档，非会议论文） | Lightbend/Netflix/Pivotal/Red Hat 联合工作组 | reactive-streams.org | 2015 | `Publisher/Subscriber/Subscription/Processor` 四接口与背压契约，后被 JDK 9 `java.util.concurrent.Flow` 采纳 |
| *Structured Concurrency*（Nathaniel Smith 的 *Notes on structured concurrency, or: Go statement considered harmful*） | Nathaniel J. Smith | 个人技术笔记 / 广泛引用 | 2018 | "go statement considered harmful"，直接启发 JEP 453 `StructuredTaskScope` |
| *Scheduling Multithreaded Computations by Work Stealing* | Robert D. Blumofe, Charles E. Leiserson | Journal of the ACM | 1999 | `ForkJoinPool.commonPool()` 的理论基础，解释 `CompletableFuture` 默认执行器的调度性质 |

## 五、近年研究与工业界实践（2020-2026）

| 项目 | GitHub 地址 | 看点 |
| --- | --- | --- |
| OpenJDK jdk | https://github.com/openjdk/jdk | `src/java.base/share/classes/java/util/concurrent/CompletableFuture.java`：`postComplete`、`Delayer`、VarHandle 改写全过程 |
| Reactor | https://github.com/reactor/reactor-core | `Mono`/`Flux` 与 `CompletableFuture` 互转（`Mono.fromFuture`）；有背压与取消链，是 CF 的"升级形态" |
| Guava | https://github.com/google/guava | `ListenableFuture` 与 `Futures.transform/transformAsync/successfulAsList`，CF 出现前的工业方案 |
| Netty | https://github.com/netty/netty | `ChannelFuture` + `Promise`：`addListener` 模型与 EventLoop 线程绑定，展示 CF 之外的另一种异步约定 |
| Caffeine | https://github.com/ben-manes/caffeine | `AsyncLoadingCache.get(key)` 返回 `CompletableFuture`，是 CF 在缓存领域最典型的工业用法 |
| resilience4j | https://github.com/resilience4j/resilience4j | 用装饰器为 `CompletableFuture` 叠加熔断、限流、重试、隔离舱 |
| gRPC-java | https://github.com/grpc/grpc-java | `ListenableFuture` 与 `FutureStub`，以及 `Context` 跨线程传播——CF 编排中"上下文丢失"问题的一手案例 |
| Kotlin kotlinx.coroutines | https://github.com/Kotlin/kotlinx.coroutines | `CompletableFuture.await()` 互操作，展示"把 CF 接回协程"以消除函数染色的做法 |
| Netflix RxJava | https://github.com/ReactiveX/RxJava | Meijer 反应式思想在 JVM 上的落地，是 CF 能力不足时的替代路线 |

**2020 年后的主流判断**：虚拟线程让"用同步代码写 IO 编排"重新可行，`CompletableFuture` 仍应保留在两类场景——(1) 结果需要跨方法边界返回给外部（缓存、批量扇出）；(2) 需要超时/兜底/重试等**横切语义**的管线。纯"调三个服务再聚合"的代码，JDK 21+ 用 `StructuredTaskScope` 写法更短、取消更干净。

## 六、常见误区 + 跨语言对照

| 误区 | 真相 / 正确写法 |
| --- | --- |
| 不传 `Executor`，让 `*Async` 跑在 `ForkJoinPool.commonPool()` | 该池并行度 = 核数−1，且被 `parallelStream` 共用；一个阻塞 IO 就能拖垮全 JVM。IO 场景**必须**传自己的 `Executor` |
| 用 `thenApply` 返回 `CompletableFuture` | 会得到嵌套 future 且异常不再传播，应改用 `thenCompose`（flatMap） |
| 忘记 `exceptionally`/`handle` | 异常被吞；`join` 时才炸出来，且包装成 `CompletionException`（`get` 是 `ExecutionException`），需 `ex.getCause()` |
| 认为 `cancel(true)` 能停掉正在跑的任务 | `CompletableFuture.cancel` 只把结果置为 `CancellationException`，**不会中断已提交的任务**；需自行向上游传播中断 |
| 以为 `allOf` 会取消兄弟任务 | 不会。某任务失败后其余仍在后台跑，长期占用线程池 |
| 用 `get()` 而不是 `join()` 或在回调链里阻塞 | 在 `thenApply` 里调 `get()` 会阻塞线程池工作线程，可能**饿死整个池** |
| 依赖 `orTimeout` 做毫秒级精确超时 | 其 `Delayer` 是单线程 daemon 调度器，超时精度与任务量相关 |

**跨语言对照**：`CompletableFuture` ≈ JavaScript `Promise`（`.then` 链、微任务 vs 线程池的差异在于调度器）≈ C# `Task`（`ContinueWith` / `await`）≈ Rust `tokio::spawn` 返回的 `JoinHandle` + `join!`/`try_join!` ≈ Python `asyncio.Task` + `asyncio.gather`/`wait`（`anyOf`≈`FIRST_COMPLETED`，`allOf`≈`ALL_COMPLETED`）≈ Go 的 `errgroup.Group`（Go 没有 Future 抽象，用 goroutine + channel + `WaitGroup` 组合）。
