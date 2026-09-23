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
