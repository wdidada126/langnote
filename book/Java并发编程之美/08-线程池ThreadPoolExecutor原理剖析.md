# 第 8 章 Java 并发包中线程池 ThreadPoolExecutor 原理探究（原书 pp.225-242）

> 主角：`ThreadPoolExecutor`、`Worker`、`Executors` 工厂、`ScheduledThreadPoolExecutor`（第 9 章）
> 本章是全书的枢纽：前面所有组件（阻塞队列、AQS、CAS、ThreadLocal）最后都汇聚到线程池这一个"生产线"上。

## 一、本章地图

| 小节 | 主题 | 页码 |
| --- | --- | --- |
| 8.1 | 介绍 | 225 |
| 8.2 | 类图介绍 | 225 |
| 8.3.1 | `execute(Runnable command)` | 230 |
| 8.3.2 | 工作线程 Worker 的执行 | 235 |
| 8.3.3–8.3.5 | `shutdown` / `shutdownNow` / `awaitTermination` | 238–241 |
| 8.4 | 总结 | 242 |

## 二、8.1–8.2 为什么需要线程池，以及类图

线程池解决三个问题：

1. **降低资源开销**——线程创建/销毁是系统调用（`pthread_create` + 内核栈分配），线程池把"每次任务一次系统调用"摊薄成"一次创建、N 次复用"。
2. **提高响应速度**——任务到达时线程已存在，无需等待创建。
3. **提供可管理的边界**——可以统一限制并发度、队列长度、拒绝策略、命名、监控。生产环境中**"能管住"比"跑得快"更重要**。

类图关系：

```
Executor                       execute(Runnable)
  └─ ExecutorService           submit()/shutdown()/invokeAll()
       └─ AbstractExecutorService   实现了 submit -> newTaskFor -> execute
            └─ ThreadPoolExecutor   ← 本章主角
                 └─ ScheduledThreadPoolExecutor   （第 9 章）
```

`AbstractExecutorService` 的关键作用是把 `Runnable`/`Callable` 统一包装成 `FutureTask` 再交给 `execute()`，所以 **`submit()` 返回的 Future 异常处理与 `execute()` 不同**：`execute()` 里抛出的异常会打到 `UncaughtExceptionHandler` 并**导致该工作线程死亡**（线程池会补一个新 Worker），而 `submit()` 的异常被 `FutureTask` 吞进 `outcome`，只有调用 `get()` 才抛出。

## 三、8.3 源码分析：`ctl` —— 一个 int 装下两个状态

```java
private final AtomicInteger ctl = new AtomicInteger(ctlOf(RUNNING, 0));
private static final int COUNT_BITS = Integer.SIZE - 3;          // 29
private static final int CAPACITY   = (1 << COUNT_BITS) - 1;     // 低 29 位掩码

// runState 存高 3 位，单调递增
private static final int RUNNING    = -1 << COUNT_BITS;          // 接收新任务 + 处理队列任务
private static final int SHUTDOWN   =  0 << COUNT_BITS;          // 不接收新任务，但处理队列任务
private static final int STOP       =  1 << COUNT_BITS;          // 不接收新任务，不处理队列，中断在跑的
private static final int TIDYING    =  2 << COUNT_BITS;          // 所有任务结束，workerCount=0
private static final int TERMINATED =  3 << COUNT_BITS;          // terminated() 执行完
```

用 **一个 `AtomicInteger` 同时编码"运行状态 + 工作线程数"** 是 Doug Lea 的经典技巧：状态的迁移和计数的增减必须是原子的，否则会出现"刚把状态改到 SHUTDOWN，另一个线程却在加 worker"的竞态。代价是**最大线程数被压到 2^29-1 ≈ 5.37 亿**（实际不可能达到），以及所有读写都要 `runStateOf`/`workerCountOf` 位运算，可读性差。

> **JDK 演进补充**：社区对此有很多吐槽。JDK 21 之后 `ThreadPoolExecutor` 内部仍是这个设计（源码未重构），但 `Executors.newVirtualThreadPerTaskExecutor()` 走的是完全不同的路径——它**没有池、没有队列、没有 ctl**，每个任务一个虚拟线程。

## 四、8.3.1 `execute()` —— 三段决策树

```java
public void execute(Runnable command) {
    if (command == null) throw new NullPointerException();
    int c = ctl.get();
    // ① 工作线程数 < corePoolSize：直接新建核心线程，把 command 作为第一个任务
    if (workerCountOf(c) < corePoolSize) {
        if (addWorker(command, true)) return;
        c = ctl.get();
    }
    // ② 仍在 RUNNING 且成功入队：还要二次检查，防止入队后状态变了/线程全死了
    if (isRunning(c) && workQueue.offer(command)) {
        int recheck = ctl.get();
        if (!isRunning(recheck) && remove(command))
            reject(command);                       // 状态已变 -> 撤出并拒绝
        else if (workerCountOf(recheck) == 0)
            addWorker(null, false);                // 没有活线程 -> 补一个空转的
    }
    // ③ 队列满了：尝试开到 maximumPoolSize；再不行就拒绝
    else if (!addWorker(command, false))
        reject(command);
}
```

理解这三段是理解线程池"何时扩容"的钥匙：

- **core → queue → max 的顺序**是反直觉的：不是"先开满 core，再开到 max，最后进队列"，而是**先开满 core，然后进队列，队列满了才开到 max**。所以 `LinkedBlockingQueue`（默认无界）配 `maximumPoolSize` 是**无效的**——max 永远不会生效。这是生产中最常见的配置错误。
- **② 的二次检查**是必要的：入队之后状态可能被 `shutdown()` 改掉，也可能所有 worker 恰好执行完退出了（`allowCoreThreadTimeOut` 场景），必须在环形窗口内补一次判断。
- `addWorker(command, true/false)` 的布尔参数是 `core`，决定用 `corePoolSize` 还是 `maximumPoolSize` 做上界。

## 五、8.3.2 Worker 与 `runWorker`

```java
private final class Worker extends AbstractQueuedSynchronizer implements Runnable {
    final Thread thread;            // 由 ThreadFactory 创建
    Runnable firstTask;             // 可能为 null
    volatile long completedTasks;
    // AQS 被用作一个不可重入的互斥锁（state 0/1），保护"空闲/忙碌"状态
    protected boolean tryAcquire(int unused) {
        if (compareAndSetState(0, 1)) { setExclusiveOwnerThread(Thread.currentThread()); return true; }
        return false;
    }
}
```

注意两点，本书讲得比较简略：

1. **Worker 本身就是一个 AQS**。这里 AQS 不是用来排队的，而是当作一个**不可重入的独占锁**：`shutdown()` 中断 worker 前要先 `tryLock()` 拿锁，拿到说明线程空闲（安全中断），拿不到说明正在跑任务（不打断）。这是 AQS 的一个"非典型用法"，但完美复用了它的 state + 队列。
2. **`runWorker` 的循环**才是任务真正执行的地方：

```java
final void runWorker(Worker w) {
    Thread wt = Thread.currentThread();
    Runnable task = w.firstTask; w.firstTask = null;
    w.unlock();                       // 允许被中断
    boolean completedAbruptly = true;
    try {
        while (task != null || (task = getTask()) != null) {
            w.lock();                 // 标记忙碌，防止 shutdown 打断
            if ((runStateAtLeast(ctl.get(), STOP) || ...) && !wt.isInterrupted()) wt.interrupt();
            try {
                beforeExecute(wt, task);       // ← Hook，可用来做 ThreadLocal 传递/监控
                task.run();                    // ← 直接 run()，不是 start()
                afterExecute(task, null);      // ← Hook，可用来统计耗时
            } finally { task = null; w.completedTasks++; w.unlock(); }
        }
        completedAbruptly = false;             // 正常退出
    } finally {
        processWorkerExit(w, completedAbruptly);
    }
}
```

**关键**：`task.run()` 是**同步调用**，任务抛异常会一路冒泡终止 `while` 循环，进入 `processWorkerExit`，其中若 `completedAbruptly == true` 会 `decrementWorkerCount()` 并在需要时补一个 Worker。所以**任务里不要吞异常**，最好用 `submit()` + `Future.get()` 或全局 `UncaughtExceptionHandler`。

`beforeExecute`/`afterExecute`/`terminated` 三个空方法是官方留给用户的扩展点，工业界大量框架靠它们做**链路追踪上下文传递**（SkyWalking、transmittable-thread-local 都有对应接入方式）。

## 六、`getTask()`：线程池"缩容"的真正开关

```java
private Runnable getTask() {
    boolean timedOut = false;
    for (;;) {
        int c = ctl.get();
        if (runStateAtLeast(c, SHUTDOWN) && (runStateAtLeast(c, STOP) || workQueue.isEmpty())) {
            decrementWorkerCount(); return null;         // 状态已停 -> 退出
        }
        int wc = workerCountOf(c);
        // 关键：是否允许核心线程超时
        boolean timed = allowCoreThreadTimeOut || wc > corePoolSize;
        if ((wc > maximumPoolSize || (timed && timedOut)) && (wc > 1 || workQueue.isEmpty())) {
            if (compareAndDecrementWorkerCount(c)) return null;   // 超时回收
            continue;
        }
        try {
            Runnable r = timed
                ? workQueue.poll(keepAliveTime, TimeUnit.NANOSECONDS)   // 会阻塞等待
                : workQueue.take();                                     // 永久阻塞
            if (r != null) return r;
            timedOut = true;
        } catch (InterruptedException retry) { timedOut = false; }
    }
}
```

- `workQueue.take()` 的阻塞就是**工作线程"待命"的实现**，不需要额外的 sleep/spin。
- 只有 `timed == true` 的线程才会被回收，即**默认情况下核心线程永不销毁**，除非 `allowCoreThreadTimeOut(true)`。
- 因此 `corePoolSize=0` 且 `allowCoreThreadTimeOut=false` 时，任务会先入队且没有线程取——**JDK 的 `addWorker(null,false)` 补救分支就是为此存在**。`Executors.newCachedThreadPool()` 正是 `core=0, max=Integer.MAX_VALUE, SynchronousQueue`，靠这个分支工作。

## 七、8.3.3–8.3.5 关闭：三个方法语义完全不同

| 方法 | 新任务 | 队列里的存量任务 | 正在执行的任务 | 返回值 |
| --- | --- | --- | --- | --- |
| `shutdown()` | 拒绝（`RejectedExecutionException`） | **继续跑完** | 不打断 | void，立即返回 |
| `shutdownNow()` | 拒绝 | **丢弃并返回 List** | 发 `interrupt()` | `List<Runnable>` |
| `awaitTermination(t, u)` | — | — | — | 阻塞等待，超时返回 false |

`shutdown()` 内部是 **优雅停机**的教科书实现：`advanceRunState(SHUTDOWN)` → `interruptIdleWorkers()`（只对 `tryLock()` 成功的空闲线程发中断）→ `tryTerminate()`。而 `shutdownNow()` 是 `advanceRunState(STOP)` → `interruptWorkers()`（全部中断，不管忙闲）→ `drainQueue()`。

> ⚠️ 常见误解：**`shutdownNow()` 并不能"杀死"线程**。它只发中断信号；如果任务里不检查 `Thread.interrupted()`、也不调用任何可中断的阻塞方法（如 `Thread.sleep`、`BlockingQueue.take`、`Future.get`），任务会一直跑到自然结束。Java 早已废弃 `Thread.stop()`，没有强制杀线程的手段。

## 八、拒绝策略（RejectedExecutionHandler）

| 策略 | 行为 | 适用场景 |
| --- | --- | --- |
| `AbortPolicy`（默认） | 抛 `RejectedExecutionException` | 快速失败，让上游感知 |
| `CallerRunsPolicy` | **让提交者线程自己执行** | 天然的反压（backpressure），提交方变慢，间接降低到达速率 |
| `DiscardPolicy` | 静默丢弃 | 几乎不该用（数据丢失无感知） |
| `DiscardOldestPolicy` | 丢队首，重试入队 | 允许丢老的，如日志/心跳 |

生产实践：大多数业务应**自定义策略**——记录日志 + 上报指标 + 触发告警，并优先选 `CallerRunsPolicy` 做反压。Netty、RocketMQ、Dubbo 都有各自的 `RejectedExecutionHandler` 实现。

## 九、JDK 版本演进（本书基于 JDK 8，以下为后续重大变化）

| 版本 | JEP / 变更 | 对线程池的影响 |
| --- | --- | --- |
| JDK 5 | JSR 166，`java.util.concurrent` 引入 | 线程池首次进入标准库（Doug Lea 主导） |
| JDK 7 | ForkJoinPool（JSR 166y） | 工作窃取（work-stealing），适合递归分治；`commonPool()` 默认并行度 = CPU-1 |
| JDK 8 | `CompletableFuture`、`Executors.newWorkStealingPool()` | 异步编排成为主流，线程池从"执行器"升级为"组合子" |
| JDK 9 | JEP 266 引入 `Flow`（响应式流）；`CompletableFuture` 增加超时 `orTimeout`（实际 JDK 9） | 与 Reactive 生态对接 |
| JDK 19/20 | JEP 425/436 结构化并发（预览） | `StructuredTaskScope`：把"一组并发子任务"当作一个作用域，父任务取消/失败自动传播到子任务 |
| JDK 21 | **JEP 444 虚拟线程** + `Executors.newVirtualThreadPerTaskExecutor()` | 见下节 |
| JDK 21 | JEP 453 结构化并发（预览） | `StructuredTaskScope.ShutdownOnFailure` |
| JDK 24 | **JEP 491 解除虚拟线程在 synchronized 中的钉住（pinning）** | 此前在 `synchronized` 内阻塞会把虚拟线程钉在 carrier 线程上，导致 carrier 饥饿；现在改用独立锁实现 |
| JDK 25 | **JEP 506 ScopedValue**（正式） | 虚拟线程场景下替代 `ThreadLocal`：不可变、有作用域生命周期、继承开销 O(1) |

### 虚拟线程下的"线程池"观念要改写

```java
// JDK 21+
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return i; }));
}
```

- 虚拟线程**廉价到不需要池化**（JDK 21 起百万级虚拟线程可行），`newVirtualThreadPerTaskExecutor()` 内部是"每任务一个新虚拟线程"，**没有队列、没有 corePoolSize**。
- 但**不要用它做 CPU 密集任务**——虚拟线程不增加并行度，只提高并发度（IO 阻塞时让出 carrier）。CPU 密集仍应 `ForkJoinPool` 或固定大小 `ThreadPoolExecutor`。
- 阿里/美团等国内团队的实践结论：虚拟线程最适合"高并发 IO + 每请求独立上下文"的 Web 服务；替换后 CPU 与内存显著下降，但**必须排查 `synchronized` 钉住（JDK 24 前）、`ThreadLocal` 滥用、以及连接池（DB/HTTP）本身成为新瓶颈**。

## 十、经典论文与理论

| 论文 | 出处 | 与本章的关系 |
| --- | --- | --- |
| Doug Lea, *The java.util.concurrent Synchronizer Framework* | JACM 52(3), 2005 | AQS；`Worker` 继承 AQS 即源于此 |
| Blumofe & Leiserson, *Scheduling Multithreaded Computations by Work Stealing* | JACM 46(5), 1999 | `ForkJoinPool` 工作窃取的理论基础：证明期望空间与时间复杂度界 |
| Michael & Scott, *Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms* | PODC 1996 | 第 7 章队列；线程池的 `workQueue` 多半是它的阻塞变体 |
| Herlihy & Wing, *Linearizability* | TOPLAS 1990 | 判断线程池/队列行为是否正确的一致性标准 |
| Lea, *A Java Fork/Join Framework* | OOPSLA 2000 | ForkJoin 的初始设计 |
| Butenhof, *Programming with POSIX Threads* | 1997 | 线程池模式的工程起源（worker pool / boss-worker） |

**近年研究（2020 年后）**：

- **结构化并发的形式化**：Nathaniel Smith 的 *Notes on structured concurrency*（2018）启发了 JEP 453；后续有 *Structured Concurrency for Java* 相关的类型系统与作用域语义研究（PLDI/ICFP 2022-2024 多篇关于 structured/asynchronous effects 的工作）。
- **虚拟线程调度器的评估**：近年（ICPE/ATC 2023-2025）有多篇针对 Loom 的实测研究，结论一致——IO 密集吞吐提升显著，carrier 线程数应设为 CPU 核数；pinning 是 JDK 21-23 的主要性能陷阱。
- **自适应线程池调参**：SIGMOD/ATC 2021-2024 上针对数据库/存储的线程池自调节工作（如 "adaptive thread pool for HTAP"），思路与 `dynamic-tp` 工程实践一致。

## 十一、工业界最新开源实现（可直接读源码对照）

| 项目 | 地址 | 值得看的东西 |
| --- | --- | --- |
| **OpenJDK jdk** | https://github.com/openjdk/jdk — `src/java.base/share/classes/java/util/concurrent/ThreadPoolExecutor.java` | 权威实现；JDK 21+ 的 `VirtualThreadPerTaskExecutor` 在同一目录 |
| **Netty `EventLoopGroup`** | https://github.com/netty/netty | `NioEventLoopGroup` 本质是"每线程一个任务队列 + selector"的专用线程池；`ioRatio` 控制 IO/任务时间配比 |
| **LMAX Disruptor** | https://github.com/LMAX-Exchange/disruptor | 无锁环形缓冲 + `SequenceBarrier`，把线程池的队列换成 RingBuffer 消除伪共享与锁 |
| **JCTools** | https://github.com/JCTools/JCTools | `MpscUnboundedArrayQueue` 等多生产者单消费者队列，替代 `LinkedBlockingQueue` 可显著降低线程池入队争用 |
| **dynamic-tp** | https://github.com/dromara/dynamic-tp | 国产线程池动态调参 + 监控告警，解决"线程池参数拍脑袋"问题 |
| **transmittable-thread-local** | https://github.com/alibaba/transmittable-thread-local | 解决线程池场景下 `ThreadLocal`（链路追踪 ID）无法传递的问题，配合 `beforeExecute/afterExecute` |
| **JMH** | https://github.com/openjdk/jmh | OpenJDK 官方微基准，测线程池配置必须用它（否则 JIT 会骗你） |
| **Kafka / RocketMQ** | Apache | 大量自研线程池 + 自定义拒绝策略 + 线程命名规范，是"生产级线程池"的样板 |

## 十二、跨语言对比：线程池这件事别人怎么做

| 语言 | 并发单元 | 调度 | 典型"池/执行器" | 与 Java 的差异 |
| --- | --- | --- | --- | --- |
| **Java（JDK 8）** | 平台线程（1:1 内核线程） | OS 抢占式 | `ThreadPoolExecutor`、`ForkJoinPool` | 线程昂贵 → 必须池化；阻塞调用是常态 |
| **Java 21+** | 虚拟线程（M:N）+ carrier | JVM 调度，阻塞时挂起 | `newVirtualThreadPerTaskExecutor` | 写代码仍是阻塞风格，但不再需要池；`StructuredTaskScope` 管生命周期 |
| **Go** | goroutine（M:N，默认栈 2KB 起） | GMP 调度器 | 一般**不池化**；需要限流用 `errgroup` + 带缓冲 channel 或 semaphore | 自 2009 起就是"廉价并发"，Java 21 才追上；Go 无 ThreadLocal（`context.Context` 显式传递） |
| **Rust（tokio）** | async task（零成本状态机） | 协作式 + `tokio` 多线程 work-stealing 调度器 | `tokio::runtime::Runtime`、`rayon`（CPU 并行） | 无 GC + 所有权，`Send + 'static` 在编译期保证跨线程安全；阻塞任务必须 `spawn_blocking` 隔离 |
| **C++** | `std::thread`（1:1） | OS | 无标准线程池（`std::async` 不算）；常用 `boost::asio::io_context`、`folly::CPUThreadPoolExecutor`、`BS::thread_pool` | 2024 年提案 `std::execution`（P2300）推进标准执行器，仍未落地 |
| **Erlang/BEAM** | process（极轻量，独立堆） | 抢占式 reduction 调度 + 每核调度器 | 无需池；`supervisor` 树负责重启 | "let it crash" + 监督树 ≈ Java 的结构化并发 + 重启策略 |
| **Python** | thread（受 GIL 限制）/ asyncio task | OS / 事件循环 | `concurrent.futures.ThreadPoolExecutor`、`ProcessPoolExecutor`、`asyncio.gather` | GIL 使线程池无法并行 CPU 任务；3.13 起 free-threading（PEP 703）实验性关闭 GIL |
| **C#/.NET** | `Thread` / `Task` | `ThreadPool` + `TaskScheduler` | `ThreadPool`、`Parallel.ForEach`、async/await | `async/await` 语法被 Java 生态大量借鉴；`CancellationToken` ≈ Java 中断机制但更结构化 |

**横向结论**：Java 8 时代"必须池化"的约束是**内核线程太贵**导致的；Go/Erlang/Rust tokio/Node.js 从一开始就用轻量并发绕开了它。Java 21 虚拟线程是**补齐这一课**，但保留了阻塞式 API 的写法习惯，因此迁移成本远低于"改成 async/await"。

## 十三、误区与纠错（本书这里最容易读错）

1. ❌ "线程池越大越快" → CPU 密集任务的线程数应 ≈ CPU 核数（或核数+1），超出只会增加上下文切换与内存（默认栈 1MB/线程）。IO 密集可用 `N_threads = N_cpu * U_cpu * (1 + W/C)`（Little's Law 变形）。
2. ❌ "用 `Executors` 工厂就够了" → `newFixedThreadPool` 与 `newSingleThreadExecutor` 用**无界 `LinkedBlockingQueue`**（默认 `Integer.MAX_VALUE`），`newCachedThreadPool` 的 max 是 `Integer.MAX_VALUE`；在流量突增时会 OOM 或打满线程数。**阿里巴巴 Java 开发手册明确禁止直接用 `Executors` 创建**，必须显式 `new ThreadPoolExecutor(...)`。
3. ❌ "队列越大越好（能扛住峰值）" → 大队列把延迟藏在队列里，任务被消费时早已超时，且让 `maximumPoolSize` 失效。**有界队列 + 合理拒绝策略**才是可控的。
4. ❌ "`shutdown()` 就能立刻停掉" → 见第七节；需要 `shutdown()` + `awaitTermination()` + 必要时 `shutdownNow()` 三步组合。Spring 的 `ThreadPoolTaskExecutor` 建议设置 `setWaitForTasksToCompleteOnShutdown(true)` 与 `setAwaitTerminationSeconds(n)`。
5. ❌ "线程池里的 `ThreadLocal` 没问题" → 线程复用导致**上下文污染与内存泄漏**（见第 11.10 节与 `concepts/ThreadLocal与内存泄漏.md`）。虚拟线程时代应改用 `ScopedValue`。
6. ❌ "`submit()` 抛异常能被看到" → 异常被封进 `FutureTask`，不 `get()` 就静默消失。建议重写 `afterExecute` 兜底打印。

## 十四、本章一页纸总结

- `ctl` = 高 3 位状态 + 低 29 位线程数，一个 `AtomicInteger` 解决两个状态的原子迁移。
- `execute()` 三段：**core 未满就建线程 → 否则入队 → 队满才扩到 max → 再满就拒绝**。
- Worker 继承 AQS 当不可重入锁用，用来安全中断空闲线程。
- `getTask()` 的 `timed` 决定线程能否被回收；`allowCoreThreadTimeOut` 是核心线程回收的开关。
- 关闭三兄弟：`shutdown`（优雅）/ `shutdownNow`（尽力）/ `awaitTermination`（等待）。
- JDK 21 之后：IO 密集优先虚拟线程，CPU 密集仍用固定池/ForkJoin；不要混用。
- 永远显式 `new ThreadPoolExecutor(...)`，配上有界队列、线程名、拒绝策略与监控。
