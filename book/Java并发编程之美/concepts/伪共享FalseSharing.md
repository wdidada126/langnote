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
