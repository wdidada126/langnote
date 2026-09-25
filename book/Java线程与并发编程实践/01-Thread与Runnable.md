# 第 1 章 Thread 和 Runnable

> 创建线程（`Thread` 子类 / `Runnable` / `Callable`）、生命周期、优先级、`sleep`/`join`、`interrupt`、`daemon`。本书作为 API 手册逐方法讲，与黄文海 1 章、手册 1 章互补。

## 一、核心精讲

### 2.1 🔧 用 Runnable 而非 Thread 子类
- 继承 `Thread` 耦合类层级且难共享；实现 `Runnable` 更灵活（🔧 配合线程池/`ThreadFactory`；虚拟线程 `Thread.ofVirtual().start(Runnable)`）。

### 2.2 `interrupt` 是协作
- `interrupt()` 仅设标志；`sleep`/`wait`/`join` 抛 `InterruptedException` 并**清除**标志（🔧 捕获后要么重设 `interrupt()`，要么上抛，别吞；见 Goetz concepts/中断与取消策略）。

### 2.3 优先级/守护
- 优先级 OS 依赖不可靠；守护线程随 JVM 退出（🔧 别用守护做必须完成的清理）。

## 二、版本演进 / 论文 / 前沿

- JLS 第 17 章；JEP 444 虚拟线程（`Thread.ofVirtual()`）。
- 工具：JOL（2.1k）、async-profiler（11k）。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "继承 Thread 方便" | 用 Runnable + 池/虚拟线程 |
| 2 | "吞 InterruptedException" | 重设/上抛 |
| 3 | "优先级保证调度" | OS 依赖 |
