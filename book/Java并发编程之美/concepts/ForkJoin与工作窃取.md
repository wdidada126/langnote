# 专篇：ForkJoinPool、工作窃取与"分治并行"的边界

> 对应本书第 8 章（线程池）的**邻居**，也是全书**没有正面讲**的一块。
> 更重要：`Executors.newWorkStealingPool()`、`parallelStream()`、`CompletableFuture`
> 的默认池，全都长在 ForkJoinPool 上——**你没显式用它，它也在为你工作**。

## 一、本章地图

```
为什么普通线程池跑不动"递归分治"任务？（任务会派生子任务并等待子任务）
        ↓
Fork/Join 框架三件套：ForkJoinPool + ForkJoinTask(RecursiveTask/RecursiveAction) + WorkQueue
        ↓
核心：工作窃取（Work-Stealing）与双端队列（ Chase-Lev deque ）
        ↓
三个易忽略的机制：join 时"帮忙执行"、LIFO/FIFO 的取任务方向差、外部提交走 submit 队列
        ↓
parallelStream 与 commonPool 的共享灾难
        ↓
虚拟线程时代：ForkJoinPool 还是 CPU 密集并行的答案吗？
```

## 二、为什么普通线程池跑不动递归分治

```java
// 用普通线程池做归并排序/斐波那契/树遍历，会死锁或吞吐崩掉
ExecutorService pool = Executors.newFixedThreadPool(4);
pool.submit(() -> {
    var left  = pool.submit(subTask1);
    var right = pool.submit(subTask2);
    left.get(); right.get();     // ← 工作线程阻塞等子任务
});
```

**死锁机理**：线程 A 执行的父任务阻塞等子任务，子任务排在队列里等空闲线程。
当**所有线程都在等子任务**且队列里有子任务时 → **线程饥饿死锁（thread starvation deadlock）**。
固定大小的池 + 父子依赖 = 必然出问题（除非池无界，那就失去意义）。

ForkJoinPool 的解法：**等待中的线程不空转，去偷别人的活干**。

## 三、核心数据结构：工作窃取双端队列

```
   Worker-1 (deque)                  Worker-2 (deque)
  ┌────────────────┐                ┌────────────────┐
  │base→           │←top            │base→           │←top
  │ [t1][t2][t3]   │                │ (empty)        │
  └────────────────┘                └────────────────┘
        ↑                                    │
        └──────── 窃取（steal）──────────────┘
                 从 base 端偷（FIFO）
  自己从 top 端取（LIFO）
```

| 角色 | 操作端 | 顺序 | 并发程度 |
| --- | --- | --- | --- |
| **队列所有者** | `top`（push/pop） | **LIFO** | 无竞争，通常只需普通读写 + 偶发 CAS |
| **窃取者** | `base`（take/steal） | **FIFO** | 需要 CAS（多窃取者竞争 base） |

**为什么自己用 LIFO、别人偷 FIFO？**

- **LIFO 保证局部性**：分治任务里"最后派生的子任务"通常工作集最小、最可能命中缓存 → 先做它，减少内存占用，也让大任务尽早下沉给别人偷。
- **FIFO 保证窃取到"大块任务"**：`base` 端是最早派生的、通常是**最大的**子任务 → 偷一次能干很久，**减少窃取次数**（窃取本身有同步开销）。
- 结果：窃取次数是 **O(P × log n)** 量级，这是 Blumofe-Leiserson 理论界的界。

> 这个结构就是 **Chase-Lev 双端队列**（见第九节论文）。Java 的 `ForkJoinPool.WorkQueue`
> 用的正是它的变体，数组按 2 的幂扩容，`base`/`top` 是 `volatile int`。

## 四、三个容易被忽略的机制

### 1. `join()` 时不阻塞，而是"帮忙干活"（helping / compensating）

```java
left.fork();
right.compute();      // 自己算一个，而不是 fork 两个再 join
left.join();          // 等另一个；此时**不是 sleep**，而是尝试执行队列里的其他任务
```

- `ForkJoinTask.join()` 内部调用 `doJoin()` → 若未完成，线程会尝试 `tryHelpJoin` / 执行本地队列任务；
- 若实在无事可做，`ForkJoinPool` 会**补偿创建**新线程（`tryCompensate`）以保持目标并行度，避免"全都在等"导致吞吐塌方。

> **这条解释了为什么 ForkJoinPool 不会像 `FixedThreadPool` 那样死锁**——但前提是
> **任务必须通过 `fork()/join()` 表达依赖**。若你在 ForkJoinTask 里自己 `Thread.sleep()`
> 或阻塞在外部 `Future.get()`，框架**不知道**你在等什么，照样死锁/饿死。

### 2. 提交路径分两种：内部 `fork` vs 外部 `submit`

| 提交方式 | 进入哪个队列 | 公平性 |
| --- | --- | --- |
| 任务内部 `fork()` | 该 worker 自己的 deque | 无 |
| 外部线程 `pool.submit()/invoke()` | **共享的 submission 队列**（随机或轮询选一个 WorkQueue） | FIFO，较公平 |

所以从外部一次性提交 1000 个小任务，它们会**轮流分散**到各 worker 队列；
但如果全部由 `fork()` 递归派生，就可能出现负载不均（靠窃取兜底）。

### 3. `commonPool` 与并行度

- 默认并行度 = `Runtime.availableProcessors() - 1`（**减 1**，给主线程留一个核）；
- 可用 `-Djava.util.concurrent.ForkJoinPool.common.parallelism=N` 调整；
- `parallelStream()`、`CompletableFuture` 的默认 Async **共享这一个池**。

## 五、`parallelStream` 的五大陷阱

```java
list.parallelStream().forEach(...);   // 看起来很美
```

| # | 陷阱 | 说明 |
| --- | --- | --- |
| 1 | **共享 commonPool** | 一个慢/阻塞任务拖垮整个 JVM 里所有 `parallelStream` 与 CF 默认异步 |
| 2 | **阻塞 I/O 会饿死池** | ForkJoinPool 不补偿阻塞（它只补偿"等待 fork/join 依赖"） |
| 3 | **不一定更快** | 拆箱/装箱、`ArrayList` 可分割性好，`LinkedList`/`Iterator` 源几乎无法并行（需先物化成数组，有拷贝成本） |
| 4 | **顺序语义丢失** | `forEach` 无序，`forEachOrdered` 有同步开销；`Collectors.toMap` 合并有代价 |
| 5 | **容器内 CPU 配额失真** | JVM 早期版本读的是**物理核数**而非 cgroup 配额，8u191+ / JDK 10+ 才正确识别容器限制 |

> **`ArrayList` vs `LinkedList` 的分割性能差**是 `Spliterator` 的关键：
> `ArrayListSpliterator` 二分即可 O(1) 分割；`LinkedList` 的分割需要遍历，代价 O(n)。

## 六、正确用法清单

| 场景 | 建议 |
| --- | --- |
| CPU 密集 + 可递归分治（排序、遍历、矩阵、归并） | ✅ `ForkJoinPool` / `RecursiveTask` + **阈值 cutoff** |
| CPU 密集 + 数据并行（map/reduce/filter） | ✅ `parallelStream`，但**自建池**跑（用 `pool.submit(() -> stream.parallel()...)` 的方式隔离） |
| **阻塞 I/O** | ❌ 不要用 ForkJoinPool；用固定池，或 JDK 21+ **虚拟线程** |
| 需要保证顺序/副作用 | ❌ 别并行 |
| 小集合（< 万级） | ❌ 拆分与窃取开销 > 收益 |

```java
// 阈值是性能的关键：太小→任务过多；太大→负载不均
static final int THRESHOLD = 10_000;
if (hi - lo <= THRESHOLD) { computeDirectly(); return; }
```

## 七、虚拟线程时代还要不要 ForkJoinPool？

**结论：分工变清晰了。**

| 维度 | 虚拟线程（JEP 444） | ForkJoinPool |
| --- | --- | --- |
| 目标负载 | **阻塞 I/O**（等待时不占 OS 线程） | **CPU 密集**（窃取保证核饱和） |
| 调度单位 | 虚拟线程 → 载体线程（ForkJoinPool 作为默认调度器） | 任务 → worker 线程 |
| 数量级 | 百万级 | 核数级（十几个） |
| 阻塞代价 | 近乎免费 | 灾难（不补偿） |

> 有趣的一点：**虚拟线程的默认调度器本身就是 `ForkJoinPool`**（JDK 21 起），
> 只是它工作在 **asyncMode = true** 模式（FIFO，无窃取栈），并且能感知虚拟线程的 mount/unmount 来补偿线程。
> 这说明 ForkJoinPool 并没有被取代，而是**换了个岗位**。

## 八、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Chase, D. & Lev, Y. 2005. "Dynamic Circular Work-Stealing Deque." SPAA '05, pp. 21-28.** | **Java `ForkJoinPool.WorkQueue` 的直接原型**；证明了 owner 端可无锁（除扩容）、steal 端单点 CAS 的正确性 |
| **Blumofe, R. D. & Leiserson, C. E. 1999. "Scheduling Multithreaded Computations by Work Stealing." JACM 46(5): 720-748.** | 工作窃取的**理论基础**：给出期望空间 O(S₁×P)、期望通信 O(P×S_max×T_∞) 的界；证明"贪心调度"最优到常数因子 |
| **Blumofe, R. D., Joerg, C. F., Kuszmaul, B. C., Leiserson, C. E., Randall, K. H., Zhou, Y. 1995. "Cilk: An Efficient Multithreaded Runtime System." PPoPP '95.** | Cilk 的 `spawn/sync` 与 work-stealing 调度器，Fork/Join 框架的**直系祖先**；Doug Lea 的 JSR 166 设计说明明确引用 Cilk |
| **Frigo, M., Leiserson, C. E., Randall, K. H. 1998. "The Implementation of the Cilk-5 Multithreaded Language." PLDI '98.** | "work-first" 原则与 THE protocol（双端窃取的实现细节） |
| **Arora, N. S., Blumofe, R. D., Plaxton, C. G. 1998. "Thread Scheduling for Multiprogrammed Multiprocessors." SPAA '98.** | **非阻塞式**工作窃取（避免窃取失败时的忙等），Java ForkJoinPool 的 `awaitWork`/补偿机制受此影响 |
| **Leiserson, C. E. 2009. "The Cilk++ Concurrency Platform." / 教材《Structured Parallel Programming》(McCool, Robison, Reinders 2012)** | 从 Cilk 到 TBB/并行编程模型的工程化总结 |
| **Lê, N. M., Pop, A., Cohen, A., Zappa Nardelli, F. 2013. "Correct and Efficient Work-Stealing for Weak Memory Models." PPoPP '13.** | **关键**：在 C11/Java 这类弱内存模型下，Chase-Lev deque 的朴素实现**是错的**，需要额外的 fence；Java 实现里 `base`/`top` 都是 `volatile` 正是为此 |
| **Doug Lea, "A Java Fork/Join Framework"（2000, ACM Java Grande / ISCOPE Conference）** | Java 版框架的第一篇设计论文，**权威来源**（jsr166 站可下载） |

## 九、近年研究与工业界前沿

### 近年研究（工作窃取的持续演进）

- **弱内存模型下的正确性**（上表 Lê 等 PPoPP'13）已成该领域标准关注点；后续工作（包括 Chase-Lev deque 在 ARM/POWER 上的 fence 放置）持续有 PPoPP/PLDI 论文。
- **NUMA 感知的窃取**：多插槽服务器上"偷跨节点"代价高，近年研究偏向层次化（hierarchical）窃取 + 任务亲和性。
- **与协程/虚拟线程结合的调度**：把"阻塞让出"与"窃取"统一在一个调度器里（JDK 21 的虚拟线程调度器即工业界答案）。
- **确定性并行**：Cilk 的另一条遗产是"并行程序的串行语义等价"（deterministic race detection，如 Cilktools/Cilksan），近年与结构化并发思想汇合。

### 工业界开源实现

| 项目 | Stars | 语言 | 说明 |
| --- | --- | --- | --- |
| **rayon-rs/rayon** | 13.3k | Rust | **Rust 的 Fork/Join 事实标准**；`par_iter()` = Rust 版 parallelStream；同样基于 Chase-Lev 窃取（其内部 `rayon-core` 的 `Worker` 就是 CL deque） |
| **openjdk/jdk** | 23.4k | Java | `ForkJoinPool.java`（约 3000 行，注释极详）、`ForkJoinTask.java`、`Spliterators.java` |
| Intel oneTBB（`oneapi-src/oneTBB`） | — | C++ | `parallel_for` / `task_group`，Cilk 精神在工业界的主力延续 |
| Go runtime `runtime/proc.go` | — | Go | goroutine 的 **P/M/G** 调度器同样是工作窃取（每个 P 一个本地 runq，全局 runq + `stealWork`，Vyukov 2012 设计文档） |
| Tokio（`tokio-rs/tokio`） | — | Rust | 多调度线程 + 本地队列窃取的 async runtime |

> **跨语言对照小结**：Cilk → Java ForkJoinPool → TBB → Rayon → Go/Tokio 调度器，
> 全都用同一套 Chase-Lev 双端队列。看懂一次，五处通用。

## 十、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "ForkJoinPool 就是线程池的一种，随便用" | 它是**为 CPU 密集分治任务**设计的；放阻塞 I/O 会饿死且不补偿 |
| 2 | "`parallelStream` 一定更快" | 小于万级数据、链表源、有装箱/有顺序要求时，**更慢** |
| 3 | "`fork()` 越多越并行" | 必须设**阈值 cutoff**；任务粒度太小会被拆分开销淹没 |
| 4 | "在 RecursiveTask 里调用 `Thread.sleep()` 没问题" | 框架无法感知，等同阻塞，会导致吞吐塌方 |
| 5 | "`commonPool` 是私有的" | 全 JVM 共享，且被 `parallelStream` 与 CF 默认异步共用 |
| 6 | "递归里 `fork()` 两个再 `join()` 两个" | **反模式**。应 `fork()` 一个、`compute()` 一个、`join()` 一个，少一次入队且天然负载均衡 |
| 7 | "`invokeAll(a, b)` 只是语法糖" | 它有专门的优化（只 fork 除最后一个外的任务，其余本地执行），优于手写循环 fork |
| 8 | "并行度 = CPU 核数" | 默认 **`核数 - 1`**；且容器里要确认 JVM 是否识别 cgroup 配额 |
| 9 | "ForkJoinPool 对异常友好" | 异常封装在 `ForkJoinTask` 里，`join()` 时抛；但 `RecursiveAction` 里未捕获异常可能只在 `join()` 才暴露，易被忽略 |
| 10 | "虚拟线程出来了 ForkJoinPool 就没用了" | 虚拟线程的**默认调度器就是** ForkJoinPool（FIFO 模式）；CPU 密集并行仍然是它的主场 |

> **本书补充定位**：本书第 8 章只讲 `ThreadPoolExecutor`，没有覆盖 ForkJoinPool
> 与工作窃取。这一篇把 `newWorkStealingPool`、`parallelStream`、`CompletableFuture`
> 默认池三者的共同底座讲透，并接上 JDK 21 虚拟线程调度器的新角色。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

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
