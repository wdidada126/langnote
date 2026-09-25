# 第 8 章 Java中的并发工具类（原书第 2 版 pp.281-310）

> 四个"同步协调"工具类：CountDownLatch、CyclicBarrier、Semaphore、Exchanger。与《实战》5 章（基础构建模块）+ 《之美》10-线程同步器.md 互补（本书给出更多源码/状态机细节；注意《之美》对 CountDownLatch 与 CyclicBarrier 实现差异的澄清）。

## 一、本章地图

| 工具 | 语义 | 复用 | 底层 |
| --- | --- | --- | --- |
| `CountDownLatch` | 等待 N 个事件完成（门闩） | **一次性** | AQS 共享模式（`state`=倒数） |
| `CyclicBarrier` | 等 N 个线程到齐再同时放行 | **可循环** | `ReentrantLock` + `Condition` |
| `Semaphore` | 控制并发访问的许可数 | 可循环 | AQS 共享模式（`state`=剩余许可） |
| `Exchanger` | 两线程在汇合点交换数据 | 成对 | 锁 + 槽（slot） |

## 二、核心精讲

### 2.1 `CountDownLatch`（一次性门闩）
- 构造 `N`：`countDown()` 把 `state` 减 1；`await()` 阻塞直到 `state==0`（AQS 共享获取：`tryAcquireShared` 看 `state==0`）。
- 典型：主线程等所有 worker 初始化完成；或测试里等 N 个线程就绪再发令。
- **不可重置**：用完即废；要重复用 → `CyclicBarrier`。

### 2.2 `CyclicBarrier`（可循环栅栏）
- `N` 个线程调用 `await()`，第 N 个到达时**全部放行**，并可执行一个 `barrierAction`（汇总/快照）。
- 底层：`ReentrantLock` + `Condition` + 代（generation）计数；一轮结束自动进入下一代 → 可循环。
- `reset()` 可中途打破（会让等待线程抛 `BrokenBarrierException`）。
- 与 CountDownLatch 核心区别（本书易混点）：《之美》10 章**重点澄清**——`CyclicBarrier` 用**锁+条件变量**实现（非 AQS），且强调"所有线程互相等对方到齐"；`CountDownLatch` 是"一个或多个等待者等 N 个事件"，事件与线程解耦。

### 2.3 `Semaphore`（信号量）
- `acquire()` 拿许可（许可不够则阻塞），`release()` 归还；`state` = 剩余许可（AQS 共享）。
- 用途：限流（数据库连接池、并发任务数上限）、资源池准入。
- 公平/非公平：`tryAcquire` 支持超时/可中断。
- 🔧 注意：信号量**限制并发数**，不保证"线程安全"——被准入的线程访问共享资源仍要自己加锁。

### 2.4 `Exchanger`（成对交换）
- 两线程在 `exchange(V)` 汇合，互相交换数据（经典：生产者/消费者各持 buffer 交换）。
- 底层：用一个 `slot`（单槽）配合锁；多槽优化用于高并发。
- 仅限**成对**（两个线程）；多于两个会随机配对，非预期。

## 三、版本演进

- **JDK 5 (2004)**：四者随 J.U.C 引入。
- **JDK 8+**：`CyclicBarrier` 的实现细节稳定；`Phaser`（JDK 7 引入）作为更灵活的分代屏障补充（见《之美》10 章）。
- **JDK 21+**：结构化并发 `StructuredTaskScope` 提供"等所有子任务完成"的**作用域级**替代（比 Latch/Barrier 更不易漏 `countDown`）。

## 四、经典论文 / 原始文献

- **Doug Lea, "The java.util.concurrent Synchronizer Framework" (SCIENCE 2004)**——CountDownLatch/Semaphore 的 AQS 实现。
- **Herlihy & Shavit, "The Art of Multiprocessor Programming"**——屏障/信号量的算法理论。
- **JEP 453/505 Structured Concurrency**——现代"等全部完成"的范式。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `CountDownLatch`/`CyclicBarrier`/`Semaphore`/`Exchanger`/`Phaser` |
| **ReactiveX/RxJava** | 48k | `zip`/`merge` 等算子替代"等 N 个结果"的 Latch 模式 |
| **Kotlin/kotlinx.coroutines** | 13.8k | `awaitAll`/`withTimeout` 替代 Latch/Barrier |
| **openjdk/jdk (`StructuredTaskScope`)** | 23.4k | 作用域级"等全部/取首成" |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CountDownLatch 可重置" | 一次性；要复用改 `CyclicBarrier`/`Phaser` |
| 2 | "Latch 和 Barrier 一样" | Latch 是"等事件"，Barrier 是"线程互等"；底层 AQS/锁不同（《之美》10 章） |
| 3 | "Semaphore 保证线程安全" | 只限并发数；共享资源仍需锁 |
| 4 | "Exchanger 支持多线程" | 仅成对交换 |
| 5 | "忘记 `countDown` 只是慢" | 会**永久阻塞**等待线程；用 `try/finally` 或虚拟线程作用域 |
| 6 | "新代码手写 Latch 编排" | 虚拟线程 + `StructuredTaskScope` 更不易漏 |
