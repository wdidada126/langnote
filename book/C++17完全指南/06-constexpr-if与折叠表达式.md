# 06 constexpr if 与折叠表达式（编译期分支与参数包）

> 覆盖原书 **Part II 第 10–12 章与第 14 章**：`if constexpr`、编译期计算增强（字面量作模板参数）、
> 折叠表达式（Variadic Templates Without Recursion）、扩展的 `using` 声明。
> 一句话：**把「按类型分发」的模板样板压进一条编译期语句，把「递归展开参数包」压进一个运算符。**
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)｜[05-类模板实参推导CTAD.md](05-类模板实参推导CTAD.md)

## 核心概念速览（中英对照）

- **编译期 if** — `if constexpr`：条件是编译期常量表达式；未选中分支**不被实例化**，类型检查随之推迟或免除。
- **丢弃语句** — discarded statement：`if constexpr` 未选中的整句/整支；语法仍必须合法，非依赖错误多数实现仍要检查（GCC 宽松，见实测）。
- **实例化消除** — instantiation suppression：`Heavy<T>` 只有主模板无定义时，丢弃分支里的 `Heavy<T>::f()` 不会导致编译失败——这是 `if constexpr` 的全部魔法来源。
- **折叠表达式** — fold expression：`(... op pack)`、`(pack op ...)`、`(... op pack op init)`、`(pack op ... op init)` 四种形态，把一个二元运算符作用到整个参数包。
- **一元折叠与空包** — unary fold & empty pack：`&&` 空包 → `true`，`||` 空包 → `false`，`,` 空包 → `void()`；`+`、`*` 等**没有规定单位元**，空包是硬错误（实测）。
- **二元折叠** — binary fold：带初始值 `init`，空包时结果就是 `init`，所以 `(args + ... + 0)` 对空包合法。
- **字面量作模板参数** — literals as template arguments：`template<auto N>`（见 `05`）让 `Fixed<3>`、`Fixed<'c'>` 直接写字面量；`3` 与 `3L` 是**不同**模板实参（实测）。
- **扩展的 using 声明** — extended using-declarations：C++17 起允许 `using A::f, B::f;`（一条声明多个名字）与 `using Ts::operator()...;`（打包展开）。
- **Overloaded 惯用法** — overload set idiom：继承 + 打包 using 把若干 lambda 合成一个重载集，是 `std::visit` 的标准拍档（见 `08`）。

## 本章地图

| 问题 | 本章的答复 |
| --- | --- |
| 它解决什么 | tag-dispatch/偏特化/递归可变参数这三类「只为分发而写」的样板 |
| 机制 | 常量条件 → 丢弃分支不实例化；折叠 → 编译期把运算符铺满参数包 |
| 边界 | 丢弃分支不是「不编译」：语法、非依赖名字查找仍检查；空包对多数运算符无定义 |
| 权衡 | 可读性大幅提升 vs「模板函数只实例化一条路径」带来的调试/ODR 心智负担 |

## 动机：没有它们之前代码长什么样

```cpp
// 🔧 C++14 时代的两坨经典样板
// 1) 按类型分发：tag dispatch 或全特化
template <typename T> void process(T v, std::true_type)  { /* 整型 */ }
template <typename T> void process(T v, std::false_type) { /* 其他 */ }
template <typename T> void go(T v) { process(v, std::is_integral<T>{}); }
// 2) 递归展开参数包：打印/求和都要「递归出口 + 递归步」两份
void print() {}
template <typename T, typename... Rest> void print(T v, Rest... r) {
    std::cout << v; print(r...);            // 少写一个出口 = 一屏错误
}
```

C++17 之后（**已实测 g++ 15.2 -std=gnu++17**）：

```cpp
template <typename T> void go(T v) {
    if constexpr (std::is_integral_v<T>) { /* 整型分支 */ }
    else                                 { /* 其他分支 */ }
}
template <typename... A> auto sum(A... a) { return (a + ... + 0); }   // 空包→0
template <typename... A> void print(A&&... a) { (std::cout << ... << a) << '\n'; }
```

## 机制与实测证据

### 1. 实例化消除的铁证（编译期 counter）

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17，运行输出原样记录
template <typename T> struct Heavy;                       // 只有特化、没有主模板定义
template <> struct Heavy<int> { static const char* who() { return "Heavy<int> instantiated"; } };
template <typename T> const char* route(T v) {
    if constexpr (std::is_same_v<T, int>) return Heavy<T>::who();
    else { (void)v; return "light branch"; }
}
// 实测输出：route('c') 正常返回 light 分支——Heavy<char> 从未被实例化，链接照过。
```

再配一个运行时计数器：`go(char{})` 走丢弃分支、`go(1)` 走选中分支，实测 `taken=2 dropped=1`（三个调用中两个
触发 `sizeof(T)>4 || sizeof(T)==4`），证明**每个函数特化只有一条路径进入二进制**。

### 2. 丢弃分支里到底什么被免除（三条负例/宽例，全部实测）

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
// (a) 非依赖名字查找不免除：硬错误
template <typename T> void f() { if constexpr (sizeof(T) == 0) { bogusCall(); } }
//    错误原文：there are no arguments to 'bogusCall' that depend on a template parameter,
//              so a declaration of 'bogusCall' must be available [-Wtemplate-body]
// (b) 非模板函数里的 if constexpr：丢弃语句照常检查
int main_ish() { if constexpr (false) { int i = "x"; } }   // 错误原文：invalid conversion from 'const char*' to 'int'
// (c) 依赖条件丢弃分支里的非依赖类型错误：GCC 15 实测【放行】，17/20/23 三档均无诊断
template <typename T> void g() { if constexpr (sizeof(T) == 0) { int i = "not an int"; } }
```

(c) 是**实现分歧点** ⚠️：按严格的检查时点解读，(c) 应报错（MSVC 系实践更严）；本机 GCC 15 接受，
不能据此认为跨编译器安全。另外 `static_assert(false)` 放进丢弃分支：

```cpp
// 🔧 已实测 g++ 15.2：以下两种写法在 -std=gnu++17/20/23 三档全部编译通过
template <typename T> void h() { if constexpr (std::is_same_v<T,int>) { static_assert(false, "x"); } }
template <typename T> void k() { if constexpr (false) { static_assert(false, "x"); } }
```

⚠️ 这是 GCC 的一贯宽松；「`static_assert(false)` 未实例化时也算病句」是旧标准文本下的通行口径，
C++23 由 **P2593R1「Allowing static_assert(false)」**（wg21.link/p2593 实测可达 ✅）正式合法化。

### 3. 折叠：四种形态与空包单位元（实测输出）

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
template <typename... A> bool all(A... a)  { return (a && ...); }     // 一元右折叠
template <typename... A> bool any(A... a)  { return (... || a); }     // 一元左折叠
template <typename... A> void nothing(A... a){ (void(a), ...); }      // 逗号折叠，空包→void()
template <typename... A> auto sum(A... a)  { return (a + ... + 0); }  // 二元右折叠
// 实测：all()=1  all(1,1)=1  all(1,0)=0  any()=0  sum()=0
```

二元与一元的**求值顺序不同**（`(... op a op init)` 左结合、`(a op ... op init)` 右结合），除法/减法结果
可用来自查：`(a / ... / 1)` 与 `(1 / ... / a)` 展开方向相反 ⚠️ 具体展开请打印验证。

负例（实测被 g++ 15.2 拒绝，错误原文）：

```cpp
template <typename... A> auto f(A... a) { return (a + ...); }   // 一元 + 折叠
int main() { return f<>(); }
// error: fold of empty expansion over operator+
```

### 4. 扩展的 using 与 Overloaded

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
struct A { int f(int)   { return 1; } };
struct B { int f(double){ return 2; } };
struct Both : A, B { using A::f, B::f; };       // 一条 using 声明带两个名字
// f(1)=1 f(1.0)=2（实测）——两个签名合成一个重载集
// 若 A::f 与 B::f 签名完全相同：实测诊断 "call of overloaded 'f()' is ambiguous"
template <class... Ts> struct Overloaded : Ts... { using Ts::operator()...; };
template <class... Ts> Overloaded(Ts...) -> Overloaded<Ts...>;   // C++17 必须（见 05 坑 1）
```

档位对照（实测）：

| 写法 | gnu++14 | gnu++17 | gnu++20 |
| --- | --- | --- | --- |
| `using A::f, B::f;` | 错误原文：`comma-separated list in using-declaration only available with '-std=c++17'` | ✅ | ✅ |
| `using Ts::operator()...;` | 本目录最小复现**未报专属错误**（GCC 作扩展放行）⚠️ 严格口径请自行 `-pedantic-errors` 复测 | ✅ | ✅ |
| `Overloaded{...}` 无推导指引 | — | 错误原文：`class template argument deduction failed`（聚合无隐式指引） | ✅（P0960/聚合指引回归） |
| `if constexpr` | 仅警告 `'if constexpr' only available with '-std=c++17'`（GNU 扩展放行）| ✅ | ✅ |

## 权衡

| 决策点 | if constexpr / 折叠 | 老写法（特化/递归） |
| --- | --- | --- |
| 只编译一条路径 | ✅ 丢弃分支不实例化，`Heavy<T>` 无定义也过 | ❌ 全特化都要写出来 |
| 调试 | ⚠️ 断点/堆栈里「没走的那条路」根本不存在 | 函数边界清楚 |
| 错误信息 | 折叠版通常短得多（实测递归版少写出口时报一串候选） | 递归版错误更长 |
| 兼容老编译器 | ❌ 需 C++17 起步（`-std=gnu++14` 实测仅 GNU 扩展放行，跨编译器别赌） | ✅ 全版本可用 |
| 空包健壮性 | 一元 `&&`/`||`/`,` 有单位元；`+` 必须走二元带 0 | 递归版天然安全 |

## 相邻概念对比

- **vs 模板偏特化**：`if constexpr` 是**函数体内**的分发，不产生新符号；偏特化是**类型层面**的整函数替换。分发点少、想让丢弃代码「存在但不编译」→ `if constexpr`。
- **vs C++20 concepts/`requires`**：concepts 把「约束」写进接口（可诊断、可部分排序）；`if constexpr` 只做「选实现」。C++20 里典型组合是 `requires` 选重载 + `if constexpr` 处理细节（见 [../C++20模板元编程.md](../C++20模板元编程.md)）。
- **vs 递归可变参数**：折叠省掉「递归出口」，但**不能**表达「只对第 2 个之后的元素做 X」这类位置逻辑——那仍然需要 `std::tuple` + `std::apply` 或索引折叠 `(f(std::get<I>(t)), ...,)` 的替身（C++20 前用 `std::index_sequence`，见 `12`）。
- **vs `std::apply`**：折叠作用于**实参包**；把 tuple **展开成函数实参**用 `apply`，两者互补（`01` 的结构化绑定是第三种）。

## 最新演进与工业实践

**标准之后**
- **C++20**：聚合 CTAD 恢复，`Overloaded` 可不写指引（实测 gnu++20 无指引通过，见 `05`）；`using` 打包展开不受影响。
- **C++23**：**P2593R1**（✅ 实测可达）把「丢弃分支里的 `static_assert(false)`」合法化，`if constexpr` 写 trait 校验更顺手；折叠本身无改动。
- **C++26**：**P2996「Reflection for C++26」**（wg21.link/p2996 实测可达，当前修订 R13 ✅）落地后，「遍历成员」不再需要折叠 tuple 的样板——序列化库是最大受益方（⚠️ 定稿范围请以 00 的会议口径为准）。

**工业实践与开源口径**
- **`Overloaded` + `std::visit`** 是 `std::variant` 访问的事实标准写法（见 `08`）；Abseil（`abseil/abseil-cpp`，00 当日实测 ≈18.1k★）风格的解析代码、range-v3（`ericniebler/range-v3`）的适配器聚合里大量使用折叠做 `&&`/`,` 检查。
- **fmt**（`fmtlib/fmt`，00 当日实测 ≈25.8k★）在格式化参数处理里用 `if constexpr` 按类型分派编译期格式串，等价于手写 switch-on-type 的特化矩阵。
- 纪律：**丢弃分支里只放「依赖 T 的代码」**；名字查找级错误（实测 (a)）不会因为你加了 `if constexpr` 而消失。

## 常见误区（实测）

1. **「丢弃分支完全不编译」——错**：语法必须合法；非依赖的名字查找照常失败（实测 (a) 硬错误）。
2. **「`if constexpr` 条件运行时也行」——错**：条件必须常量表达式，实测 `if constexpr (someInt)` 被拒（诊断含 `condition is not a constant expression` ⚠️ 原文未逐字留存，形态为字面量要求）。
3. **「`(args + ...)` 空包返回 0」——错**：实测报 `fold of empty expansion over operator+`；0 只属于**二元**折叠 `(args + ... + 0)`。
4. **「`using A::f, B::f;` 在 C++14 也能用」——错**：实测被拒并直接提示需要 `-std=c++17`。
5. **「有了 `if constexpr` 就不再需要偏特化」——不完全对**：类型级别的「按位选择」（如 `std::variant_size` 类 trait）仍是特化/`_v` 的地盘（见 `12`）。

## 与其他章 / 其他笔记的联系

- ← 本目录 `05`：CTAD 与占位类型是本章 `template<auto>`/指引写法的语法地基。
- → 本目录 `08`：`Overloaded` 惯用法在 `std::visit` 处兑现价值；`using Ts::operator()...` 的坑也在那章复现。
- → 本目录 `12`：`_v` 变量模板把 `is_same_v` 这类条件写短，与 `if constexpr` 配套。
- → [../C++模板元编程/08-跨越编译期与运行期边界.md](../C++模板元编程/08-跨越编译期与运行期边界.md)：tag-dispatch 时代的完整样板对照。
- → [../现代C++实战30讲/10-可变模板tuple与类型擦除.md](../现代C++实战30讲/10-可变模板tuple与类型擦除.md)：折叠之前的递归可变参数讲法。
- → [../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)

## 思考题

1. `template<class... T> void f(T... t) { ((void)t, ...); }` 对空包合法吗？换成 `((t + 1), ...)` 再传空包，编译器说什么？（用本章实测口径回答，再在你机器上验证。）
2. 为什么 C++17 的 `Overloaded{...}` 必须配一条推导指引而 C++20 不用？把错误原文贴进你的笔记（提示：`05` 坑 1 + 本章档位表）。
3. 写出「对参数包从左到右做除法、要求至少一个实参」的折叠，并解释 `(a / ... / 1)` 与 `(1 / ... / a)` 哪个是左结合。
