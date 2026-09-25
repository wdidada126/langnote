# 第 5 章 C++ 内存模型和原子操作

> **一句话**：内存模型回答一个问题——**一个线程的写，什么时候对另一个线程可见**；六种内存序就是六种不同强度的承诺。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 | 基础概念 | 对象、内存区域、修改序列 |
| 5.2 | 原子类型 | `atomic_flag`、整型原子、`is_always_lock_free` |
| 5.3 | 六种内存序 | seq_cst、acquire、release、acq_rel、relaxed、consume |
| 5.4 | 释放序列与栅栏 | 为什么读改写操作能传递同步关系 |
| 5.5 | 让非原子操作服从内存序 | 用 acquire/release 保护普通数据 |

---

## 核心精讲

### 5.1 修改序列（modification order）

每个原子变量都有一个唯一的修改序列，所有线程必须同意这个顺序。它比 happens-before 更基础：即使两个操作之间没有同步关系，它们也必须落在同一条修改序列上。

### 5.2 六种内存序

| 内存序 | 语义 | 典型用途 |
| --- | --- | --- |
| `memory_order_seq_cst` | 再加一个全局唯一顺序 | 默认值，最安全；先用它写对，再谈优化 |
| `memory_order_acquire` | 之后的读写不能重排到它前面 | 加锁、读取已发布指针 |
| `memory_order_release` | 之前的读写不能重排到它后面 | 解锁、发布数据 |
| `memory_order_acq_rel` | acquire 加 release | CAS 成功路径 |
| `memory_order_relaxed` | 只保证原子性，不保证顺序 | 计数器 |
| `memory_order_consume` | 只携带依赖顺序 | 实际实现都按 acquire 处理，不建议使用 |

```cpp
// 教学示意：release / acquire 的经典搭配（不参与构建）
std::atomic<bool> ready{false};
int data = 0;

void writer() {
    data = 42;                                    // 1) 写普通数据
    ready.store(true, std::memory_order_release); // 2) 发布：1 不会被重排到 2 之后
}
void reader() {
    while (!ready.load(std::memory_order_acquire)) {}  // 3) 获取
    assert(data == 42);                           // 4) 一定成立
}
```

**这一个例子就是本章的核心，值得亲手推一遍。**

### 5.3 计数场景为什么 relaxed 就够

```cpp
// 教学示意：引用计数（不参与构建）
std::atomic<int> refcount{1};
void inc_ref() { refcount.fetch_add(1, std::memory_order_relaxed); }
void dec_ref() {
    if (refcount.fetch_sub(1, std::memory_order_acq_rel) == 1) {
        delete this;              // acq_rel 保证能看见其他线程的写入
    }
}
```

理由：计数本身不携带任何数据依赖，只需要「不丢更新」；而在真正析构时，需要一个 acquire 语义来看到别人写过的内容。

### 5.4 释放序列与比较交换

关键点：**读改写（RMW）操作会延长释放序列**。因此一串 RMW 可以把 Release 之前的写入一直传递到后面的 Acquire 读取者。

```cpp
// 教学示意：自旋锁（不参与构建）
class spinlock {
    std::atomic_flag flag = ATOMIC_FLAG_INIT;
public:
    void lock()   { while (flag.test_and_set(std::memory_order_acquire)) {} }
    void unlock() { flag.clear(std::memory_order_release); }
};
```

> `compare_exchange_weak` 可能因虚假失败返回 false，必须放在循环里；只有在循环体开销很小时才值得用 weak 版本。

### 5.5 栅栏

```cpp
std::atomic_thread_fence(std::memory_order_release);   // 配合 relaxed store 使用
```

栅栏的特点是它不依附于某个具体的原子变量，而是对「前后的所有操作」施加顺序约束。它常用于同时发布多个变量，或把多个 relaxed 操作组合成一次性的发布。

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++11 | 首次给出内存模型与 `<atomic>`；`consume` 从一开始就争议最大 |
| C++17 | 明确不建议依赖 `consume`（多数实现直接当成 acquire） |
| C++20 | 新增 `atomic::wait/notify`、`atomic_ref`；继续完善形式化描述 |

---

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Adve & Gharachorloo, *Shared Memory Consistency Models: A Tutorial* | **IEEE Computer 1996** | 一致性模型最经典的综述 |
| Boehm & Adve, *Foundations of the C++ Concurrency Memory Model* | **PLDI 2008** | C++11 模型的基础 |
| Batty et al., *Mathematizing C++ Concurrency* | **POPL 2011** | 首次给出形式化模型，并找出了标准中的漏洞 |
| Lahav et al., *Repairing Sequential Consistency in C/C++11* | **PLDI 2017** | 修复 SC 相关缺陷，提出 RC11 模型 |
| Sewell et al., *x86-TSO* | **CACM 2010** | x86 硬件模型的严格刻画 |

---

## 近年研究与工业界开源实践

- **RC11 成为共识**：C++20 之后的主流语义模型采用 RC11，编译器层面的实现也在向它对齐。
- **跨语言内存模型互操作**：Rust 的原子序与 C++ 高度相似，两者的形式化模型已经可以放在一起做跨语言验证。
- **弱内存序必须在弱序硬件上测**：x86 是 TSO，很多错误坐等到 ARM 或 POWER 上才暴露。

| 实现 | star | 说明 |
| --- | --- | --- |
| `facebook/folly` | ≈**30.5k★** | 大量自定义的 acquire/release 用法，并有 `AtomicStructOfArrays` 减少伪共享 |
| `google/benchmark` | ≈**10.4k★** | 量化不同内存序带来的收益，避免为了优化而优化 |
| `google/sanitizers` | ≈**12.5k★** | TSan 的数据竞争检测底层依赖 happens-before 的形式化定义 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「用了 atomic 就不用考虑锁」 | 原子量只保护单个变量的原子性，多变量的不变式仍需同步 |
| 2 | 「relaxed 到处都能用」 | 只要操作之间携带数据依赖，就必须用 acquire 或 release |
| 3 | 「x86 上测过就没问题」 | 弱序硬件（ARM、POWER）会暴露许多 x86 上看不出的重排 |
| 4 | 「consume 能省很多开销」 | 实践中编译器都按 acquire 处理，收益为零，反而增加误解 |
| 5 | 🔧 本书对 consume 的篇幅偏多 | 2026 年的建议是**不用 consume**，只用 seq_cst 与 acquire/release 两类 |
| 6 | 🔧 本书未强调 `is_always_lock_free` | 大类型的 `std::atomic` 可能在内部退化为带锁实现，使用前应先检查 |

---

## 与其他章 / 其他书的联系

- **第 7 章**直接使用本章的六种内存序来实现无锁栈与队列。
- **`book/多处理器编程的艺术2/04-共享内存基础.md`**：同一主题的理论版本（寄存器分级、层级构造与原子快照）。
- **`book/Java并发编程之美/concepts/volatile.md`**：Java 的 volatile 与 VarHandle 的五种访问模式可与本节对照。
