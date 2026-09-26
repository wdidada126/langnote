# 04 lambda 扩展、新属性与其他语法变化

> 覆盖原书 **Part I 第 6–8 章**：Lambda Extensions and Improvements / New Attributes / Miscellaneous Changes。
> 这一组特性没有「新抽象」，全是把 lambda 与声明语法上原本「差一点就够用」的缺口补平。
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)

## 核心概念速览（中英对照）

- **constexpr lambda** — constexpr lambda：无捕获（或捕获 constexpr 友好）的 lambda 自动满足 constexpr 要求，可进常量表达式。
- **捕获初始化（init-capture）** — init-capture `[p = std::move(q)]`：C++14 引入、C++17 补齐 `[*this]`，是移动捕获的唯一手段。
- **按值捕获 `*this`** — `[*this]` capture：显式拷贝当前对象进闭包，替代 `[=]` 只拷指针带来的悬垂风险。
- **属性说明符序列** — attribute-specifier-seq：`[[nodiscard]]`、`[[maybe_unused]]`、`[[fallthrough]]` 三个新标准属性。
- **弃用标注** — `[[deprecated("msg")]]`：把「别再用」写进声明，让诊断代替文档。
- **嵌套名字空间定义** — nested namespace definition：`namespace a::b::c { }`。
- **属性在 lambda 上的位置** — attribute placement：实测只能写在**捕获列表之后、参数列表之前**，写在捕获列表前是语法错误。
- **constexpr 构造/隐式 constexpr** — implicitly constexpr constructors：C++17 放宽常量对象的构造条件（本章点到，详见 `03`）。

## 本章地图

| 小节 | 补的缺口 | 关键 API/语法 |
| --- | --- | --- |
| 4.1 lambda | 不能 constexpr、不能移动捕获、`[=]` 语义暧昧 | `constexpr auto f = []{...}`、`[p = std::move(p)]`、`[*this]` |
| 4.2 属性 | 意图只能写注释，工具无从诊断 | `[[nodiscard]]` `[[maybe_unused]]` `[[fallthrough]]` `[[deprecated]]` |
| 4.3 其他语法 | 名字空间层级冗长、`auto` 用法零碎 | `namespace a::b`、属性可用于名字空间/using 声明 |

## 4.1 lambda 的四项补强

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17 编译并运行（输出 g=6 / h=8 s.v=7 / 101）
// (1) constexpr lambda：可直接用于常量表达式
constexpr auto twice = [](int x) { return x * 2; };
static_assert(twice(21) == 42, "constexpr lambda 进入常量求值");
std::array<int, twice(3)> arr{};                 // 用作数组维度
static_assert(arr.size() == 6);

// (2) init-capture：把值「移动」进闭包
auto up = std::make_unique<int>(5);
auto g = [p = std::move(up)]() { return *p + 1; };   // 闭包独占所有权

// (3) [*this]：拷贝当前对象，回调/异步里不再怕对象先死
struct S { int v = 1; auto m() { return [*this]{ return v + 100; }; } };
S s;  s.m()();                                      // 闭包持有 s 的副本

// (4) 仍可普通按值捕获（注意 s.v 不受影响）
struct T { int v = 7; };
T t; auto h = [c = t]() mutable { c.v += 1; return c.v; };   // h()=8，t.v 仍是 7
```

**同一段代码在 `-std=gnu++14` 下的实测差异**（说明档位边界）：
- `constexpr auto f = [](int x){...};` → **硬错误**：`the type 'const main()::<lambda(int)>' of 'constexpr'
  variable 'f' is not literal` + `non-constant condition for static assertion`。
- `[*this]` → 只是警告：`'*this' capture only available with '-std=c++17' or '-std=gnu++17'
  [-Wc++17-extensions]`，GNU 扩展模式仍放行。

### `[=]` 的暧昧与后续

`[=]` 捕获的是 `this` 指针（不是对象副本），于是「把 lambda 存进队列、对象析构后再执行」= 悬垂。
C++17 给了 `[*this]` 这个明确选项；C++20/23 把「隐式捕获 `this` 的 `[=]`」列为 **deprecated**——
**已实测 g++ 15.2 的档位差异**（同一句 `return [=]{ return v; };`，`-Wall -Wextra`）：
`-std=gnu++17` 无任何诊断；`-std=gnu++20` 与 `-std=gnu++23` 给出
`warning: implicit capture of 'this' via '[=]' is deprecated in C++20 [-Wdeprecated]`。

这正是 C++17 项目的隐蔽处：**警告只在 C++20 及以后出现**，纯 C++17 代码库里编译器不会提醒你，
迁移只能靠人查。建议一律写 `[=, this]`（显式指针捕获）或 `[*this]`（拷副本）。

## 4.2 三个新属性 + 一个老属性的新用法

```cpp
// 🔧 已实测 g++ 15.2 -std=c++17 -Wall 通过；诊断（原样抄自编译器输出）：
//   warning: ignoring return value of 'int compute()', declared with attribute 'nodiscard' [-Wunused-result]
//   warning: 'Old' is deprecated: 用 NewThing 代替 [-Wdeprecated-declarations]
[[nodiscard]] int compute() { return 42; }                    // 返回值不可丢
[[deprecated("用 NewThing 代替")]] struct Old {};              // 弃用带信息
enum class Color { Red, Green };
[[maybe_unused]] constexpr Color kUnused = Color::Green;      // 未使用也不警告（调试期常量常用）
int step(int i) {
    switch (i) {
        case 0: [[fallthrough]];                              // 明示「我就是想贯穿」
        case 1: [[fallthrough]];
        case 2: return i + 1;
        default: return i;
    }
}
```

**属性位置的实测（很容易写错）**：

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
auto f = [[maybe_unused] v = s](){ return 1; };     // ❌ error: expected identifier before '[' token
auto g = [v = s] [[maybe_unused]] () { return v.v; };  // ✅ 通过（属性在捕获列表之后）
```

**`[[nodiscard]]` 用于类型与成员函数**（实测）：`struct [[nodiscard]] Handle` 与
`[[nodiscard]] int get() const` 在 `-std=gnu++17` 和 `-std=gnu++20` 两个档位下，g++ 15.2 **都会**在丢弃
返回值时报 `-Wunused-result`。⚠️ 标准层面「成员/协程/结构体上的 nodiscard」的适用范围在 C++20 才补齐；
`[[nodiscard("带消息")]]` 形式在本机连 `-std=c++17 -pedantic-errors` 都**不报错**（实测只有
`-Wunused-result` 警告），即 GCC 把它当扩展放行——别据此认为所有 C++17 实现都支持。

## 4.3 其他语法变化

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17（含 static_assert 与 inline namespace 验证）
namespace a::b::c { constexpr int v = 1; }      // 嵌套名字空间定义（C++17）
static_assert(a::b::c::v == 1);
namespace alias = a::b;                          // 名字空间别名（C++11 起，不是 C++17 新东西）
namespace x { inline namespace v1 { struct S { int k() { return 1; } }; } }
x::S s;                                           // inline namespace 让 v1::S 直接以 x::S 出现
```

原书 Ch8 的其他条目（多数与库相关）在本目录另有归处：`_v` 后缀与 `void_t` 见 `12`，
`std::shared_mutex`/`std::scoped_lock` 见 `12`，`if constexpr` 与折叠见 `06`。

## 权衡

| 选择 | 好处 | 代价 |
| --- | --- | --- |
| `[*this]` vs `[=]` | 闭包自持数据，异步安全 | 拷贝成本、与 `mutable` 语义叠加后易误解「改的是副本」 |
| `[p = std::move(q)]` | 唯一能表达「闭包独占所有权」的写法 | 名字要与被捕获量区分，递归/共享时要 `std::function` 包一层 |
| `[[nodiscard]]` 广撒 | API 误用当场报错/告警 | 老库升级时会把调用方的既有「故意丢弃」变成噪音；通常配 `(void)` 或 `[[maybe_unused]]` |
| `[[fallthrough]]` | 抑制 `-Wimplicit-fallthrough` 噪音 | 只写属性仍易漏；团队常强制要求伴随 `// fall through to X` 注释 |

## 相邻概念对比

- **constexpr lambda vs `constexpr` 函数**：前者是闭包类型的 `operator()` 满足 constexpr 条件，
  捕获了非 constexpr 可用对象就不再是常量表达式；不要指望「有 constexpr 关键字就一定能常量求值」。
- **init-capture vs 显式捕获**：`[x]` 拷贝现有名字，`[x = expr]` 新建一个闭包成员；后者才能移动、才能造新名字。
- **属性 vs 编译器扩展 `__attribute__`**：标准属性可移植但表达能力弱；GCC 的 `__attribute__((...))`
  在本章示例里**未被使用**（`-Wattributes` 对未知标准属性保持沉默，见 `12`）。
- **嵌套名字空间 vs C++20 点号名字空间**：`namespace a::b::c {}`（C++17）与 `namespace a.b.c {}`（C++23 ⚠️
  该语法是否最终进入 C++23 未核实，勿在生产代码依赖）。

## 最新演进与工业实践

**标准之后**
- **C++20**：模板 lambda `[]<class T>(T x){}`（P0624R2 ⚠️ 编号未逐字核实）。实测档位细节：
  `-std=gnu++17` **静默放行**（GNU 扩展），`-std=c++17 -pedantic-errors` 报
  `error: lambda templates are only available with '-std=c++20' or '-std=gnu++20' [-Wc++20-extensions]`；
  `[=, this]` 明确写法成为 `[=]` 的推荐替代；`[[likely]]`/`[[unlikely]]`
  （P0478R5 ⚠️ 编号未核实，实测 `-std=c++17` 下被忽略、`-std=c++23` 接受）、`[[no_unique_address]]`
  （EBO 的语言化）加入。
- **C++23**：`[[assume]]`（实测 `-std=c++17` 下被 g++ 15.2 **静默忽略**，`-std=gnu++23` 接受并生效）、
  `[[nodiscard]]` 可携带消息（实测 C++20/23 均可）。
- **C++26**：反射相关提案会改变「属性驱动的代码生成」生态，但对 lambda/属性语法本身无破坏 ⚠️。

**工业实践与开源口径**
- **`fmtlib/fmt`（实测 ≈25.8k★）**：格式化 API 全面 `[[nodiscard]]`，并把「丢弃格式化结果」当成
  明确的误用信号；这也是把 `[[nodiscard]]` 引入自有 API 时可参照的样板。
- **Abseil（实测 ≈18.1k★）**：`absl::` 里大量 `[[nodiscard]]` + `[[maybe_unused]]` 组合，
  并用 `ABSL attributes` 宏兼容 C++11/14 编译期——迁移期项目的标准做法是**属性也要有宏包装层**。
- **`range-v3`（实测 ≈4.4k★）**：其 `views` 管道全靠 lambda/闭包 + constexpr 设施；C++17 的 constexpr lambda
  是这类库能在纯标准库里落地的前提之一。
- **`neargye/magic_enum`（实测 ≈6.2k★）**：用 `__PRETTY_FUNCTION__` 做反射，与本节属性的「可移植诊断」形成
  互补——标准属性管「意图声明」，反射库管「信息提取」。

**迁移与评审清单**
1. 所有「返回错误码/句柄/布尔成功标志」的函数加 `[[nodiscard]]`；先在一个模块试，观察噪音再推广。
2. 所有把 lambda 存起来（回调、线程、队列）的 `[=]` 检查是否为 `this` 捕获，改 `[*this]` 或 `[x = ...]`。
3. `-Wall -Wextra` 之外，把 `-Wswitch-default`/`-Wimplicit-fallthrough` 打开，让 `[[fallthrough]]` 有对手。
4. 别用 `[[assume]]` 等 C++23+ 属性写 C++17 代码——**实测它是被静默忽略而不是报错**，
   这类「属性拼错/超前」没有诊断保护，是隐藏最深的坑（见 `12` 同类讨论）。

## 与其他章 / 其他笔记的联系

- ← 本目录 `03`：lambda 的捕获与「就地构造」共同决定闭包里到底有什么对象。
- → 本目录 `05`：`Overloaded{f1, f2}` 惯用法 = lambda 集 + CTAD，两个特性都要到位才可用（实测结论见 `05`）。
- → 本目录 `06`：`[=](auto x){ if constexpr (...) }` 是泛型 lambda 与编译期分支的组合拳。
- → 本目录 `12`：`[[nodiscard]]` 在 `to_chars`/`from_chars`、`filesystem` 错误码重载上的实战意义。
- → [../现代C++实战30讲/09-函数对象lambda与函数式编程.md](../现代C++实战30讲/09-函数对象lambda与函数式编程.md)：
  lambda 从 C++11 起的完整演化与闭包类型细节。
- → [../C++标准库/06-函数对象与Lambda.md](../C++标准库/06-函数对象与Lambda.md)：同一作者的 lambda/函数对象基线讲法。
- → [../C++代码整洁之道.md](../C++代码整洁之道.md)：属性作为「让机器帮你守住风格」的手段。

## 思考题

1. `[*this]` 捕获后在 lambda 里修改成员，会不会影响原对象？`mutable` 在这里起什么作用？（4.1 的实测已给答案。）
2. 为什么 `auto f = [[maybe_unused] x = 1](){...};` 是语法错误而 `auto f = [x = 1] [[maybe_unused]](){...};` 合法？
   从「lambda 表达式的语法产生式」回答。
3. `-std=c++17` 下写 `[[assume(x > 0)]]` 会发生什么？为什么这种「无诊断的沉默」比报错危险？
