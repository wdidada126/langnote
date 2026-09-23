# AQS 抽象同步队列

> 定位：`java.util.concurrent.locks.AbstractQueuedSynchronizer`（下称 AQS）是 JUC 的同步器底座。ReentrantLock、ReentrantReadWriteLock、Semaphore、CountDownLatch、FutureTask、ThreadPoolExecutor.Worker 全部建立在它之上。
> 对应《Java并发编程之美》第 6 章「锁原理剖析」；权威设计说明是 Doug Lea 的 JACM 2005 论文。

## 一、是什么（最小示例）

一个不可重入互斥锁就是 AQS 的全部用法：子类只重写 `tryAcquire/tryRelease`，排队、阻塞、唤醒、取消全在父类里。

```java
final class Mutex implements Lock {
    private static final class Sync extends AbstractQueuedSynchronizer {
        protected boolean isHeldExclusively() { return getState() == 1; }
        protected boolean tryAcquire(int acquires) {           // state: 0 空闲, 1 占用
            if (compareAndSetState(0, 1)) {
                setExclusiveOwnerThread(Thread.currentThread());
                return true;
            }
            return false;
        }
        protected boolean tryRelease(int releases) {
            if (getState() == 0) throw new IllegalMonitorStateException();
            setExclusiveOwnerThread(null);
            setState(0);                                       // 释放无需 CAS：此刻独占
            return true;
        }
        final ConditionObject newCondition() { return new ConditionObject(); }
    }
    private final Sync sync = new Sync();
    public void lock()                { sync.acquire(1); }
    public void lockInterruptibly() throws InterruptedException { sync.acquireInterruptibly(1); }
    public boolean tryLock()          { return sync.tryAcquire(1); }
    public boolean tryLock(long t, TimeUnit u) throws InterruptedException {
        return sync.tryAcquireNanos(1, u.toNanos(t));
    }
    public void unlock()              { sync.release(1); }
    public Condition newCondition()   { return sync.newCondition(); }
}
```

## 二、实现原理（源码级）

**1）state：一个 `volatile int`，语义完全交给子类。** 模板方法只提供 `getState/setState/compareAndSetState`。ReentrantLock 用它记重入次数，Semaphore 记剩余许可，CountDownLatch 记未完成的计数值，ReentrantReadWriteLock 把 32 位劈成高 16（读计数）+ 低 16（写计数）。

**2）等待队列：CLH 的变体，不是原版 CLH。** 原版（Craig 1993）是**隐式**单向链表、每个线程在自己前驱的 `locked` 标志上**本地自旋**；AQS 改为**显式双向链表**（保留 `prev`，用于节点被取消或超时后从尾部回退重连），等待者用 `LockSupport.park` **阻塞**而非自旋，唤醒信号存放在**前驱节点的 waitStatus** 里。`head` 是哨兵，不代表任何等待者。

**3）waitStatus 五态**（Node 内 `volatile int`）：
`CANCELLED = 1`（超时/中断，出队前先标记）／`SIGNAL = -1`（后继待唤醒，本节点释放时必须 unpark 它）／`CONDITION = -2`（该节点在 condition 队列上）／`PROPAGATE = -3`（共享模式下"还有余量"需继续向后传播）／`0`（初始态）。非负值即"无需动作"，`ws > 0` 可直接判为已取消。

**4）独占获取 `acquire(int arg)` 是模板方法**：
`tryAcquire` 失败 → `addWaiter(Node.EXCLUSIVE)`（先一次乐观 enq，再 CAS tail）→ `acquireQueued`：循环里先 `shouldParkAfterFailedAcquire`（跳过 `ws>0` 的前驱；否则 CAS 把前驱置为 SIGNAL），再 `parkAndCheckInterrupt`。被唤醒后重试，成功则 `setHead`（节点 thread 置空，成为新哨兵）。循环对中断**只记不抛**，退出后由 `selfInterrupt()` 补回中断标记。

**5）释放 `release`**：`tryRelease` 成功 → `unparkSuccessor(h)`：把 head 的 ws 清 0，然后**从 tail 往回找**最靠前的非取消节点再 unpark。原因：激烈竞争下 `next` 指针可能尚未 CAS 完成，而 `prev` 一定已连好。

**6）共享模式**：`tryAcquireShared` 返回负数（失败）/0（成功但无余量）/正数（成功且有余量）。成功后 `setHeadAndPropagate`：若余量 > 0 或 head 为 PROPAGATE，则 `doReleaseShared` 继续唤醒后继——PROPAGATE 正是为修掉"共享传播中途中断导致后续线程漏唤醒"而引入。

**7）ConditionObject**：每个 Condition 是一条**单向**等待队列（复用 Node，`nextWaiter` 串联）。`await()`：`addConditionWaiter` → `fullyRelease`（一次性释放**全部**重入计数，因为 state 不记录"每层重入属于哪个条件"）→ `isOnSyncQueue` 为 false 时 park → 被 `signal` 时 `transferForSignal` 把节点 CAS 回同步队列 → 重新 `acquireQueued` 抢锁。`signalAll` 是逐个 transfer。条件队列与同步队列分离，正是"一把锁支持多个等待集"的实现方式。

## 三、JDK 版本演进

| 版本 | 与 AQS 相关的变化 |
| --- | --- |
| JDK 8 | 基线：`state`/`head`/`tail` 用 `sun.misc.Unsafe` 的 CAS，`LockSupport.park/unpark` 为阻塞原语；独占、共享、条件三种机制齐备 |
| JDK 9 | JEP 193（Variable Handles）：`STATE/HEAD/TAIL` 及 Node 字段改为静态 VarHandle 访问，语义等价 Unsafe 的 volatile/CAS，但类型安全且可被 JIT 内联 |
| JDK 11 | AQS 无功能变化，无新增公开 API |
| JDK 17 | 无变化；JEP 403（JDK 16 起强封装 JDK 内部 API）之后，业务代码无法再反射 AQS 私有字段 |
| JDK 21 | JEP 444 虚拟线程：虚拟线程在 ReentrantLock 上 park/unpark 时可被 JVM 卸载、重挂到 carrier thread，**不会**钉住；但 `synchronized` 会钉住 carrier。等待队列可能瞬间膨胀到百万量级，公平锁的尾延迟需重新评估 |
| JDK 24 | JEP 491（同步虚拟线程而不钉住）：`synchronized` 也不再钉住；JMM 与 AQS 契约不变 |
| JDK 25 | AQS 本身无新 API；随 JEP 471（JDK 23 弃用）/ JEP 498（JDK 24 使用告警）推进，`sun.misc.Unsafe` 的内存访问方法继续退役，JUC 内部已全部走 VarHandle |

## 四、经典论文

| 论文 | 出处 | 与 AQS 的关系 |
| --- | --- | --- |
| The java.util.concurrent Synchronizer Framework | Doug Lea, J. ACM 52(3), 2005 | AQS 的权威设计说明：acquire/release 模板、CLH 变体、条件队列 |
| Building FIFO and Priority-Queuing Spin Locks from Atomic Swap | Craig, Univ. of Washington Tech. Rep., 1993 | CLH 锁出处：原子 swap 入队、严格 FIFO、自旋于前驱 |
| Queue Locks on Cache Coherent Multiprocessors | Magnusson, Landin & Hagersten, 1994 | 队列锁在 cache-coherent 机器上的系统评估（CLH 命名的常见引用源） |
| Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors | Mellor-Crummey & Scott, TOCS 9(1), 1991 | MCS 锁：显式链表 + 每节点本地自旋；AQS"节点等自己的信号"思路同源 |
| Linearizability: A Correctness Condition for Concurrent Objects | Herlihy & Wing, TOPLAS 12(3), 1990 | 判定 Lock/Semaphore/Latch 这类并发对象正确性的标准模型 |
| Wait-Free Synchronization | Herlihy, TOPLAS 13(1), 1991 | 非阻塞层级（wait-free / lock-free / obstruction-free）的源头 |
| The Java Memory Model | Manson, Pugh & Adve, POPL 2005 | `state` 的 volatile 语义、happens-before 与"锁释放-获取"配对的正式定义 |
| Software Transactional Memory | Shavit & Touitou, PODC 1995 | 对照路线：AQS 走"阻塞 + 队列"，STM 走"乐观事务" |
| The Art of Multiprocessor Programming | Herlihy & Shavit, 2008 / 2012 | 教材：队列锁与锁的公平性、可伸缩性对比 |

## 五、近年研究与工业界实践

**同行评审论文**
- NVTraverse（Friedman 等，PPoPP 2021）：在非易失内存上遍历时不必持久化中间态、只需保证到达终态，为持久化队列/同步器提供了新思路。
- RefinedRust（Gäher 等，2024）：用 Rust 类型系统 + 分离逻辑自动验证并发数据结构，其典型目标之一就是"带等待队列的互斥锁"这类 AQS 式组件。
- Understanding Real-World Concurrency Bugs in Go（Tu 等，ASPLOS 2019）：对真实并发 bug 的分类研究表明，多数缺陷源于"误以为某段代码是原子的"，与 JMM（POPL 2005）的告诫一致。

**工业界资料**
- OpenJDK 主仓 `src/java.base/share/classes/java/util/concurrent/locks/AbstractQueuedSynchronizer.java` — https://github.com/openjdk/jdk
- JCTools — https://github.com/JCTools/JCTools ：无锁队列与缓存行填充实现，可与 AQS 的阻塞路径做吞吐对照
- JMH — https://github.com/openjdk/jmh ：锁竞争基准；jcstress — https://github.com/openjdk/jcstress ：JMM 一致性压力测试
- Netty — https://github.com/netty/netty ：`io.netty.util.concurrent` 中把 AQS 用于异步 Future 与线程模型

## 六、常见误区 + 跨语言对照

**常见误区**
1. "AQS 队列就是 CLH 队列"——是**变体**：双向链表、阻塞代替自旋、信号存在前驱的 waitStatus 中。
2. "公平锁所有入口都公平"——只有 `lock()`/`tryLock(timeout)` 走 `hasQueuedPredecessors()` 判断；无参 `tryLock()` **直接抢**，不排队。
3. "state 只能表示加锁次数"——许可数、倒计数值、读写 32 位拆分都可以是它。
4. "`await()` 只释放一层锁"——它 `fullyRelease`，重入 N 次会一次性清 0，返回时再恢复为 N。
5. "`lock()` 被中断会退出排队"——不会，它只置中断标记并继续抢锁；`lockInterruptibly()` 才抛异常。
6. "共享模式唤醒一次就够了"——漏掉 PROPAGATE 会让后续线程永久不被唤醒（JDK 历史缺陷，已在 JDK 6u 起修复）。
7. "虚拟线程下用 AQS 会钉住 carrier"——AQS 走 `LockSupport.park`，虚拟线程可卸载；钉住只发生在 `synchronized`（JDK 21，JDK 24 起已消除）。

**跨语言对照**

| 语言 | 对应设施 | 与 AQS 的差异 |
| --- | --- | --- |
| Java | `AbstractQueuedSynchronizer` + `ReentrantLock` + `Condition` | 单一队列承载同步与条件等待；可中断、可超时、可选公平 |
| C++ | `std::mutex` + `std::condition_variable`（C++11 起，多由 futex 支撑） | 无用户态等待队列抽象，队列在内核；无公平保证，等待不可中断 |
| Rust | `std::sync::Mutex` / `Condvar`；第三方 `parking_lot` | 标准库直接交予 futex；`parking_lot` 用自适应自旋 + 显式等待队列 + park/unpark，思路最接近 AQS |
| Go | `sync.Mutex`（Go 1.9 起有饥饿模式）+ `sync.Cond`；惯用法是 channel | 无等价 CLH 队列，用运行时 semaphore 排队；语言层面鼓励以通信代替共享内存 |
| Erlang | 无共享内存锁；`gen_server` 串行化 + 进程邮箱 | Actor 模型，进程内天然串行，靠消息传递而非队列锁 |
| Python | `threading.Lock` / `threading.Condition`（pthread 锁或信号量） | 不可中断、无公平队列；GIL 只保证单字节码/单 C 调用原子，不保证复合操作 |
