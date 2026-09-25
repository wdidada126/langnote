# 讲 16 + 17｜函数对象与 lambda：进入函数式编程

> **一句话**：lambda 不是「语法糖」这么简单——它同时是一个**匿名类型、一个闭包、一个可移动的值**；理解了它携带了什么（捕获列表），才谈得上用函数式的方式组织代码。

---

## 本章地图

| 节 | 来源 | 内容 | 结论 |
| --- | --- | --- | --- |
| 函数对象 | 16 | `operator()`、`mutable`、无状态 vs 有状态 | 无状态函数对象可被优化为直接调用 |
| lambda 语法 | 16 | 捕获列表、参数、返回类型推导 | 尽量「无捕获」，可隐式转函数指针 |
| 捕获的三种语义 | 16 | 值 / 引用 / 隐式 / `this` | 按引用捕获的生命周期是最大的坑 |
| 泛型 lambda 与初始化捕获 | 16 | `auto` 参数、`init-capture` | C++14 起 lambda 自己就是模板 |
| `std::function` 的代价 | 16 | 类型擦除、堆分配、间接调用 | 性能热路径不要默认用 `std::function` |
| 函数式三件套 | 17 | `map` / `filter` / `fold` | 用组合表达流程，而不是用状态机 |
| 不可变与纯函数 | 17 | 无副作用、可缓存、易并行 | 切分状态边界比切函数更值钱 |
| 🔧 现代补充 | 16/17 + 2026 | `static operator()`（P1169）、`std::move_only_function`（C++23）、Ranges 管道 | 函数式风格在 2026 年已完全进入标准库 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 函数对象：带状态的可调用物

```cpp
// 教学示意：函数对象（不参与构建）
struct Counter {
    int n = 0;
    int operator()() { return ++n; }        // 有状态：每次调用结果不同
};
Counter c;
c(); c();                                   // 返回 1, 2

struct Add {
    int operator()(int a, int b) const { return a + b; }   // 无状态：可转成函数指针
};
int (*fp)(int, int) = Add{};                                // 无捕获 lambda 同理
```

规则：**无捕获 lambda 与无状态函数对象可以退化为函数指针**；一旦带状态，就必须走对象。

### 2. lambda 的完整语法与捕获语义

```cpp
// 教学示意：lambda 的写法（不参与构建）
std::vector<int> v{5, 2, 9};

auto by_value  = [v](int x) { return x + v[0]; };     // 拷贝整个 vector
auto by_ref    = [&v](int x) { return x + v[0]; };    // 引用：v 必须活得比闭包久
auto implicit  = [=](int x) { return x + v.size(); }; // 隐式值捕获
auto only_one  = [&v](int x) { return x + v.size(); };
auto mutating  = [n = 0]() mutable { return ++n; };    // C++14 init-capture + mutable

int total = std::count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });   // 捕获列表为空
```

捕获方式的判据：

| 捕获方式 | 语义 | 风险 |
| --- | --- | --- |
| `[]` | 不捕获 | 最安全，可转函数指针 |
| `[&]` | 引用捕获外部变量 | 闭包可能活得比被引用对象更久 → 悬垂 |
| `[=]` | 值捕获（拷贝） | 大对象拷贝有开销；但 snapshot 语义清晰 |
| `[x, &y]` | 混合 | 精确控制，推荐 |
| `[this]` / `[*this]`（C++20） | 捕获当前对象的指针 / 拷贝整个对象 | 跨线程回调里 `[this]` 是经典的生命周期 bug |

> **跨线程的一条硬规则**：把 lambda 交给线程或异步任务时，捕获列表里**不要放 `this`，也不要放引用**；放值或 `weak_ptr`。

### 3. `std::function` 到底贵在哪

```cpp
// 教学示意：类型擦除的代价（不参与构建）
std::function<int(int, int)> f = [](int a, int b) { return a + b; };
// 建一个匿名类型 → 塞进 std::function 的内部缓冲 / 若大于小对象阈值则堆分配
// 调用时：一次虚式调度 + 可能的一次间接跳转，通常无法内联
```

| 场景 | 建议 |
| --- | --- |
| 回调注册表、策略参数、异步任务 | `std::function`（必要时用 `folly::Function` 等可移动版本） |
| 内层循环、热点比较器 | 模板参数或 lambda 直接内联 |
| 需要「只可移动」的回调 | C++23 的 `std::move_only_function` |

### 4. 函数式的三件套：map / filter / fold

```cpp
// 教学示意：把流程写成组合（不参与构建）
std::vector<int> scores{90, 72, 85, 60};

auto passed = [&scores] {                       // filter
    std::vector<int> out;
    for (int s : scores) if (s >= 60) out.push_back(s);
    return out;
};
int sum = 0;                                     // fold（without ranges）
for (int s : passed()) sum += s;

// C++20 Ranges 的等价写法（惰性、不分配中间容器）
// auto result = scores | std::views::filter([](int s) { return s >= 60; })
//                | std::views::transform([](int s) { return s * 2; });
```

函数式风格的四条实用纪律：

1. **优先返回新集合而不是原地修改**；只在明确需要时写原地版本；
2. **纯函数可缓存、可并行**：把「只读」的部分做成无副作用的纯函数；
3. **状态越小越好**：把循环里的可变计数器抽成「一次 fold」；
4. **不要为了函数式而牺牲可读**：命令式与函数式混杂的写法在 C++ 里完全正当。

### 5. 用 lambda 表达策略与责任链

```cpp
// 教学示意：把分支表写成函数对象（不参与构建）
std::unordered_map<std::string, std::function<void()>> handlers;
handlers["reload"] = [this] { reload_config(); };     // 注意捕获 this 的生命周期
handlers["quit"]   = [app] { app->quit(); };          // 捕获智能指针更安全
```

### 6. 递归与编译期递归的差别

```cpp
// 教学示意：运行期递归 vs 编译期递归（不参与构建）
int fib_run(int n) { return n < 2 ? n : fib_run(n - 1) + fib_run(n - 2); }   // 运行期，栈深度 = n

constexpr int fib_cx(int n) {                                                // 编译期
    return n < 2 ? n : fib_cx(n - 1) + fib_cx(n - 2);                       // 模板递归有展开上限
}
static_assert(fib_cx(10) == 55);
```

> 编译期递归受「模板实例化深度」限制，写元程序时要靠折半/分治而不是线性递归；这也是为什么折叠表达式那么受欢迎。

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++98 | 只有函数对象（functor） |
| C++11 | lambda、可变 lambda 变量的 `auto` 类型、`std::function`、`std::ref`/`std::cref` |
| C++14 | **泛型 lambda**（`auto` 参数）、**初始化捕获**（`[x = f()]`）、返回类型推导 |
| C++17 | `static_assert` 里用 lambda、`std::invoke` 统一调用语法、`if constexpr` |
| C++20 | **模板 lambda**（`[]<typename T>(T t)`）、`[*this]` 捕获、捕获重载函数名与成员函数、三向比较 |
| C++23 | **`static operator()`（P1169）**、**`std::move_only_function`**、多维下标 |
| C++26 | 反射与更完整的编译期组合；Ranges 与执行策略进一步整合 |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Vandevoorde & Josuttis, *C++ Templates: The Complete Guide*, 2nd ed. | **Addison-Wesley 2017** | 第 3、6 章：函数对象与 lambda 的类型系统 |
| Josuttis, *The C++ Standard Library, 2nd ed.* | **Addison-Wesley 2012** | `<functional>` 与 `std::invoke` 的完整说明 |
| ISO/IEC 14882 第 7.5 节与 `<functional>` | C++ 标准 | lambda 表达式的正式语义与捕获规则 |
| Bird & Wadler, *Introduction to Functional Programming* | **Prentice Hall 1988** | `map`/`filter`/`fold` 三件套的原始出处（函数式传统的源头） |
| **P1169** *static operator()* 与 **P0288** 一系（可移动可调用包装） | **WG21 提案** | 本章「现代补充」的提案来源 |

---

## 近年研究与工业界开源实践（2015–2026）

- **`std::function` 的开销被反复量化**：多数实测表明「间接调用 + 可能的堆分配」在热路径上显著慢于模板/lambda 内联；回调注册表通常是设计需要，而不是性能需要。
- **`static operator()`（P1169）改变了无状态函数对象的表达**：同一个类型的多个无捕获 lambda 可以共享类型并被当作函数指针传递。
- **Ranges 把函数式管道变成标准写法**：`views::filter/transform/join` 让「不建中间容器」成为默认，惰性求值不再是函数式库的专利。
- **不可变数据的成本被重新评估**：C++ 里拷贝语义天然便宜（移动），因此「拷贝而非共享」在函数式风格里代价可控；但大对象的写时复制需要显式分配器支撑。
- 🔧 **`std::move_only_function`（C++23）**：只可移动的可调用包装补上了「异步任务里放只移动回调」的缺口，取代了大量自制的 `unique_ptr<Callable>`。
- 🔧 **RAII + lambda 成为新惯用法**：`folly::ScopeGuard` 一类「捕获资源的 lambda + 作用域」写法，正在取代手写守卫类。
- 🔧 **并行与函数式**：C++17 的执行策略与 C++23 的并行算法让「用函数式表达 + 库负责并行」成为可能，但仍需谨慎对待「纯函数 + 无共享」的前提。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `google/benchmark` | **10.4k★** | lambda vs `std::function` vs 函数指针的微基准首选 |
| `facebook/folly` | **30.5k★** | `folly::Function`（可移动、小对象优化）、`ScopeGuard` |
| `fmtlib/fmt` | **25.8k★** | 编译期格式字符串的 `constexpr` + 模板实践 |
| `uxlfoundation/oneTBB` | **6.8k★** | 并行算法与 lambda 的组合用法 |
| `microsoft/STL` | **11.2k★** | `std::function`/`std::invoke` 的实现细节 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「lambda 就是匿名函数」 | 它是一个**匿名局部类**，拷贝/移动语义由捕获列表决定；`auto` 拿到的类型各不相同 |
| 2 | 「`[&]` 捕获很方便，用着省心」 | 闭包若逃离作用域（存起来、跨线程）就是悬垂引用；跨线程一律用值捕获或 `weak_ptr` |
| 3 | 「`std::function` 就是类型擦除的通用回调」 | 热路径上它纳税（间接 + 可能堆分配）；能用模板就别用 |
| 4 | 「`mutable` lambda 是非 const 的」 | C++23 起无捕获 lambda 的 `operator()` 其实是 `const`；有捕获时 `mutable` 才有意义 |
| 5 | 「函数式就一定更快」 | 惰性管道与临时集合会带来分配；C++ 的优势在于两者可选 |
| 6 | 🔧 本讲未提 `static operator()`（P1169） | 无捕获 lambda 现在可以直接当函数指针用，模板代码更干净 |
| 7 | 🔧 本讲未提 `std::move_only_function`（C++23） | 只移动回调有了标准答案，特别适用于线程池任务与事件回调 |
| 8 | 🔧 缺少 Ranges 视角的管道示例 | 讲 29 / 本文件的「现代补充」已给出 `views::filter | views::transform` 的等价写法 |
| 9 | 🔧 未强调用 `std::invoke` 的可调用统一 | C++17 起 `std::invoke` 让「成员函数指针 + 对象」与函数对象走同一条调用路径，回调库应默认使用它 |

---

## 与其他章 / 其他书的联系

- **`06-迭代器与新for和易用性改进.md`**：lambda 最常见的宿主就是算法与范围 for。
- **`08-模板编译期多态与编译期计算.md`**：泛型 lambda 是「模板 + lambda」的合体，SFINAE 与 `requires` 同样适用于它。
- **`04-容器汇编上下.md`**：`map`/`set` 的比较器几乎都是函数对象。
- **`10-可变模板tuple与类型擦除.md`**：`std::function` 是类型擦除的第一课。
- **`12-工具漫谈与构建依赖.md`**：`std::function` 与模板实例化都会影响编译时间。
- **`book/C++并发编程实战2/09-高级线程管理.md`**：线程池任务就是「带捕获的 lambda」。
- **`book/C++并发编程实战2/10-并行算法函数.md`**：执行策略如何把 lambda 并行化。
- **`book/C++CoreGuidelines解析.md`**：`F.8`（lambda 捕获列表要短）、`F.20` 等条目。
