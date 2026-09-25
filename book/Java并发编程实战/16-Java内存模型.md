# 第 16 章 Java 内存模型（原书 pp.278-296）

> 与 `concepts/JMM与happens-before.md`、`concepts/volatile与内存可见性.md` 三篇互锁。本章是"为什么需要 JMM"的理论篇；专篇是"规则表 + 硬件 + 坑"的速查篇。建议对照读。

## 一、本章地图

| 小节 | 主题 | 关键结论 |
| --- | --- | --- |
| 16.1 | 什么是内存模型 | 定义"多线程下什么读能看到什么写"——**可见性 + 重排的契约** |
| 16.2 | 发布 | **不安全发布**导致其他线程看到**部分构造对象**（`final`/线程封闭/volatile/锁 四种安全发布） |
| 16.3 | `final` 字段的语义 | `final` 字段的**正确构造保证**：发布后一定看到初始化值（JSR 133 修复前没有） |
| 16.4 | 迟重做与 `happens-before` | **happens-before 是 JMM 的核心偏序关系** |
| 16.5 | 安全初始化惯用法 | `final` 域 / 静态初始化器（JVM 保证线程安全）/ 双重检查锁定（DCL）的正确写法 |
| 16.6 | 双重检查锁定（DCL） | 经典反例：`volatile` 缺失导致读到**坏单例**；JDK 5+ 用 `volatile` 修复 |
| 16.7 | 原子性与可见性 | 32 位 JVM 上 `long`/`double` 非原子（JLS 17.7）；`volatile` 不保证复合操作原子 |

## 二、核心精讲

### 2.1 内存模型是什么（16.1）
- JMM 回答一个核心问题：**一个线程的写，另一个线程多久、如何能看到**。
- 没有 JMM，编译器的重排、CPU 的乱序执行、缓存一致性都会让"直觉上的顺序"失效。
- JMM 在**"程序员好理解"与"编译器/CPU 能优化"之间取平衡**——它不禁止所有重排，只禁止"会破坏 happens-before 的程序员可观察行为"的重排。

### 2.2 不安全发布（16.2）
- 反例：`this` 在构造函数里泄漏（启动线程 / 注册监听器 / 把 `this` 存到共享集合）→ 别的线程可能看到**字段还是默认值（0/null）**的对象。
- 四种**安全发布**方式：① 静态初始化器；② `volatile`/`AtomicReference`；③ 锁保护；④ 线程封闭（仅单线程碰）。

### 2.3 `final` 语义（16.3，JSR 133 重大修正）
- JSR 133 前：`final` 字段**没有**跨线程可见性保证 → 能看到默认值。
- JSR 133 后（`final` 字段在构造器里正确初始化、且 `this` 不泄漏）：**任何线程看到的一定是完全构造的对象**，引用的 `final` 字段值保证可见。
- 这是"不可变对象天然线程安全"的基石。

### 2.4 happens-before（16.4，详见 concepts/JMM）
- 八条规则（程序序 / 监视器锁 / volatile / 线程启动 / 线程终止 / 中断 / 终结器 / 传递性）构成偏序。
- 若 A *happens-before* B，则 A 的写对 B **可见且有序**。
- **没有 happens-before 关系的两操作 → 结果不确定（数据竞争）**。

### 2.5 安全初始化 + DCL（16.5 / 16.6）
- **静态初始化器最安全**：JVM 保证类初始化期间加锁，天然线程安全（延迟初始化占位类 idiom）。
- **DCL 的正确写法**（JDK 5+）：`private static volatile Singleton instance;`，`volatile` 阻断"构造重排到引用赋值之前"——否则别的线程可能拿到**已赋值但未构造完**的对象。
- 现代推荐：**直接 `static final` 或延迟占位类**，别写 DCL。

### 2.6 原子性（16.7）
- 除 `long`/`double`（非 volatile 时）的 64 位读写为两步、可能撕裂外，**JMM 保证所有读写是原子的**。
- **`volatile` 不保证 `i++` 原子**：它只保证可见+有序，不保证"读-改-写"整体（需 `Atomic*`）。
- 64 位 JVM 上 `long`/`double` 实际已是原子，但**规范仍允许撕裂**，写可移植代码应加 `volatile`。

## 三、版本演进

- **JDK 1.0–1.4**：**无正式 JMM**，语义靠直觉，DCL 等写法在不同 JVM 行为不一致。
- **JDK 5 (JSR 133, 2004)**：**正式、健壮的 JMM** 落地——`volatile` 升级为"读写全屏障的 acquire/release 语义"、`final` 有安全发布保证、DCL 靠 `volatile` 修复。这是并发编程的"宪法修订"。
- **JDK 9 (JEP 193)**：`VarHandle` 提供 5 档内存语义（plain/opaque/acquire/release/volatile），让程序员精确控制屏障强弱。
- **JDK 21–25**：`Unsafe` 废弃通道（JEP 471/498）→ 内存屏障走 `VarHandle`/`MemorySegment`；`ScopedValue`（JEP 506, JDK 25 GA）提供比 `ThreadLocal` 更安全的"不可变上下文传递"，绕开 `final` 发布的部分痛点。
- **虚拟线程**：JMM 对虚拟线程**完全适用**（虚拟线程不改变内存模型，只改变调度），DCL/可见性规则一字不改。

## 四、经典论文 / 原始文献

- **JSR 133 (Java Memory Model and Thread Specification Revision, 2004)**——**现代 JMM 的宪法**，必读。
- **Manson, Pugh, Adve, "The Java Memory Model" (POPL 2005)**——JSR 133 的形式化，获**PLDI 10-year 影响力**认可。
- **Pugh, "The 'Double-Checked Locking is Broken' Declaration" (2000)**——DCL 坏写法的权威申明。
- **Adve & Gharachorloo, "Shared Memory Consistency Models: A Tutorial" (IEEE Computer 1996)**——从顺序一致性到释放一致性，理解 JMM 为何"宽松"的理论背景。
- **Lamport, "How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs" (1979)**——**顺序一致性**定义源头。
- **Adve & Hill, "Weak Ordering—A New Definition" (ISCA 1990) / "A Unified Formalization" (TPDS 1993)**——**DRF-SC（Data-Race-Free ⇒ Sequential Consistency）定理**，JMM 的设计哲学基础。
- **Boehm & Adve, "Foundations of the C++ Memory Model" (PLDI 2008)**——C++11 / Java 宽松内存模型互通的理论。

## 五、近年研究与工业界前沿

### 5.1 内存模型的工程化验证
- **`openjdk/jcstress`**（2.1k★）——**专门模糊测试** JVM 内存模型实现与你的并发代码；提供现成 `Concurrent-Test` 模板（如验证 DCL、`final` 安全发布、volatile 语义）。工业界验证 JMM 假设的唯一标准工具。
- **`herd7` + `diy7`**（Cambridge, 配套 litmus tests）——用 **.litmus** 文件形式化描述弱内存交错，Java/C/C++ 通吃；Linux 内核的 memory model 也是它。
- **`openjdk/jol`**（Java Object Layout，2.1k★）——看对象头/字段布局/对齐填充，理解"为什么 volatile 字段会踩伪共享、为什么 `@Contended` 有用"。

### 5.2 弱内存模型的现实冲击
- **ARM/POWER 的弱内存**让"在 x86 上跑得好好的并发代码"在 ARM 服务器（AWS Graviton）上**翻车**——因为 x86 是 TSO（强），ARM 是真弱。jcstress 在多架构 CI 上跑是新的工业标配。
- **C/C++/Rust 的 `memory_order`**（acquire/release/relaxed/seq_cst）与 Java 的 `VarHandle` 5 档一一对应，跨语言并发移植时语义要显式对齐。

### 5.3 新原语
- **`ScopedValue`（JEP 506, JDK 25 GA）**：不可变、可继承、自动清理的"上下文"，比 `ThreadLocal` + final 发布更安全，是安全发布的现代替代。
- **`MemorySegment`（FMA/Panama, JDK 22+）**：带所有权与边界检查的堆外内存，提供 `VarHandle` 级内存语义，替代 `Unsafe`。
- **`ReentrantLock` + 虚拟线程**：AQS 等待不 pin 平台线程（对比 `synchronized` 的 pin 限制），JMM 语义不变。

### 5.4 工业界开源
| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jcstress** | 2.1k | JMM / 内存可见性的模糊测试权威 |
| **openjdk/jol** | 2.1k | 对象布局 / 伪共享可视化 |
| **openjdk/jdk** | 23.4k | `VarHandle`、`MemorySegment`、`volatile` 实现 |
| **herd+diy (Cambridge)** | — | 弱内存 litmus 测试形式化（跨语言） |
| **crossbeam-rs/crossbeam** | 8.6k | Rust 内存序 / epoch GC，与 Java VarHandle 语义对照 |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "DCL 加双重 `if` 就安全" | **必须 `volatile`** 否则读到半构造对象（JDK 5+ 才因 JSR 133 可被 volatile 修） |
| 2 | "构造器里 `this` 泄漏无所谓" | 别的线程可能看到**未初始化字段**；JSR 133 下 `final` 也救不了 this 泄漏 |
| 3 | "`volatile` 能让 `i++` 线程安全" | `volatile` 只管可见+有序，**不管原子**；复合操作要用 `Atomic*` |
| 4 | "我的代码 x86 跑过就稳了" | ARM/Graviton 是弱内存，x86 的巧合不保证；上 jcstress 多架构 CI |
| 5 | "`long`/`double` 读写总原子" | 规范允许 64 位非 volatile 读写**撕裂**；可移植要加 `volatile` |
| 6 | "新代码还用 `ThreadLocal` 传上下文" | 虚拟线程 + 泄漏风险下，优先 `ScopedValue`（JDK 25 GA） |
