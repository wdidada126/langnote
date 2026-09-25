# 第 2 章 使用基本元素：Thread 和 Runnable

> 最底层的并发原语：`Thread`/`Runnable`/`Callable`、`ThreadGroup`、异常处理、`UncaughtExceptionHandler`、守护线程、优先级。与手册 1 章、黄文海 1 章互补，本书重「基准测试对比」。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| Runnable / Callable | 无返回 / 有返回 |
| 生命周期 | NEW→RUNNABLE→BLOCKED→WAITING→TIMED_WAITING→TERMINATED |
| 异常处理 | `UncaughtExceptionHandler` |
| 守护/优先级 | `setDaemon` / `setPriority`（平台相关） |

## 二、核心精讲

### 2.1 🔧 直接 new Thread 的代价
- 每线程 1MB 栈（默认，可 `-Xss` 调）+ 内核调度开销；高并发下须用池/虚拟线程（🔧 JDK 21 虚拟线程栈是栈 chunk，按需增长，百万级轻量）。

### 2.2 优先级不可移植
- `setPriority` 映射依赖 OS 调度器；不要把它当正确性依赖（🔧 实时性靠 `ReentrantLock`+公平/自定义调度，而非优先级）。

## 三、版本演进 / 论文 / 前沿

- 论文：JLS 第 17 章定义 Java 内存模型与线程（JSR 133 修订）。
- 前沿：JEP 444 虚拟线程；`Thread` API 新增 `ofVirtual()`/`ofPlatform()`；虚拟线程无 daemon 概念（均为 daemon 语义）。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "直接 new Thread 简单够用" | 高并发用池/虚拟线程 |
| 2 | "优先级保证实时" | OS 依赖，不可靠 |
| 3 | "submit 异常自动抛" | 吞到 Future.get() |
| 4 | "忘了 UncaughtExceptionHandler" | 线程池用 afterExecute 兜底 |
