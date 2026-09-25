# 专篇：伪共享（False Sharing）—— 那个让你慢 10 倍却查不到的 bug

> 对应本书**完全没有提到**的概念。伪共享是并发性能里**最隐蔽的一类问题**：
> 代码逻辑毫无问题、线程之间也没有共享任何变量、锁竞争为零——
> 但程序就是比预期慢一个数量级。原因在**硬件缓存行**，而不在代码。
> 理解它，是理解 `LongAdder`、`Disruptor`、JCTools 为什么要"浪费内存"的前提。

## 一、本章地图

```
缓存行（Cache Line）是什么：CPU 与主存之间交换的最小单位（64B / 128B）
        ↓
伪共享的定义：两个线程改两个不同的变量，但它们恰好落在同一行
        ↓
为什么有害：MESI 一致性协议以"行"为粒度失效 → 无谓的写失效风暴
        ↓
量化：一行之隔，10 倍差距（可复现实验）
        ↓
Java 的解法：JEP 142 @Contended（+ 手动填充的历史技巧）
        ↓
如何检测：JOL 看布局、perf c2c 看热点行、JMH 做对照实验
        ↓
代价与边界：什么时候不该填充
```

## 二、硬件背景：缓存行与 MESI

```
  CPU-0              CPU-1
   L1 (64B 行)        L1 (64B 行)
      │                  │
      └──── 共享 L3 / 内存 ────┘
```

| 概念 | 事实 |
| --- | --- |
| **缓存行（Cache Line）** | 缓存与主存交换数据的**最小单位**。x86（Intel/AMD）为 **64 字节** |
| Apple Silicon（M1/M2/M3） | L2 缓存行为 **128 字节** |
| IBM POWER / 部分 ARM | 以 **128 字节 sector** 管理一致性 |
| **MESI 协议** | 缓存一致性以**行为粒度**：只要行内任一字节被写，整行在其他核失效 |
| **相邻行预取器** | Intel/AMD 会把**成对的 64B 行**一起预取 → 实战隔离需要 **128 字节** |

> **关键结论**：CPU 不知道你改的是行里的哪个 `long`。
> 它只知道"这一行被写了"，于是把**整行**在其他核心上作废。

## 三、伪共享的定义与可复现实验

```java
// 反例：两个 volatile long 紧挨着，几乎必然落在同一缓存行
public class FalseSharing {
    public volatile long a;   // 线程 1 疯狂写
    public volatile long b;   // 线程 2 疯狂写
}
```

两个线程各写一个 `long`，**没有任何逻辑共享**，却因为 `a`/`b` 相距 8 字节：

```
线程1 写 a → 整行失效 → 线程2 的 b 也失效 → 线程2 要重新从内存/其他核拉行
线程2 写 b → 整行失效 → 线程1 的 a 也失效 → ...
                    ↕ 无限乒乓，每次约 100+ 时钟周期
```

**经典实验**（Martin Thompson / Mechanical Sympathy，Disruptor 团队，2011）：

| 布局 | 两个线程各写 1 亿次的耗时 |
| --- | --- |
| 无填充（相邻） | 慢（基准 1.0×） |
| 用 7 个 `long` 隔开两个变量 | 快约 **5-10×** |

> 自己复现：写两个类，一个字段相邻、一个用 `@Contended` 或继承填充，
> 用 **JMH**（`@BenchmarkMode(Mode.Throughput)` + `@Threads(2)` + `@State(Scope.Benchmark)`）跑。
> 注意**不要用 `System.currentTimeMillis()` 手写循环**，JIT 会把无副作用的代码优化掉。

## 四、量化：为什么会慢这么多

| 事件 | 典型延迟（x86，参考值） |
| --- | --- |
| L1 命中 | ~1 ns（4 周期） |
| L2 命中 | ~4 ns |
| L3 命中 | ~15 ns |
| **跨核缓存行转移（RFO）** | **~30-100 ns** |
| 主存访问 | ~80-100 ns |

一次伪共享触发的"失效 + 重新加载" ≈ 一次跨核行转移。
如果热点循环每 10 个周期就触发一次，**吞吐直接崩掉**。

> 这也是为什么 **`volatile` 写比 `volatile` 读贵得多**（见《volatile与内存可见性》）：
> 写是"排他 + 失效他人"，读是"共享"。

## 五、Java 的解法

### 5.1 JEP 142：`@Contended`（JDK 8 引入）

```java
// JDK 8
@sun.misc.Contended static final class Cell { volatile long value; }

// JDK 9+
@jdk.internal.vm.annotation.Contended
static final class Cell { volatile long value; }
```

| 开关 | 说明 |
| --- | --- |
| `-XX:ContendedPaddingWidth` | 填充宽度，**默认 128**（HotSpot 参数，可调） |
| `-XX:-EnableContended`（JDK 8） | JDK 8 早期是实验特性，需 `-XX:+UnlockExperimentalVMOptions` |
| `-XX:-RestrictContended`（JDK 9+） | **默认只有 JDK 内部（boot classloader）能用 `@Contended`**，用户代码要加此开关才生效 |

**JDK 内部的使用点**（都能在 OpenJDK 源码里搜到）：

- `Striped64.Cell`（`LongAdder` 的计数单元）
- `ConcurrentHashMap.CounterCell`
- `Thread` 里的 `threadLocalRandomSeed` / `threadLocalRandomProbe`
- `Exchanger.Node`
- `ConcurrentHashMap` 的 `baseCount`

### 5.2 JDK 8 之前的手动填充技巧（仍需了解，很多老库在用）

```java
class Padding { long p1, p2, p3, p4, p5, p6, p7; }   // 56 字节
class Value extends Padding { volatile long value; }
class Tail extends Value { long q1, q2, q3, q4, q5, q6, q7; }  // 尾部也填
```

**为什么用继承而不是直接在类里塞 7 个 `long`？**
因为 JVM 会**重排字段**（把小的/宽的字段聚在一起、做对齐优化），
同一类里的填充字段可能被优化掉；而**子类的字段一定排在父类字段之后**，
用继承链可以强制布局顺序。

> Disruptor 的 `Sequence` 正是这么做的：`LhsPadding` / `RhsPadding` 各 7 个 `long`，
> `Sequence extends RhsPadding`，前后共 **128 字节**隔离。

### 5.3 数组元素的伪共享

```java
long[] a = new long[8];   // 8 个 long = 64 字节 = 一行！
// 线程 i 写 a[i] → 所有线程互相伪共享
```

**对象数组同样危险**：`Cell[] cells` 里每个 `Cell` 只有一个 `long`，
若不加 `@Contended`，相邻 Cell 对象很可能挤在一行——这正是 LongAdder 必须注解的原因。

## 六、如何检测伪共享

| 工具 | 用途 | 适用层 |
| --- | --- | --- |
| **JOL**（Java Object Layout，OpenJDK 官方工具） | 打印对象内存布局，验证填充是否真的生效 | Java 对象布局 |
| **perf c2c**（Linux，`perf c2c record`，Joe Mario 2015 引入） | **直接定位"HITM"（Hit-Modified）热点缓存行**，并给出竞争的 CPU、指令地址、数据符号 | 系统级，最权威 |
| **Intel VTune Profiler** | Memory Access 分析里的 false sharing 检测 | 系统级（含 Windows） |
| **JMH** | 对照实验：填充 vs 不填充 | Java 微基准 |
| **eBPF / `perf stat` 看 `machine clears` 与 `remote HITM`** | 辅助指标 | 系统级 |

> **实用判据**：如果 `perf c2c` 报告某个**只被写、不被多线程共享**的变量出现高 HITM，
> 那就是伪共享的典型信号。

## 七、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Eggers, S. J. & Katz, R. H. 1989. "The Effect of Sharing on the Cache and Bus Performance of Parallel Programs." ASPLOS IV.** | **伪共享的开创性系统测量**：量化了真共享 vs 伪共享对总线/缓存的开销，并评估多种一致性协议下的表现 |
| **Torrellas, J., Lam, M. S., Hennessy, J. L. 1990. "False Sharing and Spatial Locality in Multiprocessor Caches." IEEE Trans. Computers 39(4).** | 给出伪共享的解析模型，指出"空间局部性"与"伪共享"是一对矛盾 |
| **Bolosky, W. J. & Scott, M. L. 1993. "False Sharing and Its Effect on Shared Memory Performance." USENIX SEDMS IV.** | 在真实系统上测量多种负载，给出"**何时伪共享真的有害**"的量化边界 |
| **Liu, T. & Berger, E. D. 2011. "SHERIFF: Precise Detection and Automatic Mitigation of False Sharing." OOPSLA '11.** | **自动检测 + 自动修复**：用采样 + 差分分析定位伪共享，并在运行时把冲突对象迁移到不同行；近年工具的思想源头 |
| **Drepper, U. 2007. "What Every Programmer Should Know About Memory."** | 虽非论文，但是工程界公认的缓存/内存系统教科书（含 NUMA、预取、伪共享） |
| **JEP 142: Reduce Cache Contention on Specified Fields** | Java 侧 `@Contended` 的官方提案与设计说明 |
| Martin Thompson et al., Mechanical Sympathy 系列（2011-2013） | Disruptor 团队的工程实践总结，把伪共享从论文带进主流 Java 工程 |

## 八、近年研究与工业界前沿

### 近年研究

- **自动化检测与修复**：SHERIFF 之后，方向转向"低开销在线检测 + 编译器/运行时自动布局"（如基于采样的 page-level 拆分、NUMA 感知布局）。
- **NUMA 维度**：现代多路服务器上，伪共享与"远程内存访问"叠加，研究重点转向 **NUMA-aware 数据布局 + 线程绑核**。
- **异构缓存行宽度**：Apple Silicon（128B）、部分 ARM 服务器核、以及"每核 L1 私有 + 大共享 L2"的设计，让"到底填 64 还是 128"变得依赖硬件——**建议直接用 `@Contended` 让 JVM 按平台决定**。
- **硬件计数器**：Linux `perf c2c` 已成为事实标准工具；近年也有基于 Intel PEBS / AMD IBS 的精确定位方案。

### 工业界开源实现（2026-09 核验）

| 项目 | Stars | 伪共享相关设计 |
| --- | --- | --- |
| **LMAX-Exchange/disruptor** | 18.5k | `Sequence` 用 `LhsPadding`/`RhsPadding` **双向 128 字节**填充；`RingBuffer` 的 `Sequencer` 也做隔离；**最有代表性的工程实践** |
| **JCTools/JCTools** | 3.9k | `MpscArrayQueue` 等的 `producerIndex`/`consumerIndex` 各占独立缓存行；`PaddedAtomicLong` 系列专门提供填充类 |
| **openjdk/jdk** | 23.4k | `Striped64.Cell`、`ConcurrentHashMap.CounterCell`、`Thread` 的 TLS 相关字段全部 `@Contended` |
| Netty | 35.1k | `InternalThreadLocalMap`、`Recycler` 的 padded 结构 |
| Linux kernel | — | `__cacheline_aligned`、`____cacheline_aligned_in_smp` 宏；per-CPU 变量按行对齐 |

## 九、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "填充 64 字节就够了" | x86 有**相邻缓存行预取**，实际要 **128 字节**（`@Contended` 默认就是 128） |
| 2 | "我给字段加了 `@Contended`" | JDK 9+ 该注解是 `jdk.internal.vm.annotation.Contended`，**用户代码默认被忽略**，要 `-XX:-RestrictContended` |
| 3 | "只有写写才会伪共享" | **读 + 写**也会（写者让读者的行失效），只是代价通常小一些 |
| 4 | "伪共享只影响 C/Java" | 与语言无关，是硬件效应；Go/Rust/C++ 同样存在 |
| 5 | "字段不声明 `volatile` 就没事" | 只要**真的被并发写**，普通字段一样发生缓存行乒乓；`volatile` 只是让**每一次**写都落到内存语义上，加剧它 |
| 6 | "填充越多越好" | 填充浪费内存。只在**确认的高频写热点**上做；`LongAdder` 最多 NCPU 个 Cell，可接受 |
| 7 | "看到慢就怀疑伪共享" | 先排除锁竞争、GC、内存带宽、NUMA。伪共享要用 **`perf c2c` 或 JMH 对照实验**确证，不要猜 |
| 8 | "数组里每个元素占一行" | **不会**。`long[8]` 恰好一行；`Cell[]` 若不加 `@Contended`，相邻对象很可能挤在一行 |
| 9 | "Apple/ARM 上 64 字节也对" | Apple Silicon 的 L2 缓存行是 **128 字节**，填充策略要跟着平台走 |
| 10 | "填充后 JIT 会优化掉" | 继承式填充（padding 在父类）不会被重排；`@Contended` 由 JVM 保证，不会被 JIT 消除 |

> **本书补充定位**：本书第 2 章讲 JMM 与 `volatile`、第 4 章讲原子类，
> 但**没有提到缓存行这一层**。读者读完后会以为"不加锁 + `volatile` 就一定快"——
> 这一篇补上"内存层次结构"这个维度，是并发性能优化的必备常识。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

# 伪共享（False Sharing）

> 定位：《Java并发编程之美》第 2 章 2.11 节（p.67）。这是一个**纯硬件层面的性能陷阱**——代码看起来没错、逻辑也对，但就是慢。
> 一句话：两个线程各自写两个**毫无关系**的变量，只要它们落在**同一条 CPU 缓存行（cache line）**里，就会像共享变量一样互相把对方的缓存行作废。

## 一、是什么（最小示例）

```java
// 两个 volatile long 在内存中相邻（大概率落在同一条 64 字节 cache line）
public class FalseSharing {
    static class Pair { volatile long a; volatile long b; }
    static Pair p = new Pair();

    // 线程 1 只写 a，线程 2 只写 b —— 逻辑上毫无共享
    // 但因为 a、b 在同一 cache line，两核的 L1/L2 会不停互相 invalidate
}
```

经典基准（`LongAdder` 作者 Doug Lea 与 Martin Thompson 的示例）：

| 写法 | 典型耗时（1 亿次自增 × 2 线程） |
| --- | --- |
| 两个相邻 `volatile long` | ~2-3 倍慢 |
| 两个 long 之间插 7 个 `long` 填充（各占一条 cache line） | 基准 |
| `LongAdder`（分段 + `@Contended`） | 最快 |

**为什么慢**：CPU 的缓存一致性协议（MESI）以 **cache line（x86 上 64 字节）** 为最小单位。线程 A 写 `a` 会把整条 line 置为 Modified，并使线程 B 所在核的副本 Invalid；线程 B 写 `b` 又反过来作废 A 的副本。于是**每次写都变成一次跨核的 cache line 传输**（通过 QPI/UPI，几十到上百纳秒），退化成"像用锁一样慢"。

> 注意区分：**真共享**（true sharing）是两个线程真的写同一个变量，无可避免；**伪共享**（false sharing）是它们写不同变量却被硬件"误伤"。

## 二、实现原理（深入一层）

**1）缓存行与 MESI**

```
Core 0  L1d ──┐
Core 1  L1d ──┼── L3 (共享) ── 内存
              │
    一致性以 64B cache line 为单位维护（MESI: Modified/Exclusive/Shared/Invalid）
```

- 只要 line 内**任何一个字节**被写，整条 line 都要在核间同步。
- 写竞争严重时表现为：`perf c2c` / `perf stat` 里 **HITM（Hit Modified）** 事件飙升，这是诊断伪共享的金标准。

**2）三种规避手法**

```java
// ① 手动填充（JDK 7 时代的主流做法，JDK 8 之前 LongAdder 的 Cell 就是这么干的）
static final class PaddedAtomicLong extends AtomicLong {
    public volatile long p1, p2, p3, p4, p5, p6, p7 = 7L;   // 56 字节填充
    public long sumPaddingToPreventOptimisation() {
        return p1 + p2 + p3 + p4 + p5 + p6 + p7;              // 防止 JIT 消除无用字段
    }
}

// ② @Contended 注解（JDK 8+，JDK 内部使用；需 -XX:-RestrictContended 才能给用户类用）
@sun.misc.Contended           // JDK 8
@jdk.internal.vm.annotation.Contended   // JDK 9+
static final class Cell { volatile long value; }

// ③ 继承填充法（规避 JIT 的字段重排，JDK 8 LongAdder 的 Striped64.Cell 实际采用）
abstract class RingPad   { protected long p1,p2,p3,p4,p5,p6,p7; }
abstract class RingValue extends RingPad { protected volatile long value; }
abstract class RingTail  extends RingValue { protected long p9,...,p15; }
```

> 现代 JDK 的 `LongAdder`/`ConcurrentHashMap#CounterCell`/`Thread` 的 `threadLocalRandomSeed`、以及 `Exchanger` 的 `Node`，全部用了填充或 `@Contended`。

**3）为什么"字段顺序"不可靠**：JVM（HotSpot）会对字段做**重排（field layout）**，把相同宽度类型放一起以压缩对象头/对齐。所以"我只是隔一个 long"并不保证隔开 64 字节；**只有继承链填充或 `@Contended` 才可靠**（`@Contended` 由 JVM 直接把字段挪到 line 边界之外）。

**4）读多写少场景不需要填充**：伪共享只在**高频写**下才明显。只读或低频写的变量做填充反而浪费内存（每个实例多 64 字节）。

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 6/7 | 无标准手段，靠手写 padding；`LinkedTransferQueue` 等并发类内部用 `PaddedAtomicReference` |
| JDK 8 | 引入 `@sun.misc.Contended`；`LongAdder`/`Striped64.Cell` 用继承填充；`-XX:-RestrictContended` 允许用户类使用 |
| JDK 9 | 注解迁移为 `@jdk.internal.vm.annotation.Contended`（`jdk.internal`，默认仍不开放给用户）；JEP 260 封装内部 API |
| JDK 14+ | JEP 352（Non-Volatile Mapped Byte Buffers）等无关；`@Contended` 仍是内部注解 |
| JDK 15 | JEP 374 移除偏向锁——与伪共享无关，但同属"锁优化退场"系列 |
| **JDK 17+ / 21+** | 社区普遍做法：自己写 padding 类，或用 `VarHandle` + 手动布局；`jdk.internal.vm.annotation.Contended` 可用 `--add-exports java.base/jdk.internal.vm.annotation=ALL-UNNAMED` 开放（不推荐生产使用） |

> 权威参考：JOL（Java Object Layout，https://github.com/openjdk/jol）可以打印对象实际布局，验证填充是否生效（`jol-cli` 的 `internals` / `estimates` 子命令）。

## 四、经典论文与著作

| 工作 | 出处 | 关联 |
| --- | --- | --- |
| **Lamport, *How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs*** | IEEE TC 1979 | 顺序一致性与缓存一致性的源头 |
| **Eggers & Katz, *A Characterization of Sharing in Parallel Programs and Its Application to Coherency Protocol Evaluation*** | ISCA 1988 | **"false sharing" 概念的定量研究**，测量真共享 vs 伪共享比例 |
| **Anderson, Lazowska & Levy, *The Performance Implications of Thread Management Alternatives for Shared-Memory Multiprocessors*** | IEEE TPDS 1989 | 同步原语中的伪共享开销 |
| **Mellor-Crummey & Scott, *Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors*** | TOCS 1991 | MCS 锁显式考虑"每个等待者占独立 cache line" |
| **Herlihy & Shavit, *The Art of Multiprocessor Programming***（第 2 版 2020，第 4 章有专门分析） | 2008/2020 | 教科书级的伪共享章节 |
| **Sewell 等, *x86-TSO*** | CACM 2010 | 说明 x86 的强内存模型下伪共享依然会发生（与内存模型无关，是缓存一致性问题） |

## 五、近年研究与工业界实践（2020-2026）

**研究侧**：
- **性能剖析工具的进步**：Linux `perf c2c`（cache-to-cache）成为定位伪共享的标准工具；近年（ISPASS/IISWC 2021-2024）有多篇"自动检测 false sharing"的工作，思路是在硬件性能计数器上做在线分析（如基于 HITM 采样的自动归因），也有基于 PMU 的运行时重排（runtime field reordering）研究。
- **语言/编译器层面的支持**：Rust 有 `#[repr(align(64))]` 与 `crossbeam` 的 `CachePadded`；C++17 有 `std::hardware_destructive_interference_size`（C++17 引入，C++20/23 讨论其 constexpr 语义），**Java 至今没有语言级的标准对齐注解**，这是 Java 在高性能场景的一处短板。
- **新硬件的影响**：ARM 服务器（如 Ampere/鲲鹏）与 AMD EPYC（NUMA + chiplet）上 cache line 一致性代价更高，伪共享的惩罚比单机 x86 更显著；近年有针对 ARM 服务器的 Java 并发库调优报告（如 Alibaba Dragonwell / 华为毕昇 JDK 的相关实践）。

**工业界**：

| 项目 | 地址 | 看点 |
| --- | --- | --- |
| **LMAX Disruptor** | https://github.com/LMAX-Exchange/disruptor | `Sequence` 用 padding 到 64 字节；`RingBuffer` 的序号填充是它性能的关键 |
| **JCTools** | https://github.com/JCTools/JCTools | `MpscArrayQueue` 里大量 `long p1..p15` 填充 + `Sequenced` 检查 |
| **JOL** | https://github.com/openjdk/jol | 验证对象布局与填充是否生效 |
| **JMH** | https://github.com/openjdk/jmh | `@State(Scope.Thread)` + `@CompilerControl` 才能写出可信的伪共享基准 |
| **Netty / Chronicle** | https://github.com/OpenHFT | 大量 cache line 对齐实践 |
| **async-profiler / perf c2c** | https://github.com/async-profiler/async-profiler | 生产环境定位伪共享 |

## 六、常见误区 + 跨语言对照

**误区**：

1. ❌ "只要两个变量被不同线程写就会伪共享" → 必须落在**同一条 64 字节 cache line**；隔得远就没事。
2. ❌ "用 `volatile` 就能避免" → 恰恰相反：**`volatile` 写会触发缓存一致性流量**，伪共享只在写场景下才成为问题。非 volatile 的普通字段若被 JIT 优化进寄存器，反而不产生每次写回。
3. ❌ "填充字段随便写就行" → 会被 JIT 消除（dead field elimination），必须有 `sumPaddingToPreventOptimisation()` 之类的读取保证；且 JVM 字段重排会破坏你的布局，最可靠是**继承链填充**或 `@Contended`。
4. ❌ "JDK 8 之后不用管了" → `@Contended` 只对 JDK 内部类默认生效，用户代码仍需手动处理。
5. ❌ "读操作也会伪共享" → 只读时多核可同时持有 Shared 副本，**不会互相作废**；伪共享是**写**的问题。

**跨语言对照**：

| 语言 | 规避手段 | 是否语言级 |
| --- | --- | --- |
| **Java** | 手动 padding / 继承链填充 / `@jdk.internal.vm.annotation.Contended`（内部） | ❌ 无标准用户级注解 |
| **C++** | `alignas(64)`、`std::hardware_destructive_interference_size`（C++17） | ✅ 标准库常量 |
| **C++（Boost/folly）** | `folly::cacheline_aligned`、`boost::core::aligned_storage` | 事实标准 |
| **Rust** | `#[repr(align(64))]`、`crossbeam::utils::CachePadded` | ✅ 语言级 align + 社区工具 |
| **Go** | 手动 `[8]uint64` 填充（如 `runtime` 里 `padded`） | ❌ 无语言级 |
| **C#** | `[StructLayout(LayoutKind.Explicit)]` 手动布局 | ❌ |
| **Zig / Odin** | `@align(64)` | ✅ |

**一句话结论**：伪共享是**硬件对软件的无声惩罚**——它不产生错误结果，只让你慢 2-5 倍。诊断靠 `perf c2c` / async-profiler，解决靠 cache line 对齐，验证靠 JMH + JOL。
