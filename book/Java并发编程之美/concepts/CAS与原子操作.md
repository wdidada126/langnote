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
