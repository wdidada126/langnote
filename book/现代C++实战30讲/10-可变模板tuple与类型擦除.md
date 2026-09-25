# 讲 18｜应用可变模板和 tuple 的编译期技巧

> **一句话**：可变模板让「类型」和「数量」都成为参数，`tuple` 让「多个返回值」变成一等公民；而一旦你想把它们折叠成单一类型，就走到了**类型擦除**的门口。

---

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 参数包 | 模板参数包、函数参数包、`sizeof...` | 展开靠递归或折叠表达式 |
| 转发与展开 | `std::forward`、转发引用 | 转发只能做一次，重复 `std::move` 会掏空对象 |
| 编译期展开 | 折叠表达式（C++17） | 取代线性递归，深度与可读性都更好 |
| `tuple` 与 `pair` | `get`、`tie`、结构化绑定 | 多返回值优先用 `struct`，其次 `tuple` |
| 结构化绑定 | `auto [a, b] = ...`、`std::ignore` | 让「解包」成为语法，而不是 `get<0>()` |
| 类型擦除三方案 | 虚函数 / `std::function` / `std::any` | 抹掉类型是代价换灵活性 |
| 手写擦除 | 继承 + 虚调用的最小实现 | 看清 `std::function` 的成本构成 |
| 🔧 现代补充 | `std::apply`、`move_only_function`、`function_ref/inplace_function` | 擦除容器的分配与拷贝正在被逐步优化掉 |

---

## 核心精讲

> 以下均为**教学示意，不参与构建**。

### 1. 参数包：一切组合子的地基

```cpp
// 教学示意：参数包与展开（不参与构建）
template <typename... Ts>
struct Tuple { static constexpr std::size_t size = sizeof...(Ts); };

template <typename... Args>
void log_all(Args&&... args) {                  // 转发引用 + 参数包
    ((print(std::forward<Args>(args))), ...);    // C++17 折叠：逐个展开
}

template <typename... Args>
constexpr std::size_t total_bytes() { return (sizeof(Args) + ...); }   // 一元折叠
static_assert(total_bytes<int, char, double>() == sizeof(int) + sizeof(char) + sizeof(double));
```

四种折叠写法值得记住（以 `+` 为例）：`(pack + ...)`、`(... + pack)`、`(pack + ... + init)`、`(init + ... + pack)`。

### 2. 转发引用的三个坑

```cpp
// 教学示意：转发里的经典错误（不参与构建）
template <typename T>
void good(T&& x) { consume(std::forward<T>(x)); }          // 正确：转发一次

template <typename T>
void bad(T&& x) { consume(std::move(x)); consume(std::move(x)); }  // 错误：第二次已掏空
```

| 坑 | 表现 | 规避 |
| --- | --- | --- |
| 重复 `std::move`/`std::forward` | 第二次拿到 moved-from 对象 | 转发只做一次 |
| 转发引用接左值时会退化成 `T&` | 模板参数变成引用 | 用 `std::remove_reference_t` 后再取属性 |
| 重载时 `T&&` 会意外胜出 | 本该走 const& 的重载被抢 | 用 `requires` / `enable_if` 明确约束 |

### 3. `tuple`：多返回值的标准答案（以及它的更好替代品）

```cpp
// 教学示意：tuple 与结构化绑定（不参与构建）
std::tuple<int, std::string, bool> probe() { return {42, "ok", true}; }

auto [code, msg, ok] = probe();                    // C++17 结构化绑定
auto [c2, m2, o2] = probe();                       // 复制而非引用
auto& [c3, m3, o3] = probe();                      // 引用到临时 → 悬垂，勿写

std::tie(c2, m2, o2) = probe();                    // 赋值解包
std::tie(c3, std::ignore, o3) = probe();           // 只接关心的两个

bool same = (c2 == c3) && (o2 == o3);              // 比较 tuple 是按字典序的
```

**实践判断**：

- 返回值 ≥ 3 个且字段含义稳定 → 定义一个 `struct`（命名可读，可加方法，还能加默认值）；
- 返回值是「一个值 + 一个状态」优先考虑 `std::pair` / `std::optional` / `std::expected`；
- `tuple` 适合**泛型胶水代码**（工厂、包装器），不适合作为长期维护的对外接口——访问只能靠位置，改名就得改全部 `get<>` 调用点。

### 4. `std::apply` 与「把 tuple 拆开当参数」

```cpp
// 教学示意：apply 与 invoke（不参与构建）
std::tuple<int, std::string> t{1, "x"};
auto result = std::apply([](int a, const std::string& s) { return a + s; }, t);
```

### 5. 类型擦除：三种方案的取舍

| 方案 | 抹掉的类型数 | 分配 | 内联 | 典型用途 |
| --- | --- | --- | --- | --- |
| 虚函数 + 派生类 | 1 个基类 | 无（若用值语义小对象） | 否 | 插件、策略、稳定 ABI |
| `std::function` | 任意可调用 | 可能（超过小对象阈值） | 否 | 回调、事件、任务 |
| `std::any` | 任意可拷贝类型 | 可能 | 否 | 容器里塞异质值 |
| 模板 | 不擦除 | 无 | 是 | 热路径的默认选择 |

```cpp
// 教学示意：最小可运行的类型擦除（不参与构建）
class Drawable {
public:
    virtual ~Drawable() = default;
    virtual void draw(std::ostream&) const = 0;
};
template <typename F>
class DrawableImpl final : public Drawable {
    F f_;
public:
    explicit DrawableImpl(F f) : f_(std::move(f)) {}
    void draw(std::ostream& os) const override { f_(os); }
};
template <typename F>
Drawable make_drawable(F&& f) {
    return DrawableImpl<std::decay_t<F>>(std::forward<F>(f));   // 返回基类，类型被抹掉
}
```

```cpp
// 教学示意：std::any 与 variant 的差别（不参与构建）
std::any a = 42;
if (int* p = std::any_cast<int>(&a)) { use(*p); }     // 取回原类型，可能失败

std::variant<int, std::string> v = "text";
std::visit([](const auto& x) { log(x); }, v);          // 类型集合固定，编译期可穷尽
```

> **`std::any` 与 `std::variant` 的区别只有一条**：`any` 的类型是运行时才知道的单个值，`variant` 的类型集合在编译期写死。因此 `variant` 的 `visit` 可以被完全优化，而 `any_cast` 一定是运行期检查。

### 6. 一个常见组合：可变模板工厂

```cpp
// 教学示意：编译期注册表（不参与构建）
template <typename... Handlers>
struct Registry : Handlers... {                        // 用继承展开参数包
    template <typename Msg> void dispatch(const Msg& m) {
        (this->Handlers::handle(m), ...);              // 逐个尝试，注意求值顺序规则
    }
};
```

> 参数包展开中的**求值顺序是无保证的**（除了 `<<` 与逗号折叠的少数情形）；若各元素之间必须按序执行，不要用折叠表达式，改用显式展开。

---

## 版本演进

| 版本 | 变化 |
| --- | --- |
| C++98 | 定长模板参数列表；没有参数包 |
| C++11 | **可变模板**（ variadic templates）、`std::tuple`、`std::forward`、`std::move` |
| C++14 | 变量模板、返回类型推导；`make_unique` |
| C++17 | **折叠表达式**、结构化绑定、`std::apply`、`std::optional`/`variant` 生态成熟、模板参数 `auto` |
| C++20 | 模板 lambda、`constexpr` 虚函数、`std::span`；`visit` 的错误信息改善 |
| **C++23** | **`std::move_only_function`**、多维下标（P2128）、`static operator()`（P1169） |
| C++26 | 反射落地后，「手写注册表」这类模式会被大幅简化 |

---

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Vandevoorde & Josuttis, *C++ Templates: The Complete Guide*, 2nd ed. | **Addison-Wesley 2017** | 第 2 章：可变模板与 `tuple` 展开技巧的完整谱系 |
| Josuttis, *The C++ Standard Library, 2nd ed.* | **Addison-Wesley 2012** | 第 9 章：`<tuple>` 与 `<utility>` 的细节 |
| ISO/IEC 14882，`[temp.variadic]` / `[tuple]` / `[any]` | C++ 标准 | 参数包展开规则与求值顺序的正式表述 |
| Myers, *More Effective C++*（Item 2：区分 `new` 与 `new[]`；Item 6：`auto_ptr` 的坑） | **Addison-Wesley 1995** | 早期「擦除类型」与资源传播的教训 |
| **P0357** 一系（反射与元编程） | **WG21 提案** | 反射方向，会改写本章大量手写模式（编号请以提案列表为准） |

---

## 近年研究与工业界开源实践（2015–2026）

- **`inplace_function` / `function_ref` 提案在推进**：把「小对象内联 + 无分配」做成标准类型，直接削弱 `std::function` 的分配开销；C++23 的 `std::move_only_function` 已是第一步。
- **`tuple` 作为内部胶水、结构体作为对外接口**：这条分工已成为 C++ 团队的通用经验，避免 `get<3>()` 式的脆弱接口。
- **结构化绑定与 POD 的边界**：聚合类型、`tuple`、`pair`、`std::array` 都支持，但绑定引用到临时对象会产生悬垂，编译器警告在逐步覆盖。
- **类型擦除的成本被量化**：`std::function` 的平均构造成本在小对象优化下已接近一次间接调用，但超过阈值后是堆分配；`folly::Function` 提供了可移动、可内联的版本。
- 🔧 **`std::apply` + `expected`/`optional` 的互操作**：把「可能失败」传播给 tuple 元素（如 `expected<tuple<...>, E>`）在 2026 年仍是热门话题，`std::expected` 落地后此类组合明显增多。
- 🔧 **反射会重写这一章**：当语言支持反射后，「按参数包注册 handler」「按字段生成序列化代码」这类手写模板会被大幅压缩（本文不写提案编号，请以 WG21 列表为准）。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `facebook/folly` | **30.5k★** | `folly::Function`、`tuple` 扩展工具与「小对象优化」的工业实践 |
| `abseil/abseil-cpp` | **18.1k★** | `absl::variant`/`InPlaceFactory` 等擦除与就地构造的样板 |
| `microsoft/STL` | **11.2k★** | `std::function`/`std::any`/`std::variant` 的实现细节 |
| `fmtlib/fmt` | **25.8k★** | 参数包 + `visit` + 编译期检查的模板组合范例 |
| `TartanLlama/expected` | **1.9k★** | `expected` 与 `tuple` 组合的三方参考 |

---

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「`tuple` 是返回多值的首选」 | 对外接口优先 `struct`；`tuple` 只适合泛型胶水 |
| 2 | 「`auto [a,b] = f();` 一定安全」 | `auto& [..] = 临时对象` 会悬垂；绑定引用时要确认对象存活 |
| 3 | 「`std::any` 比 `variant` 更灵活所以更好」 | `variant` 的类型集合编译期已知，`visit` 可完全优化；`any` 只能运行期检查 |
| 4 | 「折叠表达式按顺序求值」 | 参数包展开的求值顺序**未指定**；顺序敏感的逻辑要靠显式循环或分号折叠之外的手段 |
| 5 | 「`std::function` 可以随便拷贝」 | 拷贝带状态的闭包会复制其状态；跨线程传递要考虑数据竞争 |
| 6 | 🔧 本讲未提及 `std::move_only_function`（C++23） | 只可移动的可调用包装是「异步任务 + 移动回调」的标准答案 |
| 7 | 🔧 未提「擦除的分配优化」 | `inplace_function` 一类类型（以及各厂商的小对象优化）正在把「擦除必然堆分配」变成历史 |
| 8 | 🔧 缺少反射对本章的影响评估 | C++26 方向的反射会显著削减手写可变模板与注册表的面积，建议留出跟进预算 |
| 9 | 🔧 未对比「擦除 vs 模板 + 约束」 | 2026 年的默认思考顺序应是：**能用模板 + `requires` 约束就别擦除**，擦除留给真正的动态边界 |

---

## 与其他章 / 其他书的联系

- **`09-函数对象lambda与函数式编程.md`**：`std::function` 正是本章「擦除」的对象。
- **`08-模板编译期多态与编译期计算.md`**：折叠表达式与参数包展开的常量来源。
- **`03-右值与移动及返回对象.md`**：`tuple` 是按值返回多值的现代答案。
- **`05-异常与错误处理的现代化.md`**：`variant` 与 `visit` 是类型化错误的 precursor。
- **`16-未来篇Concepts-Ranges-协程.md`**：Concepts 与 Ranges 在泛型层的进一步抽象。
- **`book/C++模板元编程.md` / `book/C++20模板元编程.md`**：本章的可变模板谱系的完整教材。
- **`book/C++标准库.md`**：`<tuple>`/`<any>`/`<variant>` 的逐条说明。
