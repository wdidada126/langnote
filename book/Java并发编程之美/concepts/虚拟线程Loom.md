# 专篇：虚拟线程（Project Loom）

> **贯穿全书的修正因子**。《Java并发编程之美》写于 2018 年（JDK 8 基线），
> 而 JDK 21 的虚拟线程**改变了"线程"的成本模型**——本书第 1、6、8、9、10、11 章的部分结论必须按此修正。
> 本专篇是这些修正的集中说明处，各章笔记直接链接到这里。

## 一、一句话概括

**虚拟线程是 JVM 管��的、极廉价的用户态线程**：阻塞（IO、sleep、park）时不再占住 OS 线程，
而是把栈"卸载"到堆上、释放 carrier thread 去跑别的虚拟线程——
于是 **"一个请求一个线程"** 这个被异步回调统治了十几年的反模式，又变回了正解。

## 二、它到底是什么

| | 平台线程（Platform Thread） | 虚拟线程（Virtual Thread） |
| --- | --- | --- |
| 实现 | 对 OS 线程（pthread）的 1:1 包装 | JVM 管理，**M:N** 映射到 carrier thread（ForkJoinPool） |
| 栈 | 固定大小（默认 1MB，可 `-Xss` 调），预分配在 native 内存 | **在堆上**，按需增长/收缩，初始仅几百字节 |
| 创建成本 | ~1MB 内存 + 系统调用，**毫秒级** | ~几百字节，**微秒级** |
| 可创建数量 | 几千个（受内存与内核限制） | **百万级** |
| 阻塞代价 | 占住整个 OS 线程，吞吐崩塌 | 近乎为零（卸载/挂载） |
| 调度者 | 操作系统内核 | **JVM**（`ForkJoinPool` 作为 carrier） |
| 抢占 | 内核时间片抢占 | **协作式**——只在阻塞点让出（JDK 24 前无时间片抢占） |

> ⚠️ **JDK 21-23 的虚拟线程没有时间片抢占**：一个纯 CPU 密集、永不阻塞的虚拟线程会一直占着 carrier thread。
> 这是"虚拟线程不适合 CPU 密集"的技术原因。

## 三、最小可用代码

```java
// ① 直接创建
Thread vt = Thread.ofVirtual().name("vt-1").start(() -> {
    System.out.println("hello from " + Thread.currentThread());
});

// ② 每任务一线程的执行器（最常用）—— 注意：用完要 close
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    var futures = IntStream.range(0, 100_000)
        .mapToObj(i -> executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));     // 阻塞几乎免费
            return i;
        }))
        .toList();
    // 10 万个并发 sleep，1 秒后全部完成 —— 平台线程池下这是不可能的
}

// ③ 虚拟线程 + 结构化并发（JDK 21+ 预览）
try (var scope = StructuredTaskScope.open()) {
    Subtask<String> a = scope.fork(() -> fetchA());
    Subtask<String> b = scope.fork(() -> fetchB());
    scope.join();
    return new Result(a.get(), b.get());
}
```

## 四、正确的使用准则（官方 + 实践）

| 准则 | 说明 |
| --- | --- |
| ✅ **每个任务一个虚拟线程，不要池化** | 创建成本极低，池化反而引入无谓的排队与泄漏风险 |
| ✅ 适合 **IO 密集** | 阻塞是它的主场 |
| ❌ **不适合 CPU 密集** | 没有抢占，且不会比平台线程更快；CPU 密集仍用固定大小的平台线程池（≈ CPU 核数） |
| ⚠️ **不要用 `synchronized` 包裹长阻塞操作**（JDK 21-23） | 会 **pinning**（钉住 carrier thread），导致 carrier 耗尽。JDK 24（JEP 491）已修复 |
| ⚠️ **谨慎使用 `ThreadLocal`** | 百万级虚拟线程 × ThreadLocal = 巨大内存；用 `ScopedValue` 替代 |
| ⚠️ **不要缓存/池化虚拟线程** | 同上 |
| ⚠️ **`Thread.getAllStackTraces()` 等行为会变慢** | 虚拟线程太多，批量操作代价高 |

## 五、Pinning 问题（JDK 21-23 的重要限制）

```java
// ❌ JDK 21-23：synchronized 里的阻塞会 pin 住 carrier thread
synchronized (lock) {
    socket.read();      // 阻塞 → carrier thread 被钉住，无法调度其他虚拟线程
}
// ✅ 改用 ReentrantLock
lock.lock();
try { socket.read(); }
finally { lock.unlock(); }
```

| JDK | 状态 |
| --- | --- |
| 21-23 | `synchronized` 内阻塞 → **pinning**，carrier 被占用 |
| **JDK 24（JEP 491）** | 🔴 **修复**：虚拟线程可在 `synchronized` 中不钉住（移除了 VTD 的 pinning 限制） |
| JDK 25 | 已稳定可用 |

> 这是"要不要因为虚拟线程而把 `synchronized` 全部改写成 `ReentrantLock`"这一争议的答案：
> **JDK 24+ 不需要了**。

## 六、对本书各章的具体修正

| 章节 | 本书（2018, JDK 8）的结论 | 虚拟线程下的修正 |
| --- | --- | --- |
| 第 1 章 | 线程创建昂贵，要复用 | ✅ 仍然适用于 CPU 密集；❌ IO 密集下**每任务一线程**才是正解 |
| 第 1.11 `ThreadLocal` | 线程池下要 `remove()` | ⚠️ 风险放大：百万虚拟线程；✅ 改用 `ScopedValue`（JDK 25 GA） |
| 第 6 章 锁 | 锁竞争会导致线程挂起、上下文切换昂贵 | ⚠️ 竞争代价仍在（锁本身没变），但**阻塞等待不再消耗 OS 线程** |
| 第 8 章 线程池 | 核心公式：按 CPU/IO 比例配线程池 | 🔴 **IO 密集场景公式失效**——不要池化；✅ CPU 密集公式仍有效（≈核数） |
| 第 8 章 队列容量 | 有界队列形成背压 | ✅ 仍然需要——虚拟线程不解决"无限堆积"，只是让等待变廉价。**仍需有界队列/限流** |
| 第 9 章 定时任务 | 调度线程阻塞在 `awaitNanos` | ⚠️ 调度线程**仍是平台线程**，无法虚拟线程化 |
| 第 10 章 `Semaphore` | 限并发数 | ✅ **依然必要**——它限制的是并发数，与线程成本无关 |
| 第 10 章 `CountDownLatch` | 等一批任务 | ⚠️ 优先用**结构化并发** `StructuredTaskScope`（自动取消、无孤儿线程） |
| 第 11.1 线程饥饿死锁 | 池内互等死锁 | ⚠️ 每任务一虚拟线程下**有所缓解**，但仍属坏设计，应改异步编排 |

## 七、性能数据（需要注意口径）

| 场景 | 平台线程池（200 线程） | 虚拟线程 |
| --- | --- | --- |
| 10,000 并发 HTTP 请求（每个 sleep 100ms） | 受限于 200 并发，约 50 秒 | 全部并发，约 0.1-0.2 秒 |
| CPU 密集计算 | 更快（有抢占） | 不变或略慢 |
| 内存占用（10 万并发任务） | ~200GB（不可行） | ~几百 MB |

> ⚠️ **口径提醒**：网络上流传的"虚拟线程快 N 倍" benchmarks 几乎都是 **IO 密集 + 对比配置不当的线程池**。
> 公平对比应是「虚拟线程 vs 同等并发能力的异步框架（Netty/Reactor）」，此时差距远没有那么夸张——
> 虚拟线程的真正卖点是**代码可读性**（同步写法获得异步吞吐），而非绝对性能。

## 八、经典论文 / 原始文献

| 主题 | 文献 / 规范 | 出处 |
| --- | --- | --- |
| **权威规范** | **JEP 444: Virtual Threads** | https://openjdk.org/jeps/444 （JDK 21 GA） |
| pinning 修复 | **JEP 491: Synchronize Virtual Threads without Pinning** | https://openjdk.org/jeps/491 （JDK 24） |
| 结构化并发 | JEP 428 / 437 / 453 / 480 / 505 | 见 [结构化并发与ScopedValue.md](结构化并发与ScopedValue.md) |
| 协程/用户态线程的理论 | Conway, *Design of a Separable Transition-Diagram Compiler* | **CACM 6(7), 1963** —— **协程概念的原始出处**（比线程还早） |
|  continuation 的形式化 | Felleisen 等, *The Theory of First-Class Continuations* | 相关基础见 Felleisen & Hieb, *The Revised Report on the Algebraic Theories of Control*, 1992 |
| M:N 调度的经典分析 | Anderson 等, *Scheduler Activations: Effective Kernel Support for the User-Level Management of Parallelism* | **SOSP 1991 / TOCS 10(1), 1992** —— **虚拟线程调度器设计的理论祖宗**，讨论了内核线程与用户线程的两级调度 |
| 事件驱动 vs 线程之争 | **von Behren, Condit, Brewer, *Why Events Are A Bad Idea (for high-concurrency servers)*** | **HotOS 2003** —— 论证「线程才是对的模型，事件驱动是历史妥协」，**20 年后被 Loom 印证** |
| 反面经典 | Ousterhout, *Why Threads Are A Bad Idea (for most purposes)* | USENIX 1998（线程悲观派的经典，可作对照阅读） |

> **HotOS 2003 那篇（Brewer 组）特别值得读**：它在异步/事件驱动大行其道的年代就论证了
> 「线程模型更适合高并发服务器，只是当时的线程实现太重」。Loom 正是这个论断的实现。

## 九、工业界资料（非同行评审）

- **OpenJDK Loom 官方主页与 JEP 列表**：最权威，含设计动机与已知限制。https://openjdk.org/projects/loom/
- **JEP 索引**：https://openjdk.org/jeps/0
- **Spring Boot 3.2+ 的虚拟线程支持**：`spring.threads.virtual.enabled=true`，Tomcat/Jetty 的请求处理线程切换为虚拟线程。
  https://github.com/spring-projects/spring-boot
- **Quarkus 的虚拟线程集成**：较早大规模落地虚拟线程的企业级框架，有实测报告。
  https://github.com/quarkusio/quarkus
- **Helidon Níma**：Oracle 的虚拟线程原生 Web 框架，完全放弃异步 API。
  https://github.com/helidon-io/helidon
- **Go 的 goroutine**：工业界最成功的 M:N 实现，GMP 调度器是虚拟线程的重要参照（1990 年代 SOSP'91 的 scheduler activations 思路的现代落地）。

## 十、常见误区

1. **❌「虚拟线程让 CPU 密集任务更快」** —— 不会。它没有时间片抢占，CPU 密集请用固定大小平台线程池。
2. **❌「虚拟线程要池化」** —— 不要。创建成本微秒级，池化只会带来排队与泄漏。
3. **❌「有了虚拟线程就不需要限流/背压」** —— 完全错误。无限创建虚拟线程只会把「线程池队列 OOM」变成「堆 OOM」。
   有界队列、`Semaphore`、`RateLimiter` 依然必需。
4. **❌「异步框架（Reactor/RxJava）可以全部废弃了」** —— 不建议一刀切。异步框架在**流式处理、背压传播、复杂编排**上仍有优势；
   虚拟线程的优势在**请求-响应式**的简单 IO 密集场景。
5. **⚠️ `ThreadLocal` 在虚拟线程下代价放大** —— 改用 `ScopedValue`。
6. **⚠️ `synchronized` + 阻塞的 pinning** —— JDK 21-23 有问题，JDK 24+（JEP 491）已修复。
7. **⚠️ 调试与可观测性需要更新工具链** —— 百万虚拟线程下 `jstack` 不可用，要用 `Thread.dump_to_file -format=json` 与 JFR。


---

<!-- ===== 以下为 gitlab 端合并保留版本（2026-09-25 merge） ===== -->

# 虚拟线程（Project Loom）

> 定位：**本书完全没有、但最必须补的一章**。本书基于 JDK 8，"线程 = 内核线程、创建昂贵、必须池化"是全书第 1、8、9、11 章的隐含前提；JDK 21（JEP 444）之后这个前提**不再成立**。
> 一句话：虚拟线程是 **JVM 管理的用户态线程（M:N 调度）**，阻塞时不占用操作系统线程，因此"一个请求一个线程"从奢侈变成可行。

## 一、是什么（最小示例）

```java
// JDK 21+
Thread vt = Thread.ofVirtual().name("worker-", 0).start(() -> {
    System.out.println("hello from " + Thread.currentThread());
});

// 百万级并发：这在 JDK 8 时代是不可能的
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 1_000_000).forEach(i ->
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));     // 阻塞，但**不占** OS 线程
            return i;
        }));
}   // try-with-resources 结束 = 所有任务结束
```

与平台线程（platform thread）的对照：

| 维度 | 平台线程（JDK 8 的 `Thread`） | 虚拟线程（JDK 21+） |
| --- | --- | --- |
| 实现 | 1:1 包装 OS 线程（`pthread`） | M:N，由 JVM 调度到 carrier 线程（ForkJoinPool） |
| 默认栈 | 1 MB（`-Xss`，预留虚拟内存） | **按需增长的栈 chunk**，初始约几百字节，堆上分配 |
| 创建成本 | ~1 ms 级 + 内核资源 | ~微秒级，可创建百万级 |
| 阻塞 `Thread.sleep` / IO | **占住 OS 线程**（啥也不干还占着） | **挂起并让出 carrier**，carrier 去跑别的虚拟线程 |
| 调度 | OS 抢占式 | JVM 协作式（在阻塞点挂起）+ carrier 由 OS 抢占 |
| 是否需要池化 | **需要**（本书第 8 章的全部动机） | **不需要**，用完即弃 |
| ThreadLocal | 可用 | 可用但**代价被放大**（百万线程 × map） |
| 守护/优先级 | 有 | **不支持** `setPriority`、不支持 `setDaemon`（恒为 daemon） |

## 二、实现原理（深入一层）

**1）调度模型**

```
虚拟线程 VT-1 ┐
虚拟线程 VT-2 ┼── mount/unmount ──> carrier 线程（ForkJoinPool，默认并行度 = CPU 核数）
虚拟线程 VT-3 ┘                         ↑
                                        └── 由 OS 调度的平台线程
```

- 虚拟线程**运行在 carrier 线程之上**（mount）。当它执行阻塞操作（`LockSupport.park`、`Thread.sleep`、JDK 的 NIO/Socket 已改造的方法）时，JVM 把它的栈从 carrier 上**卸载**（unmount）到堆里，carrier 立刻可以 mount 另一个虚拟线程。
- JDK 21 对 **`java.net.Socket`/`ServerSocket`/`SocketChannel`、`Thread.sleep`、`Future.get`、以及大部分 `java.util.concurrent` 阻塞点**做了改造，使其可挂起。
- 调度器默认是 `ForkJoinPool` 的一个特殊实例（`ForkJoinPool.createThreadPoolExecutor` 风格），并行度 = `Runtime.availableProcessors()`，可用 `jdk.virtualThreadScheduler.parallelism` 调整。

**2）钉住（pinning）与 JEP 491**

- 在 JDK 21~23，如果虚拟线程在 **`synchronized` 块内部**发生阻塞，它**无法卸载**（因为 `synchronized` 是绑定在 carrier 线程的 monitor 上），这就是 **pinning**。极端情况：carrier 数 = N，N 个虚拟线程都在 synchronized 里阻塞 → 全部 carrier 卡死 → **整个应用停滞**。
- **JDK 24（JEP 491）** 通过把 `synchronized` 的 monitor 实现从 carrier 绑定改为独立锁，**彻底解除 pinning**。
- 诊断：`-Djdk.tracePinnedThreads=short`（JDK 21-23）会打印发生 pinning 的栈。

**3）哪些代码要改**

| 场景 | JDK 8 写法 | JDK 21+ 建议 |
| --- | --- | --- |
| Web 服务 IO | 线程池 + 异步回调 / Reactor | **虚拟线程 + 同步阻塞写法**（Tomcat 10.1+/Spring Boot 3.2+ 已支持） |
| CPU 密集 | 固定线程池 = 核数 | **仍然是固定线程池 / ForkJoinPool**（虚拟线程不增加并行度） |
| 限流 | `Semaphore` / 有界队列 | 仍需要——虚拟线程不解决"下游扛不住" |
| 线程池大小公式 | 本书第 8 章的公式 | **不再需要池化**；但要限制"并发度" |
| 数据库连接池 | 池大小 ≈ 线程数 | **池成为新瓶颈**：10000 虚拟线程抢 50 个连接，仍会排队 |

## 三、JDK 版本演进

| 版本 | JEP | 变化 |
| --- | --- | --- |
| JDK 19 | JEP 425 | 虚拟线程**预览**（`--enable-preview`） |
| JDK 20 | JEP 436 | 第 2 轮预览（API 微调） |
| **JDK 21 (LTS)** | **JEP 444** | 🔴 **虚拟线程 GA**；`Thread.ofVirtual()`、`Executors.newVirtualThreadPerTaskExecutor()`、`Thread.isVirtual()` |
| JDK 22 | JEP 462（结构化并发 2 预览）、JEP 464（ScopedValue 预览） | 生态配套继续预览 |
| **JDK 24** | **JEP 491** | 🔴 **解除 synchronized pinning**；`jdk.tracePinnedThreads` 不再需要；同时 **JEP 490** 移除部分旧的线程 API 限制 |
| **JDK 25 (LTS)** | **JEP 506** | 🔴 **ScopedValue GA**（虚拟线程时代的 ThreadLocal 替代，见 [结构化并发与ScopedValue.md](结构化并发与ScopedValue.md)） |
| JDK 25 | JEP 505 | 结构化并发第 5 轮预览（`StructuredTaskScope.open()` 静态工厂 + `Joiner`） |

> **注意**：虚拟线程**没有改变 JMM**（JEP 444 明确说明）。happens-before、volatile、锁的可见性语义与平台线程完全一致——这一点非常关键，意味着本书第 2 章的知识**全部仍然有效**。

## 四、经典论文与理论源头

虚拟线程并非新发明，它是**协程/绿色线程**这一脉思路在 JVM 上的落地：

| 工作 | 出处 | 关联 |
| --- | --- | --- |
| **Conway, *Design of a Separable Transition-Diagram Compiler*** | CACM 1963 | **协程（coroutine）概念的提出** |
| **Hewitt, Bishop & Steiger, *A Universal Modular Actor Formalism for Artificial Intelligence*** | IJCAI 1973 | Actor 模型——海量轻量并发的另一条路线（Erlang 的源头） |
| **Tarjan & van Wyk, *An O(nm log n) Algorithm for Tries***（coroutine 工程实践） | — | 常被引用为协程在 C 中的实践；更权威的综述见 Moura 等 *Revisiting Coroutines*（TOPLAS 2009） |
| **Moura, Rodriguez & Ierusalimschy, *Revisiting Coroutines*** | ACM TOPLAS 31(2), 2009 | 协程分类学（对称/非对称、栈式/无栈），虚拟线程属于**栈式对称协程** |
| **Blumofe & Leiserson, *Scheduling Multithreaded Computations by Work Stealing*** | JACM 1999 | carrier 用 ForkJoinPool 的理论基础 |
| **von Behren, Condit & Brewer, *Why Events Are a Bad Idea (for High-Concurrency Servers)*** | HotOS 2003 | **"线程 vs 事件驱动"之争的经典论文**——论证了线程模型在可维护性上优于回调；Loom 的结论与之一致 |
| **Adya 等, *Cooperative Task Management Without Manual Stack Management*** | ATC 2002 | 协作式任务管理的经典，Loom 的设计参照之一 |
| **Ousterhout, *Why Threads Are a Bad Idea (for Most Purposes)*（1996）与 Behren 等的反驳（2003）** | — | 理解"为什么 Java 一开始选择 1:1 内核线程" |

## 五、近年研究与工业界实践（2020-2026）

**研究侧（2023 年后虚拟线程成为研究热点）**：
- **Loom 的性能评估**：多篇实测研究（ICPE 2023、Middleware/ATC 2024、JAOO/JVMLS 报告）结论一致——IO 密集场景吞吐提升 2~10 倍、内存下降一个数量级；**CPU 密集无提升**；carrier 并行度应等于核数；pinning 是 JDK 21-23 的主要陷阱。
- **虚拟线程调度器的改进**：2024-2025 有工作讨论"虚拟线程 + 阻塞 IO 时 carrier 饥饿"的边界情况，以及把 carrier 调度与 CPU 亲和性结合。
- **与协程语言的正面对比研究**：2023-2025 有多篇把 Java 虚拟线程与 Go goroutine、Kotlin 协程、Rust tokio 做定量对比的论文与报告，结论大致是：吞吐同量级，Java 的优势是**无需函数染色（function coloring）**、可直接复用阻塞式生态，劣势是生态改造（JDBC 尚未完全支持挂起）。
- **内存模型与正确性**：虚拟线程不改变 JMM，但"百万线程 × ThreadLocal"的内存放大是新的研究问题，也直接催生了 `ScopedValue`（JEP 506）。

**工业界**：

| 项目 | 地址 | 看点 |
| --- | --- | --- |
| **OpenJDK Loom 仓库归档** | https://github.com/openjdk/loom | 设计文档（`VirtualThreads.md`）极佳 |
| **Spring Boot 3.2+** | https://github.com/spring-projects/spring-boot | `spring.threads.virtual.enabled=true`，Tomcat/Jetty/Undertow 一键切虚拟线程 |
| **Tomcat 10.1+ `VirtualThreadExecutor`** | https://github.com/apache/tomcat | 与本书 11.2 节的 `NioEndpoint` 直接相关 |
| **Netty 的 FastThreadLocal / 未来适配** | https://github.com/netty/netty | 事件循环模型与虚拟线程的分工 |
| **Quarkus / Helidon / Micronaut** | Red Hat / Oracle / Micronaut | 虚拟线程原生支持的先行者 |
| **JMH / async-profiler** | https://github.com/openjdk/jmh | 评估虚拟线程必须用 JMH；async-profiler 可看 `VirtualThread*` 事件 |
| **Dragonwell / 毕昇 JDK** | Alibaba / Huawei | 国内发行版的虚拟线程实测报告（-XX:+UseWisp 等历史方案已让位于标准虚拟线程） |

## 六、常见误区 + 跨语言对照

**常见误区**：

1. ❌ "虚拟线程更快" → **不增加并行度**。CPU 密集任务用虚拟线程只会多一层调度开销，应继续用固定线程池/`parallelStream`。它解决的是**并发度**（能同时挂起多少等待），不是**并行度**（同一时刻能算多少）。
2. ❌ "有了虚拟线程就不要线程池了" → 对 **IO 密集**成立；**CPU 密集、需要限流、需要复用昂贵资源（连接、缓冲区）**时仍然要池。而且**共享资源池（DB/HTTP 连接池）本身成为新瓶颈**——把 Web 线程换成虚拟线程后，常见结果是连接池先被打满。
3. ❌ "虚拟线程廉价，所以 ThreadLocal 随便用" → 恰恰相反：百万虚拟线程 × 各自的 ThreadLocalMap 会显著放大内存。改用 `ScopedValue`（JDK 25 GA）。
4. ❌ "synchronized 里的阻塞没问题" → JDK 21-23 会 **pinning**，可能导致 carrier 饥饿；JDK 24（JEP 491）后才解决。迁移时优先把 `synchronized` 换成 `ReentrantLock`（JUC 锁本来就不 pin）。
5. ❌ "虚拟线程改变了内存模型/可见性规则" → 没有。JMM 语义完全不变（本书第 2 章依然适用）。
6. ❌ "可以给虚拟线程设优先级 / 设为非守护线程" → 不支持；虚拟线程恒为 daemon，优先级固定 `NORM_PRIORITY`。
7. ❌ "`Executors.newVirtualThreadPerTaskExecutor()` 是"池"" → 它不是池，**没有队列、没有 core/max**，每个任务一个新虚拟线程。因此**不能**用它做限流。

**跨语言对照**：

| 语言 | 轻量并发机制 | 引入时间 | 是否函数染色 | 与虚拟线程的差异 |
| --- | --- | --- | --- | --- |
| **Java** | 虚拟线程（JEP 444） | **2023（JDK 21）** | ❌ 无（阻塞写法照旧） | 最晚到，但**迁移成本最低**——老代码几乎不用改签名 |
| **Go** | goroutine + channel | 2009 | ❌ 无 | 最接近的设计；但 Go 没有 ThreadLocal，用 `context.Context` 显式传递 |
| **Kotlin** | 协程（`suspend`） | 2017 | ✅ 有（`suspend` 关键字） | `suspend fun` 不能从普通函数直接调用 |
| **Rust** | async/await（tokio/async-std） | 2019 稳定 | ✅ 有 | 零成本抽象，但需 `Send + 'static`、需显式 runtime |
| **C#/.NET** | async/await + `Task` | 2012 | ✅ 有 | 织入状态机；`TaskScheduler` 可换 |
| **Python** | asyncio / `async def` | 3.5（2015） | ✅ 有 | GIL 限制，多进程绕开 |
| **Erlang/BEAM** | process | 1986 | ❌ 无 | 抢占式调度 + 无共享内存，比虚拟线程更彻底 |
| **Node.js** | 回调/Promise → async | 2009 / 2017 | ✅ 有 | 单线程事件循环，CPU 密集需 worker_threads |

**一句话结论**：Loom 的价值不在于"更快"，而在于**把"高并发 IO"从"必须异步化"的约束里解放出来**——你可以继续写同步、可读、可调试的阻塞式代码，同时获得与 Go/Rust async 同量级的并发能力。这是 Java 生态 20 年来最大的一次并发编程范式修正，也是重读本书第 1、8、9、11 章时必须随身携带的修正项。

**迁移检查清单**：

1. 确认 JDK ≥ 21（建议 JDK 25 LTS，同时拿到 ScopedValue 与非 pinning）。
2. 扫描代码里的 `synchronized` + 阻塞调用（JDK 24 前会 pinning）。
3. 检查 `ThreadLocal` 用法，尤其是链路追踪类（考虑 `ScopedValue` 或 transmittable-thread-local）。
4. 检查连接池、信号量等**真实资源上限**——它会成为新瓶颈。
5. CPU 密集路径**保持原样**（固定线程池/`parallelStream`）。
6. 用 JMH + async-profiler 做前后对比，别信直觉。
