# 附录 A–D + 从 MPL 到现代 C++ 的替代地图（Preprocessor Metaprogramming; typename/template; Compile-Time Performance; Portability; and the Modern Successors）

> 对应已核实中译本目录：附录 A 预处理元编程简介 ｜ 附录 B typename 和 template 关键字 ｜
> 附录 C 编译期性能 ｜ 附录 D MPL 可移植性摘要 ｜ 参考文献。
> 本文件承担双重任务：**逐附录精读** + **全书 11 章的现代替身总对账**（任务主题 10 的落点）。

## 核心概念速览（中英对照）

- **预处理元编程** — preprocessor metaprogramming（附录 A）：用 `#define` 做文本级生成式编程（Boost.Preprocessor 提供列表/循环/条件）；模板出现前时代的"另一个元语言"。
- **typename/template 双咒语** — 附录 B：依赖名规则——`typename` 声明"这是类型"、`template` 声明"这是成员模板"（`it->template get<T>()`）；SFINAE 与一切 `::type` 语法的语法地基。
- **编译期性能** — compile-time performance（附录 C）：以**实例化次数×深度**为单位的复杂度分析；TMP 程序的第一类资源问题。
- **可移植性摘要** — MPL portability（附录 D）：2004 年主流编译器（EDG 系/borland/mwcc 等）对成员模板偏特化、部分排序等特性的支持差异表——"库在方言上抽象"的历史标本。
- **替代地图** — 本文件自制：MPL 设施 → C++11/14/17/20/23 替身 → 仍无替身之处的三列总账。
- **Hana** — Boost.Hana：C++14 constexpr 重写的 MPL 后继（类型与值统一的元编程库）。
- **静态反射** — static reflection（P2996）：编译期读取程序实体（成员/名字/限定名）的语言设施；TMP 多数"手工 traits"的终局替代。
- **consteval / 缩写模板参数** — C++20 `P...`（`template<class... T> f(P...)`）与编译期函数：变参时代的"免 lambda"表达力。

## 本文件地图

```text
第一部分 附录精读: A 预处理器元编程 → B typename/template 语法地基 →
                C 编译期性能账本 → D 可移植性方言表(2004 博物馆) → 参考文献注记
第二部分 替代地图: 正文 11 章逐设施 → 标准替身 → 残余价值 三列对账(下表)
第三部分 仍无替身之处: 三块"标准还没接管/接管不完全"的硬骨头(见下)
```

## 仍无替身（或替身不完整）的三处——读 MPL 的最后正当理由

1. **"类型当数据流"的完整管道**：tuple/variant 覆盖了异构容器，但 MPL 式的"按运行时整数选编译期类型"
   （如按 `N` 展开固定大小缓存类型）仍需手写 `switch`+模板或依赖 `integral_constant` 桥——
   反射（P2996）路线成熟前，这一格仍是元编程独占领地（标准替身 ⚠️ 不完整）。
2. **跨序列的元算法**：`zip/transpose/幂集构造`一类在标准里始终缺席，Hana 有而 std 无——
   这正是第 6 章"自写算法"技能今天仍然活着的领域。
3. **零成本边界控制**：9.2 的标签分派在"需要不同可见签名"的接口上仍优于 `if constexpr`；
   concepts 只是把语法翻新，没有替代这个设计维度。

## 常见误区

- **误区一：把附录当"可跳过的历史"**。A 解释 MPL 的形状（为何 `_1.._5`、为何 vector0..20 家族），
  C 解释全书复杂度论证的计价单位，D 解释为什么 MPL 源码里满是 `#if BOOST_WORKAROUND`——
  跳过附录会让正文的"丑"变得不可理解。
- **误区二：认为"现代替身"意味着"可以不用学原语"**。`integral_constant`/`index_sequence` 本身
  就是 MPL 原语的标准收编；不懂装箱/拆箱语义，读不懂 `<type_traits>` 的一半 API。
- **误区三：拿替代地图反向歧视存量代码**。维护 Boost 存量（大量 MPL 在 Qt 旧版/Poco/各 ORM 中）
  是工业现实；[boostorg/mpl](https://github.com/boostorg/mpl) 未归档本身就是"该技能仍有市场"的凭证。

## 动机：附录是"元语言之外"的全部成本清单

正文 11 章讲"怎么算"，附录讲"算之前先付什么"：

- A：模板不够时人们曾向预处理器回流（生成 `tuple` 的 N 种偏特化宏），**这段历史解释了 MPL 为什么长满
  手工重复的 `_1.._5`、`vector0..vector20` 家族**——不是美学，是变参模板缺席的补偿。
- B：`typename` 规则是"模板作为语言"的语法税；读者在第 2/5 章见过的每一次 `typename X::type` 都欠它的债。
- C：编译期性能是 TMP 唯一的"性能工程"章节——实例化数量决定构建时间，`mpl::vector` vs `list` 的选择、
  `range_c` 的存在理由、fold 的成本模型，全部在此结账。
- D：可移植性是"编译器方言时代"的证物；今天 GCC/Clang/MSVC 对 C++17/20 的一致性使这类表格几乎消失，
  只在最前端特性上复现（P2996 实现状态即新例证）。

## 机制：四个附录各自的一句话技术内核

```text
A(预处理器): BOOST_PP_LIST_FOR_EACH / BOOST_PP_ENUM 生成重复片段
             → 缺陷: 无类型检查、调试黑洞 → C++11 变参 + 折叠接管 95% 场景
B(依赖名):   模板体内遇到 限定依赖名 时必须消歧:
               typename T::type     ← 宣告"类型"
               x.template f<T>()    ← 宣告"成员模板"
             规则根源: 编译器在实例化前不知道名字的意义 → 附录C的惰性实例化的语法面
C(编译期性能): 成本单位 = 类实例化次数 (+函数模板/别名展开)
             分析样例: fold 链 O(N) 深度受 -ftemplate-depth 钳制(默认当年 ~16-256, 今天 GCC 默认 900 ⚠️版本相关)
             优化手段: 树折叠/尾递归类型/惰性区间(range_c 不实例化中间元素)
D(可移植性):  2004 年 MPL 的 workaround 家族(如 is_convertible 的编译器专用分支)
             → 今天: ISO 测试集 + 三大实现高合规 → 仅剩"新特性进度差"(cppreference 支持表)
```

## 替代地图（正文 11 章逐设施对账）

| MPL 设施（章） | 现代替身（标准） | 残余价值 |
| --- | --- | --- |
| 元函数 + `::type`（2） | `std::` 类型萃取 + 别名模板 `remove_ref_t`；`if constexpr` | 概念本身仍是 `<type_traits>` 用户的地基 |
| 高阶元函数/lambda/apply（3） | C++20 concepts 约束、Hana 占位符、P2996 元对象 | "函数当参数"的类型层设计意识 |
| `bool_/if_/eval_if/integral_c`（4） | `conditional_t`、`integral_constant`、`if constexpr`、折叠 | `integral_constant` 仍是值↔类型唯一标准桥 |
| 序列 vector/list/map（5） | `std::tuple`、`integer_sequence`、`variant`、`index_sequence` | Hana 继续供给（未归档） |
| 算法 transform/fold（6） | 折叠表达式、`apply+index` 遍历、ranges | 算法词汇表设计仍教科书级 |
| 视图 transform/filter_view（7） | C++20 `views::transform/filter`（值层同名同义） | 概念先行的库设计方法 |
| assert_/诊断（8） | `static_assert`、concepts 诊断、`__PRETTY_FUNCTION__` | 主动布置断言的工程观 |
| for_each/标签分派/类型擦除/CRTP（9） | 折叠 for_each、约束重载、`std::function/any/variant visit`、CRTP 仍活着 | CRTP+反射组合是新语法 |
| ET/DSEL/Spirit（10–11） | 编译期/运行期统一：constexpr 容器、`std::format` 编译检查、X3；反射改写具名参数 | ET 在数值库长存 |
| 预处理器生成（A） | 变参模板 + 折叠（"95% 场景"为本目录判断） | 注册表/字符串化等 5% 仍用宏 |

## 权衡

- **读附录的史学方法**：A/D 的价值不在"该忘"，在"解释形态"——理解了预处理器补偿与方言差异，
  就理解了 MPL 为什么"重"（文件数、宏数、深层技巧）；这是任何"为什么 2004 的代码这么丑"的完整答案。
- **编译期性能的现代翻转**：附录 C 的"少实例化"在 C++20 后部分失效——折叠/constexpr 把成本搬进
  编译器前端；新的预算问题变成模板膨胀（代码大小、链接时间），Lakos 式物理设计重新相关
  （本仓库 [../大规模c++程序设计.md](../大规模c++程序设计.md) 主题衔接）。

## 最新演进与工业实践

- **C++11→23 逐项清单**（正文各章已分述，此处汇总）：变参模板/tuple/type_traits/index_sequence（11）→
  变量模板 + `_v`（14）→ `if constexpr`/折叠/`variant visit`/`std::apply`（17）→ concepts/requires/
  ranges/`<>` 缩写模板参数/`consteval`（20）→ 占位参数 `_`、`std::expected`（23）→
  **P2996 静态反射**（目标 C++26；[已核实当前 R13，2025 文档号](https://wg21.link/p2996)——
  注意提案演进中，措辞/设施名可能变动 ⚠️）。
- **库侧现状（全部实测可达）**：[boostorg/mpl](https://github.com/boostorg/mpl)（未归档、维护模式）、
  [boostorg/hana](https://github.com/boostorg/hana)（未归档、独立版停止）、
  [boostorg/fusion](https://github.com/boostorg/fusion)、[boostorg/xpressive](https://github.com/boostorg/xpressive)、
  [facebook/folly](https://github.com/facebook/folly)、[abseil/abseil-cpp](https://github.com/abseil/abseil-cpp)。
  结论：MPL 未死，但**新项目的默认答案是标准设施 + （必要时）Hana**——与 Boost 官方文档的"仍可用"立场一致
  （[MPL 文档](https://www.boost.org/doc/libs/release/libs/mpl/doc/index.html)已核实在线）。
- **诊断体验**（已实测 g++ 15.2）：`concepts_diag.cpp` 在 `-fconcepts-diagnostics-depth=3` 下输出
  "constraints not satisfied → no operand of the disjunction is satisfied → is_arithmetic_v<T> unsatisfied"
  的树状理由——对照第 8 章（本目录 [07](07-诊断.md)）的实例化回溯， TMP 可读性问题已发生**代际翻转**。
- **参考文献注记** ⚠️：原书「参考文献」条目未逐条核到可达 URL（C++ Report 停刊、genprog.org 域名已转手），
  本目录仅在 09 章保留书目线索，不伪造链接；可核实的当代锚点以上表仓库与 wg21 文档号为准。

## 互链

- 大纲笔记：[../C++模板元编程.md](../C++模板元编程.md) ｜ 索引：[../C++系列·总索引.md](../C++系列·总索引.md)
- 各概念的正文出处：[02-Traits与类型操纵.md](02-Traits与类型操纵.md)、[03-高阶元函数与lambda.md](03-高阶元函数与lambda.md)、
  [04-整型外覆器与布尔元编程.md](04-整型外覆器与布尔元编程.md)、[05-序列与迭代器.md](05-序列与迭代器.md)、
  [06-算法与视图适配器.md](06-算法与视图适配器.md)、[07-诊断.md](07-诊断.md)、
  [08-跨越编译期与运行期边界.md](08-跨越编译期与运行期边界.md)、[09-DSEL与表达式模板.md](09-DSEL与表达式模板.md)
- 物理设计衔接：[../大规模c++程序设计.md](../大规模c++程序设计.md)
- 现代替身的中文专著：[../C++20模板元编程.md](../C++20模板元编程.md)、[../深入实践C++模板编程.md](../深入实践C++模板编程.md)、
  [../C++模板元编程实战.md](../C++模板元编程实战.md)
- 总览与阅读地图：[00-总览与阅读地图.md](00-总览与阅读地图.md)
