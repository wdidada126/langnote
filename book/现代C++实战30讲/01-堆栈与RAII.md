# 讲 01｜堆栈与 RAII：C++ 里该如何管理资源？

> **一句话**：C++ 的资源管理只有一条主线——**把资源的所有权放进对象，让构造获取、析构释放**；栈上对象因此成为默认选择，而 RAII 是这条主线的名字。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 讲 01 引子 | 栈与堆的代价差异 | 栈分配只是改栈指针，堆分配涉及元数据与系统调用，默认应该是栈 |
| 资源与裸指针 | 为什么 `new` 出来的指针容易泄漏 | 异常或提前 return 会跳过任何「记得释放」的约定 |
| RAII | 构造函数获取、析构函数释放 | 作用域即是生命周期，异常路径自动走析构 |
| 作用域守卫 | 锁、文件句柄、临时状态回滚 | 把「配对操作」写成构造/析构，而不是 try/finally |
| 可移动、不可复制 | 所有权语义的表达方式 | 移动表示「转移」，复制表示「共享一份」 |
| 与智能指针的关系 | 本讲留下的尾巴 | `unique_ptr`/`shared_ptr` 只是 RAII 的现成实现，见 `02-自己动手实现智能指针.md` |
| 🔧 现代补充 | 常量正确性、`noexcept`、`constexpr` 容器 | 2026 年的 RAII 还要顺带谈「析构不许抛」与编译期可构造性 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 栈上的对象才是默认答案

```cpp
// 教学示意：栈对象的代价远低于堆对象（不参与构建）
void stack_path() {
    std::string a = "hello";        // 一次分配，栈上对象持有堆缓冲区
    std::vector<int> v{1, 2, 3};    // 同理：栈上小对象 + 堆上缓冲
    // 离开作用域：a、v 的析构按逆序自动调用
}

void heap_path() {
    auto* p = new std::string("hello");  // 裸 new：所有权立刻变得模糊
    // 若这里提前 return 或抛异常，delete 就不会被执行
    delete p;
}
```

要点不是「栈一定更快」，而是**栈对象的生命周期由作用域决定，因此不存在「忘记释放」这一类错误**。

### 2. RAII 的最小形态

```cpp
// 教学示意：把资源装进对象（不参与构建）
class File {
    FILE* fp_ = nullptr;
public:
    explicit File(const char* path) : fp_(std::fopen(path, "rb")) {
        if (!fp_) throw std::runtime_error("open failed");   // 构造失败就不留半成品
    }
    ~File() { if (fp_) std::fclose(fp_); }                  // 无论怎么离开都释放
    File(const File&) = delete;                             // 不可复制
    File(File&& other) noexcept : fp_(other.fp_) { other.fp_ = nullptr; }
    File& operator=(File&& other) noexcept {
        if (this != &other) { if (fp_) std::fclose(fp_); fp_ = other.fp_; other.fp_ = nullptr; }
        return *this;
    }
    FILE* get() const { return fp_; }
};
```

三条可迁移的律令：

1. **构造函数要么成功，要么抛异常**；不要在构造函数里留下需要调用方额外调用的 `init()`。
2. **析构函数必须 `noexcept`**：析构抛异常会直接调用 `std::terminate`。
3. **五条特殊成员函数**（拷贝构造、拷贝赋值、移动构造、移动赋值、析构）要一起考虑；删掉其一往往要显式删掉其他（「规则 of five」）。

### 3. 作用域守卫：锁是最典型的例子

```cpp
// 教学示意：用 RAII 表达「配对操作」（不参与构建）
class MutexLockGuard {
    std::mutex& m_;
public:
    explicit MutexLockGuard(std::mutex& m) noexcept : m_(m) { m_.lock(); }
    ~MutexLockGuard() { m_.unlock(); }
    MutexLockGuard(const MutexLockGuard&) = delete;
};

std::mutex g_mutex;
int g_counter = 0;

void safe_increment() {
    MutexLockGuard guard(g_mutex);   // 异常、return、break 都会解锁
    ++g_counter;
}
```

> 标准库已经给好了：`std::lock_guard`（C++11）、`std::unique_lock`（可解锁、可延迟）、`std::scoped_lock`（C++17，一次锁多把且自动避免次序死锁）。**自己写的守卫只在需要_custom 语义时才有必要。**

### 4. 「零开销」的真实含义

RAII 的代价是：每个对象有一个析构函数，离开作用域时插入一次调用。对一个空析构的类型，编译器通常直接消除。**真正的开销来自堆分配与不内联的析构**，而不是 RAII 本身。

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++98 | RAII 已经成型（智能指针、锁守卫都靠它），但没有统一的移动语义，所有权只能靠「不拷贝」约定 |
| C++11 | 移动构造/移动赋值、`noexcept`、删除/默认函数、`std::unique_ptr` 让「独占所有权」成为默认表达 |
| C++17 | 析构函数的 `noexcept` 推导、`std::scoped_lock`、`constexpr` 逐步进入容器，栈对象可为常量表达式 |
| C++20 | `constexpr` 允许动态分配与栈上对象的编译期构造；`std::jthread` 的 `stop_token` 也用 RAII 表达取消 |
| C++23/26 | `constexpr` 容器（P2273 路线）与「编译期堆」让 RAII 对象可以活到编译期；C++26 的生命周期分析工具会把「返回悬垂引用」变成可诊断错误 |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Koenig & Stroustrup, *RAII: Resource Acquisition Is Initialization* | **OOPSLA 1994** | RAII 一词的原始出处，也是「析构即释放」的规范化表述 |
| Stroustrup, *The C++ Programming Language, 4th Edition* | **Addison-Wesley 2013** | 第 5、17 章对栈对象、所有权与 RAII 的系统说明 |
| Sutter, *Exceptional C++* / *More Exceptional C++* | **Addison-Wesley 2000/2001** | 异常安全与资源安全的一组经典习题 |
| ISO/IEC JTC1 SC22 WG21, *C++ Core Guidelines* | 持续更新（2015 起） | 「用 RAII 管理资源」「不返回未拥有指针」等规则的官方清单 |
| Meyers, *Effective C++*, 3rd ed. | **Addison-Wesley 2005** | 第 3 章「资源管理」是 RAII 的最佳短训 |

---

## 近年研究与工业界开源实践（2015–2026）

- **RAII 成了跨语言模板**：Rust 的所有权与 Drop trait、Zig 的 defer，都直接借鉴了 C++ 的 RAII 思路；反过来，C++ 生态也在吸收它们的「类型系统强制所有权」。
- **静态分析接手裸内存**：`clang-tidy` 的 `cppcoreguidelines-owning-memory`、`clang-analyzer-cplusplus-*` 把「裸 `new` 必须进智能指针」变成可落地的 CI 规则。
- ** lifetimes 走向编译期诊断**：C++ Core Guidelines 的 Lifetime profile 与 Compilers 的 borrow 分析，正在把「返回局部变量的引用」这类错误从 review 讨论变成编译错误。
- **`noexcept` 成为接口契约**：析构、`swap`、移动构造是否 `noexcept` 已被视为库 API 的一部分（移动构造不 `noexcept` 会导致 `std::vector` 退化到拷贝）。
- 🔧 **堆分配的合规化**：Google、Microsoft 等在关键路径上用自定义分配器 + `std::pmr`（C++17 的 polymorphic allocator）替代全局 `operator new`，让「资源从哪来」成为类型的一部分。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `microsoft/GSL` | **6.7k★** | `gsl::not_null`、`gsl::span`、`final_action` 等 RAII 与所有权辅助 |
| `facebook/folly` | **30.5k★** | `folly::ScopeGuard`、自定义分配器与 `SmallVector`，工业级资源管理范本 |
| `abseil/abseil-cpp` | **18.1k★** | `absl::MutexLock` 等守卫类，展示「 RAII + 异常安全」的取舍 |
| `google/benchmark` | **10.4k★** | 量化栈 vs 堆、移动 vs 拷贝的真实差距 |
| `cpp-best-practices/cppbestpractices` | **8.8k★** | 可直接抄进团队的 RAII 与所有权检查清单 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「RAII 就是智能指针」 | RAII 是**模式**，智能指针只是标准库给好的一个实现；锁、文件、Socket、临时状态回滚都适用 |
| 2 | 「析构函数里可以抛异常」 | 析构抛异常会 `std::terminate`；保持 `noexcept`，需要报告错误就在销毁**之前**处理 |
| 3 | 「类里有裸指针成员就一定要写析构函数」 | 只写析构不禁用拷贝是经典陷阱（浅拷贝导致双重释放）；应一并处理拷贝/移动的五种函数 |
| 4 | 「栈上对象比堆上快，所以什么都往栈上放」 | 栈对象的**生命周期**受作用域限制，返回大对象时用返回值（RVO）而不是在栈上造一个大结构再拷走 |
| 5 | 「构造函数里调用 `init()` 再释放是标准做法」 | 两步式初始化在异常路径上必然泄漏；要么在构造函数里完成，要么提供工厂函数 |
| 6 | 🔧 本讲未强调 `noexcept` 的契约价值 | 2026 年的建议：移动构造与析构默认 `noexcept`，否则 `std::vector` 扩容会退化成拷贝 |
| 7 | 🔧 本讲未提「 ownership 类型化」 | `gsl::not_null`、C++23 的 `std::move_only_function`、以及 pmr 分配器把「谁拥有、从哪分配」写进类型系统 |
| 8 | 🔧 本讲的 RAII 局限在运行时 | C++23 起 `constexpr` 动态分配（`std::vector` 进常量表达式，P2273）让 RAII 对象也能活在编译期 |

---

## 与其他章 / 其他书的联系

- **`02-自己动手实现智能指针.md`**：本讲「把资源装进对象」的正式版本，手写 `unique_ptr`/`shared_ptr` 一口气讲透。
- **`03-右值与移动及返回对象.md`**：为什么「返回对象」不再等于「性能灾难」。
- **`05-异常与错误处理的现代化.md`**：异常路径下的资源安全，以及 `expected` 作为「可预期失败」的替代。
- **`08-模板编译期多态与编译期计算.md`**：`constexpr` 让 RAII 对象进入编译期。
- **`book/C++并发编程实战2/02-线程管控.md`**：线程对象本身也是 RAII，`detach` 与 `join` 的选择就是所有权选择。
- **`book/C++并发编程实战2/03-线程间共享数据.md`**：锁守卫是本章第 3 节的工业版。
- **`book/多处理器编程的艺术2/19-乐观与手工内存管理.md`**：当 RAII 的所有者管理成本过高时，手工内存管理（hazard pointer、RCU）的取舍。
- **`book/软件架构设计/03-语言.md`**：语言层面的「零成本抽象」与架构层面的资源治理如何对齐。
