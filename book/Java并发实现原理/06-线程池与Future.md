# 第 6 章 线程池与Future（原书 pp.163-189）

> 手写 `ThreadPoolExecutor`（含 `ctl` 位运算、`Worker` 循环 `getTask`）、`FutureTask` 状态机、`submit/invokeAll`。与《艺术》9 章 + 《之美》08-线程池ThreadPoolExecutor.md 互补——本书是"从零写企业级线程池"，另两本是"读 JDK 源码"。

## 一、本章地图

| 主题 | 手写要点 |
| --- | --- |
| `ctl` 位运算 | 高 3 位状态 + 低 29 位工作线程数（手写拆包/封包） |
| `execute` 三步走 | ① <core 则 addWorker ② 入队 ③ 失败且 <max 则 addWorker 否则拒绝 |
| `Worker` | 继承 AQS（不可重入锁）+ Runnable，跑首任务后循环 getTask |
| 拒绝策略 | Abort/Discard/DiscardOldest/CallerRuns |
| `FutureTask` | 状态机 NEW→COMPLETING→NORMAL/EXCEPTIONAL；get 阻塞 |

## 二、核心精讲

### 2.1 手写 `ctl`
- `private AtomicInteger ctl`：手写 `RUNNING=-1<<COUNT_BITS` 等常量；`runStateOf`/`workerCountOf`/`ctlOf` 用位运算拆包。
- 状态：RUNNING > SHUTDOWN > STOP > TIDYING > TERMINATED（注意本书用高 3 位编码）。
- 拆包避免两个原子变量竞态（状态与工作数必须原子一起变）。

### 2.2 手写 `execute` 三步走（与《艺术》9 章一致）
1. `wc < corePoolSize` → `addWorker(command, true)`。
2. 否则 `workQueue.offer(command)`；成功后 double-check 状态（防入队后已 shutdown）。
3. 入队失败 → `addWorker(command, false)`（用 maxPoolSize）；失败 → `reject()`（拒绝策略）。

### 2.3 手写 `Worker`
- `Worker` 继承 AQS 实现**不可重入**锁（覆盖 `tryAcquire/tryRelease` 用 CAS 抢 `state` 0→1）。
- `run()`：先跑 `firstTask`，然后循环 `getTask()` 从队列取；取不到（超时/超 max）则退出，线程回收。
- `getTask()` 会吞 `InterruptedException` 后重新检查状态（详见《之美》08 章）。

### 2.4 手写 `FutureTask`
- `state` + `outcome` + `waiters`（Treiber 栈）；`run()` 执行 Callable → CAS state 到 COMPLETING → 设 outcome → NORMAL → `finishCompletion` unpark 所有等待者。
- `get()`：state 未完成则 park 入 waiters 栈；完成被 unpark 后返回 outcome（或抛 `ExecutionException`）。
- 🔧 JDK 7+ 内部从 AQS 改为 `state`+栈（更轻），外部语义不变（见《艺术》10 章 / 《实战》14.6）。

## 三、版本演进

- **JDK 5**：`ThreadPoolExecutor`/`FutureTask` 随 J.U.C 引入（本书手写对象的官方原版）。
- **JDK 7**：`FutureTask` 内部改 `state`+栈。
- **JDK 8**：`CompletableFuture` 引入（见第 8 章）。
- **JDK 21**：`Executors.newVirtualThreadPerTaskExecutor()` + `StructuredTaskScope` → IO 密集不再需手写线程池复用。

## 四、经典论文 / 原始文献

- **Doug Lea, J.U.C Executor 源码注释**——`ctl`/状态机/Worker 设计说明。
- **Goetz, "Java Concurrency in Practice" 第 6/8 章**——线程池配置策略。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `ThreadPoolExecutor`/`Worker`/`FutureTask`/`StructuredTaskScope` |
| **Netflix/concurrency-limits** | 1.4k | 自适应并发限制，补"公式照抄"之不足 |
| **Kotlin/kotlinx.coroutines** | 13.8k | 协程调度器替代线程池（IO 并发） |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "线程池越大越好" | 受 CPU/下游；公式 + 压测 |
| 2 | "快捷池放心用" | Fixed/Single 无界队列 OOM；Cached 无限建线程 |
| 3 | "maxPoolSize 总生效" | 无界队列下永不触发；max 形同虚设 |
| 4 | "忘 shutdown 没关系" | 非 daemon 线程阻止 JVM 退出 |
| 5 | "新代码手写线程池" | IO 密集改虚拟线程执行器 + 结构化并发 |
