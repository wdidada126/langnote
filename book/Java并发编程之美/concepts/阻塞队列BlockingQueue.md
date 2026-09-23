# 阻塞队列 BlockingQueue

> 定位：`java.util.concurrent.BlockingQueue` 是生产者-消费者模型的标准载体，也是线程池的任务队列。核心特征是**四组 API** 与**有界/无界**之分。
> 对应《Java并发编程之美》第 7 章「并发队列原理剖析」。

## 一、是什么（最小示例）

```java
BlockingQueue<Runnable> queue = new ArrayBlockingQueue<>(1024);  // 有界，背压生效

// 生产者：队列满时阻塞，可被中断
queue.put(() -> handle(request));

// 消费者：队列空时阻塞；InterruptedException 必须显式处理
while (!Thread.currentThread().isInterrupted()) {
    Runnable task = queue.take();
    task.run();
}
```

## 二、实现原理（源码级）

**1）四组 API（同一个语义的四种失败策略）**

| | 抛异常 | 返回特殊值 | 一直阻塞 | 超时退出 |
| --- | --- | --- | --- | --- |
| 插入 | `add(e)` | `offer(e)` → false | `put(e)` | `offer(e, time, unit)` |
| 移除 | `remove()` | `poll()` → null | `take()` | `poll(time, unit)` |
| 检查 | `element()` | `peek()` → null | — | — |

只有**阻塞**与**超时**两组会响应中断（抛 `InterruptedException`）；`put/take` 不允许 null 元素（null 被用作 `poll` 的"空"哨兵值）。

**2）ArrayBlockingQueue**：定长数组构成环形缓冲，一把 `ReentrantLock` 配 `notEmpty` / `notFull` 两个 Condition，`takeIndex`/`putIndex`/`count` 三个游标。入队出队互斥，吞吐受限于单锁。

**3）LinkedBlockingQueue**：**双锁分离**——`putLock` 与 `takeLock` 两把锁，使生产与消费可并行；共享的 `count` 是 `AtomicInteger`，因此在两把锁之间需要跨锁协调（唤醒对方的条件信号要"跨锁 signal"）。默认容量 `Integer.MAX_VALUE`，属**名义上有界、实际上无界**。

**4）SynchronousQueue**：容量为 0，数据**直接移交**，不存储元素。内部是 `Transferer`：`TransferStack`（非公平，LIFO 栈）与 `TransferQueue`（公平，FIFO 队列），用 CAS 配对"取数者"与"存数者"，节点带 `isData` 与 `mode` 字段。`Executors.newCachedThreadPool()` 正是用它。

**5）PriorityBlockingQueue**：无界，用数组二叉堆按 `Comparator` 排序，**不保证同优先级元素的顺序**；单锁保护，但扩容时先用 CAS 抢 `allocationSpinLock` 在**锁外**分配新数组，避免扩容期间阻塞消费者。

**6）DelayQueue**：`PriorityQueue` + leader-follower 模式——leader 线程只等到队首元素到期（定时 `awaitNanos`），其余线程无限等待，减少无谓的定时唤醒；用于缓存过期、超时订单、定时任务。

**7）LinkedTransferQueue**（JDK 7 起）："双重队列"（dual queue），节点带 `isData` 位，同一条链上同时存放"等数据的消费者"和"没被取走的数据"，提供 `transfer(e)`（必须被消费才返回）与 `tryTransfer(e)`。

**8）线程池里为什么不能用无界队列**：
- `Executors.newFixedThreadPool(n)` / `newSingleThreadExecutor()` 内部用的是**无界** `LinkedBlockingQueue`。当生产速度持续高于消费速度，任务无限堆积 → 老年代膨胀 → **OOM**，且异常表现为"堆溢出"而非"拒绝任务"，难以定位。
- 无界队列还会让 `maximumPoolSize` 与拒绝策略**永久失效**（线程数永远不会超过 corePoolSize）。
- 注意 `ThreadPoolExecutor` 的入队顺序与直觉相反：**corePoolSize 满 → 先入队 → 队列满了才创建到 maximumPoolSize → 再满才执行拒绝策略**。所以用无界队列时第二、三步永远走不到。
- 正确做法：显式 `new ThreadPoolExecutor(core, max, keepAlive, TimeUnit, new ArrayBlockingQueue<>(cap), namedFactory, handler)`，并监控队列长度、选择 `AbortPolicy` 或 `CallerRunsPolicy`（自带背压）。

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 8 | 家族齐备：`ArrayBlockingQueue`、`LinkedBlockingQueue`、`LinkedBlockingDeque`、`PriorityBlockingQueue`、`DelayQueue`、`SynchronousQueue`、`LinkedTransferQueue`；内部使用 `sun.misc.Unsafe` 的 CAS |
| JDK 9 | JEP 193（Variable Handles）：内部 volatile/CAS 访问改为 VarHandle |
| JDK 11 | 无公开 API 变化 |
| JDK 17 | 无公开 API 变化 |
| JDK 21 | JEP 444 虚拟线程：`take/put` 底层是 `LockSupport.park`，虚拟线程可被卸载，**不会**钉住 carrier，"每任务一个虚拟线程 + 阻塞队列"重新变得合理；但若自定义队列用 `synchronized` 保护临界区，JDK 21 仍会钉住（JEP 374 已先在 JDK 15 废弃偏向锁，两者无关） |
| JDK 24 | JEP 491（同步虚拟线程而不钉住）：`synchronized` 版队列也不再钉住 |
| JDK 25 | 无新 API；随 JEP 471（JDK 23 弃用）/ JEP 498（JDK 24 告警）推进，Unsafe 内存访问方法继续退役，JUC 内部统一走 VarHandle |

## 四、经典论文

| 论文 | 出处 | 与阻塞队列的关系 |
| --- | --- | --- |
| Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms | Michael & Scott, PODC 1996 | 论文第二种算法即"两锁（head/tail）阻塞队列 + 哨兵节点"，正是 `LinkedBlockingQueue` 双锁分离的理论原型 |
| The java.util.concurrent Synchronizer Framework | Doug Lea, J. ACM 52(3), 2005 | `ReentrantLock` + `Condition`（`notEmpty`/`notFull`）的实现基础 |
| Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors | Mellor-Crummey & Scott, TOCS 9(1), 1991 | 可伸缩同步与队列锁的经典依据 |
| Linearizability: A Correctness Condition for Concurrent Objects | Herlihy & Wing, TOPLAS 12(3), 1990 | 判定 `put/take` 线性化点、以及 `size()`/`remainingCapacity()` 为何只是快照 |
| Safe Memory Reclamation for Dynamic Lock-Free Objects Using Hazard Pointers | Michael, IEEE TPDS 15(6), 2004 | 对照：阻塞队列靠锁与 GC 免于回收问题，无锁队列才需 hazard pointer |
| The Java Memory Model | Manson, Pugh & Adve, POPL 2005 | volatile 字段与锁的 happens-before，保证元素写入对消费者可见 |
| The Art of Multiprocessor Programming | Herlihy & Shavit, 2008 / 2012 | 教材：monitor 与阻塞同步的总述 |

## 五、近年研究与工业界实践

**同行评审论文**
- Understanding Real-World Concurrency Bugs in Go（Tu 等，ASPLOS 2019）：对真实 bug 的统计显示，消息传递（channel）同样普遍存在阻塞/泄漏类缺陷，说明"换模型"不等于"免死锁"，边界与超时设计才是关键。
- RefinedRust（Gäher 等，2024）：并发数据结构的自动验证，涵盖有界队列的容量不变式。
- NVTraverse（Friedman 等，PPoPP 2021）：非易失内存上的遍历优化，对持久化队列有参考价值。

**工业界资料**
- OpenJDK：`src/java.base/share/classes/java/util/concurrent/ArrayBlockingQueue.java` 等 — https://github.com/openjdk/jdk
- JCTools — https://github.com/JCTools/JCTools ：`SpscArrayQueue`/`MpscArrayQueue`/`MpmcArrayQueue`，单生产者/多生产者变体，缓存行填充 + 免锁路径
- LMAX Disruptor — https://github.com/LMAX-Exchange/disruptor ：环形缓冲 + 序号屏障，消除队列的节点分配与锁开销
- Netty — https://github.com/netty/netty ：EventLoop 的任务队列采用多生产者单消费者（MPSC）队列，避免多生产者锁竞争
- Chronicle-Queue — https://github.com/OpenHFT/Chronicle-Queue ：mmap 持久化 append-only 队列，面向超低延迟与堆外存储
- JMH — https://github.com/openjdk/jmh ；jcstress — https://github.com/openjdk/jcstress ：分别用于吞吐基准与内存模型一致性测试

## 六、常见误区 + 跨语言对照

**常见误区**
1. "`LinkedBlockingQueue` 是无界队列"——严格说默认容量是 `Integer.MAX_VALUE`，是有界但等于无界。
2. "用 `size()` 做流控"——它只是快照；有界背压应靠 `put()` 阻塞或 `offer()` 返回值 + `remainingCapacity()`。
3. "`offer` 总能成功"——有界队列满时返回 false，忽略返回值会静默丢任务。
4. "捕获 `InterruptedException` 后吞掉"——必须恢复中断标记或向上抛出，否则关闭流程会卡死。
5. "用 `Executors` 工厂方法就够了"——见第二节第 8 点，无界队列带来 OOM 且使拒绝策略失效。
6. "`drainTo` 只是语法糖"——它一次持锁批量摘取，能显著减少锁获取次数，但会改变公平性并可能一次拿光。
7. "`SynchronousQueue` 是个容量为 1 的队列"——容量为 0，必须配对移交，没有缓冲。
8. "用 `PriorityBlockingQueue` 做定时任务"——同优先级无序、无延迟语义；定时请用 `DelayQueue` 或 `ScheduledThreadPoolExecutor`。

**跨语言对照**

| 语言 | 对应设施 | 关键差异 |
| --- | --- | --- |
| Java | `BlockingQueue` 家族（有界/无界/优先/延迟/直接移交） | 四组 API 统一封装；阻塞可中断、可超时 |
| C++ | 标准库无并发队列；常用 `boost::lockfree::queue`、Folly 的 `MPMCQueue`、或 `std::deque` + `mutex` + `condition_variable` | 需手写条件变量谓词（含虚假唤醒处理）；无统一四组 API |
| Rust | `std::sync::mpsc`（含 `SyncSender` 有界变体）；`crossbeam-channel`（有界/无界 MPMC） | 类型系统区分 Sender/Receiver；有界即"零容量/固定容量"由构造函数指定 |
| Go | `channel`：`make(chan T, n)` 即带缓冲的有界队列，满则阻塞；无界需自行组合 | 语言原语，配合 `select` 与 `context` 实现超时/取消 |
| Erlang | 进程邮箱（默认无界，需自行做背压，如 `gen_statem` 限流） | 无内建有界队列原语，消息传递语义优先 |
| Python | `queue.Queue(maxsize)`（有界阻塞）、`asyncio.Queue`、`multiprocessing.Queue` | `deque` 自身非阻塞且需加锁；`Queue.join()`/`task_done()` 提供任务追踪 |
