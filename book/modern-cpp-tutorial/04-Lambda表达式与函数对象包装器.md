# 04 · Lambda 表达式与函数对象包装器

> 系列导航：[C++ 系列·总索引](../C++系列·总索引.md) · [《现代 C++ 教程》单文件](../modern-cpp-tutorial.md) · [00 总览与阅读地图](./00-总览与阅读地图.md)
>
> 覆盖原书：第 3 章 §3.1 Lambda 表达式（基础：值捕获/引用捕获/隐式捕获/表达式捕获；泛型 Lambda）、§3.2 函数对象包装器（`std::function` / `std::bind` 和 `std::placeholder`）（`book/zh-cn/03-runtime.md`，标题逐字）。

## 一、动机：把"函数"变成一等公民

C++98 里"能传的东西"和"能调用的东西"是两套体系：函数指针简单但不能带状态；函数对象（重载 `operator()` 的类）能带状态但要为每个回调手写一个 struct。Lambda 把两者合并：**语法是函数，本质是编译器生成的闭包类**——捕获列表就是构造函数参数，`mutable` 决定 `operator()` 是否 const。`std::function` 则解决"统一容器"问题：函数指针、闭包、成员函数绑定体类型各异，需要一个类型擦除的包装器把"可调用性"变成一种值类型。`std::bind` 是"部分应用"的语言层答案（占位符 `_1.._N`），历史地位与 lambda 高度重叠——这直接决定了本章的现代重估结论。

## 二、机制：逐条拆开

**闭包类型的四条规则**（原书分散讲，这里收拢）：① 每个 lambda 生成**唯一**的未命名类类型；② 空捕获的 lambda 可隐式转成函数指针（原书 `functional(f)` 示例展示了这一点：形参写函数类型 `foo`，实参退化/转换为 `foo*`）；③ 默认 `operator()` 是 const——值捕获成员只读，`mutable` 解锁写；④ 捕获发生在**创建时**而非调用时（原书值捕获示例：`value=1` 创建、改 100 后调用仍返回 1）。

**四种捕获形态**：`[]`、`[a,b]`、`[&]`（按用到的隐式引用捕获）、`[=]`（按用到的隐式值捕获）。原书 2026 修订版特意强调 `[&]`/`[=]` 是"从函数体内的使用确定"——这正是工业规范反对裸 `[&]` 的原因（捕获集随函数体演化而漂移，悬垂风险不可见）。

**表达式捕获（初始化捕获，C++14）**：`[v2 = std::move(important)]` 允许任意表达式初始化捕获成员，类型按 auto 规则推导——它把"独占指针移动进闭包"从不可能变成一行。泛型 lambda（C++14）= `auto` 形参，闭包类型的 `operator()` 变成成员模板。

**std::function**：持有目标的可调用包装器，可拷贝/可空（`operator bool`）。类型擦除意味着堆分配与小对象优化并存、调用路径含间接跳转。**std::bind**：`bind(f, _1, 1, 2)` 返回一个存储了拷贝的参数包对象，占位符下标决定形参去向；它对参数做"decay-copy 存储"，且调用时一律按 `CVT` 转换——语义细节多，出过错的读者不少（引用参数需 `std::ref`）。

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

已实测 g++ 15.2：`-std=c++11` → 第一道墙是 `error: 'make_unique' is not a member of 'std'`（原书代码隐含 C++14 依赖，示例本身混用两档特性——教程的"混合档位"陷阱）；把 make_unique 换掉后 C++11 仍会在 `v2 = std::move(...)` 处报"lambda capture initializers only available with '-std=c++14'"；`-std=c++14` → 通过，输出 `add(1,2) = 7`。

## 三、权衡与陷阱

- **值捕获 vs 引用捕获的生死线**：异步/延迟执行（线程池、回调注册）里，引用捕获栈变量 = 定时炸弹；`[=]` 捕获的是 `this` 指针而非成员本身，这一经典陷阱在 C++20 被标记为弃用方向（须显式写 `[=, this]`）——教程未讲这条后续。
- **`std::function` 的成本**：类型擦除→构造可能堆分配、调用无法内联、拷贝语义深复制闭包。热路径用模板参数（编译期多态）或 C++23 `move_only_function`（无拷贝、无分配保证路径）。
- **`std::bind` 已输掉竞争**：同样的部分应用，lambda 可读、可内联、可显式控制引用捕获（`std::ref` 只出现一次而非每个占位符脑内展开）。教程在 §3.1 的 `[out = std::ref(...)]` 花式示例与 §6 习题里用 lambda 替代 bind，态度其实已经摆明。
- **递归 lambda**：`std::function` 自引用是经典绕法；C++23 显式对象形参给出正解（见 12 篇）；教程止步于"别扭但可行"。

## 四、与相邻概念对比

| 维度 | 函数指针 | Lambda（空捕获） | `std::function` | `std::bind` 结果 |
|---|---|---|---|---|
| 携带状态 | 无 | 无→闭包无大小；有捕获则类成员 | 有（类型擦除） | 有（存储 decay-copy） |
| 可拷贝/可空 | 可/可 | 是/否（闭包不可空） | 是/是 | 是/否 |
| 内联友好 | 高 | 高 | 低 | 低 |
| 现代推荐 | 简单回调用 | **默认选择** | 需要存储+异构时 | 基本弃用 |

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

## 最新演进与工业实践

- **`std::move_only_function`（C++23，P1840）**：wg21.link/P1840 实测 302（*General-purpose move-only function wrappers*）。它去掉拷贝、保留移动，从而在闭包持有独占资源时零额外堆分配——libstdc++/libc++ 均已实现；对 `std::function` 长期被诟病的"必须 CopyConstructible 才能装"是一次定点修复。
- **隐式 this 的末路（C++20 警告 → 提案持续收紧）**：`[=]` 捕获 `this` 在 C++20 起被弃用方向明确；C++26 时代 lint 已默认要求显式 `[=, this]` 或 `[&]`。原书未覆盖，属教程停更段位的正常体现——教程现随仓库更新到 C++26 展望，但捕获语义修订未回写第 3 章。
- **工业口径**：Core Guidelines Lan.3/Lambda 系列、F.4–F.10 一致推荐"小 lambda 优先、bind 不推荐"；Abseil/folly 的异步 API（`folly::Function`、`absl::AnyInvocable`/`FunctionRef`）正是围绕"闭包存储成本"的工业化回答——`FunctionRef` 非拥有引用适合形参位，思路直通 C++26 `std::function_ref`（13 篇）。
- **社区重估**：2015–2019 年中文圈把"bind 还是 lambda"当争议题，2020 后已成定论（lambda 胜出，bind 仅存于旧代码迁移）；本章的教学价值重心已移到"捕获即析构责任转移"的生命周期视角（与 07 篇智能指针、09 篇线程池习题构成同一能力链）。
