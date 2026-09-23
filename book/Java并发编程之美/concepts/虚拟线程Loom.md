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
