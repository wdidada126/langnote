# 专篇：Java 内存模型与 happens-before

> 对应本书 2.4 / 2.6 / 2.10 节。**JMM 是整个 Java 并发正确性的地基**——
> 它回答一个看似简单、实则极难的问题：**"线程 A 的写入，线程 B 什么时候能看到？"**

## 一、一句话概括

JMM 是一套 **"在什么条件下，一个线程的写操作对另一个线程可见"** 的**契约**（不是硬件模型本身）。
它由 **happens-before 规则** 定义：**如果 A happens-before B，那么 A 的结果对 B 可见**。

编译器与 CPU 可以自由重排、可以延迟写回缓存——**只要不违反 happens-before**。
这是"给程序员一个强保证，给硬件留最大优化空间"的经典设计。

## 二、为什么需要它：三个"反直觉"的真实来源

```java
// 共享变量，无任何同步
int a = 0; boolean flag = false;

// 线程 A
a = 1;            // 写
flag = true;      // 写

// 线程 B
if (flag) {       // 读
    assert a == 1;  // ❌ 可能失败！
}
```

这段"显然正确"的代码**在缺少同步时可能失败**，原因有三：

1. **编译器重排**：`a = 1` 与 `flag = true` 无数据依赖，JIT 可能调换顺序
2. **CPU 乱序执行**：即使编译期不重排，CPU 也可能乱序提交
3. **写缓冲与缓存一致性延迟**：`flag = true` 刷到主存时，`a = 1` 可能还在 store buffer 里

> 在 **x86（TSO 模型）** 上，store-store 重排不会发生，这段代码实际上很难复现失败；
> 但在 **ARM / RISC-V / Power（弱内存模型）** 上**会真实失败**。
> 这正是"我的机器跑了一百万次都没问题"这种经验主义最危险的地方——
> **换 CPU 架构就可能崩**。

## 三、happens-before 的八条规则（JLS §17.4.5）

| # | 规则 | 说明 |
| --- | --- | --- |
| 1 | **程序顺序规则** | 同一线程内，前面的操作 happens-before 后面的操作（**仅针对有依赖的**） |
| 2 | **volatile 变量规则** | 对 volatile 变量的**写** happens-before 后续对该变量的**读** |
| 3 | **锁规则（监视器锁）** | 解锁 happens-before 后续对同一锁的加锁 |
| 4 | **传递性** | A hb B 且 B hb C ⇒ A hb C |
| 5 | **线程启动规则** | `Thread.start()` happens-before 该线程内的任何操作 |
| 6 | **线程终止规则** | 线程内的任何操作 happens-before 其他线程通过 `join()` / `isAlive()` 检测到它终止 |
| 7 | **中断规则** | 对线程 `interrupt()` 的调用 happens-before 被中断线程检测到中断 |
| 8 | **对象终结规则** | 对象构造完成 happens-before 其 `finalize()` 开始 |

**外加**（JUC 补充）：

| 规则 | 说明 |
| --- | --- |
| `volatile` 的传递性用法 | A 写 volatile v ← B 读 v，则 A 在写 v 之前的**所有**操作对 B 可见 |
| 并发容器的隐含保证 | 将对象放入 `ConcurrentHashMap`/`BlockingQueue` happens-before 从它取出的操作 |
| `CountDownLatch` / `CyclicBarrier` | `countDown()` hb `await()` 返回后的操作 |
| `Future.get()` | 任务内的操作 hb `get()` 返回 |
| `AtomicXxx` 的 `volatile` 语义 | 同 volatile |

## 四、volatile 的两重语义

```java
volatile boolean flag;
```

| 语义 | 作用 |
| --- | --- |
| **可见性** | 写立即刷主存；读从主存读。等价于"每次读写都穿过缓存" |
| **禁止重排** | volatile 写**之前**的操作不能被重排到写之后；volatile 读**之后**的操作不能被重排到读之前 |

具体重排规则（JMM 的 volatile 语义）：

```
普通读/写  ⇄  volatile 写   →  ❌ 不可重排（写之前的不能跑到写后面）
volatile 读  ⇄  普通读/写   →  ❌ 不可重排（读之后的不能跑到读前面）
volatile 写  ⇄  volatile 读  →  ❌ 不可重排
```

**⚠️ 关键：volatile 不保证原子性。**

```java
volatile int count = 0;
count++;        // ❌ 仍然是 read-modify-write 三步，并发下丢失更新
```

> `volatile` 适合的场景只有一个半：
> ① **单写多读的状态标志**（如停机标志）
> ② 配合 happens-before 做"安全发布"（见第六节）

## 五、内存屏障：JMM 在硬件上的落地

JMM 是抽象模型，落到硬件靠内存屏障（JMM 定义了 4 种，硬件按能力实现）：

| JMM 屏障 | 作用 | x86 实现 |
| --- | --- | --- |
| `LoadLoad` | 禁止读-读重排 | `lfence`（x86 上通常是空操作，TSO 已保证） |
| `StoreStore` | 禁止写-写重排 | `sfence`（x86 上通常空操作） |
| `LoadStore` | 禁止读-写重排 | 通常空操作 |
| **`StoreLoad`** | **禁止写-读重排** | **`mfence` 或 `lock` 前缀指令** —— **唯一有实质开销的** |

> 这就是为什么 **volatile 写在 x86 上很贵**（需要 `StoreLoad` 屏障，约几十个时钟周期），
> 而 volatile 读几乎免费。也是为什么 **x86 上"写 volatile" 比 "读 volatile" 慢得多**。

## 六、安全发布（Safe Publication）——JMM 最实用的部分

**问题**：一个对象的引用被其他线程看到时，它的**字段**可能还没被看到（重排导致）。这就是"逸出"的半成品对象。

四种安全发布方式：

```java
// ① static 初始化（最安全，JVM 保证）
class Holder { static final Resource R = new Resource(); }

// ② volatile 引用
volatile Resource r;
void init() { r = new Resource(); }        // 写 volatile → 之前的所有写对读者可见

// ③ final 字段（JMM 专门保证：正确构造的对象，其 final 字段无需同步即可见）
class Holder { final Resource r; Holder() { r = new Resource(); } }

// ④ 加锁 / 并发容器
synchronized void init() { r = new Resource(); }
// 或 map.put(k, new Resource()) —— 放入并发容器 hb 取出
```

**⚠️ 双重检查锁定（DCL）的经典 bug**：

```java
// ❌ JDK 5 之前的 DCL 是坏的（volatile 语义不足）
class Singleton {
    private static Singleton instance;
    static Singleton get() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) instance = new Singleton();   // 可能逸出半成品
            }
        }
        return instance;
    }
}

// ✅ JDK 5+ 必须加 volatile
private static volatile Singleton instance;

// ✅ 更好的写法：静态内部类（JVM 保证初始化安全，零成本）
class Singleton {
    private Singleton() {}
    private static class Holder { static final Singleton I = new Singleton(); }
    static Singleton get() { return Holder.I; }
}
```

> DCL 是 JMM 历史上最著名的案例：它在 JDK 1.4 及之前**确实是坏的**，
> JDK 5 修复 volatile 语义后才可用。这也是"JSR 133 修订 JMM"的直接动因。

## 七、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 1.4 及之前 | **JMM 有缺陷**：volatile 语义太弱、final 字段无保证、DCL 失效 |
| **JDK 5（JSR 133）** | 🔴 **JMM 大修**：volatile 获得 acquire/release 语义、final 字段安全发布保证、`java.util.concurrent` 引入 |
| JDK 8 | `StampedLock`；`Unsafe` 的 `loadFence/storeFence/fullFence` |
| **JDK 9** | 🔴 **VarHandle**（JEP 193）：暴露 `opaque` / `acquire` / `release` / `releaseAcquire` / `volatile` 五档内存语义，比 volatile 更细粒度 |
| JDK 17 | JEP 403 强封装，`Unsafe` 受限 |
| JDK 23/24 | `Unsafe` 内存访问方法标记废弃（JEP 471/498），全面转 VarHandle |
| **JDK 21+** | 🔴 **虚拟线程不改变 JMM** —— happens-before 规则完全不变，虚拟线程只是改变了线程的成本模型 |

> ⚠️ **重要澄清**：虚拟线程**没有**放宽任何内存可见性保证。
> 但实践中容易出问题：以前"线程复用导致上一任务的写入被下一任务看到"这种**意外的**可见性（靠 `ThreadLocal` 或线程内缓存）
> 在虚拟线程下**不再可靠**——因为每个任务都是新线程。
> 换句话说：**虚拟线程把你过去侥幸依赖的隐式可见性拿走了**，代码若依赖它就会出错。

## 八、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| **JMM 的官方规范** | **JSR 133: Java Memory Model and Thread Specification** | 2004（JSR 133 专家组，成员含 Doug Lea、Bill Pugh、Jeremy Manson、Sarita Adve 等）—— **必读一手文献** |
| JMM 的设计说明 | **Manson, Pugh, Adve, *The Java Memory Model*** | **POPL 2005** —— JMM 形式化的官方论文 |
| 为什么旧 JMM 坏了 | **Pugh, *The Java Memory Model is Fatally Flawed*** | **Concurrency: Practice and Experience, 2000** —— 直接促成 JSR 133 的檄文 |
| DCL 的失效分析 | Bacon et al., *The "Double-Checked Locking is Broken" Declaration* | 2000-2001（Pugh 等维护的著名声明文档） |
| 内存模型理论 | **Adve & Gharachorloo, *Shared Memory Consistency Models: A Tutorial*** | **IEEE Computer 29(12), 1996** —— **内存模型领域最好的入门文献** |
| 顺序一致性 | **Lamport, *How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs*** | **IEEE TC 28(9), 1979** —— 顺序一致性的原始定义 |
| 线性一致性 | Herlihy & Wing, *Linearizability: A Correctness Condition for Concurrent Objects* | TOPLAS 12(3), 1990 |
| 释放一致性（JMM 的基础） | Gharachorloo et al., *Memory Consistency and Event Ordering in Scalable Shared-Memory Multiprocessors* | ISCA 1990 |
| 数据竞争自由 ⇒ 顺序一致 | **Adve & Hill, *A Unified Formalization of Four Shared-Memory Models*** | IEEE TPDS 4(6), 1993 —— **DRF-SC 定理**的出处，JMM 的核心理论支柱 |
| 教材 | Herlihy & Shavit, *The Art of Multiprocessor Programming* | 2008/2012（第 3 章讲内存模型） |

> **DRF-SC（Data-Race-Free ⇒ Sequential Consistency）是理解 JMM 的钥匙**：
> JMM 承诺——**只要你的程序没有数据竞争，它的行为就和顺序一致的一样**。
> 换句话说，**JMM 只对"正确同步的程序"给出强保证，对有数据竞争的程序几乎不保证任何事**。
> 这解释了为什么"没同步的代码看起来能跑"是危险的：它依赖的是未定义行为。

## 九、近年研究与工业界前沿（2020-2026）

**同行评审论文**

- **硬件内存模型的公理化（2018-2025）**：继 x86-TSO、ARMv8、POWER 的形式化模型之后，
  **RISC-V 内存模型（RVWMO）** 的形式化工作近年完成（2020 年前后），标志着所有主流 ISA 都有了精确模型。
  代表工作：Alglave, Maranget, Tautschnig 的 **herd7 工具链**（TOPLAS 2014 及后续）。
- **弱内存模型下的编译正确性**：证明 JIT 编译（尤其是 C2 的激进优化）在 ARM 上不违反 JMM，是近年的活跃方向（PLDI / OOPSLA）。

**工业界资料（非同行评审）**

- **OpenJDK `jcstress`**：**验证 JMM 结论的唯一可信工具**。本书所有关于可见性/重排的结论都应跑一遍。
  ```bash
  git clone https://github.com/openjdk/jcstress && cd jcstress
  mvn clean install -DskipTests
  java -jar tests-all/target/jcstress.jar -t ".*UnsafePublication.*"
  ```
  https://github.com/openjdk/jcstress
- **JMM 的 Pragmatic 讲解**：Aleksey Shipilëv 的 *Java Memory Model Pragmatics*（JPoint 2014 演讲与 slides），
  是"JMM 到底在说什么"讲得最清楚的工程向材料。
- **herd7 / diy7 工具**：形式化地探索内存模型行为。https://github.com/herd/herdtools7
- **JOL（Java Object Layout）**：观察对象布局、伪共享。https://github.com/openjdk/jol

## 十、常见误区（本书 2.4/2.6 需修正之处）

1. **❌「volatile 保证原子性」** —— 只保证可见性与禁止重排，`count++` 仍会丢失更新。
2. **❌「x86 上跑通就等于正确」** —— x86 是 TSO（较强），ARM/RISC-V 是弱模型。**必须按 JMM 写，不能按硬件猜。**
3. **❌「DCL 不加 volatile 也行」** —— 仅 JDK 5+ 且加了 volatile 才正确；更好的写法是静态内部类。
4. **⚠️ 本书对 happens-before 的"传递性"强调不足** —— 传递性才是 volatile 能做"安全发布"的根本原因。
5. **⚠️ 本书未覆盖 VarHandle**（JDK 9+）——它提供了比 volatile 更细的 5 档内存语义，
   在高性能无锁代码里（如 `ConcurrentLinkedQueue` 内部）广泛使用，`volatile` 只是其中最强的那一档。
6. **⚠️ `final` 字段的可见性保证是有条件的**：必须在构造函数内完成赋值，且**不得让 `this` 逸出**。
7. **❌「虚拟线程放宽了内存可见性」** —— 完全没有。但它移除了"线程复用带来的意外可见性"，依赖旧行为的代码会出错。
8. **⚠️ 不要靠"跑一百万次没出错"验证并发** —— 请用 `jcstress`，它会穷举各种交织。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

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
