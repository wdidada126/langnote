# 第 1 章 Java 线程的实践及原理揭秘

> 线程创建（继承 Thread/实现 Runnable/Callable/线程池/虚拟线程）、生命周期（6 态）、调度、守护线程、优先级、线程栈。`start()` vs `run()` 的本质。与黄文海 1 章、手册 1 章互补，本书重「JVM 线程 ↔ OS 线程映射」。

## 一、核心精讲

### 1.1 🔧 `start()` 才建真线程
- 调 `run()` 只是普通方法调用（当前线程执行）；`start()` 才向 JVM 申请建 OS 线程并异步跑 `run()`（🔧 一个 Thread 只能 start 一次，二次抛 `IllegalThreadStateException`）。

### 1.2 线程 ↔ 内核
- 传统平台线程：**1:1** 映射到 OS 线程，1MB 栈 + 内核调度（🔧 JDK 21 虚拟线程是「多对多」在 carrier 平台线程上调度，栈按需增长，百万级轻量）。

### 1.3 生命周期六态
- NEW → RUNNABLE（含就绪/运行）→ BLOCKED（等锁）→ WAITING（wait/join/park）→ TIMED_WAITING → TERMINATED（🔧 用 `jstack`/`Thread.dumpAllStackTraces` 诊断卡点）。

## 二、版本演进 / 论文 / 前沿

- JLS 第 17 章线程模型；JEP 444 虚拟线程；`Thread` 新 API `ofVirtual()/ofPlatform()`。
- 工具：async-profiler（火焰图，11k）、JOL（对象布局，2.1k）。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "调 run 起线程" | 必须 start |
| 2 | "线程可重复 start" | 一次，二次抛异常 |
| 3 | "优先级保证调度" | OS 依赖 |
| 4 | "2026 还 new Thread" | 虚拟线程/池 |
