# 笔记：C++11 `std::shared_ptr` 总结与使用

> **来源**：博客园 [C++11 std::shared_ptr总结与使用](https://www.cnblogs.com/xudong-bupt/p/9027609.html)
> **作者**：旭东的博客（xudong-bupt）
> **发布时间**：2018-05-12 10:34
> **原文阅读**：约 6.3 万
> **整理日期**：2026-09-12
> **一句话概括**：`std::shared_ptr` 用**引用计数**管理共享所有权，在最后一个持有者析构时**自动释放资源**；计数增减是原子的（线程安全），但被指向对象本身不因此获得保护。

---

## 1. 核心要点（原文总结的 7 条）

| # | 要点 | 说明 |
|---|---|---|
| 1 | **自动释放资源** | 智能指针主要用途是方便资源管理：没有指针引用时自动释放。 |
| 2 | **引用计数标识共享数** | 用引用计数表示是否还有多余指针指向该资源；**shared_ptr 自身也算 1 个引用**。 |
| 3 | **赋值会加减计数** | 赋值时：原资源计数 **−1**，新指向的资源计数 **+1**。 |
| 4 | **计数操作是原子的** | 引用计数加一/减一是原子操作，故计数管理线程安全。 |
| 5 | **优先 `make_shared`** | 可一次性把所需内存分配好，优于 `shared_ptr<T>(new T)`。 |
| 6 | **大小是裸指针的两倍** | 内部一个指针指向资源对象，另一个指向引用计数（控制块）。 |
| 7 | **计数在动态分配的控制块中** | 因此支持拷贝，新指针可获知当前引用计数个数（`use_count()`）。 |

赋值语义示例：

```cpp
std::shared_ptr<Test> p1(new Test);
std::shared_ptr<Test> p2(new Test);
p1 = p2;   // p1 原资源计数 -1（归零则析构），p2 的资源计数 +1
```

`make_shared` 与 `new` 的写法对比：

```cpp
std::shared_ptr<Test> p = std::make_shared<Test>();   // 推荐
std::shared_ptr<Test> p(new Test);                    // 不推荐（两次分配）
```

---

## 2. 原文示例代码（多线程下的引用计数演示）

```cpp
#include <iostream>
#include <memory>
#include <thread>
#include <chrono>
#include <mutex>

struct Test
{
    Test() { std::cout << "  Test::Test()\n"; }
    ~Test() { std::cout << "  Test::~Test()\n"; }
};

// 线程函数
void thr(std::shared_ptr<Test> p)
{
    // 线程暂停 1s
    std::this_thread::sleep_for(std::chrono::seconds(1));

    // 赋值操作，shared_ptr 引用计数 use_count 加 1（c++11 中是原子操作）
    std::shared_ptr<Test> lp = p;
    {
        // static 变量（单例模式），多线程同步用
        static std::mutex io_mutex;

        // std::lock_guard 加锁
        std::lock_guard<std::mutex> lk(io_mutex);
        std::cout << "local pointer in a thread:\n"
                  << "  lp.get() = " << lp.get()
                  << ", lp.use_count() = " << lp.use_count() << '\n';
    }
}

int main()
{
    // 使用 make_shared 一次分配好需要内存
    std::shared_ptr<Test> p = std::make_shared<Test>();
    // std::shared_ptr<Test> p(new Test);

    std::cout << "Created a shared Test\n"
              << "  p.get() = " << p.get()
              << ", p.use_count() = " << p.use_count() << '\n';

    // 创建三个线程 t1,t2,t3
    // 形参作为拷贝，引用计数也会加 1
    std::thread t1(thr, p), t2(thr, p), t3(thr, p);
    std::cout << "Shared ownership between 3 threads and released\n"
              << "ownership from main:\n"
              << "  p.get() = " << p.get()
              << ", p.use_count() = " << p.use_count() << '\n';

    // 等待结束
    t1.join(); t2.join(); t3.join();
    std::cout << "All threads completed, the last one deleted\n";

    return 0;
}
```

> 说明：示例出自 cppreference 的 shared_ptr 词条风格。原博文写了"编译执行:"一行但**未附编译命令与运行输出**；示例代码首行 `include <iostream>` 漏了 `#`，本笔记已补全。

---

## 3. 示例运行过程与预期输出

编译：

```bash
g++ -std=c++11 -pthread shared_ptr_demo.cpp -o shared_ptr_demo
./shared_ptr_demo
```

执行流程与计数变化：

| 阶段 | 事件 | `use_count()` |
|---|---|---|
| 1 | `make_shared<Test>()` 构造 | 1 |
| 2 | 三个线程对象构造，形参**按值拷贝**，各 +1 | 4 |
| 3 | `main` 打印后 `join` | — |
| 4 | 三个线程各 `sleep(1s)`，内部 `lp = p` 再 +1 | 5（各线程内） |
| 5 | 线程结束，形参 `p`、局部 `lp` 析构，逐次 −1 | 降至 1 |
| 6 | `main` 中 `p` 析构，计数归零 | **`~Test()` 被调用** |

预期输出（顺序在 `use_count` 打印处基本确定，线程内部的先后不确定）：

```
  Test::Test()
Created a shared Test
  p.get() = 0x..., p.use_count() = 1
Shared ownership between 3 threads and released
ownership from main:
  p.get() = 0x..., p.use_count() = 4
local pointer in a thread:
  lp.get() = 0x..., lp.use_count() = 5
local pointer in a thread:
  lp.get() = 0x..., lp.use_count() = 5
local pointer in a thread:
  lp.get() = 0x..., lp.use_count() = 5
All threads completed, the last one deleted
  Test::~Test()
```

> 注意：`std::cout << p`（未加 `.get()`）打印的是布尔值（非空为 `1`），原文统一使用 `p.get()` 打印地址，这是正确写法。

---

## 4. 原文参考链接

- http://www.cnblogs.com/xudong-bupt/p/6736783.html
- https://blog.csdn.net/coolmeme/article/details/43195587
- http://www.cnblogs.com/lanxuezaipiao/p/4132096.html

---

## 5. 整理者补充与勘误

### 5.1 原文笔误

- `shart_ptr` → 应为 `shared_ptr`。
- 代码注释中的 `use_cont` → 应为 `use_count`。
- 示例代码首行缺 `#`，已在笔记中补为 `#include <iostream>`。
- 原文"编译执行:"后未给出命令和输出，本笔记补了 `g++ -std=c++11 -pthread` 与预期输出。

### 5.2 "线程安全"要说清楚边界（原文只说了计数原子）

`shared_ptr` 的线程安全需要拆成三层：

| 层面 | 是否线程安全 |
|---|---|
| 不同 `shared_ptr` 实例同时操作 | ✅ 安全（各自独立） |
| **同一个** `shared_ptr` 实例被多线程同时读写（`=`、`reset`） | ❌ **不安全**，会数据竞争；需自行加锁或用 `std::atomic<std::shared_ptr<T>>`（C++20）／`std::atomic_load/store(&sp)`（C++11 已弃用） |
| 计数增减（`use_count` 内部操作） | ✅ 原子 |
| **被指向对象本身**的读写 | ❌ 与智能指针无关，需自己同步（原文示例正是用 `mutex` 保护 `std::cout`） |

另外：**`use_count()` 在多线程环境下只是近似值**，不要用它做同步或正确性判断。

### 5.3 `make_shared` 的优势与代价

- **优势**：对象与控制块**一次分配**（通常同一块内存），少一次 malloc、缓存局部性更好；异常安全（`shared_ptr(new T)` 在参数求值阶段若抛异常可能泄漏）。
- **代价**：① 控制块与对象同块内存，**只要还有 `weak_ptr` 存活，整块内存（含对象空间）都不会归还**给分配器；② 若自定义了 `operator new/delete`（如类级内存池），`make_shared` **不会**使用它。

### 5.4 大小与开销

"大小为裸指针两倍"是**主流实现**（libstdc++ / libc++ / MSVC）的情况：`ptr` + 控制块指针。所以：

- **按值传参** `void f(std::shared_ptr<T> p)` 是有成本的（拷贝 + 原子加/减）；只读场景应传 `const std::shared_ptr<T>&`。
- 需要**延长生命周期**时才按值传（原文示例的线程函数正是这种故意按值传的场景）。
- 若只要访问对象，更轻量的是传 `T*` / `T&`，但**必须保证生命周期覆盖调用期**。

### 5.5 必须配对的坑

- **循环引用**：`A` 持有 `shared_ptr<B>`，`B` 持有 `shared_ptr<A>` → 计数永不归零，**内存泄漏**。解法：一方改为 `std::weak_ptr`，用 `lock()` 升级后再访问。
- **`enable_shared_from_this`**：类内部要拿到指向自身的 `shared_ptr`，必须继承它并调用 `shared_from_this()`；直接 `shared_ptr<T>(this)` 会创建**第二个控制块**，导致双重析构。
- **所有权语义**：`shared_ptr` 表达**共享所有权**；若语义上只有一个主人，应用 `std::unique_ptr`（零开销、可 `std::move`），需要共享时再转换。
- **跨模块/DLL 边界**：控制块与删除器由创建方决定，跨 CRT 或跨库传递可能因分配器不匹配而崩溃。

### 5.6 与相关设施的关系

- `std::make_shared` / C++20 的 `std::make_shared_for_overwrite`。
- C++17 起 `std::shared_ptr` 支持 `[]` 数组形式的 `shared_ptr<T[]>`（但 `make_shared` 支持数组要到 C++20）。
- 自定义删除器：`std::shared_ptr<T>(new T, [](T* p){ ... })`；用 `make_shared` 时不支持自定义删除器。
