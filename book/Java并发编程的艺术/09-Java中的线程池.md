# 第 9 章 Java中的线程池（原书第 2 版 pp.311-345）

> 线程池源码级讲解：`ThreadPoolExecutor` 的 `ctl` 位运算、`execute()` 三步走、`Worker` 非可重入 AQS 锁、4 种快捷池（Fixed/Single/Cached/Scheduled）+ 配置公式。与《之美》08-线程池ThreadPoolExecutor.md、09-ScheduledThreadPoolExecutor.md 互补（本书给更多位运算/状态机细节）。

## 一、本章地图

| 主题 | 关键结论 |
| --- | --- |
| `ctl` 原子整数 | 高 3 位 = 运行状态（RUNNING/SHUTDOWN/STOP/TIDYING/TERMINATED），低 29 位 = 工作线程数 |
| `execute()` 三步 | ① 少于 core 则 addWorker ② 入队 ③ 入队失败且少于 max 则 addWorker，否则拒绝 |
| `Worker` | 继承 AQS（不可重入锁）+ 实现 `Runnable`，跑首个任务后循环 `getTask()` |
| 4 种快捷池 | Fixed/Single/Cached/Scheduled 的适用与坑 |
| 配置公式 | `N_cpu` 与 `U_cpu`、阻塞系数 `W/C` → `N_threads = N_cpu * U_cpu * (1 + W/C)` |

## 二、核心精讲

### 2.1 `ctl` 的位打包（本书精华）
- 一个 `AtomicInteger ctl` 同时装两份信息：**高 3 位 = 运行状态**，**低 29 位 = 工作线程数**（`COUNT_BITS=29`，最大线程数 `2^29-1`）。
- 状态枚举（从高到低）：`RUNNING(111)` / `SHUTDOWN(000)` / `STOP(001)` / `TIDYING(010)` / `TERMINATED(011)`。
- 用位运算 `runStateOf(c)` / `workerCountOf(c)` / `ctlOf(rs, wc)` 拆包，避免两个独立原子变量的竞态。
- 详见《之美》08 章「`ctl` 位运算」段。

### 2.2 `execute()` 三步走（与《之美》一致）
1. 当前线程数 < `corePoolSize` → 直接 `addWorker(command, true)`。
2. 否则尝试入 `workQueue`；入队成功再 double-check 状态（防止入队后池已 shutdown）。
3. 入队失败（队列满）→ 尝试 `addWorker(command, false)`（用 `maximumPoolSize`）；仍失败 → 拒绝策略。

### 2.3 `Worker` 的非可重入锁
- `Worker` 继承 `AbstractQueuedSynchronizer` 实现一个**不可重入**的互斥锁（`lock`/`unlock` 包裹任务执行），目的是让 `interruptIdleWorkers()` 能区分"空闲 worker（在 `getTask` 阻塞）"与"正在跑任务的 worker"。
- `getTask()`：从队列取任务；超时/超 max 时返回 null 让 worker 退出；会吞 `InterruptedException` 后重新检查（详见《之美》08 章）。

### 2.4 4 种快捷线程池（🔧 修正提示）
- `newFixedThreadPool(n)`：core=max=n，无界 `LinkedBlockingQueue` → 任务堆积撑爆内存（**生产慎用**）。
- `newSingleThreadExecutor()`：单线程串行；无界队列同样有堆积风险。
- `newCachedThreadPool()`：core=0, max=`Integer.MAX_VALUE`，`SynchronousQueue` → 任务暴增时**无限建线程**撑爆（**生产慎用**）。
- `newScheduledThreadPool()`：见《之美》09 章（`DelayedWorkQueue` 领导-跟随者）。
- 🔧 本书给出配置公式但实际应**结合压测**，而非照抄（见总览"常见误区"）。

## 三、版本演进

- **JDK 5 (2004)**：`ThreadPoolExecutor` + 4 种快捷池随 J.U.C 引入。
- **JDK 7 (2011)**：`ForkJoinPool` 独立（与 ThreadPoolExecutor 不同 lineage）。
- **JDK 8 (2014)**：`CompletableFuture` 默认用 `ForkJoinPool.commonPool()`。
- **JDK 21+**：虚拟线程让"每请求一线程"重获可行 → 多数 IO 密集场景**不再需要线程池复用**（结构化并发接管编排）；CPU 密集仍用 `ThreadPoolExecutor`。

## 四、经典论文 / 原始文献

- **Doug Lea, "Thread Pools" / J.U.C Executor 源码注释**——`ctl`/状态机设计说明。
- **Goetz, "Java Concurrency in Practice" 第 6/8 章**——线程池配置策略与陷阱。
- **JEP 444 (Virtual Threads)** —— 线程池范式的现代冲击。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `ThreadPoolExecutor`/`Worker`/`ctl`/`ScheduledThreadPoolExecutor` 源码 |
| **Netflix/concurrency-limits** | 1.4k | 自适应并发限制，补"公式照抄"之不足 |
| **Kotlin/kotlinx.coroutines** | 13.8k | 协程调度器替代线程池做 IO 并发 |
| **openjdk/jdk (`StructuredTaskScope`)** | 23.4k | 虚拟线程下作用域级任务编排 |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "线程池越大越好" | 受 CPU/下游资源；公式 + 压测（《实战》11 章） |
| 2 | "快捷池放心用" | Fixed/Single 无界队列撑爆内存；Cached 无限建线程 |
| 3 | "maximumPoolSize 总生效" | 无界队列下永远不入队失败 → max 形同虚设 |
| 4 | "忘了 shutdown 没关系" | 非 daemon 线程会阻止 JVM 退出；用 `try-with-resources`/作用域 |
| 5 | "新代码照旧用线程池" | IO 密集改虚拟线程 + 结构化并发；CPU 密集保留 |
