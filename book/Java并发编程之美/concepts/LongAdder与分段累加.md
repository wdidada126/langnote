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
