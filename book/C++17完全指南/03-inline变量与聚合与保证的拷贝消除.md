# 03 inline 变量、聚合扩展与保证的拷贝消除

> 覆盖原书 **Part I 第 3–5 章**：Inline Variables / Extensions for Aggregates / Mandatory Copy Elision。
> 三个特性看似无关，其实同一主题：**去掉「为了让编译器满意而写的样板与多余拷贝」**。
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)

## 核心概念速览（中英对照）

- **inline 变量** — inline variables：`inline int x = 0;` 允许在头文件里定义非局部变量而不违反 ODR（所有 TU 共享一个实体）。
- **inline 静态数据成员** — inline static data members：`struct C { inline static int n = 0; };` 从此不需要类外定义。
- **聚合类型** — aggregate：无用户构造、无私有/保护非静态成员、无虚函数/虚基类/私有基类的「纯数据」类型；C++17 放宽了「可有默认成员初始化器」「可有公有基类」两条。
- **花括号省略** — brace elision：聚合初始化时嵌套花括号可省，把实参依次喂给「展开后的子对象序列」。
- **保证的拷贝消除** — mandatory copy elision：prvalue 直接在目标存储就地构造，**不再要求**拷贝/移动构造存在且可访问。
- **就地构造** — in-place construction：`emplace`、`std::pair` 的 piecewise、`make_from_tuple` 的共同思想。
- **NRVO 非强制** — non-mandatory named return value optimization：返回**具名**局部量仍需可移动/可拷贝（实测确认）。

## 3.1 inline 变量（原书 Ch3）

### 动机

C++14 之前，「头文件里声明 + 某个 cpp 里定义」是唯一合法做法，代价是：模板静态成员的类外定义、
`constexpr` 静态成员的 ODR-use 链接错误、单例/全局计数器要在多个 TU 间手工协调。

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17：两个 TU 分别 include 同一头文件，链接后计数合并
// hdr.h
#pragma once
#include <string_view>
inline constexpr std::string_view kVersion{"1.0"};
inline int g_counter = 0;                                   // ← C++17 才合法的头文件定义
struct Config { inline static int instances = 0; };          // ← 静态数据成员就地定义
// tu1.cpp: int use1() { ++g_counter; ++Config::instances; return (int)kVersion.size(); }
// tu2.cpp: main 里调用 use1() 两次并打印
// 运行输出：g_counter=2 instances=2      （若为每 TU 各一份，会打印 1 1 或直接链接冲突）
```

### 机制与注意

- `inline` 在这里**不是**「建议内联展开」，而是「允许多处定义、实体唯一」——和 inline 函数的语义一致。
- `inline constexpr` 组合是库作者的最爱：头文件里给出可 ODR-use 的常量对象，不需要再写类外定义。
- **不要**给函数内 static 局部变量加 `inline`（无意义，局部 static 本来就是单实体）。

⚠️ 实测补充：`g++ -std=gnu++14` 对本例**只是警告**（`warning: inline variables are only available with
'-std=c++17' or '-std=gnu++17' [-Wc++17-extensions]`）并照常编译——GNU 扩展模式下特性被当作扩展放行。
判断标准支持度要看 `-std=c++17`（严格档）而不仅是能否编过。

## 3.2 聚合类型的扩展（原书 Ch4）

C++17 把「聚合」的定义放宽了两条，于是 `struct` 重新变得可用：

| 条件 | C++11 | C++14 | C++17 | C++20 |
| --- | --- | --- | --- | --- |
| 允许非静态数据成员带默认成员初始化器（`= 42`） | ❌ | ⚠️ 见下注 | ✅ | ✅ |
| 允许有基类（须公有、非虚） | ❌ | ❌ | ✅ | ✅（要求见下） |
| 有用户提供的构造 | 不是聚合 | 不是聚合 | 不是聚合 | 不是聚合 |
| 私有/保护非静态成员 | 不是聚合 | 不是聚合 | 不是聚合 | 不是聚合 |
| 有虚函数/虚基类/私有保护基类 | 不是聚合 | 不是聚合 | 不是聚合 | 不是聚合 |
| 聚合能否用**圆括号**初始化 | ❌ | ❌ | ❌ | ✅（P0960R3，见 `05`） |

⚠️ 关于第一行的实测修正：`struct S { int a; int b = 2; };  S s{1, 5};` 在
`g++ -std=gnu++14 -Wall -pedantic-errors` 下**照样通过**——「带默认成员初始化器的聚合」这一限制被当作
缺陷修复在 C++14 就放行了（社区一般以 CWG1397 记录 ⚠️ 编号未逐字核实）。表里 C++14 的 ❌ 是原书面貌
（它对照的是 C++11），今天写代码请按下表理解：**C++11 非法，C++14 起合法**。

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17 通过（三条 static_assert 全部成立）
struct Base { int b; };
struct Mid  : Base { int m; };                 // 有公有基类 → C++17 仍是聚合
struct Leaf : Mid  { int l = 42; };            // 带默认成员初始化器 → C++17 仍是聚合
struct NoAgg { NoAgg(int) {} int x; };         // 有用户构造 → 不是聚合
static_assert(std::is_aggregate_v<Mid>);
static_assert(std::is_aggregate_v<Leaf>);
static_assert(!std::is_aggregate_v<NoAgg>);
```

⚠️ 跨档位实测更正（对「C++20 收紧聚合」这一常见记忆的修正）：我在 `-std=gnu++17/20/23` 三个档位下
重复 `std::is_aggregate_v<Mid>`，**g++ 15.2 三次都给 true**。也就是说「带公有基类的派生类在 C++20 不再
是聚合」这一说法在本机实现上不成立；聚合规则在 C++20 的变化点是
「带用户构造函数的**类模板特化**、以及 `using Base::Base` 继承构造」等细节，需按标准原文核对 ⚠️（未逐字核实）。

### 花括号省略：聚合的新表达力也是新坑

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17，输出（原样抄自运行结果）：
//   x: 1 0 2
//   y: 1 2 42
//   z: 7 8 9
struct Base { int b; };  struct Mid : Base { int m; };  struct Leaf : Mid { int l = 42; };
Leaf x{{1}, 2};      // {1} 整体喂给基类 Mid（Mid 的 b=1、m=值初始化 0），2 喂给 Leaf::l
Leaf y{1, 2};        // 省略嵌套花括号：1→Base::b，2→Mid::m，l 取默认 42
Leaf z{Base{7}, 8, 9};  // 显式花括号：7→b，8→m，9→l
```

**结论**：同一层花括号写不写，会**改变实参与子对象的对齐方式**，从而静默地少初始化/错初始化成员
（`x` 的 `m` 成了 0，`l` 成了 2）。这类错误编译器完全不报——**多维聚合请用显式花括号**，或干脆给它写构造函数。

## 3.3 保证的拷贝消除（原书 Ch5）

### 动机：C++14 的「可选优化」让 API 行为不确定

C++14 里 `T a = f();` 允许发生一次拷贝/移动（能否被优化是实现选择），因此：
- 不可拷贝/不可移动的类型**不能**这样用；
- 「到底调用了几次构造函数」不可依赖，测试与日志会随优化档位变。

C++17 改成**语义保证**：prvalue 不再是一个临时对象「然后」初始化目标，而是**直接在目标存储上构造**。

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17 通过并运行；输出：
//   a 构造后 created=1
//   形参就地构造，created=2
//   总计 created=2（若无强制消除会编译失败）
struct NoMove {
    NoMove() { ++created; }
    NoMove(const NoMove&) = delete;      // 既不可拷贝
    NoMove(NoMove&&) = delete;           // 也不可移动
    static int created;
};
int NoMove::created = 0;
NoMove make() { return NoMove{}; }       // ✅ C++17：prvalue 返回，不需要可访问的拷贝/移动
void sink(NoMove p) { (void)p; }         // ✅ C++17：prvalue 实参直接构造形参
int main() { NoMove a = make(); sink(NoMove{}); }
```

**同一份代码在 `-std=gnu++14` 下被实测拒绝**（错误原文节选）：
`error: use of deleted function 'NoMove::NoMove(NoMove&&)'`，分别出现在 `return NoMove{};` 与
`NoMove a = make();` 两处。这就是「强制消除」最直观的证明：**它改变的是合法性，不只是性能**。

### 它没有覆盖的两处（实测）

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17 拒绝（两处）
struct T { T(){} T(const T&)=delete; T(T&&)=delete; };
T f1(){ T local; return local; }         // error: use of deleted function 'T::T(T&&)'  ← NRVO 不保证
T f2(NoMove p) { return p; }             // error: 同上 ← 具名形参 return 仍需可移动
```

`return 具名变量;` 是 lvalue→移动构造的语境，标准只把 NRVO 列为「可选」。所以「不可移动类型只能
一路 prvalue 传到底」，中途落地成变量就破功。

## 权衡

| 选择 | 好处 | 代价 |
| --- | --- | --- |
| `inline` 变量替代「extern 声明 + 单点定义」 | 头文件自洽、模板静态成员简单 | 全局状态更「顺手」，滥用即耦合；`inline` 变量的初始化顺序问题依旧存在 |
| 聚合 + 默认成员初始化器（C++17 写法） | 无样板构造、可 `T{a,b}`、与 CTAD/结构化绑定配合 | 花括号省略静默错位（3.2 实测）；无法做参数校验 |
| 依赖强制拷贝消除 | 不可移动类型可穿越工厂函数；无性能悬念 | 一旦引入具名中间变量即失效；`-std=c++14` 迁移回退会硬报错 |

## 相邻概念对比

- **强制消除 vs RVO/NRVO**：前者是**语义**（prvalue 无独立对象），后者是**优化**（具名对象的拷贝可被省）。
- **强制消除 vs 移动语义**：移动不是「消除拷贝的替代」，prvalue 语境下根本没有对象可移动。
- **聚合 vs 带构造的值类型**：要不变式（invariant）就写构造函数；聚合适合「纯数据 + 手工保证合法」的边界内代码。
- **inline 变量 vs 匿名命名空间**：前者解决「一个实体多处声明」，后者解决「每 TU 各一份」；两者目标相反。
- **`std::is_aggregate_v` vs `std::is_trivially_copyable`**：聚合是关于初始化语法，可平凡拷贝是关于内存布局；
  加构造函数会同时破坏两者，但 `= default` 构造在 C++17 的判定细节需查表 ⚠️。

## 最新演进与工业实践

**标准之后**
- **C++20 P0960R3（已核实标题「Parenthesized initialization of aggregates」）**：`Leaf y(1, 2, 42);`
  这种圆括号聚合初始化终于合法；与 CTAD 的聚合推导（见 `05`）合起来补齐了「聚合不像类」的缺口。
- **C++20 designated initializers（`.b = 1`）**：GCC 在 `-std=gnu++17` 下作为扩展接受 ⚠️（严格
  `-std=c++17 -pedantic-errors` 会拒），迁移代码时别被 GNU 模式的绿灯误导。
- **C++23/C++26**：`inline` 变量与强制消除没有新增语法；C++26 的反射提案会让「按字段初始化聚合」更工程化，
  但对本章三项无破坏性改动 ⚠️。
- **静态初始化顺序**：inline 变量没解决「跨 TU 初始化顺序」，工业代码仍用函数内 static（Meyers singleton）绕开。

**工业实践与开源口径**
- **Abseil / fmt / range-v3** 都大量使用 `inline constexpr` 常量对象与标签对象（tag object）：
  `fmtlib/fmt`（实测 **≈25.8k★**，2026-09-26）里格式化字符串与编译期检查所需的常量即以
  `inline constexpr` 形态存在于头文件；`ericniebler/range-v3`（实测 **≈4.4k★**）同理。
- **单例/全局注册表**：现代做法是 `inline` 变量 + 函数内 static 混合；`boost::core::addressof` 一类
  库设施也走 inline 变量口径（`boostorg/boost` 实测 **≈8.6k★**）。
- **反射库**：`neargye/magic_enum`（实测 **≈6.2k★**，2026-09-26）依赖编译器对枚举/类型的可访问性，
  与聚合的可拆性配合良好；它同时是 `08` 章 variant 名字反射的常用补丁。
- **性能口径**：强制消除的收益在「返回大对象 + 不可移动资源」的场景最明显；对可移动的小对象，
  移动本来就近乎零成本，别把「省一次移动」当成迁移理由。

## 与其他章 / 其他笔记的联系

- ← 本目录 `01`：聚合是结构化绑定的三类可拆对象之一；默认成员初始化器让「拆出来再改」更常见。
- → 本目录 `05`：聚合的 CTAD 缺失（C++17）正是本章「聚合规则放宽」的另一面后果，两章要连读。
- → 本目录 `07`：`std::optional`/`std::variant` 的 `emplace` 就是就地构造思想的标准化 API。
- → 本目录 `12`：`std::make_from_tuple`、`try_emplace` 同属「少一次临时对象」家族。
- → [../现代C++实战30讲/03-右值与移动及返回对象.md](../现代C++实战30讲/03-右值与移动及返回对象.md)：
  值类别与移动语义的前置讲解——不懂 prvalue/xvalue 就读不动 3.3。
- → [../Effective_Modern_C++/05-右值移动完美转发.md](../Effective_Modern_C++/05-右值移动完美转发.md)：
  Meyers 的 Item 25–30 是「C++14 视角的痛点清单」，本章是它的 C++17 答复。
- → [../C++标准库/03-STL总览.md](../C++标准库/03-STL总览.md)、[../深度探索C++对象模型.md](../深度探索C++对象模型.md)
  （对象布局视角解释「就地构造」到底省了什么）。

## 思考题

1. 把一个 C++14 代码库切到 `-std=c++17` 后，哪一类「原本能编过」的代码会**新增**编译错误？（提示：3.3 的
   `return 具名量;` 与 `-Wc++17-extensions` 的反面。）
2. `struct S { int a; int b = 2; };` 在 C++14 与 C++17 分别是不是聚合？`S s{1};` 的 `b` 是多少？
3. `inline constexpr std::array<int, 3> kPrimes{{2,3,5}};` 为什么必须写双花括号？与 3.2 的花括号省略有何关系？
