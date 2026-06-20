# clh

在 Craig、Landin 和 Hagersten (CLH) 队列锁 问世之前，常见的同步机制主要依赖于 TAS（Test-and-Set）、TTAS（Test-and-Test-and-Set）、Peterson 锁、Bakery 算法等。这些早期的同步机制存在一些局限性，特别是在多处理器系统中使用时性能不佳的问题。CLH 队列锁作为一种改进方案，解决了这些问题，并引入了一些新的特性。
### 发明 CLH 队列锁之前的常见同步机制

1. Test-and-Set (TAS):
   - 工作原理: 使用一个原子操作来检查并设置某个标志位，用于表示是否有一个线程正在访问临界区。
   - 问题: 高竞争条件下会导致大量缓存一致性流量，因为所有线程都在竞争同一个内存位置。
2. Test-and-Test-and-Set (TTAS):
   - 工作原理: 在 TAS 的基础上增加了一层测试，即在执行 TAS 之前先进行一次非原子的读取检查。
   - 问题: 尽管减少了对共享变量的竞争，但在高竞争环境下仍然会产生大量的缓存失效和内存总线流量。
3. Peterson 锁:
   - 工作原理: 主要用于两个线程间的互斥，通过两个布尔变量和一个指示当前“轮到”哪个线程进入临界区的计数器实现。
   - 问题: 扩展性差，难以应用于多于两个线程的情况；并且在现代硬件架构上可能无法保证正确性。
4. Bakery 算法:
   - 工作原理: 类似于现实生活中的排队买票，每个线程获取一个唯一的号码，只有当其号码是最小的时候才能进入临界区。
   - 问题: 需要维护全局状态，导致较高的内存开销和潜在的性能瓶颈。

### CLH 队列锁的改进之处
CLH 队列锁是由 Craig, Landin 和 Hagersten 提出的一种基于链表结构的自旋锁机制，它有效地解决了上述传统同步机制存在的问题：
1. 减少缓存失效:
   - 每个线程都有自己的节点，节点之间形成一个单向链表。只有当前节点的状态会影响下一个节点的行为，这样就避免了所有线程争抢同一个内存位置的情况，从而减少了缓存失效的数量。
2. 提高可扩展性:
   - CLH 锁设计为支持多个线程同时等待，通过链表结构可以轻松地管理任意数量的等待者，具有良好的扩展性。
3. 公平性:
   - CLH 锁确保了请求锁的顺序与释放锁的顺序一致，提供了一定程度上的公平性，防止某些线程长时间得不到调度（饥饿现象）。
4. 低延迟:
   - 当前持有锁的线程释放锁时，只需要通知下一个等待的线程即可，无需遍历整个等待队列，降低了解锁操作的延迟。
5. 局部性优化:
   - 由于每个线程只关心其前驱节点的状态，这有助于提升 CPU 缓存的局部性，进一步提高了性能。

综上所述，CLH 队列锁通过引入一种新的同步模型，解决了早期同步机制中存在的诸多问题，特别是针对多处理器环境下的高效性和公平性做出了显著改进。然而，值得注意的是，尽管 CLH 锁在很多场景下表现出色，但它并不是万能的，在某些特定的应用场景中，其他类型的锁如 MCS 锁可能会更适合。例如，MCS 锁相比 CLH 锁，在某些情况下能更好地利用局部性优势，减少不必要的内存访问。因此，选择合适的锁类型应根据具体的应用需求而定。
如果你在寻找 C/C++ 实现的 CLH 队列（或自旋锁）开源库，以下是几个推荐和资源，涵盖 CLH Lock、队列实现、无锁/低锁并发结构 的开源项目和库，适合嵌入式系统、高性能服务器、操作系统开发等场景。

## 一、支持 CLH 锁或队列的开源库推荐

### 🔹 1. [libcds (Concurrency Data Structures for C++)](https://github.com/khizmax/libcds)

- 语言: C++
- 特点:
  - 支持多种无锁数据结构：队列、栈、哈希表等
  - 提供 `cds::sync::clh_lock` 实现 CLH 自旋锁
  - 跨平台支持（Linux / Windows）
- 适用场景:
  - 多线程高并发环境下的同步控制
  - 对公平性要求高的锁机制
- 文档地址: https://libcds.sourceforge.net/doc/cds-api/

```cpp
#include <cds/sync/clh_lock.h>

cds::sync::clh_lock lock;
{
    cds::sync::clh_lock::scoped_lock sl(lock);
    // critical section
}
```



### 🔹 2. [Boost.Thread](https://www.boost.org/doc/libs/release/libs/thread/)

- 语言: C++
- 特点:
  - Boost 是 C++ 最广泛使用的标准外库之一
  - 虽然没有直接提供 CLH 队列，但提供了丰富的多线程原语（mutex、condition variable、atomic 等）
  - 可作为你自己实现 CLH 队列的基础库
- 文档地址: https://www.boost.org/doc/libs/release/libs/thread/



### 🔹 3. [tbox (TBOOX Open Source Library)](https://github.com/tboox/tbox)

- 语言: C
- 特点:
  - 跨平台、模块化设计
  - 包含多种同步锁（spinlock, mutex 等）
  - 可以结合 atomic 和 thread 模块实现 CLH 队列逻辑
- 文档地址: https://tboox.io/#/

> 注：虽然没有内置 CLH 锁，但其原子操作和线程管理模块非常适合构建自己的 CLH 队列。



### 🔹 4. [Folly (Facebook's Open-source Library)](https://github.com/facebook/folly)

- 语言: C++
- 特点:
  - Facebook 开源的现代 C++ 工具库
  - 提供高性能并发结构（如 `DistributedMutex`, `AtomicLinkedList`）
  - 虽未直接提供 CLH 队列，但有很多底层工具可复用
- 文档地址: https://github.com/facebook/folly/wiki



### 🔹 5. [MoodyCamel's ConcurrentQueue](https://github.com/cameron321/concurrentqueue)

- 语言: C++
- 特点:
  - 无锁队列（Wait-free / Lock-free）
  - 高性能、跨平台、生产级代码
  - 不是 CLH 队列，但可用于替代 CLH 队列实现场景
- 适用场景:
  - 高吞吐量的生产者-消费者模型
  - 无锁通信、日志系统、任务调度器

## 二、CLH 队列实现参考项目（可学习）
以下是一些公开的 CLH 队列实现示例，可供学习或直接使用：
### 示例 1：GitHub 上的 CLH 锁实现
- 地址：https://gist.github.com/coolxv/6f0e8c91b2d7a07d7f8c
- 内容：
  - 使用 `std::atomic`
  - C++11 实现 CLH 自旋锁
  - 简洁易懂，适合教学和快速集成

### 示例 2：StackOverflow 上的 CLH 锁实现（C++）
- 地址：https://stackoverflow.com/questions/44532715/implementing-clh-lock-in-c
- 特点：
  - 基于链表的节点结构
  - 使用 `std::shared_ptr` 避免内存泄漏
  - 支持 RAII 风格加锁

### 示例 3：《Art of Multiprocessor Programming》书中的伪代码实现
- 推荐书籍：[The Art of Multiprocessor Programming](https://dl.acm.org/doi/book/10.5555/2385482)
- 内容：
  - 经典并发算法教材
  - 包含 CLH 锁、MCS 锁等公平锁实现
  - 可作为理论基础 + 伪代码参考

## 三、如何选择？
| 目标 | 推荐 |
|------|------|
| 学习 CLH 锁原理 | GitHub 示例、StackOverflow 示例、《Art of Multiprocessor Programming》 |
| 在 C++ 中使用 CLH 锁 | libcds |
| 构建自己的 CLH 队列 | Boost.Thread 或 tbox + std::atomic |
| 替代 CLH 队列（更高性能） | moodycamel::concurrentqueue |
| 嵌入式系统 / 小型项目 | 手写 CLH 锁 + tbox 原子操作 |

## 四、总结一句话
> 如果你需要一个现成的 C/C++ CLH 队列库，推荐使用 libcds；如果只是想实现或学习 CLH 锁，可以参考 GitHub 上的开源实现或者 StackOverflow 示例。对于高性能无锁队列，也可以考虑 moodycamel::concurrentqueue。

如果你希望我：
- 帮你生成一个完整的 CLH 队列实现（C++/C）
- 基于 Boost 或 tbox 构建
- 支持 CMake 构建系统
- 支持 RAII、智能指针、日志跟踪等功能


`CLH Lock`（Craig, Landin, and Hagersten）是一种基于链表的公平自旋锁，常用于实现无等待线程同步机制。它非常适合用于高性能并发场景，如操作系统内核、实时系统和高性能库中。

在 C++ 生态中，一些知名的开源库（如 Boost.Thread 和 Facebook Folly）都提供了与 CLH 类似的并发原语或锁机制。虽然它们可能没有直接命名 `CLH Lock`，但其底层原理相似，都是通过节点链表维护线程排队顺序，从而实现公平性。
## 一、CLH Lock 的基本概念
### 原理简述：
- 每个线程将自己加入一个隐式的链表队列
- 每个线程只关注前驱节点的状态（是否释放锁）
- 线程自旋等待，直到前驱节点释放锁
- 公平性强，先进先出（FIFO）

### 优点：
- 高效缓存一致性（仅访问本地变量）
- FIFO 公平性
- 不需要原子交换操作（可以用 fetch_add 实现）

## 二、使用 Boost 实现类似 CLH 的锁（间接方式）
Boost 并没有直接提供 `CLH Lock`，但它提供了底层的原子操作和线程支持，可以手动实现一个简单的 CLH 锁。
### 示例：Boost 中实现简易 CLH Lock
```cpp
#include <boost/thread.hpp>
#include <atomic>
#include <iostream>

struct CLHNode {
    std::atomic<bool> spin{true};
};

class CLHLock {
public:
    using Node = CLHNode;

    CLHLock() {
        tail = new Node();
    }

    ~CLHLock() {
        delete tail;
    }

    void lock(Node*& node) {
        node = new Node();
        Node* prev = tail.exchange(node);
        node->spin.store(true);
        while (prev->spin.load()) {} // 自旋等待前驱释放
    }

    void unlock(Node* node) {
        node->spin.store(false);
        delete node;
    }

private:
    std::atomic<Node*> tail;
};

// 使用示例
void threadFunc(CLHLock& lock, int id) {
    CLHLock::Node* node;
    lock.lock(node);
    std::cout << "Thread " << id << " entered critical section" << std::endl;
    boost::this_thread::sleep_for(boost::posix_time::millisec(100));
    lock.unlock(node);
}

int main() {
    CLHLock lock;
    std::vector<boost::thread*> threads;

    for (int i = 0; i < 5; ++i)
        threads.push_back(new boost::thread(threadFunc, std::ref(lock), i));

    for (auto t : threads)
        t->join();

    return 0;
}
```

## 三、Facebook Folly 提供的类似结构（间接使用）
Facebook Folly库提供了多种高性能并发原语，其中最接近CLH的是：

### `folly::DistributedMutex`
- 分布式互斥锁，适用于 NUMA 架构
- 内部使用类似 CLH 的排队机制
- 每个线程都有自己的局部状态，避免跨核心竞争

#### 示例代码：使用 `folly::DistributedMutex`

```cpp
#include <folly/DistributedMutex.h>
#include <thread>
#include <iostream>

folly::DistributedMutex mutex;

void threadFunc(int id) {
    std::lock_guard<folly::DistributedMutex> lock(mutex);
    std::cout << "Thread " << id << " entered critical section" << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i)
        threads.emplace_back(threadFunc, i);

    for (auto& t : threads)
        t.join();

    return 0;
}
```

## 四、其他类似结构推荐（C++ 标准 + 第三方库）

| 技术 | 描述 | 推荐理由 |
|||-|
| `std::mutex` / `std::unique_lock` | C++11 标准锁 | 简单易用，适合大多数场景 |
| `folly::SpinLock` | Folly 提供的轻量级自旋锁 | 单核性能高，低延迟 |
| `folly::UnboundedQueue` | 支持生产者消费者模型的无界队列 | 可用于替代你自己的 CLH 队列 |
| `boost::fibers::mutex` | Boost.Fiber 提供的协程安全锁 | 支持纤程调度器下的同步 |

## 五、总结对比表

| 特性 | Boost 手动实现 CLH | Folly DistributedMutex | C++ 标准 mutex |
||||-|
| 是否公平 | 是（FIFO） | 是 | ❌ 否 |
| 是否自旋 | 是 | 是 | ❌ 否 |
| 性能 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 易用性 | ❌ 复杂 | 简单 | 简单 |
| 是否适合 NUMA | ❌ | | ❌ |
| 是否可移植 | | ✅（Linux） | |

## 六、建议
如果你的目标是：

- 实现一个公平且高效的并发控制结构
- 替代你自己写的 `LockFreeLinkedQueue`
- 在多线程环境下保证顺序执行

你可以选择以下方案之一：

### 推荐方案 1：使用 Folly 的 `DistributedMutex`（适合 Linux 高性能并发）

```cpp
#include <folly/DistributedMutex.h>
folly::DistributedMutex mtx;
std::lock_guard lock(mtx);
```

### 推荐方案 2：使用 Boost 手动实现 CLH（跨平台兼容好）
- 如果你需要完全掌控锁机制，或项目必须支持 Windows，建议使用 Boost + 自定义 CLH

## 如需帮助

如果你愿意提供你的 `LockFreeLinkedQueue` 实现，我可以帮你：

- 改写为使用 `folly::DistributedMutex` 或 `boost::thread`
- 加入测试用例验证公平性和正确性
- 转换为更现代的 C++ 设计（如 RAII + `std::shared_ptr`）
