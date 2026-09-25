# 专篇：Michael-Scott 队列、无锁算法与"内存回收"这个真正的难题

> 对应本书第 7 章《并发队列原理剖析》。本书讲了 `ConcurrentLinkedQueue` 的**使用**，
> 但**没有展开算法本身**，更没有触及无锁编程真正的深水区——
> **内存回收（memory reclamation）**。在有 GC 的 Java 里这个问题被"藏"起来了，
> 但只要你读 C++/Rust 的无锁代码，或者要回答"为什么 Java 的无锁队列还是有坑"，
> 就绕不开它。

## 一、本章地图

```
有锁队列的局限：一个线程阻塞 → 所有人不能进（锁的"护航效应"）
        ↓
Michael-Scott (1996) 算法：哑节点 + 两步 CAS + tail 允许"落后"
        ↓
JDK ConcurrentLinkedQueue 的实现细节：slack、自链接（self-link）助 GC
        ↓
无锁 ≠ 无代价：ABA、内存回收、size() 是 O(n)
        ↓
内存回收四代方案：hazard pointer / epoch / interval-based / VBR
        ↓
近年：LCRQ、k-FIFO —— 无锁队列还在演进
```

## 二、为什么需要无锁队列

| 锁的问题 | 说明 |
| --- | --- |
| **护航效应（convoy effect）** | 持锁线程被抢占/页缺失/GC 停顿 → **所有**等待者一起卡住 |
| **死锁 / 优先级反转** | 锁的固有风险 |
| **无法在信号处理器等上下文用** | 阻塞不安全 |
| **粒度固定** | 锁把整个结构串行化，哪怕两个线程操作的是不同部分 |

无锁（lock-free）的定义：**系统整体保证向前推进**（某个线程一定能在有限步内完成操作），
但**不保证每个线程**都能完成（那是 wait-free）。

## 三、Michael-Scott 算法（PODC 1996）

### 3.1 结构：单链表 + 哑节点（sentinel）

```
   head                                  tail
    ↓                                     ↓
  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
  │ dummy  │→  │  data1 │→  │  data2 │→  │  data3 │→ null
  │(sentinel) │        │        │        │
  └────────┘   └────────┘   └────────┘   └────────┘
```

- **`head` 永远指向哑节点**（已出队、值域为 `null`）；
- **`tail` 允许落后**——它可能指向最后一个节点，也可能指向**倒数第二个**；
  这是"允许松弛（slack）"的关键设计，让入队只需 **1 次成功 CAS**（摊销）。

### 3.2 `enqueue(x)`

```java
// 伪代码
Node n = new Node(x);
for (;;) {
    Node t = tail, next = t.next;
    if (t == tail) {                       // ① 确认 tail 没被别人改
        if (next == null) {                // ② tail 确实是最后一个
            if (CAS(t.next, null, n)) {    // ③ 关键 CAS：接上链表
                CAS(tail, t, n);           // ④ 推进 tail —— 失败也没关系！
                return;
            }
        } else {
            CAS(tail, t, next);            // ⑤ tail 落后了，帮别人推进
        }
    }
}
```

> **第 ④ 步失败不用管**——这是 MS 算法最精妙的一点：
> `tail` 落后一个节点是**允许的**，别的线程会帮它推进（第 ⑤ 步）。
> 因此入队的**关键路径只需一次 CAS**，而不是两次（早期算法要求两次都成功，
> 会导致一个线程阻塞时整条链卡住）。

### 3.3 `dequeue()`

```java
for (;;) {
    Node h = head, t = tail, next = h.next;
    if (h == head) {
        if (h == t) {                 // 队列空，或 tail 落后
            if (next == null) return EMPTY;
            CAS(tail, t, next);       // 帮 tail 推进
        } else {
            E v = next.item;
            if (CAS(head, h, next))   // 关键 CAS：把 head 推到 next
                return v;             // next 成为新的哑节点
        }
    }
}
```

**出队只需一次 CAS**：把 `head` 前移一格，原 `head` 变成废弃哑节点。

### 3.4 为什么它是正确的

- 每个 CAS 都是**单一内存字的原子操作**，成功后全局状态前进一格；
- 失败的线程只是"重试"，不会破坏不变量（哑节点始终在 head，链表始终连通）；
- 它是 **lock-free**（不是 wait-free）：某个线程会成功，但特定线程可能饿死。

## 四、JDK `ConcurrentLinkedQueue` 的实现细节

JDK 的 Javadoc 明说：

> "This implementation employs an efficient non-blocking algorithm based on one described in
> *Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms*
> by Maged M. Michael and Michael L. Scott."

### 4.1 松弛（slack）策略

| 版本 | 做法 |
| --- | --- |
| JDK 6/7 | 常量 `HOPS = 1`：`tail` 允许落后至多 1 个节点，超过才 CAS 推进 |
| JDK 8+ | **去掉 `HOPS` 常量**，改为在遍历中内联判断 `p != t && t != (t = tail)` 来推进 `head`/`tail`——效果相同但代码更紧凑 |

### 4.2 **自链接（self-link）助 GC** —— JDK 特有的精巧设计

```java
// JDK 8+ updateHead
final void updateHead(Node<E> h, Node<E> p) {
    if (h != p && casHead(h, p))
        h.lazySetNext(h);      // ← 让旧 head 的 next 指向自己！
}
```

**作用**：

1. **帮助 GC**：出队后的节点从链表上"摘下来"（`next` 指向自己，不再指向后继），
   避免长链表被废弃节点拖住无法回收；
2. **作为"已删除"标记**：其他线程读到 `p == p.next` 就知道这个节点已被移出，
   需要**从头重新开始遍历**（`continue restartFromHead`）。

> 这是"用 GC 语言写无锁结构"的一个独特优势：C/C++ 里无法这么做
> （`next` 指向自己后节点本身还是不能释放，需要 hazard pointer 保护）。

### 4.3 `ConcurrentLinkedQueue` 的四个坑

| # | 坑 | 说明 |
| --- | --- | --- |
| 1 | **`size()` 是 O(n)** | Javadoc 明说："**not a constant-time operation**"，且并发修改时结果不可靠。判断非空请用 `isEmpty()`（O(1)） |
| 2 | `contains()` / `remove(Object)` 是 O(n) | 不要当 Set 用 |
| 3 | 迭代器是**弱一致**的 | 不抛 `ConcurrentModificationException`，可能看到部分修改 |
| 4 | `addAll()` 不是原子的 | 只保证逐个元素入队 |

## 五、无锁 ≠ 没有代价：三个真实问题

### 5.1 ABA 问题

```
线程 A 读到 head.next = X
线程 A 被挂起
线程 B 出队 X，出队 Y，又把 X 重新入队（地址复用！）
线程 A 恢复，CAS(head, X, ...) 成功 —— 但它以为 X 还是原来的 X
```

**在 Java 里为什么通常没事？**
因为 **GC 保证：只要线程 A 还持有 X 的引用，X 就不会被回收、更不会被复用为新节点**。
所以 MS-queue 在 Java 里是安全的。

**但 ABA 在其他地方照样咬人**：

- 无 GC 语言（C/C++/Rust 裸指针）；
- **值域 ABA**：`ConcurrentLinkedQueue` 用 `CAS(p.item, item, null)` 来"逻辑删除"，
  这就要求 `item` 一旦置 `null` 就不能再被改回——否则线程会看到"复活"的元素；
- 自定义无锁结构用自己的对象池时（**最容易踩**：对象池 = 手工的"内存复用"）。

**解法**：版本号（`AtomicStampedReference`）、hazard pointer、tagged pointer（把计数器塞进指针低位）。

### 5.2 内存回收（真正的深水区）

在 C/C++/Rust 里，一个节点被"逻辑删除"后，**可能还有别的线程正拿着它的指针**，
此时 `free()` 会造成 **use-after-free**。这就是无锁编程最难的部分。

| 方案 | 思想 | 代价 |
| --- | --- | --- |
| **Hazard Pointer**（Michael 2004） | 每个线程**公告**"我正要访问这几个指针"，删除者看到公告就不释放 | 每次访问一次 fence（写公告 + 重读验证）；退役列表批量扫描 |
| **Epoch-Based Reclamation**（Fraser 2004） | 全局"纪元计数器"，线程进入临界区时登记 epoch；只有**所有线程都离开某 epoch** 才能释放该 epoch 的退役节点 | 轻量，但**一个线程卡住会阻塞全局回收**（内存膨胀） |
| **Interval-Based**（Ruan 等 PPoPP'18） | 用**时间戳区间**精确刻画"节点何时绝对无人引用"，无需线程遍历退役列表 | 需要全局时钟/计数器；近年主流方向 |
| **VBR（Version Based Reclamation）** | 给节点打版本号，读者声明版本号范围 | 需要两次读 + 全局版本号 |
| **Quiescent State / DEBRA+** | 线程周期性声明"我 quiescent 了"，之后该线程之前退役的节点可释放 | 依赖线程主动让出 |
| **GC**（Java/Go/C#） | 让运行时负责 | **最省心，但 STW 停顿 + 分配速率代价** |

> **这就是 Java 的隐藏福利**：JUC 所有无锁结构之所以敢写，是因为有 GC 兜底。
> 但代价是：**无法精确控制回收时机**，且高分配速率会加剧 GC 压力。
> 因此 Disruptor、JCTools 这类追求极致延迟的库会**预分配环形数组**，几乎不做分配。

### 5.3 争用反而更糟

MS-queue 的**入队都 CAS 同一个 `tail`**，多生产者下 `tail` 本身就是热点：
100 个线程同时入队 → 与 `AtomicLong` 一样的问题（见《LongAdder与分段累加》）。

**工业界的答案**：

- **专用化**：SPSC / MPSC / SPMC / MPMC 分开实现（JCTools 的核心思路），
  SPSC 无锁队列可以做成**完全无 CAS**的（只有 volatile 读写 + 缓存行填充）；
- **批处理**：一次挪一批（k-FIFO）；
- **环形缓冲 + 序号**：Disruptor；
- **多队列 + 窃取**：LCRQ 的 CRQ（Concurrent Ring Queue）变体。

## 六、JDK 8 → 21 的变化

| 版本 | 变化 |
| --- | --- |
| JDK 7 | 引入 `ConcurrentLinkedDeque`（无锁双端队列，基于 Sundell-Tsigas 一脉的思路） |
| JDK 8 | `ConcurrentLinkedQueue` 重写（`HOPS` 移除、自链接助 GC、`lazySetNext` 用 `putOrderedObject`） |
| JDK 9 | `Unsafe` → **VarHandle**；`lazySet` 语义由 `VarHandle.setRelease` 表达（见《CAS与原子操作》） |
| JDK 21 | 虚拟线程下无锁队列**依然推荐**（CAS 不涉及 pin） |

## 七、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Michael, M. M. & Scott, M. L. 1996. "Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms." PODC '96, pp. 267-275.** | **本篇主题**。一篇论文同时给出无锁队列与两锁阻塞队列；`ConcurrentLinkedQueue` 与 `LinkedBlockingQueue` 的共同源头 |
| **Treiber, R. K. 1986. "Systems Programming: Coping with Parallelism." IBM Research Report RJ 5118.** | **Treiber 栈**：最简单的无锁结构；也是理解 CAS 循环的最佳入门 |
| **Valois, J. D. 1995. "Lock-Free Linked Lists Using Compare-and-Swap." PODC '95.** | 早期无锁链表；**系统讨论 ABA 问题**并提出"引用计数 + 辅助节点"方案 |
| **Herlihy, M. 1991. "Wait-Free Synchronization." ACM TOPLAS 13(1).** | 提出 **wait-free / lock-free / obstruction-free** 的层级划分与通用构造（universal construction） |
| **Michael, M. M. 2004. "Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects." IEEE TPDS 15(6): 491-504.** | **内存回收的奠基作**，至今仍是 C/C++ 无锁库的标配 |
| **Fraser, K. 2004. "Practical Lock-Freedom." PhD thesis, University of Cambridge.** | Epoch-based reclamation 的系统化；影响了 Linux RCU 的设计思路 |
| **Harris, T. L. 2001. "A Pragmatic Implementation of Non-Blocking Linked-Lists." DISC '01.** | 无锁链表 + 标记删除（marked pointer） |
| **Sundell, H. & Tsigas, P. 2005. "Lock-Free and Practical Doubly Linked List-Based Deques Using Single-Word Compare-and-Swap." DISC '05.** | `ConcurrentLinkedDeque` 的算法来源 |
| **Morrison, A. & Afek, Y. 2013. "Fast Concurrent Queues for x86 Processors." PPoPP '13.** | **LCRQ**：用环形数组 + `fetch&add` 取代链表 CAS，多生产者下吞吐远超 MS-queue；近年最有影响力的队列工作 |
| **Yang, X. & Mellor-Crummey, J. 2016. "Fast and Scalable Lock-Free k-FIFO Queues." ACM TOPC 3(2).** | 批量出队降低争用 |
| **Brown, T. A. 2015. "Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way." PPoPP '15.** (DEBRA+) | 对"退役列表扫描"开销的批判与改进 |
| **Ruan, W., Spear, M., Michael, M. M., Scott, M. L. 2018. "Interval-Based Memory Reclamation." PPoPP '18.** | 用时间戳区间精确判定安全回收点，避免遍历退役列表 |
| **Sheffi, G., Luchangco, V., Petrank, E. 2021. "VBR: Version Based Reclamation." OPODIS '21.** | 近年新方案；用版本号范围做回收判定（可按标题检索核实） |
| **Herlihy, M. & Shavit, N.《The Art of Multiprocessor Programming》第 10-11 章** | 队列 + 池 + 内存回收的系统教材 |

## 八、近年研究与工业界前沿

### 近年研究

- **从链表回到数组**：MS-queue 是链表，缓存局部性差；LCRQ / CRQ 用"环形数组 + FAA"重新成为主流研究方向。
- **专用化胜于通用**：SPSC 队列可以做到**零 CAS**（只有 volatile load/store + padding），是近十年延迟敏感系统的共识。
- **内存回收仍是开放问题**：PPoPP 每年都有新方案；近年热点是"与语言集成的自动回收"（如 Rust 的 `crossbeam-epoch` 与类型系统结合）。
- **持久内存队列**：崩溃一致性（flush + fence 顺序）给无锁队列带来新的正确性维度。
- **形式化验证**：用模型检测/定理证明验证无锁队列的线性化性（如 Verified SC/SCQ 的形式化工作）。

### 工业界开源实现（2026-09 核验）

| 项目 | Stars | 说明 |
| --- | --- | --- |
| **JCTools/JCTools** | 3.9k | **Java 无锁队列的权威实现**。按 SPSC/MPSC/SPMC/MPMC × 有界/无界提供十余种队列；`MpscUnboundedArrayQueue` 是 Netty 默认队列；大量使用缓存行填充（配合《伪共享FalseSharing》篇看） |
| **LMAX-Exchange/disruptor** | 18.5k | 环形缓冲 + 序号 + 无分配；**SPSC/MPSC 场景下比 MS-queue 快一个数量级** |
| **facebook/folly** | 30.5k | `folly::MPMCQueue`（Vyukov 有界 MPMC 队列，用序号 + 版本号而非链表）、`folly::ProducerConsumerQueue`（SPSC） |
| **crossbeam-rs/crossbeam** | 8.6k | Rust：`SegQueue`（无界无锁）、`ArrayQueue`；`crossbeam-epoch` 是 epoch 回收的 Rust 标准实现 |
| **netty/netty** | 35.1k | EventLoop 用 MPSC 队列；`Recycler` 用无锁栈做对象池 |
| **openjdk/jdk** | 23.4k | `ConcurrentLinkedQueue.java`、`ConcurrentLinkedDeque.java`（源码注释里直接写着论文出处） |
| Dmitry Vyukov, 1024cores.net | — | **有界 MPMC 队列的经典设计文档**（序号 + 版本号），folly/JCTools 都有对应实现 |

## 九、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "无锁一定比加锁快" | **低争用**无锁快；**高争用**下所有线程 CAS 同一个 `tail`，退化成热点，可能不如锁 |
| 2 | "lock-free = 每个线程都会成功" | 那是 **wait-free**。lock-free 只保证**系统整体**前进，个别线程可能饿死 |
| 3 | "Java 里没有 ABA 问题" | GC 解决了**节点复用型** ABA；但**值域 ABA** 与**自定义对象池**里照样发生 |
| 4 | "无锁就不需要内存回收策略" | Java 有 GC 兜底；C/C++/Rust 必须配 hazard pointer / epoch 等方案 |
| 5 | "`ConcurrentLinkedQueue.size()` 很快" | **O(n) 且并发下不准**；用 `isEmpty()` |
| 6 | "`tail` 总指向最后一个节点" | **允许落后一格**（slack），这是算法的核心取舍 |
| 7 | "出队后节点立刻被回收" | JDK 用**自链接** `h.lazySetNext(h)` 帮助 GC；否则废弃链表可能长期驻留 |
| 8 | "无锁结构可以随便迭代" | 弱一致迭代器；`addAll` 非原子 |
| 9 | "虚拟线程会破坏无锁队列" | **不会**，CAS 路径不涉及 `synchronized` pinning |
| 10 | "MS-queue 是最终形态" | 近年 LCRQ / 环形队列在**多生产者**场景吞吐显著更高；MS-queue 的优势是**无界 + 实现简单** |

> **本书补充定位**：本书第 7 章讲到了 `ConcurrentLinkedQueue` 的用法层面，
> 本篇补上算法本身（两步 CAS + slack）、JDK 的自链接技巧，
> 并打开"内存回收"这个 Java 程序员平时看不到、但在跨语言与极致性能场景绕不开的话题。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

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
