# 第 2 章 Traits 和类型操纵（Traits and Type Manipulation）

> 对应已核实中译本目录：2.1 类型关联（直接方式/迂回方式/捷径）｜2.2 元函数｜2.3 数值元函数｜
> 2.4 在编译期作出选择（iter_swap、美中不足、外覆器）｜2.5 Boost TypeTraits 程序库概览（一般知识/
> 主类型归类/次类型归类/类型属性/类型之间关系/类型转化）｜2.6 无参元函数｜2.7 元函数的定义｜2.8 历史｜
> 2.9 细节（特化/实例化/多态）｜2.10 练习。
> 本章是全书的"λ演算 + 类型系统"层：traits、元函数、`::type` 约定、nullary 约定在此一次立规。

## 核心概念速览（中英对照）

- 特性/traits — traits class：以嵌套类型或静态成员把"关于 T 的知识"关联到 T 上的类模板惯用法（本书 2.1"类型关联"）。
- 元函数 — metafunction：带类型参数的类模板；调用=实例化，返回=嵌套成员（`::type`/`::value`）。
- 元函数类 — metafunction class：2.7 术语，把"带 `apply` 嵌套成员的类"当编译期函数对象——第 3 章高阶元函数的地基。
- 主类型归类 — primary type categorization：`is_void/is_pointer/is_reference` 等互斥 predicates，2.5 对 Boost.TypeTraits 的巡礼。
- 次类型归类/类型属性/类型关系/类型转化 — secondary categorization / type properties / type relations / type transformations：traits 库的四族设施，C++11 全盘收编进 `<type_traits>`。
- 无参元函数约定 — nullary metafunction：每个元函数结果本身也是"可再取 `::type` 的类"，使 `if_` 与 `eval_if` 能统一处理（2.6，与第 4 章呼应）。
- 外覆器 — wrapper："美中不足"的解药——把 `::type` 与 `::value` 统一装箱，让选择结构不必关心分支是类型还是值（2.4.4）。
- 类模板局部特化 — partial specialization：元函数的分支语句；2.9.1 讨论匹配与"最特殊者优先"规则。
- 实例化 — instantiation：模板实体化的单位；既是计算模型（一次实例化=一次归约步）也是成本模型（编译时间账本）。
- iter_swap — 编译期选择案例：按迭代器类别选择交换实现，示范"if 语句→特化选路"的标准翻译。

## 本章地图

```text
2.1 类型关联        → 三段式: 直接(为每类型手写)→迂回(重载探测)→捷径(traits 定型)
2.2 元函数          → 类模板=编译期函数, ::type=返回类型
2.3 数值元函数      → 第二条返回通道 ::value 的确立
2.4 编译期作出选择  → iter_swap 案例 + "美中不足"系列 → 引出外覆器雏形
2.5 TypeTraits 概览 → 五族设施巡礼(归类/属性/关系/转化)——今天的 <type_traits> 目录
2.6 无参元函数      → nullary 统一约定(if_ 与 eval_if 得以同构)
2.7 元函数的定义    → 元函数类 apply 协议(第 3 章入口)
2.8 历史 / 2.9 细节(特化匹配/惰性实例化/类型层多态) / 2.10 练习
```

## 机制再走一步：为什么"捷径"恰好是 traits 而非重载探测

2.1 迂回路线（重载+`sizeof` 探测）能拿到的只有整数值；要"返回一个类型"（如元素类型、对应迭代器类型），
值通道无法承载——于是类型通道必须借道类模板的嵌套 typedef。两条通道并立（`::type` / `::value`）
自此成为 MPL 全部 API 的签名语法。代价也要当面算清：

- 每个"调用"都伴随一次类实例化（计算被编译器的实例化引擎执行，无栈、无步点）；
- 取值要用 `typename` 消歧、取类型要用 `::type` 解包——语法税由附录 B 全额记账；
- 特化匹配是静态的：不存在"运行时决定用哪个 traits"，那正是第 9 章标签分派要解决的缺口。

## 动机：类型层需要一个"带返回值的函数"语法，但语言没给

2.1 的三段式（直接→迂回→捷径）是全章灵魂，也是 2004 年 TMP 教学的最优路径：

1. 直接方式：想为每个类型 T 关联一个"对应迭代器类型"，最自然是写 `iterator<T>::type`——问题是没有通用
   设施时得为每个 T 手写特化，且无法为"第三方类型"补信息（闭开两难）。
2. 迂回方式：借道函数模板重载（`sizeof(test(declval<T>()))` 类探测）获得"值"——能算，但拿不到"类型"，
   而且不可组合（值无法再被特化匹配）。
3. 捷径（traits 的定型形态）：类模板的嵌套 typedef + 针对具体类型的偏特化 + 对开放类型的"派生自 traits 特化"
   外挂（`std::iterator` 时代风格）。类型关联的通用形式被确立：`T 的信息 = T 的某个伴生类模板实例的嵌套成员`。

这个设计同时把"函数调用语法缺失"变成了机会：`X::type` 读起来像取成员，实际是"调用并取返回值"；
`is_pointer<T>::value` 是"调用并取布尔"。2.2 顺势把类模板重命名为"元函数"，2.3 定义"数值元函数"
（返回 `value` 的元函数）——两条返回通道（类型/值）贯穿全书。

## 机制：调用、分支与类型层的 if

```cpp
// 🔧 2.4 的 iter_swap 案例,以 2004 风格重写(历史语境,已在本机以等价手写版实测语法形状 g++ 15.2)
template <class Iterator> struct iterator_category { using type = struct input_tag; }; // 默认
template <class T> struct iterator_category<T*> { using type = struct forward_tag; };  // 特化=分支

template <class It> void iter_swap_impl(It a, It b, input_tag)   { /* 三步交换 */ }
template <class It> void iter_swap_impl(It a, It b, forward_tag)  { std::iter_swap(a, b); }

template <class It>
void iter_swap(It a, It b) {
    iter_swap_impl(a, b, typename iterator_category<It>::type{});  // 类型→值参数:标签分派雏形
}
```

三条机制要点：

- `::type` 是类型层的"解包"；分支发生在特化匹配，不在函数体——元函数体内写 `if` 毫无意义（2.9 展开）。
- 选择结构雏形（2.4"编译期作出选择"的 if/else 等价物）：用两个偏特化表达"条件成立取 A 否则取 B"，
  这就是后来 `mpl::if_c` 的原型（第 4 章产品化）。
- nullary 统一约定（2.6）：规定"任何元函数的返回物也带 `::type`"，于是"返回类型的分支"与"返回值的分支"
  可共用同一外壳——MPL 的 `if_`（作用于元函数）因此能优雅实现（3.5.4"懒惰"的重要性在此埋下伏笔：
  只有让 `::type` 延迟到被取用时才实例化分支，未选分支才不会过早报错）。
- 2.9 细节三题：特化的部分排序决定哪个匹配胜出（重载决议的类型层镜像）；实例化是惰性按需的
  （成员定义不实例化，这保证元函数"只算要用的"）；多态靠"同一 traits 接口 + 不同特化"实现——
  编译期的子类型替换不存在，ad-hoc 多态在类型层全部走特化，regular 多态走迭代器类别这类标签。

## 权衡

- traits 把开放扩展（任何人可为新类型加特化）和编译期可判定同时买到；代价是：信息必须"以类型/常量
  形式存在"，任何运行期才可得的知识都进不来；以及 `typename`/`::type` 的仪式感（附录 B 专治这个）。
- 与 2.1"直接方式"对比：特化方案不可"集中修改"（加一条规则=加一个特化，散布全工程）；这是后来
  concepts（约束聚合）与反射（信息内建）分别攻击的痛点。
- Boost.TypeTraits（2.5 巡礼对象） vs 当年手工 traits：前者"广度"（50+ 个标准谓词），后者"深度"（自定义关联）。
  C++11 之后前者已被 `<type_traits>` 全面替代——2.5 整节今天应当直接对照 `std::` 版本读。

## 相邻概念对比

| 设施 | 信息载体 | 扩展方式 | 现代归宿 |
| --- | --- | --- | --- |
| traits 类 | 嵌套 `::type`/`::value` | 偏特化/派生 | `<type_traits>`、区间迭代器 traits（活得好好的） |
| 探测技巧（2.1 迂回） | `sizeof` 结果 | 重载决议 | SFINAE 惯用法（`std::void_t` 化） |
| 外覆器（2.4.4） | 统一装箱的类型 | — | `integral_constant` |
| 元函数类（2.7） | 带 `apply` 的类 | 特化/lambda | `mpl::lambda` → Hana 一等函数 → （反射后部分失去意义） |

## 最新演进与工业实践

- C++11：`<type_traits>` 标准化了 2.5 的全部巡礼（谓词/变换如 `remove_reference`、`conditional`），
  2.1–2.4 的手工 traits 在新代码里不应再出现；`using` 别名模板省掉一半 `typename ...::type`。
- C++14/17：变量模板（`is_pointer_v`）与别名模板（`std::void_t`）把 traits 从"类模板仪式"降级为
  "读起来像布尔常量"；`if constexpr`（17）直接吃 traits 的 `::value` 当分支条件——本章的"类型层 if"
  正式并入语句层。
- C++20/23：concepts 用"约束"替代一部分 SFINAE 探测（"2.1 迂回方式"的精神继承者）；
  `std::type_identity` 补齐恒等变换。P2996 静态反射（[已核实，当前 R13](https://wg21.link/p2996)）
  的元对象若按现行措辞落地，将为"为第三方类型关联信息"提供 traits 之外的第二条正路。
- 已实测 g++ 15.2：本章示例的标签分派新旧对照在 `dispatch_old_new.cpp` 中编译运行通过
  （tag dispatch old = 5, if constexpr new = 5）；`if constexpr` 版直接以
  `std::iterator_traits<It>::iterator_category` + `std::is_convertible_v` 表达，零手工 traits。
- 工业实践：现代库仍以 traits 为骨架（标准库 allocator/iterator traits、Qt 的 type traits 层），
  但惯例改为"组合 `std::` 设施"而非新造；folly 的 `IsRelocatable` 一类"开放 traits + 显式 opt-in"
  是 2004 风格在 2020s 的直系后代——证明"类型关联"这一抽象不过时，过时的只是 `::type` 写法。

## 互链

- 大纲笔记：[../C++模板元编程.md](../C++模板元编程.md) ｜ 系列索引：[../C++系列·总索引.md](../C++系列·总索引.md)
- 上一章：[01-概述与元编程的动机.md](01-概述与元编程的动机.md)
- 下一章（把元函数当参数传——高阶与 lambda）：[03-高阶元函数与lambda.md](03-高阶元函数与lambda.md)
- 布尔与外覆器的产品化：[04-整型外覆器与布尔元编程.md](04-整型外覆器与布尔元编程.md)
- 同类中文讲解（C++11 视角）：[../深入实践C++模板编程.md](../深入实践C++模板编程.md)、[../C++20模板元编程.md](../C++20模板元编程.md)
- SFINAE 探测的现代工程化标本：[../C++模板元编程实战.md](../C++模板元编程实战.md)
