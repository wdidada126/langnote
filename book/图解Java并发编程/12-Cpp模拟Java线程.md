# 第 12 章 用 C++ 模拟实现 Java 线程（本书独门章）

> 用 C++（POSIX `pthread` / C++11 `std::thread`）模拟 Java 线程：线程创建与生命周期、`std::mutex` 模拟 `synchronized`、`std::condition_variable` 模拟 `wait/notify`、线程局部存储 `thread_local` 模拟 `ThreadLocal`、原子操作模拟 CAS。本书唯一一本做「跨语言造轮子」的并发书。

## 一、核心精讲

### 12.1 🔧 Java 线程 → C++ 映射
| Java | C++ |
| --- | --- |
| `Thread`/`Runnable` | `std::thread`（构造即启动，无 `start()`） |
| `synchronized` | `std::mutex` / `std::lock_guard`（或 `std::recursive_mutex` 模拟可重入） |
| `wait`/`notify` | `std::condition_variable` + `std::unique_lock` |
| `ThreadLocal` | `thread_local` 关键字（编译器支持，无泄漏问题） |
| `AtomicInteger` | `std::atomic<int>`（`compare_exchange_weak`） |
| `join` | `std::thread::join()` |

### 12.2 关键差异
- C++ 无 GC：无对象头 Mark Word，锁是显式 `mutex` 对象；无「锁升级」（🔧 Java 的锁在对象头里，C++ 靠显式 mutex）。
- `std::thread` 构造即运行（Java 需 `start()`）；必须 `join`/`detach`，否则 `terminate`（🔧 Java 线程由 JVM 管理，无 detach 强制）。
- 内存序可选：C++ `std::memory_order`（relaxed/acquire/release/seq_cst），比 Java 默认 seq-cst 更细粒度（🔧 与 Java `VarHandle` 5 档语义对应）。

### 12.3 无锁与内存回收
- C++ 无锁队列需 hazard pointer / epoch 回收（🔧 Java 靠 GC 天然解决，见《之美》concepts/Michael-Scott无锁队列）。

## 二、版本演进 / 论文 / 前沿

- 论文/标准：POSIX Threads（IEEE 1003.1c, 1995）；C++11 `<thread>`/`<atomic>`/`<mutex>`；C++20 `std::jthread`（自动 join，可停止令牌）；Herlihy Wait-Free（PODC'91）；Michael-Scott（PODC'96）。
- 工业界：folly（Meta，30.5k）、oneTBB（6.8k）、crossbeam（Rust，8.6k）、tokio（33.2k）。
- 开源 stars（2026-09）：folly 30.5k / oneTBB 6.8k / crossbeam 8.6k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "C++ 线程有对象头锁" | 显式 mutex |
| 2 | "忘了 join/detach" | 析构时 terminate |
| 3 | "C++ 无锁同 Java 易" | 需 hazard pointer 回收 |
| 4 | "内存序随意" | 弱序平台需显式 acquire/release |
