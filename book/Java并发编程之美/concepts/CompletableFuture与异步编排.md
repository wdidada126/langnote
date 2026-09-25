# 专篇：CompletableFuture、异步编排与"回调地狱"的退场

> **本书没有专门章节讲 CompletableFuture**（本书第 8/9 章只讲线程池与定时任务，
> 第 11 章讲实践陷阱）。这是本书相对 JDK 8 时代**最大的一块缺口**——
> JDK 8 同时引入 lambda 和 CompletableFuture，本应是"并发 + 函数式"的转折点。
> 而且 2023 年之后 JDK 21 虚拟线程落地，**异步编排的必要性正在被重新评估**。

## 一、本章地图

```
Future（JDK 5）的四个死穴
        ↓
CompletableFuture = Future + CompletionStage
        ↓
方法命名三维矩阵：apply/accept/run × then/both/either/compose × 同步/Async/Async(Executor)
        ↓
异常传播：exceptionally / handle / whenComplete 的区别（最容易搞混的一块）
        ↓
默认线程池 ForkJoinPool.commonPool 的坑
        ↓
JDK 9-21 的新增能力（超时、copy、minimalCompletionStage）
        ↓
虚拟线程时代的重构：还要不要 CompletableFuture？
```

## 二、`Future` 的四个死穴（为什么需要 CompletableFuture）

```java
Future<String> f = executor.submit(() -> fetchUserName(42));
String name = f.get();   // ① 阻塞：调用线程挂起，违背异步初衷
```

| 死穴 | 表现 |
| --- | --- |
| ① **只能阻塞拿结果** | `get()` 阻塞，没有"结果好了回调我"的机制 |
| ② **无法组合** | 两个 Future 的结果要合并？只能在调用线程里手工编排 |
| ③ **无法手动完成** | 无法从外部把一个值/异常塞进 Future（对 RPC 框架是致命的） |
| ④ **异常传播断裂** | 线程池里抛的异常被吞进 `ExecutionException`，非受检异常没法直接 catch |

`CompletableFuture` 同时实现 `Future` + `CompletionStage`，补上了全部四点。

## 三、方法命名三维矩阵（80+ 方法其实只有三个维度）

**维度 1：消费方式**

| 词根 | 参数 | 返回 | 类比 |
| --- | --- | --- | --- |
| `thenApply` | `Function<T,R>` | `CF<R>` | `map` |
| `thenAccept` | `Consumer<T>` | `CF<Void>` | `forEach` |
| `thenRun` | `Runnable` | `CF<Void>` | 纯副作用 |

**维度 2：组合拓扑**

| 词根 | 语义 | 触发条件 |
| --- | --- | --- |
| `thenXxx` | 串行：上一阶段的输入 | 上游正常完成 |
| `thenCombine` / `thenAcceptBoth` / `runAfterBoth` | **AND**：两个都要完成 | 双上游都完成 |
| `applyToEither` / `acceptEither` / `runAfterEither` | **OR**：谁先完成用谁 | 任一上游完成 |
| `thenCompose` | **扁平化串行** | 上游结果是 `CF<T>` 时，避免 `CF<CF<T>>` |

**维度 3：执行线程**

| 后缀 | 执行位置 |
| --- | --- |
| `thenApply(...)` | 上游完成的那个线程（可能是完成 `complete()` 的业务线程！） |
| `thenApplyAsync(...)` | 默认 `ForkJoinPool.commonPool` |
| `thenApplyAsync(..., executor)` | **指定线程池 —— 生产环境唯一推荐写法** |

> **`thenApply` vs `thenCompose` 一句话区分**：
> `thenApply(f)` 中 `f` 返回 `T` → 得到 `CF<T>`；`f` 返回 `CF<T>` → 得到 `CF<CF<T>>`（嵌套）。
> `thenCompose(f)` 中 `f` 返回 `CF<T>` → **扁平化成 `CF<T>`**。凡是回调里又要发起异步调用，必须用 `compose`。

```java
// 反例：嵌套地狱
CompletableFuture<CompletableFuture<Order>> bad = uid.thenApply(this::findOrderAsync);
// 正解
CompletableFuture<Order> good = uid.thenCompose(this::findOrderAsync);
```

## 四、异常传播：三者区别（面试与事故高发区）

```java
CompletableFuture<String> cf = ...;

cf.exceptionally(ex -> "default");        // ① 只处理异常；异常被"吃掉"转成正常值
cf.handle((r, ex) -> ex != null ? "d" : r); // ② 正常和异常都走，可改变结果
cf.whenComplete((r, ex) -> log(r, ex));   // ③ 都走，但**不能改变结果**（类似 finally）
```

| 方法 | 上游成功 | 上游异常 | 能否改变结果 | 能否把成功变异常 |
| --- | --- | --- | --- | --- |
| `exceptionally` | 透传 | 拦截，返回替代值 | ✅（仅异常路径） | ❌ |
| `handle` | 收到 `(r, null)` | 收到 `(null, ex)` | ✅ | ✅ |
| `whenComplete` | 收到 `(r, null)` | 收到 `(null, ex)` | ❌ | ✅（可抛异常覆盖） |

**四条硬规则：**

1. 异常沿链**向下传播但跳过普通 `thenApply`**：中间任何一个 `thenApply` 都不会执行，直接跳到下一个 `handle/exceptionally/whenComplete`。
2. 异常被包装成 `CompletionException`，`get()`/`join()` 时再拆包抛出；链式上连加**多次包装**——`ex.getCause()` 可能还要再剥一层。
3. `exceptionally` 放在链**中间**会截断异常（下游再也看不到），放在链**末尾**才是兜底。
4. `allOf` 的异常只暴露**第一个**完成的异常，其余被吞；要拿全量，得对每个子 Future 单独 `handle`。

## 五、`ForkJoinPool.commonPool` 的大坑

`thenApplyAsync(...)` 不传 Executor 时，用 `ForkJoinPool.commonPool()`：

| 坑 | 说明 |
| --- | --- |
| 并行度 = `Runtime.availableProcessors() - 1` | 1 核容器 → 并行度 **0**，退化成单线程 |
| 整个 JVM **共享一个池** | 一个业务的慢任务会拖垮所有用了默认池的库 |
| 线程是 **daemon** | JVM 退出时不等待任务完成 |
| 设计目标是 **CPU 密集的 fork-join 任务** | 放进阻塞 I/O 会**饿死**池（不会自动补偿线程） |

**生产规则**：任何时候 `xxxAsync` 都要显式传业务线程池。
**虚拟线程规则**：JDK 21 起传 `Executors.newVirtualThreadPerTaskExecutor()`，阻塞不再有代价。

## 六、JDK 9 → 21 的新增能力（本书完全没覆盖）

| 版本 | 新增 | 解决的问题 |
| --- | --- | --- |
| JDK 9 | `orTimeout(timeout, unit)` / `completeOnTimeout(value, ...)` | **JDK 8 的 Future 没有超时**（只能用 `get(timeout)` 在调用侧兜） |
| JDK 9 | `defaultExecutor()` / `newIncompleteFuture()` | 子类可定制默认执行器 |
| JDK 9 | `minimalCompletionStage()` / `copy()` | 防御性拷贝，防止下游调用方 `complete()` 篡改上游 |
| JDK 9 | `completeAsync(Supplier, Executor)` | 异步产生值 |
| JDK 12 | `exceptionallyAsync` / `exceptionallyCompose` | 恢复逻辑本身也可以是异步的 |
| JDK 19-21 | `StructuredTaskScope`（预览 → JDK 25 转五度预览） | 见本目录《结构化并发与 ScopedValue》 |
| JDK 21 | 虚拟线程 | 见下 |

## 七、虚拟线程时代：还要不要 CompletableFuture？

这是 **2023 年后最值得重新思考的一点**。CompletableFuture 的存在理由只有一个：
**"不让线程阻塞在等待上"**。而虚拟线程的阻塞几乎免费——于是同步写法重新可行。

```java
// 旧范式：链式回调（回调地狱的现代精装版）
CompletableFuture<User> u = uid.thenComposeAsync(this::findUser, pool);
CompletableFuture<Order> o = u.thenComposeAsync(this::findOrder, pool);
return o.thenApply(order -> render(order));

// 新范式：虚拟线程 + 同步代码，可读性完胜
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User>  u = scope.fork(() -> findUser(uid));   // 每个 fork 一个虚拟线程
    Subtask<Order> o = scope.fork(() -> findOrder(uid));
    scope.join().throwIfFailed();
    return render(o.get());
}
```

**选择建议**：

| 场景 | 推荐 |
| --- | --- |
| 扇出多个独立 I/O 再聚合 | 虚拟线程 + `StructuredTaskScope`（JDK 21+）或 `newVirtualThreadPerTaskExecutor() + invokeAll` |
| 事件流、背压、多值序列 | `Reactive Streams` / `Flow`（JDK 9 `java.util.concurrent.Flow`） |
| 已有大量 CF 代码、需要超时/组合语义 | 保留 `CompletableFuture`，但务必显式指定 Executor |
| 纯 CPU 密集并行 | `ForkJoinPool` / `parallelStream`（见《ForkJoin与工作窃取》） |

> **注意**：`CompletableFuture` 在 JDK 21 也做了适配——虚拟线程里 `get()` 阻塞**不会**钉住（pin）载体线程，
> 因为 JDK 21 起 `ForkJoinPool` 在虚拟线程阻塞时知道补偿；但如果是 `synchronized` 块里的阻塞，
> 在 JDK 24（JEP 491）之前仍会 pin。**JEP 491 之后 `synchronized` 不再 pin**。

## 八、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Halstead, R. H. 1985. "MultiLisp: A Language for Concurrent Symbolic Computation." ACM TOPLAS 7(4): 501-538.** | **`future` 原语**（`call/future`）首次成为一等语言构造，提出 *touch* 阻塞语义与"最左最外"求值 |
| **Baker & Hewitt 1977. "The Incremental Garbage Collection of Processes."** | future/promise 的概念源头（MIT AI Lab），提出"进程即垃圾可回收" |
| **Liskov, B. & Shrira, L. 1988. "Promises: Linguistic Support for Efficient Asynchronous Procedure Calls in Distributed Systems." SIGPLAN '88.** | **promise 这个词的正式出处**；区分 *call-stream* / *call-return* / *call-forward*；提出 **promise pipelining**（把后续 RPC 直接发给未完成的 promise） |
| **Miller, M. S., Tribble, E. D., Shapiro, J. 2005. "Concurrency Among Strangers." Symposium on Trustworthy Global Computing.** | E 语言的 **eventual send** 与 vat 模型；把 promise 提升为分布式安全原语；直接影响后来的 JavaScript Promise / async-await |
| Moggi 1991 / Wadler 1992（monad 系列） | `thenCompose` 本质就是 monadic bind；解释了为什么 `applyToEither` 这类"天然并行"操作**无法**用 monad 表达 |
| Reactive Streams **规范 1.0.4**（2015，Netflix/Pivotal/Typesafe/Lightbend 联合） | 与 CF 互补的另一条路线：处理**多值 + 背压**，CF 只能表示单个值 |
| JEP 266 "More Concurrency Updates"（JDK 9） | `Flow` API、超时方法、CF 增强的官方说明 |
| JEP 444 / JEP 491 / JEP 506 | 虚拟线程、synchronized 不 pin、ScopedValue |

> **CompletableFuture 本身没有论文**。Doug Lea 在 JDK 源码里的类注释与
> `jsr166` 邮件列表存档是最权威的设计文档——这一点和 AQS 一样。

## 九、近年研究与工业界前沿

### 工业界开源实现（2026-09 核验，stars 数来自 GitHub）

| 项目 | Stars | 路线 | 与 CF 的关系 |
| --- | --- | --- | --- |
| **ReactiveX/RxJava** | 48.2k | Reactive Streams + 背压 | CF 的能力超集（多值、背压、重试、超时算子）；Spring WebFlux 的底座 |
| **Google Guava** | 51.9k | `ListenableFuture` / `FluentFuture` | JDK 8 之前的 CF 替代品；`Futures.transform` 是 CF 的直接前身 |
| **Netty** | 35.1k | `DefaultPromise` / `ChannelFuture` | **Netty 自己实现了一套 promise**，因为 CF 太重（每个节点一个对象、链式 GC 压力） |
| **Kotlin kotlinx.coroutines** | 13.8k | 挂起函数 + 结构化并发 | "同步写法 + 异步执行"的最成功实践；Loom 的设计参照 |
| **SmallRye Mutiny**（Quarkus 生态） | — | 声明式异步编排 | 与虚拟线程混合使用的现代方案 |
| **Vert.x** | — | 事件循环 + Future 组合 | 与 Netty 同栈，CF 之外的一条成熟路线 |
| **OpenJDK `jdk`** | 23.4k | `CompletableFuture.java` / `StructuredTaskScope.java` | 权威实现；源码里 200+ 行类注释讲清了"依赖栈/完成栈"的设计 |

**值得读的源码位置**：

- `java.base/share/classes/java/util/concurrent/CompletableFuture.java` —— 类注释详细解释了 *Completion* 节点的
  **Treiber 栈**式依赖结构，以及为什么 `complete()` 是 O(依赖数) 而非 O(1)。
- `java.base/share/classes/java/util/concurrent/StructuredTaskScope.java` —— JDK 21+ 的结构化并发实现。

### 近年研究

- **结构化并发**（JEP 453/480/491 预览演进，及 Nathaniel J. Smith 2018 年的 "Notes on structured concurrency, or: Go statement considered harmful"）——对"fire-and-forget 的 Future"最系统的批判：Future 没有生命周期边界，任务会泄漏到作用域之外。
- **"async/await 的函数染色问题"（function coloring）** —— 异步 API 会传染调用栈，这一批评推动了虚拟线程路线（让异步"隐形"）。
- **背压与流控**：Reactive Streams 之后，近年研究集中在"如何在虚拟线程/协程里表达背压"（Mutiny、Kotlin Flow 的 `buffer`/`conflate` 语义）。

## 十、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "`allOf` 能拿到所有结果" | **`allOf` 返回 `CompletableFuture<Void>`**！要 `allOf(...).join()` 之后再对每个子 Future `join()` 取值 |
| 2 | "`exceptionally` 就是 catch-all" | 它**只**捕获**上游**异常，且会把异常变成成功值，下游 `handle` 再也看不到异常 |
| 3 | "`thenApplyAsync` 有线程池兜底" | 默认 `commonPool`，1 核容器下并行度为 0；阻塞 I/O 会饿死它 |
| 4 | "`complete()` 可以多次设值" | **只有第一次生效**，后续返回 false（不抛异常）；要强制覆盖用 `obtrudeValue()`（危险，通常仅用于测试） |
| 5 | "`cancel()` 总是生效" | 只对**未完成**的 CF 生效；且它抛的是 `CancellationException`，下游 `handle` 会看到 `CancellationException` 而非你自定义的异常 |
| 6 | "CompletableFuture 有超时" | **JDK 8 没有**。`get(timeout)` 只是调用侧放弃等待，**任务仍在跑**。真正超时要 JDK 9+ `orTimeout`，或自建调度器 `completeExceptionally` |
| 7 | "链路上的异常就是原始异常" | 被 `CompletionException` 包装，链式多段会**多层包装**，要循环剥 `getCause()` |
| 8 | "虚拟线程出来了，CF 就该全删" | 对于**需要超时/取消/组合语义**的长期链路，CF 仍是最清晰的表达；虚拟线程更适合"扇出-聚合"与同步化的 I/O |
| 9 | "`whenComplete` 可以改返回值" | 不能，它返回的是原结果，类似 `finally`；只有 `handle` 能改 |
| 10 | "CF 链式调用没有开销" | 每建一个阶段就 new 一个 `Completion` 节点，长链有显著的分配与 GC 成本；热点路径上 Netty 因此不用 CF |

> **本书补充定位**：本书第 11 章讲的 10 个实践陷阱里没有异步编排相关的坑，
> 这一篇补齐。同时把 JDK 9-25 的演进（超时、`copy`、虚拟线程、结构化并发）接上，
> 避免读者停留在 2018 年的 JDK 8 世界。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

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
