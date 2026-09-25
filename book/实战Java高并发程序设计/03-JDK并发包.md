# 第 3 章 JDK并发包（原书）

> J.U.C 全景速览：原子类、锁框架、并发容器、同步工具、线程池、ForkJoin、Future。与《艺术》5-10 章 + 冷血 2-7 章互补，本书重"一张地图 + 选型"。

## 一、本章地图

| 包 | 内容 |
| --- | --- |
| `atomic` | `Atomic*` / `LongAdder`（见《艺术》7 章） |
| `locks` | `ReentrantLock`/`ReadWriteLock`/`StampedLock`/`Condition`（见《艺术》5 章） |
| `concurrent` 容器 | `ConcurrentHashMap`/`CopyOnWrite`/阻塞队列（见《艺术》6 章） |
| 同步工具 | `CountDownLatch`/`CyclicBarrier`/`Semaphore`/`Exchanger`/`Phaser`（见《艺术》8 章） |
| 线程池 | `ThreadPoolExecutor`/`Executors`（见《艺术》9 章） |
| `forkjoin` | `ForkJoinPool`（见冷血 7 章） |
| `Future`/`CompletableFuture` | 异步（见冷血 8 章 / 之美专篇） |

## 二、核心精讲

### 2.1 选型原则
- 计数：`Atomic*` 低争用、`LongAdder` 高争用。
- 互斥：`synchronized` 默认；需定时/可中断/公平/多条件用 `ReentrantLock`；读多写极少用 `StampedLock` 🔧。
- 容器：高并发用 `ConcurrentXxx` 而非 `Collections.synchronizedXxx`。
- 协作：Latch/Barrier/Semaphore 按语义选；批量任务用 `StructuredTaskScope` 🔧。

### 2.2 🔧 现代
- 虚拟线程执行器 + 结构化并发接管多数线程池/编排场景（JDK 21+）。

## 三、版本演进 / 论文 / 前沿

- Doug Lea AQS (SCIENCE 2004)；Michael-Scott (PODC 1996)；开源 JDK 23.4k / JCTools 3.9k / Disruptor 18.5k。

## 四、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "synchronized 慢用 Lock" | JDK 6+ 反之 |
| 2 | "AtomicLong 可伸缩" | 高争用 LongAdder |
| 3 | "synchronizedXxx 够并发" | 用 ConcurrentXxx |
| 4 | "新代码手写线程池" | 虚拟线程 + 结构化并发 |
