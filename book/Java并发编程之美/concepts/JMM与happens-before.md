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
