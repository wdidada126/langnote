# 专篇：ThreadLocal 与内存泄漏

> 对应本书 1.11 节（基本用法）与 11.10 节（泄漏）。
> 这是 **Java 并发里最经典的生产事故**之一，也是虚拟线程时代必须重新审视的机制。

## 一、一句话概括

`ThreadLocal` 是「**每个线程一份独立副本**」的容器，实现为 `Thread` 对象内的一个 `ThreadLocalMap`。
泄漏的根源是：**线程池里的线程永远不销毁，而 `ThreadLocalMap` 的 key 是弱引用、value 是强引用**——
`ThreadLocal` 被 GC 后 key 变 `null`，但 value 仍被强引用，形成「永远访问不到又永远不释放」的内存。

## 二、结构与引用链

```java
// Thread 类内部
class Thread {
    ThreadLocal.ThreadLocalMap threadLocals = null;      // 普通 ThreadLocal
    ThreadLocal.ThreadLocalMap inheritableThreadLocals = null;  // 可继承的
}

static class ThreadLocalMap {
    static class Entry extends WeakReference<ThreadLocal<?>> {   // ⭐ key 是弱引用
        Object value;                                            // ⭐ value 是强引用
    }
    private Entry[] table;
}
```

引用链画图：

```
Thread (强, 线程池里永不销毁)
   └─→ threadLocals: ThreadLocalMap (强)
           └─→ Entry[] table (强)
                   └─→ Entry
                          ├─→ key:   WeakReference<ThreadLocal>  ─弱→  ThreadLocal 对象
                          └─→ value: 强引用 ──────────────────强→  你的对象（如 1MB 的 byte[]）
```

## 三、泄漏是怎么发生的（四步）

```java
void handleRequest() {
    threadLocal.set(new byte[1024 * 1024]);    // 1MB
    // ... 忘了 remove()
}
```

1. 线程池线程 T 执行任务，`ThreadLocalMap` 里加了一条 `Entry(TL → 1MB byte[])`
2. 任务结束，**线程 T 归还线程池，不销毁** → `threadLocals` 还在
3. 某个时刻 `TL` 这个 `ThreadLocal` 变量本身不再被引用（比如是方法内的局部变量，或类被卸载）→ **GC 回收 TL**
4. 于是 `Entry.key` 变成 `null`（弱引用被清理），**但 `Entry.value` 仍强引用着那 1MB**
   → 这 1MB **永远无法通过 `get()` 访问到**（key 是 null 了），**也永远不会被释放**（线程活着）

**每个请求泄漏 1MB × 线程池 200 线程 × 运行几天 = 堆 OOM。**

## 四、JDK 的"补救"及其局限

`ThreadLocalMap` 在 `set()` / `get()` / `remove()` 时**顺带做清理**（`expungeStaleEntry`）：

```java
private int expungeStaleEntry(int staleSlot) {
    Entry e = table[staleSlot];
    e.value = null;              // ⭐ 断开强引用，让 value 可被 GC
    table[staleSlot] = null;
    size--;
    // 并对后续连续段做 rehash 清理...
}
```

**为什么这不够？** 因为清理是**惰性、触发式**的：

- 只有再次访问**同一个 `ThreadLocalMap`** 且**哈希命中附近**时才会清理
- 如果某线程之后**再也不碰任何 `ThreadLocal`**，那条脏 Entry 会一直留到线程死亡
- 线程池线程恰恰符合「长期存活 + 可能不再访问 ThreadLocal」

> **结论：JDK 的清理是"尽力而为"，不是保证。根本解法仍然是显式 `remove()`。**

## 五、正确用法（三条防线）

```java
// ① 必须 remove()，放 finally
try {
    TL.set(ctx);
    doWork();
} finally {
    TL.remove();        // ⭐ 唯一可靠的防御
}

// ② 声明为 static final（避免 ThreadLocal 自身被 GC 导致 key 变 null）
private static final ThreadLocal<Ctx> TL = new ThreadLocal<>();
//  ⚠️ 用 ThreadLocal.withInitial() 更安全：
private static final ThreadLocal<Ctx> TL =
    ThreadLocal.withInitial(() -> new Ctx());

// ③ 不要往里面放大对象；不要放整个 Request/Session
```

> **为什么 `static final` 重要？**
> 如果 `ThreadLocal` 是**实例变量**或**局部变量**，它自己会被 GC → key 变 null → 脏 Entry。
> `static final` 让它与类同生命周期，key 不会变成 null（虽然 value 仍会随线程存活而泄漏，
> 但至少 `get()` 还能访问到、能 `remove()`）。

## 六、`InheritableThreadLocal`：另一个坑

```java
InheritableThreadLocal<String> TL = new InheritableThreadLocal<>();
TL.set("parent-value");
new Thread(() -> System.out.println(TL.get())).start();   // 子线程能看到 "parent-value"
```

**机制**：`Thread` 构造时会把父线程的 `inheritableThreadLocals` **浅拷贝**给子线程。

**四大坑**：

1. **只在线程创建时拷贝一次** —— 父线程之后改值，子线程看不到
2. **线程池下完全失效** —— 线程是预先创建的，拷的是"创建时"的值（通常是 null），且复用线程会**串数据**
3. **浅拷贝** —— 父子共享同一个对象引用，不是深拷贝
4. **异步框架下丢失** —— `CompletableFuture` / Reactor 的线程切换不会传递它

**正解**：用 **Alibaba TransmittableThreadLocal（TTL）** 或 JDK 21+ 的 `ScopedValue`。

## 七、虚拟线程时代：问题被放大，解法也变了

| 维度 | 平台线程 + 线程池 | 虚拟线程 |
| --- | --- | --- |
| 线程数量 | 几百 | **百万级** |
| `ThreadLocal` 内存 | 几百 × 每个 TL 大小 | **百万 × 每个 TL 大小** → 灾难 |
| 泄漏风险 | 高 | **极高** |
| 推荐替代 | `remove()` + `static final` | **`ScopedValue`**（JDK 25 GA） |

### `ScopedValue`（JEP 506，JDK 25 转正）

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

void handle(User user) {
    ScopedValue.where(CURRENT_USER, user).run(() -> {
        // 作用域内可读
        process();                    // 内部可直接 CURRENT_USER.get()
    });
    // ⭐ 退出作用域自动清除，无需 remove，不会泄漏
}
```

对比：

| | `ThreadLocal` | `ScopedValue` |
| --- | --- | --- |
| 可变性 | ✅ `set()` 可改 | ❌ **不可变**（绑定后不能改） |
| 生命周期 | 与线程绑定，需手动清理 | **词法作用域**，自动清除 |
| 继承 | `InheritableThreadLocal`（有坑） | **结构化并发下自动传递** |
| 内存 | 每线程一份 | 更轻量，且自动回收 |
| 虚拟线程友好 | ❌ | ✅ |

> ⚠️ **`ScopedValue` 不是 `ThreadLocal` 的完全替代**：它**不可变**，
> 需要"在作用域内修改值"的场景（如 MDC、计数器）仍需 `ThreadLocal` 或其他方案。

## 八、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 1.2 | `ThreadLocal` 引入 |
| JDK 5 | `ThreadLocal.remove()` 加入（早期版本只有 `set` / `get`，泄漏更严重） |
| JDK 8 | `ThreadLocal.withInitial()`；`ThreadLocalMap` 清理逻辑改进 |
| JDK 21 | 🔴 虚拟线程 GA —— `ThreadLocal` 内存代价放大；`ScopedValue` 孵化（JEP 429） |
| JDK 22-24 | `ScopedValue` 持续预览 |
| **JDK 25** | 🔴 **`ScopedValue` GA**（JEP 506）—— `ThreadLocal` 的现代替代正式可用 |

## 九、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| 线程局部存储的原始概念 | **Butterfield et al., *Thread-Local Storage in Programming Languages*** | 相关讨论见 GCC/ELF 的 TLS 规范；概念出自 1990 年代多线程系统的 ELF TLS 设计 |
| 弱引用的语义 | **Jones et al., *The Garbage Collection Handbook*（第 10 章）** | CRC 2011（第 2 版 2023）—— 弱/软/虚引用的权威说明 |
| 作用域绑定（ScopedValue 的学术前身） | **Najafzadeh, *Structured Concurrency***；另见 **Fluet et al., *Semantics of Future and Anomaly*** | 作用域限定的值绑定在函数式语言（如 Koka、OCaml 的 `let`）中历史悠久 |
| Java 侧的权威规范 | **JEP 506: Scoped Values** | https://openjdk.org/jeps/506 |
| 内存泄漏的实证研究 | 见 [11 章](../11-并发编程实践.md)：Lu et al., ASPLOS 2008 | — |

## 十、近年研究与工业界前沿（2020-2026）

**工业界资料（非同行评审）**

- **Alibaba TransmittableThreadLocal（TTL）**：国内最广泛使用的 `ThreadLocal` 跨线程池传递方案，
  解决了 `InheritableThreadLocal` 在线程池下失效的问题（通过包装 `Runnable`/`Callable` 在提交时快照、执行时恢复）。
  https://github.com/alibaba/transmittable-thread-local
  ⚠️ 它仍有**必须清理**的问题，且对虚拟线程支持需要额外注意。
- **Micrometer Context Propagation / Reactor Context**：响应式框架用自己的 `Context` 而非 `ThreadLocal`，
  因为线程会频繁切换。这是"放弃 ThreadLocal"的一条成熟路线。
- **SLF4J MDC 的 `ThreadLocal` 陷阱**：MDC 底层是 `ThreadLocal`（或 `InheritableThreadLocal`），
  在异步/线程池场景下**链路追踪 ID 会丢失**——这是分布式追踪最常见的"断链"原因。
  解法：TTL 或显式在任务提交时传递 MDC。
- **Spring Security `SecurityContextHolder`**：默认 `MODE_THREADLOCAL`，
  异步方法（`@Async`）里拿不到认证信息，必须配 `MODE_INHERITABLETHREADLOCAL` 或 `DelegatingSecurityContextRunnable`。

## 十一、常见误区（本书 1.11 / 11.10 需修正之处）

1. **❌「用完不 remove 也没事，反正线程会被回收」** —— **线程池线程永不回收**，这是泄漏的直接原因。
2. **❌「JDK 有弱引用就自动安全了」** —— 弱引用的是 **key**，**value 仍是强引用**，这才是泄漏的根源（见第三节）。
3. **⚠️ 必须 `static final`** —— 否则 `ThreadLocal` 自身被 GC 会让 key 变 null，连 `remove()` 的机会都没有。
4. **❌「`InheritableThreadLocal` 能在线程池里传值」** —— **完全不能**，线程是复用的（见第六节）。改用 TTL。
5. **⚠️ `remove()` 必须放 `finally`** —— 异常路径最容易漏。
6. **⚠️ 虚拟线程下优先考虑 `ScopedValue`** —— 百万级虚拟线程 × `ThreadLocal` 是不可接受的。
7. **❌「`ScopedValue` 能完全替代 `ThreadLocal`」** —— 它**不可变**，需要修改值的场景（MDC、计数器）不行。
8. **⚠️ 框架层的 `ThreadLocal` 泄漏你很难发现** —— MDC、Spring Security、各种 TraceContext 都可能泄漏；
   排查手段：heap dump 后看 `Thread.threadLocals` 里哪个 value 占了大量内存。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

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
