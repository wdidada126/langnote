# ThreadLocal 与内存泄漏

> **ThreadLocal 的 key 是弱引用、value 是强引用：ThreadLocal 对象本身能被 GC 回收，但 value 仍被线程的 `ThreadLocalMap` 强引用链持有；在线程复用的池化场景中，唯一可靠的释放手段是用完在 `finally` 里 `remove()`。**

## 一、是什么（最小可运行示例）

```java
import java.util.concurrent.*;

public class ThreadLocalDemo {
    static final ThreadLocal<byte[]> BUF =
            ThreadLocal.withInitial(() -> new byte[4 * 1024 * 1024]);   // 每线程一份 4MB 缓冲

    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2);          // 线程长期存活并复用
        for (int i = 0; i < 4; i++) {
            final int id = i;
            pool.execute(() -> {
                byte[] b = BUF.get();
                System.out.printf("%s 拿到缓冲 #%d，首字节=%d%n",
                        Thread.currentThread().getName(), System.identityHashCode(b), b[0]);
                b[0] = (byte) id;                                        // ① 写入本线程副本
                // ② 缺少 BUF.remove()：值一直挂在线程上，且下一个任务会读到上一个任务的残留
            });
        }
        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.SECONDS);
    }
}
```

`BUF` 只有一个实例，但每个线程通过 `Thread.currentThread().threadLocals` 各持一份 `byte[]`：4 个任务落到 2 个线程上，只会看到 2 个不同的 `identityHashCode`，且第 3、4 个任务会读到前面任务写入的 `b[0]` —— 这就是"线程封闭"带来的复用，也是"上下文污染"的根源。

## 二、实现原理（深入一层）

```
Thread (强) → threadLocals : ThreadLocal.ThreadLocalMap
                              └─ table : Entry[]
                                   Entry extends WeakReference<ThreadLocal<?>>
                                        key   → ThreadLocal 实例（弱引用，GC 后变 null）
                                        value → 业务对象（★ 强引用，泄漏点）
```

```java
// java.lang.ThreadLocal$ThreadLocalMap，JDK 8 节选
static class ThreadLocalMap {
    static class Entry extends WeakReference<ThreadLocal<?>> {   // ★ 弱 key
        Object value;                                            // ★ 强 value
        Entry(ThreadLocal<?> k, Object v) { super(k); value = v; }
    }
    private static final int INITIAL_CAPACITY = 16;
    private Entry[] table;
    private int threshold;                                       // 默认 len * 2/3
    private static final int HASH_INCREMENT = 0x61c88647;        // 黄金分割数，散列均匀
}
```

要点：

1. **数据结构不是 `HashMap`**：`ThreadLocalMap` 用**开放地址法 + 线性探测**（冲突后 `index+1` 顺延），装载因子 2/3，扩容翻倍后整体 rehash。
2. **泄漏链条**：`Thread` 活着 → `threadLocals` 活着 → `table[i]` 活着 → `entry.value` 活着。key 被 GC 置 `null` 后，entry 变 "stale entry"，value 却仍在这条强引用链上。
3. **为什么 key 必须是弱引用**：若 key 为强引用，只要线程不死，ThreadLocal 对象（以及它引用的 `Class` → `ClassLoader` → 整个 Web 应用的一堆类）永远无法回收，容器热部署必炸。弱引用是把泄漏范围从"整个类空间"缩小到"value 本身"的折中，**不等于没有泄漏**。
4. **清理时机是被动的**：只有三种情况会调用 `expungeStaleEntry()` 清掉 stale entry —— `set()` 时的 `cleanSomeSlots()`、探测到 stale entry 的 `replaceStaleEntry()`、`getEntry()` 未命中后的 `getEntryAfterMiss()`，以及显式 `remove()`。池化线程长期存活且不再触碰该 ThreadLocal 时，这些路径都不会走到。
5. **两个必备写法**：声明为 `static final`（否则每次 new 出的 ThreadLocal 都会在 GC 后变成 stale key），以及 `try { tl.set(x); ... } finally { tl.remove(); }`。

## 三、JDK 版本演进

| 版本 | 与本主题相关的变化 |
| --- | --- |
| JDK 8 | `ThreadLocal.withInitial()` 出现；`ThreadLocalMap` 弱 key + 惰性清理（本书基线）；`Thread` 的 `threadLocalRandomSeed` 等字段用 `@Contended("tlr")` 隔离 |
| JDK 9 | JEP 193 引入 `VarHandle`，JEP 260 把 `sun.misc.*` 迁到 `jdk.unsupported`；`ThreadLocal` 语义未变，但 JDK 内部开始用 VarHandle 替代 Unsafe 做字段访问 |
| JDK 11 | 无直接变化：`ThreadLocalMap` 仍是弱 key + `cleanSomeSlots` 惰性清理，`remove()` 仍是唯一主动手段 |
| JDK 17 | JEP 403 强封装 JDK 内部；`ThreadLocal` 语义未变，反射改 `threadLocals` 的 hack 开始失效 |
| JDK 21 | 🔴 **JEP 444 虚拟线程转正**：ThreadLocal 对虚拟线程仍可用，但"百万虚拟线程 × 每线程一份副本"会变成 O(线程数) 的内存放大，官方明确建议改用不可变、有作用域的 `ScopedValue`（JEP 446 预览） |
| JDK 25 | 🔴 **JEP 506 ScopedValue 转正**：`ScopedValue.where(...).run(...)` 在作用域结束时自动解绑，值不可变且可被子任务继承，从根上消除了 `ThreadLocal` 的可变性与忘记 remove 的问题 |

## 四、经典论文

| 主题 | 文献（作者, 标题, 会议/期刊 + 年份） | 出处/备注 |
| --- | --- | --- |
| 线程封闭与"局部推理" | O'Hearn, *Resources, Concurrency and Local Reasoning*, Theoretical Computer Science 375(1-3), 2007 | 分离逻辑的奠基综述；"只推理自己拥有的那部分状态"正是 ThreadLocal 有效性的理论依据 |
| 分离逻辑原始论文 | Reynolds, *Separation Logic: A Logic for Shared Mutable Data Structures*, LICS 2002 | 上一行的形式化起点 |
| 别名/所有权约束 | Clarke, Potter & Noble, *Ownership Types for Flexible Alias Protection*, OOPSLA 1998 | 用类型系统保证"对象不被线程外引用"，是线程封闭的类型化版本 |
| 共享可变状态的正确性基线 | Herlihy & Wing, *Linearizability: A Correctness Condition for Concurrent Objects*, TOPLAS 12(3), 1990 | 说明为什么 ThreadLocal 这种"不共享"能直接绕开线性一致的负担 |
| 显示器与结构化并发概念 | Hoare, *Monitors: An Operating System Structuring Concept*, CACM 17(10), 1974 | 与 ScopedValue/StructuredTaskScope 一脉的"结构化"思想源头 |
| 垃圾回收与引用强度 | Jones, Hosking & Moss, *The Garbage Collection Handbook*, CRC 2011 | 教科书（非论文）；弱/软/虚引用语义的权威说明 |

## 五、近年研究与工业界实践（2020-2026）

**同行评审论文**

- ThreadLocal 属于工程实践议题，近年缺乏直接对应的高影响力论文；可参照的相邻工作：
  - Tu, Liu, Song & Zhang, *Understanding Real-World Concurrency Bugs in Go*, ASPLOS 2019 —— 大规模实证显示共享状态（含被复用的上下文）误用是主要 bug 类别，可解释池化场景下 ThreadLocal 污染的高发。（年份略早于 2020，作为基线引用）
  - Gäher, Sammler, Dang, Jung & Dreyer, *RefinedRust: A Refinement Type System for High-Assurance Verification of Rust Programs*, PLDI 2024 —— 在 Rust 侧对"线程局部/所有权封闭"做高保证验证，是局部推理思想的最新工业化。

**工业界资料（非同行评审）**

- [openjdk/jdk](https://github.com/openjdk/jdk)：`java.lang.ThreadLocal`、`ScopedValue` 源码（JDK 25 起在 `java.lang`）；看 `ThreadLocalMap.expungeStaleEntry` 最能理解清理时机。
- [openjdk/jmh](https://github.com/openjdk/jmh)：测 `ThreadLocal.get()` 与 `ScopedValue.get()` 开销差异必须用 JMH，裸 `System.nanoTime()` 循环会被 JIT 优化掉。
- [async-profiler/async-profiler](https://github.com/async-profiler/async-profiler)：`--alloc` 与堆转储定位"大量 `byte[]` 挂在 `Thread.threadLocals` 上"的泄漏。
- [openjdk.org/jeps/0](https://openjdk.org/jeps/0)：JEP 444 / 506 原文，含"为什么虚拟线程不鼓励 ThreadLocal"的官方论述。
- Netty 的 `FastThreadLocal`（`io.netty.util.concurrent`）：用数组索引代替哈希探测规避同类问题，是工业界最著名的替代实现。

## 六、常见误区 / 与其他语言对比

- ❌ **"key 是弱引用，所以不会内存泄漏"** —— 弱引用只保证 `ThreadLocal` 对象可回收，value 仍是强引用；池化线程上不 `remove()` 就会累积。
- ❌ **"线程结束后 value 会自动释放"** —— 只有 `Thread` 对象本身被回收才释放；线程池的核心线程永不结束，`remove()` 才是确定性释放。
- ❌ **"用了 `static final` 就安全"** —— 它只防止 ThreadLocal 实例被反复创建（减少 stale key），不解决 value 的生命周期。
- ⚠️ **`InheritableThreadLocal` 在线程池里是错的** —— 子线程创建时才拷贝一次；池中线程早已创建，既拿不到新父值，又会残留旧值。
- ⚠️ **把 ThreadLocal 当跨层传参的"隐式全局变量"** —— 增大耦合、难以测试；JDK 25 起用 `ScopedValue` 表达"有作用域的只读上下文"。

| 语言 | 等价机制 | 说明 |
| --- | --- | --- |
| Java | `ThreadLocal`（可变、弱 key、需 `remove()`）；JDK 25 `ScopedValue`（不可变、自动解绑） | 唯一同时提供"线程局部"与"作用域局部"两套机制的主流语言 |
| C++ | `thread_local` 关键字（C++11） | 随线程构造/析构，有确定 destructor；无 remove 需求，但不可跨线程继承 |
| Rust | `thread_local!` 宏 + `Cell`/`RefCell` | 类型系统保证不会跨线程共享，编译期即排除污染问题 |
| Go | 语言刻意不提供 goroutine-local storage；用 `sync.Pool` 的 per-P 缓存 | `sync.Pool` 会被 GC 清空且不做身份绑定，明确不适用于上下文传递 |
| Erlang/OTP | 进程字典 `put/erase`（官方不推荐）；进程本身天然隔离 | 无共享内存，不需要线程局部副本 |
| Python | `threading.local()`；异步场景用 `contextvars.ContextVar`（PEP 567） | `ContextVar` 面向 asyncio task 上下文，语义更接近 ScopedValue |
