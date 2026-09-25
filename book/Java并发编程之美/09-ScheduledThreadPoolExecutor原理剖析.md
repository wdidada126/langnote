# 第 9 章 Java 并发包中 ScheduledThreadPoolExecutor 原理探究（原书 pp.243-255）

> 主角：`ScheduledThreadPoolExecutor`、`DelayedWorkQueue`、`ScheduledFutureTask`
> 前置：第 8 章 `ThreadPoolExecutor`（它继承了 `ThreadPoolExecutor`）、第 7 章的 `DelayQueue`（`DelayedWorkQueue` 是其无界堆版本）

## 一、本章地图

| 小节 | 主题 | 页码 |
| --- | --- | --- |
| 9.1 | 介绍 | 243 |
| 9.2 | 类图介绍 | 243 |
| 9.3.1 | `schedule(Runnable, long, TimeUnit)` | 246 |
| 9.3.2 | `scheduleWithFixedDelay(...)` | 252 |
| 9.3.3 | `scheduleAtFixedRate(...)` | 254 |
| 9.4 | 总结 | 255 |

## 二、9.1–9.2 类图与设计定位

```java
public class ScheduledThreadPoolExecutor
        extends ThreadPoolExecutor
        implements ScheduledExecutorService { ... }
```

与父类 `ThreadPoolExecutor` 的三个关键差异：

1. **任务队列固定为 `DelayedWorkQueue`**（无界、堆结构），所以 `maximumPoolSize` 无效（无界队列永不触发扩容）。
2. **任务被包装成 `ScheduledFutureTask`**，携带 `time`（下次触发的绝对纳秒时间）、`period`（>0 固定速率，<0 固定延迟，0 一次性）、`sequenceNumber`（同时间平局时的 FIFO 排序键）。
3. **时间基准是 `System.nanoTime()`（单调时钟）而不是 `currentTimeMillis()`（墙钟）**——后者会被 NTP 校时、闰秒、手动改系统时间影响，可能导致定时任务错乱。这是本书值得强调但常被忽略的细节。

```java
private class ScheduledFutureTask<V> extends FutureTask<V> implements RunnableScheduledFuture<V> {
    private final long sequenceNumber;                 // 构造时自增，用于 compareTo 平局裁决
    private long time;                                 // 下次执行时间（nanoTime 基准）
    private final long period;
    public int compareTo(Delayed other) {
        long diff = time - ((ScheduledFutureTask) other).time;
        if (diff != 0) return (diff < 0) ? -1 : 1;     // 先按时间
        return (sequenceNumber < other.sequenceNumber) ? -1 : 1;   // 再按提交顺序（FIFO）
    }
}
```

> `compareTo` 的**两级排序**很重要：若只按时间比较，`TreeSet`/堆 不保证稳定性，先提交的同刻任务可能后执行；`sequenceNumber` 用 `AtomicLong sequencer` 全局自增，保证 FIFO。这与第 7 章 `DelayQueue` 里 `Leader-Follower` 的设计同源——`DelayedWorkQueue` 事实上就是 `DelayQueue` 的"线程本地化"重写版本（Doug Lea 注释里明确说明：为线程池场景做了定制，用 `Thread leader` 避免不必要的 timed wait 竞态）。

## 三、9.3.1 `schedule()`：一次性延时任务

```java
public ScheduledFuture<?> schedule(Runnable command, long delay, TimeUnit unit) {
    RunnableScheduledFuture<?> t = decorateTask(command,
        new ScheduledFutureTask<Void>(command, null,
                                      triggerTime(delay, unit),   // now + delay
                                      sequencer.getAndIncrement()));
    delayedExecute(t);
    return t;
}

private void delayedExecute(RunnableScheduledFuture<?> task) {
    if (isShutdown()) reject(task);
    else {
        super.getQueue().add(task);                     // 入堆，O(log n)
        if (isShutdown() && !canRunInCurrentRunState(task.period) && remove(task))
            task.cancel(false);
        else
            ensurePrestart();                           // 至少保证一个 worker 存在
    }
}
```

- `triggerTime` 内部做的是 `now() + unit.toNanos(delay)`，并对**负延时**做保护（`triggerTime` 里 `delay < 0` 会被当作 0 处理的一部分逻辑在 `triggerTime(long)` 中）。
- 注意 `ensurePrestart()` 与父类 `execute()` 的区别：定时任务**不走 core→queue→max 决策树**，而是直接入堆并保底开一个线程。

**任务如何被触发**：工作线程 `getTask()` → `DelayedWorkQueue.take()` → 队首元素 `getDelay(NANOSECONDS) <= 0` 时出队 → `runWorker` 调用 `ScheduledFutureTask.run()`：

```java
public void run() {
    if (!canRunInCurrentRunState(periodic)) { cancel(false); return; }
    if (!periodic) { ScheduledFutureTask.super.run(); }        // 一次性
    else if (ScheduledFutureTask.super.runAndReset()) {         // 周期性：跑完且成功 reset
        setNextRunTime();                                      // 计算下次时间
        reExecutePeriodic(outerTask);                          // 重新入堆
    }
}
```

## 四、9.3.2 vs 9.3.3：`fixedRate` 与 `fixedDelay` —— `period` 的正负号

| 方法 | `period` 符号 | 下次执行时间计算 | 语义 |
| --- | --- | --- | --- |
| `scheduleAtFixedRate(r, initDelay, period, unit)` | **正** | `time = time + period` | 按"绝对频率"追赶：不管任务跑了多久，都以固定周期排期 |
| `scheduleWithFixedDelay(r, initDelay, delay, unit)` | **负** | `time = now() - period`（即 `now + delay`） | 按"任务结束 + delay"排期 |

```java
private void setNextRunTime() {
    long p = period;
    if (p > 0) time += p;                       // fixedRate：在上次理论时间点累加
    else       time = triggerTime(-p);          // fixedDelay：从"现在"起算
}
```

由此产生两个必须记住的行为差异：

1. **fixedRate 会"追赶"**：如果某次任务执行耗时超过了 period，后续会连续触发多次以补上进度（可能出现"一次卡住、之后疯狂补跑"）。适合**绝对周期型**任务（如每 5 秒上报一次指标）。
2. **fixedDelay 不会追赶**，永远在上一次**结束**后再等 delay。适合**依赖上一次执行结果/资源**的任务（如轮询、重连）。

> ⚠️ **本书没讲清的第三点**：**周期性任务一旦抛异常就永久停止**。`runAndReset()` 在任务抛异常时返回 `false`，于是不再 `reExecutePeriodic`，该任务从线程池中"消失"且**没有任何日志**——这是生产上"定时任务悄悄不跑了"的头号原因。解决办法：任务体内部必须 `try/catch` 兜住所有异常。

## 五、`DelayedWorkQueue`：为定时场景定制的堆

`DelayedWorkQueue` 是一个**基于数组的二叉小顶堆**（`RunnableScheduledFuture[] queue`），与 `DelayQueue`（用 `PriorityQueue`）思路一致，但做了线程池定制：

- **无界**（`grow` 扩容，最大 `Integer.MAX_VALUE - 8`），因此 `maximumPoolSize` 无意义。
- 用 **`leader` 线程**（Leader-Follower 变体）优化：只有 leader 线程做 `available.awaitNanos(delay)` 定时等待，其余线程无限期等待，避免所有线程同时被唤醒又同时抢锁的"惊群"。
- `siftUp`/`siftDown` 用 `compareTo` 排序，插入 O(log n)，取队首 O(1)，出队 O(log n)。
- 与 `DelayQueue` 的另一个差别：它 **`remove(Object)` 支持按任务对象删除**（堆里维护了 `heapIndex`），这是 `cancel()` 生效的基础。

> 对比 `java.util.Timer`：`Timer` 是**单线程** + 一个 `TaskQueue`，一个任务抛未捕获异常会**终止整个 Timer 线程**，且使用 `currentTimeMillis()` 墙钟。所以 `ScheduledThreadPoolExecutor` 是 `Timer` 的官方替代品（见第 11.5 节）。

## 六、关闭策略：两个容易被忽略的参数

`ScheduledThreadPoolExecutor` 额外提供两个关闭开关：

| 开关 | 默认 | 作用 |
| --- | --- | --- |
| `setContinueExistingPeriodicTasksAfterShutdownPolicy(boolean)` | **false** | `shutdown()` 后是否继续跑已存在的周期性任务 |
| `setExecuteExistingDelayedTasksAfterShutdownPolicy(boolean)` | **true** | `shutdown()` 后是否继续跑已存在的一次性延时任务 |

默认语义：**一次性延时任务在 shutdown 后仍会执行；周期性任务在 shutdown 后不再执行**。这与 `ThreadPoolExecutor.shutdown()` "跑完队列"略有差异，是 `canRunInCurrentRunState(periodic)` 判断的结果。业务上若希望优雅停机时把周期任务也跑完（如 flush 一次），需要显式打开第一个开关。

另外：**`shutdownNow()` 返回的 List 不包含已被取消的任务**，`cancel(false)` 不会中断正在执行的任务，`cancel(true)` 才会。

## 七、JDK 版本演进

| 版本 | 变更 | 影响 |
| --- | --- | --- |
| JDK 5 | `ScheduledThreadPoolExecutor` 引入（JSR 166） | 取代 `Timer` |
| JDK 6 | `ScheduledExecutorService` 增加 `scheduleAtFixedRate` 的规范化语义说明 | — |
| JDK 9 | `CompletableFuture` 增加 `orTimeout` / `completeOnTimeout`（内部用 `Delayer` 的 `ScheduledThreadPoolExecutor` 单例） | 异步超时成为标准能力 |
| JDK 21 | 虚拟线程下 `ScheduledExecutorService` 仍可用，但**阻塞的定时任务会占住 carrier** | IO 型定时任务建议"虚拟线程 + sleep 循环"而非占用调度池 |
| JDK 21+ | `ScheduledThreadPoolExecutor` 未做虚拟线程化改造 | 短任务仍推荐平台线程池；长阻塞任务应派发到虚拟线程执行 |

> 实践经验：定时任务体里**不要做长时间阻塞 IO**。正确姿势是 `schedule()` 只负责触发，任务体立刻把实际工作 `submit` 到业务线程池；或（JDK 21+）在 `newVirtualThreadPerTaskExecutor()` 里用 `Thread.sleep` 自己写循环。

## 八、经典论文与近年研究

| 论文 / 工作 | 出处 | 关联 |
| --- | --- | --- |
| Michael & Scott, *...Blocking Concurrent Queue Algorithms*（含阻塞的优先级实现讨论） | PODC 1996 | `DelayedWorkQueue` 的阻塞优先级队列思想基础 |
| Varghese & Lauck, *Hashed and Hierarchical Timing Wheels* | TOCS 1996 | **时间轮（timing wheel）**——`DelayedWorkQueue` 的堆是 O(log n)，时间轮是 O(1)；Netty `HashedWheelTimer`、Kafka `TimingWheel` 都用它 |
| Doug Lea, *The java.util.concurrent Synchronizer Framework* | JACM 2005 | `DelayedWorkQueue` 内部用 `ReentrantLock` + `Condition` 实现的等待/通知 |
| Leader-Follower 模式（Buschmann et al., *POSA 2*, 1996） | 模式语言 | `leader` 字段的设计来源 |
| *Priority Queue* 经典堆结构（Williams 1964 / Floyd 1964） | CACM | `siftUp`/`siftDown` |

**近年研究（2020 后）**：

- **定时器数据结构的再评估**：近年（EuroSys/ATC 2022-2025）多篇工作指出，在百万级定时器场景下"堆"的 cache 局部性差，分层时间轮（hierarchical timing wheel）与 4-ary 堆更优；Linux 内核 `hrtimer` 亦从红黑树迁移到基于时间轮的改进（6.x 的 timer wheel 优化讨论）。
- **分布式调度的一致性**：Cron 类任务在分布式环境需要选主/幂等，研究多集中在 Raft leader lease（Ongaro & Ousterhout, ATC 2014）与幂等执行记录上——对应工程实现是 XXL-JOB、ElasticJob。
- **单调时钟与分布式时间**：Google TrueTime（Corbett et al., OSDI 2012 / ToCS 2013）说明墙钟不可靠，`nanoTime()` 的选择在系统层面是对的。

## 九、工业界最新开源实现

| 项目 | 地址 | 看点 |
| --- | --- | --- |
| **OpenJDK** | `src/java.base/share/classes/java/util/concurrent/ScheduledThreadPoolExecutor.java` | 权威实现；`DelayedWorkQueue` 在同一文件里 |
| **Netty `HashedWheelTimer`** | https://github.com/netty/netty | O(1) 定时，适合海量短超时（连接超时、心跳） |
| **Kafka `TimingWheel`** | https://github.com/apache/kafka | 分层时间轮，支撑百万级延迟操作（`DelayedOperationPurgatory`） |
| **Quartz** | https://github.com/quartz-scheduler/quartz | 企业级 Cron 调度，支持持久化、集群、misfire 策略 |
| **XXL-JOB / ElasticJob / PowerJob** | 国产开源 | 分布式定时任务：分片广播、失败重试、动态调度、控制台 |
| **Spring `@Scheduled`** | spring-context | 默认单线程 `ThreadPoolTaskScheduler`，**必须自定义 `setPoolSize`**，否则所有定时任务串行互相阻塞 |
| **Akka Scheduler** | https://github.com/akka/akka | Actor 模型下的定时调度 |

## 十、跨语言对比：定时任务怎么做

| 语言 | 定时能力 | 底层数据结构 | 与 Java 的差异 |
| --- | --- | --- | --- |
| **Java** | `ScheduledThreadPoolExecutor`、Spring `@Scheduled` | 二叉堆（`DelayedWorkQueue`），O(log n) | 语义清晰，海量定时器需换时间轮 |
| **Go** | `time.Ticker` / `time.AfterFunc` / `time.Timer` | 运行时内置**四叉堆**定时器（Go 1.14+ 与 netpoll 集成，P 各自持有 timer heap） | 与 goroutine 天然协作：`select { case <-ticker.C: }`；无需线程池 |
| **Rust (tokio)** | `tokio::time::interval` / `sleep` | tokio 的 **timer wheel**（`tokio::time` 驱动） | 与 async 任务结合，`tick().await`；零成本 |
| **C++** | `boost::asio::deadline_timer` / `steady_timer`；`std::chrono` | asio 用**堆** | 需自己持 io_context 线程；标准库无执行器 |
| **Python** | `threading.Timer`、`asyncio.sleep`、`sched`、APScheduler | `heapq` | GIL 下单线程事件循环；`asyncio` 用堆管理 callbacks |
| **Erlang** | `timer:send_after` / `erlang:send_after` | BEAM 内置 timer wheel | 与进程邮箱天然结合（超时是一条消息） |
| **Linux 内核** | `timerfd`、`hrtimer`、`io_uring timeout` | 红黑树 / timer wheel 混合 | 用户态定时器的最终落点 |

**共同规律**：
1. 语义上都要区分 "fixed rate"（绝对频率，会追赶）与 "fixed delay"（相对结束），Go 的 `Ticker` 与 Java 的 `scheduleAtFixedRate` 语义类似，但 Go 会**丢弃堆积的 tick**（channel 缓冲为 1），因此不会"补跑"——这是行为差异，不可照搬。
2. 数据结构上，堆适合"定时器数量中等、精度要求高"；时间轮适合"数量巨大、精度可放宽"（网络超时、心跳）。

## 十一、误区与纠错

1. ❌ "`scheduleAtFixedRate` 只会在上次跑完后才排下一次" → 错。它是**按理论时间累加**，会追赶补跑；要"跑完再等"必须用 `scheduleWithFixedDelay`。
2. ❌ "定时任务抛异常没关系，下次还会跑" → 错。**周期性任务一旦抛异常就永久终止且静默**（见第四节）。必须 `try/catch`。
3. ❌ "可以随便设 `corePoolSize`" → `ScheduledThreadPoolExecutor` 的队列无界，`maximumPoolSize` 无效；core 设太大只是浪费线程。
4. ❌ "用 `Timer` 就够了" → `Timer` 单线程 + 墙钟 + 异常终止全线程，已在第 11.5 节被本书批评。
5. ❌ "延迟用 `System.currentTimeMillis()` 计算" → 墙钟会跳变；JDK 内部用 `nanoTime()`，业务代码也应如此。
6. ❌ "取消任务用 `cancel(false)` 就能立刻停" → 只对**尚未开始**的任务生效；正在跑的任务需要 `cancel(true)` + 任务内响应中断。

## 十二、本章一页纸总结

- `ScheduledThreadPoolExecutor extends ThreadPoolExecutor`，队列替换为无界堆 `DelayedWorkQueue`，`maxPoolSize` 失效。
- 任务包装为 `ScheduledFutureTask`：三要素 `time`（nanoTime 基准）、`period`（正=固定频率，负=固定延迟，0=一次）、`sequenceNumber`（同级 FIFO）。
- 触发链路：`take()` 阻塞到队首到期 → `run()` → 周期性任务 `runAndReset()` 成功后 `setNextRunTime()` + 重新入堆。
- `fixedRate` 追赶、`fixedDelay` 不追赶；**异常会静默终止周期任务**。
- 海量/低精度定时改用时间轮（Netty、Kafka）；分布式定时用 Quartz / XXL-JOB / PowerJob。

---

> 延伸阅读：[第 8 章 线程池](08-线程池ThreadPoolExecutor原理剖析.md) · [第 11 章 实践篇](11-并发编程实践.md)（11.5 Timer 的坑） · [concepts/阻塞队列BlockingQueue.md](concepts/阻塞队列BlockingQueue.md)
