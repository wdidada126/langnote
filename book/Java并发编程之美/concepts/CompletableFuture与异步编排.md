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
