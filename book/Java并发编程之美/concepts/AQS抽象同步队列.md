# 专篇：AQS 抽象同步队列（AbstractQueuedSynchronizer）

> 对应本书 6.2 / 6.3 / 6.4 节。**AQS 是整个 `java.util.concurrent` 的地基**——
> `ReentrantLock`、`ReentrantReadWriteLock`、`StampedLock`、`Semaphore`、`CountDownLatch`、
> `FutureTask`、`ThreadPoolExecutor.Worker`，乃至 JDK 7 的 `Phaser`，全部建在它之上。
> 理解 AQS 一个，等于理解 JUC 一大半。

## 一、一句话概括

AQS 把「同步」抽象成两件事：

1. 一个 **`volatile int state`**（同步状态），具体语义由子类定义
2. 一个 **FIFO 双向等待队列**（CLH 队列的变体），存放获取失败的线程

子类只需实现 **`tryAcquire/tryRelease`（独占）或 `tryAcquireShared/tryReleaseShared`（共享）**，
「排队、阻塞、唤醒、取消、超时、中断」这些脏活全由 AQS 基类做完。

> 这就是**模板方法模式**在并发领域的经典应用：基类管流程，子类管语义。

## 二、三大件

```java
public abstract class AbstractQueuedSynchronizer {
    private volatile int state;                    // ① 同步状态
    private transient volatile Node head;          // ② 队列头（哑节点）
    private transient volatile Node tail;          // ③ 队列尾
    // 通过 Unsafe（JDK 8）/ VarHandle（JDK 9+）做 CAS 与阻塞原语
}
```

### ① `state`：语义完全由子类定

| 同步器 | `state` 的含义 |
| --- | --- |
| `ReentrantLock` | 重入次数（0=未锁，n=重入 n 次） |
| `ReentrantReadWriteLock` | 高 16 位=读锁计数，低 16 位=写锁重入次数 |
| `Semaphore` | 剩余许可数 |
| `CountDownLatch` | 剩余计数值 |
| `FutureTask` | 任务状态（NEW/COMPLETING/NORMAL/EXCEPTIONAL/CANCELLED/INTERRUPTING/INTERRUPTED） |
| `ThreadPoolExecutor.Worker` | 0=空闲，1=忙碌，-1=初始化中（且**不可重入**，见 08 章） |

### ②③ 队列：CLH 队列的变体

```
        head                                    tail
          ↓                                       ↓
     [哑节点] ⇄ [Node(T2)] ⇄ [Node(T3)] ⇄ [Node(T4)]
       (已获取)    waitStatus       waitStatus
```

`Node` 的关键字段：

```java
static final class Node {
    volatile int waitStatus;          // 见下表
    volatile Node prev;
    volatile Node next;
    volatile Thread thread;           // 该节点代表的线程
    Node nextWaiter;                  // 条件队列用；也用来标记 SHARED/EXCLUSIVE
}
```

`waitStatus` 取值：

| 值 | 含义 |
| --- | --- |
| `0` | 初始/默认 |
| `SIGNAL (-1)` | **后继节点需要被唤醒**——本节点释放时必须 unpark 后继 |
| `CANCELLED (1)` | 该节点已取消（超时或中断），将被跳过并从队列移除 |
| `CONDITION (-2)` | 节点在**条件队列**里（`Condition.await()`） |
| `PROPAGATE (-3)` | 共享模式下，唤醒需要**向后传播** |

## 三、独占模式的获取流程

```java
public final void acquire(int arg) {
    if (!tryAcquire(arg) &&                                  // ① 先抢一次（子类实现）
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))       // ② 失败则入队并阻塞
        selfInterrupt();                                     // ③ 补上被吞掉的中断
}

private Node addWaiter(Node mode) {
    Node node = new Node(currentThread(), mode);
    Node pred = tail;
    if (pred != null) {
        node.prev = pred;
        if (compareAndSetTail(pred, node)) { pred.next = node; return node; }  // 快速入队
    }
    enq(node);                                               // CAS 失败则自旋入队
    return node;
}

final boolean acquireQueued(final Node node, int arg) {
    boolean failed = true;
    try {
        boolean interrupted = false;
        for (;;) {
            final Node p = node.predecessor();
            if (p == head && tryAcquire(arg)) {              // 前驱是头 → 再试一次
                setHead(node);
                p.next = null;                               // 帮助 GC
                failed = false;
                return interrupted;
            }
            // 判断是否需要 park：把前驱的 waitStatus 置为 SIGNAL
            if (shouldParkAfterFailedAcquire(p, node) &&
                parkAndCheckInterrupt())                     // LockSupport.park(this)
                interrupted = true;                          // ⚠️ 只记标志，不抛异常
        }
    } finally {
        if (failed) cancelAcquire(node);
    }
}
```

**四个容易被忽略的设计细节**：

1. **入队后还会再 `tryAcquire` 一次**（`p == head` 时）——因为前驱可能刚好释放了，避免无谓的 park/unpark。
2. **`park()` 返回后要检查中断，但不立即响应**——只设 `interrupted = true`，等真正获取到锁后才 `selfInterrupt()` 补上。
   这就是 **`ReentrantLock.lock()` 不可中断**的原因（要 `lockInterruptibly()` 才响应）。
3. **`shouldParkAfterFailedAcquire` 会跳过 `CANCELLED` 节点**，并把前驱 `waitStatus` 改成 `SIGNAL`——
   保证「我释放时一定有人唤醒我」这个契约。
4. **公平性只差一行**：`FairSync.tryAcquire` 多了 `!hasQueuedPredecessors()` 判断。
   **AQS 本身不保证公平，公平与否完全由子类的 `tryAcquire` 决定。**

## 四、释放流程与「为什么不直接唤醒 head.next」

```java
public final boolean release(int arg) {
    if (tryRelease(arg)) {                    // 子类：state 归零（重入锁要考虑重入次数）
        Node h = head;
        if (h != null && h.waitStatus != 0)
            unparkSuccessor(h);               // 唤醒后继
        return true;
    }
    return false;
}

private void unparkSuccessor(Node node) {
    int ws = node.waitStatus;
    if (ws < 0) compareAndSetWaitStatus(node, ws, 0);
    Node s = node.next;
    // ⚠️ 关键：从 tail 往前找，而不是直接用 next
    if (s == null || s.waitStatus > 0) {
        s = null;
        for (Node t = tail; t != null && t != node; t = t.prev)
            if (t.waitStatus <= 0) s = t;
    }
    if (s != null) LockSupport.unpark(s.thread);
}
```

**为什么要从 tail 反向遍历找后继，而不是直接用 `head.next`？**

因为 **`next` 指针是不可靠的**——`addWaiter` 里 `CAS(tail)` 成功后才执行 `pred.next = node`，
这中间有个窗口：`next` 还是 `null`，且**新节点入队时也可能因并发导致 `next` 链暂时断裂**。
而 `prev` 是在 CAS 之前就设置好的，**反向遍历一定能走到所有已入队节点**。

> 这是 AQS 里最精妙也最容易被讲解者跳过的一处工程细节。

## 五、共享模式与传播（propagation）

```java
public final void acquireShared(int arg) {
    if (tryAcquireShared(arg) < 0)
        doAcquireShared(arg);
}

private void doAcquireShared(int arg) {
    final Node node = addWaiter(Node.SHARED);
    for (;;) {
        final Node p = node.predecessor();
        if (p == head) {
            int r = tryAcquireShared(arg);
            if (r >= 0) {
                setHeadAndPropagate(node, r);   // ⭐ 传播：可能继续唤醒下一个
                p.next = null;
                return;
            }
        }
        if (shouldParkAfterFailedAcquire(p, node) && parkAndCheckInterrupt())
            interrupted = true;
    }
}
```

`tryAcquireShared` 返回值的语义：

| 返回值 | 含义 |
| --- | --- |
| `< 0` | 失败，入队等待 |
| `= 0` | 成功，但**不传播**给后续共享节点 |
| `> 0` | 成功，且**继续传播**（还有余量，唤醒下一个） |

这就是为什么 `CountDownLatch` 归零后返回 `1`（而非 `0`）——
它要触发传播，让 AQS 一次性唤醒**所有**等待线程（见 [10 章](../10-线程同步器.md)）。

## 六、条件变量：一个 AQS 两套队列

```java
public class ConditionObject implements Condition {
    private transient Node firstWaiter;      // 条件队列头
    private transient Node lastWaiter;
}
```

**关键点：`Condition` 用的是另一条单向链表（条件队列），与 AQS 的同步队列是两套**：

```
await()  =  释放锁（完全释放，重入也要全放） → 加入条件队列 → park
signal() =  把条件队列的头节点「转移」到同步队列 → 等它重新抢到锁才继续
```

```java
public final void await() throws InterruptedException {
    if (Thread.interrupted()) throw new InterruptedException();
    Node node = addConditionWaiter();
    int savedState = fullyRelease(node);       // ⭐ 完全释放（考虑重入）
    ...
    while (!isOnSyncQueue(node)) {
        LockSupport.park(this);
        if ((interruptMode = checkInterruptWhileWaiting(node)) != 0) break;
    }
    if (acquireQueued(node, savedState) && interruptMode != THROW_IE)  // 重新抢回锁
        interruptMode = REINTERRUPT;
    ...
}
```

> ⚠️ `await()` 会**完全释放**锁（包括重入次数），并在唤醒后**恢复原重入次数**——
> 这一点与 `Object.wait()` 一致，但很多人误以为只释放一次。

## 七、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 5 | AQS 引入（Doug Lea, JSR 166） |
| JDK 6 | 性能优化、取消节点的清理改进 |
| JDK 7 | `Phaser`、`LinkedTransferQueue`（内部自建类似结构） |
| JDK 8 | `StampedLock`——**刻意不继承 AQS**（自己实现 CLH + 读锁"戳"机制，避免 AQS 的写饥饿） |
| JDK 9 | 内部 `sun.misc.Unsafe` → `VarHandle`（`compareAndSetState` 等改为 VarHandle） |
| JDK 17 | JEP 403 强封装内部 API，反射访问 AQS 内部字段开始受限 |
| JDK 23/24 | `Unsafe` 内存访问方法标记废弃（JEP 471/498），AQS 已全面改用 VarHandle |

## 八、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| **CLH 锁** | **Craig, *Building FIFO and priority-queuing spin locks from smaller atomic primitives*** | 1993（技术报告，未正式发表但被广泛引用）—— AQS 队列的原型 |
| CLH 锁的系统性分析 | **Magnussen, Landin, Hagersten, *Queue locks on cache coherent multiprocessors*** | **IPPS/SPDP 1994** —— MCS 锁的出处，与 CLH 并列为两大队列锁 |
| **AQS 本身的论文** | **无**——AQS 是 Doug Lea 的工程实现，未单独发论文 | 权威文档是 `AbstractQueuedSynchronizer` 类的**源码注释**（约 300 行，写得极好，必读） |
| JSR 166 | Lea, *The java.util.concurrent Synchronizer Framework* | Sun/Oracle 技术资料；另见 Lea 的 *Concurrent Programming in Java* (2nd ed., 2000) |
| 无阻塞同步理论 | Herlihy, *Wait-Free Synchronization* | TOPLAS 13(1), 1991 |
| 线性一致性 | Herlihy & Wing, *Linearizability* | TOPLAS 12(3), 1990 |

> 📌 **AQS 最权威的"论文"就是它的源码注释**。Doug Lea 在类注释里写清了独占/共享两套模式、
> 为什么需要 `PROPAGATE`、以及条件队列与同步队列的关系。**读 AQS 前先读那段注释**。

## 九、近年研究与工业界前沿（2020-2026）

**同行评审论文**

- **队列锁的 NUMA 感知变体（2020-2025）**：CLH/MCS 在 NUMA 机器上跨节点传递 cacheline 代价很高，
  近年 PPoPP / SC 上持续有 NUMA-aware 的层次化队列锁研究。JDK 的 AQS 并未采纳（通用性优先）。
- **形式化验证 AQS 类结构**：有用 Iris（Coq）/ TLA+ 对 AQS 做模型检测的工作，验证其无死锁与线性一致性。
  这类工作属于"补上当年缺失的证明"。

**工业界资料（非同行评审）**

- **`StampedLock` 是 AQS 的重要反例**：Doug Lea 自己后来写的 `StampedLock` **故意不用 AQS**，
  因为它需要「读锁不排队、写锁不饥饿」的语义，AQS 的 FIFO 排队会饿死写线程。
  → **AQS 不是万能的，需要非 FIFO 语义时得自己写。**
- **`StampedLock` 的三个致命坑**（工业界血泪）：
  1. **不可重入**，且 `tryOptimisticRead()` 后必须 `validate()`
  2. `readLock()` 获取的锁**不是可中断的**，且**不支持 `Condition`**
  3. **不支持公平模式**（构造参数的 fair 只对写锁部分生效）
  → 实践中**能用 `ReentrantReadWriteLock` 就用它**，`StampedLock` 只在读极多写极少且已实测收益时才上。
- **Netty / Disruptor 的自旋策略**：在极低延迟场景下用 `busy-spin + Thread.onSpinWait()`（JDK 9+）替代 `park/unpark`，
  是 AQS 之外的另一条路（AQS 的 park/unpark 有约 1-10μs 的内核切换成本）。
- **JOL（Java Object Layout）**：分析 `Node` 对象布局与伪共享必用。https://github.com/openjdk/jol

## 十、常见误区

1. **❌「AQS 就是 CLH 队列」** —— 是**变体**：原版 CLH 是自旋 + 隐式前驱链表，AQS 改为 `park/unpark` 阻塞 + **显式双向链表**（需要 `prev` 来做取消与反向遍历）。
2. **❌「公平锁性能一定差」** —— 公平锁吞吐确实低一个数量级，但它**消除线程饥饿**。只有在有大量短临界区且能接受饥饿时才用非公平。
3. **⚠️ `park()` 会吞掉中断**：`acquireQueued` 只记标志，最后才 `selfInterrupt()` 补上——所以 `lock()` 不可中断。
4. **⚠️ `unparkSuccessor` 从 tail 反向遍历**，不是用 `head.next`（原因见第四节）。
5. **⚠️ `Condition.await()` 完全释放锁**（含重入次数），唤醒后恢复——与 `Object.wait()` 一致。
6. **⚠️ `StampedLock` 不是 AQS 的子类**，别按 AQS 的心智模型去用它。
7. **❌「`state` 就是锁计数」** —— 语义完全由子类定（见第一节表格）。
