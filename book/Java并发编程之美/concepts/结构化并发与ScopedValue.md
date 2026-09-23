# 结构化并发与 ScopedValue

> 定位：本书第 1 章（线程生命周期）、第 10 章（同步器）、第 11.8（线程池关闭）、第 11.10（ThreadLocal 泄漏）四处的**现代解法**。
> 两件事：**结构化并发**解决"并发任务的生命周期没人管"；**ScopedValue** 解决"ThreadLocal 在虚拟线程时代的内存与泄漏问题"。它们都随 Project Loom 而来，是同一套设计哲学的两面。

## 一、是什么（最小示例）

```java
// ① 结构化并发（JDK 21 预览 / JDK 25 第 5 预览，JEP 453/480/499/505）
Response handle() throws Exception {
    try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {
        Subtask<String>  user = scope.fork(() -> queryUser(id));
        Subtask<Orders>  ords = scope.fork(() -> queryOrders(id));
        scope.join();                       // 等所有子任务
        return new Response(user.get(), ords.get());   // 任一失败 -> 抛异常
    }   // ← 作用域结束：所有子任务**必然**已结束，不可能泄漏
}
```
```java
// ② ScopedValue（JDK 25 正式，JEP 506；JDK 21-24 为预览/孵化）
static final ScopedValue<Principal> PRINCIPAL = ScopedValue.newInstance();

void serve(Request req) {
    ScopedValue.where(PRINCIPAL, req.principal()).run(() -> handle());
    // ↑ 只在 run(...) 的作用域内可见；退出自动解绑，无需 remove()
}
void handle() {
    Principal p = PRINCIPAL.get();          // 同一线程（及子作用域）内可读
}
```

与旧写法对照：

| 问题 | 本书（JDK 8）写法 | 结构化/ScopedValue 写法 | 改进点 |
| --- | --- | --- | --- |
| 等 N 个并行任务 | `CountDownLatch` + 线程池 | `StructuredTaskScope` + `fork` | 子任务失败/超时**自动传播**；作用域结束必终止 |
| 一个失败要取消其他 | 手写 `cancel()` 或 `interrupt()` | `Joiner.allSuccessfulOrThrow()` + `shutdownOnFailure` | 自动取消兄弟任务 |
| 超时 | `Future.get(timeout)` | `joinUntil(Instant)` | 超时自动中断全部子任务 |
| 关闭线程池 | `shutdown()` + `awaitTermination()`（11.8） | `try-with-resources` | 语言级保证 |
| 传递上下文 | `ThreadLocal`，需 `remove()`（11.10） | `ScopedValue` | 不可变、有作用域、自动解绑 |

## 二、实现原理（深入一层）

**1）结构化并发的核心不变式**

> **一个并发操作的生命周期，必须嵌套在它的调用者的生命周期之内。**

对应到代码就是 `try (var scope = ...)`。**离开作用域时，作用域内所有子任务要么已完成、要么已被取消**——不存在"父任务返回了，子线程还在跑"的情况。这消灭了三类经典 bug：线程泄漏、结果被丢弃后仍在空转、取消无法传播。

实现要点：
- `StructuredTaskScope` 持有一个**虚拟线程集合**（每个 `fork` 起一个虚拟线程），并维护一个 "owner" 线程引用（非 owner 调用 `fork`/`join` 会抛异常）。
- `Forker`（JDK 25 起为 `Joiner`）策略决定"何时结束、如何聚合、失败如何处理"：`allSuccessfulOrThrow()`（全成功或抛）、`anySuccessfulResultOrThrow()`（任一成功即返回并取消其余）。
- `shutdown()` 会中断所有子任务；`joinUntil(deadline)` 超时自动 shutdown。

**2）ScopedValue 为什么比 ThreadLocal 好**

| 维度 | `ThreadLocal` | `ScopedValue`（JDK 25） |
| --- | --- | --- |
| 可变性 | `set()` 可任意改 | **不可变**，只能在 `where(...)` 时绑定 |
| 生命周期 | 与线程同生共死，需手动 `remove()` | 与**作用域**一致，退出自动解绑 |
| 继承 | `InheritableThreadLocal` 需**拷贝整个 map**，O(n) | 结构化继承，**O(1)**（虚拟线程有结构化的父子关系） |
| 内存 | 每线程一个 `ThreadLocalMap` | 存在作用域的栈帧里，无 hash 表 |
| 泄漏风险 | 高（key 弱引用 + value 强引用，见 11.10） | **无**（作用域结束即失效） |
| 适用线程 | 平台线程 | 平台线程 + **虚拟线程（为它而设计）** |

```java
// 嵌套与重绑定
ScopedValue.where(USER, alice).run(() -> {
    handle();                                  // USER = alice
    ScopedValue.where(USER, bob).run(() -> inner());   // 内层重绑定为 bob
    handle();                                  // 又回到 alice
});
```

**3）与 `StructuredTaskScope` 的协同**

```java
// ScopedValue 会在 fork 出的子任务中自动可见（结构化继承）
ScopedValue.where(TRACE_ID, req.traceId()).run(() -> {
    try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {
        scope.fork(() -> callA());     // callA() 里 TRACE_ID.get() 可用
        scope.fork(() -> callB());
        scope.join();
    }
});
```

这正是 `InheritableThreadLocal` + 线程池做不好、需要 transmittable-thread-local（TTL）来打补丁的事情；结构化并发 + ScopedValue 从语言层面解决了它。

## 三、JDK 版本演进

| 版本 | JEP | 状态 |
| --- | --- | --- |
| JDK 19 | JEP 428 | 结构化并发**孵化**（`StructuredTaskScope`，incubator） |
| JDK 20 | JEP 437 | 孵化第 2 版 |
| **JDK 21 (LTS)** | **JEP 453** | **预览**（`--enable-preview`）；`StructuredTaskScope.ShutdownOnFailure/ShutdownOnSuccess` |
| JDK 22 | JEP 462 | 预览第 2 版 |
| JDK 23 | JEP 480 | 预览第 3 版 |
| JDK 24 | JEP 499 | 预览第 4 版 |
| **JDK 25 (LTS)** | **JEP 505** | 预览第 5 版：API 大幅简化为 `StructuredTaskScope.open(Joiner)`，**`fork` 返回 `Subtask`**；同时 **JEP 506 `ScopedValue` 正式 GA** |
| JDK 26+ | — | 结构化并发预计转正，以 [OpenJDK JEP 索引](https://openjdk.org/jeps/0) 为准 |

> 提示：由于仍处预览，编译需 `--enable-preview --release 25`，运行需 `--enable-preview`。**生产使用要评估 API 稳定性风险**，很多团队选择先用 `ExecutorService` + `CompletableFuture`，等转正再迁移。

## 四、经典论文与理论源头

| 工作 | 出处 | 关联 |
| --- | --- | --- |
| **Dijkstra, *Go To Statement Considered Harmful*** | CACM 1968 | 结构化编程的源头；结构化并发是其**并发版**类比 |
| **Smith (Nathaniel J.), *Notes on Structured Concurrency, or: Go Statement Considered Harmful*** | 博客/技术笔记，2018 | 🔴 **直接启发 JEP 453**；提出 "go statement considered harmful" 与 nursery 概念（Trio 库） |
| **Hewitt, Bishop & Steiger, *A Universal Modular Actor Formalism*** | IJCAI 1973 | Actor 模型：另一种"结构化"并发（监督树） |
| **Armstrong, *Making Reliable Distributed Systems in the Presence of Software Errors*** | 博士论文，2003 | Erlang/OTP **监督树（supervisor tree）**——工业界最早的结构化并发实践 |
| **Liskov & Shrira, *Promises: Linguistic Support for Efficient Asynchronous Procedure Calls*** | SIGPLAN Notices 1988 | Promise/Future 的起源，结构化并发聚合结果的语义基础 |
| **Manson, Pugh & Adve, *The Java Memory Model*** | POPL 2005 | ScopedValue 的可见性语义仍建立在 JMM 之上（绑定在调用前，happens-before 成立） |

**近年研究（2020 后）**：
- **结构化并发的形式化**：2022-2025 年有多篇把结构化并发与**代数效应（algebraic effects）**联系的工作（如 *Structured Asynchrony with Algebraic Effects*，ICFP/OOPSLA 系列），把"作用域 + 取消传播"建模为 effect handler。
- **取消传播的正确性**：研究集中在"取消是否保证资源清理"（类似 C++ RAII、Rust `Drop`），结论是需要语言级别的 `try-with-resources` 配合——Java 的选择正是如此。
- **与 Actor/监督树的对比研究**：2023-2025 有工作指出 Java 的结构化并发在语义上**趋同于 Erlang 的监督树**，但 Java 缺少"重启策略"这一层。

## 五、近年研究与工业界实践（2020-2026）

**工业界落地情况（2026）**：
- **Spring Framework 6.x / Boot 3.x**：`StructuredTaskScope` 尚未进入核心编程模型，但 Spring 已在其 `ContextPropagation` 库中支持 ScopedValue 风格的上下文传播。
- **Micrometer / OpenTelemetry Java**：正在从 `ThreadLocal` 迁移到支持 `ScopedValue` 的上下文存储（OTel Java agent 已有实验支持）。
- **Quarkus / Helidon 4**：Helidon 4 全面转向虚拟线程，其 `Context` 传播机制与 ScopedValue 思路一致。
- **Kotlin `coroutineScope` / `supervisorScope`**：2018 年起就提供了结构化并发，**是 Java 的先行参考实现**——`coroutineScope { }` 结束时所有子协程必然结束，与 `StructuredTaskScope` 语义几乎一致；`SupervisorJob` 对应"任一失败不取消兄弟"。
- **Go `errgroup.WithContext`**：事实上的结构化并发库（非语言级），`g.Wait()` + context 取消。
- **Python Trio / AnyIO**：nursery 模型，Nathaniel Smith 提出者的实现，最纯粹的对照物。

| 项目 | 地址 | 看点 |
| --- | --- | --- |
| **OpenJDK JEP 505 / 506** | https://openjdk.org/jeps/505 · https://openjdk.org/jeps/506 | 权威规范与设计动机 |
| **Trio（Python）** | https://github.com/python-trio/trio | nursery 模型的参考实现 |
| **golang.org/x/sync/errgroup** | https://github.com/golang/sync | Go 的结构化并发实践 |
| **Kotlin Coroutines** | https://github.com/Kotlin/kotlinx.coroutines | `coroutineScope`/`supervisorScope` |
| **transmittable-thread-local** | https://github.com/alibaba/transmittable-thread-local | 线程池时代 ThreadLocal 传递的补丁；ScopedValue 是它的"官方终局" |
| **OpenTelemetry Java** | https://github.com/open-telemetry/opentelemetry-java | 上下文传播从 ThreadLocal 向 ScopedValue 迁移的现实例子 |

## 六、常见误区 + 跨语言对照

**常见误区**：

1. ❌ "`StructuredTaskScope` 是线程池" → 不是。它**不复用线程、没有队列、没有 core/max**；每个 `fork` 起一个虚拟线程。要限流仍需 `Semaphore` 或有界队列。
2. ❌ "结构化并发已经 GA 了，可以直接上生产" → 截至 JDK 25 仍是**预览 API**（JEP 505 第 5 预览），需 `--enable-preview`；`ScopedValue` 才是 JDK 25 正式 GA（JEP 506）。上生产要评估 API 变更风险。
3. ❌ "`ScopedValue` 就是 `ThreadLocal` 的改名" → 语义完全不同：**不可变**是核心（不能 `set`），因此也无法被下游污染；生命周期由作用域而非线程决定。
4. ❌ "`ScopedValue` 可以在任意地方 `set`" → 只能在 `ScopedValue.where(k, v).run(...)` / `.call(...)` 中绑定。需要"可变上下文"的场景（如累加计数器）不适合它。
5. ❌ "用了结构化并发就不用管中断了" → 取消仍是**协作式**的：子任务必须能响应中断/检查取消标志，纯 CPU 死循环不会被中断。
6. ❌ "`scope.fork()` 可以在任意线程调用" → 只能由**创建 scope 的 owner 线程**调用，否则抛 `WrongThreadException`（这正是"结构化"的强制手段）。

**跨语言对照**：

| 语言 | 结构化并发 | 上下文传递 | 成熟度 |
| --- | --- | --- | --- |
| **Java** | `StructuredTaskScope`（JDK 19 孵化 → 25 第 5 预览） | `ScopedValue`（JDK 25 GA） | 虚拟线程生态中，预览中 |
| **Kotlin** | `coroutineScope` / `supervisorScope`（2018 起） | `CoroutineContext`（含 `ThreadLocal` 桥接） | ✅ 成熟，Java 的重要参照 |
| **Go** | 无语言级；`errgroup` + `context.Context` 取消 | `context.Context`（显式传参，无 TLS） | ✅ 事实标准 |
| **Rust (tokio)** | `JoinSet`；tokio task 随 runtime drop 而取消 | 显式传参（`Arc<T>`） | ✅ 成熟 |
| **Python** | **Trio nursery**（最纯粹）/ `asyncio.TaskGroup`（3.11+） | `contextvars` | ✅ 成熟 |
| **Erlang/OTP** | **监督树**（1980s 起） | 进程字典 + 显式传参 | ✅ 最早、最彻底 |
| **C++** | 无；提案 `std::execution`（P2300）讨论中 | 显式传参 | 未落地 |
| **Swift** | **Structured Concurrency**（Swift 5.5, 2021，语言级） | `TaskLocal` | ✅ 成熟，与 Java 设计最接近 |

**一句话结论**：结构化并发把本书第 11.8 节（记得关闭线程池）从"开发者纪律"升级为**语言保证**；`ScopedValue` 把第 11.10 节（ThreadLocal 泄漏）从"记得 remove"升级为**不可能发生**。这两者合起来，是 Loom 项目给"并发代码正确性"带来的最大贡献——它们不提升性能，但消灭了整整一类 bug。

---

> 相关：[虚拟线程Loom.md](虚拟线程Loom.md) · [ThreadLocal与内存泄漏.md](ThreadLocal与内存泄漏.md) · [第 10 章 线程同步器](../10-线程同步器原理剖析.md) · [第 8 章 线程池](../08-线程池ThreadPoolExecutor原理剖析.md)
