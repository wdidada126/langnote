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
