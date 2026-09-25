# 卷2·CompletableFuture 异步回调（尼恩）

> 卷2 第 10 章。`CompletableFuture` 工厂（`supplyAsync`/`runAsync`）、编排（`thenApply`/`thenCompose`/`thenCombine`/`allOf`/`anyOf`）、异常（`exceptionally`/`handle`）、线程池（默认 `ForkJoinPool.commonPool`）。详见《之美》concepts/CompletableFuture与异步编排.md（最细）。

## 一、核心精讲

### 1.1 🔧 默认执行器陷阱
- 不传 `Executor` 时用 `ForkJoinPool.commonPool()`（🔧 线程数 = 核数-1；其中提交阻塞任务会饿死全局池，拖垮所有并行流与 `CompletableFuture`；务必传自定义池）。

### 1.2 编排 API
- `thenApply`（变换，同线程）、`thenCompose`（扁平化依赖）、`thenCombine`（两结果合并）、`allOf`/`anyOf`（多任务汇聚）（🔧 `thenCompose`≠`thenApply`：前者返回 `CompletableFuture`，避免嵌套）。

### 1.3 异常与超时
- `exceptionally` 兜底；`handle` 拿结果+异常；超时用 `orTimeout`/`completeOnTimeout`（JDK 9+）（🔧 别忘了处理，否则异常静默吞）。

## 二、版本演进 / 论文 / 前沿

- 论文/规范：Promises/A+；Liskov Promises（1988）。
- 工业界：CompletableFuture（JDK8）、kotlinx `Deferred.await`、Reactor `Mono`、RxJava `Single`。
- 开源 stars（2026-09）：JDK 23.4k / kotlinx 13.8k / reactor 5.2k / rxjava 48k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "不传 Executor" | commonPool 被阻塞饿死 |
| 2 | "thenApply 当 compose" | 依赖用 thenCompose |
| 3 | "异常不处理" | exceptionally/handle 兜底 |
| 4 | "不超时" | orTimeout 防永久挂 |
