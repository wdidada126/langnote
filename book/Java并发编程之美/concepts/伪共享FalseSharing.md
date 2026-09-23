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
