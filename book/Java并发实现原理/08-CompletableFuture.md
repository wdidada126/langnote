# 第 8 章 CompletableFuture（原书 pp.226-265）

> 手写 `CompletableFuture` 的核心：状态机、`thenApply`/`thenAccept`/`thenRun`/`thenCombine`/`thenCompose` 的依赖链、`complete`/`completeExceptionally` 唤醒依赖。与《之美》`concepts/CompletableFuture与异步编排.md` 互补——本书是"从零写一个异步编排框架"，另两本是"读 JDK 源码 + 现代用法"。

## 一、本章地图

| 主题 | 手写要点 |
| --- | --- |
| 状态机 | `result` + `stack`（依赖的等待者 Treiber 栈） |
| `complete` | 设结果 → CAS 状态 → `postComplete` 唤醒依赖链 |
| `thenApply` | 注册依赖：源完成后把函数应用到结果，再 `complete` 下游 |
| `thenCompose` | 扁平化（避免 `CompletableFuture<CompletableFuture<T>>`） |
| `thenCombine` | 两源都完成才触发 |
| 线程模型 | 默认 `ForkJoinPool.commonPool()` 或调用者线程 |

## 二、核心精讲

### 2.1 手写 `CompletableFuture` 状态机
- 字段：`Object result`（null=未完成；用特殊标记区分"未完成/已完成/异常"）；`Completion stack`（依赖的等待者，Treiber 栈）。
- `complete(v)`：`CAS` 把 `result` 从 null 设为 v → 调 `postComplete()` 弹出 stack 逐个唤醒/执行依赖。

### 2.2 手写 `thenApply`（依赖链）
- 注册一个 `UniApply` 节点到源的 stack：源 `complete` 后，`postComplete` 取出该节点 → 在当前线程/池中执行 `function.apply(result)` → 把结果 `complete` 到下游 `CompletableFuture`。
- 链式：`cf.thenApply(f).thenApply(g)` 形成依赖链，源完成逐级传播（类似 Promise 的 `then`）。

### 2.3 手写 `thenCompose`（扁平化）
- `thenCompose(f)` 的 f 返回 `CompletableFuture<U>`；源完成后用其结果启动新 CF，并把"最终完成"传播到外层 → 避免嵌套 Future。
- 对应 JS `Promise.then`（flatMap 语义）/ Kotlin `flatMap` / Rust `and_then`。

### 2.4 手写 `thenCombine` / `allOf` / `anyOf`
- `thenCombine(other, fn)`：两源各维护一个"对方完成否"标志，都完成后触发 `fn`。
- `allOf`：N 个都完成才 complete；`anyOf`：任一完成即 complete（对应《艺术》10 章 `invokeAll`/`invokeAny` 的异步版）。

### 2.5 线程模型与异常
- 默认异步分支跑在 `ForkJoinPool.commonPool()`（或自定义 `Executor`）；同步分支（`*Async` 不带 Executor）可能由调用者线程直接执行。
- 异常：`completeExceptionally(ex)` 存入 result → 下游 `handle`/`exceptionally` 捕获（类似 `try/catch` 沿链传播）。

## 三、版本演进

- **JDK 8 (2014)**：`CompletableFuture` 引入——从"拉式 `Future.get()`"进化到"推式回调/组合"。
- **JDK 9**：`Executor` 默认 `delayedExecutor`、超时 API、`completeOnTimeout`/`orTimeout`。
- **JDK 12+**：`exceptionallyAsync`/`exceptionallyCompose` 等。
- **JDK 21+**：结构化并发 `StructuredTaskScope` 提供"批量子任务 + 作用域取消"，是 `CompletableFuture` + 手动异常处理的现代替代（见《之美》结构化并发专篇）。

## 四、经典论文 / 原始文献

- **Lea, J.U.C `CompletableFuture` 注释**——依赖链/栈设计。
- **Promises/A+ 规范**——JS Promise 的 `then` 语义（与 `CompletableFuture` 同源思想）。
- **JEP 453/505 Structured Concurrency**——现代替代范式。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jdk** | 23.4k | `CompletableFuture`/`StructuredTaskScope` |
| **ReactiveX/RxJava** | 48k | 响应式替代 `Future.get()` 拉式等待 |
| **project-reactor/reactor** | 5.2k | `Mono`/`Flux` 背压式异步 |
| **Kotlin/kotlinx.coroutines** | 13.8k | `async/await`/`Deferred` 替代 `CompletableFuture` 组合 |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "`get()` 不会卡" | 阻塞；设超时或用 `*Async` 回调 |
| 2 | "忽略异常就消失" | `completeExceptionally` 沿链传；用 `exceptionally`/`handle` |
| 3 | "默认用 commonPool 安全" | 共享池别提交阻塞任务 |
| 4 | "thenApply 返回嵌套 Future 也行" | 用 `thenCompose` 扁平化 |
| 5 | "新代码全用 CompletableFuture" | 批量任务改 `StructuredTaskScope`（作用域取消，不易漏） |
