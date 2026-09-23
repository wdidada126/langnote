# JMM 与 happens-before

> 定位：《Java并发编程之美》第 2 章 2.4（内存可见性）、2.7（原子性）、2.10（指令重排序）三节的**理论基础**。
> 一句话：**JMM（Java Memory Model）回答的是"一个线程写入的值，另一个线程什么时候、能否看到"**。它不是一个物理内存模型，而是一套**给编译器和 CPU 定的规则**：哪些重排允许、哪些必须禁止。

## 一、是什么（最小可运行示例）

```java
class Visibility {
    static boolean ready = false;      // 普通字段，非 volatile
    static int data = 0;

    public static void main(String[] args) {
        new Thread(() -> { data = 42; ready = true; }).start();      // 写线程
        new Thread(() -> { while (!ready) {} System.out.println(data); }).start();  // 读线程
    }
}
```

这段代码的合法结果包括：
- 打印 `42`（我们看到的最常见结果）
- **死循环**（读线程永远看不到 `ready == true`）
- 理论上打印 `0`（若发生重排，`ready = true` 先于 `data = 42` 生效——注意：普通字段间无 happens-before，CPU/编译器可重排）

**没有 happens-before 就没有可见性保证**。加上 `volatile boolean ready` 后，程序就**必然**打印 42（volatile 写 → volatile 读 建立 happens-before）。

## 二、实现原理（深入一层）

**1）为什么会有可见性问题**

| 层次 | 造成的重排/不可见 |
| --- | --- |
| **编译器**（javac / C2 JIT） | 指令调度、循环外提、把变量缓存到寄存器、消除"看似无用"的读 |
| **CPU 乱序执行** | Store Buffer、Load Buffer、乱序发射、推测执行 |
| **缓存层次** | 各核 L1/L2 独立，写先落在 store buffer，未及时对其他核可见 |
| **写缓冲与内存屏障** | x86 只有 StoreLoad 重排（TSO）；ARM/POWER 允许几乎所有重排 |

**2）happens-before 的 8 条规则（JLS §17.4.5）**

| 规则 | 说明 |
| --- | --- |
| ① **程序顺序规则** | 同一线程内，前面的操作 happens-before 后面的操作 |
| ② **volatile 规则** | volatile 写 happens-before 后续对该变量的 volatile 读 |
| ③ **监视器锁规则** | `unlock` happens-before 后续对同一锁的 `lock` |
| ④ **线程启动规则** | `Thread.start()` happens-before 该线程的任何动作 |
| ⑤ **线程终止规则** | 线程中的任何动作 happens-before 其他线程检测到它终止（`join()` 返回、`isAlive() == false`） |
| ⑥ **中断规则** | 调用 `interrupt()` happens-before 被中断线程检测到中断 |
| ⑦ **传递性** | A hb B 且 B hb C ⇒ A hb C |
| ⑧ **对象终结规则** | 构造器结束 happens-before `finalize()` 开始 |

**注意**：happens-before **不等于**"时间上先发生"。它只是一个**偏序关系**，用来保证可见性。"A hb B" 意味着 A 的结果对 B 可见；但两个没有 hb 关系的操作，**JVM 可以按任意顺序执行，甚至看起来"未来先发生"**（只要不违反 intra-thread 语义）。

**3）`volatile` 的实现（内存屏障）**

JMM 规定 volatile 写之前的操作不能被重排到写之后（StoreStore + LoadStore），volatile 读之后的操作不能被重排到读之前（LoadLoad + LoadStore），且 volatile 写与后续 volatile 读之间需要 **StoreLoad 屏障**。

HotSpot 在 x86 上的实现：

```
volatile 写：  mov [addr], val ; lock addl $0,(%rsp)   ← lock 前缀指令即 StoreLoad 屏障
volatile 读：  mov eax, [addr]                          ← x86 TSO 下 load 本身不重排，无需额外屏障
```

在 **ARM/AArch64** 上则要用 `dmb ish`（数据内存屏障）或 `stlr`/`ldar`（store-release / load-acquire），这也解释了**为什么在 x86 上跑对的并发代码，搬到 ARM 服务器（鲲鹏、Ampere、Graviton）上可能出错**。

**4）`final` 字段的特殊保证**：JMM 对 `final` 提供了**初始化安全**——只要对象在构造期间没有逸出（`this` 没泄露），其他线程无需同步就能看到正确初始化的 final 字段。这是 `java.time` 不可变类、`String`、以及安全发布（safe publication）的理论基石。

**5）安全发布的四种方式**（Goetz《Java Concurrency in Practice》）：
- 在静态初始化器中初始化（`static final`）
- `volatile` / `AtomicReference` 引用
- 放入 `final` 字段
- 放入由锁保护的字段 / 并发容器（`ConcurrentHashMap`）

## 三、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| **JDK 1.4 及之前** | 旧的 JMM（JLS 第 1 版）有严重缺陷：允许"final 字段被重排导致看到默认值"、volatile 语义过弱 |
| **JDK 5（JSR 133）** | **现代 JMM 诞生**：重新定义 volatile/final/happens-before，修复了双重检查锁定（DCL）问题——这也是"DCL 单例在 JDK 5 之后才真正可用"的原因 |
| JDK 8 | `StampedLock`、`LongAdder`、VarHandle 前身的 `Unsafe` 内存序；JMM 本身未变 |
| **JDK 9（JEP 193）** | **`VarHandle`** 引入，提供比 volatile 更细的内存序：`plain` / `opaque` / `acquire` / `release` / `volatile` 五档 |
| JDK 9 | JEP 260 封装 `Unsafe`（为后续退役做准备） |
| JDK 14 | JEP 370 外部内存访问 API（孵化） |
| JDK 21/22 | JEP 442/454 `MemorySegment` + `VarHandle` 成为堆外内存访问的正道 |
| **JDK 21（JEP 444）** | 虚拟线程——**不改变 JMM**（虚拟线程与平台线程遵循同一套内存模型，这是 Loom 的重要设计约束） |
| JDK 23/24 | JEP 471 弃用 `Unsafe` 内存访问方法；JEP 498 使用时告警 |
| JDK 25 | JEP 506 `ScopedValue` 正式化——同样不引入新的内存序语义 |

**VarHandle 的五档内存序**（JDK 9+，比 volatile 更精细）：

| 模式 | 语义 | 典型用途 |
| --- | --- | --- |
| `plain` | 无屏障，与普通字段访问一致 | 只在已知有外部同步时用 |
| `opaque` | 保证"对同一变量的访问按程序顺序"，不保证与其他变量的顺序 | 自旋标志、无锁数据结构里的进度保证 |
| `release/acquire` | 单向屏障（release 写 / acquire 读），**比 volatile 便宜** | 生产者-消费者：写端 release，读端 acquire |
| `volatile` | 完全双向，等价 `volatile` 字段 | 通用 |

```java
private static final VarHandle STATE;
static { try { STATE = MethodHandles.lookup()
    .findVarHandle(MyClass.class, "state", int.class); } catch (...) {...} }
STATE.setRelease(this, 1);        // release 写
int s = (int) STATE.getAcquire(this);  // acquire 读
```

## 四、经典论文

| 论文 | 出处 | 关联 |
| --- | --- | --- |
| **Manson, Pugh & Adve, *The Java Memory Model*** | POPL 2005 | **JMM 的正式定义**（JSR 133 的学术输出），happens-before 因果模型的论文版 |
| **Pugh, *The Java Memory Model is Fatally Flawed***（系列批评文章，1999-2000） | — | 推动 JMM 重写；指出旧模型中"final 可见性"与"volatile 一致性"的缺陷 |
| **Adve & Gharachorloo, *Shared Memory Consistency Models: A Tutorial*** | IEEE Computer 1996 | 内存一致性模型的入门经典（顺序一致性 / TSO / PSO / 释放一致性） |
| **Lamport, *How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs*** | IEEE TC 1979 | **顺序一致性（Sequential Consistency）** 的定义 |
| **Sewell 等, *x86-TSO: A Rigorous and Usable Programmer's Model for x86 Multiprocessors*** | CACM 2010 | x86 实际内存模型的精确描述（用 HOL4 / Coq 机器验证） |
| **Herlihy & Wing, *Linearizability: A Correctness Condition for Concurrent Objects*** | TOPLAS 1990 | 与 SC 的区别：linearizability 针对**单个对象**，SC 针对**整个执行** |
| **Boehm & Adve, *Foundations of the C++ Concurrency Memory Model*** | PLDI 2008 | C++11 内存模型（与 JMM 最重要的对照物，见跨语言部分） |

## 五、近年研究与工业界实践（2020-2026）

**研究侧**：
- **弱内存模型的形式化**：ARMv8（Pulte 等 POPL 2018）与 **RISC-V 内存模型**（Lahav 等 PLDI 2021-2024）的形式化工作，直接影响了 JVM 在这些平台上的屏障指令选择。近年还有 *Promising Semantics*（Kang, Hur 等 POPL 2017 起）与 *Weakestmo* 等框架用于推理 Java/C++ 的松弛访问。
- **JMM 本身的修订讨论**：OpenJDK 有 JMM 现代化的讨论（JEP 草案层面），方向是引入更明确的 `opaque`/`release`/`acquire` 到语言层面（目前只有 VarHandle 有）；学界也在讨论 **JMM 与 C++ 内存模型的对齐**（2023-2025 有多篇对比与互操作研究）。
- **并发缺陷的实证研究**：ICSE/FSE 2021-2024 的多项研究发现，Java 项目里的并发 bug 中，最常见类型仍是"误以为有 happens-before"（如用普通 boolean 做停止标志），与 20 年前同类型研究结论一致——说明 **JMM 的心智负担并没有随时间减轻**。

**工业界**：

| 工具 | 地址 | 用途 |
| --- | --- | --- |
| **jcstress** | https://github.com/openjdk/jcstress | OpenJDK 官方并发正确性测试工具，能**实证**重排是否发生（带 `IR` 结果分析） |
| **JMH** | https://github.com/openjdk/jmh | 测量屏障开销 |
| **VMLens / Relacy** | https://github.com/vmlens/vmlens · Relacy Race Detector | Java 并发的模型检查 |
| **TSAN / ThreadSanitizer** | LLVM/Google | 主要用于 C/C++，但思想（happens-before 动态检测）值得借鉴 |
| **Dragonwell / 毕昇 JDK / GraalVM** | Alibaba / Huawei / Oracle | 各厂商 JDK 在 ARM 上的屏障实现差异（如 `-XX:+UseBarriersForVolatile`） |

## 六、常见误区 + 跨语言对照

**常见误区**：

1. ❌ "`volatile` 能保证原子性" → 不能。它只保证**可见性 + 禁止重排**，`i++` 这样的复合操作仍需要锁或原子类。
2. ❌ "`volatile` 比锁快，能替代锁" → 只有在"单写多读 / 状态标志"场景才成立；一旦需要复合操作就必须加锁。
3. ❌ "happens-before = 时间先后" → 它是**可见性偏序**，不是时间序。两个无 hb 关系的操作，JVM 可以任意重排。
4. ❌ "`synchronized` 退出后所有修改都可见" → 只对**同一个锁**成立。用不同锁保护同一个变量等于没保护。
5. ❌ "64 位 long/double 的读写是原子的，所以不用管" → JLS 允许非 volatile 的 long/double 读写被拆成两个 32 位操作（**word tearing**），虽然现代 JVM 实际都实现了原子，但**规范不保证**——用 `volatile long` 或 `AtomicLong` 才安全。
6. ❌ "构造完对象再赋给共享引用就一定能安全发布" → 需要 `final`/`volatile`/锁/静态初始化/并发容器之一，否则可能有**部分构造的对象**被其他线程看到（著名的 DCL 单例 bug）。
7. ❌ "虚拟线程改变了内存模型" → 没有。虚拟线程与平台线程遵循同一套 JMM（JEP 444 明确说明）。

**跨语言对照（内存模型）**：

| 语言 | 内存模型 | 关键差异 |
| --- | --- | --- |
| **Java** | **happens-before（因果/释放一致性）**，JSR 133（JDK 5） | 对"数据竞争"给出**明确定义**：无竞争的程序保证顺序一致（DRF-SC）；有竞争时不保证 |
| **C/C++11** | **release/acquire + 松弛原子**，Boehm & Adve (PLDI 2008) | 提供 `memory_order_relaxed/consume/acquire/release/acq_rel/seq_cst` **六档**；`seq_cst` ≈ Java 的 volatile 全序；**允许写出有数据竞争也未定义行为的程序** |
| **Rust** | **直接复用 C++20 的内存模型**（LLVM 后端），`std::sync::atomic::Ordering` | 靠所有权 + `Send/Sync` **在编译期消除大部分数据竞争**；unsafe 代码才需要手动选 Ordering |
| **Go** | Go Memory Model（2022 年正式修订，Russ Cox 的三篇系列文章） | 同样采用 DRF-SC：**无竞争的程序表现为顺序一致**；`sync` 包与 channel 是主要同步手段；go 语句的启动建立 hb |
| **C#/.NET** | CLI 内存模型 + ECMA-335 | 历史上比 Java 弱，.NET Core 后收紧；`Interlocked`/`Volatile` 类 |
| **Erlang/BEAM** | **无共享内存** | 根本不需要内存模型 |

**最重要的对照结论**：

> **DRF-SC（Data-Race-Free ⇒ Sequential Consistency）** 是 Java（JSR 133）、C++11、Go、Rust 内存模型的**共同底线**：只要你的程序没有数据竞争，它就表现得像是顺序执行的。这条性质是"写并发代码还能保持理智"的根本原因——一旦出现数据竞争，Java 至少还有定义（不会像 C++ 那样是 UB），但结果不可预测。

## 七、一页纸总结

- **JMM 是规则不是硬件**：它约束编译器与 CPU 的重排，向上提供 happens-before 保证。
- **8 条 happens-before 规则**是判断"能不能看到"的唯一依据；传递性是推理的常用手段。
- **volatile = 可见性 + 禁止重排 ≠ 原子性**；`final` 提供初始化安全。
- **安全发布四法**：static 初始化 / volatile / final 字段 / 加锁或并发容器。
- JDK 9+ 有 **VarHandle 五档内存序**（plain < opaque < release/acquire < volatile），比无脑 volatile 更快。
- x86（TSO）上很多 bug 不复现，**ARM/RISC-V 上会暴露**——别拿 x86 当标准。
- 判断工具：**jcstress** 实证重排、**JMH** 测开销、静态检查抓"未同步的共享可变状态"。
