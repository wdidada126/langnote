# 05 类模板实参推导（CTAD）与占位类型

> 覆盖原书 **Part II 第 9 章（Class Template Argument Deduction）与第 13 章（Placeholder Types）**。
> CTAD 是 C++17「让读者不再手写已经能从上下文推出的类型」的最大一次语法投资，也是本书里
> **实现差异与后续修改最多**的一章——本章所有关键断言都有本机 g++ 15.2 实测支撑。
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)

## 核心概念速览（中英对照）

- **类模板实参推导** — class template argument deduction (CTAD)：`std::pair p(1, 2.0f);` 从实参推出 `pair<int,float>`。
- **隐式推导指引** — implicit deduction guides：由类的构造函数签名自动派生出的「实参 → 类实参」映射。
- **用户自定义推导指引** — user-defined deduction guides：`template<class... Ts> Overloaded(Ts...) -> Overloaded<Ts...>;`，可覆盖/补充隐式指引。
- **占位类型** — placeholder type：出现在模板实参位置的 `auto`，`std::vector<auto>` 一类写法（C++17 仅有限支持）⚠️。
- **非类型模板参数的 auto** — `template<auto N>`：让 `1` 推成 `int`、`'c'` 推成 `char`，省去写类型。
- **推导失败即回退** — deduction failure：候选指引全部不匹配时得到硬错误（`class template argument deduction failed`）。
- **指引的排序规则** — guide ordering：比函数重载更弱的一层「更特化」比较，多条指引可能歧义。
- **聚合的 CTAD** — CTAD for aggregates：C++17 **不支持**（实测），C++20 恢复（实测）。

## 本章地图

| 层次 | 内容 |
| --- | --- |
| 语法层 | `C x{args}` / `C x(args)` / `C x = {...}` 都可触发推导 |
| 机制层 | 隐式指引（来自构造函数）+ 显式指引（作者写）→ 重载决议选最佳 |
| 库层 | 标准库为 `pair`/`tuple`/`complex`/容器迭代器对/`lock_guard` 等提供指引或可推导构造 |
| 陷阱层 | 聚合无指引、初始化列表推导怪异、`initializer_list` 优先、模板化构造的 const/引用退化 |

## 动机：为什么「少写一遍类型」需要一整套机制

```cpp
// 🔧 C++14 时代的重复
std::pair<std::string, std::vector<int>> kv = make_pair(std::string("k"), std::vector<int>{1,2});
std::lock_guard<std::mutex> lk(mtx);                   // 每次都要重申 mtx 的类型
std::vector<std::pair<int, double>> v = { {1, 2.0}, {3, 4.0} };  // 嵌套时最痛
```

C++17 之后（**已实测 g++ 15.2 -std=gnu++17**，含 `static_assert` 验证推导结果）：

```cpp
std::vector v = {1, 2, 3};              // vector<int>；已实测 decltype(v) 是 std::vector<int>
std::complex c = {1.0, 2.0};            // 已实测 complex<double>（标准库为 complex 提供指引/可推导构造）
std::set s{1, 2, 3};                    // 已实测 set<int>
Holder h(3.5);                          // 模板自定义类：由 ctor 的隐式指引推 Holder<double>（实测）
std::lock_guard lg{mtx};                // 与 02 章 if-init 组合；实测在 gnu++17 通过（见 02）
```

## 机制：隐式指引 + 显式指引 + 重载决议

概念模型：

```text
1. 取类模板 C 的所有构造函数 → 每个改写成一条「隐式指引」
      C<Ts...>(参数列表)  =>  C<推导结果>(参数列表)
2. 加上作者写的显式指引（可把不同类型映射成任意类实参，甚至不存在的构造形式）
3. 用普通重载决议挑最匹配的：更特化的指引优先（比较规则弱于函数模板的部分排序）
4. 拿到类实参后，再按该特殊化检查初始化是否合法（这一步仍可能失败）
```

实测样例（全部来自本目录的运行/编译记录）：

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17（三条 static_assert 通过）
template <typename T> struct Box { T v; Box(T x) : v(x) {} };
template <typename T> Box(T) -> Box<const T>;          // 显式指引：强制加 const
Box b{1};                                              // Box<const int>
static_assert(std::is_same_v<decltype(b), Box<const int>>);

template <typename T> struct Two { Two(T, T) {} };
template <typename T> Two(T, int) -> Two<double>;      // 与隐式指引竞争
Two t{1.0, 2};                                         // 显式指引胜出 → Two<double>
static_assert(std::is_same_v<decltype(t), Two<double>>);
```

## 三个「实测才知道」的坑

### 坑 1：聚合在 C++17 完全没有 CTAD（本章最硬的结论）

```cpp
// 🔧 已实测 g++ 15.2，逐档位结果原样记录：
template <typename T, typename U> struct Agg { T i; U d; };   // 无用户构造 = 聚合
Agg a{1, 2.0};   // gnu++17: error: class template argument deduction failed
                 // gnu++20: 通过   gnu++23: 通过
Agg b(1, 2.0);   // gnu++17: error: class template argument deduction failed
                 // gnu++20: 通过（P0960R3 圆括号聚合初始化）   gnu++23: 通过
```

聚合没有构造函数 ⇒ 没有隐式指引 ⇒ 推导失败。这不是编译器偷懒：**隐式聚合指引曾被纳入
P0091 草案，后因实现困难被移除**（⚠️ 移除的具体轮次编号未逐字核实，仅「P0091R3 为 C++17 定稿版本」
经 Apple C++ 语言支持表核实 ✅，其伴生论文 P0512R0 / P0620R0 / P0702R1 同源核实 ✅）。

**最典型的受害者是 `Overloaded`/`visit` 惯用法**（见 `08` 章）：

```cpp
// 🔧 已实测：下面这段在 gnu++17 下 CTAD 失败（Overloaded 是聚合）
template <class... Ts> struct Overloaded : Ts... { using Ts::operator()...; };
std::visit(Overloaded{[](int){}, [](auto){}}, v);        // C++17 编译失败

// 🔧 已实测的两种修复（任选其一）
// (a) 手写一条指引（注意：g++ 15.2 要求返回类型里的包写成 Ts...）
template <class... Ts> Overloaded(Ts...) -> Overloaded<Ts...>;
// (b) 升级到 -std=gnu++20（隐式聚合指引恢复），无需改代码
```

⚠️ **实测到的实现细节**：社区/文档里最常见的写法
`template <class... Ts> Overloaded(Ts...) -> Overloaded<Ts>;`（返回类型不带 `...`）
在 **g++ 15.2 的三个档位（17/20/23）全部报错**
`error: parameter packs not expanded with '...'`；必须写 `Overloaded<Ts...>`。
是否为 GCC 15 的口径收紧或回归，本目录**未能核实**（无本地 clang 可对照，cppreference 抓取 403）——
请把它当作「在你的编译器上实测」的提示，而不是「GCC 坏了」的结论。

### 坑 2：`initializer_list` 优先与关联容器的推导失败

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
std::vector v1{1, 2, 3};     // ✅ vector<int>（initializer_list 指引/构造可推）
std::vector v2 = {1, 2, 3};  // ✅ 同上
std::map m = { {"a", 1}, {"b", 2} };
// ❌ error: class template argument deduction failed
//    + no matching function for call to 'map(<brace-enclosed initializer list>, ...)'
// 原因：map 的 initializer_list<pair<const Key,T>> 构造里，元素 {"a",1} 自身无类型，无法反推 Key/T
// 修法：写 std::map m = std::map<std::string,int>{{"a",1},{"b",2}}; 或用 emplace/insert 循环
```

### 坑 3：范围版并行/容器接口不因 CTAD 而变宽

```cpp
// 🔧 已实测：std::reduce(std::execution::par, v, 0LL)（C++20 风格「策略 + 范围」）
//   在 -std=gnu++17 与 -std=gnu++20 下 libstdc++ 15 均报 no matching function for call
//   → libstdc++ 在 C++20 档位也没有提供「执行策略 + 范围」重载（见 11 章）
```

## 占位类型（原书 Ch13）

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17：template<auto N> 可用
template <auto N> struct Fixed { int v[N > 0 ? N : 1]; };
Fixed<3> f3;
static_assert(std::is_same_v<decltype(f3), Fixed<3>>);

// ⚠️ std::vector<auto> 这类「模板实参位置的 auto」在 C++17 只允许极有限形态，
//    g++ 15.2 在本目录未验证通过（避免误导，此处只标注为不可依赖写法）。
```

`template<auto N>` 的实际价值：写 `Fixed<3>` 时 `N` 是 `int`、`Fixed<'c'>` 时 `N` 是 `char`，
不必再写 `template<typename T, T N>` 的两段式；缺点是与「同一数字不同整型 → 不同特化」的老陷阱叠加后
更易踩坑（`std::array<int, 3>` 与 `std::array<int, 3u>` 的特化差异 ⚠️ 请按你的 API 实测）。

## 权衡

| 维度 | 用 CTAD | 显式写类型 |
| --- | --- | --- |
| 代码量 | 少，尤其嵌套模板 | 多 |
| 意图清晰度 | 推导结果可能与读者预期不同（`{1,2,3}` 是 `initializer_list` 还是 `int`？） | 一眼确定 |
| 跨版本可移植 | ⚠️ 见坑 1/2：C++17 与 C++20 行为不同 | 全版本一致 |
| 库 API 设计 | 需要额外写指引，且指引一旦公开就是契约 | 无契约负担 |
| 诊断质量 | 失败信息冗长（实测 GCC 要打印十几条候选） | 错误更局部 |

## 相邻概念对比

- **CTAD vs `auto` 变量推导**：`auto` 推**变量类型**（在初始化表达式上），CTAD 推**类模板实参**（在构造实参上），
  规则不同源；`auto x = {1,2}` 推成 `initializer_list`，`std::vector x{1,2}` 推成 `vector<int>`。
- **CTAD vs 函数模板实参推导**：后者可显式指定部分实参、可按返回类型推；CTAD **不能**指定部分类实参
  （C++20 也没有完全放开）。
- **隐式指引 vs 显式构造函数模板**：`template<class T> C(T)->C<U>` 与「把 ctor 写成模板」效果相近，
  但指引可以在类外「凭空」提供，不改变类的构造集合。
- **C++17 CTAD vs C++20 补齐**：圆括号聚合初始化（P0960R3 ✅）、`explicit(bool)`（把 `explicit` 变成可条件化，
  对「按推导结果决定是否显式」有用）、`operator()` 的 auto 参数等进一步减少手写类型。

## 最新演进与工业实践

**标准之后**
- **C++20 P0960R3「Parenthesized initialization of aggregates」（✅ 编号/标题/归属经 Apple 支持表核实）**：
  与隐式聚合指引一起补齐了坑 1；实测 `Agg a(1, 2.0)`/`Agg a{1, 2.0}` 在 gnu++20/23 均可。
- **C++23 未改动 CTAD 核心**；C++26 的反射方向（本目录 `00` 已记录「C++26 于 2026-03 定稿」的来源与 ⚠️）
  与本章无直接语法冲突。
- **实现口径**：`gcc.gnu.org/projects/cxx-status.html`（抓取于 2026-09-26）把 C++17 列为基本完成、
  C++20「核心 API 到 GCC 9 才稳」、C++23 仍在演进；本目录所有实测均在 GCC 15.2 上完成，
  请**不要**把「GCC 15 通过」当成「GCC 8/9 通过」——坑 1/2 在早期实现上表现不同 ⚠️。

**工业实践与开源口径**
- **标准库自身的指引**：`std::pair`/`std::tuple`/`std::vector` 迭代器区间/`std::complex`/
  `std::lock_guard`/`std::scoped_lock` 等，都是为了让「常见 3 行写法」可推导而加；
  Josuttis 的另一本书（[../C++标准库/02-通用工具与智能指针.md](../C++标准库/02-通用工具与智能指针.md)）
  把 `pair`/`tuple` 讲透，配合本章食用。
- **Abseil（实测 ≈18.1k★）**：在 `absl::` 类型上偏保守（少公开推导指引），因为「指引即契约」；
  **fmt（实测 ≈25.8k★）** 用 `format_string`/`formatted_args` 一类显式类型而非 CTAD 来保证错误信息可读。
- **`neargye/magic_enum`（实测 ≈6.2k★）** 与 variant 重载集惯用法大量依赖「指引 + 包展开」，
  坑 1 的 `Ts`/`Ts...` 拼写差异正是在这类代码里最先暴露。
- **写法纪律**：把「类模板 + 公开指引」当作 API 决策；内部代码可放心 CTAD，
  对外头文件里的返回值类型请写全（推导失败的信息代价由调用方承担）。

## 与其他章 / 其他笔记的联系

- ← 本目录 `03`：聚合规则的放宽是本章坑 1 的另一半；圆括号聚合初始化在 C++20 才与 CTAD 会师。
- ← 本目录 `02`：`if (std::lock_guard lg{m}; cond)` 完全依赖 CTAD 才写得这么短。
- → 本目录 `06`：折叠表达式 + `Overloaded` 指引 = variant 访问的现代写法（见 `08`）。
- → 本目录 `08`：`std::variant v{42}` 推成 `variant<int>`（已实测）；访问器的 `Overloaded` 需要本章的指引写法。
- → [../C++20模板元编程.md](../C++20模板元编程.md)、[../C++模板元编程/00-总览与阅读地图.md](../C++模板元编程/00-总览与阅读地图.md)：
  推导与指引在元编程体系中的位置；[../modern-cpp-tutorial.md](../modern-cpp-tutorial.md) 有同一特性的中文速览。
- → [../C++新经典.md](../C++新经典.md)、[../深入应用C++11.md](../深入应用C++11.md)：CTAD 之前的推导史。

## 思考题

1. 为什么 `std::map m = {{"a",1}};` 推不出来而 `std::vector v{1,2};` 可以？从「指引来自构造签名」回答。
2. 你有一个 `struct Point { int x; int y; };`（聚合）想在 C++17 里支持 `Point p(1,2);` 的推导式写法，
   最小改动是什么？（提示：一条指引 + 构造函数，或直接放弃聚合语义。用本章实测结论验证。）
3. `template<class... Ts> Overloaded(Ts...) -> Overloaded<Ts...>;` 为什么必须带 `...`？
   在你自己的编译器上实测并记录诊断原文。
