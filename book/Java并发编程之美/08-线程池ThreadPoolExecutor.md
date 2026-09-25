# 第 8 章 ThreadPoolExecutor 原理探究（原书 pp.225-242）

> 全书工程价值最高的两章之一（另一是第 6 章 AQS）。线程池是 **AQS + 阻塞队列 + 状态机** 三者的组合体：
> `Worker` 用 AQS 做「空闲/忙碌」标记，任务排队在 `BlockingQueue`，线程池生命周期用一个 `AtomicInteger` 的高 3 位编码。
> 延伸专篇：[concepts/ForkJoin与工作窃取.md](concepts/ForkJoin与工作窃取.md) · [concepts/虚拟线程Loom.md](concepts/虚拟线程Loom.md)

## 一、本章地图

| 小节 | 主题 | 页码 |
| --- | --- | --- |
| 8.1 | 线程池的创建与核心参数 | 225 |
| 8.2 | `ctl`：一个 int 同时装下状态与线程数 | 228 |
| 8.3 | `execute()` 的三级执行流程 | 231 |
| 8.4 | `addWorker()` 与 `Worker`（AQS 的非典型用法） | 234 |
| 8.5 | `runWorker()` / `getTask()`：工作线程的主循环 | 237 |
| 8.6 | 拒绝策略与 `shutdown()` / `shutdownNow()` | 239 |

## 二、8.1 为什么不许用 `Executors` 创建线程池

`ThreadPoolExecutor` 的七参数构造：

```java
public ThreadPoolExecutor(
    int corePoolSize,              // 常驻核心线程数（含空闲不被回收的）
    int maximumPoolSize,           // 最大线程数
    long keepAliveTime,            // 超出核心的那部分线程，空闲多久后被回收
    TimeUnit unit,
    BlockingQueue<Runnable> workQueue,   // 任务队列
    ThreadFactory threadFactory,         // 线程工厂（给线程起名字！）
    RejectedExecutionHandler handler)    // 拒绝策略
```

`Executors` 的四个工厂方法**每一个都有生产事故级缺陷**：

| 工厂方法 | 内部实现 | 致命缺陷 |
| --- | --- | --- |
| `newFixedThreadPool(n)` | `LinkedBlockingQueue` **无界**（`Integer.MAX_VALUE`） | 任务堆积 → **堆 OOM** |
| `newSingleThreadExecutor()` | 同上 | 同上 |
| `newCachedThreadPool()` | `maximumPoolSize = Integer.MAX_VALUE` | 高并发下**无限建线程** → 线程耗尽 / native OOM |
| `newScheduledThreadPool(n)` | `DelayedWorkQueue` 无界 | 同 Fixed |

> 这也是《阿里巴巴 Java 开发手册》把「不允许用 `Executors` 创建线程池」列为**强制**项的原因——
> 缺陷不在线程池本身，而在于**工厂方法替你选了一个无界队列**，把背压（backpressure）这个你必须做的决策偷偷拿走了。

正确写法——**显式给出队列容量与拒绝策略**：

```java
var pool = new ThreadPoolExecutor(
    8, 32,
    60L, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(2000),              // 有界，形成背压
    new ThreadFactory() {                        // 给线程起名，出事时能定位
        private final AtomicInteger n = new AtomicInteger(1);
        public Thread newThread(Runnable r) {
            return new Thread(r, "biz-pool-" + n.getAndIncrement());
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy()    // 让调用者自己跑，天然降速
);
```

## 三、8.2 `ctl`：一个 int 装两件事

```java
private final AtomicInteger ctl = new AtomicInteger(ctlOf(RUNNING, 0));
private static final int COUNT_BITS = Integer.SIZE - 3;          // 29
private static final int CAPACITY   = (1 << COUNT_BITS) - 1;     // 低 29 位掩码

// runState 存高 3 位，且按数值单调递增排列
private static final int RUNNING    = -1 << COUNT_BITS;   // 111... 接受新任务 + 处理队列
private static final int SHUTDOWN   =  0 << COUNT_BITS;   // 000... 不接受新任务，但处理队列
private static final int STOP       =  1 << COUNT_BITS;   // 001... 不接受，不处理，中断在跑的
private static final int TIDYING    =  2 << COUNT_BITS;   // 010... 全部结束，workerCount=0
private static final int TERMINATED =  3 << COUNT_BITS;   // 011... terminated() 执行完
```

**为什么这样做**：线程池的「状态」与「工作线程数」必须**原子地一起变**——
否则「我先判断是 RUNNING，再去 CAS 加线程数」这两步之间状态可能已经变成 SHUTDOWN。
把它们打包进一个 `AtomicInteger`，一次 CAS 同时更新，就消除了这个竞态。

**状态迁移路径**（不可逆）：

```
RUNNING ──shutdown()──▶ SHUTDOWN ──队列空&&wc=0──▶ TIDYING ──terminated()──▶ TERMINATED
   │                                                  ▲
   └──────────shutdownNow()──▶ STOP ──── wc=0 ────────┘
```

> 记忆要点：`SHUTDOWN` 是「关门但不赶客」（队列里的任务继续做完），`STOP` 是「关门且赶客」。

## 四、8.3 `execute()`：三级递进

```java
public void execute(Runnable command) {
    if (command == null) throw new NullPointerException();
    int c = ctl.get();

    // ① 工作线程数 < corePoolSize → 直接新建核心线程，任务作为 firstTask
    if (workerCountOf(c) < corePoolSize) {
        if (addWorker(command, true)) return;
        c = ctl.get();   // 并发下失败了，重新读
    }

    // ② 仍在 RUNNING 且入队成功
    if (isRunning(c) && workQueue.offer(command)) {
        int recheck = ctl.get();                       // 入队后再查一次（经典 double-check）
        if (!isRunning(recheck) && remove(command))    // 入队期间被关闭了 → 撤回来拒绝
            reject(command);
        else if (workerCountOf(recheck) == 0)          // 允许 corePoolSize=0 的边界情形
            addWorker(null, false);
    }

    // ③ 队列也满了 → 扩容到 maximumPoolSize；还不行就拒绝
    else if (!addWorker(command, false))
        reject(command);
}
```

**最容易被误解的一点**：线程池不是「先到 corePoolSize，再排队，再扩到 max」这么简单的线性关系吗？是的——
但关键在于**队列的选择决定了扩容是否会发生**：

| 队列 | 何时会创建超过 corePoolSize 的线程 |
| --- | --- |
| `LinkedBlockingQueue`（无界） | **永远不会**。`offer()` 恒成功，永远走不到 ③ → `maximumPoolSize` 形同虚设 |
| `ArrayBlockingQueue`（有界） | 队列满时才会扩容到 max |
| `SynchronousQueue`（0 容量） | `offer()` 恒失败（无消费者时）→ **永远走 ③** → 等价于 `newCachedThreadPool` 的行为 |

> 所以「设了 `maximumPoolSize=32` 为什么线程数一直是 8？」的答案通常是：**你用了无界队列**。
> 这是面试与线上排查中出现频率最高的线程池问题。

## 五、8.4 `Worker`：AQS 的非典型用法

```java
private final class Worker extends AbstractQueuedSynchronizer implements Runnable {
    final Thread thread;
    Runnable firstTask;
    volatile long completedTasks;

    Worker(Runnable firstTask) {
        setState(-1);                                  // 初始 -1：抑制中断直到 runWorker
        this.firstTask = firstTask;
        this.thread = getThreadFactory().newThread(this);
    }
    public void run() { runWorker(this); }

    // 一个「不可重入」的独占锁
    protected boolean tryAcquire(int unused) {
        if (compareAndSetState(0, 1)) { setExclusiveOwnerThread(currentThread()); return true; }
        return false;                                  // state!=0 就失败 → 不可重入
    }
    protected boolean tryRelease(int unused) { setExclusiveOwnerThread(null); setState(0); return true; }
    public void lock()    { acquire(1); }
    public boolean tryLock() { return tryAcquire(1); }
    public void unlock()  { release(1); }
}
```

**为什么要一个「不可重入」的锁？**

第 6 章讲的 `ReentrantLock` 是可重入的（同一线程可反复 `lock`），而这里**故意不可重入**，目的是：

> **用「能否 `tryLock()` 成功」来判定一个工作线程此刻是空闲还是在执行任务。**

- 线程执行任务前 `w.lock()`（state 0→1），执行完 `w.unlock()`（1→0）
- `shutdown()` 要中断**空闲**线程时，只需 `w.tryLock()`：成功说明它没在跑任务，可以安全中断；失败说明它在忙，不动它
- 如果用可重入锁，同一个线程重入时 `tryLock()` 也会成功，这个判定就失效了

**`setState(-1)` 的作用**：`Worker` 刚创建、还没进入 `runWorker` 时不允许被中断——
否则 `shutdownNow()` 可能在线程还没开始跑时就中断它，导致 `firstTask` 丢失。

`addWorker()` 的两层循环（`retry:` 标签 + 内层 CAS）是标准的 **CAS + 状态重检查** 模式：

```java
retry:
for (;;) {
    int c = ctl.get();
    int rs = runStateOf(c);
    // SHUTDOWN 之后不接受新任务；但 SHUTDOWN 且队列非空时，允许加一个「无 firstTask」的线程来消化队列
    if (rs >= SHUTDOWN && !(rs == SHUTDOWN && firstTask == null && !workQueue.isEmpty()))
        return false;
    for (;;) {
        int wc = workerCountOf(c);
        if (wc >= CAPACITY || wc >= (core ? corePoolSize : maximumPoolSize)) return false;
        if (compareAndIncrementWorkerCount(c)) break retry;      // 唯一成功出口
        c = ctl.get();
        if (runStateOf(c) != rs) continue retry;                 // 状态变了，回到外层重新判断
    }
}
// ...真正创建 Worker、加入 workers（需 mainLock）、t.start()
```

## 六、8.5 `runWorker()` 与 `getTask()`

```java
final void runWorker(Worker w) {
    Thread wt = Thread.currentThread();
    Runnable task = w.firstTask;
    w.firstTask = null;
    w.unlock();                               // state -1 → 0，从此允许中断
    boolean completedAbruptly = true;
    try {
        while (task != null || (task = getTask()) != null) {   // 主循环
            w.lock();                                          // 标记「忙碌」
            if ((runStateAtLeast(ctl.get(), STOP) ||
                 (Thread.interrupted() && runStateAtLeast(ctl.get(), STOP))) &&
                !wt.isInterrupted())
                wt.interrupt();                                // STOP 时确保被中断
            try {
                beforeExecute(wt, task);                       // 钩子
                Throwable thrown = null;
                try { task.run(); }
                catch (RuntimeException | Error x) { thrown = x; throw x; }
                finally { afterExecute(task, thrown); }        // 钩子
            } finally {
                task = null;
                w.completedTasks++;
                w.unlock();                                    // 标记「空闲」
            }
        }
        completedAbruptly = false;
    } finally {
        processWorkerExit(w, completedAbruptly);               // 回收 + 补偿线程
    }
}
```

`getTask()` 决定了线程如何退出（这是 `keepAliveTime` 的落点）：

```java
private Runnable getTask() {
    boolean timedOut = false;
    for (;;) {
        int c = ctl.get();
        // SHUTDOWN 且队列空 / STOP → 减线程数并返回 null（线程自然退出）
        if (runStateOf(c) >= SHUTDOWN && (runStateOf(c) >= STOP || workQueue.isEmpty())) {
            decrementWorkerCount(); return null;
        }
        int wc = workerCountOf(c);
        // 核心线程是否也参与超时回收，由 allowCoreThreadTimeOut 决定
        boolean timed = allowCoreThreadTimeOut || wc > corePoolSize;
        if ((wc > maximumPoolSize || (timed && timedOut)) && (wc > 1 || workQueue.isEmpty())) {
            if (compareAndDecrementWorkerCount(c)) return null;
            continue;
        }
        try {
            Runnable r = timed
                ? workQueue.poll(keepAliveTime, TimeUnit.NANOSECONDS)  // 超时等待
                : workQueue.take();                                     // 永久等待
            if (r != null) return r;
            timedOut = true;                                            // 超时了，下轮退出
        } catch (InterruptedException retry) {
            timedOut = false;                                           // 被中断则重新判断状态
        }
    }
}
```

**这里有一个极其隐蔽的坑**：`getTask()` 里 `catch (InterruptedException)` 后把 `timedOut` 重置为 false 并**继续循环**，而不是直接退出。
这意味着**线程池里的任务如果被外部 `Thread.interrupt()`，不会导致工作线程退出，但中断状态被吞掉了**。
所以：**不要在线程池任务里依赖中断状态做业务语义**，要用自己的标志位。

## 七、8.6 拒绝策略与关闭

四种内置 `RejectedExecutionHandler`：

| 策略 | 行为 | 适用 |
| --- | --- | --- |
| `AbortPolicy`（**默认**） | 抛 `RejectedExecutionException` | 希望Fail Fast，由上游感知 |
| `CallerRunsPolicy` | **调用者线程自己执行该任务** | 最推荐的兜底：天然形成反压，调用方变慢 → 提交变慢 |
| `DiscardPolicy` | 静默丢弃，无任何日志 | 基本不该用（丢了都不知道） |
| `DiscardOldestPolicy` | 丢弃队列头（最老的任务），重试提交 | 允许丢旧任务的场景（如实时行情） |

> 生产建议：**有界队列 + `CallerRunsPolicy`**。它把「系统过载」这件事诚实地反馈给了调用方，而不是假装没事。

关闭的两种方式：

```java
pool.shutdown();      // 平滑：不再收新任务，队列里的继续执行完
pool.shutdownNow();   // 立即：尝试中断所有工作线程，返回队列中尚未执行的 List<Runnable>
pool.awaitTermination(30, TimeUnit.SECONDS);   // 阻塞等待真正结束
```

`shutdown()` 只中断**空闲**线程（靠 `tryLock()` 判断），所以正在执行的任务不会被打断；
`shutdownNow()` 则对所有 `Worker` 调 `interrupt()`，正在执行的任务若响应中断就会提前结束。

## 八、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 5 | `ThreadPoolExecutor`、`Executors`、`Future`/`FutureTask` 引入（JSR 166） |
| JDK 6 | `allowCoreThreadTimeOut` 等增强 |
| JDK 8 | `CompletableFuture` 提供异步编排，线程池成为其默认执行器（`ForkJoinPool.commonPool()`） |
| JDK 9 | 内部 `Unsafe` → `VarHandle` |
| **JDK 19/21** | 🔴 **虚拟线程**（JEP 425/444）+ `Executors.newVirtualThreadPerTaskExecutor()` |
| JDK 21 | `ThreadPoolExecutor` 本身**并未被取代**，但**使用范式发生根本变化**（见下） |

### 虚拟线程带来的范式反转

| | 平台线程 + 线程池 | 虚拟线程（JDK 21+） |
| --- | --- | --- |
| 稀缺资源 | OS 线程（几千个就到顶） | **内存**（每个虚拟线程栈约几百字节～几 KB，可百万级） |
| 池化的目的 | 复用昂贵的 OS 线程 | **没有意义**——创建成本极低 |
| 正确用法 | 按 CPU/IO 比例配线程池 | **每个任务一个虚拟线程，不要池化** |
| 阻塞代价 | 占住 OS 线程，吞吐崩塌 | 几乎为零（挂载/卸载到 carrier thread） |

```java
// JDK 21+：不要池化虚拟线程
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 100_000).forEach(i -> executor.submit(() -> {
        Thread.sleep(Duration.ofSeconds(1));   // 阻塞几乎免费
        return i;
    }));
}
```

> ⚠️ **本书第 8 章的整套调优方法论（corePoolSize 公式、队列容量估算）是针对「线程昂贵」这一前提建立的。**
> 在虚拟线程下这些公式**全部失效**——但**对 CPU 密集型任务仍然有效**：
> CPU 密集型仍应用**固定大小的平台线程池**（线程数 ≈ CPU 核数），虚拟线程只对 **IO 密集型**有奇效。
> 这是最容易搞错的一点：**虚拟线程不会让 CPU 密集型任务变快**。

## 九、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| 线程池/工作队列的理论基础 | **Little's Law**（`L = λW`） | Little, *A Proof for the Queuing Formula L = λW*, Operations Research 9(3), 1961 —— 线程池大小估算的数学依据 |
| Fork/Join 与工作窃取 | **Lea, *A Java Fork/Join Framework*** | **OOPSLA 2000**，Doug Lea 本人的论文，`ThreadPoolExecutor` 与 `ForkJoinPool` 的设计同源 |
| 工作窃取调度 | **Blumofe & Leiserson, *Scheduling Multithreaded Computations by Work Stealing*** | FOCS 1994 / **JACM 46(5), 1999** —— 证明 work-stealing 的空间与时间界 |
| 任务队列算法 | Michael & Scott, *Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms* | PODC 1996（见 [07 章](07-并发队列原理剖析.md)） |
| 排队论与容量规划 | Gunther, *Guerrilla Capacity Planning* | 2015（工程向，Little's Law 的实操） |
| 结构化并发（现代替代） | **Najafzadeh, *Structured Concurrency*** | 见 [concepts/结构化并发与ScopedValue.md](concepts/结构化并发与ScopedValue.md) |

## 十、近年研究与工业界前沿（2020-2026）

**同行评审论文 / 权威技术报告**

- **虚拟线程的设计与实现**：OpenJDK Project Loom 的官方文档与 JEP 444 是最权威来源，其中明确了「虚拟线程不应用于 CPU 密集任务」「不要池化虚拟线程」两条工程准则。
- **自适应线程池 sizing（2020-2025）**：学术界持续研究根据运行时反馈（队列延迟、CPU 利用率、尾延迟 SLO）自动调整池大小；核心思路仍是 Little's Law 的动态版本。这类工作多以 USENIX ATC / EuroSys 的系统论文形式出现，尚无被 JDK 采纳的实现。

**工业界资料（非同行评审）**

- **Netflix 的线程池动态配置**（Hystrix 后继 Resilience4j 的 `ThreadPoolBulkhead`）：用线程池做舱壁隔离（bulkhead），把「一个下游慢」限制在固定线程数内。
  https://github.com/resilience4j/resilience4j
- **Netty `EventLoop`**：本质是一个**单线程的 `ScheduledExecutorService`**，是「IO 密集场景下少量线程 + 事件循环」的工业级范本，也是虚拟线程之前的通行解法。
  https://github.com/netty/netty
- **Tomcat / Jetty 的 `Executor` 抽象**：Web 容器的线程池调优（acceptors/poller 与 worker 分离）是 `ThreadPoolExecutor` 最复杂的真实用法。
- **Dubbo / gRPC Java 的线程池隔离**：按服务维度分池，避免慢服务耗尽全局线程。
- **Micrometer / Dropwizard Metrics 的 `ExecutorService` 埋点**：线程池**必须**监控（活跃数、队列长度、拒绝次数），否则线上问题完全不可见。

**最小验证范式**

```java
// JMH 之外的最小观测：暴露线程池内部状态
ThreadPoolExecutor p = (ThreadPoolExecutor) executor;
System.out.printf("pool=%d/%d active=%d queue=%d completed=%d rejected=?%n",
    p.getPoolSize(), p.getMaximumPoolSize(), p.getActiveCount(),
    p.getQueue().size(), p.getCompletedTaskCount());
```

## 十一、常见误区 / 本书需修正之处

1. **⚠️ 最大的误区：以为 `maximumPoolSize` 一定会生效。** 无界队列下它永远不会触发（见第四节表格）。本书对这点强调不足。
2. **⚠️ 本书的线程池大小公式需要按任务类型区分**：
   - CPU 密集：`N_threads ≈ N_cpu`（+1 有余）；`Runtime.getRuntime().availableProcessors()`
   - IO 密集：本书给的公式（按 IO 等待比例放大）在**平台线程**下成立；**虚拟线程下应直接改成「不要池化」**
3. **`Executors` 的四个工厂方法在生产环境一律禁用**（本书成书时 JDK 8，这一共识在 2020 年后才通过《阿里 Java 开发手册》广泛普及）。
4. **吞掉中断**：`getTask()` 会吞掉 `InterruptedException`（见第六节），业务代码不要依赖线程池任务的中断状态。
5. **`ThreadLocal` 与线程池冲突**：线程复用导致 `ThreadLocal` 串数据 + 内存泄漏（见 [concepts/ThreadLocal与内存泄漏.md](concepts/ThreadLocal与内存泄漏.md)），这是本书第 8 章未展开但生产上必踩的坑。
6. **虚拟线程下 `ThreadLocal` 的代价被放大**：百万级虚拟线程 × `ThreadLocal` = 巨大的内存压力 → JDK 21+ 用 `ScopedValue` 替代（见 [concepts/结构化并发与ScopedValue.md](concepts/结构化并发与ScopedValue.md)）。
7. **不要忽略 `ThreadFactory`**：默认线程名 `pool-1-thread-1` 在故障排查时毫无信息量，且无法区分业务池。
