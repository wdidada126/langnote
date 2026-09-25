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
