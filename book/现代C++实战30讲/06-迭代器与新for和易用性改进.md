# 讲 07 + 08 + 09｜迭代器与新 for、易用性改进（上/下）

> **一句话**：现代 C++ 的一半「语法糖」其实是在消灭模板里的类型噪音和样板流程——`auto` 让你不再手写类型，`nullptr` 让指针与整数彻底分开，静态断言把文档搬进编译器。

---

## 本章地图

| 节 | 来源 | 内容 | 结论 |
| --- | --- | --- | --- |
| 迭代器族 | 07 | 输入/前向/双向/随机访问、概念式要求 | 迭代器是有要求的「指针」；用错族的迭代器会静默变慢 |
| 范围 for | 07 | 语法糖展开、失效规则 | 不要在其中插入元素；要索引就用下标循环 |
| 迭代器失效 | 07 | `vector` 插入/删除、`unordered` 重哈希 | 保留 `iterator` 前先想清楚容器行为 |
| `auto` 与类型推导 | 08 | `auto`、`decltype`、`decltype(auto)` | 减少噪音但仍要看得懂推导结果 |
| 统一初始化与 `{}` | 08 | `std::initializer_list`、最令人烦恼的解析 | 用 `{}` 时必须小心函数式 conversion |
| `nullptr` 与 `NULL` | 08 | 指针 vs 整型 | 一律用 `nullptr` |
| 字面量 | 09 | 数字分隔符、自定义字面量、`u8`/`u`/`U`/`L` | 自定义字面量做单位换算，编译期完成 |
| 静态断言 | 09 | `static_assert`（C++11 起可用 `constexpr`） | 把运行期检查提前到编译期 |
| 成员函数说明符 | 09 | `constexpr` 成员函数、`const` 重载、`virtual` 默认 | 说明符是接口契约的一部分 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 迭代器族的代价曲线

```cpp
// 教学示意：不同迭代器族的算法代价（不参与构建）
std::vector<int> v{3, 1, 2};
std::list<int>   l{3, 1, 2};

// std::sort 需要随机访问迭代器；对 std::list 编译不过，应改用 std::list::sort
std::sort(v.begin(), v.end());

// std::find 只需要输入迭代器；对 list 也成立
auto it = std::find(l.begin(), l.end(), 1);

// std::list::sort 是成员函数：稳定且只遍历一次，优于「取到 vector 排序再塞回去」
l.sort();
```

| 族 | 能力 | 典型容器 |
| --- | --- | --- |
| 输入 | 只读、可单向、可能单次 | `istream_iterator` |
| 前向 | 可重复读写、单向 | `forward_list` |
| 双向 | `++`/`--` | `list`、`set/map` 迭代器 |
| 随机访问 | `it + n`、`it - it2`、`[]` | `vector`、`deque`、`string` |

> C++20 起这些要求有了名字（ concepts 层的 `std::random_access_iterator` 等），编译错误终于会告诉你「哪个操作不满足哪条要求」——这正是讲 28 Concepts 的动因。

### 2. 范围 for 展开后长什么样

```cpp
// 教学示意：范围 for 等价于什么（不参与构建）
for (auto& x : v) { body(x); }

// 大致等价于：
//   auto&& __range = v;                       // 绑定，注意 lifetime
//   for (auto __begin = v.begin(), __end = v.end(); __begin != __end; ++__begin) {
//       auto&& x = *__begin;                   // 绑定元素
//       body(x);                               // 变量声明处的 cv/ref 决定 x 的属性
//   }
```

四条经验：

1. 只想读：`for (const auto& x : v)`；
2. 要修改：`for (auto& x : v)`；
3. 拷贝小对象：`for (auto x : v)`；
4. **不要在循环体内插入/删除容器元素**——迭代器与结束位置都可能失效；需要遍历并删除时用 `erase(it)` 的返回值推进（`C++11` 起 `vector::erase` 返回新位置）。

```cpp
// 教学示意：边遍历边删除的正确写法（不参与构建）
for (auto it = v.begin(); it != v.end(); ) {
    it = v.erase(it);                      // erase 返回下一个有效位置
}
```

### 3. `auto` 的三档用法

```cpp
// 教学示意：auto 与 decltype（不参与构建）
auto x = 42;                       // int
auto y = {1, 2, 3};                // std::initializer_list<int> ← 常见意外
auto& r  = v.front();              // 保留引用
auto ptr = std::make_unique<int>(7);

template <typename T>
auto identity(T& t) -> decltype(t) { return t; }              // 尾置返回类型

template <typename T>
decltype(auto) forward_like(T&& t) { return std::forward<T>(t); }  // 精确保留值类别
```

- `auto` 会**剥掉引用与顶层 const**，写 `auto&`/`const auto&` 才能保留；
- `decltype(auto)`（C++14）用于转发函数，能精确保留引用；
- 当类型来自复杂表达式（迭代器、lambda、模板）时，`auto` 的价值最大；类型本身一目了然时，写全反而更清楚。

### 4. `{}` 与「最令人烦恼的解析」

```cpp
// 教学示意：初始化歧义（不参与构建）
std::vector<int> a{1, 2, 3};      // 初始化列表构造：三个元素
std::vector<int> b(3, 7);         // 圆括号：元素 7 重复三次
std::vector<int> c = {1, 2, 3};   // 与 a 等价

class Widget { public: Widget(int); };
Widget w1(1);                     // 正常构造
Widget w2{1};                     // 正常构造
// Widget w3();                   // 函数声明，而不是构造：最令人烦恼的解析
// Widget w4{};                   // 值初始化：默认构造
```

**规则**：容器/聚合用 `{}`，单个值用 `()`；需要「构造一个临时对象传给函数」的场合用命名变量或花括号避免函数式声明。

### 5. 自定义字面量与静态断言

```cpp
// 教学示意：编译期单位换算与静态断言（不参与构建）
constexpr long long operator"" _km(long long v) { return v * 1000; }
constexpr long long operator"" _m(long long v)  { return v; }

static_assert(sizeof(void*) >= 8, "需要 64 位平台");
static_assert(std::is_same_v<decltype(1_km), long long>, "字面量应返回 long long");

template <typename T>
struct RingBuffer {
    static_assert(std::is_pod_v<T>, "仅支持平凡类型，避免非平凡元素的移动开销");
    static_assert(std::atomic<T>::is_always_lock_free, "该类型在目标平台退化为带锁实现");
    // ...
};
```

> `static_assert` 支持消息是 C++17 起的能力；在此之前消息是可选的。C++26 起 `static_assert(false)` 的「总是失败」写法也比过去的技巧更规范。

### 6. 成员函数说明符的四个要点

| 说明符 | 作用 | 注意 |
| --- | --- | --- |
| `constexpr` 成员函数 | 可在编译期调用 | C++14 起允许多条语句；C++23 起虚函数也可 `constexpr` |
| `const` 重载 | 按可修改性选版本 | **`const` 版本隐藏了非 `const` 的可见性**：`const` 对象访问不到非 `const` 重载 |
| `virtual ... = default` | 显式默认实现 | 与 `= delete` 搭配表达「必须提供」 |
| `explicit` | 禁止隐式转换 | 单参数构造函数应默认 `explicit` |

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++98 | 无 `nullptr`；`static_assert` 只能通过 `typedef char[x]` 的技巧实现 |
| C++11 | `auto`（类型推导）、`nullptr`、`constexpr` 函数、范围 for、委托构造与继承构造、`=default/=delete` |
| C++14 | `decltype(auto)`、泛型 lambda、变量模板 |
| C++17 | `if constexpr`、折叠表达式、`inline` 变量、`static_assert` 支持消息、数字分隔符 `'` |
| C++20 | concepts 约束、Ranges、三向比较 `<=>`、`consteval`/`constinit`、`std::span` |
| C++23 | `static operator()`（P1169）、`std::print`、`if consteval`、多维下标（P2128） |
| C++26 | 反射、`constexpr` 放宽、更多编译期检查 |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| ISO/IEC 14882，第 24 章（Iterators） | C++ 标准 | 迭代器要求（LegacyForwardIterator 等）的正式条款 |
| Meyers, *Effective Modern C++* | **O'Reilly 2014** | 第 2 章：`auto` 的推导规则与类型简写 |
| Stroustrup, *The C++ Programming Language, 4th ed.* | **Addison-Wesley 2013** | 第 6 章：范围 for 与初始化列表的完整语义 |
| Sutter & Alexandrescu, *C++ Coding Standards* | **O'Reilly 2005** | 「不要重新发明 `auto`」「使用 `nullptr`」等条目 |
| P1169（静态化 `operator()`）与 P2128（多维下标） | **WG21 提案** | 2026 年本章代码最值得直接换用的现代写法 |

---

## 近年研究与工业界开源实践（2015–2026）

- **`auto` 已成为新代码的默认**：接口边界处仍写完整类型（方便阅读文档），实现处大量用 `auto`。
- **初始化歧义的教学价值被低估**：`std::vector<int> v(3)` 与 `v{3}` 的差别是新手最常见的 bug 之一；编译器警告与 clang-tidy 规则正在逐步覆盖。
- **字面量做单位安全**：`operator"" _km` 一类写法在嵌入式与游戏引擎里用于编译期单位换算，避免「差 1000 倍」事故。
- **静态断言进入 CI**：把 `is_always_lock_free`、平台位数、POD 要求写进 `static_assert`，是把架构约束变成「编译不过」的有效手段。
- 🔧 **`static operator()`（C++23，P1169）**：无捕获 lambda 现在可以隐式转成函数指针，且同一个类型的多个 lambda 不再互相冲突——无状态函数对象终于可以共享类型。
- 🔧 **`std::print`/`std::format`（P2093）** 与 `if consteval`：让「编译期能做的就编译期做」的分支写法统一，减少模板代码里的 `#ifdef` 式分支。
- 🔧 **`constexpr` 容器（P2273 路线）** 让本章那些「编译期跑通」的例子真正能在编译期跑通。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `microsoft/STL` | **11.2k★** | 范围 for 与迭代器适配的标准实现 |
| `facebook/folly` | **30.5k★** | 大量使用 `auto`、自定义字面量（`folly::literals`）与编译期检查 |
| `fmtlib/fmt` | **25.8k★** | 编译期格式字符串检查，把「格式化错误」提前到编译期 |
| `google/benchmark` | **10.4k★** | 用 `auto`/lambda 写基准，看编译器到底内联了什么 |
| `andreasfertig/cppinsights` | **4.5k★** | 把模板与范围 for 展开后的代码打给人看，理解糖衣下的真相 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「`auto x = {1,2,3};` 得到 `vector<int>`」 | 它得到 `std::initializer_list<int>`，生命周期止于该语句 |
| 2 | 「范围 for 里 `push_back` 也没关系」 | 扩容会使结束迭代器失效，导致未定义行为 |
| 3 | 「`const` 成员函数只能读」 | 它同时**限制了可调用的非 `const` 重载**，这是最容易踩的重载隐藏问题 |
| 4 | 「`auto` 让代码变难读」 | 类型来自复杂表达式时 `auto` 更好；公开签名仍应写全类型 |
| 5 | 「`NULL` 就是 `nullptr`」 | `NULL` 通常是 `0`，会与整型重载歧义 |
| 6 | 🔧 本讲把 `static_assert` 当作「文档」 | 2026 年的正确用法是**约束**：平台要求、平凡性、`is_always_lock_free` 都应当是编译期失败而不是运行时崩溃 |
| 7 | 🔧 未提 C++23 的 `static operator()`（P1169） | 无捕获 lambda 可直接作为函数指针传递、可放入同一类型容器；会显著改写「函数对象」类代码 |
| 8 | 🔧 未提 C++23 的 `if consteval` | 它取代了 `if (std::is_constant_evaluated())`，让同一个函数体同时服务编译期与运行期 |
| 9 | 🔧 缺少「多维下标」（P2128）的实用价值 | 自定义矩阵/张量类型现在可以写 `m[i][j]` 而不是 `m(i,j)`，代价很小 |

---

## 与其他章 / 其他书的联系

- **`04-容器汇编上下.md`**：容器的遍历接口与失效规则是本章迭代器讨论的对象。
- **`03-右值与移动及返回对象.md`**：`const auto&` 绑定临时对象是移动语义的常用写法。
- **`09-函数对象lambda与函数式编程.md`**：`auto` 与 lambda 的组合是函数式风格的入口。
- **`08-模板编译期多态与编译期计算.md`**：`static_assert` 与 `constexpr` 成员函数是编译期计算的守卫。
- **`16-未来篇Concepts-Ranges-协程.md`**：C++20 的 concepts 正是把本讲「迭代器要求」写成了名字（讲 28）。
- **`book/C++并发编程实战2/10-并行算法函数.md`**：执行策略与范围 for 的性能对照。
- **`book/C++CoreGuidelines解析.md`**：`ES.11`（不重新发明 `auto`）、`ES.41`（`nullptr` 优于 `0`/`NULL`）等条目。
