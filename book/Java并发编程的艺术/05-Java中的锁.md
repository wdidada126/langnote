# 第 5 章 Java中的锁（原书第 2 版 pp.139-196）

> 本书对 AQS 的**源码级剖析**是最大亮点，与《实战》14 章（设计）+ 《之美》`concepts/AQS抽象同步队列.md`（原理）三件套互补。本章含：`Lock` 接口、队列同步器 AQS（CLH 变体、`state`、Node）、`ReentrantLock`、`ReentrantReadWriteLock`、`Condition`、`LockSupport`。

## 一、本章地图

| 主题 | 关键结论 |
| --- | --- |
| `Lock` 接口 | `lock`/`tryLock`/`unlock`/`lockInterruptibly`/`newCondition` |
| AQS（队列同步器） | CLH 变体 FIFO 队列；`state` + `head`/`tail` + `Node.waitStatus` |
| `ReentrantLock` | 公平/非公平（默认非公平）；可重入、可中断、定时 |
| `ReentrantReadWriteLock` | 读写分离；高 16 位读计数 / 低 16 位写持有 |
| `Condition` | 一个 `Lock` 多等待集；`await/signal` 替代 `wait/notify` |
| `LockSupport` | `park/unpark` 底层；不限监视器、可先 unpark |

## 二、核心精讲

### 2.1 AQS 的源码结构（本章精华）
- **同步状态 `state`**：`volatile int`，原子读写（CAS）；不同同步器语义不同（锁=重入次数，信号量=剩余许可，闭锁=剩余倒数）。
- **CLH 变体 FIFO 队列**：每个等待线程封装成 `Node`，通过 `prev/next`/`waitStatus` 连成双向队列（`tail` 入队，`head` 出队）。
- **`waitStatus`**：`CANCELLED(1)` / `SIGNAL(-1)` / `CONDITION(-2)` / `PROPAGATE(-3)` / `0`。
- **acquire 流程**（独占）：`tryAcquire`（子类实现）→ 失败入队 → `acquireQueued` 自旋/ park 抢锁 → 成功则出队。
- **`unparkSuccessor` 从 tail 往前遍历**：因为 `next` 指针在节点入队后异步设置、不可靠，从 `tail` 反向找最前可唤醒节点（详见《之美》AQS 专篇）。
- **共享模式 `PROPAGATE`**：`tryAcquireShared` 返回 `>0` 时唤醒后继并传播（信号量/闭锁用）。

### 2.2 `ReentrantLock`（与《实战》13 章互补）
- 公平锁：`tryAcquire` 先判队列有无前驱 → 有则排队（吞吐低，无饥饿）。
- 非公平锁（默认）：直接 CAS 抢 `state`，抢不到再排队（吞吐高，可能饥饿）。
- 可重入：`state` 累加；释放时递减至 0 才真正释放。

### 2.3 `ReentrantReadWriteLock`
- 把 `state` 的 32 位拆分：高 16 位 = 读持有计数，低 16 位 = 写持有（单线程）。
- 写锁降级：持有写锁时可获取读锁再释放写锁（读可升级？**不可**，写→读可、读→写死锁）。
- 读锁不支持条件变量（无 `newCondition`）。
- 🔧 第 2 版未提 **`StampedLock`**（JDK 8，乐观读）——读多写极少时比读写锁更快，但不可重入、API 复杂（见《之美》锁/StampedLock 讨论）。

### 2.4 `Condition`
- `lock.newCondition()` 返回 `ConditionObject`，内部维护**条件队列**（与 AQS 同步队列不同链表）。
- `await()`：释放锁 → 入条件队列 → park；`signal()`：把条件队列头节点移到同步队列 → 等锁。
- 优势：一个 `Lock` 可建多个 `Condition`（如 `ArrayBlockingQueue` 的 `notEmpty`/`notFull`），`wait/notify` 做不到。

### 2.5 `LockSupport`
- `park()`/`unpark(thread)`：基于 `Unsafe.park`，**不限监视器**，可在任意处挂起/唤醒。
- **先 unpark 再 park 也有效**（不像 `wait/notify` 必须先 wait）——因为 `unpark` 设"许可"标志。
- AQS 内部用 `LockSupport` 做线程挂起/唤醒。

## 三、版本演进

- **JDK 5 (2004)**：`Lock`/`AQS`/`ReentrantLock`/`ReentrantReadWriteLock`/`Condition` 随 J.U.C 引入（Doug Lea）。
- **JDK 8 (2014)**：`StampedLock`（乐观读，非 AQS）。
- **JDK 9+**：AQS 内部 `Unsafe` 字段操作逐步迁 `VarHandle`（JEP 193）。
- **JDK 21+**：AQS 等待不 pin 虚拟线程（对比 `synchronized` 的 pin），虚拟线程时代 AQS 相对 `synchronized` 的优势来源。

## 四、经典论文 / 原始文献

- **Doug Lea, "The java.util.concurrent Synchronizer Framework" (SCIENCE 2004 / Tech Report)**——AQS 权威论文（必读）。
- **Craig, "Building FIFO and Priority-Queuing Spin Locks from CAS" (1993)** / **Magnussen et al., "Queue Locks on Cache Coherent Multiprocessors" (IPPS 1994)**——CLH/MCS 队列锁源头。
- **Hoare, "Monitors" (CACM 1974)**——Condition 语义。
- **JEP 471/498**——`Unsafe` 废弃，AQS 迁 `VarHandle`。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `AQS`/`ReentrantLock`/`ReentrantReadWriteLock`/`Condition`/`LockSupport` 源码 |
| **JCTools/JCTools** | 3.9k | 手写无锁同步器，绕开 AQS（极端吞吐） |
| **LMAX-Exchange/disruptor** | 18.5k | `Sequence`/`SequenceBarrier` 自研同步协议，无 AQS |
| **ben-manes/caffeine** | 17.9k | 读写锁 + 分段 + 无锁混合 |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "AQS 是 `CLH` 锁" | 是 **CLH 变体**（加了 `state`、共享传播、条件队列），非原版 CLH |
| 2 | "读写锁读多一定快" | 写频繁/写饥饿时更慢；考虑 `StampedLock` 🔧 |
| 3 | "读锁可升级写锁" | 会死锁；仅写→读可降级 |
| 4 | "一个对象只能一个等待集" | `Lock`+`Condition` 可多等待集，优于 `wait/notify` |
| 5 | "AQS 万能" | `StampedLock`、无锁队列刻意不用 AQS |
| 6 | "在看源码用 `Unsafe`" | JDK 21+ 废弃；改 `VarHandle` |
