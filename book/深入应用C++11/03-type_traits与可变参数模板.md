# 03 · 消除重复，提高代码质量：type_traits 与可变参数模板（原书第 3 章）

> 覆盖原书 3.1 type_traits / 3.2 可变参数模板 / 3.3 综合应用（optional、lazy、dll 帮助类、function_traits、any、variant、ScopeGuard、tuple_helper）。
> 大纲形态见 [../深入应用C++11.md](../深入应用C++11.md)；返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **类型萃取** — type traits：`is_xxx / remove_xxx / conditional / enable_if` 一族编译期类型查询与变换，全部是 `integral_constant`/别名。
- **SFINAE** — Substitution Failure Is Not An Error：模板实参替换失败只淘汰该重载，不是硬错误——`enable_if` 的机制底座。
- **标签分派** — tag dispatch：以类型标签重载选择实现，与 SFINAE 二选一的分支手段。
- **可变参数模板** — variadic templates：`template<class... Args>`，`sizeof...` 取包长，`Args&&...` 展开。
- **递归展开** — recursion on packs：C++11 唯一的遍历手段：空包重载 + 剥头递归。
- **可选值** — optional：`有/无` 二态值容器；书中用 `aligned_storage` + placement new 自造。
- **惰性求值** — lazy：首次访问才构造的 optional 近亲，构造成本与使用与否的博弈。
- **函数特征** — function_traits：从任意可调用对象拆出返回类型与形参包，绑定器/总线共用的元信息底座。
- **任意类型容器** — any：完全类型擦除，类型信息只留运行期一份（typeinfo/标签）。
- **判别式并集** — variant：类型集编译期已知、运行期持其一，访问靠访问者。
- **作用域守卫** — ScopeGuard：析构时执行登记动作，异常路径的资源兜底。
- **变量模板** — variable templates：`template<class T> constexpr bool v = ...`，traits 查询的 C++14 去 `::value` 写法。
- **折叠表达式** — fold expressions：C++17 `(args + ...)`，一行替代"空包重载 + 剥头递归"四件套。

## 一、动机：库作者替标准库"提前干活"

2015 年的现实：`std::optional/variant/any` 都不存在（C++17 才有），`std::function` 拿不到签名信息，
写一个通用 `make_unique`/参数转发/插件导出需要手写 10 份重载。第 3 章教的正是那代库作者的
生产力工具——用 type_traits 做"编译期的 if"，用参数包做"编译期的 for"，把重复代码压缩成一次
模板展开。这些自研物（cosmos 的 Optional.hpp / Variant.hpp / function_traits.hpp / ScopeGuard.hpp，
均实测在仓库顶层）就是本章的"开源库案例"。

## 二、机制

### 2.1 traits 的三形态
①查询：`integral_constant<bool, …>` 派生类，读 `::value`（运行期零成本，编译期常量）；
②变换：`remove_reference<T>::type` 之流，产出新类型；③控制：`enable_if<b, T>`——只有 `b` 为真
才有嵌套 `type`，SFINAE 据此淘汰重载。`conditional<b, A, B>` 是编译期三元。C++11 的语法税：
处处 `typename` + `::type`；`_t` 别名是 C++14 补的（实测：`remove_reference_t` 在 gnu++11 下 error），
`_v` 变量是 C++17 补的。

### 2.2 参数包的展开 algebra
`f(args...)` 在 C++11 只有三条路：递归重载（剥头）、数组初始化列表技巧 `int a[] = {(push(args),0)...}`、
逗号展开。`sizeof...(Args)` 是唯一直接可得包信息的算子。本章 3.3 的所有自研物都是这三招的组合：
optional 用 placement new 在 `aligned_storage_t` 缓冲上按 `is_trivially_destructible` 决定是否登记析构；
function_traits 对 `R(Args...)`/成员指针各写一组偏特化"拆签名"；variant 把访问者双分派写成一个
`switch(index_) + cast` 的展开表。

### 2.3 三种"装异构值"的梯度（本章最重要的对比）
| 方案 | 类型信息在哪 | 布局 | 代价 |
| --- | --- | --- | --- |
| optional 自研 | 编译期已知 T | `[对齐缓冲][bool]`，无堆分配 | 每类型一份模板代码 |
| variant 自研 | 类型集编译期已知，持哪支运行期 | 最大成员 + tag | 访问必须分派/visit |
| any 自研 | 完全未知 | 指针 → 堆上"带虚表/函数指针的持有者" | 堆分配 + 间接访问 |
| `std::function` | 只知签名 | SBO 缓冲 + 指针 | 调用协议擦除而非类型擦除 |
梯度即权衡：知道得越多，运行时税越少。C++17 的 `std::optional/variant/any` 就是这条梯度的标准化。

### 2.4 三个自研应用件的机制速览（3.3 节"综合应用"的底座）
- **lazy 惰性对象**：典型实现是"构造 thunk + 对齐缓冲 + 已初始化标志"，首次 `get()` 才在缓冲上
  placement new——省掉的不是拷贝而是"未被用到的构造"。它至今未进标准：`std::expected`/ranges 的
  惰性各分走一部分场景，通用 lazy 无人收编。
- **dll 帮助类**：`注册表 = map<类型名字符串, 工厂函数>`，导出/导入两端靠同一张"名字→构造动作"表
  在运行期物化对象——RTTI 之外的第四种类型擦除（名字键），今天插件系统/COM 工厂的 C++ 直译版。
- **function_traits**：对 `R(Args...)`、函数指针、`std::function`、lambda、成员函数指针各写一组
  偏特化拆出 `return_type / arg_types`（tuple 承载）——第 9 章 IoC 容器"按签名注入"与第 10 章
  消息总线"按 topic 查表调用"的元信息都从这里来。

## 三、权衡与实战提示

- 递归展开的报错是模板深水区（实测 gnu++11 的第一条 error 常指在无关行）；今天用折叠表达式 + `if constexpr` 把这类代码量砍半。
- `aligned_storage` 手写 optional 的对齐/异常路径极易错——2015 年值得练，2026 年生产代码直接 `std::optional`。
- ScopeGuard 在 book 里的动机是 sqlite 事务回滚（[10 章](10-消息总线与SQLite封装.md)），它证明"RAII 的泛化形态=析构回调"。

## 四、相邻概念对比

见 2.3 表；另：SFINAE vs `if constexpr`——前者作用于**重载决议**（函数外部分支），后者作用于**函数体**
（分支代码不实例化）；概念（concepts）则把"约束"从隐式（替换失败）变显式（requires 子句，报错友好）。

| 对比项 | 差异一句话 |
| --- | --- |
| 自研 optional vs `unique_ptr` 表"可能没有" | 前者值语义、无堆、拷贝行为随 T；后者偷来堆分配且语义是"拥有"不是"有无" |
| 折叠表达式 vs 递归展开 | 一行 vs 四件套；折叠的实例化深度也更浅（诊断与编译期成本双收益） |

## 五、实测（🔧 四档：g++ 15.2，gnu++11/14/17/23，`ch03.cpp`）

```text
gnu++11: 编译失败——error: 'remove_reference_t' is not a member of 'std'（_t 别名属 C++14；泛型 lambda 亦是 C++14）
gnu++14: OK  输出 "is_int=1 / sizeof...=4 / recursion sum11=10 / pre-C++17: no fold/no optional/no variant"
gnu++17: OK  追加 "fold sum=10 / sizeof(optional<int>)=8 / sizeof(variant<int,double>)=16"
gnu++23: OK  同 17
```

- `sizeof(std::optional<int>)=8`：1 字节标志 + 对齐到 4 的 int——标准库实现同样无堆分配，与书中自研布局同构。
- `sizeof(std::variant<int,double>)=16`：tag + 最大成员 double 对齐，印证 2.3 的"最大成员 + tag"结论。
- 递归版 `sum11(1,2,3,4)=10` 与折叠版 `fold=10` 同值：C++11 手写四行递归 == C++14 一行折叠。
- 🔧 探针实测 `sizeof(std::any)=16`（libstdc++ x86_64，管理器指针+存储指针两枚）：完全擦除只留
  两个指针，对象本体外置堆上——与 2.3 表"自研 any＝指针→持有者"的布局结论同构。

## 六、最新演进与工业实践

- **C++14**：变量模板与 `_t` 别名、折叠表达式 `(args + ...)`、泛型 lambda——本章 80% 样板被官方语法糖溶解。
- **C++17**：`std::optional / std::variant`（提案 P0088R3《Variant: a type-safe union for C++17》，
  wg21.link/p0088 实测解析且标题亲验）`/ std::any`、`if constexpr`（P0292R2 实测）、`std::apply/invoke`——
  书中 3.3 的自研清单逐项失去生产理由；`variant + overloaded 模式`（见 [07 章](07-C++11重思设计模式.md)）成访问者现代写法。
- **C++20**：concepts（wg21.link/p0734 实测解析）把 `enable_if` 的隐式约束改写成 `requires`；
  ranges 借用本章的投影/迭代协议。展开见 [../C++20模板元编程.md](../C++20模板元编程.md) 与 [../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md](../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md)。
- **C++23**：`std::expected<T,E>`（P0792R14，wg21.link/p0792 实测解析至 r14）= optional + 错误携带，
  本书 ScopeGuard/返回码场景的制度性终点。
- **当年替代品的现状**：boost::optional→std 收编；folly::Optional/URI 等仍在生产；
  ScopeGuard 家族工业实现（folly/`boost::scope`，⚠️ boost 版本号未核）始终没进 C++ 标准，
  2026 年主流仍是手写 RAII 包装。
- **`_v`/`_t` 的现实形态**：libstdc++ 的 `_v` 别名只在 gnu++17 及以上可见（🔧 本次 ch03 四档中
  11/14 档需手写 `::value`/`::type`）——本章"语法税"的消失时点可用同一探针复现。
- **元编程教学对账**：本章精神史可上溯 [../C++模板元编程.md](../C++模板元编程.md)（Boost MPL 时代），
  下承 [../C++模板元编程实战.md](../C++模板元编程实战.md)（深度学习框架实例）；两本与本章互读。

## 七、交叉互链

- 大纲：[../深入应用C++11.md](../深入应用C++11.md)；总索引：[../C++系列·总索引.md](../C++系列·总索引.md)
- 条款版：[../Effective_Modern_C++/01-类型推导.md](../Effective_Modern_C++/01-类型推导.md)、[../Effective_Modern_C++/05-右值移动完美转发.md](../Effective_Modern_C++/05-右值移动完美转发.md)
- 教程线：[../现代C++实战30讲/10-可变模板tuple与类型擦除.md](../现代C++实战30讲/10-可变模板tuple与类型擦除.md)、[../现代C++实战30讲/08-模板编译期多态与编译期计算.md](../现代C++实战30讲/08-模板编译期多态与编译期计算.md)、[../modern-cpp-tutorial.md](../modern-cpp-tutorial.md)
- 语言核心视角：[../现代C++语言核心特性解析.md](../现代C++语言核心特性解析.md)
- 标准库事实：[../C++标准库/02-通用工具与智能指针.md](../C++标准库/02-通用工具与智能指针.md)
- C++17 增量：[../C++17完全指南.md](../C++17完全指南.md)
- 辨析：[../C++实战.md](../C++实战.md)（吴咏炜课程书对可变模板的处理更"专题化"，无自研库环节）
