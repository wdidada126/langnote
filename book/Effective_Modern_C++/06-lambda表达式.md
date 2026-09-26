# 第 6 章 lambda 表达式（Lambda Expressions，Items 31–34）

> 对应原书第 6 章（Items 31–34）。单文件大纲 [../Effective_Modern_C++.md](../Effective_Modern_C++.md)；
> 导航 [00-总览与阅读地图.md](00-总览与阅读地图.md)｜索引 [../C++系列·总索引.md](../C++系列·总索引.md)。
> 本书把 lambda 当**对象**讲：闭包类型、捕获即成员、`operator()` 默认 const——
> 因此所有陷阱都是对象生命周期与 const 语义的陷阱，而不是「匿名函数」的语法题。

## 核心概念速览（中英对照）

- **闭包类型** — closure type：编译器为每个 lambda 合成的唯一类，捕获变量成为其数据成员。
- **隐式捕获（默认捕获）** — default capture：`[&]`/`[=]` 不列出被捕的名字；本书两大事故源（Item 31）。
- **this 捕获** — capturing `this`：`[=]` 时代 `this` 被悄悄按值捕获，对象析构后闭包仍持裸 this → 悬垂。
- **初始化捕获** — init capture（C++14 generalized lambda capture）：`[p = std::move(res)]`，把 move-only 对象移进闭包。
- **泛型 lambda** — generic lambda：形参写 `auto`，即「带推导的 operator() 模板」。
- **`std::bind`** — std::bind：占位符 `_1/_2` 的部分求值工具；lambda 在可读性/内联/完美转发三方面全面胜出。
- **std::function** — std::function：可拷贝的调用包装（类型擦除），代价是可能的堆分配 + 间接调用。
- **mutable 闭包** — mutable lambda：把 `operator()` 的 const 去掉，允许修改捕获副本（标志位惯用法的前身）。

## 本章地图

| Item | 核心论点 |
| --- | --- |
| 31 | 避免 `[=]`/`[&]`：悬垂 this、悬垂引用捕获、以及「看起来捕获了其实捕获的是 this 指针」 |
| 32 | 用初始化捕获把对象**移入**闭包；C++11 时代用 `std::shared_ptr`+bind 或自造包装做退化方案 |
| 33 | 泛型 lambda 里转发 `auto&&` 形参必须 `std::forward<decltype(x)>(x)`，`decltype` 在这里恢复类别 |
| 34 | 优先 lambda 而非 `std::bind`：参数转发透明、可内联、constexpr 友好、`_1` 噪声大 |

## 动机：为什么 lambda 的 bug 全是「对象 bug」

lambda 展开后是一个类：捕获列表 = 构造函数初始化列表，调用 = `cl(args)…` 的
`operator()`（默认 `const`）。于是两类 C++ 老问题原样迁移：**对象生命周期**（闭包被存进
`std::function`、注册回调、异步任务里活得比宿主久）与**按值/按引用的快照语义**。
Item 31–34 的所有建议，本质是把这两条老纪律套上新语法。

## 机制：从语法糖到对象模型

### 1. `[=]` 的真实身份：捕获 this 裸指针（Item 31）

成员函数里的 `[=]{ return x + y; }`（x、y 为成员）展开为 `return this->x + this->y;`——
捕获的不是成员值，而是**这一秒还活着的 this**。典型事故形态：把闭包丢进线程池/
`std::function` 注册表，宿主对象先析构，回调醒来读 freed memory。
`[&]` 同构问题：按引用捕获局部变量 + 异步执行 = 经典悬垂。
书的解药分层：① 显式列出捕获（`[x = x]` 的 C++14 自遮蔽写法把「拷快照」写脸上）；
② 需要成员值时 C++14 用 `[this]`（语义诚实：还是裸 this）+ 局部再快照；
③ C++20 的 `[=, *this]` 给出「真按值捕对象」的选项（见演进节）。

### 2. 初始化捕获：move-only 入闭包（Item 32）

```cpp
// 🔧 自写示意（核心三行在本目录实测 lambda 脚本中验证编译）
auto handle = std::make_unique<std::fstream>("data.bin", std::ios::in);
auto process = [h = std::move(handle)]() mutable {
    if (h) h->seekg(0);      // 闭包独占资源；h 在闭包内是成员，mutable 后可改
};
// C++11 退化方案（书给出）：用 shared_ptr 包一层 + std::bind 按值捕
```

没有初始化捕获的 C++11，lambda 只能按引用/按值拷贝捕获——move-only（unique_ptr、
fstream、std::thread）进不去。书的两个 workaround（shared_ptr 包一层；自造
`CaptureHelper` 模板 + 模板 operator()）都说明同一件事：**这是语法缺口而非设计妥协**，
C++14 补得干脆。异步任务场景（`std::async(..., std::move(lambda))`）里，
「闭包即独占资源载体」正是 [07 章](07-并发API.md) 任务化的前提。

### 3. 泛型 lambda 的转发正确姿势（Item 33）

```cpp
// 🔧 自写示意；等价机制已在 s3/s1 实测（forward+decltype 的类别还原）
auto logger = [](auto&&... args) {
    record(std::forward<decltype(args)>(args)...);   // 形参 auto&& 是转发引用
};
```

规则背下来：**每个 `auto&&` 具名形参都是转发引用**；对它必须
`std::forward<decltype(p)>(p)`（p 具名 → 恒为左值，不转发即「全转左值」，移动被静默吞掉）。
`decltype(p)` 在这里给出的是推导出的 `T&` 或 `T`，正是 forward 需要的类别记忆——
第 1 章的 decltype 与第 5 章的 forward 在 lambda 里会师。

### 4. lambda vs std::bind（Item 34）

| 维度 | lambda | std::bind |
| --- | --- | --- |
| 参数转发 | 可见、可完美转发 | 占位符被 eager 求值并转发，规则不透明 |
| 内联 | 闭包 operator() 是普通成员函数，几乎必内联 | 经 `bind` 结果对象的 `operator()`，常被内联但不保证 |
| 类型 | 唯一匿名类型，`auto` 可持有 | 类型名 `std::_Bind<…>` 不可读 |
| 可读性 | 形参/返回类型自文档 | `_1`/`_2` 位置噪声 |
| 编译期 | C++14 起 lambda 可 constexpr（C++17 起隐式） | 不能 constexpr |

bind 仅存的合理场景：老代码里「按值捕获求值的哨兵参数」（`bind(f, _1, chrono::seconds(10))`
的占位技巧）与极少数占位复用；新代码一律 lambda。

## 权衡：std::function 的税

把闭包装进 `std::function<bool(int)>` 的代价：① 超出 SBO（libstdc++ 通常 16 字节）即堆分配；
② 间接调用挡住内联；③ 每次拷贝闭包可能重新分配。热路径的正确默认是**模板参数**
（`template<typename F> void algorithm(F&& f)`——转发引用 + 零开销），
或 C++26 时代的 `function_ref`（见演进节）。接口边界（回调注册表、Pimpl 内）再用
`std::function` 换可存储性。这条「先模板后 function」的排序与
[02-auto.md](02-auto.md) 的「auto 默认」同源：**抽象成本要按场景付费**。

## 相邻概念对比

- **`[=]` vs `[this]` vs `[=, this]`（C++20）vs `[=, *this]`（C++20）**：
  四代语义从「隐式捕 this」到「显式声明捕 this」再到「按值拷整个对象」。
- **lambda vs 函数对象类**：同一件事的两种写法；需要**状态机**（多次调用间累加）时具名类
  仍胜在可测试性。
- **lambda vs `std::bind`**：见上表。
- **泛型 lambda vs 模板函数**：`auto` 形参即函数模板；差别只在捕获与声明位置。

## 最新演进与工业实践

- **C++14→20 的 lambda 年表**：C++14 泛型 lambda + 初始化捕获（本书主体）；
  C++17 lambda 满足条件时隐式 `constexpr`；
  **C++20**：lambda 在**unevaluated context** 可用（`decltype([]{…})`，构造一次性比较器
  进 `set` 的工厂从此不写函数名）、**模板 lambda**（`[]<typename T>(T x){…}` 显式模板参数列表合法）、
  `[=, this]` 显式写出、`[=]` 中隐式捕 this 被**弃用**（警告级）——
  Item 31 的「事故源一」由编译器接管。
- **`function_ref` 路线**：LLVM 的 `llvm::function_ref`、Folly 的 `folly::FunctionRef`
  提供「不拥有、非擦除」的轻量调用引用；C++23 已收录 `std::move_only_function`
  （提案 [P2387R3](https://wg21.link/P2387)，经 wg21.link 解析核实存在，标题不在此逐字引用）；
  `function_ref` 本体仍在推进 ⚠️。对 Item 34/std::function 税的最终答案大概率是它。
- **ranges 的管道就是 lambda 工厂**：`v | std::views::filter([](auto x){…})` 的可组合性
  建立在「view 可平凡拷贝」约束上——闭包对象生命周期纪律的库层兑现
  （[range-v3](https://github.com/ericniebler/range-v3)）。
- **协程与 lambda**：C++20 协程体里按引用捕 lambda 的悬挂是新型事故（协程帧即「闭包的闭包」）；
  工业库（[folly::coro](https://github.com/facebook/folly)）在文档里强制「捕获即拥有」。
- **对本书结论的修订**：四条全部存活；Item 31 从「建议」升级为「C++20 警告」；
  Item 32 的 C++11 workaround 全部可删。

## 常见误区

1. 「`[=]` 捕获了成员值」——捕的是 this 指针（C++11/14）；C++20 起该写法已被弃用，
   想按值捕对象要 `[=, *this]`。
2. 「`[&]` 只捕了我用的」——它捕到你**写出的**每个名字，新增引用形参/成员即静默扩员；
   显式捕获列表的 diff 才是可审计的。
3. 「`auto&&` 形参反正都是引用，直接传给下游」——丢类别：`int` 左值实参会以左值身份到底
   （Item 33 的 forward 正是为此）。🔧 s3 实测路径分叉。
4. 「std::function 很轻」——它比裸 lambda 多一层类型擦除；把「传个比较器」写成
   `std::function` 形参是在热循环里交税。
5. 「闭包 `operator()` 不能改捕获」——默认 const 而已；`mutable` 即解禁，
   一次性闭包（once_flag 自造版）靠它。

## 与其他章/其他笔记的联系

- 类别与转发：[01-类型推导.md](01-类型推导.md)、[05-右值移动完美转发.md](05-右值移动完美转发.md)。
- 闭包入任务/线程：[07-并发API.md](07-并发API.md)（Item 32 的最大买家）；
  资源入闭包的拥有链：[04-智能指针.md](04-智能指针.md)。
- 中文体系化：[../现代C++实战30讲/09-函数对象lambda与函数式编程.md](../现代C++实战30讲/09-函数对象lambda与函数式编程.md)、
  类型擦除：[../现代C++实战30讲/10-可变模板tuple与类型擦除.md](../现代C++实战30讲/10-可变模板tuple与类型擦除.md)。
- 本仓库笔记：[../../cpp/cpp11.md](../../cpp/cpp11.md)、[../../cpp/CRTP.md](../../cpp/CRTP.md)（函数对象替代谱系）。

---
上一章：[05-右值移动完美转发.md](05-右值移动完美转发.md) ｜ 下一章：[07-并发API.md](07-并发API.md) ｜ 返回：[00-总览与阅读地图.md](00-总览与阅读地图.md)
