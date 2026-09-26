# 第 5 章（中）编译器是你的同事：UB、Type-Rich 与"了解你的库"

> 英文原章：Chapter 5 的 5.3 The Compiler Is Your Colleague（5.3.1 Automatic Type Deduction /
> 5.3.2 Computations during Compile Time / 5.3.3 Variable Templates）、5.4 Don't Allow Undefined Behavior、
> 5.5 Type-Rich Programming、5.6 Know Your Libraries（5.6.1 Take Advantage of `<algorithm>` /
> 5.6.2 Take Advantage of Boost / 5.6.3 More Libraries That You Should Know About）。
> 原版 p102–123；中译 p102–122。
> 系列导航：[../C++系列·总索引.md](../C++系列·总索引.md) ｜ 单文件大纲：[../C++代码整洁之道.md](../C++代码整洁之道.md) ｜ 返回：[00-总览与阅读地图.md](00-总览与阅读地图.md)

## 核心概念速览（中英对照）

- **自动类型推导** — Automatic Type Deduction：`auto`/`decltype` 让类型由表达式给出，减少噪音且防失配（5.3.1）
- **编译期计算** — Computations during Compile Time：`constexpr` 函数/对象把执行搬到编译期（5.3.2，L5-16 阶乘）
- **变量模板** — Variable Templates：`template<typename T> constexpr T pi_v`（C++14；L5-17/L5-18 求圆周长）
- **字面类型** — Literal Type：可在常量表达式中使用的类型；`constexpr` 类（L5-19 `Rectangle`）的前提
- **未定义行为** — Undefined Behavior（UB）：标准不承诺后果的一切写法；"编译器同事"在这里帮不了你（5.4）
- **诊断覆盖** — Diagnostic Coverage：`-Wall -Wextra -Wshadow -Wformat` 能抓的只是 UB 的一个子集（本文件实测）
- **富类型编程** — Type-Rich Programming：把领域约束编码进类型，让非法状态无法表示（5.5）
- **量纲/单位类型** — Dimensioned Type：`Quantity<M,KG,S>` 模板参数即量纲指数（L5-20/L5-21，作者给出的招牌例子）
- **强类型枚举** — `enum class`：不隐式转整型、不泄漏枚举数（5.5 现代立场）
- **不透明别称** — Opaque Alias：`using CustomerId = ...` 只是起点，`strong_type`/包装结构才阻断混用
- **了解你的库** — Know Your Libraries：先用标准库/Boost 再自己写（5.6）
- **算法库优先** — Take Advantage of `<algorithm>`：`std::sort/find/copy/count_if/transform/accumulate` 替代手写循环（5.6.1，L5-22…L5-26）
- **Boost** — Boost：`optional/variant/string_ref/range/filesystem` 等在进入标准之前的过渡地位（5.6.2）
- **Range-v3 / libcds** — 5.6.3 点名的两个第三方库：Eric Niebler 的 range 库、Max Khizhinsky 的无锁并发容器库

## 1. 动机：把"检查"从人转移到机器

这三节共享一个论点：**能被机器检查的错误，就不该由人眼发现**。
5.3 让机器多算（推导 + 编译期求值），5.5 让机器多判（类型系统挡住非法状态），5.6 让人少写（复用经过验证的实现）。
5.4 则是这条论点的反面教材区：**UB 是机器拒绝帮忙的领域**——所以它的对策不是更聪明的类型，
而是纪律（少用低层设施）+ 外部工具（sanitizer，本书时代尚无广泛可用的 sanitizer）。

作者把 `auto` 的正当性说得很克制（5.3.1）：它不是为了少打字，而是为了**消除类型失配**
（迭代器类型手写出错是 2010 年代 C++ 的日常）与**强迫使用 `const auto&` 而非误抄值类型**。

## 2. 机制：三层"机器可判定"

1. **推导层**：`auto x = f()` 保证类型与返回一致；范围 for 里 `for (const auto& e : c)` 避免切片与拷贝。
2. **求值层**：`constexpr` 函数既能编译期跑也能运行期跑（L5-16 阶乘、L5-19 `constexpr` 类）；
   变量模板（L5-17 `pi_v<T>`）替掉宏常量（呼应 4.4.5），并保证按类型正确精度（`pi_v<float>` vs `pi_v<double>`）。
3. **判决层（Type-Rich）**：5.5 的招牌是 `Quantity<M,KG,S>`（L5-20/21）——**量纲作为模板参数**，
   于是"米 + 秒"在过载解析阶段就无解可匹配，编译失败。同节还包括 `enum class`、强别称、
   用 `std::optional<T>` 表示"可能没有"而不是返回哨兵值。

5.6 的机制是"查找优先于编写"：`std::sort`/`std::find_if`/`std::count_if`/`std::equal`（L5-24/25/26 给出对照），
Boost/range-v3 处理标准库留白（作者特别推荐 range-v3 以省下 `std::begin(c), std::end(c)` 的杂耍）。

## 🔧 实测（已实测 g++ 15.2）

**(1) 编译期计算与变量模板**（`-std=gnu++17 -Wall -Wextra`）：

```text
编译期斐波那契表: 0 1 1 2 3 5
pi_v<double>=3.14159265358979  pi_v<float>=3.141593
is_numeric_v<int>=1 is_numeric_v<std::string>=0
-1 < 1u ? false   （int 与 unsigned 比较的整型提升陷阱）
```

`static_assert(ipow(2,10)==1024)` 与 `constexpr std::array<int,6>` 表在编译期成型；同一份代码 `-O0/-O2` 输出一致
（因为结果早已不是运行期算的）。

**(2) 诊断覆盖有限，但比没有强**：同一程序编译时编译器顺手抓到两处典型陷阱：

```text
warning: comparison of integer expressions of different signedness: 'int' and 'unsigned int' [-Wsign-compare]
warning: integer overflow in expression of type 'int' results in '-294967296' [-Woverflow]
```

注意第二条：`2000000000 + 2000000000` 这类**常量折叠阶段的有符号溢出**会被 `-Woverflow` 报出；
一旦操作数是运行期值，同样的 UB 编译器通常沉默。

**(3) UB 的沉默：memcpy 误用侥幸正确。** 按 5.4 精神构造的对照实验（`-std=gnu++17 -O2 -Wall -Wextra`）：

```text
memcpy(&array) -> 10 20
memcpy(array.data()) -> 10 20
```

**两者输出相同**——这正是要如实记录的地方：`std::memcpy(dst, &a, sizeof(a))`（传数组对象地址而非首元素地址）
在 libstdc++/MinGW 的 `std::array` 布局上与正确写法偶然一致，**没有任何诊断**，但在别的实现/别的容器上会读到垃圾。
书里那句"不允许未定义行为"的真实含义是：**UB 的代价通常不在今天，也不在这里**。

**(4) Type-Rich 的红利：非法状态在编译期消失。** 只给同量纲定义 `operator+` 之后：

```text
error: no match for 'operator+' (operand types are 'Meter' {aka 'Quantity<1, 0, 0>'} and 'Second' {aka 'Quantity<0, 0, 1>'})
```

而用 `int` 表达同样两个量：`已实测 g++ 15.2` 输出 `把米和秒直接相加 = 109`——**安静地错**。
一次实测运行也给出富类型的表达力上限：`100m / 9.58s = 10.438 m/s`（量纲在除法中自动合成 `Quantity<1,0,-1>`）。

**(5) GCC 诊断本身已是"同事"**：写漏 `#include <optional>` 时 GCC 15 直接给出

```text
note: 'std::optional' is defined in header '<optional>'; this is probably fixable by adding '#include <optional>'
```

2017 年的编译器还没有这种"补丁建议级"诊断；今天它把 5.3 的"编译器是同事"从修辞变成默认体验。

## 3. 权衡

- **`auto` 的代价是可见性**：`auto v = map[0]` 与 `auto rc = f()` 把关键类型藏起来；接口层（头文件里的公开函数返回类型）
  仍应显式。作者的立场是"实现里大胆用、接口上写清楚"。
- **`constexpr` 不是免费**：编译期执行受"常量表达式步骤上限"约束，复杂计算显著拉长编译时间；
  且 `constexpr` 函数在 C++17 时期限制比今天多（不能随意用 `throw`/`new`/虚函数）。
- **Type-Rich 的成本是模板报错**：量纲写错时报的是重载解析失败（如实测 (4)），对新人不友好；
  C++20 concepts 把这类错误前移为**约束不满足**的明确说明（相邻节已引）。
- **Boost 的历史地位变化**：本书列的 Boost 组件（`optional/variant/string_ref/filesystem`）大多已进入标准（C++17）——
  **今天"用 Boost"的默认理由减弱**，剩下的是 Boost.Asio/JSON/Multi-index 等标准尚无等价物的领域。
- **`<algorithm>` 优先 vs 可读性**：`std::for_each` + lambda 有时比范围 for 更难读；作者给的判据是
  "能用命名算法表达意图就用"，而不是"永远别写循环"。

## 4. 相邻概念对比

| 概念对 | 差别 | 为什么容易混 |
| --- | --- | --- |
| `const auto&` vs `auto` | 前者借用、避免拷贝与切片；后者取值（对 `std::vector<bool>` 代理还会取到临时位） | 范围 for 里 `auto` 拷贝整元素是性能与语义双重事故 |
| `constexpr` 函数 vs 模板元编程（TMP） | `constexpr` 是"普通函数可被编译期求值"；TMP 靠模板特化/偏特化模拟计算 | 旧 TMP 写法（L5-3 式阶乘模板）在 C++17 后应优先由 `constexpr` 递归替代 |
| 宏常量 vs 变量模板 | 变量模板有类型、有作用域、可重载、可调试；宏只是文本 | `#define PI 3.14` 的类型是 `double`，浮点后缀靠运气 |
| 强类型（量纲/枚举） vs 校验（运行期断言） | 前者让非法状态**不可表示**，后者允许表示但拒绝进入 | 团队常二者混用；判据：非法值是否来自外部输入（外部输入必须运行期校验） |
| UB vs 实现定义行为 | UB 什么都不保证；实现定义行为有文档化实现选择（可移植性受限但可测） | 把"在我机器上没问题"当证据是 UB 的常规死法（本文件实测 (3) 即样本） |
| 标准库 vs Boost vs 手写 | 优先级：标准库 → 成熟第三方 → 手写（5.6 的次序） | 手写"自己的排序/智能指针/字符串"是熵的最大来源之一 |

## 最新演进与工业实践

- **C++20/23 对位**：
  - **concepts**（C++20）把 5.5 的"用类型表达约束"工程化：`template<std::integral T>`、`ranges` 的
    `std::ranges::sort`（约束检查错误信息远好于 SFINAE 时代）。提案 wg21.link/P0898 ⚠️（标题复核未成功，仅确认链接存在）。
  - **ranges**（C20）落地了作者推荐 range-v3 的官方版本；`std::views::filter/transform` 让 5.6.1 的
    "算法优先"变成"管道优先"，也让他点名的 range-v3 变成历史角色。
  - **`std::expected`**（C++23，wg21.link/P0323，实测标题 *std::expected*，R12）替代"返回哨兵值"，
    与 `optional` 共同构成 Type-Rich 的错误处理出口（详见 [08-异常与错误处理.md](08-异常与错误处理.md)）。
  - **`std::format`/`std::print`**（wg21.link/P0645 *Text Formatting* / P2093 *Formatted output*）把 5.6 的"用库"
    落到最日常的输出场景。
  - **`std::to_underlying`、`[[assume]]`、`std::start_lifetime_as`**（C++23）进一步压缩"必须靠 reinterpret 的黑区"，
    与 5.4 的精神一致。⚠️ 该组未给提案号，按标准版本口径引用。
- **工具接管（本机实测边界）**：GCC 15 的 `-Wall -Wextra` 已覆盖 sign-compare/shadow/overflow/return-local-addr/catch-order；
  **但本机 MinGW 无 libasan 也无 libubsan**（`-fsanitize=undefined` 链接期 `cannot find -lubsan` 实测失败）——
  5.4 提到的 UB 在本机只能靠"编译期诊断 + 代码纪律 + 第三方 CI（MSVC `/fsanitize` 或 WSL 下 GCC）"。
- **clang-tidy 对应项**（⚠️ 本机未装，按上游文档口径）：`bugprone-*` 家族是 5.4 的直接对位
  （`bugprone-narrowing-conversions`、`bugprone-suspicious-stringview-data-usage`、`bugprone-unsafe-functions`、
  `bugprone-misplaced-widening-cast`）；`modernize-use-constexpr`、`modernize-use-using`（替 typedef/宏）、
  `performance-*`（`performance-unnecessary-copy-initialization` 正是 `auto` 误用的捕手）。
- **工业仓库**：fmt（`std::format` 的上游与长期超集，`FMT_CONSTEXPR` 把编译期检查做到极致）、
  abseil（`absl::Status`/`absl::string_view` 的过渡史恰好证明"标准吸收第三方库"这条路径）、
  range-v3（作者点名的库，今天仍是 `std::ranges` 未覆盖特性的试验场）、
  `strong_type`（rollno/strong_type 一类富类型库，把 5.5 变成几行依赖）。
- **测试生态**：Type-Rich 的最大红利是**测试数量下降**——非法组合不再需要"负例测试"（它编译不过），
  测试只需覆盖合法状态空间；这条变化在 Catch2/doctest 的参数化测试里体现得最清楚。

## 与相邻章/相邻书的互链

| 主题 | 去处 | 关系 |
| --- | --- | --- |
| 资源与移动 | [06-资源管理-RAII智能指针与Move.md](06-资源管理-RAII智能指针与Move.md) | 本章前一节 |
| 异常与错误处理 | [08-异常与错误处理.md](08-异常与错误处理.md) | Type-Rich 在"可失败函数"上的收口 |
| 函数式与算法管道 | [10-函数式编程.md](10-函数式编程.md) | 5.6.1 的下一步就是 ranges |
| `constexpr`/TMP 技术细节 | [../C++模板元编程/00-总览与阅读地图.md](../C++模板元编程/00-总览与阅读地图.md)、[../C++20模板元编程/00-总览与阅读地图.md](../C++20模板元编程/00-总览与阅读地图.md) | 机制层的深水区 |
| C++17 特性本体 | [../C++17完全指南/06-constexpr-if与折叠表达式.md](../C++17完全指南/06-constexpr-if与折叠表达式.md)、[../C++17完全指南/09-string_view.md](../C++17完全指南/09-string_view.md) | 本书"库"节的现代答案 |
| UB 与调试工具链 | [../C++代码调试的艺术/00-总览与阅读地图.md](../C++代码调试的艺术/00-总览与阅读地图.md) | sanitizer 在本平台的现实路线 |
| 规则编号版对照 | [../C++CoreGuidelines解析/08-表达式和语句.md](../C++CoreGuidelines解析/08-表达式和语句.md) | Type-Rich/UB 的条款化表述 |

导航：上一级 [00-总览与阅读地图.md](00-总览与阅读地图.md) ｜ 上一章 [06 资源管理](06-资源管理-RAII智能指针与Move.md) ｜ 下一章 [08 异常与错误处理](08-异常与错误处理.md) ｜
单文件版 [../C++代码整洁之道.md](../C++代码整洁之道.md) ｜ 系列 [../C++系列·总索引.md](../C++系列·总索引.md)
