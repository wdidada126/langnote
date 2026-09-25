# 第 5 章 并发工具类和 Executor 框架

> `Executor`/`ExecutorService` 框架、`Callable`/`Future`、`invokeAll`/`invokeAny`、拒绝策略。本书 API 手册式，与艺术 10 章、冷血 6 章、之美 08 章、手册 4 章互补。

## 一、核心精讲

### 2.1 🔧 拒绝 Executors 快捷工厂
- `newFixedThreadPool`/`newSingleThreadExecutor` 用无界 `LinkedBlockingQueue`→OOM；`newCachedThreadPool` 用 `SynchronousQueue`+无限线程（🔧 显式 `ThreadPoolExecutor` 构造，设容量 + `CallerRunsPolicy`）。

### 2.2 `invokeAll` / `invokeAny`
- `invokeAll` 等全部完成（超时则返回，未完的 cancel）；`invokeAny` 取首个成功（🔧 多源取最快；见冷血 6 章、手册 4 章）。

### 2.3 Future.get 超时
- 不设超时可能永久挂（🔧 `get(timeout, unit)`；JDK 19+ `resultNow()` 非阻塞取已完成）。

## 二、版本演进 / 论文 / 前沿

- 论文：Lea Executor 框架（JDK5）；Futures/Promises（Baker-Ponder 1977）。
- 工业界：Netty `EventLoopGroup`、Tomcat `NioEndpoint`；Micrometer 线程池监控。
- 开源 stars（2026-09）：JDK 23.4k / netty 34k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "Executors 快捷工厂" | 显式构造 + 容量 |
| 2 | "get() 不设超时" | 必设超时 |
| 3 | "Cached 无限线程" | 限 max + 有界队列 |
