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
