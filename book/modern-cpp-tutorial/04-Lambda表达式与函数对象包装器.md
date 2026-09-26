# 04 · Lambda 表达式与函数对象包装器

> 系列导航：[C++ 系列·总索引](../C++系列·总索引.md) · [《现代 C++ 教程》单文件](../modern-cpp-tutorial.md) · [00 总览与阅读地图](./00-总览与阅读地图.md)
>
> 覆盖原书：第 3 章 §3.1 Lambda 表达式（基础：值捕获/引用捕获/隐式捕获/表达式捕获；泛型 Lambda）、§3.2 函数对象包装器（`std::function` / `std::bind` 和 `std::placeholder`）（`book/zh-cn/03-runtime.md`，标题逐字）。

## 一、动机：把"函数"变成一等公民

C++98 里"能传的东西"和"能调用的东西"是两套体系：

- 函数指针：简单、可内联，但**不能带状态**；
- 函数对象（重载 `operator()` 的类）：能带状态，但每个回调要手写一个 struct；
- `std::bind1st/bind2nd` 等适配器：表达力残缺，C++11 直接弃用。

Lambda 把前两者合并：**语法是函数，本质是编译器生成的闭包类**——捕获列表就是构造函数参数，`mutable` 决定 `operator()` 是否 const。`std::function` 则解决"统一容器"问题：函数指针、闭包、成员函数绑定体类型各异，需要一个类型擦除的包装器把"可调用性"变成一种值类型。`std::bind` 是"部分应用"的语言层答案（占位符 `_1.._N`），历史地位与 lambda 高度重叠——这直接决定了本章的现代重估结论。

## 二、机制：逐条拆开

### 2.1 闭包类型的四条规则（原书分散讲，这里收拢）

1. 每个 lambda 生成**唯一**的未命名类类型（闭包类型），它的每个实例是闭包对象；
2. 空捕获的 lambda 可隐式转成函数指针——原书 `functional(f)` 示例展示了形参写函数类型 `foo` 时实参退化/转换为 `foo*` 的一条龙；
3. 默认 `operator()` 是 const——值捕获成员只读，`mutable` 解锁写；
4. 捕获发生在**创建时**而非调用时——原书值捕获示例：`value=1` 时创建 lambda，随后把外部 `value` 改成 100，调用仍返回 1。

### 2.2 四种捕获形态

- `[]`：不捕获，纯函数体；
- `[a, b]`：显式值捕获清单；
- `[&]`：按函数体**用到的**名字隐式引用捕获；
- `[=]`：按函数体用到的名字隐式值捕获。

原书 2026 修订版特意强调 `[&]`/`[=]` 的捕获集"从函数体内的使用确定"——这正是工业规范反对裸 `[&]`/`[=]` 的原因：函数体一改，捕获集静默漂移，悬垂风险不可见。

### 2.3 表达式捕获与泛型 Lambda（C++14 双子星）

- 表达式捕获（init-capture）：`[v2 = std::move(important)]` 允许任意表达式初始化捕获成员，类型按 auto 规则推导——它把"独占指针移动进闭包"从不可能变成一行；
- 泛型 lambda：形参写 `auto`，闭包类型的 `operator()` 变成**成员模板**，一份 lambda 覆盖全部实参组合；
- 两者同属 C++14，原书例 `[out = std::ref(x)](auto&& ...)` 已把 vararg+转发引进闭包（教程的"提前量"风格）。

### 2.4 std::function 与 std::bind

- `std::function<R(Args...)>`：持有目标的可调用包装器，可拷贝、可空（`operator bool`）；类型擦除意味着堆分配与小对象优化并存、调用路径含间接跳转；赋值 `nullptr` 即置空。
- `std::bind(f, _1, 1, 2)`：返回存储了拷贝的参数包对象，占位符下标决定调用实参去向；对参数做 decay-copy 存储，想保引用必须 `std::ref`——语义细节多，出过错的读者不少。

### 🔧 实测：表达式捕获 + 泛型 lambda 的 C++14 档位（复现原书 §3.1.4 例）

```cpp
#include <cstdio>
#include <memory>
#include <utility>
int main() {
    auto important = std::make_unique<int>(3);
    auto add = [v1 = 1, v2 = std::move(important)](auto x, auto y) -> int {
        return x + y + v1 + (*v2);
    };
    std::printf("add(1,2) = %d\n", add(1, 2));  // 1+2+1+3 = 7
}
```

已实测 g++ 15.2：`-std=c++11` → 第一道墙是 `error: 'make_unique' is not a member of 'std'`（原书代码隐含 C++14 依赖，示例本身混用两档特性——教程的"混合档位"陷阱）；把 make_unique 换掉后 C++11 仍会在 `v2 = std::move(...)` 处报 "lambda capture initializers only available with '-std=c++14'"；`-std=c++14` → 通过，输出：

```text
add(1,2) = 7
```

### 🔧 实测 b：闭包语义四连 + bind 求值时刻 + move_only_function 收官（g++ 15.2）

```cpp
int value = 1;
auto by_value = [value] { return value; };
auto by_ref   = [&value] { return value; };
value = 100;                                   // 创建之后改外部
auto counter = [c = 0]() mutable { return ++c; };  // init-capture + mutable 状态机
auto g = std::bind([](int x) { printf("bound call sees x=%d\n", x); }, noise());
std::function<int(int)> fact = [&](int n) { return n <= 1 ? 1 : n * fact(n - 1); };
```

已实测 g++ 15.2（`-std=gnu++14`），输出逐行对应机制：

```text
by_value=1 by_ref=100 (outer value=100)
counter: 1 2 3
noise() evaluated NOW
-- bind() returned, target NOT yet called --
bound call sees x=42
fact(5)=120
owned()=7, p null now? 1
```

- `by_value=1`：捕获发生在**创建时**，闭包成员是快照——原书示例的机器复现；
- `counter: 1 2 3`：`mutable` 把 `operator()` 的 const 拿掉后，闭包成员就成了合法状态槽——这就是"无类名的类如何带可变态"；
- **bind 求值时刻铁证**：`noise()` 在 `bind(...)` 返回**之前**就打印（输出顺序实锤）——bind 存储的是 decay-copy 的结果而非"调用时再算"的延迟表达式，与 lambda `[x = f()]` 每调用一次算一次的直觉完全不同；想要延迟求值，唯一正解是把 `f()` 写进 lambda 体。
- `owned()=7, p null=1`：`[q = std::move(p)]` 让闭包成为 `unique_ptr` 的唯一主人——C++11 时代这必须靠 `std::shared_ptr` 或裸 new 绕路。
- 对照实验（延迟求值）：lambda 体里调 `make_p()` 则**每次调用各算一次**（实测输出两行 `make_p() called` 跟在两行 body 提示之后），bind 存储则是"bind 时刻一次算完"——同一个 `f()` 调用点，两种语义天壤之别。
- 值捕获只读性的编译器原话：在 `[v]{ v += 1; }` 处报 `error: assignment of read-only variable 'v'`——"`operator()` 默认 const"不是抽象说法，是成员变量层面的 const。

C++23 收官实测（同机 `-std=gnu++23`）：`std::move_only_function<int()> f = [q = std::make_unique<int>(9)] { return *q; };` 编译通过、移动后源置空（`move_only_function=9, moved-from empty=1`）；而把同款闭包塞进 `std::function` 则命中 libstdc++ 的定点诊断：

```text
error: static assertion failed: std::function target must be copy-constructible
```

——"std::function 要求可拷贝"这条二十年老规约最终以新增类型而非废除旧类型的方式解决（`function.h` 直接 `static_assert` 拦在构造函数，报错质量远好于旧时代"实例化深处几十行"的传说）。

## 三、权衡与陷阱

- **值捕获 vs 引用捕获的生死线**：异步/延迟执行（线程池、回调注册）里，引用捕获栈变量 = 定时炸弹；同步算法（sort 的比较器）里，值捕获拷贝反而白付钱。
- **`[=]` 捕获的是 `this` 指针而非成员本身**——这一经典陷阱在 C++20 被标记为弃用方向（须显式写 `[=, this]`）；教程未讲这条后续，见演进节。
- **`std::function` 的成本三连**：构造可能堆分配、调用无法内联、拷贝深复制闭包；热路径用模板参数（编译期多态）或 `function_ref` 类非拥有引用。
- **`std::bind` 已输掉竞争**：同样的部分应用，lambda 可读、可内联、可显式控制捕获方式；bind 的参数包还会把实参求值提前到 bind 调用时刻（而非目标调用时刻），与直觉相反。
- **递归 lambda**：`std::function` 自引用是经典绕法；C++23 显式对象形参给出正解（见 12 篇）；教程止步于"别扭但可行"。
- **mutable 的真实用途很窄**：给闭包内计数器/缓存留写口；用它修改值捕获的"本应冻结"状态多半是设计信号。

## 四、与相邻概念对比

| 维度 | 函数指针 | Lambda（空捕获） | `std::function` | `std::bind` 结果 |
|---|---|---|---|---|
| 携带状态 | 无 | 无（可转函数指针） | 有（类型擦除） | 有（存储 decay-copy） |
| 可拷贝/可空 | 可/可 | 可/否 | 是/是 | 是/否 |
| 内联友好 | 高 | 高 | 低 | 低 |
| 现代推荐 | 简单回调用 | **默认选择** | 需要存储+异构时 | 基本弃用 |

- 对比 C++11 前夜：`boost::lambda`/`boost::bind` 是同一问题的第三方答案——std 化后 boost 版即退出主流视野，这是第 8 章正则"去 Boost 化"叙事的可复制样本。

## 核心概念速览（中英对照）

- **闭包类型 / 闭包对象** — closure type / closure object：lambda 生成的未命名类与其实例
- **捕获列表** — capture list：`[]` 内声明的外部名字进入闭包的方式
- **值捕获 / 引用捕获** — capture by value / by reference：拷贝进闭包 vs 存引用
- **隐式捕获** — implicit capture：`[=]`/`[&]` 由函数体用到的名字决定捕获集
- **初始化捕获（表达式捕获）** — init-capture：`[x = expr]`，C++14，可移动右值进闭包
- **泛型 Lambda** — generic lambda：`auto` 形参，`operator()` 是成员模板（C++14）
- **可调用对象** — callable object：满足"能用 `()` 调用"的任何表达式类型
- **函数对象包装器** — function wrapper：`std::function<R(Args...)>` 的类型擦除容器
- **占位符** — placeholder：`std::placeholders::_1..` 标记 bind 结果调用的参数槽位
- **类型擦除** — type erasure：以虚表/存储盒换统一外部类型的内部机制

## 最新演进与工业实践

- **`std::move_only_function`（C++23，P1840）**：wg21.link/P1840 实测 302（*General-purpose move-only function wrappers*）。去掉拷贝、保留移动，闭包持有独占资源时零额外堆分配——libstdc++/libc++ 均已实现（本机 libstdc++ 15.2 实测通过，见 🔧 实测 b：构造即通过 `static_assert(is_copy_constructible)` 的移除换成了"只要求 MoveConstructible"的窄门）；对 `std::function` 长期被诟病的"必须 CopyConstructible 才能装"是一次定点修复（`std::unique_ptr` 捕获进 function 的时代之耻终结）。机制注脚：move_only 版能缩小目标存储盒（不需要为"拷贝构造管理器"留函数指针槽），并强制 `operator=` 只收 rvalue——语义与 `std::unique_ptr` 同构。
- **类型擦除的成本账本**：libstdc++ 的 `std::function` 走"16 字节内联缓冲 + 超出走堆"路线（可拷贝目标要带 clone 管理器，内联盒因此更贵）；`absl::AnyInvocable`（move-only，业界最早量产的 move_only_function 平替）、`folly::Function`（自定义小缓冲尺寸）都是围绕这本账的开源答案。`absl::FunctionRef`/`std::function_ref`（13 篇）则干脆取消存储盒——形参位用"指针+调用蹦床"两字段，零分配零所有权。
- **`std::bind` 的官方降级路径**：C++20 时代三家 lint 一致（clang-tidy `modernize-avoid-bind` 默认开启、bugprone 系跟进），Google 内部风格明文"don't use std::bind"；保留场景收缩为两格——老代码里的成员函数指针绑定、以及 `std::placeholders` 在测试桩里的残值。教程保留 bind 节的价值变成**读旧代码的考古地图**。
- **隐式 this 的末路（C++20 起）**：`[=]` 捕获 `this` 在 C++20 标记弃用方向，C++26 时代 lint 默认要求 `[=, this]` 显式化。教程现随仓库更新到 C++26 展望，但捕获语义修订未回写第 3 章（见 00 勘误台账"教材时间差"条目）。
- **工业口径**：Core Guidelines Lan.3/F.4–F.10 一致推荐"小 lambda 优先、bind 不推荐"；`folly::Function`、`absl::AnyInvocable`/`FunctionRef` 是围绕"闭包存储成本"的工业化回答——`FunctionRef` 非拥有引用适合形参位，思路直通 C++26 `std::function_ref`（13 篇）。
- **社区重估**：2015–2019 年中文圈把"bind 还是 lambda"当争议，2020 后已是单方面判词——bind 仅在"旧代码+成员函数指针存储"残存；教程保留 bind 节的价值变成**读旧代码的考古地图**。
- **对照阅读**：`../Effective_Modern_C++/06-lambda表达式.md`（Meyers 条款 29–34：`std::function` 开销、初始化捕获捕获右值、泛型 lambda 等价于成员模板）从决策角度覆盖同一片地形。
