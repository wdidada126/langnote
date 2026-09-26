# 第 6 站 · 函数对象与 Lambda（原书第 10 章）

> 覆盖原书第 10 章「STL 函数对象及 Lambda」：10.1 函数对象概念（排序准则/内部状态/for_each 返回值/
> 判断式 vs 函数对象）、10.2 预定义函数对象与适配器/Binder、10.3 运用 Lambda（vs binder、vs 带状态对象、
> 调成员函数、作 hash/准则）。

## 核心概念速览（中英对照）

- **函数对象** — Function Object / Functor：重载 `operator()` 的对象；可携带状态、可内联、类型独特。
- **闭包类型** — Closure Type：lambda 表达式的编译器生成匿名类；每个捕获是一个成员。
- **捕获** — Capture：`[=]` 值捕获 / `[&]` 引用捕获 / `[x]` 精选 /（C++14）初始化捕获 `[p = std::move(q)]`。
- **判断式** — Predicate：`bool(T)`（一元）或 `bool(T,U)`（二元）的可调用体；**必须无副作用**（会被复制与多次调用）。
- **预定义函数对象** — Predefined Function Objects：`plus/less/equal_to/hash/…`（functional 头），算术/比较/逻辑三族。
- **函数适配器** — Function Adapter：`std::bind`/`std::function`/`mem_fn`/`reference_wrapper` 的签名变换族。
- **Binder** — Binder：`bind1st/bind2nd`（C++11 已弃用、C++17 移除）与 `std::bind` 的前世今生。
- **类型擦除** — Type Erasure：`std::function<Signature>` 统一存放一切匹配签名的可调用体。
- **外覆引用** — `std::ref/std::cref`：让 bind/function/容器「按引用」持有目标的唯一合法通道。

## 动机：为什么准则不能是一个普通函数指针

三个理由贯穿全章：
1. **状态**：「按工资降序、平级按工龄」的准则可能需要一个阈值成员；函数指针带不动。
2. **内联**：比较是排序/查找的内循环，模板参数下的 functor/lambda 类型唯一，编译器可展平
   ——函数指针经过间接调用，`sort` 可能慢一截（书中 10.1 的动机段）。
3. **类型即身份**：map 的比较器类型进键类型，不同准则 → 不同类型 → 不能互相赋值（10.1.1 的运行期准则专节
   引出 `function<bool(a,b)>` 作类型擦除的解法，与 7.7.5 运行期指定排序准则互引）。

## 机制

### 1. 函数对象的生命周期税（10.1.2–10.1.3，全书最阴的坑）

STL **按值复制**你传入的函数对象，且实现可以在任意时刻用任一副本、调用次数也不固定。三条推论：

- **状态会分裂**：你最后读的那个对象和算法实际用的不是同一个。`for_each` 的解药是**把最终副本返回给你**：

```cpp
struct Cumul { long total{0}; void operator()(int x) { total += x; } };
auto f = std::for_each(v.begin(), v.end(), Cumul{});   // f.total == 10
// 但 transform/count_if 不返回副本 → 有状态的它们必须靠引用捕获的外部变量
```

🔧 已实测 g++ 15.2（`-std=gnu++23`，v={1,2,3,4}）：`for_each` 返回的副本 `total == 10`。

- **计数类状态不可靠**：`count_if(pred)` 里 pred 篡改外部计数器 = UB 级坏品味；判断式要求「等价的多次调用同结果」。
- **拷贝成本**：lambda 捕获大对象按值 → 每次算法复制 functor 都拷大对象。解法：`shared_ptr` 捕获或（C++14）初始化捕获。

### 2. 预定义件与其用途（10.2.1）

| 族 | 件 | 典型用途 |
| --- | --- | --- |
| 算术 | `plus minus multiplies divides modulus negate` | `transform(a,b,out,plus<>{})` 做向量加法 |
| 比较 | `equal_to less greater...` | `sort(v.beg,v.end(),greater<>{})` 降序 |
| 逻辑 | `logical_and/not` | 罕见（判断式组合一般手写 lambda） |
| 杂项 | `hash`（C++11） | unordered 容器默认准则；也常做 lambda 版准则的替身 |

C++14 起这些件可以写 `std::plus<>{}`（透明实参），C++20 的 `std::plus<>` 直接支持指针算术与 `void` 特化。

### 3. bind 家族的真实地位（10.2.2–10.2.4）

- `bind1st/bind2nd` + 适配器（`not2`、`bind2nd` 时代）：类型体操繁琐、性能差，**C++17 已全灭**——
  书中 10.2.4 的「过时」名单今天读作墓志铭。
- `std::bind(f, _1, 42, _2)`：仍活着，但工业界几乎降级为「历史代码兼容层」：可读性输给 lambda、
  参数求值策略怪异（全部实参先求值）、阻碍内联的报道屡见。
- `std::function`：类型擦除的存放处（见 02 站权衡表）；构造可能堆分配、调用必间接、
  拷贝语义（C++11 要求可拷贝——**move-only 捕获的 lambda 塞不进去**，C++23 才放宽 ⚠️ 见演进节）。
- `mem_fn(&T::m)` / lambda 调成员函数（10.3.3）：`[=](auto& p){ return p.name(); }` 完胜。

### 4. Lambda 的四张对账单（10.3）

| 对手 | lambda 的赢面 | 对手仍赢的场景 |
| --- | --- | --- |
| binder（10.3.1） | 一目了然、可内联、可重载 | 需要在「声明处不可拼写类型」的高阶模板里传参？bind 结果类型同样不可拼写——两败 |
| 带状态 functor（10.3.2） | 就地定义、捕获免样板 | 状态需要跨多次算法调用复用/对外暴露接口 → 正经 class |
| 函数指针 | 捕获 + 内联 | 存进 C API/函数表（无捕获 lambda 可隐式转指针） |
| 全局函数/成员函数（10.3.3） | 适配签名 | 逻辑复杂/需复用 → 命名函数，lambda 只做一行转发 |

10.3.4 的「lambda 作 hash/排序/相等准则」是 unordered 容器实用主义入口：
`unordered_map<K,V,HashFn,EqFn>` 的 `HashFn/EqFn` 两个模板参数在 C++11 时代就要靠 decltype 拼装
——CTAD（C++17）之前这是最烦心的样板之一。

## 权衡：性能、尺寸与「可见的类型」

- functor/lambda：类型独一无二 → 容器 `set<Foo>` 按值比较器类型区分？**注意**：lambda 类型无默认构造，
  作为 map 比较器成员时必须构造期显式给实例。
- `std::function` 的税：一次间接调用 + 可能的堆 +「签名可拼写」的收益；异步 API/回调注册表用后者买单，
  热循环用前者。
- 「比较器必须建立严格弱序」（`comp(a,b)` 与 `comp(b,a)` 不同真；等价可传递）是 map/set 正确性的宪法，
  违反 = 未定义行为，甚至死循环。`[](auto& a, auto& b){ return a.score >= b.score; }` 是经典事故（>= 非严格）。

## 相邻概念对比

- **mutable lambda vs 带状态 functor**：`[&]` 已是引用通道；`mutable` 只放行「值捕获副本成员可改」，两者都不解决
  「算法可能用别的副本」——状态归宿永远是外部变量或 for_each 返回值。
- **无捕获 lambda vs 函数指针**：可隐式转换（回调 API 的救赎），但转换后的函数指针失去内联保证。
- **判断式（predicate）vs 一般函数对象**：判断式是「返回可转 bool 且无副作用」的特化承诺，
  算法文档里的 `UnaryPredicate` 模板参数即此（10.1.4 专节）。

## 最新演进与工业实践

- **C++11**：lambda、`std::function`、`bind`；函数适配器 `unary_function/binary_function` 弃用起点。
- **C++14**：泛型 lambda `[](auto a, auto b)`；初始化捕获（捕获即移动 `[p = std::move(q)]`）；
  lambda 隐式 constexpr 化机会增多（constexpr lambda 正式规则在 C++17）。
- **C++17**：`constexpr` lambda 正式化；`bind1st/bind2nd/not1...` 移除。
- **C++20**：lambda 模板参数 `[]<class T>(T a, T b)`；`std::function` 对移动友好度提升（分配器感知的 `std::function`
  未进标准 ⚠️）；`[[likely]]` 无关但同期；**旧式适配器全灭**：`unary_function/binary_function/ptr_fun/mem_fun` C++17 移除。
- **C++23**：`std::function` **允许 move-only 可调用体**（P2652R1 ⚠️ 编号未核实，本次只以「C++23 放宽可拷贝要求」记述）；
  `std::move_only_function`（P0290R4 ⚠️ 同上未核）进入 llvm libc++ 并推动标准化——确切名称以 cppreference 为准。
- **工业实践**：
  - Google/Chromium 风格：新代码**禁 std::bind**，一律 lambda（可读性 + 编译期检查）；回调存储用
    `absl::FunctionRef`（非拥有版 function，[abseil](https://github.com/abseil/abseil-cpp)）替代临时 `std::function`。
  - `std::function` 内联失败问题由 `std::type_identity`+模板参数或 `function_ref`（非标准，LLVM `llvm::function_ref`）解决。
  - 比较器准则：现代写法 `std::ranges::sort(v, {}, &T::key)`（投影参数，第 7 站），或显式
    `std::ranges::sort(v, std::greater<>{}, &T::score)` —— 避免手写 `<`/`>` lambda。
  - 验证行为的第一手资料：[cppreference lambda](https://en.cppreference.com/w/cpp/language/lambda)、
    [libcxx](https://github.com/llvm/llvm-project/tree/main/libcxx) `<functional>` 测试目录。

## 联系

- callable 概念的定义层：[01-导读与一般概念.md](01-导读与一般概念.md)；`std::function/ref` 工具层：
  [02-通用工具与智能指针.md](02-通用工具与智能指针.md)。
- 消费判断式的大户：[07-算法.md](07-算法.md)。
- 条款对照：[../Effective_Modern_C++.md](../Effective_Modern_C++.md)（条款 29–34：move 捕获、声明式偏好）。
- 课程式短讲：[../现代C++实战30讲/09-函数对象lambda与函数式编程.md](../现代C++实战30讲/09-函数对象lambda与函数式编程.md)。
- 系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)；单文件大纲：[../C++标准库.md](../C++标准库.md)。
