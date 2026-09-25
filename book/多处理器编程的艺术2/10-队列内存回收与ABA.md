# 第 10 章 队列、内存管理与 ABA 问题

> **本章地图**：队列接口与三种类型（**有界 Partial / 无界 Total / 无界 + 部分 Sentinel）→ 有界阻塞队列（条件队列 + `notFull/notEmpty`）→ 无界**加锁**队列（**两把锁**：`putLock` 与 `takeLock`）→ 无界**无锁**队列（**Michael & Scott queue**，哨兵哑节点）→ **ABA 问题**：它是如何无声地破坏 CAS 的 → 版本戳（`AtomicStampedReference`）与 GC 的关系 → 为什么 Java 里 MS 队列不容易 ABA，而 C/C++ 必须配合第 19 章的内存回收。

## 二、核心精讲

### 10.1 队列的四种分类（本书术语）

| 类型 | 语义 | 典型实现 |
| --- | --- | --- |
| **Bounded Partial Queue（有界部分队列）** | 容量固定；空时 `deq` 阻塞（或返回特殊值），满时 `enq` 阻塞 | `ArrayBlockingQueue` |
| **Unbounded Total Queue（无界全队列）** | 容量无限；只有队空时 `deq` 阻塞 | `LinkedBlockingQueue` |
| **Unbounded Lock-free Queue** | 同上但不阻塞，空时返回 null/特殊值 | `ConcurrentLinkedQueue`（MS 队列） |
| **Bounded Lock-free Queue** | 极少使用，需要原子同时操纵计数 | 研究性质 |

### 10.2 有界队列：一把锁 + 两个条件队列

```java
// （教学片段，不参与构建）有界阻塞队列的经典写法
class BoundedQueue<T> {
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull  = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();
    private final Object[] items;
    private int head, tail, count;

    public void enq(T x) throws InterruptedException {
        lock.lock();
        try {
            while (count == items.length) notFull.await();      // while + await，Mesa 语义
            items[tail] = x; tail = (tail + 1) % items.length; count++;
            notEmpty.signal();
        } finally { lock.unlock(); }
    }

    public T deq() throws InterruptedException {
        lock.lock();
        try {
            while (count == 0) notEmpty.await();
            T x = (T) items[head]; head = (head + 1) % items.length; count--;
            notFull.signal();
            return x;
        } finally { lock.unlock(); }
    }
}
```
- 🔧 一把锁意味着**生产与消费互相阻塞**，这就是为什么 JDK 的 `LinkedBlockingQueue` 用两把锁。

### 10.3 无界加锁队列：双锁优化 + 哨兵节点
- **两把锁**：`putLock` 保护尾、`takeLock` 保护头。生产者与消费者各自竞争自己的锁，**互不干扰**。
- **哑节点 / 哨兵（sentinel / dummy node）**：始终有一个"假"的头节点，`head` 指向它，`head.next` 才是真正的队首。这样"头指针不变"，消除了"空队列时 `head == tail`"的复杂度。
- 但要注意：count 字段需要跨两把锁更新，因此 `LinkedBlockingQueue` 用 `AtomicInteger count`；JDK 还通过对 count 的原子更新避免了“同时拿两把锁”的需要。
- 🔧 这是 JDK 的真实实现（`LinkedBlockingQueue` 内部就是 putLock / takeLock 两把锁）；它也是 `ThreadPoolExecutor` 的默认队列选择之一，详见 `Java并发编程之美/08-线程池`。

### 10.4 无锁队列：Michael & Scott Queue（PODC 1996）

```java
// （教学片段，不参与构建）MS 队列：入队两步、出队一步，全部用 CAS
public class MSQueue<T> {
    AtomicReference<Node> head, tail;

    public MSQueue() {
        Node sentinel = new Node(null);          // 哨兵哑节点：head 永远指向它
        head.set(sentinel); tail.set(sentinel);
    }

    public void enq(T item) {
        Node newNode = new Node(item);
        while (true) {
            Node last = tail.get(), next = last.next.get();
            if (last == tail.get()) {                       // last/next 是否还自洽？
                if (next == null) {                         // 尾部确实是最后一个
                    if (last.next.compareAndSet(next, newNode)) {  // ① 链接新节点
                        tail.compareAndSet(last, newNode);         // ② 更新 tail（可 lazy）
                        return;
                    }
                } else {                                    // tail 落后了，帮它推进
                    tail.compareAndSet(last, next);
                }
            }
        }
    }

    public T deq() {
        while (true) {
            Node first = head.get(), last = tail.get(), next = first.next.get();
            if (first == head.get()) {                      // 三者是否自洽？
                if (first == last) {                        // 队列空（或 tail 落后）
                    if (next == null) return null;
                    tail.compareAndSet(last, next);         // 帮 tail 推进
                } else {
                    T value = next.item;
                    if (head.compareAndSet(first, next))    // 出队：head 前移
                        return value;
                }
            }
        }
    }
}
```
- **线性化点**：入队 = `next` CAS 成功；出队 = `head` CAS 成功。
- **tail 可以滞后**：入队第二步失败无所谓，其它线程会"帮它推进"（helping）。这是无锁算法最典型的优化手法。
- 🔧 JDK 的 `ConcurrentLinkedQueue` 就是 MS 队列的工业版本，且做了两个重要优化：**延迟更新 tail（hoplite 2-hop hopskip）** 与用 `VarHandle` 对 head/tail 做精确的内存序控制。

### 10.5 ABA 问题：无声破坏 CAS 的经典

**场景**（以栈/队列为例）：
1. 线程 T1 读 A 处，读到 `head == A`，准备执行 `CAS(head, A, B)`；
2. T1 被挂起；
3. 其它线程执行了：弹出 A、弹出 B、再把 A **重新压回**（或从对象池复用同一个节点地址）；
4. T1 恢复执行 CAS：`head` 看起来**还是 A**，于是 CAS 成功 —— 但实际上链表结构已经完全变了，T1 把错的东西接了上去。

```java
// （教学片段，不参与构建）ABA 的可NumberOfForms化的解法：给指针打版本戳
class StampedNode<T> {
    final T value;
    final AtomicStampedReference<StampedNode<T>> next;   // 引用 + 版本戳，每次修改都自增
}
// CAS 时同时比较引用与版本戳：CAS(expectedRef, newRef, expectedStamp, newStamp)
AtomicStampedReference<Node> ref = new AtomicStampedReference<>(head, 0);
ref.compareAndSet(head, newHead, 0, 1);   // 既校验地址也校验“被改过几次”
```

- **为什么 Java 里的 MS 队列通常不用担心 ABA**：每次 `new Node()` 都产生一个新的对象身份，GC 保证旧对象不会被回收后再用同一个地址生成新对象 —— 因此"地址复用 ABA"不可能发生。
- **但只要有对象复用就回到 ABA**：如果你用对象池（`ArrayBlockingQueue` 的 node pool、Netty 的 `Recycler`）或者写 C/C++/Rust，就必须处理。这正是第 19 章（HP / EBR）存在的原因。
- 🔧 **JVM 侧的现实 1**：`Disruptor` 的 ring buffer 用预分配数组，天然没有 ABA；反而是通过内存预分配避免了 GC 与 ABA 双重问题。
- 🔧 **JVM 侧的现实 2**：JDK 的 `ConcurrentLinkedDeque`、`LinkedTransferQueue` 等都有各种 slots + GC 的假定；把 `Node.item = null` 作为"已出队"标记，依赖 GC 回收 —— 这是一个"用 GC 换正确性"的经典 tradeoff。

## 三、经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| **Michael & Scott《Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms》** | PODC 1996 | **MS 队列**（本章核心，也是 `ConcurrentLinkedQueue` 的直接来源） |
| Treiber《Systems Programming: Coping with Parallelism》 | IBM RJ 5118, 1986 | Treiber 栈（下一章）与本处的并发 cinqit 思路 |
| Michael《Safe Memory Reclamation for Dynamic Lock-Free Objects Using Atomic Reads and Writes》 | PODC 2002 | 内存回收与 ABA 关系的系统阐述 |
| Michael《ABA Prevention Using Single-Word Instructions》 | IBM TR 2003 | 用单字解决 ABA 的技巧 |
| Luchangco, Moir, Shavit（哨兵节点相关的 correctness 分析） | 本书 Ch10 | 本书自己的教学表述 |

## 四、近年研究与工业界开源实践

- **近年研究**：**基于插槽 reservation 的内存回收协议**（2020 年代）与"零单操作开销的延迟回收"（如 Version Based Reclamation，VBR，PPoPP 2017，Alistarh et al.）；NVIDIA 的 libcu++ 与各类 CUDA 并发数据结构也是在更弱的内存序层次上对队列实现的探索；MS 队列的**形式化验证**已成为模型检查领域的事实标准样例（可用 lincheck / VerCors / Iris 等工具验证）。
- **工业界开源**（star 数 2026-09 实测）：
  - `openjdk/jdk`（≈23.4k★）：`ConcurrentLinkedQueue`、`LinkedBlockingQueue`（双锁）、`ArrayBlockingQueue`（条件队列）三份源码，是本章三个版本的完整对照。
  - `JCTools/JCTools`（≈3.9k★）：工业级无锁队列，包含 MPSC/MPMC/SPMC 各种变体，展示了"限制生产者/消费者数量"能带来多大优化空间。
  - `LMAX-Exchange/disruptor`（≈18.5k★）：用**预分配 ring buffer + 序号屏障**绕开了队列节点的动态分配与竞争，是应对内存回收问题的另一条思路。
  - `facebook/folly`（≈30.5k★）：folly 的 `ProducerConsumerQueue`、`MPMCQueue` 与 hazptr 配合的典型产品级实现。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "两把锁一定比一把锁好" | 只有当生产端与消费端使用**相互独立**的两把锁时才划算；双锁还带来复杂度：count 需要跨锁维护 |
| 2 | "哨兵节点只是为了让 head 不为 null" | 它更重要的作用是让"空队列"与"非空队列"的判定统一，从而简化 CAS 逻辑 |
| 3 | "无锁队列不会阻塞，所以一定更快" | 空出队时它会自旋重试；高争用下 MS 队列的 CAS 争抢开销可能远不如双锁版本 |
| 4 | "ABA 是现代机器上的老黄历" | 只要使用对象池、无 GC 语言，或复用同一地址的节点，ABA 就会出现 |
| 5 | "GC 语言就不需要关心回收算法" | Java 靠 GC 兜住了节点回收，但对象池场景（如 Netty 的 `Recycler`）又把 ABA 带了回来 |
| 6 | 🔧 本书视角 | 本书以 C/Java 混合视角写；现代 C++ 与 Rust 有完全不同的资源管理负担，必须叠加第 19 章的内容与语言级 hooks（`Send`/`Sync`、ARC/ownership） |
