# 讲 19 + 讲 20｜thread 和 future、内存模型与 atomic

> **一句话**：`std::thread` 与 `std::future` 给你「怎么写对」的原语，而**内存模型回答的是「为什么它真的对」**——前者是接口，后者是契约。

---

## 本章地图

| 节 | 来源 | 内容 | 结论 |
| --- | --- | --- | --- |
| 线程的生命周期 | 19 | `join`/`detach`、可移动、传递参数与返回值 | 线程是独占所有权的资源，别忘 `join` |
| `async`/`future` | 19 | `std::async`、`future::get`、`shared_future` | 返回值与异常都经 `future` 回到调用方 |
| `promise`/`packaged_task` | 19 | 手工设置结果、异常也能传递 | 跨线程异常必须用 `future` 承载 |
| 同步原语 | 19 | `mutex`、`condition_variable`、`atomic` | 先用 `seq_cst` 写对，再谈 `acquire/release` |
| 内存模型 | 20 | 修改序列、happens-before、六种内存序 | **深度讨论见 `book/C++并发编程实战2/05-Cpp内存模型与原子操作.md`，本文不重复** |
| 原子类型与无锁 | 20 | `atomic_flag`、CAS、ABA、回收问题 | 无锁要写清「谁负责回收」，否则会内存泄漏 |
| 🔧 现代补充 | 19/20 + 2026 | `jthread`/`stop_token`、`atomic::wait/notify`（P1135）、C++23 并行算法、C++26 hazard pointer | 2026 年的并发代码可以「可取消、不忙等」 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 线程是「可移动但不可拷贝」的资源

```cpp
// 教学示意：线程的生命周期（不参与构建）
std::thread t(worker);          // 构造即开始执行
t.join();                       // 必须：否则 std::thread 析构时 terminate
// t.detach();                  // 另一种选择：脱离后由运行时回收，但要小心对象生命周期

std::thread t2 = std::move(t);  // 移动：所有权转移，t 变成「非可 join」
```

三条硬规则：

1. **析构时既不 `join` 也不 `detach` 的线程 → `std::terminate`**；
2. **不要 `detach` 一个捕获了局部变量的线程**；
3. 向线程传参时，`std::ref` 传给引用捕获，大对象用 `std::move` 避免拷贝。

### 2. 用 `future` 拿回返回值与异常

```cpp
// 教学示意：async 与 future（不参与构建）
std::future<int> fut = std::async(std::launch::async, []() -> int {
    throw std::runtime_error("worker failed");      // 异常被存进 future
    return 42;
});
try {
    int v = fut.get();                              // 异常在这里重现
} catch (const std::exception& e) {
    log(e.what());                                  // 跨线程异常不会直达主线程
}
```

| 工具 | 适用场景 | 特点 |
| --- | --- | --- |
| `std::async` | 一次性的异步任务 | 默认策略由实现决定；对「fire and forget」不友好 |
| `std::promise` | 手工在某个时刻填结果 | 可控制 `set_value`/`set_exception` 的时机 |
| `std::packaged_task` | 把 callable 包成任务 | 与线程池搭配最常见 |
| `std::shared_future` | 多处等待同一个结果 | `get()` 是 const，可多次调用 |

### 3. 条件变量的标准用法

```cpp
// 教学示意：mutex + condition_variable（不参与构建）
std::mutex m;
std::condition_variable cv;
bool ready = false;

void waiter() {
    std::unique_lock<std::mutex> lock(m);
    cv.wait(lock, [] { return ready; });          // 谓词循环：抵挡虚假唤醒
    use_data();                                    // 只有拿到锁才操作共享数据
}
void setter() {
    { std::lock_guard<std::mutex> lock(m); ready = true; }
    cv.notify_one();                               // 先解锁再通知
}
```

**为什么必须用谓词形式？** 因为虚假唤醒真实存在，且通知与解锁之间可能插入其他线程的结果。

### 4. 内存模型：本讲只给框架，细节在并发书

六种内存序的速查（完整讨论请读 `book/C++并发编程实战2/05-Cpp内存模型与原子操作.md`）：

| 内存序 | 语义 | 典型用途 |
| --- | --- | --- |
| `seq_cst`（默认） | 全局唯一顺序，最严格 | 先用它写对 |
| `acquire` | 之后的操作不能被重排到它之前 | 读取已发布的数据 |
| `release` | 之前的操作不能被重排到它之后 | 发布数据 |
| `acq_rel` | 两者兼备 | CAS 成功路径 |
| `relaxed` | 只保证原子性，不保证顺序 | 纯计数 |
| `consume` | 依赖顺序 | **实际实现都按 `acquire` 处理，不要用** |

```cpp
// 教学示意：release/acquire 的经典搭配（不参与构建）
std::atomic<bool> ready{false};
int payload = 0;

void writer() { payload = 42; ready.store(true, std::memory_order_release); }
void reader() { while (!ready.load(std::memory_order_acquire)) {} assert(payload == 42); }
```

> 本文不重复推导修改序列、释放序列与 happens-before 的形式化定义——那是并发书第 5 章的内容，也是目前中文材料里最系统的一版。

### 5. 无锁不等于免费：回收才是难点

```cpp
// 教学示意：自旋锁与 CAS 的骨架（不参与构建）
class Spinlock {
    std::atomic_flag flag_ = ATOMIC_FLAG_INIT;
public:
    void lock()   { while (flag_.test_and_set(std::memory_order_acquire)) {} }
    void unlock() { flag_.clear(std::memory_order_release); }
};

std::atomic<Node*> head;
void push(Node* n) {
    Node* old = head.load(std::memory_order_relaxed);
    do { n->next = old; } while (!head.compare_exchange_weak(old, n,
                                     std::memory_order_release, std::memory_order_relaxed));
}
// 注意：pop 后被弹出的节点谁来释放？——无锁结构必须回答这个问题，
// 否则就是经典的 ABA + 内存泄漏问题（见并发书第 7 章与多处理器编程艺术版第 10 章）。
```

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++11 | `std::thread`/`future`/`promise`/`packaged_task`/`atomic`/`mutex`/`condition_variable` + 内存模型首次入标准 |
| C++14 | `std::shared_timed_mutex`（读写锁）、原子操作的部分改进 |
| C++17 | `std::scoped_lock`、`std::shared_mutex`、并行算法与执行策略（`par`/`par_unseq`） |
| C++20 | **`jthread` + `stop_token`**（可取消）、**`atomic::wait/notify`**（P1135）、`latch`/`barrier`/`semaphore`、`atomic_ref` |
| C++23 | 并行算法补齐（`std::execution::for_each` 一系，见「Parallelism 2」提案）；`barrier` 的 `arrive` 系列完善 |
| C++26 | **`std::hazard_pointer` 与 RCU 进入标准**（回收问题的正式答案）；`std::execution` 与 executors 继续整合 |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Adve & Gharachorloo, *Shared Memory Consistency Models: A Tutorial* | **IEEE Computer 1996** | 一致性模型最经典的综述 |
| Boehm & Adve, *Foundations of the C++ Concurrency Memory Model* | **PLDI 2008** | C++11 内存模型的理论根基 |
| Batty et al., *Mathematizing C++ Concurrency* | **POPL 2011** | 形式化模型，并找出标准中的漏洞 |
| Lahav et al., *Repairing Sequential Consistency in C/C++11* | **PLDI 2017** | RC11 模型，C++20 之后的语义基础 |
| ISO/IEC 14882，`[intro.races]`、`[atomics.order]` | C++ 标准 | happens-before 与内存序的正式条款 |
| **P1135** *atomic::wait and atomic::notify* | **WG21 提案** | 让原子变量可以阻塞等待，取代忙轮询 |

---

## 近年研究与工业界开源实践（2015–2026）

- **`jthread`/`stop_token` 改变了「取消」这件事的可写性**：不再需要每个循环都手写 `while (!stop_requested())`。
- **`atomic::wait/notify`（P1135）落地**：自旋等待被替换为「休眠 + 唤醒」，在无锁队列等待场景上有明显收益。
- **TSan 常态化**：数据竞争的检测已经进入 CI；但 TSan 只能发现**被执行的路径**上的竞争，未覆盖的路径需要靠测试设计补齐。
- **真正的无锁代码在减少**：工业界更倾向「分段 + 锁」或「RCU + 延迟回收」；`folly` 的 `ConcurrentHashMap` 与 `SharedMutex` 是典型样本。
- 🔧 **RCU 与 hazard pointer 进入 C++26**：`std::hazard_pointer` 的提案方向是把「读侧无锁 + 写侧延迟回收」的标准做法写进标准库，直接补上本章第 5 节留下的洞。
- 🔧 **执行策略的现实状态**：C++17 的 `par_unseq` 在实践中因向量化语义与开销问题使用受限；C++23 通过「Parallelism 2」补充了 `std::execution::for_each` 等算法，但**完整的 executors（`std::exec::`）仍未进标准**，工业上仍用 `oneTBB`、`folly` 自带的执行器。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `facebook/folly` | **30.5k★** | `SharedMutex`、`MPMCQueue`、hazard pointer 式回收的工业范本 |
| `uxlfoundation/oneTBB` | **6.8k★** | 任务窃取 + 并行算法实现，比手写线程池更稳 |
| `google/sanitizers` | **12.5k★** | TSan 的数据竞争检测，本章所有规则的执行者 |
| `google/benchmark` | **10.4k★** | 量化不同内存序与锁策略的实际收益 |
| `microsoft/STL` | **11.2k★** | `atomic`/`jthread`/`stop_token` 的标准实现 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「用了 `std::atomic` 就线程安全」 | 原子只保护**单个变量**；跨变量的不变式仍要靠锁 |
| 2 | 「`relaxed` 随处可用」 | 一旦操作间有数据依赖（读对方写的 payload），必须用 acquire/release |
| 3 | 「x86 上跑过就没事」 | x86 是 TSO，许多重排只在 ARM/POWER 上暴露 |
| 4 | 「`detach()` 之后就不用管了」 | 脱离后线程可能在主线程退出后仍在跑，捕获的局部变量会悬垂 |
| 5 | 「无锁一定更快」 | 争用下的 CAS 失败重试与缓存行乒乓常使其慢于锁；且回收方案可能是灾难 |
| 6 | 🔧 本讲的「内存模型」只走马观花 | 这是有意的：深度内容在 `book/C++并发编程实战2/05-Cpp内存模型与原子操作.md`，本目录不重复 |
| 7 | 🔧 本讲未提 `atomic::wait/notify`（P1135） | 它们已进入 C++20；自旋等待应改成 `wait`，省掉热点 CPU |
| 8 | 🔧 未强调 `std::jthread` 与 `stop_token` | C++20 起应该有默认选择：可取消的线程比「不可取消 + 超时轮询」更可靠 |
| 9 | 🔧 未提 C++26 的 `std::hazard_pointer` | 无锁结构的内存回收终于有了标准答案，值得在 2026 年的技术规划中占位 |

---

## 与其他章 / 其他书的联系

- **必读**：`book/C++并发编程实战2/05-Cpp内存模型与原子操作.md`——修改序列、释放序列、栅栏的严格推导都在那里。
- `book/C++并发编程实战2/02-线程管控.md`：`std::thread` 生命周期与参数传递的完整讨论。
- `book/C++并发编程实战2/03-线程间共享数据.md`：死锁四条件与锁的选择。
- `book/C++并发编程实战2/06-基于锁的并发数据结构.md`：本章第 3、5 节的结构化版本。
- `book/C++并发编程实战2/07-无锁数据结构.md`：ABA 与引用计数回收。
- `book/多处理器编程的艺术2/19-乐观与手工内存管理.md`：RCU 与 hazard pointer 的理论与算法层解释。
- `book/多处理器编程的艺术2/10-队列内存回收与ABA.md`：本章「回收才是难点」那一行字背后的完整故事。
- **`12-工具漫谈与构建依赖.md`**：TSan 与 thread-sanitizer 在 CI 中的接入方式。
