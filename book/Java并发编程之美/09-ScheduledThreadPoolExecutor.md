# 第 9 章 ScheduledThreadPoolExecutor 原理探究（原书 pp.243-255）

> 第 8 章的延续：把普通 `BlockingQueue` 换成 **`DelayedWorkQueue`**（按到期时间排序的堆），
> 再叠加「周期任务的三种语义」，就得到了定时任务线程池。
> 延伸专篇：[concepts/ForkJoin与工作窃取.md](concepts/ForkJoin与工作窃取.md)

## 一、本章地图

| 小节 | 主题 | 页码 |
| --- | --- | --- |
| 9.1 | `ScheduledThreadPoolExecutor` 的结构与 `ScheduledFutureTask` | 243 |
| 9.2 | `DelayedWorkQueue`：延迟队列的实现 | 246 |
| 9.3 | `schedule()`：一次性延迟任务 | 249 |
| 9.4 | `scheduleAtFixedRate()` vs `scheduleWithFixedDelay()` | 251 |
| 9.5 | 与 `Timer` 的对比，以及生产级替代方案 | 253 |

## 二、9.1 结构：三层包装

```java
public class ScheduledThreadPoolExecutor extends ThreadPoolExecutor
        implements ScheduledExecutorService {
    // 注意：maximumPoolSize 对它无效（构造时被忽略），队列是无界的 DelayedWorkQueue
    private final AtomicLong sequencer = new AtomicLong();   // 到期时间相同时的 tie-breaker
    volatile boolean continueExistingPeriodicTasksAfterShutdown;  // 默认 false
    volatile boolean removeOnCancelPolicy;                        // 默认 false ⚠️
}
```

任务被包成 `ScheduledFutureTask`（继承 `FutureTask` 并实现 `RunnableScheduledFuture`）：

```java
private class ScheduledFutureTask<V> extends FutureTask<V> implements RunnableScheduledFuture<V> {
    private final long sequenceNumber;   // 序号，用于 FIFO 打破时间相同的平局
    private long time;                   // 下次执行的绝对时间（nanoTime）
    private final long period;           // >0 固定频率; <0 固定延迟; 0 一次性
    ...
}
```

**`period` 的符号编码了三种语义**，这是本章的核心设计：

| `period` | 含义 | 对应 API |
| --- | --- | --- |
| `0` | 一次性任务 | `schedule()` |
| `> 0` | **固定频率**（fixed rate）：以上一次**开始时间**为基准累加 | `scheduleAtFixedRate()` |
| `< 0` | **固定延迟**（fixed delay）：以上一次**结束时间**为基准累加 | `scheduleWithFixedDelay()` |

## 三、9.2 `DelayedWorkQueue`：堆 + Leader-Follower

`DelayedWorkQueue` 是一个**基于数组的小顶堆**（按 `time` 排序），不是 `PriorityQueue` 的简单包装——它自己实现堆是为了做**leader-follower 优化**：

```java
private Thread leader = null;   // 当前「盯」着堆顶的线程

public Runnable take() throws InterruptedException {
    final ReentrantLock lock = this.lock;
    lock.lockInterruptibly();
    try {
        for (;;) {
            RunnableScheduledFuture<?> first = queue[0];
            if (first == null)
                available.await();                       // 空队列，无限等
            else {
                long delay = first.getDelay(NANOSECONDS);
                if (delay <= 0) return finishPoll(first);  // 到期了，取走
                // 未到期：放弃 first 引用，避免持有对象
                first = null;
                if (leader != null)
                    available.await();                   // 已有 leader，自己当 follower 无限等
                else {
                    Thread thisThread = currentThread();
                    leader = thisThread;                 // 自己当 leader
                    try {
                        available.awaitNanos(delay);     // 只等到堆顶到期
                    } finally {
                        if (leader == thisThread) leader = null;
                    }
                }
            }
        }
    } finally {
        if (leader == null && queue[0] != null)
            available.signal();                          // 唤醒一个 follower 接任 leader
        lock.unlock();
    }
}
```

**为什么需要 leader-follower？**

如果每个等待线程都 `awaitNanos(delay)`，那么 N 个线程会在同一时刻被唤醒，其中只有 1 个能真正取到任务，
其余 N-1 个是**虚假唤醒**（spurious wakeup）——白白浪费 N-1 次线程调度。

> leader-follower 的做法：**只让一个线程（leader）定时等待到堆顶到期，其余线程（follower）无限等待**。
> leader 拿到任务后唤醒一个 follower 接任。这样同一时刻只有一次定时等待。

这个模式出自 Schmidt 的 *Pattern-Oriented Software Architecture Vol. 2*（2000），
在第 7 章的 `DelayQueue` 里也用了同一套机制。

> `poll(timeout)` 版本则不用 leader-follower——因为每个线程有自己的超时时间，无法共享。

## 四、9.3/9.4 三种提交方式

```java
ScheduledExecutorService ses = Executors.newScheduledThreadPool(4);

// ① 一次性：延迟 3 秒执行
ses.schedule(() -> System.out.println("once"), 3, TimeUnit.SECONDS);

// ② 固定频率：每 1 秒一次，以上次「开始」为基准
ses.scheduleAtFixedRate(task, 0, 1, TimeUnit.SECONDS);

// ③ 固定延迟：上次「结束」后再等 1 秒
ses.scheduleWithFixedDelay(task, 0, 1, TimeUnit.SECONDS);
```

**两者的关键差异在任务执行时间超过周期时**：

```
任务耗时 3s，周期 1s

scheduleAtFixedRate:      期望时刻: 0  1  2  3  4  5  6
                          实际执行: [==0==]  [===3===]  [===6===]
                          → 会「追赶」：落后时连续触发（无重叠，同一任务不并发）
                          实际触发时刻: 0, 3, 6, 9 ...（每次执行完立即开始下一次）

scheduleWithFixedDelay:   实际执行: [==0==] 等待1s [===4===] 等待1s [===8===]
                          → 不追赶，节奏稳定：结束 + delay
                          实际触发时刻: 0, 4, 8, 12 ...
```

源码中这一点体现为下次时间的计算：

```java
private void setNextRunTime() {
    long p = period;
    if (p > 0)  // fixed rate：基于「计划开始时间」累加，会追赶
        time += p;
    else        // fixed delay：基于「现在」（即刚结束的时刻）累加
        time = triggerTime(-p);
}
```

⚠️ **两个必须知道的语义细节**：

1. **同一个周期任务永远不会并发执行**。若上一次还没结束，下一次不会启动（即使是 `AtFixedRate`）——因为它要先出队、执行完、重新计算 `time` 再入队。
2. **周期任务抛异常后就永久停止了**（异常被 `FutureTask` 吞进 `future.get()` 里，但你通常没调 `get()`，于是**静默停止**）。
   → **必须在周期任务内部 `try-catch` 所有异常**，这是定时任务最常见的线上事故。

```java
// 正确写法
ses.scheduleAtFixedRate(() -> {
    try { doWork(); }
    catch (Throwable t) { log.error("scheduled task failed", t); }  // 绝不让异常逃逸
}, 0, 1, TimeUnit.MINUTES);
```

## 五、9.5 为什么不许用 `Timer`

| | `Timer`（JDK 1.3） | `ScheduledThreadPoolExecutor`（JDK 5+） |
| --- | --- | --- |
| 线程模型 | **单线程** | 多线程池 |
| 任务异常 | 一个任务抛异常 → **整个 Timer 线程死掉**，所有后续任务全部失效 | 只影响该任务（但仍会终止该周期任务） |
| 时间基准 | `System.currentTimeMillis()` —— **受系统时钟调整影响**（NTP 校时、手动改表） | `System.nanoTime()` —— **单调递增**，不受时钟调整影响 |
| 周期语义 | 只有 fixed delay 一种 | 支持 rate / delay 两种 |
| CPU 密集 | 单线程串行，慢任务阻塞后续所有任务 | 可并行 |

> **结论：任何新代码都不要用 `Timer` / `TimerTask`。** 本书成书时这一点已是共识，但 `Timer` 仍在大量遗留代码里。

## 六、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 5 | `ScheduledThreadPoolExecutor`、`DelayedWorkQueue` 引入 |
| JDK 6 | `removeOnCancelPolicy` 相关改进 |
| **JDK 9** | 内部 `Unsafe` → `VarHandle`；`CompletableFuture` 增加 `orTimeout()` / `completeOnTimeout()` |
| **JDK 21** | 🔴 虚拟线程下，定时任务里的阻塞不再占用 OS 线程；但**虚拟线程不适合承载长周期定时任务**（见下） |

### 虚拟线程与定时任务的关系（需要澄清的常见误解）

- ✅ 虚拟线程**可以**用在 `ScheduledThreadPoolExecutor` 里执行任务（阻塞廉价）
- ❌ 但 **`ScheduledThreadPoolExecutor` 自身的「调度线程」（跑 `DelayedWorkQueue.take()` 的那些）永远是平台线程**，无法虚拟线程化——它需要长时间阻塞在 `awaitNanos` 上，这正是平台线程池的本职工作
- ⚠️ 实践中**几乎不需要**给定时任务配虚拟线程：定时任务通常不密集，平台线程池完全够用

## 七、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| **Leader-Follower 模式** | Schmidt, Stal, Rohnert, Buschmann, *Pattern-Oriented Software Architecture Vol. 2: Patterns for Concurrent and Networked Objects* | Wiley, 2000（第 3 章专述 LF 模式） |
| 延迟队列 / 优先队列 | **Fredman & Tarjan, *Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms*** | **JACM 34(3), 1987** —— 堆的理论基础 |
| 实时调度的经典结果 | **Liu & Layland, *Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment*** | **JACM 20(1), 1973** —— 周期任务可调度的充分条件（利用率 ≤ n(2^(1/n)-1)） |
| 单调时钟的工程必要性 | Mills, *Computer Network Time Synchronization* | 2nd ed., CRC 2011（NTP 为何会回拨时钟，以及为何要用 monotonic clock） |
| 时间轮（替代方案的理论） | 见下方工业界 —— Kafka 的 `TimingWheel` | — |

## 八、近年研究与工业界前沿（2020-2026）

**同行评审论文**

- **时间轮 vs 堆的复杂度对比**是近年工程论文里反复出现的主题：JDK 的 `DelayedWorkQueue` 是 O(log n) 的堆，
  而**分层时间轮（Hierarchical Timing Wheel）在海量短周期任务下能做到近似 O(1)**。
  原始思想出自 Varghese & Lauck, *Hashed and Hierarchical Timing Wheels*（**SOSP 1987 / TOCS 1997**）——
  这篇论文常被误认为只是「工业技巧」，实际上它有严格的复杂度分析，是本节最值得补读的经典文献。

**工业界资料（非同行评审）**

- **Netty `HashedWheelTimer`**：分层时间轮的经典 Java 实现，适合数万级定时器。
  https://github.com/netty/netty
- **Kafka 的 `TimingWheel`**：Kafka 的延迟操作（延迟生产/消费）用的就是分层时间轮，是「什么时候该抛弃 JDK 的 `DelayedWorkQueue`」的最佳判例。
- **Quartz**：企业级调度（cron 表达式、持久化、集群），当你的需求已经超出「线程池定时」的范畴时用它。
  https://github.com/quartz-scheduler/quartz
- **`removeOnCancelPolicy` 的坑**：默认 `false` 时，被 `cancel()` 的任务**不会立即从队列移除**，会一直占堆内存直到到期。
  任务量大时必须显式开启：
  ```java
  ses.setRemoveOnCancelPolicy(true);      // 否则 cancel 的定时任务堆积 → 内存泄漏
  ```

## 九、常见误区 / 本书需修正之处

1. **⚠️ `maximumPoolSize` 对 `ScheduledThreadPoolExecutor` 完全无效**——它的队列是**无界**的 `DelayedWorkQueue`，
   构造时传入的 `maximumPoolSize` 被直接忽略。本书未明确点出这一点，极易造成误配。
2. **⚠️ 周期任务抛异常会静默永久停止**，这是线上事故重灾区（见第四节）。必须内部 try-catch。
3. **⚠️ `Executors.newScheduledThreadPool()` 同样是无界队列**，大量堆积的定时任务会导致 OOM。
4. **⚠️ `removeOnCancelPolicy` 默认 false** → `cancel()` 的任务继续占堆 → 内存泄漏。生产必须设为 `true`。
5. **`scheduleAtFixedRate` 在系统时钟回拨时的行为**：因为用的是 `nanoTime()`（单调），**不受影响**——
   这是它相对 `Timer` 的关键优势，但很多人误以为定时任务都怕时钟回拨。
6. **虚拟线程不是定时任务的银弹**：调度线程仍是平台线程（见第六节），别盲目替换。
7. **分布式场景不要用单机 `ScheduledThreadPoolExecutor`**：多实例部署会导致任务重复执行。
   需要分布式锁或专门的调度中心（XXL-Job、ElasticJob、Quartz 集群模式）。
