# 讲 28 + 29 + 30｜Concepts、Ranges 与协程（附结束语）

> **一句话**：Concepts 让「模板要求什么」写成人话，Ranges 让「数据怎么流」写成人话，协程让「异步怎么写」写成人话——这三件事在 2026 年都已经部分落地，但各自的坑也都还在。

---

## 本章地图

| 节 | 来源 | 内容 | 结论 |
| --- | --- | --- | --- |
| Concepts 的基本形态 | 28 | 概念定义、`auto` 约束、`requires` 子句 | 约束写在名字旁边，错误信息终于可读 |
| 概念组合与标准概念库 | 28 | `std::integral`、`std::ranges::range` 等 | 优先复用标准概念，别自己造 |
| Concepts vs SFINAE | 28 | 重载决议的差异 | 概念更清晰地表达「候选为何不可用」 |
| Ranges 的心智模型 | 29 | 区间、视图、惰性、管道 | 视图不拷贝元素，只有 `pages::` 这类消费才落地 |
| 视图与算法 | 29 | `views::filter/transform/take`、`ranges::sort` | 组合表达流程，编译期生成流水线 |
| 惰性带来的代价 | 29 | 编译时间、调试难度、抽象开销 | 不是所有地方都值得管道化 |
| 协程的三件套 | 30 | `co_await`/`co_yield`/`co_return`、`promise_type` | 协程是「可暂停的函数」，不是线程 |
| 生命周期与调度 | 30 | 跨 `co_await` 的引用、executors 缺位 | 协程的坑集中在生命周期与调度两处 |
| `std::generator` 与 C++26 | 30 | 标准协程工具、反射方向 | 2026 年：能用标准 parts 就用，别急着自造 task |
| 结束语 | — | 继续学什么、怎么读标准 | 跟进 WG21 与提案，比追新特性更值钱 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. Concepts：把「要求」写进签名

```cpp
// 教学示意：概念的定义与使用（不参与构建）
template <typename T>
concept HasArea = requires(const T& t) { t.area(); };          // 结构化要求

template <HasArea T>
double total_area(const std::vector<T>& shapes) {              // 约束写在模板参数上
    double s = 0;
    for (const auto& x : shapes) s += x.area();
    return s;
}

template <typename T> requires std::integral<T>                // 也可以用 requires 子句
T twice(T v) { return v * 2; }

static_assert(HasArea<Circle>);
static_assert(!HasArea<int>);
```

三种写法（概念名后置、`auto` 约束、`requires` 子句），选哪个？**按可读性**：能用概念名就写概念名，需要额外条件时用 `requires` 子句。

```cpp
// 教学示意：概念让错误回到「人话」（不参与构建）
template <std::ranges::range R>
void dump(R&& r) { for (auto& x : r) log(x); }
// 传错类型时，报错是「constraint not satisfied: range」，而不是几百行模板展开
```

| 对比 | SFINAE（C++17 及以前） | Concepts（C++20 起） |
| --- | --- | --- |
| 表达位置 | 返回类型 / 默认模板参数的 `enable_if` | 模板参数或 `requires` 子句 |
| 失败时的信息 | 「无匹配函数」 | 「哪个约束未满足、差哪个操作」 |
| 重载决议 | 靠 `enable_if` 让候选「不可用」 | 语义明确，可作为重载排序依据 |
| 组合性 | 难（嵌套 `enable_if`） | 好（`&&`、`||`、概念复合） |

### 2. Ranges：从「迭代器对」到「管道」

```cpp
// 教学示意：Ranges 的两种写法（不参与构建）
std::vector<Employee> staff{ /* ... */ };

// 传统：算法作用在迭代器对上，中间集合靠自己建
std::vector<int> ids;
for (const auto& e : staff) if (e.age >= 18) ids.push_back(e.id);
std::sort(ids.begin(), ids.end());

// Ranges（C++20）：视图是惰性的，filter 不分配中间容器
auto result = staff | std::views::filter([](const Employee& e) { return e.age >= 18; })
                    | std::views::transform([](const Employee& e) { return e.id; });
```

| 组件 | 作用 | 是否持有数据 |
| --- | --- | --- |
| `std::ranges::range` | 能遍历的东西（容器、数组、视图） | 由被引用的对象持有 |
| `view`/`views::xxx` | 惰性变换，不拥有元素 | 否（视图要绑到右值时要小心） |
| `ranges::` 算法 | 在 ranges 上工作，通常接受投影 | — |
| `views::all` | 把容器包成视图 | 引用底层容器 |

三条实用提醒：

1. **视图不拥有元素**：`auto v = some_lvalue_vector | views::filter(...);` 引用原容器，原容器必须先活着；
2. **`ranges::sort` 会改原容器**，与 `views::` 管道不同——前者是「消费/原地」，后者是「投影」；
3. **管道不是免费的**：每段视图都是一层抽象，编译时间与调试难度都会上升；热路径上先测「展开后的手写循环」是否更快。

### 3. 协程：可暂停的函数

```cpp
// 教学示意：最小协程（不参与构建）
#include <generator>                                   // C++23 的 std::generator

std::generator<int> fib() {                            // 每次调用返回一个可迭代对象
    int a = 0, b = 1;
    co_yield a;
    co_yield b;
    for (;;) { auto next = a + b; co_yield next; a = b; b = next; }
}

for (int v : take_n(fib(), 10)) use(v);               // 惰性、按需计算
```

三个关键字与三件事：

| 关键字 | 含义 |
| --- | --- |
| `co_await` | 挂起当前协程，等待某个 awaitable |
| `co_yield` | 产出（挂起并返回一个值，等价于 `co_await suspend_always{ yield }`） |
| `co_return` | 结束协程并返回结果 |

协程的形态取决于它的 `promise_type`；标准库在 C++23 提供了 `std::generator`（惰性序列）与 `std::task` 风格的参考实现，但**没有提供调度器**。

```cpp
// 教学示意：协程的关键约束（不参与构建）
// 1) 生命周期：跨越 co_await 的引用 / 指针必须继续有效
// auto& r = co_await get_ref();   // 危险：get_ref 返回的引用可能已经失效
// 2) 必须「对称」：谁启动、谁恢复、谁销毁
// 3) 无栈协程：所有协程共用调用栈，递归的协程会爆栈吗？——不会递归调用，但 awaitables 的嵌套会
```

> 最典型的坑：**在 `co_await` 之间持有指向局部变量的指针/引用**。标准规定协程帧把局部变量提升到堆/静态存储，但 **`co_await` 之后的引用有效性**需要你自己保证。

### 4. executors 缺位：协程最大的现实问题

C++20 的协程没有调度器概念，`co_await` 之后「在哪个线程继续」由 awaiter 决定。现实中的三种做法：

| 做法 | 代表 |
| --- | --- |
| 自造 `task`/`sender` + 线程池 | `folly::coro`、各家自研框架 |
| 用 Asio 的 `co_composed`/`awaitable` 体系 | 与 Asio 的执行器深度绑定 |
| 等到标准库给出统一方案 | C++26 方向（`std::execution` / executors 仍在推进） |

### 5. 结束语：接下来读什么

- **标准本身**：先在 [eel.is/c++draft](https://eel.is/c++draft)（在线草案）上按条款读，比任何中文教程都精确；
- **WG21 提案列表**：提案=P 编号，是语言演进的一手材料（本文刻意不写提案编号，请以 WG21 提案列表为准）；
- **真实论文**：本章引用的形式化工作（内存模型、范围类型）都来自顶会，值得按图索骥；
- **一条实践建议**：把「要不要用这个新特性」当作一次架构决策——**新代码用，存量代码不动**，除非它正处在重构窗口。

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++17 | 并行算法与执行策略（Ranges 的前身） |
| **C++20** | **Concepts** 与 **Ranges** 同批落地；协程进入标准；`std::jthread`、`std::format` |
| **C++23** | **`std::generator`**、更多视图（`views::split`/`join_with` 等）、`std::expected`、`std::print`、多维下标（P2128） |
| C++26 | 反射方向推进、`std::execution` 与 executors 继续整合、更多编译期设施 |
| 2026 现状 | Concepts 与 Ranges 已是 Daily Use；协程在服务端与游戏里落地，但调度器仍靠生态补齐 |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| **P0898R3** *The One Ranges Proposal* | **WG21 提案（C++20）** | Ranges 成文的集中体现 |
| **P0127R2** *Coroutines* | **WG21 提案（C++20）** | 协程进入标准的原始提案 |
| ISO/IEC TS 1929（Concepts for C++，即 Concepts TS） | **ISO 发布** | 概念语言设施的最初定型 |
| ISO/IEC 14882，`[concept.lang]`、`[range.prim]`、`[coroutine]` | C++ 标准 | 概念、Ranges 与协程的正式语义 |
| Richards et al., *Ranges and Universe: One Simple Evaluation Interface*（Doxygen 论文） | **2017 起的多篇** | Ranges 设计中的「domain/range 概念」讨论 |

---

## 近年研究与工业界开源实践（2015–2026）

- **Concepts 的第一个大受益者是 Ranges**：错误从「模板展开金字塔」变成一句话，是 C++ 用户体验史上最大的单次改善。
- **Ranges 的采用曲线**：视图管道在「数据整理脚本」与「流水线处理」里收益最大；在极端热路径上仍以手写循环为主。
- **协程的落地集中在两类产品**：高并发 IO 服务（替代回调地狱）与游戏逻辑（替代状态机）；两者的共同需求都是**可取消与可调度**。
- **`std::generator` 让「惰性序列」成为标准能力**，很多自造 `iterator` 的库开始改为生成器。
- 🔧 **协程 + executors**：C++26 仍在推进 `std::execution`；在此之前，工业项目要么用 Asio 体系，要么自己实现 `task<T>` + 线程池。
- 🔧 **反射与编译期元编程**：C++26 方向的反射一旦成熟，会同时改写 Concepts（约束可自动派生）、Ranges 与序列化三块代码，值得保持关注。
- 🔧 **调试工具在追赶**：协程栈与 Ranges 管道的调试体验仍是短板；`andreasfertig/cppinsights` 一类工具正在补位。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `lewissbaker/cppcoro` | **3.9k★** | C++20 协程的经典参考实现（`task`、`generator`、`sync_wait`） |
| `facebook/folly` | **30.5k★** | `folly::coro` 与 `SyncWait`、`Executor` 结合的工业范例 |
| `uxlfoundation/oneTBB` | **6.8k★** | 并行算法与任务调度，Ranges 与执行策略的落地参考 |
| `fmtlib/fmt` | **25.8k★** | 编译期格式检查，与 Concepts 同代的经验 |
| `andreasfertig/cppinsights` | **4.5k★** | 看协程与模板展开后的真实形态 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Concepts 只是更好的 `enable_if`」 | 它是**重载决议的一等公民**，可用于排序与重载，而不只是「让候选消失」 |
| 2 | 「视图管道一定更快」 | 视图是惰性的，中间不分配，但每层抽象都有成本；先测再决定 |
| 3 | 「`views::filter` 返回新容器」 | 视图不拥有数据，返回的是「对原序列的投影」 |
| 4 | 「协程就是绿色线程/用户态线程」 | 协程不自己调度；「在哪个线程恢复」由 awaiter 决定，这是最大的认知差 |
| 5 | 「协程能减少线程切换，所以更快」 | 减少的是**回调栈抖动**，不是线程切换；真正的收益是可读性与组合性 |
| 6 | 🔧 本讲把 C++20 三件套当作「未来looking」 | 2026 年它们已是日常工具：新代码默认用 Concepts 约束模板、Ranges 表达数据管道、协程表达异步；但**存量代码不必强行迁移** |
| 7 | 🔧 未讲 `std::generator` 与自造 `task` 的取舍 | C++23 起 `std::generator` 可用；除非你需要取消、单所有者语义或异步等待，否则优先标准设施 |
| 8 | 🔧 缺少反射与 C++26 的前瞻 | 反射会显著削减「手写特化/手写序列化/手写约束」的面积，建议纳入下阶段技术规划 |
| 9 | 🔧 协程的生命周期陷阱讲得还不够狠 | 必须强调：**跨 `co_await` 的引用不可依赖跨暂停仍有效**；这是协程崩溃的第一来源 |

---

## 与其他章 / 其他书的联系

- **`08-模板编译期多态与编译期计算.md`**：Concepts 是 `08` 章 SFINAE 的正式替代方案。
- **`10-可变模板tuple与类型擦除.md`**：`tuple`/`variant` 与 Ranges 的组合式抽象。
- **`09-函数对象lambda与函数式编程.md`**：视图管道就是函数式组合子在标准库里的样子。
- **`04-容器汇编上下.md`**：Ranges 是容器的下一层抽象。
- **`12-工具漫谈与构建依赖.md`**：C++20 三件套的编译器版本要求与工具链支持。
- **`11-thread与future及内存模型.md`**：协程与 `future` 在异步模型上的分工。
- **`15-REST-SDK与网络应用.md`**：协程将改变异步 HTTP 代码的写法。
- **`book/C++并发编程实战2/10-并行算法函数.md`**：执行策略与 Ranges 的接缝。
- **`book/C++20设计模式.md`**：C++20 特性在设计模式层面的重构案例。
