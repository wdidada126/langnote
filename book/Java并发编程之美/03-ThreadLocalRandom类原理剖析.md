# 第 3 章 ThreadLocalRandom 类原理剖析（原书 pp.80-87）

> 源码：`java.util.concurrent.ThreadLocalRandom`、`java.util.Random`、`java.util.SplittableRandom`
> 延伸：[concepts/并发模型跨语言对比.md](concepts/并发模型跨语言对比.md)

## 一、本章地图（原书小节）

| 小节 | 主题 | 页码 |
| --- | --- | --- |
| 3.1 | Random 类及其局限性 | 80 |
| 3.2 | ThreadLocalRandom | 82 |
| 3.3 | 源码分析 | 84 |
| 3.4 | 总结 | 87 |

## 二、核心精讲

### 3.1 Random 的局限：一把 CAS 全局种子

```java
// java.util.Random 的核心（JDK 8）
protected int next(int bits) {
    long oldseed, nextseed;
    AtomicLong seed = this.seed;
    do {
        oldseed = seed.get();
        nextseed = (oldseed * multiplier + addend) & mask;   // 线性同余 LCG
    } while (!seed.compareAndSet(oldseed, nextseed));        // ★ 全局单点 CAS
    return (int) (nextseed >>> (48 - bits));
}
```

问题不是"LCG 不够随机"，而是：
1. **所有线程争抢同一个 `AtomicLong`** —— 每次 `next()` 都要一次 CAS，cache line 在核间来回，多线程下吞吐崩溃（这是第 2.11 节伪共享的教科书案例）；
2. **线性同余生成器的低位周期短**，序列混合不足，`nextInt(bound)` 取模后低位比高位弱得多。

> 原书给的性能对比结论（至今依然成立）：多线程下 `ThreadLocalRandom` 的吞吐通常是 `Random` 的 **一个数量级以上**。

### 3.2 ThreadLocalRandom 的做法：种子塞进 Thread

```
Thread 对象内部三个字段（JDK 8+ 起定义在 java.lang.Thread）：
  long threadLocalRandomSeed          // 本线程的 LCG 种子
  int  threadLocalRandomProbe         // 哈希探测步长（ConcurrentHashMap/TLR 用）
  int  threadLocalRandomSecondarySeed // 次级种子
```

```java
public static ThreadLocalRandom current() {
    if (UNSAFE.getInt(Thread.currentThread(), PROBE) == 0)
        localInit();                                  // 首次访问时惰性初始化
    return instance;                                  // 单例：全局只有这一个实例
}
final long nextSeed() {
    Thread t = Thread.currentThread();
    UNSAFE.putLong(t, SEED,
        UNSAFE.getLong(t, SEED) + GAMMA);             // ★ 无需 CAS：种子是线程私有的
    return UNSAFE.getLong(t, SEED);
}
```

三点关键（原书 3.3 的精髓）：
1. **每个线程有自己的 seed** —— 完全无竞争，连 `volatile` 读都没有（通过 Unsafe 直接读写 Thread 字段）；
2. 初始化时用 `SEEDER` 这个全局 `AtomicLong` + **黄金分割常量 GAMMA = 0x9E3779B97F4A7C15**（2^64/φ）给每个线程一个彼此远离的起始种子，避免不同线程的序列相关；
3. `ThreadLocalRandom` 是**单例**（`instance`），禁止 `new` —— 所以 `setSeed()` 会直接抛 `UnsupportedOperationException`（这是刻意的：否则会破坏线程隔离性）。

### 3.3 常用 API

```java
ThreadLocalRandom r = ThreadLocalRandom.current();
int  a = r.nextInt(100);           // [0,100)
int  b = r.nextInt(10, 20);        // [10,20)
long c = r.nextLong();
// JDK 8+ 还有 Stream 工厂：
DoubleStream ds = ThreadLocalRandom.current().doubles(1_000_000).parallel();
```

⚠️ **常见错误用法**：把 `ThreadLocalRandom.current()` 存进 static 字段或在线程间共享。
```java
static final ThreadLocalRandom R = ThreadLocalRandom.current();  // ✗ 主线程装的 fallback 种子
```
正确做法是**每次使用时**调用 `current()`，或直接 `ThreadLocalRandom.current().nextInt(10)`。

## 三、JDK 版本演进（本书未覆盖的全部发生在这里）

| 版本 | 变化 |
| --- | --- |
| JDK 8 | `ThreadLocalRandom` 引入（本书基线）。同期还有 **`SplittableRandom`** |
| **JDK 17** | 🔴 **JEP 356：统一随机数 API** —— 引入 `RandomGenerator` 体系：<br>`RandomGenerator` / `.Randomizable` / `.SplittableGenerator`（可分裂）/ `.JumpableGenerator`（可跳跃，能跳过 2^64 个数）/ `.LeapableGenerator` / `.ArbitrarilyJumpableGenerator`；`RandomGeneratorFactory.of("L64X256MixRandom")` 可按算法名挑选；既有类改为实现这套接口，可以**平替**注入 |
| JDK 17+ | `RandomSupport` 里实现 **LXM 系列算法**（如 `L64X128MixRandom`），这是 JDK 17 之后主要的新算法家族 |
| JDK 19 | **虚拟线程预览**后，`ThreadLocalRandom` 依然可用，但百万级虚拟线程下每个线程一个 seed 的成本被放大；对并行 Stream/短任务更推荐 `SplittableGenerator.split()` |
| JDK 21+ | 虚拟线程 GA；`ThreadLocalRandom` 在虚拟线程中仍然工作（虚拟线程也是 `Thread`），但**大量短命虚拟线程 + ThreadLocal 系**会增加 GC/内存压力，参考 [concepts/虚拟线程Loom.md](concepts/虚拟线程Loom.md) |

```java
// JDK 17+ 推荐写法（本书没有）：可分裂 → 适合并行流/虚拟线程，无需共享 seed
RandomGenerator.SplittableGenerator gen = RandomGeneratorFactory.<RandomGenerator.SplittableGenerator>
        of("L32X64MixRandom").create();
List<RandomGenerator.SplittableGenerator> children =
        Stream.generate(gen::split).limit(8).toList();   // 每个子任务一个独立生成器
```

> **重要区别**：`SplittableRandom` / `RandomGenerator.SplittableGenerator` 是**非线程安全**的（不是 ThreadLocal 版本），设计意图是"**先分裂、再各用各的**"，恰恰适合 ForkJoin / 虚拟线程场景。

## 四、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| 线性同余生成器（LCG） | Knuth, *TAOCP 卷 2 半数值算法* §3.2.1 | 1969 起（原书 Random 的理论基础） |
| LCG 参数选取 | L'Ecuyer, *Tables of Linear Congruential Generators of Different Sizes and Good Lattice Structure* | Math. Comp. 68(225), 1999 |
| Xorshift 族 | Marsaglia, *Xorshift RNGs* | J. Statistical Software 8(14), 2003 |
| **ThreadLocalRandom 的直接理论来源** | Steele, Lea & Flood, *Fast Splittable Pseudorandom Number Generators* | **OOPSLA 2014** —— SplittableRandom 的论文，提出基于 SplitMix/DotMix 的可分裂 scheme |
| **JDK 17 的 LXM 算法来源** | Blackman & Vigna, *Scrambled Linear Pseudorandom Number Generators* | ACM TOMS 47(3), 2021（Scrambled linear 族；xoshiro 系列同一作者） |
| 并行 RNG（计数型） | Salmon, Moraes, Dror & Shaw, *Parallel Random Numbers: As Easy as 1, 2, 3* | SC'11（counter-based，与 SplitMix 不同路线） |
| 统计质量测试 | L'Ecuyer & Simard, *TestU01: A C Library for Empirical Testing of Random Number Generators* | ACM TOMS 33(4), 2007 |

## 五、近年研究与工业界前沿（2020-2026）

- **算法层面**：2020 年后主流进展是 *scrambled linear* 族（xoshiro/LXM）—— **这正是 JDK 17 换实现方式的原因**，比 JDK 8 的 LCG 有显著更好的统计质量与更长的周期。权威参考是 Blackman & Vigna 的 TOMS 论文。
- **形式化与工程交叉**：Rust 的 `rand_*`（ChaCha12/PCG）、Go 1.22 的 `math/rand/v2`、Python 的 `numpy.random.Generator`（PCG64 + `SeedSequence`）都在同期换到了现代算法 —— 一场跨语言的"LCG 退役运动"。
- **SIMD 友好 RNG**：为 GPU/向量化负载设计的批量生成器近年是 active area（调用一次生成一大批次用于 monte carlo），但与 JUC 的日常使用距离较远，不做展开。
- **实践**：OpenJDK 的 `RandomSupport` 实现（JDK 17+）与 `Thread` 上的三个字段是最新实例：https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/jdk/internal/util/random/RandomSupport.java

## 六、常见误区 / 本书需修正之处

1. ❌ `Random` 是线程安全的所以可以随便在多线程用 → 安全但**竞争**，是性能陷阱而不是正确性问题。
2. ❌ `ThreadLocalRandom` 继承自 `Random` 所以能 `new ThreadLocalRandom()`（或注入 `Random`） → 不能，它是单例且禁用了 `setSeed`。
3. ❌ 把 `current()` 缓存成 static → 会退化为主线程种子（除非你确实在主线程用）。
4. ⚠️ **本书没有提 `SplittableRandom`（JDK 8 同批引入）** —— 它是 ThreadLocalRandom 的"另一种解法"，虚拟线程时代更重要，务必补。
5. ⚠️ **本书没有 JDK 17 的 `RandomGenerator`（JEP 356）** —— 2026 年写新代码建议面向 `RandomGenerator` 接口编程，便于替换算法（含自定义seed randomizable）。
6. ⚠️ 注意 `ThreadLocalRandomSecondarySeed` 与 `probe` 字段也被 `ConcurrentHashMap`（散列争用与扩容决策）复用 —— 这是理解本书第 11.3 节 size() 计数行为的关键伏笔（见 [concepts/ConcurrentHashMap演进.md](concepts/ConcurrentHashMap演进.md)）。

## 七、跨语言对照

| 语言 | 线程安全/并发随机数方案 | 备注 |
| --- | --- | --- |
| Java（本书） | `ThreadLocalRandom`（线程私有 seed，零竞争） | 单例 + 每线程 seed；JDK 17 起另有 `RandomGenerator.SplittableGenerator` |
| Go | 全局 `math/rand` 加互斥锁；各协程共用 `rand.Rand` **不安全**，官方建议每 goroutine `rand.New()`；Go 1.22 引入 `math/rand/v2` | 若追求无锁，也需要类似 ThreadLocal 的 per-G 方案 |
| Rust | `rand::rng()` 返回 **`ThreadRng`**（线程本地、启用了 Cell RefCell）；跨线程需 `Arc<Mutex<...>>` 或 Chacha | 所有权模型让"共享未同步的可变状态"无法编译 |
| C++ | `std::mt19937` **非线程安全**；惯用法是 `thread_local std::mt19937`（本质上就是 ThreadLocalRandom 的手工版） | C++26 无 std 级urbed PRNG 接口（截止 2026 以标准进展为准） |
| Python | `random.random()` 全局 Mersenne Twister，**依赖 GIL** 才算"安全"；并发推荐 `random.Random()` 每线程一份或 NumPy `Generator` | 自由线程 Python（PEP 703 之后）会放大这个问题 |
| Erlang | `rand` process dictionary + seed per process | 天然无共享，问题根本不存在 |
