# 专篇：volatile 与内存可见性

> 对应本书 2.6 节。本文聚焦 **volatile 本身**（语义、实现、性能、陷阱）；
> happens-before 的完整规则体系见 [JMM与happens-before.md](JMM与happens-before.md)。
> 两者是"具体机制"与"全局契约"的关系。

## 一、一句话概括

`volatile` 给一个字段加**两重保证**：

1. **可见性**：写立即对其他线程可见（写穿缓存），读从主存读
2. **有序性**：禁止特定方向的重排序（acquire/release 语义）

**但不保证原子性** —— `volatile int i; i++` 依然是三步，并发下会丢失更新。

## 二、语义的精确表述

JMM 对 volatile 的定义（JSR 133 之后，JDK 5+）：

| 规则 | 内容 |
| --- | --- |
| **volatile 写** | 写之前的**所有**操作（普通读写、volatile 读写）**都不能重排到写之后** |
| **volatile 读** | 读之后的**所有**操作**都不能重排到读之前** |
| **volatile 写 → volatile 读** | 不能重排 |
| **可见性** | 写一个 volatile 变量 happens-before 后续对它的读 |

用 acquire/release 的说法（与 C++ `memory_order` 对应）：

```
volatile 写  =  release 语义（阻止之前的操作跑到后面）
volatile 读  =  acquire 语义（阻止之后的操作跑到前面）
```

## 三、硬件实现：到底插了什么屏障

JMM 定义了 4 种屏障，volatile 的实现按如下插入：

```
普通读/写
普通读/写          ←─────────┐
[StoreStore]                 │  volatile 写之前：防止前面的普通写跑到后面
volatile 写                  │
[StoreLoad]       ← 关键！   ┘  volatile 写之后：防止后续读提前（**唯一有真实开销的**）

volatile 读
[LoadLoad]                      volatile 读之后：防止后续读跑到前面
[LoadStore]                     volatile 读之后：防止后续写跑到前面
普通读/写
```

**x86（TSO 模型）上的实际代价**：

| 屏障 | x86 指令 | 代价 |
| --- | --- | --- |
| `StoreStore` | 无（TSO 已保证 store-store 有序） | **0** |
| `LoadLoad` | 无 | **0** |
| `LoadStore` | 无 | **0** |
| **`StoreLoad`** | **`mfence`** 或 `lock addl $0,(%rsp)` | **约 20-100 个时钟周期** |

> 🔑 **关键结论**：
> - **x86 上 volatile 读几乎免费**（不插屏障，只是禁止编译器重排）
> - **x86 上 volatile 写很贵**（必须 `StoreLoad` 屏障）
> - **ARM 上两者都要插屏障**（弱内存模型）

这正是 DCL 单例里 `instance` 必须 volatile 的原因，也是为什么"volatile 写比读慢得多"。

## 四、经典案例：双重检查锁定（DCL）

```java
// ❌ JDK 1.4 及之前：坏的（volatile 语义不足）
class Singleton {
    private static Singleton instance;
    static Singleton get() {
        if (instance == null) {                          // ① 第一次检查（不加锁，快）
            synchronized (Singleton.class) {
                if (instance == null)                    // ② 第二次检查
                    instance = new Singleton();          // ③ 问题在这
            }
        }
        return instance;
    }
}
```

**问题出在 ③**：`new Singleton()` 不是原子的，它被分解为：

```
1. 分配内存空间
2. 初始化对象（写字段）
3. 把引用赋给 instance
```

**步骤 2 和 3 可能被重排** → 另一个线程在 ① 处看到 `instance != null`（引用已赋值但对象未初始化），
拿到一个**半成品对象**。

```java
// ✅ JDK 5+：加 volatile 即可（volatile 写阻止步骤 2 跑到步骤 3 之后）
private static volatile Singleton instance;

// ✅✅ 更好：静态内部类（零成本，JVM 保证初始化安全）
class Singleton {
    private Singleton() {}
    private static class Holder { static final Singleton I = new Singleton(); }
    static Singleton get() { return Holder.I; }
}

// ✅✅✅ 最佳：枚举（Effective Java Item 3，还能防反射与序列化攻击）
enum Singleton { INSTANCE; }
```

> **历史注记**：DCL 在 JDK 1.4 时代是**真的坏**，这一争议直接推动了 JSR 133 修订 JMM。
> Pugh 等人 2000 年发表的 *"Double-Checked Locking is Broken"* 是并发领域最著名的工程文献之一。

## 五、volatile 的三种正确用法

### ① 状态标志（最经典）

```java
class Worker implements Runnable {
    private volatile boolean stopped = false;
    public void stop() { stopped = true; }
    public void run() { while (!stopped) doWork(); }    // ✅ 单写多读
}
```

> 这是 volatile 唯一"无损"的用法：一次写、多次读，没有复合操作。

### ② 一次性安全发布

```java
volatile Resource resource;

// 线程 A
resource = new Resource(a, b, c);      // volatile 写 → 之前的所有写对读者可见

// 线程 B
if (resource != null) resource.use();  // 能完整看到 a/b/c 的效果
```

### ③ 独立观察（定期发布的指标）

```java
volatile long lastUpdateTime;
// 写线程定期更新，读线程只读最新值
```

## 六、volatile 不适用的场景（常见误用）

```java
// ❌ 误用 1：复合操作
volatile int count;
count++;                    // 三步：读-改-写，会丢失更新 → 用 AtomicInteger / LongAdder

// ❌ 误用 2：依赖当前值
volatile boolean flag;
if (!flag) flag = true;     // check-then-act 有竞态 → 用 AtomicBoolean.compareAndSet

// ❌ 误用 3：多个 volatile 变量之间的一致性
volatile int a, b;
// 线程 A: a = 1; b = 2;
// 线程 B: if (b == 2) assert a == 1;   // ❌ 不保证！volatile 只保证各自可见，不保证相互排序
```

> ⚠️ **误用 3 是最隐蔽的**：volatile 保证"看到最新值"，但**不保证两个 volatile 变量之间的操作顺序**在对方看来是一致的。
> 需要多变量一致性时，用锁或把变量打包成一个不可变对象 + `volatile` 引用。

## 七、volatile vs 锁 vs 原子类

| 需求 | 方案 |
| --- | --- |
| 单写多读的标志位 | **`volatile`** ✅ |
| 读-改-写（如 `i++`） | `AtomicInteger` / `LongAdder` |
| check-then-act | `AtomicXxx.compareAndSet` / 锁 |
| 多变量一致性 | 锁 / 打包成不可变对象 + volatile 引用 |
| 需要等待/通知 | 锁 + `Condition` / `CountDownLatch` |

## 八、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| **JDK 5（JSR 133）** | 🔴 **volatile 语义被强化**（获得 acquire/release 语义）；此前 volatile 几乎无用 |
| JDK 8 | `StampedLock.tryOptimisticRead()` —— 一种"更弱的 volatile 读" |
| **JDK 9** | 🔴 **`VarHandle`（JEP 193）**：提供 `opaque` / `acquire` / `release` / `volatile` 五档，volatile 只是最强的一档 |
| JDK 9+ | JUC 内部大量改用 `VarHandle` 的 `opaque`/`release`（比 volatile 便宜） |
| JDK 21+ | 虚拟线程**不改变** volatile 语义 |

### VarHandle 的 5 档内存语义（JDK 9+，性能调优的关键）

| 模式 | 语义 | 开销（x86） | 典型用途 |
| --- | --- | --- | --- |
| `getPlain`/`setPlain` | 普通读写 | 0 | 单线程/已由其他方式保证 |
| `getOpaque`/`setOpaque` | 原子，但**不排序** | ~0 | 计数器、进度条、取消标志 |
| `getAcquire`/`setRelease` | 单向屏障 | 低 | 发布-消费 |
| `getVolatile`/`setVolatile` | 完整 volatile | **写很贵** | 需要 happens-before 传递 |

> **实践要点**：如果你只需要"别的线程最终能看到这个值"（如统计计数、取消标记），
> **`setOpaque` 就够了，比 `volatile` 便宜得多**。这是 JDK 9 后 JUC 内部性能提升的主要来源之一。

## 九、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| **volatile 语义的权威规范** | **JSR 133: Java Memory Model and Thread Specification** | 2004（§3.1.4 专门定义 volatile） |
| JMM 的形式化 | **Manson, Pugh, Adve, *The Java Memory Model*** | **POPL 2005** |
| 旧 volatile 为什么不够 | **Pugh, *The Java Memory Model is Fatally Flawed*** | Concurrency: Practice and Experience, 2000 |
| **DCL 失效** | **Bacon, Block, Bogda, Coward, Grove, Mitchell, Ngo, Pugh 等, *The "Double-Checked Locking is Broken" Declaration*** | 2000-2001（由 Bill Pugh 维护的著名声明） |
| 内存模型教程 | **Adve & Gharachorloo, *Shared Memory Consistency Models: A Tutorial*** | **IEEE Computer 29(12), 1996** |
| release consistency | Gharachorloo et al., *Memory Consistency and Event Ordering in Scalable Shared-Memory Multiprocessors* | ISCA 1990 |
| x86 内存模型的形式化 | **Sewell et al., *x86-TSO: A Rigorous and Usable Programmer's Model for x86 Multiprocessors*** | **CACM 53(7), 2010** —— 解释为什么 x86 上 volatile 读免费 |
| ARM 内存模型 | Alglave, Maranget, Tautschnig, *Herding Cats: Modelling, Simulation, Testing, and Data-mining for Weak Memory* | TOPLAS 36(2), 2014 |
| 教材 | Herlihy & Shavit, *The Art of Multiprocessor Programming* | 2008/2012 |

## 十、近年研究与工业界前沿（2020-2026）

**同行评审论文**

- **RISC-V 内存模型（RVWMO）的形式化**（2020 前后完成）：所有主流 ISA 现已都有精确公理化模型，
  工具链为 **herd7**。这让"这段代码在 ARM 上会不会出问题"变成可以**机器验证**的问题。
- **JIT 编译在弱内存模型下的正确性**：证明 C2 的重排优化不违反 JMM（PLDI / OOPSLA 近年工作）。

**工业界资料（非同行评审）**

- **OpenJDK `jcstress`**：验证 volatile 语义的**唯一可信工具**，它会穷举线程交织。
  ```bash
  java -jar tests-all/target/jcstress.jar -t ".*Volatile.*"
  ```
  https://github.com/openjdk/jcstress
- **Aleksey Shipilëv 的 *Java Memory Model Pragmatics***：工程向讲得最清楚的材料，
  含"volatile 到底插了什么指令"的实测数据。
- **`jctools` / `Disruptor` 的 `VarHandle` 用法**：工业级高性能代码如何用 `opaque`/`release`
  替代 volatile 以获得吞吐。https://github.com/JCTools/JCTools
- **JOL**：观察对象布局与伪共享。https://github.com/openjdk/jol

## 十一、常见误区（本书 2.6 需修正之处）

1. **❌「volatile 保证原子性」** —— 最经典的误解。只保证可见性与有序性。
2. **❌「volatile 很慢，要少用」** —— **x86 上 volatile 读几乎免费**，只有写贵。盲目避免 volatile 反而会写出 bug。
3. **❌「DCL 不加 volatile 也行，我测过没问题」** —— x86 上难复现，**ARM 上会真实失败**。
4. **⚠️ 多个 volatile 变量之间没有相互排序保证** —— 见第六节误用 3。
5. **⚠️ 本书未覆盖 `VarHandle`**（JDK 9+）。需要"最终可见但不需要 happens-before"时，
   `setOpaque` 比 volatile 便宜得多（见第八节）。
6. **❌「64 位的 `long`/`double` 读写不是原子的，所以要 volatile」** —— 部分正确：
   **非 volatile 的 long/double 确实可能被拆成两个 32 位操作**（JLS §17.7 允许），
   volatile 可以修复它，但更常见的是用 `AtomicLong`。
7. **⚠️ volatile 数组**：`volatile int[] arr` 只保证**数组引用**的可见性，**不保证元素**！
   元素可见性要用 `AtomicIntegerArray` 或 `VarHandle`。这是极常见的坑。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

# volatile 与内存可见性

> **`volatile` 同时提供"可见性"（写立刻刷新到主存）和"禁止重排序"（编译期与 CPU 屏障两层），并让 `long/double` 的单次读写具备原子性；但它不保证复合操作（如 `i++`）的原子性。**

## 一、是什么（最小可运行示例）

```java
public class VolatileDemo {
    static volatile boolean stop = false;        // 去掉 volatile，循环可能永远不退出
    static volatile int count = 0;               // volatile 也救不了 count++ 的原子性

    public static void main(String[] args) throws Exception {
        Thread t = new Thread(() -> {
            int n = 0;
            while (!stop) n++;                   // 无 volatile 时可能被 JIT 提升为 if(!stop) while(true){}（.rodata 提升）
            System.out.println("退出，自旋次数=" + n);
        });
        t.start();
        Thread.sleep(1000);
        stop = true;                             // 主线程写 → 读线程必须能看到
        t.join();

        Runnable inc = () -> { for (int i = 0; i < 100_000; i++) count++; };
        Thread a = new Thread(inc), b = new Thread(inc);
        a.start(); b.start(); a.join(); b.join();
        System.out.println("count=" + count);    // 几乎必然 < 200000：读-改-写不是原子操作
    }
}
```

去掉 `stop` 的 `volatile` 后，JIT 可以把只读不写的循环条件提升到循环外（hoisting），线程永远看不到主线程的写入；加上后每次读都从主存/一致性缓存取。而 `count++` 编译成"读 → 加一 → 写"三条指令，两个线程会互相覆盖，此时需要 `AtomicInteger` / `LongAdder` / 锁。

## 二、实现原理（深入一层）

**语言层（JMM / JSR-133）**：对同一个 volatile 变量，**写 happens-before 后续读**；再配合传递性，volatile 写之前的所有普通写，对之后的 volatile 读也可见 —— 这是它比"刷新主存"更强的真正原因。

**编译器层**：按 JSR-133 Cookbook for Compiler Writers 插入屏障：

| 操作 | 前面需要 | 后面需要 |
| --- | --- | --- |
| volatile 读 | — | LoadLoad + LoadStore |
| volatile 写 | StoreStore + LoadStore | StoreLoad |

**CPU 层（HotSpot x86-64）**：x86 是 TSO 内存模型，LoadLoad/LoadStore/StoreStore 天然成立，所以只需处理 StoreLoad：

```
volatile 读 → mov  reg, [addr]              ; 普通 load，无屏障
volatile 写 → mov  [addr], reg
              lock addl $0x0, (%rsp)        ; StoreLoad，实为 full barrier（锁总线/缓存行）
```

即 **x86 上 volatile 写远比读昂贵**（约几十个周期），这也是无竞争 `volatile` 读几乎免费的原因。**aarch64** 上则映射为 `ldar`（读-获取）/ `stlr`（写-释放），不需要 `dmb` 全屏障。

**原子性**：JSR-133（JDK 5）起，`volatile long/double` 的**单次**读/写在 32 位平台上也不撕裂；但 `volatile` 不提供任何"读-改-写"原子性。

## 三、JDK 版本演进

| 版本 | 与本主题相关的变化 |
| --- | --- |
| JDK 8 | JSR-133 语义（JDK 5 定稿，本书基线）；JEP 171 引入 `Unsafe.loadFence/storeFence/fullFence` 三个内存屏障内建方法；`StampedLock`、`ConcurrentHashMap` 大量依赖 volatile 读做无锁快路径 |
| JDK 9 | 🔴 **JEP 193 VarHandle**：提供 `getVolatile/setVolatile` 之外新增 `getOpaque/setOpaque`（无顺序、仅原子与可见性最终性）与 `getAcquire/setRelease`（单向顺序）—— 比 volatile 更弱/更精确，是 JDK 内部替换 Unsafe 的统一入口 |
| JDK 11 | 语义无变化；aarch64 后端用 `ldar/stlr` 实现 volatile，ARM 上 release/acquire 与 volatile 代码序列几乎一致 |
| JDK 17 | JEP 403 强封装 JDK 内部；volatile 语义与屏障策略不变 |
| JDK 21 | 🔴 **JEP 444 虚拟线程**：JMM 对虚拟线程完全适用（虚拟线程只是调度单位，共享同一套内存模型）；但虚拟线程内调用 `synchronized` 曾导致钉住载体线程 |
| JDK 23 / 24 | 🔴 **JEP 471 / JEP 498** 逐步废弃 `sun.misc.Unsafe` 的内存访问方法：手写 fence 与 volatile 语义请改用 `VarHandle` 的 `fullFence/acquireFence/releaseFence` 及 release/acquire/opaque 访问模式 |
| JDK 25 | 🔴 **JEP 506 ScopedValue 转正**：绑定后不可变，跨任务只读共享，从设计上减少"用 volatile 发布可变共享状态"的需求 |

## 四、经典论文

| 主题 | 文献（作者, 标题, 会议/期刊 + 年份） | 出处/备注 |
| --- | --- | --- |
| Java 内存模型官方形式化 | Manson, Pugh & Adve, *The Java Memory Model*, POPL 2005 | JSR-133 的权威论文，定义 volatile 的 happens-before 语义 |
| volatile 运行的硬件模型 | Sewell, Sarkar, Owens, Nardelli & Myreen, *x86-TSO: A Rigorous and Usable Programmer's Model for x86 Multiprocessors*, CACM 53(7), 2010 | 解释为何 x86 上只需 StoreLoad 屏障（TPHOLs 2009 原版，CACM 为普及版） |
| 一致性模型综述 | Adve & Gharachorloo, *Shared Memory Consistency Models: A Tutorial*, IEEE Computer 29(12), 1996 | 系统讲解 TSO/PSO/RMO 与屏障代价 |
| happens-before 概念源头 | Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*, CACM 21(7), 1978 | "happens-before"一词的出处 |
| 顺序一致性定义 | Lamport, *How to Make a Multiprocessor Computer That Correctly Executes Multiprogram Programs*, IEEE Trans. Computers 28(9), 1979 | SC 模型与"足够强的屏障"的经典论证 |
| 弱序化动机 | Adve & Hill, *Weak Ordering — A New Definition*, ISCA 1990 | 说明为什么硬件要给"部分有序"留出重排空间 |
| 屏障插入规则 | Doug Lea, *The JSR-133 Cookbook for Compiler Writers* | 技术备忘录（非论文），实际实现的屏障表来源 |

## 五、近年研究与工业界实践（2020-2026）

**同行评审论文**

- Kang, Hur, Lahav & Vafeiadis, *A Promising Semantics for Relaxed-Memory Concurrency*, POPL 2017（经典），及其后续一脉工作（2020-2025 持续推进）：把 Java/C++ 的 release-acquire、opaque 这类"弱于 volatile"的访问模式给出可组合的操作语义，直接对应 JDK 9 VarHandle 的 `getAcquire/setRelease/getOpaque`。
- Watt, Pulte, Podkopaev, Barbier, Dolan, Flur, Pichon-Pharabod & Guo, *Repairing and Mechanising the JavaScript Relaxed Memory Model*, PLDI 2020（展示如何用模型检验器修复/验证一个工业级内存模型，是 JMM 类规范工程化的方法论样本）。

**工业界资料（非同行评审）**

- [openjdk/jcstress](https://github.com/openjdk/jcstress)：OpenJDK 官方并发压力测试套件，验证 volatile 发布、安全初始化等 JMM 契约；是唯一能真正"证伪"内存可见性直觉的工具。
- [openjdk/jdk](https://github.com/openjdk/jdk)：`java.lang.invoke.VarHandle` 与各 `@HotSpotIntrinsicCandidate` 实现；`src/hotspot` 下 C2 的屏障插入逻辑。
- [openjdk/jmh](https://github.com/openjdk/jmh)：volatile 读/写、release/acquire、opaque 的开销对比必须用它测。
- [LMAX-Exchange/disruptor](https://github.com/LMAX-Exchange/disruptor)：靠 volatile sequence 发布 + 内存屏障做到无锁高吞吐，是 volatile 语义最著名的工业用例。
- [openjdk.org/jeps/0](https://openjdk.org/jeps/0)：JEP 193 / 471 / 498 / 506 原文。

## 六、常见误区 / 与其他语言对比

- ❌ **"volatile 保证原子性"** —— 只保证单次读写的可见性与原子（long/double），`i++`、`if (x==0) x=1` 这类复合操作仍需 CAS 或锁。
- ❌ **"volatile 变量写回主存，所以其他线程立刻读到新值"** —— JMM 不谈"主存/工作内存"的物理刷新，只谈 happens-before 边；现代 CPU 上数据大多仍在缓存中通过一致性协议传播。
- ❌ **"volatile 可以替代锁"** —— 只有"一个线程写、其他线程读"或"写入不依赖当前值"时才成立；多写者且读改写必须 CAS/锁。
- ⚠️ **"用 volatile 数组/对象，元素就可见"** —— volatile 只修饰**引用本身**，数组元素和对象字段没有 volatile 语义。
- ⚠️ **"volatile 万能发布"** —— volatile 只保证发布时的可见性；若对象在构造后仍被修改且无同步，仍然不安全（安全发布 ≠ 不可变）。
- ⚠️ **过度使用 volatile** —— 在 x86 上 volatile 写会插入 `lock` 前缀指令，热路径上应评估 `setRelease/getAcquire` 或 `setOpaque` 是否足够。

| 语言 | volatile 的等价物与语义 |
| --- | --- |
| Java | `volatile` 字段：语言级可见性 + 禁止重排序 + happens-before；`VarHandle` 另有 acquire/release/opaque 分级 |
| C++ | `volatile` **不具备线程语义**（只阻止编译器优化，不生成屏障、不保证可见性）；并发请用 `std::atomic` + `std::memory_order` |
| Rust | 同 C++：`std::ptr::read_volatile/write_volatile` 仅用于 MMIO/信号处理；并发用 `Atomic*` + `Ordering::Acquire/Release/SeqCst` |
| Go | 无 volatile 关键字；Go 1.19+ 提供类型化 `atomic.Int64` 等，`sync/atomic` 提供顺序一致（seq-cst）语义 |
| Erlang/OTP | 无共享可变内存；进程间消息传递天然传递值拷贝，可见性问题不存在 |
| Python | 无 volatile；CPython 靠 GIL 保证字节码级执行（但**不是**内存模型保证）；跨线程发布请用 `Lock`/`queue`；3.13 起的 free-threaded 构建更需显式同步 |
