# ForkJoin 与工作窃取

> 定位：《Java并发编程之美》第 4 章「Java 并发包中线程池相关类」里 `ForkJoinPool` 是独立一节：它是 JDK 7（JSR 166y，Doug Lea）引入的**分治专用线程池**，用工作窃取（work-stealing）调度大量短小、可递归拆分的 CPU 密集任务；`parallelStream`、`CompletableFuture` 默认池都建立在它之上。

## 一、是什么（最小示例）

`ForkJoinPool` 的执行单元是 `ForkJoinTask`：`RecursiveTask<V>` 有返回值，`RecursiveAction` 无返回值。任务在 `compute()` 里判断"够小就直接算，太大就拆成两个子任务 `fork()`，再 `join()` 汇总"。

```java
class SumTask extends RecursiveTask<Long> {
    static final int THRESHOLD = 10_000;
    final long[] a; final int lo, hi;
    SumTask(long[] a, int lo, int hi) { this.a = a; this.lo = lo; this.hi = hi; }

    protected Long compute() {
        if (hi - lo <= THRESHOLD) {                 // ① 足够小：直接顺序计算
            long s = 0;
            for (int i = lo; i < hi; i++) s += a[i];
            return s;
        }
        int mid = (lo + hi) >>> 1;
        SumTask left  = new SumTask(a, lo, mid);
        SumTask right = new SumTask(a, mid, hi);
        left.fork();                                // ② 左半压入自己队列，异步执行
        long r = right.compute();                   // ③ 右半在当前线程直接算（不要 fork 两边！）
        return left.join() + r;                     // ④ join 拿左半结果，阻塞时去"帮忙偷活"
    }
}
// 使用
long sum = new ForkJoinPool().invoke(new SumTask(arr, 0, arr.length));
// 或：ForkJoinPool.commonPool().invoke(task)；LongStream.range(...).parallel().sum() 内部同理
```

- **`fork()` 不是"开新线程"**：它把任务压入**当前工作线程自己的双端队列**，返回后立刻继续；真正的并行来自"别的空闲线程来偷"。
- **`join()` 不是干等**：等待期间线程会去窃取并执行其他任务（compensation），这是 ForkJoin 与"普通线程池 + 递归 submit"的根本差别，也是它不会因递归层次深而死锁的原因。
- **`invoke()` vs `submit()` vs `execute()`**：`invoke` 同步等待结果（会帮工），`submit` 返回 `ForkJoinTask` 可稍后 `join`，`execute` 纯异步。`invokeAll(a, b)` 是官方推荐的"两个都 fork"写法，内部已做优化，等价于 `b.fork(); a.compute(); b.join()`。
- **只 fork 一边**：`left.fork(); right.fork(); left.join() + right.join()` 是常见反模式——白白多一次队列操作与一次上下文切换，且第二个 `join` 得不到帮工机会。

## 二、实现原理（源码级）

### 工作窃取双端队列（WorkDeque）

```java
// jdk.internal.util / java.util.concurrent.ForkJoinPool.WorkQueue（JDK 8 源码简化）
// 每个工作线程持有自己的 WorkQueue；queue 是循环数组，base/top 用 int（不是 AtomicLong）
void push(ForkJoinTask<?> task) {                       // 本线程自己 → LIFO 压栈（top 端）
    // UNSAFE.putOrderedObject + putOrderedInt(top, s+1)：写延迟，减少缓存争用
}
ForkJoinTask<?> pop() {                                  // 本线程自己取 → 同端 LIFO
    // CAS base/top，同样从 top 端弹出
}
ForkJoinTask<?> poll() { /* 窃取者调用 */ }              // 别的线程偷 → 从 base 端 FIFO
```

- **本地 LIFO、窃取 FIFO**：本地取最新（LIFO）意味着优先跑"刚拆出来的小任务"，深度优先、缓存局部性好、递归栈浅；窃取者从另一端取最老的（FIFO）任务，那通常是**粒度最大、能再拆出活儿**的任务，一次偷走能产生更多子任务，减少后续窃取次数。这一设计出自 Blumofe & Leiserson 1999 的证明。
- **极低争用**：正常情况下每个线程只碰自己的队列，push/pop 用 `putOrderedX`（lazySet，无屏障）而非完整 `volatile` 写；窃取时才 CAS `base`。这正是"核数越多越接近线性加速"的原因。

### 关键机制

| 机制 | 作用 |
| --- | --- |
| `scan()` / 随机窃取 | 空闲线程随机选一个队列（带伪随机数），从 `base` 端偷；找不到就 `awaitWork` 阻塞 |
| 帮工（helping） | `join()` 时若自己的任务没完成，线程去执行队列里别的任务，避免"等死" |
| **补偿线程** | 线程因 `join` 或外部阻塞挂起时，池可能补偿性地激活/新建线程以维持目标并行度 |
| `ManagedBlocker` | 任务里必须阻塞（如 `Phaser.awaitAdvance`、读写锁）时，实现 `ForkJoinPool.ManagedBlocker` 并走 `ForkJoinPool.managedBlock(b)`，让池感知阻塞并补偿线程，`awaitBlocker` 会真正 park |
| **`commonPool()` 并行度** | 默认 `Runtime.availableProcessors() - 1`（留 1 个给主线程）；可用 `-Djava.util.concurrent.ForkJoinPool.common.parallelism=N` 调整 |
| `asyncMode` | 构造参数 `asyncMode=true` 时队列改为 FIFO，适合"事件型"任务（无依赖、不 join），不适合递归分治 |

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 7 | 🔴 **JSR 166y 引入 `ForkJoinPool`**（Doug Lea），`RecursiveTask`/`RecursiveAction`；`sun.misc.Unsafe` 实现无锁队列 |
| JDK 8 | 🔴 **本书基线**：`commonPool()` 静态公共池落地；`parallelStream` 默认跑在它上面；`CompletableFuture` 默认执行器也是它；新增 `CountedCompleter`（完成时触发钩子，适合遍历型任务） |
| JDK 9 | `commonPool()` 对未使用过的场景不再强行初始化；内部 `WorkQueue` 用 `VarHandle` 替代部分 `Unsafe`（JDK 9 起逐步替换） |
| JDK 17-21 | 大量内部重构（队列数组扩容策略、窃取扫描随机化）；`ForkJoinPool` 成为 **虚拟线程默认调度器**（JDK 21，`VirtualThread` 的载体线程由它提供），但虚拟线程任务**不参与**工作窃取队列的 `join` 语义 |
| JDK 21 | 官方建议：CPU 密集并行继续用 `ForkJoinPool`/`parallelStream`；IO 密集不要用（会钉住载体线程），改虚拟线程 |
| JDK 22+ | `Parallel GC`、向量化 API（JEP 460 孵化）等与 ForkJoin 组合用于数据并行；`StructuredTaskScope` 不基于 ForkJoin 的窃取语义 |

## 四、经典论文

| 论文 | 作者 | 会议 / 期刊 | 年份 | 与本篇的关系 |
| --- | --- | --- | --- | --- |
| *Thread Scheduling for Multiprogrammed Multiprocessors* | Nimar S. Arora, Robert D. Blumofe, C. Greg Plaxton | SPAA | 1998 | 提出"处理器数动态变化时"的非阻塞工作窃取调度，给出期望竞争界；是 ABP 窃取的奠基 |
| *Scheduling Multithreaded Computations by Work Stealing* | Robert D. Blumofe, Charles E. Leiserson | Journal of the ACM | 1999 | 🔴 最权威的工作窃取论文：证明 `T_P ≤ T_1/P + O(T_∞)`，并给出"本地 LIFO + 窃取 FIFO"的双端队列设计 |
| *A Java Fork/Join Framework* | Doug Lea | OOPSLA | 2000 | `ForkJoinPool` 的原始设计论文，直接描述 `fork/join`、双端队列与帮工机制 |
| *The Implementation of the Cilk-5 Multithreaded Language* | Matteo Frigo, Charles E. Leiserson, Keith H. Randall | PLDI | 1998 | Cilk 的 `spawn/sync` 与"theft-aware scheduler"，Java ForkJoin 的直接前身 |
| *Cilk: An Efficient Multithreaded Runtime System* | Robert D. Blumofe, Christopher F. Joerg, Bradley C. Kuszmaul, Charles E. Leiserson, Keith H. Randall, Andrew Zhou | Journal of Parallel and Distributed Computing | 1996 | Cilk 运行时总述：工作窃取的双端队列实现与实测加速比数据 |
| *A Dynamic-Sized Nonblocking Work Stealing Deque* | Danny Hendler, Yossi Lev, Mark Moir, Nir Shavit | DISC | 2006 | 可动态扩容的无锁窃取双端队列（Arora–Blumofe–Plaxton deque 的改进版），解释 ForkJoin 队列为何用数组 + CAS 而非链表 |

## 五、近年研究与工业界实践（2020-2026）

| 项目 | GitHub 地址 | 看点 |
| --- | --- | --- |
| OpenJDK jdk | https://github.com/openjdk/jdk | `java/util/concurrent/ForkJoinPool.java`：`WorkQueue`、`scan`/`awaitWork`、补偿线程与 `ManagedBlocker` 的真实实现 |
| **rayon**（Rust） | https://github.com/rayon-rs/rayon | Rust 生态的 fork/join：`par_iter()`、`join(a, b)`、工作窃取调度器；用 `Send`/`Sync` 在编译期保证拆分安全 |
| Go runtime（GMP） | https://github.com/golang/go | `runtime/proc.go` 的 `runqput`/`runqsteal`：每个 P 一个本地运行队列 + 全局队列，窃取时"偷一半"，是 Go 版工作窃取 |
| Intel oneTBB | https://github.com/oneapi-src/oneTBB | C++ 的 `parallel_for`/`task_arena`：基于 task 图的窃取调度，含 partitioner 与亲和性控制，工业级调优样本 |
| OpenCilk | https://github.com/OpenCilk/OpenCilk | Cilk 的现代 LLVM 实现（MIT CSAIL），`cilk_spawn`/`cilk_sync` 与 reducer hyperobject |
| Apache Flink | https://github.com/apache/flink | 算子链内的多线程并行与背压，展示工作窃取在"长任务 + 流"场景下的取舍 |
| Netty | https://github.com/netty/netty | `EventLoopGroup` 按 channel 绑线程（**无窃取**）：与 ForkJoin 形成"亲和性 vs 负载均衡"的正反对照 |
| Tokio | https://github.com/tokio-rs/tokio | Rust 异步运行时的多线程调度器：LIFO slot 优化 + work-stealing，把窃取思想用于 async task |
| ScyllaDB（Seastar） | https://github.com/scylladb/seastar | 反例：完全放弃共享与窃取，改 shard-per-core 无共享架构，说明"窃取不是唯一解" |

**2020 年后的工业共识**：工作窃取是"未知粒度、动态生成的大量短任务"的通用最优解，但在延迟敏感、有 NUMA/缓存亲和性要求或强 IO 的场景下，**分区（sharding）+ 每区一线程**（Seastar/Netty 路线）往往比窃取更可控。

## 六、常见误区 + 跨语言对照

| 误区 | 真相 / 正确做法 |
| --- | --- |
| 用 `ForkJoinPool` 跑 IO / 阻塞任务 | 它是 CPU 密集专用。阻塞会耗尽并行度；必须阻塞时用 `ForkJoinPool.managedBlock(new MyBlocker())` 让池补偿线程，或干脆换独立线程池 |
| 直接改 `commonPool` 的并行度来"提速" | `commonPool` 被 `parallelStream` 与 `CompletableFuture` 共用；改它影响全 JVM。IO 场景应自建 `ExecutorService` |
| 以为 `parallelStream` 一定更快 | 小集合、装箱流、`ArrayList` 之外的源（如 `LinkedList`）、带副作用的 lambda，都可能比串行慢；且它是公共池，一次阻塞影响其他模块 |
| `left.fork(); right.fork(); join(); join();` | 应写 `invokeAll(left, right)` 或 "fork 一个 + compute 一个"，少一次队列往返 |
| 在 `compute()` 里用 `synchronized` / 锁顺序不一致 | 窃取执行会打乱执行顺序，锁顺序不一致极易死锁；ForkJoin 任务应尽量无锁 |
| 阈值（threshold）拍脑袋 | 太小 → 任务数爆炸、调度开销主导；太大 → 负载不均。经验：每任务 1k~10k 次基本运算，再用 JMH 实测 |
| 认为递归越深越并行 | 真正的并行度上限是 `parallelism`（≈核数），拆得再细也不会超过 CPU 核数 |

**跨语言对照**：`ForkJoinPool` ≈ Cilk `spawn/sync`（Blumofe 等，1996）≈ Rust `rayon::join` ≈ Intel TBB `parallel_invoke` ≈ .NET `Parallel.For`（背后是 `ThreadPool` 的 work-stealing，.NET Core 后本地队列改为 LIFO+FIFO 混合）≈ Go 的 GMP 窃取（粒度是 goroutine 而非递归任务）。共同骨架都是：**每线程一私有双端队列 + 本地 LIFO + 窃取 FIFO + 空闲即偷**。
