# 专篇：LongAdder、分段累加与"热点计数器"这条 30 年老问题

> 对应本书第 4 章（原子操作类）**只讲了 `AtomicLong`，没讲 `LongAdder`**——
> 这是 JDK 8 引入的、在**高争用计数场景**下性能高一个数量级的类。
> 而它的思想（**分散热点 + 惰性求和**）是并发领域一条从 1980 年代延续至今的研究主线：
> 计数网络、衍射树、组合漏斗、SNZI、per-CPU 计数器，**本质是同一个问题**。

## 一、本章地图

```
问题：AtomicLong 在多核下的"热点"——所有线程 CAS 同一个缓存行
        ↓
量化：为什么争用会指数级恶化（缓存行乒乓 + CAS 成功率 1/N）
        ↓
LongAdder 的解法：base + Cell[]（热点分散）+ 求和惰性化
        ↓
代价：sum() 不是原子快照；低争用时反而更慢
        ↓
@Contended 与伪共享（配套见《伪共享FalseSharing》）
        ↓
LongAccumulator / DoubleAdder 的边界
        ↓
工业界同类方案：Linux per-CPU、Go per-P、Disruptor padding
```

## 二、问题：`AtomicLong` 的热点有多严重

```java
AtomicLong counter = new AtomicLong();
counter.incrementAndGet();   // 底层：lock xadd（JDK 8+ 用 xadd，不再用 cmpxchg 循环）
```

在 N 个线程同时自增时：

| 现象 | 代价 |
| --- | --- |
| 所有线程竞争**同一个缓存行** | MESI 协议下该行在 N 个核心间"乒乓"，每次 RFO 约 **100+ 周期** |
| CAS/xadd 成功率约 **1/N** | N-1 个线程失败重试（JDK 8+ `xadd` 是原子的不会失败，但**总线锁/缓存行争用**依然存在） |
| 吞吐随核数**不增反降** | 实测：8 线程争用一个 `AtomicLong`，吞吐可能只有单线程的 1/5 |

> 这就是经典的 **hot spot / contention on shared counter** 问题。
> 峰值出现在"所有核都在抢一个 8 字节"的时刻——**和业务逻辑无关，纯粹是硬件效应**。

## 三、LongAdder 的结构：base + Cell[]

```
  ┌──────────────────────────────────────────────┐
  │  Striped64                                   │
  │  volatile long  base;                        │  ← 无争用时直接用它（CAS）
  │  volatile Cell[] cells;                      │  ← 争用后惰性创建，长度 2 的幂
  │  volatile int   cellsBusy;                   │  ← 简易自旋锁，保护创建/扩容
  └──────────────────────────────────────────────┘
        Cell[i] = { volatile long value; }
                    ↑ @Contended：每个 Cell 独占一个（甚至两个）缓存行
```

### 3.1 `add(long x)` 的四条路径

```java
// Striped64.longAccumulate 语义（简化）
if (cells == null) {
    if (casBase(base, base + x)) return;    // ① 无争用：CAS base 成功，收工
}
// ② base 争用失败 → 惰性初始化 cells（长度 2）
// ③ 用线程的 probe 值哈希到某个 Cell，CAS 它的 value
// ④ 仍失败 → 换 Cell 重试（rehash probe）；若 cells 长度 < CPU 数，尝试扩容到 2 倍
// ⑤ 扩容也拿不到锁 → 回到 CAS base（退化为 AtomicLong，但至少不会崩）
```

**关键细节**：

| 细节 | 说明 |
| --- | --- |
| `cells` 长度上限 | 不超过 **`NCPU`**（`Runtime.availableProcessors()`）对应的 2 的幂，避免无限膨胀 |
| 哈希来源 | 用 `Thread` 里的 `threadLocalRandomProbe`（即 `ThreadLocalRandom` 的次级种子），**不需要额外 ThreadLocal** |
| 重试策略 | 失败后 `advanceProbe()` 换一个哈希值（xorshift），而不是死磕同一个 Cell |
| 扩容时机 | 仅当 `cells` 容量 < NCPU 且 `cellsBusy` 抢锁成功时扩容，最多扩到 NCPU |

### 3.2 为什么必须 `@Contended`

```java
@sun.misc.Contended              // JDK 8
@jdk.internal.vm.annotation.Contended   // JDK 9+
static final class Cell { volatile long value; ... }
```

如果 `Cell` 不填充，`Cell[0]` 和 `Cell[1]` 会落在**同一缓存行**——
分散热点等于白做（详见《伪共享FalseSharing》）。
JVM 会为每个 `@Contended` 字段/对象**前后各填充 128 字节**。

> **128 而不是 64**：x86 的缓存行是 64 字节，但 Intel/AMD 有
> **相邻缓存行预取器（adjacent cache line prefetcher）**，会把成对的 64 字节行一起拉，
> 所以实战中要用 **128 字节**间隔才能彻底隔离。这也是 Disruptor 的做法。

## 四、代价：LongAdder 不是万能的

| 维度 | `AtomicLong` | `LongAdder` |
| --- | --- | --- |
| `incrementAndGet()`（读回值） | ✅ 原子 | ❌ 只有 `increment()`，**没有** `incrementAndGet()` |
| `sum()` 的原子性 | ✅ | ❌ **求和期间可能有并发更新，结果不是任一时刻的真实快照** |
| 低争用（1-2 线程） | **更快**（一次 CAS，无数组间接寻址） | 略慢（数组访问 + 可能的 Cell 分配） |
| 高争用（≥ #core） | 极慢 | **快一个数量级** |
| 内存 | 一个 long | base + 最多 NCPU 个 Cell（每个 128+ 字节） |
| `get()` | 精确 | `sum()`，O(#cells) |

**选型规则**：

- 需要**读取精确值用于判断/比较**（如限流器的当前计数）→ `AtomicLong`
- 只需要**高频写入、低频读取**（QPS 统计、指标采集、命中数）→ **`LongAdder`**
- 求和要精确 → 只能在"**没有并发更新**"的时刻 `sum()`（如统计周期切换时）

## 五、`LongAccumulator` 与 `DoubleAdder`

```java
LongAccumulator max = new LongAccumulator(Long::max, Long.MIN_VALUE);  // 求最大值
max.accumulate(x);
long result = max.get();   // 同样不保证原子快照
```

| 类 | 用途 | 注意 |
| --- | --- | --- |
| `LongAdder` | 求和（可交换） | `LongAdder` 实际是 `LongAccumulator` 在 `Long::sum` 下的特化，代码更短 |
| `LongAccumulator` | 任意 `LongBinaryOperator` | **只有运算满足结合律/交换律时结果才稳定**；`Long::max` 可以，`a - b` 不行 |
| `DoubleAdder` | double 求和 | 内部把 `double` 用 `doubleToRawLongBits` 转成 `long` 做 CAS（因为硬件不支持 double 的 CAS） |
| `DoubleAccumulator` | 任意 double 运算 | 同上 |

> **JDK 8 的坑**：`DoubleAdder` 累加的是**位模式**，求和过程中若混入 `-0.0` / `NaN` 需小心。

## 六、JDK 8 → 21 的实现变化

| 版本 | 变化 |
| --- | --- |
| JDK 8 | `sun.misc.Unsafe` 做 CAS；`sun.misc.Contended` |
| JDK 9 | 迁移到 **VarHandle**（`BASE`/`CELLVALUE`/`CELLS`/`CTL`）；`@jdk.internal.vm.annotation.Contended`（用户代码需 `-XX:-RestrictContended` 才能用） |
| JDK 11+ | 持续微调（probe 处理、扩容边界） |
| JDK 21+ | `Striped64` 仍是内部基类，`ConcurrentHashMap.CounterCell` 复用同一套思想 |

> **思路复用**：`ConcurrentHashMap` 在 JDK 8 之后的 `size()` 用的就是
> `baseCount + CounterCell[]` ——**和 LongAdder 一模一样的代码形状**。
> 看懂 `Striped64`，就同时看懂了 CHM 的计数（见《ConcurrentHashMap演进》）。

## 七、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Yew, P.-C., Tzeng, N.-F., Lawrie, D. H. 1987. "Distributing Hot-Spot Addressing in Large-Scale Multiprocessors." IEEE Trans. Computers 36(4).** | **最早系统研究"共享计数器热点"**；提出把计数器分散到多个内存模块再合并 |
| **Gottlieb, A., Grishman, R., Kruskal, C. P., McAuliffe, K. P., Rudolph, L., Snir, M. 1983. "The NYU Ultracomputer — Designing an MIMD Shared Memory Parallel Computer." IEEE Trans. Computers.** | **软件合并（software combining）** 的起源：在互连网络上把多个 `fetch&add` 合并成一个 |
| **Aspnes, J., Herlihy, M., Shavit, N. 1994. "Counting Networks." JACM 41(5): 1020-1048.** | 用**无状态 balancing network** 实现可线性化、低争用的计数器；理论基石 |
| **Shavit, N. & Zemach, A. 1996. "Diffracting Trees." ACM TOCS 14(4): 385-428.** | 计数网络的**自适应/动态**改进：树宽随争用自适应，实测优于静态网络 |
| **Shavit, N. & Zemach, A. 1999. "Combining Funnels: A Dynamic Approach to Software Combining." PPoPP '99.** | 把 combining 做成动态数据结构；与 LongAdder 的"争用时才分叉"思想**高度一致** |
| **Ellen, F., Lev, Y., Luchangco, V., Moir, M. 2006. "SNZI: Scalable NonZero Indicators." PODC '06.** | 只用 `O(log n)` 空间判断"计数是否 > 0"，比完整计数更省；用于引用计数/信号量 |
| **Herlihy, M. & Shavit, N.《The Art of Multiprocessor Programming》第 11 章（Counting）** | 上述所有方案的教科书级统一讲解；**推荐作为这一节的延伸阅读** |
| **JEP 142: Reduce Cache Contention on Specified Fields** | `@Contended` 注解的官方提案，说明了为什么要 128 字节填充 |

> **LongAdder 本身没有论文**。Doug Lea 在 `LongAdder` 的 Javadoc 里说明：
> 它是"当争用高时优于 `AtomicLong` 的替代品"，并提示"**它有更高的内存开销**"。

## 八、近年研究与工业界前沿

### 近年研究

- **NUMA 感知的分段计数器**：在多插槽机器上，"分散"要按 NUMA 节点分组，否则跨节点 CAS 反而更贵。近年（尤其数据库/内核社区）普遍采用 **per-NUMA-node 分段 + 异步聚合**。
- **读侧精确性权衡**：LongAdder 牺牲了"读的原子性"。近年一些工作（如 *scalable read-mostly counters*）尝试用"版本号 + 双缓冲"给出近似但**单调**的读数，用于监控/限流。
- **与 eBPF/内核统计的呼应**：Linux 的 per-CPU 计数器在读取时同样要遍历所有 CPU（`for_each_possible_cpu`），与 `sum()` 遍历 `Cell[]` 是同一套取舍。
- **硬件加速**：部分架构提供真正的原子 RMW 指令与"远程原子操作"（如 CXL 3.0 的原子原语），未来可能改变这条取舍曲线。

### 工业界开源实现（2026-09 核验）

| 项目 | Stars | 同类机制 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `java.util.concurrent.atomic.Striped64.java`、`LongAdder.java`、`LongAccumulator.java`、`ConcurrentHashMap.CounterCell` |
| **LMAX-Exchange/disruptor** | 18.5k | `Sequence` 用 `LhsPadding`/`RhsPadding`（各 7 个 long）做 **128 字节填充**；其 `MultiProducerSequencer` 也做分散以避免序号热点 |
| **dropwizard/metrics** | 7.8k | Metrics 4.x 的 `Counter`、`Meter`、`Histogram` 内部直接用 **`LongAdder`**（高 QPS 下指标采集的事实标准） |
| Micrometer（`micrometer-metrics/micrometer`） | — | 同上；Spring Boot Actuator 的指标底座 |
| Linux kernel `percpu_counter` / `local_t` | — | per-CPU 计数器，读取时遍历聚合 —— **与 LongAdder 同构** |
| Go runtime `per-P` 分配计数 | — | 每个 P 维护本地 `mcache` 与分配计数，避免全局热点 |

> **可复现实验**（建议读者自己跑一次）：
> 用 JMH 写两个基准：`N` 个线程各自增 1e7 次，分别用 `AtomicLong.incrementAndGet()`
> 和 `LongAdder.increment()`。`N = 1` 时两者接近；`N = 本机核数 × 2` 时 `LongAdder`
> 通常快 **5-20 倍**。这个实验是理解"热点"最直观的方式。

## 九、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "LongAdder 一定比 AtomicLong 快" | **低争用下更慢**（数组间接寻址 + 更多内存）。只有争用达到核数量级才划算 |
| 2 | "`sum()` 是精确值" | **不是原子快照**；并发更新时求和结果可能不对应任何真实时刻 |
| 3 | "LongAdder 有 `incrementAndGet()`" | **没有**。它不返回新值；需要返回值就得用 `AtomicLong` |
| 4 | "Cell 越多越好" | 上限是 `NCPU` 对应的 2 的幂；再多的 Cell 只会让 `sum()` 变慢 |
| 5 | "@Contended 只是可选优化" | **没有它，LongAdder 就没有意义**（Cell 挤在一行等于没分散） |
| 6 | "用户代码也能随便用 `@Contended`" | JDK 9+ 该注解是 `jdk.internal.vm.annotation.Contended`，**用户代码默认被忽略**，需加 `-XX:-RestrictContended` |
| 7 | "填充 64 字节够了" | 因相邻行预取，实战要 **128 字节**（Disruptor 的做法） |
| 8 | "LongAccumulator 可以算减法" | 只有**满足结合律且交换**的运算结果才稳定；且 `get()` 同样非原子 |
| 9 | "LongAdder 不会内存泄漏" | `cells` 数组一旦扩容**不会缩回**，长期高争用会占住 `NCPU × 128B`（可接受，但要知道） |
| 10 | "ThreadLocal 也能做分段计数" | 可以但**读取必须遍历所有线程**（且线程退出时数据丢失）；`LongAdder` 的 Cell 与线程解耦，是更好的方案 |

> **本书补充定位**：本书第 4 章把"原子操作类"讲到了 `AtomicLongArray`、`AtomicReferenceFieldUpdater`，
> 但漏掉了 `LongAdder`——这是 JDK 8 里**改变性能格局**的一个类。本篇补齐，
> 并把它与 `ConcurrentHashMap` 的计数、Linux per-CPU、Disruptor padding 串成一条主线。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

# LongAdder 与分段累加

> 定位：`java.util.concurrent.atomic.LongAdder` / `LongAccumulator` / `DoubleAdder`，JDK 8 引入，用于**高并发热点计数**。思路：把一个全局原子变量拆成"一个 base + 若干 Cell"，让不同线程落在不同的缓存行上争用。
> 对应《Java并发编程之美》第 4 章「原子操作类原理剖析」；思想源头可追溯到 1987 年的 hot-spot 分散与 1991 年的 counting networks。

## 一、是什么（最小示例）

```java
LongAdder hits = new LongAdder();        // 统计 QPS、命中数、累加耗时
void onRequest(long cost) { hits.increment(); }

long report() { return hits.sum(); }     // 注意：并发更新下 sum() 是"弱一致"的

// 通用版本：可自定义二元运算（这里是取最大值）
LongAccumulator max = new LongAccumulator(Long::max, Long.MIN_VALUE);
max.accumulate(42L);
```

适用场景：**写多读少、只要求最终总和**（监控计数、限流统计）。若需要精确的瞬时值或 CAS 语义，仍应使用 `AtomicLong`。

## 二、实现原理（源码级）

**1）三层结构**（基类 `Striped64`）：`volatile long base` —— 无竞争时的单点；`volatile Cell[] cells` —— 竞争出现后按线程散列到多个槽；`volatile int cellsBusy` —— 一把 0/1 自旋锁，只在**初始化数组、新建 Cell、扩容**时短暂持有，正常累加路径完全无锁。

**2）Cell 与伪共享**：
```java
@sun.misc.Contended static final class Cell { volatile long value; ... }
```
`@Contended` 让 JVM 在该字段前后插入填充（默认 128 字节），把每个 Cell 挤进独立缓存行，避免多线程写相邻槽位造成缓存行乒乓。JDK 9 起该注解迁移为 `jdk.internal.vm.annotation.Contended`，应用代码无法直接使用。

**3）线程着色**：每个线程持有 `ThreadLocalRandom` 里的 `probe` 值，`Striped64.getProbe()` 取出后 `(n - 1) & h` 定位槽位。CAS 失败则 `advanceProbe()`（xorshift 重散列）换一个槽再试。

**4）`add(x)` 主路径**：
- `cells` 为 null 且 `casBase` 成功 → 直接返回（单线程场景成本几乎等同 AtomicLong）；
- 否则进入 `longAccumulate`：cells 未初始化 → 抢 `cellsBusy` 后建长度 2 的数组；已初始化 → 定位 Cell 做 CAS；
- CAS 仍失败且 `cells.length < NCPU` → 抢 `cellsBusy` 后**扩容为 2 倍**并 rehash 搬运；
- 已到上限（数组长度不超过 CPU 核数）→ 只 rehash 重试。上限取 NCPU 是因为热点分散到"核数"个槽即可，再多只会浪费空间与遍历成本。

**5）`sum()` 为什么弱一致**：
```java
public long sum() { Cell[] cs = cells; long sum = base; if (cs != null) for (Cell c : cs) if (c != null) sum += c.value; return sum; }
```
遍历过程**不加锁、不加快照**，并发写入时既可能漏掉刚加的值，也可能重复计入；因此返回值不是一个线性化点上的真值。同理 `reset()` 只是把 base 与各 Cell 清零，`sumThenReset()` 在并发下更不可用（Doug Lea 的 Javadoc 明确说明：只在"确实无并发更新"时才有意义）。

**6）`LongAccumulator`**：把 `add` 换成 `accumulate(x, LongBinaryOperator)`，initialValue 作为 Cell 初值，可用于 max/min 等幂等结合运算（运算必须满足结合律，否则结果依赖遍历顺序）。

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 8 | `LongAdder`/`LongAccumulator`/`DoubleAdder` 随 JSR 166e 并入 `java.util.concurrent.atomic`；`@sun.misc.Contended` 生效（需 JVM 支持） |
| JDK 9 | JEP 193（Variable Handles）：`Striped64` 的 `base`/`cellsBusy`/`cells` 与 `Cell.value` 改为 VarHandle 访问；`@Contended` 迁入 `jdk.internal.vm.annotation` |
| JDK 11 | 无功能变化 |
| JDK 17 | 无功能变化 |
| JDK 21 | JEP 444 虚拟线程：线程数量可膨胀到百万级，`probe` 冲突概率上升，但 rehash + 按核数封顶的机制仍然有效；JEP 374（JDK 15 废弃偏向锁）对这类 CAS 结构无影响 |
| JDK 25 | 无新 API；随着 JEP 471（JDK 23 弃用）/ JEP 498（JDK 24 告警）推进 `sun.misc.Unsafe` 退役，VarHandle 已成为 JUC 内部唯一的原子访问路径 |

## 四、经典论文

| 论文 | 出处 | 与 LongAdder 的关系 |
| --- | --- | --- |
| Distributing Hot-Spot Addressing in Large-Scale Multiprocessors | Yew, Tzeng & Lawrie, ISCA 1987 | 最早系统提出"把热点内存地址分散到多个副本以消除串行瓶颈"，是分段累加的思想先驱 |
| Counting Networks | Aspnes, Herlihy & Shavit, STOC 1991 / J. ACM 1994 | 用交换机网络把单一计数器变成多计数器、实现低争用且可线性化的计数；LongAdder 放弃了线性化以换取更高吞吐 |
| Wait-Free Synchronization | Herlihy, TOPLAS 13(1), 1991 | 计数网络属于 wait-free 构造的理论背景 |
| Linearizability: A Correctness Condition for Concurrent Objects | Herlihy & Wing, TOPLAS 12(3), 1990 | 用于判定 `sum()` 为何**不是**线性化的：它不对应任何单一时间点 |
| Software Transactional Memory | Shavit & Touitou, PODC 1995 | 同一时期另一条降低热点争用的技术路线（乐观事务 vs 分段累加） |
| The Java Memory Model | Manson, Pugh & Adve, POPL 2005 | `volatile long value` 与 VarHandle 的可见性/原子性保证 |
| The Art of Multiprocessor Programming | Herlihy & Shavit, 2008 / 2012 | 教材：争用、缓存一致性、组合树与计数网络的系统比较 |

## 五、近年研究与工业界实践

**同行评审论文**
- NVTraverse（Friedman 等，PPoPP 2021）：非易失内存上"只保证终态"的遍历思想，可类比"计数器只需终值、不需精确中间快照"的取舍。
- RefinedRust（Gäher 等，2024）：对并发数据结构做自动化验证，其中"分片计数器"是典型验证目标。
- Understanding Real-World Concurrency Bugs in Go（Tu 等，ASPLOS 2019）：统计显示大量 bug 来自对共享计数器的非原子读写，印证了分片/原子结构的必要性。

**工业界资料**
- OpenJDK：`src/java.base/share/classes/java/util/concurrent/atomic/Striped64.java` — https://github.com/openjdk/jdk
- LMAX Disruptor — https://github.com/LMAX-Exchange/disruptor ：其 `Sequence` 同样用缓存行填充规避伪共享，与 `@Contended` 同源思路
- JCTools — https://github.com/JCTools/JCTools ：提供面向伪共享与缓存行优化的并发结构与计数器
- JMH — https://github.com/openjdk/jmh （吞吐基准）；jcstress — https://github.com/openjdk/jcstress （验证 `sum()` 的弱一致行为）
- Chronicle-Queue — https://github.com/OpenHFT/Chronicle-Queue ：堆外持久化队列，其元数据计数也需避免热点争用

## 六、常见误区 + 跨语言对照

**常见误区**
1. "`sum()` 是精确值"——不是，遍历无快照，并发写入时既可能漏计也可能重复；只有无并发更新时才精确。
2. "任何场景 LongAdder 都更快"——单线程/低争用下它比 `AtomicLong` 略慢（多一次 probe 计算与数组定位），且 `sum()` 是 O(cells)。
3. "线程越多 Cell 越多"——数组长度上限是 CPU 核数，超出后同一槽位内的线程重新串行化竞争。
4. "我也能给自己的类加 `@Contended`"——JDK 9 起该注解迁入 `jdk.internal.vm.annotation`，应用侧只能手写填充字段。
5. "LongAdder 能当序列号用"——它没有 `compareAndSet`/`incrementAndGet`，无法做边界判断或唯一 ID。
6. "`sumThenReset()` 可以做每秒速率统计"——并发下它会丢值，应改为"记录两个时间点的 sum 差值"。
7. "分段就一定无争用"——槽位散列仍可能碰撞，靠 `advanceProbe()` 缓解，而非消除。

**跨语言对照**

| 语言 | 对应设施 | 关键差异 |
| --- | --- | --- |
| Java | `LongAdder` / `LongAccumulator` / `Striped64` | 内建分段 + `@Contended` 填充，代价是 `sum()` 弱一致 |
| C++ | 标准库无等价物；常用手工分片 `std::atomic<long>` 数组，或 Folly 的 `ThreadCachedInt`（线程本地缓存 + 定期归并） | 需自行处理伪共享（`alignas(64)`）与归并时机 |
| Rust | 标准库无；社区用手工分片 `AtomicU64` 数组或 metrics 类库的分片计数器 | 与 Java 同构，但缺少 JVM 的注解式自动填充 |
| Go | `sync/atomic` + 按 `GOMAXPROCS` 分片数组（`[N]atomic.Int64`），或 channel 聚合 | 无内建分片计数器；atomic 操作本身即顺序一致 |
| Erlang | `counters` 模块（OTP 21 起），可设 `write_concurrency` | 运行时代为按调度器分片，语义上仍保证读取一致 |
| Python | 无内建原子计数器；`+=` 在 GIL 下仍非原子，需 `threading.Lock` 或 `multiprocessing.Value` | 线程级并行受 GIL 限制，争用通常不是首要瓶颈 |
