# 专篇：BlockingQueue 全家桶 —— 7 种实现，7 个不同的取舍

> 对应本书第 7 章《并发队列原理剖析》。本书讲了 `ConcurrentLinkedQueue`、
> `LinkedBlockingQueue`、`ArrayBlockingQueue`、`PriorityBlockingQueue`、`DelayQueue`
> 的**部分**源码，但**没有给出一张横向选型表**，也没覆盖
> **`SynchronousQueue` 与 `LinkedTransferQueue`**——这两个恰恰是实践中
> 决定"线程池行为"的关键（尤其是 `newCachedThreadPool`）。
> 本篇补上选型矩阵 + JDK 8 之后的变化。

## 一、本章地图

```
BlockingQueue 的四组 API（抛异常 / 返回特殊值 / 阻塞 / 超时）
        ↓
7 种实现的横向对比表（锁策略、有界性、结构、吞吐特性）
        ↓
逐一点评：ABQ / LBQ / LBD / PBQ / DelayQueue / SynchronousQueue / LinkedTransferQueue
        ↓
生产事故 TOP：LinkedBlockingQueue 默认容量 = Integer.MAX_VALUE
        ↓
与线程池的耦合：cachedThreadPool ↔ SynchronousQueue
        ↓
虚拟线程时代的重新评估
```

## 二、`BlockingQueue` 的四组 API

| 操作 | 抛异常 | 返回特殊值 | 阻塞 | 超时 |
| --- | --- | --- | --- | --- |
| 插入 | `add(e)` | `offer(e)` → `false` | `put(e)` | `offer(e, t, u)` |
| 移除 | `remove()` | `poll()` → `null` | `take()` | `poll(t, u)` |
| 检查 | `element()` | `peek()` → `null` | — | — |

> **硬性约束**：`BlockingQueue` **不接受 `null` 元素**（`null` 被 `poll()` 用作"队列空"的哨兵值）。
> 插入 `null` 会直接 `NullPointerException`。这是与 `LinkedList` 的重要差别。

## 三、七种实现横向对比

| 实现 | 锁策略 | 有界 | 内部结构 | 特点 / 适用 |
| --- | --- | --- | --- | --- |
| **ArrayBlockingQueue** | **1 把** `ReentrantLock` + `notEmpty`/`notFull` | ✅ 强制有界 | 定长数组环形 | 内存预分配、无 GC 压力；**单锁导致生产/消费互斥** |
| **LinkedBlockingQueue** | **2 把**锁（`putLock`/`takeLock`） | ⚠️ 默认 `Integer.MAX_VALUE` | 单链表 | **生产和消费可并行**，吞吐更高；默认无界是陷阱 |
| **LinkedBlockingDeque** | 1 把锁 + 2 条件 | ⚠️ 默认无界 | 双向链表 | 支持双端操作；**工作窃取（work-stealing）场景会用** |
| **PriorityBlockingQueue** | 1 把锁 + **仅 `notEmpty`** | ❌ 无界（自动扩容） | 数组二叉堆 | 按优先级出队；**不保证同优先级顺序**；无 `notFull` 因为不会满 |
| **DelayQueue** | 1 把锁 + leader-follower | ❌ 无界 | 内部 `PriorityQueue` | 元素只有到期才能 `take()`；见本书第 9 章 ScheduledThreadPoolExecutor |
| **SynchronousQueue** | **无锁（CAS）**，双栈/双队列 | 容量恒为 **0** | 无 | **直接交付（direct handoff）**；`newCachedThreadPool` 的底座 |
| **LinkedTransferQueue** | **无锁（CAS）**，dual data structure | ❌ 无界 | 单链表（含 data/reservation 两类节点） | `tryTransfer()` / `hasWaitingConsumer()`；Doug Lea 称其为"通用首选" |

## 四、逐一点评（含源码级要点）

### 4.1 `ArrayBlockingQueue` —— 单锁环形数组

```java
final ReentrantLock lock;              // 只有一把
private final Condition notEmpty, notFull;
final Object[] items;
int takeIndex, putIndex, count;        // 非 volatile！靠锁保护
```

| 要点 | 说明 |
| --- | --- |
| 公平性可选 | `new ArrayBlockingQueue(cap, fair)` —— 公平锁显著降低吞吐，一般不开 |
| 字段无需 `volatile` | 所有访问都在锁内，靠 `ReentrantLock` 的 happens-before 保证可见性（见《JMM与happens-before》） |
| **`count` 是 int** | 锁保护下安全，不需要原子类——这是"锁能简化可见性"的典型例子 |
| 迭代 | `WeaklyConsistent` 迭代器 | 
| 局限 | 生产与消费**互相阻塞**（同一把锁），高吞吐场景不如 LBQ |

### 4.2 `LinkedBlockingQueue` —— 双锁队列

```java
private final ReentrantLock putLock  = new ReentrantLock();
private final ReentrantLock takeLock = new ReentrantLock();
private final AtomicInteger count;    // ← 两把锁都要改，故用原子类
```

**为什么 `count` 必须是 `AtomicInteger`？**
因为它被**两把不同的锁**保护，`putLock` 和 `takeLock` 之间没有 happens-before 关系，
普通 `int` 会有可见性问题 → 用 `AtomicInteger`（volatile + CAS）。

| 要点 | 说明 |
| --- | --- |
| 双锁带来的性能 | **生产者和消费者可以真正并行**（各自持一把锁），吞吐显著高于 ABQ |
| 算法出处 | 即 Michael & Scott 论文里的 **"two-lock queue"** 算法（见第八节） |
| ⚠️ **默认容量 `Integer.MAX_VALUE`** | `new LinkedBlockingQueue()` 是**事实无界**的。消费者挂了 → 生产者一路堆积 → **OOM**。这是最高频的生产事故之一 |
| 内存开销 | 每个元素一个 `Node` 对象（多一层指针 + GC 压力） |

> **工程建议**：用 `LinkedBlockingQueue` 时**必须**显式指定容量。
> 很多团队的静态扫描规则直接禁用无参构造。

### 4.3 `SynchronousQueue` —— 容量为 0 的"直接交付"

```
生产者 put(e) → 没有消费者在等？→ 阻塞（或 offer 失败）
消费者 take() → 没有生产者在等？→ 阻塞
有配对者 → 元素直接从生产者线程"递"到消费者线程，不落任何存储
```

- 内部两种模式：**非公平 = 双栈（LIFO）**、**公平 = 双队列（FIFO）**；
- 节点用 `SNode`/`QNode`（JDK 8+ 统一为 `Transferer` 抽象的两个实现）；
- 全程 **CAS + `LockSupport.park/unpark`**，无 `ReentrantLock`；
- **`Executors.newCachedThreadPool()` 用的就是它**：核心池 0、最大池 `Integer.MAX_VALUE`、
  队列容量为 0 → 每个新任务若无空闲线程就**新建线程**。

> **这解释了 `cachedThreadPool` 为什么危险**：它不是一个"池"，而是一个
> "来一个任务开一个线程"的机制（空闲 60s 才回收）。高并发下会瞬间创建大量 OS 线程 → OOM。
> **JDK 21 起，用 `Executors.newVirtualThreadPerTaskExecutor()` 替代它。**

### 4.4 `LinkedTransferQueue` —— 被低估的通用首选

```java
queue.tryTransfer(e);              // 有等待的消费者就立刻交付，否则返回 false（不等待）
if (queue.hasWaitingConsumer()) { ... }   // 探测是否有消费者在等（用于自适应批处理）
```

- 是 `SynchronousQueue` 的**超集**：既能像普通无界队列一样存，又能做直接交付；
- 基于 **dual data structure**（节点分两类：携带数据的 `DATA` 节点、表示等待的 `REQUEST` 节点，互相"配对抵消"）；
- Doug Lea 在 Javadoc 中称其"通常比 `SynchronousQueue` 和 `LinkedBlockingQueue` 更快"；
- JDK 内部使用：`Executors` 之外，很多框架（如早期 Akka、部分 RPC 框架）选它做默认队列。

### 4.5 `PriorityBlockingQueue` 与 `DelayQueue`

| 要点 | 说明 |
| --- | --- |
| 无界 | 永远不会阻塞生产者，只有 `notEmpty` 一个条件 |
| 扩容 | 数组二叉堆 + `tryGrow()`（扩容时**先释放锁**再 `Arrays.copyOf`，避免持锁做内存拷贝——这是个精妙设计） |
| 不保序 | 同优先级的出队顺序不确定；需要稳定顺序要自己加序号 |
| `DelayQueue` | 内部就是 `PriorityQueue` + `leader-follower` 等待，与本书第 9 章的 `DelayedWorkQueue` 同构 |
| `DelayQueue` 的 leader | 只允许一个线程 `awaitNanos(delay)`，其余无限等待 → 避免"惊群"（thundering herd） |

## 五、与线程池的耦合关系（本书第 8 章的补充）

| 线程池 | 用的队列 | 后果 |
| --- | --- | --- |
| `newFixedThreadPool(n)` | **`LinkedBlockingQueue`（无界！）** | 队列永远不拒绝 → `maximumPoolSize` 形同虚设（见本书第 8 章 08 篇笔记） |
| `newCachedThreadPool()` | `SynchronousQueue` | 无队列缓冲 → 任务直接变线程 |
| `newSingleThreadExecutor()` | `LinkedBlockingQueue`（无界） | 同上 |
| 你自己 `new ThreadPoolExecutor(...)` | **应该用 `ArrayBlockingQueue` 显式设界** | 才能真正触发拒绝策略 |

> **核心结论**：`Executors` 工厂方法几乎都有"无界队列"隐患，
> **生产环境必须自己 `new ThreadPoolExecutor`，并显式指定有界队列 + 拒绝策略 + 线程工厂。**

## 六、JDK 8 → 21 的变化

| 版本 | 变化 |
| --- | --- |
| JDK 8 | 现有实现基本定型；`LinkedTransferQueue` 已存在 |
| JDK 9 | 部分内部实现改用 **VarHandle** |
| JDK 21 | **虚拟线程**：JUC 的阻塞队列都用 `ReentrantLock`/`LockSupport`，**不会 pin 载体线程**（与 `synchronized` 不同）→ **队列 + 虚拟线程是安全的组合** |
| JDK 21 | `Executors.newVirtualThreadPerTaskExecutor()` 取代 `newCachedThreadPool()` 的多数用途 |
| JDK 24 | JEP 491 让 `synchronized` 也不再 pin（但队列本来就无此问题） |

> **重要区分**：如果你的代码用 **`synchronized` + `Object.wait()`** 手写阻塞队列，
> 在 JDK 21-23 上跑虚拟线程会 **pin**（钉住）载体线程；
> 换成 JUC 的 `BlockingQueue`（基于 AQS/`LockSupport`）则完全没问题。

## 七、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Michael, M. M. & Scott, M. L. 1996. "Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms." PODC '96, pp. 267-275.** | **一篇论文同时给出**：① 无锁 MS-queue；② **两把锁的阻塞队列**。后者正是 `LinkedBlockingQueue` 的算法（见《Michael-Scott无锁队列》篇） |
| **Scherer, W. N. III, Lea, D., Scott, M. L. 2006. "Scalable Synchronous Queues." PPoPP '06.** | **`SynchronousQueue` 与 `LinkedTransferQueue` 的算法论文**（Doug Lea 本人是作者之一）。提出 dual stack / dual queue，用 CAS 完成"配对交付" |
| **Scherer, W. N. III & Scott, M. L. 2004. "Nonblocking Concurrent Objects with Condition Synchronization." DISC '04.** | 上述算法的理论基础：如何在无锁结构里表达"条件同步"（等待某个条件成立） |
| **Herlihy, M. P. & Wing, J. M. 1990. "Linearizability: A Correctness Condition for Concurrent Objects." ACM TOPLAS 12(3).** | 并发容器的**正确性标准**；JUC 所有容器都追求可线性化 |
| **Herlihy, M. & Shavit, N.《The Art of Multiprocessor Programming》第 10 章（Queues）** | 从锁队列到 MS-queue 到 dual queue 的系统讲解 |
| **Thompson, M., Farley, D., et al. "Disruptor: High performance alternative to bounded queues"（LMAX, 2011）** | 工业界对"队列"的反思：队列在**多生产者多消费者**场景下是争用热点 → 用环形缓冲 + 序号取代 |

## 八、近年研究与工业界前沿

### 近年研究

- **批处理友好的队列**：近年来研究聚焦"如何让消费者一次取一批"（降低 CAS 争用），例如 *batch queue*、*flat combining* 思路；`LinkedTransferQueue` 的 `tryTransfer` 是工业界的对应手段。
- **持久内存（PMem）队列**：面向非易失内存的崩溃一致性队列设计（日志即队列）。
- **NUMA 感知队列**：多插槽机器上"跨节点"传递代价高，研究偏向分区队列 + 绑核。
- **内存回收**：无锁队列在非 GC 语言中的安全回收（hazard pointer / epoch / interval-based），见《Michael-Scott无锁队列》篇。

### 工业界开源实现（2026-09 核验）

| 项目 | Stars | 说明 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `ArrayBlockingQueue.java`、`LinkedBlockingQueue.java`、`SynchronousQueue.java`、`LinkedTransferQueue.java`、`PriorityBlockingQueue.java`、`DelayQueue.java` |
| **JCTools/JCTools** | 3.9k | **Netty 等框架的队列底座**；提供 SPSC/MPSC/SPMC/MPMC 四类专用队列（比通用队列快数倍）；`MpscUnboundedArrayQueue` 是 Netty 默认的任务队列 |
| **LMAX-Exchange/disruptor** | 18.5k | 环形缓冲 + 序号 + 缓存行填充；**"队列不是最优解"**这一派的代表作 |
| **facebook/folly** | 30.5k | `folly::MPMCQueue`（Dmitry Vyukov 有界 MPMC 队列的 C++ 实现）、`folly::UMPSCQueue` |
| **netty/netty** | 35.1k | 大量使用 JCTools 的 MPSC 队列做 EventLoop 任务队列 |
| **crossbeam-rs/crossbeam** | 8.6k | Rust 的 `SegQueue`、`ArrayQueue`；配套 epoch-based 内存回收 |
| Go `channel` | — | CSP 通道：无缓冲 = SynchronousQueue 语义，有缓冲 = 环形数组；GMP 调度器与 `gopark/goready` 完成配对 |

## 九、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "`LinkedBlockingQueue` 有默认容量" | 默认 **`Integer.MAX_VALUE`**，事实无界 → **必须显式指定容量** |
| 2 | "`ArrayBlockingQueue` 和 `LinkedBlockingQueue` 性能差不多" | LBQ **双锁**（生产/消费可并行），高吞吐下明显更优；ABQ 胜在内存可控、无 per-node 开销 |
| 3 | "队列可以放 `null`" | **不可以**，`null` 是 `poll()` 的"空"哨兵，插入会 NPE |
| 4 | "`put()` 一定成功" | 有界队列满了会**阻塞**；用 `offer(timeout)` 更好 |
| 5 | "`PriorityBlockingQueue` 会按插入顺序处理同优先级" | **不会**，同优先级顺序不确定；需要稳定顺序要自己加 `seq` |
| 6 | "`DelayQueue` 的到期时间会被自动更新" | 元素入队后**不应再修改** `getDelay()`；改了也不会重新排序 |
| 7 | "`SynchronousQueue` 是"同步"的所以慢" | 它的"同步"指**直接交付**；CAS 实现，延迟极低（是 `cachedThreadPool` 的 0 延迟来源） |
| 8 | "`size()` 精确" | 并发下是瞬时值；不要用 `size() > 0` 再 `take()`（竞态），直接 `poll()` |
| 9 | "`Executors` 工厂方法够用" | 它们几乎都用**无界队列**，`maximumPoolSize` 永不生效；生产必须自建 `ThreadPoolExecutor` |
| 10 | "虚拟线程 + 阻塞队列会 pin" | **不会**。JUC 队列基于 `ReentrantLock`/`LockSupport`，不 pin；只有 `synchronized` + `Object.wait()` 在 JDK 21-23 会 pin（JDK 24 修复） |

> **本书补充定位**：本书第 7 章逐个讲了源码，但缺一张**选型矩阵**与"SynchronousQueue /
> LinkedTransferQueue"这一块。本篇补齐，并把队列与线程池、虚拟线程的耦合讲清。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

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
