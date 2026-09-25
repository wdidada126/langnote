# 第 1 章 你好，C++ 并发世界

> **一句话**：并发是为了分离关注点与提升吞吐，**并行只是一种执行方式**；单核也能并发，但不能并行。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 1.1 | 并发 vs 并行 | 并发是代码结构，并行是硬件行为 |
| 1.2 | 为什么要用并发 | 关注点分离、吞吐、响应性 |
| 1.3 | 什么时候不用 | 复杂度成本高于收益时坚决不用 |
| 1.4 | C++ 多线程简史 | C++11 之前的多线程代码在标准层面是 UB |
| 1.5 | 第一个程序 | `std::thread` + `join()` |

---

## 核心精讲

### 并发与并行的区别

- **并发**：多个独立执行的逻辑同时存在（代码结构层面）。
- **并行**：多个计算在同一时刻被真正执行（硬件层面）。

```cpp
// 教学示意：Hello Concurrent World（不参与构建）
#include <iostream>
#include <thread>

void hello() { std::cout << "Hello Concurrent World\n"; }

int main() {
    std::thread t(hello);   // 新线程开始执行
    t.join();               // 必须 join，否则 std::terminate
}
```

### 为什么要用并发

1. **分离关注点**：UI 线程与后台任务、网络收发与业务处理互不阻塞，代码更接近问题域本身。
2. **提升吞吐**：多线程可以利用多核；单核上也能把 IO 等待与计算重叠。
3. **降低延迟**：异步化让请求不被长任务拖住（见第 8 章的「隐藏等待」一节）。

### 什么时候不要用并发

| 判据 | 说明 |
| --- | --- |
| 收益不明确 | 没有量化目标就不要并发化 |
| 线程数远大于任务 | 上下文切换开销可能吞掉全部收益 |
| 团队缺乏并发调试能力 | 数据竞争、死锁的代价远超收益 |
| 可维护性受损 | 并发不是免费午餐，它会显著增加代码复杂度 |

> **本书 1.2.3 的核心提醒**：并发的代价是**可读性**与**可测试性**。写之前先问「单线程版本真的不够快吗？」

---

## 版本演进：C++ 并发设施的时间轴

| 标准 | 年份 | 并发相关的新增 |
| --- | --- | --- |
| C++11 | 2011 | **内存模型**、`std::thread`、`std::mutex`、`std::atomic`、`std::future` |
| C++14 | 2014 | `std::shared_timed_mutex`（读写锁）、少量修正 |
| C++17 | 2017 | 并行算法 + 执行策略、`std::scoped_lock`、`std::shared_mutex` |
| C++20 | 2020 | `jthread`、`stop_token`、原子 `wait/notify`、`latch`、`barrier`、`semaphore` |
| C++23 | 2023 | 并发侧以修补为主；`std::expected` 等通用设施也简化了并 发代码 |

**关键认知**：C++11 之前没有内存模型，多线程程序在语言层面属于**未定义行为**（UB）。这也是为什么不能用「库」来实现线程，必须有语言级支持。

---

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Boehm, *Threads Cannot Be Implemented as a Library* | **PLDI 2005** | 论证单靠库无法实现多线程语义，必须有语言级内存模型 |
| Boehm & Adve, *Foundations of the C++ Concurrency Memory Model* | **PLDI 2008** | `happens-before`、`data race` 的定义，直接成为 C++11 标准内容 |
| Boehm & Adve, *You Don't Know Jack About Shared Variables or Memory Models* | **CACM 2012** | 面向工程师的内存模型科普 |

---

## 近年研究与工业界开源实践

- **协同式取消标准化**：C++20 的 `jthread` + `stop_token` 让「可取消的后台线程」终于有了标准写法；GCC 11 / Clang 12 / MSVC 19.28 之后逐步可用。
- **Executors 姗姗来迟**：C++20 协程没有标准调度器，导致本书第 8、9 章的线程池至今仍是工业代码的首选；P2300（`std::execution`）预计在 C++26 补齐这一层。
- **TSan 的普及改变了认知**：规模化启用 ThreadSanitizer 后，人们发现大量 2011 年之前的 C++ 代码存在真实数据竞争。

| 实现 | star | 说明 |
| --- | --- | --- |
| `llvm/llvm-project` | ≈**40.6k★** | libc++ 的 `<thread>` / `<atomic>` 参考实现，以及 ThreadSanitizer 的实现所在地 |
| `microsoft/STL` | ≈**11.2k★** | MSVC 标准库；其 `jthread` / `stop_token` 实现是学习新设施的好材料 |
| `uxlfoundation/oneTBB` | ≈**6.8k★** | 比手写线程池更成熟的调度器，对应本书第 9 章 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「多线程一定更快」 | 受 Amdahl 定律约束，串行部分决定上限（详见第 8 章） |
| 2 | 「`volatile` 可以同步线程」 | **`volatile` 不提供任何同步语义**，它只防止编译器优化掉访存；请用 `std::atomic` 或互斥 |
| 3 | 「单核上不需要并发」 | 单核上的并发仍可用于关注点分离与 IO 重叠 |
| 4 | 🔧 `t.join()` 的异常安全 | 若主线程在 `join()` 前抛异常，程序会调用 `std::terminate`；正确做法是 RAII（`jthread` 或自写 `thread_guard`，见第 2 章） |
| 5 | 🔧 本书 1.3.5 的「平台专属工具」需更新 | 2026 年的对照对象应是 Windows SRW lock、Linux futex、io_uring，以及 OpenMP / SyCL 等并行框架 |
