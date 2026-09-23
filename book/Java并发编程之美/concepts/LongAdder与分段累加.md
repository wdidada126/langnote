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
