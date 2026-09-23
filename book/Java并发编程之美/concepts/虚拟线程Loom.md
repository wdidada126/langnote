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
