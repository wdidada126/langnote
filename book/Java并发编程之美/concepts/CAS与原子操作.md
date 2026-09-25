# 专篇：CAS、原子操作与 `sun.misc.Unsafe` 的谢幕

> 对应本书 2.8 / 2.9 节与第 4 章。**CAS 是 JUC 所有无锁结构的原子基石**——
> AQS 的 `state` 更新、`AtomicInteger`、ConcurrentHashMap 的 bin 插入，底层全是它。
> 但本书成书时（JDK 8）重度依赖的 `sun.misc.Unsafe`，在 JDK 23/24 已进入废弃流程。

## 一、一句话概括

**CAS（Compare-And-Set / Compare-And-Swap）** 是一条**硬件原子指令**：
`CAS(V, Expected, New)` —— 若 `V == Expected` 则写入 `New` 并返回成功，否则不动并返回失败。
它是"乐观并发"的基础：**不加锁，靠重试解决冲突**。

## 二、硬件层面到底发生了什么

```java
// java.util.concurrent.atomic.AtomicInteger（JDK 8 语义简化）
public final boolean compareAndSet(int expect, int update) {
    return unsafe.compareAndSwapInt(this, valueOffset, expect, update);
}
```

落到 x86 是一条 **`lock cmpxchg`** 指令：

```asm
; 伪代码
mov eax, expected
lock cmpxchg [mem], new_value    ; lock 前缀：锁总线（或缓存行），保证原子
```

**`lock` 前缀的代价**（这是理解 CAS 性能的关键）：

| 情形 | 代价 |
| --- | --- |
| 无竞争、缓存行已在本地 L1 | 约 **10-20 个时钟周期** |
| 有竞争（缓存行在别的核心） | 缓存一致性协议（MESI）的 RFO 请求，约 **100+ 周期** |
| 跨 NUMA 节点 | 更高 |

> 所以"CAS 一定比锁快"是**错的**：高争用下，CAS 的自旋重试会消耗大量 CPU，
> 而锁会阻塞线程让出 CPU。**低争用 CAS 快，高争用锁更快**。

## 三、CAS 的三大经典问题

### ① ABA 问题

```
线程 T1 读到 V = A
      ↓（T1 被挂起）
线程 T2 把 V 改成 B，又改回 A
      ↓
线程 T1 恢复，CAS(V, A, C) → 成功！但它不知道中间变过
```

**危害**：在基于引用/指针的结构里（如无锁栈），ABA 会导致结构损坏。

**解法：版本号（stamped reference）**：

```java
// JDK 提供 AtomicStampedReference：同时 CAS 引用与版本戳
AtomicStampedReference<Node> ref = new AtomicStampedReference<>(nodeA, 0);
int[] stamp = new int[1];
Node cur = ref.get(stamp);
ref.compareAndSet(cur, nodeC, stamp[0], stamp[0] + 1);   // 版本也参与比较
```

> ⚠️ **Java 里 ABA 的实际危害有限**：因为有 GC，一个被弹出的节点不会被回收后复用地址（不会"地址重用"）。
> 真正被 ABA 咬的是 **C/C++ 的内存回收**——那里需要 hazard pointer / epoch-based reclamation。
> 但在**语义层面**（比如"余额被扣了又加回来"）ABA 依然是 bug。

### ② 自旋开销

```java
// AtomicInteger 的 getAndIncrement（JDK 8）
public final int getAndIncrement() {
    for (;;) {
        int current = get();
        int next = current + 1;
        if (compareAndSet(current, next)) return current;   // 失败就重试
    }
}
```

高争用下这个循环可能转几百次 → CPU 空转。
**`LongAdder` 就是为解决这个问题而生的**（见 [LongAdder与分段累加.md](LongAdder与分段累加.md)）。

### ③ 只能操作一个变量

CAS 只对**单个**变量原子。需要原子地改两个变量时 → 把它们打包成一个对象，用 `AtomicReference`。

## 四、`Unsafe` 的谢幕（本书 2.9 需要重大修正）

本书成书时（JDK 8），JUC 内部与很多高性能库直接使用 `sun.misc.Unsafe`：

```java
// ❌ JDK 8 时代的写法，今天已不应使用
Field f = Unsafe.class.getDeclaredField("theUnsafe");
f.setAccessible(true);
Unsafe unsafe = (Unsafe) f.get(null);
long offset = unsafe.objectFieldOffset(MyClass.class.getDeclaredField("value"));
unsafe.compareAndSwapInt(obj, offset, expect, update);
```

**JDK 的封杀时间线**：

| 版本 | 事件 |
| --- | --- |
| **JDK 9** | 🔴 **JEP 193：引入 `VarHandle`** —— 官方的 `Unsafe` 替代品 |
| JDK 9 | JEP 260 封装内部 API，`Unsafe` 开始被警告 |
| **JDK 17** | 🔴 **JEP 403：强封装 JDK 内部 API** —— 反射访问 `Unsafe` 默认失败 |
| **JDK 23** | 🔴 **JEP 471：标记 `Unsafe` 的内存访问方法为 `for removal`** |
| **JDK 24** | 🔴 **JEP 498：使用这些方法时发出运行时警告** |
| JDK 26+ | 计划移除 |

### `VarHandle`：官方替代（JDK 9+）

```java
private static final VarHandle VALUE;
static {
    try {
        VALUE = MethodHandles.lookup()
            .findVarHandle(MyClass.class, "value", int.class);
    } catch (ReflectiveOperationException e) { throw new ExceptionInInitializerError(e); }
}

VALUE.compareAndSet(obj, expect, update);
VALUE.getAndAdd(obj, 1);
VALUE.setVolatile(obj, 42);
```

**`VarHandle` 比 `volatile` / `Unsafe` 强在哪**：它提供**五档内存语义**，可以按需选择强度：

| 访问模式 | 语义 | 用途 |
| --- | --- | --- |
| `getPlain` / `setPlain` | 普通读写，**无**顺序保证 | 纯单线程数据 |
| `getOpaque` / `setOpaque` | 原子但**无**顺序保证（不与其他变量排序） | 计数器、进度指示 |
| `getAcquire` / `setRelease` | **单向**屏障（acquire 阻止后续重排；release 阻止前面重排） | 发布/消费模式 |
| `getAcquire`/`setRelease` 组合 | 成对的 acquire-release | 锁的实现 |
| **`getVolatile` / `setVolatile`** | **完整 volatile 语义**（双向） | 等价于 volatile 字段 |

> **JDK 内部（含 `ConcurrentLinkedQueue`、`ConcurrentHashMap`）在 JDK 9 后已全面改用 VarHandle**，
> 且大量使用 `opaque` / `release` 而非 `volatile`——性能更好。

**⚠️ 本书 2.9 节的 `Unsafe` 示例代码在今天已经无法直接运行**（JDK 17+ 反射受限，JDK 24+ 有警告）。
阅读时请替换为 `VarHandle`。

## 五、`AtomicXxx` 家族与选型

| 类 | 用途 | 备注 |
| --- | --- | --- |
| `AtomicInteger` / `AtomicLong` / `AtomicBoolean` | 单变量原子更新 | 低争用首选 |
| `AtomicReference<V>` | 对象引用原子更新 | 打包多字段 |
| `AtomicStampedReference<V>` | 带版本戳，解 ABA | 版本号单调递增 |
| `AtomicMarkableReference<V>` | 带 boolean 标记 | 轻量版戳 |
| **`LongAdder` / `DoubleAdder`** | **高争用累加** | 见 [LongAdder与分段累加.md](LongAdder与分段累加.md) |
| `LongAccumulator` | 自定义累加函数 | `new LongAccumulator(Long::max, 0)` 求最大值 |
| `AtomicIntegerFieldUpdater` | 原子更新对象的 volatile 字段 | 省一个对象头，用于大量实例 |

**JDK 8 的 `getAndUpdate` / `updateAndGet` / `accumulateAndGet`**：

```java
// 老写法要自己写循环
while (true) { int c = ai.get(); if (ai.compareAndSet(c, f(c))) break; }

// JDK 8+ 一行
ai.updateAndGet(x -> Math.max(x, 100));
ai.accumulateAndGet(x, (a, b) -> a * b);
```

## 六、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 5 | `AtomicXxx` 系列、`Unsafe.compareAndSwapXxx` |
| JDK 8 | `LongAdder`、`LongAccumulator`、`getAndUpdate`/`updateAndGet`、`StampedLock` |
| **JDK 9** | 🔴 **`VarHandle`（JEP 193）**；JUC 内部 `Unsafe` → VarHandle；`Thread.onSpinWait()` |
| JDK 15 | `AtomicReference` 等增加 `compareAndExchange`（返回旧值而非 boolean） |
| JDK 17 | JEP 403 强封装 |
| JDK 21 | 虚拟线程（不影响 CAS 语义）；`ScopedValue` |
| **JDK 23/24** | 🔴 **`Unsafe` 内存访问方法 for removal（JEP 471/498）** |

## 七、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| **CAS 的原始出处** | **IBM System/370 `Compare and Swap` 指令** | IBM 1970 年代；作为同步原语的讨论见 **Herlihy, *Wait-Free Synchronization*, TOPLAS 13(1), 1991** |
| **无锁同步的理论基础** | **Herlihy, *Wait-Free Synchronization*** | **ACM TOPLAS 13(1), 1991** —— 证明 CAS 的**共识数（consensus number）为 ∞**，即能实现任意对象的无锁同步 |
| 共识层级 | **Herlihy, *Wait-Free Synchronization*** 中的 consensus hierarchy | 同上；CAS 位于最高层，而 `test-and-set`、`fetch-and-add` 只有 2 |
| 线性一致性 | Herlihy & Wing, *Linearizability* | TOPLAS 12(3), 1990 |
| ABA 与安全内存回收 | **Michael, *Safe Memory Reclamation for Dynamic Lock-Free Objects Using Hazard Pointers*** | IEEE TPDS 15(6), 2004 |
| 非阻塞算法的实证 | Michael & Scott, PODC 1996 | 见 [Michael-Scott无锁队列.md](Michael-Scott无锁队列.md) |
| 事务内存（替代路线） | Herlihy & Moss, *Transactional Memory: Architectural Support for Lock-Free Data Structures* | ISCA 1993 |
| 无锁算法教材 | Herlihy & Shavit, *The Art of Multiprocessor Programming* | 2008/2012，第 5-6 章讲共识与 CAS |

> **Herlihy 1991 的 consensus hierarchy 是理解 CAS 为什么"万能"的关键**：
> `test-and-set` 的共识数是 2（只能让 2 个线程达成一致），`compare-and-swap` 是 ∞（任意多线程）。
> 这解释了为什么所有通用无锁结构最终都建立在 CAS 上。

## 八、近年研究与工业界前沿（2020-2026）

**同行评审论文**

- **安全内存回收（SMR）仍是活跃方向**：hazard pointers、epoch-based reclamation、以及 2020 年后提出的
  自动化/混合方案，持续出现在 PPoPP / PLDI / SPAA。Java 因为有 GC 天然不需要显式 SMR，
  这是托管语言的显著优势（见 [Michael-Scott无锁队列.md](Michael-Scott无锁队列.md)）。
- **硬件事务内存（HTM）的兴衰**：Intel TSX 曾被视为 CAS 的接班人，但因安全漏洞（TAA/ZombieLoad）
  在多代 CPU 上被禁用。2020 年后学术兴趣转向"受限事务内存"与软件回退路径的设计。

**工业界资料（非同行评审）**

- **JCTools / Agrona**：高性能无锁队列，内部大量使用 `VarHandle` 与缓存行填充，是"JDK 之外的最强实践"。
  https://github.com/JCTools/JCTools
- **LMAX Disruptor**：RingBuffer + 缓存填充 + 序列号 CAS，是 CAS 在工业级低延迟场景的巅峰用法。
  https://github.com/LMAX-Exchange/disruptor
- **OpenJDK `jmh`**：**测 CAS vs 锁的唯一可信方式**。裸循环测出来的结论基本都是错的（JIT 会消除死代码、预热不足）。
  https://github.com/openjdk/jmh
- **JOL（Java Object Layout）**：看 `AtomicInteger` 的对象布局。https://github.com/openjdk/jol

## 九、常见误区（本书 2.8 / 2.9 / 2.12 需修正之处）

1. **❌「CAS 一定比锁快」** —— 高争用下自旋会烧 CPU，锁会阻塞让出 CPU。**低争用用 CAS，高争用用锁或 `LongAdder`。**
2. **❌「CAS 没有 ABA 问题，因为 Java 有 GC」** —— GC 只防止**地址重用**，语义层面的 ABA 依然存在。
   需要时用 `AtomicStampedReference`。
3. **⚠️ 本书的 `Unsafe` 示例代码在今天已无法直接运行** —— JDK 17+ 反射受限，JDK 23/24 标记废弃。
   **改用 `VarHandle`**（见第四节）。
4. **❌「volatile + CAS 就够实现原子操作了」** —— 需要 `AtomicXxx` 或 VarHandle 提供**真正的原子性**，
   volatile 只保证可见性。
5. **⚠️ `AtomicInteger` 在高争用下是性能杀手** —— 所有线程 CAS 同一个 `value` 字段，缓存行疯狂 ping-pong。
   用 **`LongAdder`**（分段）。
6. **⚠️ 伪共享会让 `AtomicLong` 慢一个数量级** —— 见 [伪共享FalseSharing.md](伪共享FalseSharing.md)。
7. **❌「`LongAdder` 可以完全替代 `AtomicLong`」** —— `LongAdder` 的 `sum()` **不是原子的**（并发更新下读到的是瞬时值），
   需要精确快照的场景仍用 `AtomicLong`。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

# CAS 与原子操作

> **CAS（Compare-And-Swap）是一条"读-改-写"的硬件原子指令（`lock cmpxchg`），Java 用它实现乐观锁式无阻塞更新；它不阻塞线程，但存在 ABA、自旋空耗与单热点争用三类固有代价。**

## 一、是什么（最小可运行示例）

```java
import java.util.concurrent.atomic.AtomicInteger;

public class CasDemo {
    static final AtomicInteger N = new AtomicInteger(0);

    public static void main(String[] args) throws Exception {
        // ① incrementAndGet() 的语义等价于这段手写自旋，JDK 内部就是这样实现的
        Runnable spin = () -> {
            for (int i = 0; i < 250_000; i++) {
                for (;;) {
                    int cur = N.get();                       // 读当前值
                    int next = cur + 1;                      // 算出新值
                    if (N.compareAndSet(cur, next)) break;   // 期间没被别人改过 → 成功；否则重试
                }
            }
        };
        Thread[] ts = new Thread[4];
        for (int i = 0; i < ts.length; i++) ts[i] = new Thread(spin);
        for (Thread t : ts) t.start();
        for (Thread t : ts) t.join();
        System.out.println("N=" + N.get());                  // 恒为 1000000
    }
}
```

核心是 `compareAndSet(expected, update)`：只有当变量当前值仍等于 `expected` 时才写入，**失败不会挂起线程，而是让调用方自选重试、放弃或走慢路径** —— 这就是"乐观"与 `synchronized` 的"悲观阻塞"的根本区别。

## 二、实现原理（深入一层）

```java
// JDK 8：AtomicInteger 底层（本书基线）
public final boolean compareAndSet(int expect, int update) {
    return unsafe.compareAndSwapInt(this, valueOffset, expect, update);   // native → lock cmpxchg
}
// JDK 9+：改写为 VarHandle，语义一致，并被标记 @HotSpotIntrinsicCandidate
private static final VarHandle VALUE;                                     // 见 java.util.concurrent.atomic
public final boolean compareAndSet(int expect, int update) {
    return VALUE.compareAndSet(this, expect, update);                     // C2 内联为一条指令
}
```

- **硬件**：x86 上 C2 把 `compareAndSet` 编译为带 `lock` 前缀的 `cmpxchg`；`getAndAdd`/`incrementAndGet` 直接编译为 `lock xadd`（比 CAS 循环更快）。`lock` 前缀锁定缓存行（现代 CPU 用缓存锁定而非总线锁定），并保证全序与可见性。
- **弱 CAS**：`weakCompareAndSet`/`compareAndExchange` 在 LL/SC 架构（ARM、POWER）上允许**伪失败**，必须放循环里；x86 上它与强版本代码相同。
- **ABA 问题**：值从 A→B→A 时 CAS 误判"没变过"。解法是加版本戳（`AtomicStampedReference`）或标记位（`AtomicMarkableReference`），或在 GC 语言里依赖"节点不会被复用的地址"规避；更系统的方案是 Hazard Pointer / 基于 epoch 的回收。
- **代价模型**：CAS 是"竞争即失败"。N 个线程打同一热点，每轮只有 1 个成功 → O(N) 次重试 + 缓存行乒乓 → 吞吐随线程数上升反而下降；这就是 `LongAdder` 用分段（`Cell[]`）分散热点的原因。
- **与锁的边界**：临界区长/竞争激烈时，自旋的 CPU 空耗远大于一次阻塞唤醒；`synchronized` 在 JDK 6 后已有自适应自旋、锁粗化等优化，因此"无锁一定更快"是错的。

## 三、JDK 版本演进

| 版本 | 与本主题相关的变化 |
| --- | --- |
| JDK 8 | `sun.misc.Unsafe.compareAndSwapInt/Long/Object`（本书基线）；新增 `LongAdder`/`LongAccumulator`（CAS 分段）；`StampedLock` 也基于 CAS |
| JDK 9 | 🔴 **JEP 193 VarHandle**：`compareAndSet` / `weakCompareAndSet` / `compareAndExchange` / `getAndAdd` / `getAndUpdate` 统一 API；`java.util.concurrent.atomic` 整体改写为 VarHandle，并被 C2 内建为单条指令 |
| JDK 11 | 无语义变化；`AtomicInteger` 新增更明确的 `accumulateAndGet` 等 lambda 形式（部分在 JDK 8 已有） |
| JDK 15 | 🔴 **JEP 374 废弃并默认关闭偏向锁**：无竞争同步不再"几乎免费"，促使热点代码更多转向 CAS / 无锁结构与 `LongAdder` |
| JDK 17 | JEP 403 强封装 JDK 内部，直接反射 `Unsafe` 开始受限；`Atomic*` 不受影响 |
| JDK 21 | 🔴 **JEP 444 虚拟线程**：CAS 语义不变，但百万虚拟线程打同一个 `AtomicLong` 会极度放大热点争用；同时虚拟线程内 `synchronized` 会钉住载体线程，促使部分库改用基于 CAS 的 `ReentrantLock` |
| JDK 23 / 24 | 🔴 **JEP 471 / JEP 498**：`sun.misc.Unsafe` 的内存访问方法（含三个 CAS）逐步废弃，JDK 24 起首次使用即告警；新代码一律用 `VarHandle` 或 `Atomic*` |
| JDK 25 | 🔴 **JEP 506 ScopedValue 转正**（不涉及 CAS）；至此 `VarHandle` 是公共 API 中唯一的 CAS 通道 |

## 四、经典论文

| 主题 | 文献（作者, 标题, 会议/期刊 + 年份） | 出处/备注 |
| --- | --- | --- |
| 无锁可行性边界 | Herlihy, *Wait-Free Synchronization*, TOPLAS 13(1), 1991 | 证明 CAS 类原语的**共识数**为 ∞（可无等待实现任意对象），锁则不能 |
| 线性一致性定义 | Herlihy & Wing, *Linearizability: A Correctness Condition for Concurrent Objects*, TOPLAS 12(3), 1990 | CAS 成功点即线性化点，是判断无锁算法正确性的标尺 |
| 经典无锁数据结构 | Michael & Scott, *Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms*, PODC 1996 | `ConcurrentLinkedQueue` 的直接原型 |
| 无锁栈（CAS 教科书案例） | Treiber, *Systems Programming: Coping with Parallelism*, IBM Almaden Research Center, RJ 5118, 1986 | 技术报告（非论文），Treiber Stack 出处，也是 ABA 问题最常被引用的例子 |
| ABA / 版本化回收 | Herlihy, Luchangco, Martin & Moir, *The Repeat Offender Problem: A Mechanism for Supporting Dynamic-Sized Lock-Free Data Structures*, DISC 2002 | 用"双重比较单交换 + 版本号"解决 CAS 复用问题 |
| 安全内存回收 | Michael, *Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects*, IEEE TPDS 15(6), 2004 | ABA 之外无锁算法的另一半难题 |
| Java 侧的工程落地 | Herlihy & Shavit, *The Art of Multiprocessor Programming*, 2008/2012 | 教科书（非论文），Ch.5-11 系统讲 CAS 与无锁栈/队列 |
| AQS（CAS 驱动阻塞锁） | Lea, *The java.util.concurrent Synchronizer Framework*, Science of Computer Programming 58(3), 2005 | `ReentrantLock`/`CountDownLatch` 的 CAS 状态机设计论文 |

## 五、近年研究与工业界实践（2020-2026）

**同行评审论文**

- Friedman, Ben-Baruch & Hendler, *NVTraverse: In the Fast Lane of Traversing Semi-Persistent Trees*, PPoPP 2021 —— 把 CAS 无锁遍历搬到持久内存，讨论失败原子性与 CAS 在 NVM 上的额外代价。
- Tu, Liu, Song & Zhang, *Understanding Real-World Concurrency Bugs in Go*, ASPLOS 2019 —— 实证表明"误以为原子操作能保护复合逻辑"是常见 bug 成因（年份略早于 2020，作为基线引用）。
- Gäher, Sammler, Dang, Jung & Dreyer, *RefinedRust: A Refinement Type System for High-Assurance Verification of Rust Programs*, PLDI 2024 —— 对 Rust 侧 `compare_exchange` 弱/强语义做高保证验证，反映工业界对 CAS 内存序正确性的形式化需求。

**工业界资料（非同行评审）**

- [openjdk/jdk](https://github.com/openjdk/jdk)：`java.util.concurrent.atomic`、`Striped64`（`LongAdder` 的 CAS 分段实现）、`AbstractQueuedSynchronizer`（CAS 状态机）。
- [JCTools/JCTools](https://github.com/JCTools/JCTools)：无锁队列/栈集合，含针对 x86 优化的单生产者单消费者队列与填充策略，是 `java.util.concurrent` 之外的高性能补充。
- [openjdk/jcstress](https://github.com/openjdk/jcstress)：验证 CAS 与原子类的内存序契约。
- [openjdk/jmh](https://github.com/openjdk/jmh)：`AtomicLong` vs `LongAdder` vs `VarHandle.getAndAdd` 的可靠对比基准。
- [LMAX-Exchange/disruptor](https://github.com/LMAX-Exchange/disruptor)：用 CAS 申请序号 + 内存屏障发布替代锁，是 CAS 低延迟设计的代表作。

## 六、常见误区 / 与其他语言对比

- ❌ **"无锁（lock-free）一定比锁快"** —— 高争用下 CAS 成功率约 1/N，自旋烧 CPU；临界区长时用锁更优，应按 JMH 实测选择。
- ❌ **"AtomicInteger 能替代所有同步"** —— 它只保护**一个变量**的原子更新；多个变量的组合不变式仍需锁或事务式结构。
- ❌ **"`compareAndSet` 循环里不用重读当前值"** —— 自旋必须每次重新 `get()`，用旧值重试会死循环或覆盖他人写入。
- ❌ **"CAS 没有 ABA 问题"** —— 有；涉及指针复用/节点回收时要用 `AtomicStampedReference` 或 hazard pointer。
- ⚠️ **`weakCompareAndSet` 语义易被误解** —— 允许伪失败，JDK 9 起建议用语义明确的 `weakCompareAndSetPlain/Volatile/Acquire/Release` 或 `compareAndExchange`。
- ⚠️ **本书源码基于 JDK 8 的 `Unsafe.compareAndSwapXxx`** —— 从 JDK 9 起读 OpenJDK 会看到 VarHandle 版本，语义一致但代码不同。

| 语言 | CAS 的等价物 | 说明 |
| --- | --- | --- |
| Java | `VarHandle.compareAndSet` / `AtomicInteger.compareAndSet` (JDK 9+ 底层 VarHandle，C2 内建为 `lock cmpxchg`) | 提供强/弱两版及 `compareAndExchange`（返回实际旧值，便于无循环使用） |
| C++ | `std::atomic<T>::compare_exchange_weak/strong` + `memory_order` | `weak` 版在 LL/SC 上可能伪失败，必须放循环；可指定 success/failure 两种内存序 |
| Rust | `AtomicUsize::compare_exchange` / `compare_exchange_weak` | 与 C++ 同构，但由类型系统强制指定 `Ordering`，不会遗漏 |
| Go | `sync/atomic` 的 `CompareAndSwapInt64`，Go 1.19+ 类型化为 `atomic.Int64.CompareAndSwap` | 仅提供顺序一致语义，无弱/强与内存序分级 |
| Erlang/OTP | 无 CAS 原语；用 `ets:update_counter` 等原子计数或把写操作串行到单个进程 | 靠"进程邮箱串行化"而非硬件原子指令 |
| Python | 无 CAS；CPython 靠 GIL + `Lock`；跨进程用 `multiprocessing.Value(lock=True)` | GIL 使单变量自增实际上被解释器串行化，但这不是可移植保证 |
