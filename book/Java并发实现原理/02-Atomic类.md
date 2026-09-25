# 第 2 章 Atomic类（原书 pp.29-48）

> 手写 `AtomicInteger`/`AtomicLong`/`AtomicReference` 与 `Atomic*Array`/`Atomic*FieldUpdater`，并手写**无锁栈、无锁队列、无锁链表**验证 CAS 实战。与《艺术》7 章 + 《之美》`concepts/CAS与原子操作.md`、`Michael-Scott无锁队列.md` 互补。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| `AtomicInteger`/`Long` | 封装 `Unsafe.compareAndSwap`（手写 getAndIncrement） |
| `AtomicReference` | 引用 CAS；ABA → `AtomicStampedReference` |
| `Atomic*Array` | 数组元素级原子（计算元素偏移） |
| `Atomic*FieldUpdater` | 反射级字段 CAS（省对象分配） |
| 手写无锁栈 | Treiber 栈（CAS 头指针） |
| 手写无锁队列 | Michael-Scott（CAS 尾指针） |
| 手写无锁链表 | CAS + 标记删除（Harris/Michael） |

## 二、核心精讲

### 2.1 手写 `AtomicInteger`
- 本质：`private volatile int value;` + `Unsafe.compareAndSwapInt(this, valueOffset, expect, update)`。
- `getAndIncrement()`：自旋 `do { old=value; } while(!cas(old, old+1));`——失败重试直到成功（lock-free）。
- 🔧 现代：`Unsafe` 在 JDK 21+ 废弃 → 应改用 `VarHandle`（JEP 193/471/498）。

### 2.2 ABA 与版本戳
- 手写 `AtomicStampedReference`：`Pair(reference, stamp)`，CAS 时比 `(引用, 版本)` → 防 ABA（引用被复用 / 节点被回收再分配）。
- 无锁链表尤其需要：节点删除后内存可能被复用，光看引用相等会误判。

### 2.3 手写无锁栈（Treiber）
- `head` 用 `AtomicReference<Node>`；`push`：`do { n.next=head; } while(!cas(head, n));`——头插法，CAS 头指针。
- 出栈同理 CAS 把 head 指向 `head.next`。

### 2.4 手写无锁队列（Michael-Scott）
- `head`/`tail` 两 `AtomicReference`；入队 CAS `tail.next` 再 CAS `tail`；出队 CAS `head` 再返回 `head.next` 值。
- **tail slack**：`tail` 不总指向真正尾（CAS 成功后别的线程可能已插新节点）→ 出队/入队要"从 tail 往后找真尾"（详见《之美》MS 队列专篇）。

### 2.5 手写无锁链表（标记删除）
- 删除节点：先 CAS 把节点的 `next` 打"删除标记"（用最低位 bit），再 CAS 把前驱的 `next` 跳过它。
- Harris (2001) / Michael (2002) 算法——工业级无锁链表基础（Java `ConcurrentLinkedQueue` 用变体）。

## 三、版本演进

- **JDK 5**：`Atomic*` 全部引入（基于 `Unsafe`）。
- **JDK 8**：`LongAdder`/`LongAccumulator`（分段累加，手写 CAS 单点的高争用解药，本章未展开 → 见《之美》LongAdder 专篇）。
- **JDK 9**：`VarHandle` 替代 `Unsafe`。
- **JDK 21+**：`Unsafe` 废弃通道。

## 四、经典论文 / 原始文献

- **Herlihy, "Wait-Free Synchronization" (PODC 1991, Dijkstra 奖)**——共识层级，CAS 的 wait-free 实现。
- **Treiber, "Systems Programming: Cocycles and Linked Lists" (1986)**——无锁栈。
- **Michael & Scott, "Non-Blocking..." (PODC 1996)**——无锁队列。
- **Harris, "A Pragmatic Implementation of Non-blocking Linked Lists" (DISC 2001)** / **Michael, "Hazard Pointers" (2004)**——无锁链表 + 安全内存回收。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `Atomic*`/`VarHandle`/`ConcurrentLinkedQueue` |
| **JCTools/JCTools** | 3.9k | 工业级手写无锁队列（SPSC/MPSC/MPMC） |
| **crossbeam-rs/crossbeam** | 8.6k | Rust 无锁队列/epoch GC（思想对照） |
| **facebook/folly** | 30.5k | `AtomicHashArray`、hazard pointer |
| **openjdk/jcstress** | 2.1k | 验证手写无锁结构弱内存正确性 |

## 六、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CAS 无 ABA" | 引用/指针复用必有；用 `AtomicStampedReference` |
| 2 | "手写 Unsafe 即可" | 🔧 JDK 21+ 废弃；改 VarHandle |
| 3 | "AtomicLong 可伸缩" | 热点域抢同缓存行；高争用用 `LongAdder` |
| 4 | "无锁链表只 CAS next" | 需标记删除 + 内存回收（hazard pointer/epoch） |
| 5 | "自旋不会停" | 高争用下需退避，否则活锁 |
