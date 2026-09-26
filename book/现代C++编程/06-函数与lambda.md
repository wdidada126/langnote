# 06 函数与 lambda（原书第 9 章）

> 覆盖：**第 9 章 函数**（9.1 函数声明 / 9.2 `auto` 返回类型 / 9.3 `auto` 和函数模板 / 9.4 重载解析 / 9.5 可变参数函数 / 9.6 可变参数模板 / 9.7 函数指针 / 9.8 函数调用运算符 / 9.9 计数例子 / 9.10 lambda 表达式 / 9.11 `std::function` / 9.12 `main` 函数和命令行）。
> 返回：[目录](00-总览与阅读地图.md)｜[单文件原笔记](../现代C++编程.md)｜[C++ 系列·总索引](../C++系列·总索引.md)

## 核心概念速览（中英对照）

- **函数声明与定义** — declaration vs definition：原型携带完整类型合同；`extern`、内联、`noexcept` 皆属合同条款
- **尾置返回类型** — trailing return type：`auto f() -> T` 让「依赖参数的返回类型」(`decltype` 配套) 可写
- **重载解析** — overload resolution：以实参→形参的**隐式转换序列等级**排座次；`const`/引用/模板特化度皆计分
- **二义性** — ambiguity：`0` 同时是空指针常量与整数等历史坑，`nullptr` 与 `explicit` 是本章埋的两道闸
- **可变参数函数（C 式）** — varargs `...`：`va_list` 族，类型不安全、无法跨 ABI 检查——本章判词：仅限 C 边界
- **函数指针** — function pointers：一等函数的朴素形态，数组参数退化与签名繁琐是其痛点
- **调用运算符对象** — function objects：重载 `operator()` 的类，可携带状态——lambda 的底层真身
- **lambda 表达式** — lambda：匿名闭包类 + 捕获列表 `[=]/[&]/init`；C++14 广义捕获、C++20 按值捕获 `this` 等补票
- **`std::function`** — type-erased callable：统一「任何可复制调用物」的容器，代价是堆分配与间接调用
- **偏绑定** — `std::bind` / `std::bind_front`：前者因参数占位符与拷贝语义受围攻，C++20 的 `bind_front` 取其精华
- **完美转发** — `std::forward<T>`：在模板里原样传递值分类，与 `T&&` 推导配对使用
- **命令行入口** — `main(argc, argv)`：`string_view`/`span` 化包装前，它仍是 C ABI 的字符串数组（第 21 章交给 ProgramOptions）
- **泛型 lambda** — generic lambda：`[](auto x){}` 即「编译器写的模板 `operator()`」，C++14 起仿函数模板化门槛消失
- **按值捕获 `*this`** — capture by value of `*this`：C++17 语义（C++20 起 `this` 按值同义），闭包脱离对象生命周期的正解之一
- **`std::invoke`** — callable 统一调用：成员指针/普通函数/仿函数一视同仁，`12` 章算法投影与 `09` 章 `apply` 的地基
- **引用折叠** — reference collapsing：`&` 与 `&&` 相遇只剩 `&`，`forward` 与万能引用能成立的代数定律
- **`noexcept` 合同** — noexcept specification：可观测的异常承诺（⚠️ 它**不**进类型系统，相关提案当年被拒）；`vector` 扩容选移动还是拷贝先看它（`02`/`09` 章联动）

## 1. 动机：函数是「值分类的十字路口」

第 4 章讲对象怎么活，第 9 章讲**动作怎么传**。原书从 C 式函数声明出发，一路把重载解析、varargs 遗产、函数指针的别扭、仿函数与 lambda 的等价性、`std::function` 的代价排成一条「调用物的进化史」——9.9 的「计数例子」（带状态的仿函数）正是 lambda 存在的理由书。它同时是全书泛型机制的验收场：`04` 的模板、`02` 的移动、`03` 的接口，在这里全部变成「参数与返回值该怎么写」。

## 2. 机制：四条演进线

**返回类型的去签名化。** 9.2/9.3 讲 `auto` 返回（C++14 起多返回点须同类型）与「函数模板参数即 `auto`」的等价性（`template<typename T> T f(T)` ≡ `auto f(auto)` ⚠️ GCC 对裸 `auto` 形参的支持以 C++20 函数模板简写为准）。工程口径：`auto` 返回**只用于**返回类型平凡可见（转发、lambda 内部）的场合，公开 API 签名写出来——否则接口从类型系统里消失（EMC++ Item 3 的告诫方向）。

**重载解析是一场转换税排队。** 四级匹配阶梯：精确匹配→提升→标准转换→用户转换→变参；模板「至少同等特化」判胜负。本章的教学重点不在背阶梯，而在两处历史事故：**`0`/`NULL` 对整型与指针形参的暧昧**（`nullptr` 解药）与 **单参构造即隐式转换**（`explicit` 解药，`05` 章联动）。

**从 varargs 到可变参数模板。** `printf` 的 `...` 不携带类型；变参模板+折叠（`04` 章）+`std::index_sequence`（9.6 的高级化）才让「转发任意参数」成为类型安全动作。`<cstdarg>` 只在 C ABI 边界保留；`std::va_list` 的兄弟——`std::format` 的 `format_args`（C++20）实际上宣告了类型擦除式参数打包在标准库的胜利。

**lambda、`std::function` 与绑定家族。** lambda 即「编译器替你写的仿函数类」；捕获语义（`&`/`=`/init 捕获/`this` 与 `*this`）决定闭包对象持有什么。`std::function` 提供运行期统一接口（小对象优化、可能堆分配、间接调用）；`bind` 的历史地位在 C++20 `bind_front` + 「优先用 lambda」两条军规后基本归零。9.12 的 `main` 收尾把「函数」拉回操作系统接口，为第 21 章程序装配埋线。

## 3. 权衡：抽象层的账单

- **`std::function` vs 模板形参**：类型擦除（可存容器、可解编译依赖）换堆分配+调用间接；模板形参（零开销）换头文件暴露与单态化膨胀。第 10 章「依赖注入做可测试性」会偏向 `std::function`/接口——**先想清楚你买的是可存储性还是速度**。
- **捕获的悬垂风险**：`[&]` 闭包活过作用域即 `02` 章悬垂引用案的第二案发现场；异步场景（`13` 章 Asio 处理器）强制 `shared_ptr` 捕获或 init-capture 转移。
- **完美转发的适用面**：工厂透传值得 `forward`；单参函数「万能引用+转发」常不如按值+移动（EMC++ Item 41 的方向）。

## 4. 相邻概念对比

| 概念 A | 概念 B | 分界线 |
| --- | --- | --- |
| lambda 直接传 | `std::function` 存 | 就地消费 vs 跨时存储/多态集合 |
| `std::bind(f, ph1, x)` | `bind_front(x, f)` / lambda | 后者类型正确、可内联、参数顺序直白——bind 全场景替代 |
| `T&&` 万能引用 | 右值引用 | 看是否存在「模板/`auto` 的 `T&&` 推导」：是则万能引用 |
| 函数指针 | `void(*)()` 的替代品 | 无捕获 lambda 可转函数指针（ABI 回调桥），C 回调唯一可行解 |
| 尾置返回 `-> decltype(expr)` | C++14 裸 `auto` | 后者免写表达式但禁多返回点类型分歧与递归需显式化 |

## 典型误区与修正视角

| 误区 | 症状 | 修正视角 |
| --- | --- | --- |
| 「`T&&` 都是万能引用」 | 非模板场景也写 `forward` | 只有**推导中的** `T&&`（模板/`auto`）是万能引用；`void f(X&&)` 就是右值引用 |
| 「`std::function` 有一层薄 overhead」 | 热路径回调塞进 `function` | 可能堆分配+间接调用双重税；模板形参/`function_ref`（非拥有）才是就地消费的账 |
| 「`[&]` 捕获安全因为马上就用」 | 闭包存入成员/队列 | 异步或存储即悬垂（`13` 章 Asio 处理器现场）；默认写显式捕获或 init-capture 转移所有权 |
| 「`bind` 是函数柯里化标准件」 | 满屏 `_1/_2` 占位符 | 参数倒装、全拷贝、难内联三连败；C++20 起 `bind_front` 或 lambda 全覆盖 |
| 「lambda 不能有模板参数」 | 手写仿函数绕路 | C++14 泛型 lambda 即模板 `operator()`；C++20 更给 lambda 显式 `<T>` 模板参数列表 |
| 「递归 lambda 直接调自己」 | 编译不过误以为语言缺陷 | 闭包无名字；用 `y_combinator` 惯用法或先落成函数再包 lambda |
| 「函数指针=可调用对象全集」 | 捕获 lambda 强转函数指针失败 | 只有**无捕获** lambda 能转；带状态回调一律 `function`/模板/类型擦除三选一 |
| 「`noexcept` 只是文档」 | 违约后惊讶于 `terminate` | 承诺违约直接 `terminate()`；它不进类型系统但进标准库决策（扩容拷贝/移动选择） |

## 练习检查点（对应原书「练习/拓展阅读」栏）

- 9.4：构造一例 `0` 同时匹配整型与指针重载的二义事故，换 `nullptr` 复验消失；再给单参构造补 `explicit` 复现另一道闸。
- 9.6：用变参模板+`std::index_sequence` 手写迷你 `apply`，与标准 `std::apply` 对拍（本章 🔧 已实测 `apply`/`make_from_tuple`）。
- 9.9 计数例子三态改造：仿函数 → 等价 lambda → 装进 `std::function`，打印 `sizeof` 闭包与触发堆分配的阈值观察。
- 9.10：分别用 `[&]`、`[x]`、`[x = std::move(x)]` 捕获同一 `unique_ptr`，只许最后一种编译通过——用编译器复述 `02` 章移动语义。
- 9.11：把解析回调从 `function` 换成模板形参，量化一次全量编译时间差（`04` 章 header-only 账单的回收）。
- 9.12：把 `argc/argv` 第一时间包成 `std::span<std::string_view>` 传给 `run()`，第 21 章 ProgramOptions 迁移前哨。

## 章节依赖图

- 上游：`02` 章值分类是捕获语义与 `forward` 的代数基础；`04` 章变参模板/折叠为 9.5–9.6 供弹药；`05` 章重载/转换规则即 9.4 的判分细则。
- 平行：`07` 章 mock 用 `std::function`/接口注入做依赖替换——本章抽象层账单在测试语境重算。
- 下游：`08` 章 deleter 是「可调用对象进模板参数」的标本；`09` 章 `reference_wrapper`/`invoke`、`12` 章算法投影全面消费本章词汇。
- 下游：`13` 章异步回调的捕获纪律、`14` 章命令行解析（9.12 → ProgramOptions）双线回收。
- 一句话：本章把「动作」升格为可与数据同等传递的一等公民——第二部分所有库章的公共语法。

## 🔧 实测对照：`std::bind` 时代 vs `bind_front`/`apply`/`make_from_tuple`（已实测 g++ 15.2）

```cpp
#include <functional>
#include <cstdio>
#include <tuple>
struct Bank { int balance = 0; void deposit(int x) { balance += x; std::printf("deposit %d -> %d\n", x, balance); } };
struct Point { int x, y; };
int main() {
    Bank b;
    auto d10 = std::bind_front(&Bank::deposit, &b);            // C++20，成员指针绑定不再要占位符
    d10(10); d10(20);
    std::printf("apply=%d\n", std::apply([](int a, int c){ return a + c; }, std::tuple{2, 3}));       // C++17
    auto p = std::make_from_tuple<Point>(std::tuple{7, 8});     // C++17，P0209R2
    std::printf("from_tuple=(%d,%d)\n", p.x, p.y);
}
```

- `-std=gnu++17`：编译失败，逐字：`error: 'bind_front' is not a member of 'std'`（apply/make_from_tuple 本已 C++17 可用）。
- `-std=gnu++20` 真实输出：`deposit 10 -> 10` / `deposit 20 -> 30` / `apply=5` / `from_tuple=(7,8)`。
- 提案账：`make_from_tuple` 措辞稿 [P0209R2](https://wg21.link/p0209) 本会话实测，标题逐字 "make_from_tuple: apply for construction"——它把 tuple 作为「参数包的可存储替身」接入构造与调用（`09` 章 tuple 节的接口胶水）。
- `bind_front` 无逐字可引的已核提案号 ⚠️（本会话对候选号的证伪记录见 [目录](00-总览与阅读地图.md) 账本），引用口径写「C++20 入库」即可。

## 最新演进与工业实践

- **C++20/23 函数侧清单**：lambda constexpr 化、模板参数 lambda（C++20）；`std::move_only_function`（C++23）——只移动、可捕获 `this` 不持拷贝的回调类型，异步处理器（`13` 章）的默认容器新候选；`std::start_as`/execution 线（C++26，[P2300](https://wg21.link/p2300) 实测可达，标题逐字 std::execution）把「调用+线程调度」并入统一词汇。
- **`std::function` 的工业替代品**：[`facebook/folly`](https://github.com/facebook/folly) 的 `Function`（Noexcept 可调）、[`vectorized/function_ref`](https://github.com/vectorized-projects/function_ref)（非拥有回调引用）；本项目 [`../C++标准库/06-函数对象与Lambda.md`](../C++标准库/06-函数对象与Lambda.md) 已把 `reference_wrapper` 一节对齐此生态。
- **重载解析的可见性工具**：报错天书用 cppinsights 还原「选了哪个重载」；`static_assert` 于不可达分支的用法（`04` 章）。
- **练习/拓展接点**：9.9 计数例子 2026 版改造：lambda 计数器进 `std::function`（可存储）→ 换 `move_only_function`（禁拷贝）→ 换模板形参（零开销）三态对照，量一次捕获开销即完成本章全部账单。

## 与其他书的联系

- 条目化军规主战场：[`../Effective_Modern_C++/05-右值移动完美转发.md`](../Effective_Modern_C++/05-右值移动完美转发.md)、[`../Effective_Modern_C++/06-lambda表达式.md`](../Effective_Modern_C++/06-lambda表达式.md)。
- 课程式姊妹讲法：[`../现代C++实战30讲/09-函数对象lambda与函数式编程.md`](../现代C++实战30讲/09-函数对象lambda与函数式编程.md)、[`../现代C++实战30讲/10-可变模板tuple与类型擦除.md`](../现代C++实战30讲/10-可变模板tuple与类型擦除.md)。
- 函数对象的类型擦除内部机制：[`../C++标准库/06-函数对象与Lambda.md`](../C++标准库/06-函数对象与Lambda.md)；命令模式视角：[`../C++20设计模式/09-职责链与命令.md`](../C++20设计模式/09-职责链与命令.md)。
- 下一站：`07-测试与模拟.md`（第二部分「库和框架」开端）；回到 [目录](00-总览与阅读地图.md)。
- 向上：[单文件原笔记](../现代C++编程.md)｜[C++ 系列·总索引](../C++系列·总索引.md)。
