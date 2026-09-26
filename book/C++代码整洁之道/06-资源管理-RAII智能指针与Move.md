# 第 5 章（上）资源管理：RAII、智能指针与移动语义

> 英文原章：Chapter 5: *Advanced Concepts of Modern C++* 的 5.1 Managing Resources（5.1.1 Resource Acquisition Is
> Initialization / 5.1.2 Smart Pointers / 5.1.3 Avoid Explicit `new` and `delete` / 5.1.4 Managing Proprietary
> Resources）与 5.2 We Like to Move It（5.2.1 What Are Move Semantics? / 5.2.2 The Matter with Those lvalues and
> rvalues / 5.2.3 rvalue References / 5.2.4 Don't Enforce Move Everywhere / 5.2.5 The Rule of Zero）。
> 原版 p85–102；中译 p83–102。
> 系列导航：[../C++系列·总索引.md](../C++系列·总索引.md) ｜ 单文件大纲：[../C++代码整洁之道.md](../C++代码整洁之道.md) ｜ 返回：[00-总览与阅读地图.md](00-总览与阅读地图.md)

## 核心概念速览（中英对照）

- **资源获取即初始化** — RAII（Resource Acquisition Is Initialization）：资源在构造函数取得、在析构函数释放，生命周期=作用域（5.1.1）
- **ScopedGuard / 作用域守卫** — 书 L5-3/L5-4 的 `ScopedResource<T>`：一个通用模板管理任意"需成对释放"的资源
- **独占所有权** — Exclusive Ownership：同一时刻只有一个所有者，`std::unique_ptr<T>` 的类型化表达（5.1.2）
- **共享所有权** — Shared Ownership：引用计数控制块，`std::shared_ptr<T>`（5.1.2）
- **弱引用** — `std::weak_ptr<T>`：不拥有、可失效的观察句柄；`lock()` 提升为 `shared_ptr` 后才可用（5.1.2，L5-6…L5-8）
- **控制块** — Control Block：`shared_ptr` 的计数与删除器存放处；`make_shared` 与本体合并分配
- **循环引用** — Circular Reference：`shared_ptr` 互相指向即永不归零（L5-7），用 `weak_ptr` 破环（L5-8）
- **避免显式 new/delete** — Avoid Explicit `new` and `delete`：所有权交给工厂函数 `std::make_unique/make_shared`（5.1.3）
- **特有资源** — Proprietary Resources：句柄、套接字、`FILE*`、锁——非内存但同样需成对操作，靠自定义删除器接管（5.1.4）
- **移动语义** — Move Semantics：以窃取资源代替深拷贝（5.2.1）
- **左值/右值** — lvalue / rvalue：作者采"locator value（有身份）vs 临时可窃取"的日常定义（5.2.2）
- **右值引用** — rvalue Reference：`T&&`，移动构造/赋值与完美转发的语法基础（5.2.3）
- **移动后有效但未指定** — Valid but Unspecified：被移动对象的合法状态，"别假设它为空"（5.2.4 的隐患）
- **不要到处强制移动** — Don't Enforce Move Everywhere：对局部变量 `std::move(x)` 反而阻断 NRVO/复制消除（5.2.4）
- **零法则** — Rule of Zero：不手写特殊成员函数，把资源管理交给成员类型（5.2.5，L5-13/L5-14）
- **五法则/三法则** — Rule of Five / Rule of Three：零法则的对立面，仅在真的直接持有资源时才适用

## 1. 动机：内存泄漏不是"漏一点"，而是"不可推理"

作者的立场与 Effective 系列一致：**手工配对释放的代码无法局部推理**——任何一条提前 `return`、一个抛出、
一处 `break` 都会破坏配对。5.1.1 的对照（L5-1 堆上手工管理 vs L5-2 栈上对象）就是这个论证：
前者要在四条出口各写一次释放，后者**一条都不用写**。C++ 的异常机制使这一点从"麻烦"升级为"不可能正确"，
因此 RAII 是本书第 8 节（异常）的前置条件。

## 2. 机制：所有权分层与移动的角色

1. **默认 `unique_ptr`**：表达"一个所有者"，零开销（大小=裸指针，见实测）；跨函数传所有权用 `std::unique_ptr<T>` 值参 + `std::move`。
2. **`shared_ptr` 只在共享真是语义时**：控制块带来原子计数与额外分配；`make_shared` 把控制块与对象合并成一次分配
   （代价：弱引用存活期间对象内存不归还）。
3. **`weak_ptr` 是"不拥有"的类型化表达**：观察者、缓存、pimpl 的可选部分——L5-6 的用途正在于此。
4. **移动是智能指针的运力**：`unique_ptr` 之所以能"传所有权"，全靠移动语义；反之，5.2.4 提醒
   "`std::move` 不是指令而是许可"——写多了会把优化机会搬走。
5. **零法则是收敛点**（5.2.5）：L5-12 的 `MyString` 手写 `char*` + 五法则，L5-13 用 `= delete` 关掉拷贝，
   L5-14 把 `char*` 换成 `std::vector<char>` 后**析构函数直接不需要了**。作者的原话式结论：
   零法则的实现路径就是"永远用拥有资源的成员类型，别直接持有裸资源"。

## 🔧 实测：所有权机制的可观察后果（已实测 g++ 15.2，`-std=gnu++17 -Wall -Wextra`）

**(1) 裸 `new` 与 `make_unique` 的行为差异 + 构造/析构计数**：

```text
[open ] db-bare-new (alive=1)
[send ] -> db-bare-new
bare new 之后 alive=1（资源未归还）
[open ] db-make_unique (alive=2)
[send ] -> db-make_unique
[close] db-make_unique (alive=1)
make_unique 之后 alive=1（回到泄漏基线）
[node+] / [node+] 两个 Node 构造
离开作用域前: a.use_count=2 b.use_count=2
若上面没有两行 [node-]，循环引用即泄漏      <-- 实测确实没有 [node-]
fopen ok=1
[fclosed] 自定义删除器接管特有资源            <-- 在作用域末端自动执行
final alive=1
sizeof(unique_ptr)=8 sizeof(shared_ptr)=16 sizeof(Connection)=32 sizeof(T*)=8
```

三条被钉死的事实：①裸 `new` 的资源在函数结束时仍在世（`alive` 不回落）；②`shared_ptr` 成环后**没有任何析构输出**，
`use_count=2` 就是尸检报告；③**`unique_ptr` 与裸指针同宽（8 字节）而 `shared_ptr` 是 16 字节**（指针 + 控制块两个指针），
5.1.2 所谓"零开销抽象"对 `unique_ptr` 成立、对 `shared_ptr` 不成立。
自定义删除器（5.1.4 特有资源）的关闭动作发生在栈展开顺序的正确位置，无需一行手工配对代码。

**(2) 移动 vs 拷贝的真实计数（5.2.4/5.2.5）**：

```text
五法则版本: copies=1 moves=1
不 reserve 的 4 次 push_back: copies=1 moves=8 (若移动非 noexcept 则拷贝)
is_nothrow_move_constructible<Blob>=1 is_trivially_default_constructible<ZeroRuleBlob>=0 sizeof=32
```

`push_back(Blob{})`（临时）走移动、`push_back(named)`（具名）走拷贝——**移动不会自动发生在你叫得出名字的对象上**；
容器扩容的 8 次搬移全部走移动，前提正是那个 `noexcept`（此处为隐式获得，`std::string` 的移动构造不抛）。
"零法则类" `ZeroRuleBlob` 不是平凡构造（含 `std::string` 成员），但它**一行特殊成员函数都没写**——这就是零法则的形态。

## 3. 权衡

- **`shared_ptr` 的原子计数**：多线程共享时计数开销真实存在；单线程用 `shared_ptr` 只换来"共享所有权"这一语义收益，
  若并不需要共享，就该退回 `unique_ptr` + 引用传参。
- **RAII 的边界**：RAII 管"有明确生命周期终点"的资源。**跨进程/需要显式提交的资源**（事务、文件锁、外部副作用）
  不适合纯 RAII——"析构时悄悄回滚"是危险语义；这类要靠显式 `commit()` + 析构断言未提交（现代库普遍采此设计）。
- **移动的正确性成本**：移动后对象状态未指定，遍历时容易踩坑。零法则 + 立即重新赋值可缓释；
  对性能不敏感的接口直接禁移动（`= delete`）也是合法选择。
- **`make_unique` 的例外**：需要自定义删除器、或要接管已有裸指针（C API 返回值）时只能直接构造；
  C++17 起 `make_unique_for_overwrite` 处理未初始化内存（书中未涉及）。

## 4. 相邻概念对比

| 概念对 | 差别 | 为什么容易混 |
| --- | --- | --- |
| `unique_ptr<T>` vs `T&`/`T*` 非拥有引用 | 前者承诺"我负责销毁"，后者只承诺"此刻有效" | 把 `unique_ptr&` 当"借用的智能指针"到处传，语义反而更含糊；非拥有场景现代推荐 `std::span`/`T*`/`reference_wrapper` |
| `shared_ptr` vs 垃圾回收 | 前者是**编译期可见的所有权协议**（成本可控、成环即漏），后者是运行时系统（可处理环） | 从托管语言转来的人以为 `shared_ptr` 有环检测 |
| 移动 vs 交换 | 移动窃取资源并留下未指定态；交换让双方都保持有效 | "被移动的对象应当可安全析构"是真的，"可继续使用"是不成立的假设 |
| 零法则 vs 法则五 | 零法则=不写；五法则=要么全套要么全不 | 手写一个析构函数（为了打印日志）就会静默抑制拷贝/移动的自动生成 |
| 自定义删除器 vs 专用 RAII 类 | 删除器轻量但类型参与签名（`unique_ptr<FILE, FileCloser>`）；专用类可封装更多不变式 | 库边界上删除器会让头文件类型变复杂（`function` 型删除器还会多一个指针的体积） |
| RAII vs 智能指针 | RAII 是原则，智能指针是其一种实现；锁、文件、socket 的 RAII 与指针无关 | 于是"用了智能指针就是现代 C++"成了常见误解 |

## 最新演进与工业实践

- **语言演进对位（C++17→23）**：
  - C++17 保证复制消除（copy elision mandatory 场景），5.2.4"别对局部变量 `std::move`"的论证更硬；
    聚合初始化扩展（P0960，⚠️ 未在本目录内核验）让"零法则 + 聚合"更常用。
  - C++20 起 **`std::unique_ptr` 对数组/标量的接口统一** 与 `std::make_unique<T[]>(n)` 已完备；
    `std::to_address` 让"指针样对象"的通用代码不必再 `.get()`。
  - C++23 增补 `std::expected`（所有权之外，见 [08-异常与错误处理.md](08-异常与错误处理.md)）；
    **`std::out_ptr`/`std::inout_ptr`**（C++23）正是为"C API 输出裸指针 → 直接装进智能指针"而生，
    解决 5.1.4 里最脏的一公里（⚠️ 提案号未在本目录内核验，按标准版本口径引用）。
- **GSL 与 `owner<T>`**：Core Guidelines 用 `gsl::owner<T*>` 标注"我确实是裸所有权的出口"，把本书 5.1.3 的禁令变成
  可 grep 的约定；`Guidelines Support Library` 与 [../C++CoreGuidelines解析/07-资源管理.md](../C++CoreGuidelines解析/07-资源管理.md) 配套。
- **clang-tidy 对应项**（⚠️ 本机未安装，按上游文档口径）：
  `modernize-use-unique_ptr-for-new`、`cppcoreguidelines-owning-memory`、`cppcoreguidelines-no-suspend-with-lock`、
  `bugprone-use-after-move`（直接对应 5.2.4 的"移动后使用"）、`performance-move-const-arg`、
  `performance-unnecessary-value-param`、`hicpp-*` 家族。`bugprone-use-after-move` 是本章最值钱的一条自动检查。
- **工业仓库**：abseil 的 `absl::MutexLock`/`Cleanup` 是"非内存资源 RAII"的工业范本（`absl::Cleanup` 甚至把
  "作用域末尾执行任意善后"做成类型）；folly 的 `folly::ScopeGuard`、`fbstring` 展示了零法则在大规模库里的收益；
  fmt 的 `buffer`/`basic_memory_buffer` 是"vector 化 char* 从而析构消失"（L5-14 思路）的真实实现。
- **测试生态**：所有权语义要在测试里可见——用**计数替身资源**（本文件实测的做法）+ 断言 `alive == 0`，
  比依赖 valgrind/ASan 更可移植；GoogleTest/Catch2 均易实现。Windows 上 ASan 支持面有限，本机 MinGW 无 libasan（⚠️ 实测无法用 sanitizer），
  计数法几乎是唯一可行的常驻回归手段。

## 与相邻章/相邻书的互链

| 主题 | 去处 | 关系 |
| --- | --- | --- |
| 编译器协助（`auto`/`constexpr`）与 UB | [07-编译器搭档-UB-TypeRich与库.md](07-编译器搭档-UB-TypeRich与库.md) | 本章第 3、5 节的续 |
| 异常安全与拷贝-交换 | [08-异常与错误处理.md](08-异常与错误处理.md)、[12-设计模式与C++惯用法.md](12-设计模式与C++惯用法.md) | RAII 是异常安全的地基 |
| PIMPL 中的 `unique_ptr<Impl>` 析构点 | [12-设计模式与C++惯用法.md](12-设计模式与C++惯用法.md) | 本章机制与物理设计的交汇（实测报错见该章） |
| 智能指针条款总账 | [../Effective_Modern_C++/04-智能指针.md](../Effective_Modern_C++/04-智能指针.md)、[../Effective_Modern_C++/05-右值移动完美转发.md](../Effective_Modern_C++/05-右值移动完美转发.md) | 条款式对照（`enable_shared_from_this`、PImpl 析构点等） |
| 移动语义的机制底层 | [../深度探索C++对象模型/05-构造析构拷贝语意学.md](../深度探索C++对象模型/05-构造析构拷贝语意学.md) | 编译器到底做了什么 |
| 1993 的前史：handle/body 与引用计数 | [../C++编程惯用法/03-句柄.md](../C++编程惯用法/03-句柄.md) | 智能指针接管记账之前的世界 |
| 标准库实现视角 | [../C++标准库/02-通用工具与智能指针.md](../C++标准库/02-通用工具与智能指针.md) | 控制块、删除器、`make_*` 的实现细节 |

导航：上一级 [00-总览与阅读地图.md](00-总览与阅读地图.md) ｜ 上一章 [05 函数与 C 风格](05-函数设计与告别C风格代码.md) ｜ 下一章 [07 编译器搭档](07-编译器搭档-UB-TypeRich与库.md) ｜
单文件版 [../C++代码整洁之道.md](../C++代码整洁之道.md) ｜ 系列 [../C++系列·总索引.md](../C++系列·总索引.md)
