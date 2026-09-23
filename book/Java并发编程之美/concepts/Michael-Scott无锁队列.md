# Michael-Scott 无锁队列

> 定位：1996 年 PODC 论文提出的两种并发队列算法，是**无锁（non-blocking）队列**的事实标准。`java.util.concurrent.ConcurrentLinkedQueue` 就是它的 JDK 变体。
> 对应《Java并发编程之美》第 7 章「并发队列原理剖析」。

## 一、是什么（最小示例）

```java
ConcurrentLinkedQueue<Event> q = new ConcurrentLinkedQueue<>();

q.offer(new Event("click"));        // 入队：CAS 链表尾
Event e = q.poll();                 // 出队：CAS 链表头，空则返回 null
q.isEmpty();                        // O(1)
int n = q.size();                   // O(n)！且并发下不精确，别拿来做流控
```

它**无界、非阻塞、不允许 null 元素**，迭代器弱一致，不抛 `ConcurrentModificationException`。

## 二、实现原理（源码级）

**1）论文算法（非阻塞版）**：维护 `head`（指向哨兵 dummy）与 `tail`（指向最后一个或**倒数第二个**节点）。
- 入队两步 CAS：先 `CAS(tail.next, null, newNode)`——**这是线性化点**；再 `CAS(tail, tail, newNode)`。第二步失败没关系，说明别的线程已经帮它推进了（**helping**）。
- 出队：读 `head`、`next` 与 `next.next`；若 `head` 落后（tail 已越过 head）先帮着推进 `tail`；否则 `CAS(head, old, next)` 并取出 `next.item`。
- 关键不变式：**哨兵节点 + tail 允许滞后**，使入队的两次 CAS 不需要原子地一起完成，从而单线程失败不会阻塞他人——这就是 lock-free 的来源。

**2）论文第二种算法（两锁阻塞版）**：`head` 与 `tail` 各配一把锁，靠哨兵节点保证"队列永不为空"，使入队锁与出队锁不冲突；`LinkedBlockingQueue` 的双锁分离正是这一思路的工程实现。

**3）JDK 的惰性更新优化**：`ConcurrentLinkedQueue` 不保证 `head`/`tail` 精确定位，而是**批量推进**以降低 CAS 争用：
- tail：JDK 8 的 `offer` 里 `if (p != t) casTail(t, newNode)`，即**每两次入队才推进一次**（注释 `hop two nodes at a time`），失败可忽略。
- head：`poll` 成功后 `updateHead(h, p)` 把 head 前移一格，并 `h.lazySetNext(h)` 让被摘除的旧头**自链接**，既帮助 GC 回收已出队节点，也让遍历时能识别"已脱离队列"。
- 遍历遇到自链接（`p == q`）时，用 `p = (t != (t = tail)) ? t : head;` 从最新的 tail 或 head 重新开始。

**4）线性化点**：JDK 里**入队**的线性化点是 `casNext(null, newNode)`；**出队**的线性化点是 `p.casItem(item, null)`（把 item 置 null 表示已逻辑删除），而不是 `casHead`——head 的推进只是惰性清理。

**5）`size()` 为何 O(n)**：它遍历整条链表计数（`for (Node p = first(); p != null; p = succ(p)) if (p.item != null) ++count`）。因为结构里不维护计数器（维护一个全局原子计数会重新引入热点争用，违背无锁设计的初衷）。Javadoc 明确说明：该方法**不是常量时间**，且并发修改下结果可能不准。`isEmpty()` 只需判断 `first() != null`，是 O(1)；`contains`/`remove` 同样是 O(n)。

**6）ABA 与 GC 的角色**：
- 理论上，`CAS(next, A, B)` 会遇到 ABA：某线程读出 `next == A`，期间 A 被出队回收、又有一个新节点恰好复用同一地址。
- 在 Java 里这一问题由 **tracing GC** 兜住：只要该线程还持有对 A 的引用，A 就不可能被回收，其对象身份也不会赋给另一个逻辑节点；且 JVM 的对象引用并非裸地址（移动式/并发式 GC 下引用值对 Java 程序保持不变）。因此 CLQ 不需要版本号（tagged pointer）。
- 反过来说：**如果你用对象池复用 Node，ABA 就会真实发生**。无 GC 的语言（C/C++）必须显式做安全内存回收，Maged Michael 在 IEEE TPDS 2004 提出的 **hazard pointer** 是该问题的标准解法之一。

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 8 | `ConcurrentLinkedQueue` 基线：Unsafe CAS + 惰性 head/tail + 自链接辅助 GC；`ConcurrentLinkedDeque` 同期可用 |
| JDK 9 | JEP 193（Variable Handles）：`Node.item`、`next`、`head`、`tail` 的 volatile/CAS/lazySet 改为 VarHandle 访问 |
| JDK 11 | 无功能变化 |
| JDK 17 | 无功能变化 |
| JDK 21 | JEP 444 虚拟线程：无锁队列不使用 `synchronized`、不涉及钉住（pinning），海量虚拟线程并发访问下仍是安全选择；JDK 24 的 JEP 491 进一步消除 `synchronized` 的钉住问题 |
| JDK 25 | 无新 API；随 JEP 471（JDK 23 弃用）/ JEP 498（JDK 24 告警）推进，Unsafe 内存访问方法退役，JUC 原子访问统一为 VarHandle |

## 四、经典论文

| 论文 | 出处 | 与本文主题的关系 |
| --- | --- | --- |
| Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms | Michael & Scott, PODC 1996 | 主题论文：非阻塞版（本文 2.1 节）与两锁阻塞版（2.2 节）两种算法 |
| Safe Memory Reclamation for Dynamic Lock-Free Objects Using Hazard Pointers | Michael, IEEE TPDS 15(6), 2004 | 无 GC 环境下让无锁队列安全回收节点的经典方案 |
| Wait-Free Synchronization | Herlihy, TOPLAS 13(1), 1991 | 定义 wait-free / lock-free / obstruction-free 层级，MS 队列属 lock-free 而非 wait-free |
| Linearizability: A Correctness Condition for Concurrent Objects | Herlihy & Wing, TOPLAS 12(3), 1990 | 判定队列入队/出队线性化点的正确性条件 |
| The Java Memory Model | Manson, Pugh & Adve, POPL 2005 | `volatile` 与 `lazySet`（`putOrdered`）的语义，惰性更新依赖它 |
| The java.util.concurrent Synchronizer Framework | Doug Lea, J. ACM 52(3), 2005 | 对照路线：JUC 中阻塞队列走 AQS + Condition，无锁队列走 CAS |
| The Art of Multiprocessor Programming | Herlihy & Shavit, 2008 / 2012 | 教材专章讲并发队列与 ABA 问题 |

## 五、近年研究与工业界实践

**同行评审论文**
- NVTraverse（Friedman 等，PPoPP 2021）：非易失内存上的遍历只需保证"到达终态"而不必持久化中间态，MS 队列是该工作典型的评估对象之一。
- RefinedRust（Gäher 等，2024）：用类型系统 + 分离逻辑自动验证并发数据结构，无锁队列及其内存回收是其核心用例。
- Understanding Real-World Concurrency Bugs in Go（Tu 等，ASPLOS 2019）：真实 bug 研究显示共享队列/通道的误用是高频缺陷，与无锁结构"看起来免锁、实则语义微妙"的特点相符。

**工业界资料**
- OpenJDK：`src/java.base/share/classes/java/util/concurrent/ConcurrentLinkedQueue.java` — https://github.com/openjdk/jdk
- JCTools — https://github.com/JCTools/JCTools ：`SpscArrayQueue`/`MpscArrayQueue`/`MpmcArrayQueue`，用数组 + 缓存行填充和序号避免链表节点分配，是 MS 链表队列的高性能替代
- LMAX Disruptor — https://github.com/LMAX-Exchange/disruptor ：环形缓冲 + 序号屏障，彻底去掉节点分配与 CAS 重试，代表"换数据结构"而非"换算法"的路线
- Chronicle-Queue — https://github.com/OpenHFT/Chronicle-Queue ：mmap 持久化 append-only 队列
- Netty — https://github.com/netty/netty ：EventLoop 使用 MPSC 队列承接跨线程提交的任务
- JMH — https://github.com/openjdk/jmh （基准）；jcstress — https://github.com/openjdk/jcstress （验证队列的线性化与可见性）

## 六、常见误区 + 跨语言对照

**常见误区**
1. "无锁一定更快"——高争用下 CAS 反复失败 + 缓存行乒乓可能不如一把好锁；无锁的收益是**免死锁、免优先级反转、无上下文切换**，吞吐要实测。
2. "`size()` 很便宜"——O(n) 遍历且不精确；要流控请另配一个 `AtomicLong` 或 `LongAdder`。
3. "无锁就没有内存回收问题"——Java 靠 GC "躺赢"；C/C++ 需要 hazard pointer、epoch-based reclamation 或 RCU。
4. "ABA 不可能发生"——前提是 GC 与"不复用节点"；一旦引入对象池或堆外手工管理，ABA 立刻重现。
5. "`ConcurrentLinkedQueue` 可以阻塞等待"——不能，它是非阻塞队列；要阻塞语义用 `LinkedBlockingQueue` 或 `LinkedTransferQueue`。
6. "`poll()` 返回 null 说明队列永久为空"——只代表调用瞬间可能为空，另一个线程可能正准备入队。
7. "无界队列可以随便堆"——没有背压，消费跟不上就是内存暴涨；应改用有界队列或外部信号量。
8. "迭代器能看到所有元素"——弱一致，可能漏掉遍历期间的更新，但绝不抛 `ConcurrentModificationException`。

**跨语言对照**

| 语言 | 对应设施 | 与 MS 队列的差异 |
| --- | --- | --- |
| Java | `ConcurrentLinkedQueue`（MS 变体，惰性 tail/head + 自链接）、`ConcurrentLinkedDeque`、JCTools 队列族 | 依赖 GC 免除显式内存回收；`size()` 为 O(n) |
| C++ | 标准库无无锁队列；`boost::lockfree::queue`（MS 队列系）、`folly::MPMCQueue`（Vyukov 有界 MPMC）、`moodycamel::ConcurrentQueue` | 必须自行解决 ABA 与节点回收（hazard pointer / 引用计数 / 静态容量） |
| Rust | `crossbeam::queue::SegQueue`（无界，MS 系变体）与 `ArrayQueue`（有界）；`std::collections::VecDeque` 需配合 `Mutex` | 所有权系统可静态避免数据竞争，但无锁路径仍需 unsafe + 显式回收策略 |
| Go | 无官方无锁队列；惯用 `channel`（带缓冲）与 `sync.Pool`（per-P 私有链表） | 语言鼓励消息传递；标准库不为通用场景暴露 CAS 队列 |
| Erlang | 进程邮箱（消息传递，无共享内存队列） | 完全没有共享内存无锁结构的必要，背压需显式设计 |
| Python | `queue.Queue`（锁 + Condition）、`collections.deque`（单线程语义，需自行加锁）、`asyncio.Queue` | GIL 与解释器开销使无锁收益极小，生态里基本没有无锁队列实现 |
