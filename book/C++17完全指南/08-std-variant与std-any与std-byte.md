# 08 std::variant、std::any 与 std::byte

> 覆盖原书 **Part III 第 16–18 章**：`std::variant`（类型安全 union）、`std::any`（类型擦除容器）、`std::byte`（原始存储）。
> 一句话：**variant 把「几种类型之一」写进类型系统；any 把「任意一种」推迟到运行期；byte 把「只是一串位」和「是数」分开。**
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)｜[06-constexpr-if与折叠表达式.md](06-constexpr-if与折叠表达式.md)

## 核心概念速览（中英对照）

- **标签联合** — `std::variant<Ts...>`：任一时刻持有备选类型之一的值；`index()` 给当前下标，`variant_size_v` 给宽度。
- **无值占位** — `std::monostate`：让第一个备选可「空」的标准占位类型（`variant<monostate, T>` ≈ optional）。
- **访问器** — `std::visit(f, v)`：对**每个**备选都要有 `f` 的重载，否则编译失败；`f` 必须在所有分支上返回**同一类型**（实测诊断）。
- **重载集** — `Overloaded`/overload set：继承 + `using Ts::operator()...;` 把 lambda 堆成一个访问器（指引写法见 `05`/`06`）。
- **值丢失状态** — valueless-by-exception：标准允许 emplace/赋值中途抛出后 variant 不持有任何值；实测本机行为与标准文本有出入（见下 ⚠️）。
- **窄化剔除** — P0608：variant 的转换构造/赋值经 `Ti t[] = {e}` 语义筛选备选，**任何窄化路径直接出局**（本章有完整实测矩阵）。
- **类型擦除容器** — `std::any`：持有任意**可拷贝构造**类型；`type_info` 运行期校验，`std::any_cast<T>` 取出，失败抛 `std::bad_any_cast`。
- **字节类型** — `std::byte`：只参与位运算与 `std::to_integer<T>`，算术运算符一律缺席（实测负例）。

## 动机：union 的三宗罪与「存在性光谱」的另外两格

C 的 `union` 不记类型（读到哪个成员全凭默契）、不能持有非平凡类型（C++11 起勉强可以但构造/析构手写）、
改活跃成员即 UB。C++17 之前的标准库补法是 `boost::variant`（实现差异大）与「基类指针 + 手写虚函数」
（堆分配 + 所有权）。`optional`（`07`）解决「有没有」；`variant` 解决「是哪种（枚举在几种类型里）」；
`any` 解决「是哪种（编译期根本不知道）」；`byte` 解决「别把它当数，它只是存储」。

## 机制与实测证据

### 1. visit 如何分发（已实测 g++ 15.2 -std=gnu++17）

```cpp
std::variant<int, std::string, double> v = 3.5;
v.index()                                   // 2
std::holds_alternative<double>(v)           // 1
std::visit(Visitor{}, v);                   // 经典重载函数对象
std::visit(Overloaded{[](int){...}, [](auto){...}}, v);   // lambda 重载集（C++17 需推导指引）
try { std::get<std::string>(v); } catch (const std::bad_variant_access&) {}   // 实测抛出
std::variant<std::monostate, int> w;        // w.index()==0：monostate 占「没有」
// sizeof(variant<int,string,double>)==16（MinGW 实测；同上，布局是实现细节 ⚠️）
```

`visit` 的内核是**编译期二维表**：对 `Ts...` 的每个下标生成一条 `f(get<I>(v))` 分支，运行期按 `index()` 跳转。
分支间返回类型必须一致，实测诊断原文：
`static assertion failed: std::visit requires the visitor to have the same return type for all alternatives`。
两个 variant 的交叉访问（`visit(f, v1, v2)`）实测可用，规模是备选数的乘积。

**返回引用**：所有分支返回同一引用类型（如 `Holder&`）时，实测 C++17 档位就能拿到引用并改到原对象
（`after visit-ref: 9`）；混合返回不同引用类型则命中上面的 static_assert。

### 2. P0608 窄化剔除——本机完整实测矩阵

`std::variant` 的转换构造按标准以「`Ti t[] = {std::forward<U>(u)}` 是否良构」筛选备选（list-initialization
语义 ⇒ 窄化出局）。g++ 15.2 实测：

| 代码 | 结果（实测） | 解读 |
| --- | --- | --- |
| `variant<string, bool> v = "abc";` | ✅ index=0（string） | P0608 名场面：修复前会静默落进 `bool` |
| `variant<long, float> v{42};` | ✅ index=0（long） | `int→float` 窄化出局，`int→long` 提升留下 |
| `variant<int, float> v{1};` | ✅ index=0（int） | 精确匹配，无需转换 |
| `variant<int, string> v; v = 3.5;` | ❌ `no match for 'operator='` | `double→int` 窄化出局、`double→string` 不可——**P0608 的初衷**：修复前静默截断成 int |
| `variant<double, float> v{42};` | ❌ `no matching function` | 反直觉的一条：非恒定 `int→double` 在**列表初始化**里同样算窄化（`-pedantic-errors` 实测报 `narrowing conversion of 'i' from 'int' to 'double'`），两个备选全出局 |
| `variant<float, string> v{42};` | ❌ `no matching function` | 同上：`int→float` 窄化出局；`float` 想接住整数字面量的旧时代结束了 |

要点：**别给 variant 放「互相可隐式转换」的数值备选**（`variant<double,float>` 这类组合今天直接编不过，
过去是随机落点）；需要时写 `in_place_type` 或换类型（`variant<int64_t, double>`）。

### 3. valueless-by-exception：标准口径 vs 本机实测 ⚠️

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
struct Bad { Bad() { throw 1; } };
std::variant<S, Bad> v;          // 持 S
try { v.emplace<1>(); } catch (...) {
    // 实测：index()==0 且 valueless_by_exception()==false ——旧值竟然完好
}
```

标准文本（[variant.emplace]）说构造抛异常后 variant **应处于 valueless 状态**；本机 libstdc++ 15.2
实测却保持原值（一个「比标准更强」的实现行为，另有同型 int 版实测一致 ⚠️ 请勿把两侧任何一侧当契约）。
工程结论只有一条：**写了 variant 的代码必须能处理 `valueless_by_exception()==true`**（`index()==variant_npos`，
此时 `get`/`visit` 抛 `bad_variant_access`），哪怕你当前用的编译器不会造出这个状态。

### 4. std::any：可拷贝性是入场券（实测）

```cpp
std::any a = 1;              a.type() == typeid(int);   std::any_cast<int>(a)   // 1
sizeof(std::any)             // 16（MinGW 实测：指针+type_info 指针；small-size 优化是实现私有 ⚠️）
std::any_cast<std::string>(a) // 实测抛出：what() == "bad any_cast"
// 🔧 已实测被 g++ 15.2 拒绝：
std::any a = std::make_unique<int>(1);
// 错误原文（片段）：conversion from 'std::__detail::__unique_ptr_t<int>' to non-scalar type 'std::any' requested
```

`any` 要求 `is_copy_constructible_v<T>`——移动专用类型（`unique_ptr`）进不去；想装「独占资源」请用
`variant`/`optional<unique_ptr>`。`any_cast<T&>` 拿引用、`reset()` 释放，语义同族。

### 5. std::byte：只是存储（实测）

```cpp
std::byte b{42};                       // ✅ 从无符号整数「列表初始化」
std::byte c = 42;                      // ❌ 实测：cannot convert 'int' to 'std::byte' in initialization
std::to_integer<int>(b)                // 42
b << 1; b | std::byte{1};              // 位运算合法（实测）
b + 1;                                 // ❌ 不存在 operator+：byte 不是小整数
```

用途边界：表达「对象表示（object representation）」——内存块、序列化缓冲、`memcpy` 源。
要参与算术就 `to_integer`，这正是设计意图：**算术是整数的事，存储才是 byte 的事**。

## 权衡

| 决策点 | variant | any | 继承多态 |
| --- | --- | --- | --- |
| 类型集合是否编译期已知 | ✅ 必须 | ❌ 任意可拷贝 | 半开放（基类族） |
| 堆分配 | 无（内嵌存储） | 大对象通常有 ⚠️ 实现相关 | 有（new 派生类） |
| 访问方式 | `visit`/`get<T>`，编译期全覆盖 | `any_cast`，运行期赌博 | 虚函数 |
| 值语义 | ✅ | ✅ | ❌ 需手写 clone |
| 加新类型 | 改 `Ts...` 即改所有 visit | 无感 | 无感（多态自动） |

## 相邻概念对比

- **variant vs `01` 结构化绑定**：绑定拆「一个对象的多个成员」；variant 存「多个类型的一个」。别试着 `auto [a,b] = var`——拆不了。
- **variant vs `07` optional**：`variant<monostate, T>` ≈ `optional<T>`，但 `optional` 的接口（`has_value`/`value_or`/monadic）为人道设计，别用 variant 凑。
- **any vs `void*`**：any = 带 `type_info` 校验的 void*，`any_cast` 错了抛异常而非静默错读。
- **byte vs `uint8_t`**：`uint8_t` 是数（有算术、参与流格式化）；byte 是存储。`std::string` vs `std::vector<byte>` 的取舍同理。

## 最新演进与工业实践

**标准之后**
- **P0608R3**（✅ wg21 实测可达，标题实测抓取为 **「A sane variant converting constructor」**——网上常见的
  「improve variant and any assignments」是早期修订标题 ⚠️）：本章 §2 矩阵的规则来源。
- **C++20 P2162R2「Inheriting from std::variant」**（✅ 可达，标题实测）：让 `struct MyV : variant<...>` 能
  继承推导指引/构造函数，此前「给 variant 加成员函数」处处别扭（实测 GCC 15 的 C++17 档位已按新文本处理引用返回）。
- **C++23**：`std::to_underlying`（P1682R3 ✅ 可达）常被配进 variant+enum 的标签分发 ⚠️ 但本机 MinGW 15.2
  的 `<type_traits>` 里**找不到实体**（见 `12` 的实测坑）；any 侧的 P2665（any_cast 的 standard-layout 约束，
  wg21 可达 ✅，仅核实到 r0 PDF）。
- **C++23 `std::generator`（P2502R2 ✅ 可达）**对「树形 variant + 递归 visit」模式的冲击：递归遍历可以
  改写成惰性 yield，省掉手写栈的 visit 返回类型对齐问题（见 [../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md](../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md)）。
- **C++26 P2996 反射（✅ 可达）**：variant 最大卖点之一是「封闭类型集 ⇒ 可序列化」；反射落地后
  「结构体也能反射分发」，variant 的部分动机（手工枚举备选）会被稀释 ⚠️ 定稿范围见 `00`。

**工业实践与开源口径**
- **Abseil**：`absl::variant`/`absl::any` 为 C++14 兼容的先行实现，接口对齐标准；`absl::StatusOr` 与
  `variant<Status, T>` 语义同构（`abseil/abseil-cpp`，00 当日实测 ≈18.1k★）。
- **`neargye/magic_enum`**（00 当日实测 ≈6.2k★）：枚举名↔值↔列表反射三件套，常与 variant 的
  标签类型列表配合做「编译期注册表」。
- **visitor 模式对照**：GoF 的 AcyclicVisitor 在 variant 面前是同一件事的运行期版——见
  [../C++20设计模式/14-模板方法与访问者.md](../C++20设计模式/14-模板方法与访问者.md)。

## 常见误区（实测）

1. **`variant<int,float>` 装 42 会「自动挑 float」——错**：挑不挑得看窄化规则，`variant<double,float>{42}` 实测直接编译失败。
2. **`visit` 少写一个分支靠 `auto` 兜底就行——不完全**：`[](auto){}` 能通吃，但**拼错类型集**时静默掉进兜底分支；生产代码建议显式列举 + 兜底里 `static_assert`。
3. **`any` 能装 `unique_ptr`——错**：实测被拒（拷贝构造是入场券）。
4. **`std::byte` 是为了取代 `unsigned char` 做 `malloc` 缓冲——不对半**：`new byte[]`/`malloc` 的返回存储本来就是 `void*`；byte 的价值在**接口层**声明「这是存储不是字符」。
5. **valueless 是理论状态不用防——错**：`08` §3 实测本机行为与标准文本分歧，恰说明**两侧都不能假设**，防御性检查 `valueless_by_exception()` 是唯一安全姿势。

## 与其他章 / 其他笔记的联系

- ← 本目录 `06`：`using Ts::operator()...` 与折叠是 `Overloaded` 的语法地基。
- ← 本目录 `05`：聚合无 CTAD（C++17）⇒ `Overloaded` 必须手写指引；`variant v{42}` 的推导也在 `05`。
- ← 本目录 `07`：monostate-optional 的关系；`reference_wrapper` 作为 any/optional 的引用替身。
- → 本目录 `12`：`to_underlying`、`hardware_destructive_interference_size` 等小件与 byte/over-alignment 的交集。
- → [../C++标准库/02-通用工具与智能指针.md](../C++标准库/02-通用工具与智能指针.md)：`pair/tuple` 时代的多类型方案。
- → [../深度探索C++对象模型/06-执行期语意学.md](../深度探索C++对象模型/06-执行期语意学.md)：虚表分发 vs variant 的编译期分发在对象模型层面的成本对比。
- → [../C++20设计模式/01-导论-模式体系与C++20惯用法.md](../C++20设计模式/01-导论-模式体系与C++20惯用法.md)：「variant 改变模式写法」的总论。

## 思考题

1. 设计一个 `variant<std::monostate, int, std::string>` 状态的设置函数，写一个 visit 打印三种情况；再解释为什么不直接用两个 `optional`。
2. 用本章实测矩阵解释：`variant<double, int> v{1}` 编译得过吗？（提示：`int→double` 在列表初始化里算不算窄化？`int→int` 呢？动手测并把结果并入你的表。）
3. `any` 的 `any_cast<T>(std::move(a))` 与 `any_cast<T&>(a)` 何时各自抛 `bad_any_cast`？写 6 行代码实测三种调用，并说明类型不匹配与值类别不匹配的区别。
