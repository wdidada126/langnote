# 第 5 章 从任务获取数据：Callable 和 Future

> `Callable<V>` 有返回、`Future<V>` 异步句柄：`get()`（阻塞/超时）、`cancel()`、`FutureTask`、批量 `invokeAll`。与之美 08 章、冷血 6 章、手册 4 章互补，本书重「Future 组合瓶颈」引出 Ch10 反应流。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| Callable | 有返回值的任务 |
| Future.get | 阻塞取结果，可设超时 |
| cancel | mayInterruptIfRunning |
| FutureTask | RunnableFuture 实现，可包 Callable |

## 二、核心精讲

### 2.1 🔧 `get()` 无超时是隐患
- `future.get()` 不设超时可能永久挂起（🔧 务必 `get(timeout, unit)`；或 `future.resultNow()`（JDK 19+）非阻塞取已完成结果）。

### 2.2 Future 组合的局限
- `Future` 不能直接 `map`/`flatMap` 链式；多个 Future 的编排要手动 `get` + 嵌套（回调地狱雏形）（🔧 现代用 `CompletableFuture`（见之美 concepts/CompletableFuture）或直接虚拟线程顺序写）。

## 三、版本演进 / 论文 / 前沿

- 论文：Futures/Promises 源自 Baker-Ponder（1977）、Liskov/Promises（1988）；Promises/A+ 规范（2012）。
- 工业界：`CompletableFuture`（JDK 8）、Guava `ListenableFuture`、kotlinx `Deferred`。
- 开源 stars（2026-09）：JDK 23.4k / kotlinx 13.8k / RxJava 48k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "get() 不设超时" | 必设超时防永久挂 |
| 2 | "Future 能链式组合" | 用 CompletableFuture |
| 3 | "cancel(true) 必中断" | 仅设中断标志，任务需响应 |
