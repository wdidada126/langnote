# 第 10 章 Executor框架（原书第 2 版 pp.346-365）

> `Executor` 框架的两级调度模型与成员结构：`Executor` → `ExecutorService` → `ScheduledExecutorService`；`Callable`/`Future`/`FutureTask`；`CompletionService`；`Executor` Completion 链。与《之美》08 章 + `concepts/CompletableFuture与异步编排.md` 互补（本书偏框架成员，之美偏 `CompletableFuture` 异步编排）。

## 一、本章地图

| 主题 | 关键结论 |
| --- | --- |
| 两级调度 | 应用控制"任务提交" → Executor 框架控制"线程分配"（解耦任务与执行） |
| `Executor` 接口 | 唯一方法 `execute(Runnable)`；把"任务"与"怎么跑"解耦 |
| `ExecutorService` | `submit`（返回 `Future`）/`shutdown`/`invokeAll`/`invokeAny` |
| `FutureTask` | `Runnable` + `Future`，状态机 NEW→COMPLETING→NORMAL/EXCEPTIONAL→… |
| `CompletionService` | `Executor` + 阻塞队列，按"完成顺序"取 `Future`（`take`） |
| `Callable` vs `Runnable` | `Callable` 有返回值/抛受检异常；`Future` 取结果（阻塞 `get`） |

## 二、核心精讲

### 2.1 两级调度模型（本书图示核心）
- **上层（应用）**：控制"提交多少任务"。
- **下层（Executor 框架）**：控制"用多少线程、怎么调度"——把"任务与执行机制"解耦，是《实战》6 章"任务执行"的设计落地。
- 好处：换执行策略（线程池/单线程/ForkJoin/虚拟线程）不动业务代码。

### 2.2 `FutureTask` 的状态机
- 状态：`NEW` → `COMPLETING`（瞬态）→ `NORMAL`/`EXCEPTIONAL`；`CANCELLED`/`INTERRUPTING`/`INTERRUPTED`。
- `get()` 阻塞直到终态；`cancel(mayInterruptIfRunning)` 尝试中断底层线程。
- 🔧 JDK 7+ 内部从 AQS 改为 `state` + Treiber 栈（更轻），外部语义不变（见《实战》14.6）。

### 2.3 `CompletionService`
- 包装 `Executor` + 内部阻塞队列；`submit` 的任务完成后 `Future` 入队。
- 用法：提交 N 个任务，用 `take()` 按**完成顺序**处理（谁先好先处理），比 `invokeAll` 全等再处理更适合"早完成的先消费"。
- 典型：批量爬取/批量计算，先完成先落地。

### 2.4 `invokeAll` / `invokeAny`
- `invokeAll(tasks)`：等所有完成，返回 `List<Future>`（可带超时）。
- `invokeAny(tasks)`：任一成功即返回（其余取消）——适合"多源取最快"场景。

## 三、版本演进

- **JDK 5 (2004)**：`Executor`/`ExecutorService`/`Future`/`FutureTask`/`CompletionService` 引入。
- **JDK 7 (2011)**：`ForkJoinPool` 实现 `ExecutorService`；`FutureTask` 内部改 `state`+栈。
- **JDK 8 (2014)**：`CompletableFuture` 登场——从"拉式 `get()`"进化到"推式回调/组合"（见《之美》CompletableFuture 专篇）。
- **JDK 21+**：`Executor` 可基于虚拟线程（`Executors.newVirtualThreadPerTaskExecutor()`）；`StructuredTaskScope` 提供作用域级 `invokeAll`/取首成。

## 四、经典论文 / 原始文献

- **Goetz, "Java Concurrency in Practice" 第 6 章**——任务执行 / Executor 设计哲学。
- **Doug Lea, J.U.C Executor 包注释**——框架设计说明。
- **JEP 453/505 Structured Concurrency**——现代"批量任务 + 取消"范式。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `Executor`/`ExecutorService`/`FutureTask`/`CompletionService`/`StructuredTaskScope` |
| **ReactiveX/RxJava** | 48k | 响应式替代 `Future.get()` 的"拉式等待" |
| **Kotlin/kotlinx.coroutines** | 13.8k | `async/await` 替代 `Future` 组合 |
| **project-reactor/reactor** | 5.2k | `Mono`/`Flux` 背压式异步 |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "`Future.get()` 不会卡" | 会阻塞直到完成；设超时 |
| 2 | "忽略 `Future` 异常就消失了" | `get()` 抛 `ExecutionException`；不 `get` 则吞异常 |
| 3 | "`invokeAll` 按完成顺序" | 返回全结果列表；要按完成序用 `CompletionService.take()` |
| 4 | "Future 能组合" | 原生 `Future` 不能；组合用 `CompletableFuture` |
| 5 | "新代码手写 Executor" | IO 密集用虚拟线程执行器；CPU 用 ThreadPoolExecutor |
