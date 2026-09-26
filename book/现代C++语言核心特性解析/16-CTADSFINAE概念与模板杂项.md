# 16 CTAD、SFINAE、概念与模板杂项

> 对应原书 **第38章 类模板的模板实参推导（C++17 C++20）· 第39章 用户自定义推导指引（C++17）· 第40章 SFINAE（C++11）· 第41章 概念和约束（C++20）· 第42章 模板特性的其他优化（C++11 C++14）**
> 导航：[系列索引](../C++系列·总索引.md) ｜ [单文件笔记](../现代C++语言核心特性解析.md) ｜ [00 总览](00-总览与阅读地图.md)

## 核心概念速览（中英对照）

- **类模板实参推导** — CTAD（class template argument deduction）：`Box b(42)` 不写 `<int>`，C++17
- **隐式推导指南** — implicit deduction guide：编译器由每个构造函数生成的候选签名
- **用户自定义推导指引** — user-defined deduction guide：`Range(It,It)->Range<It>` 的"改形状"签名（C++17）
- **拷贝初始化优先** — copy-initialization preference：CTAD 对同类型源不走构造函数推导，避免套娃
- **聚合类型的 CTAD** — aggregate CTAD：C++20 才为无构造函数聚合体生成逐成员推导
- **替换失败非错误** — SFINAE：immediate context 内替换失败仅剔除候选，不是硬错误（C++11）
- **立即上下文** — immediate context：SFINAE 的作用边界，边界外（如实例化体内）是硬错误
- **概念** — concept：具名布尔约束，编译期谓词（C++20，std::concepts）
- **约束** — constraint / requires 子句：模板参数上的谓词门禁
- **原子约束与包含** — atomic constraint & subsumption：约束比较与重载消歧的偏序理论
- **requires 表达式** — 简单/类型/复合/嵌套四类要求
- **外部模板** — extern template：显式抑制本翻译单元的隐式实例化（C++11）
- **连续右尖括号** — `>>>` 词法解析解禁（C++11）
- **变量模板** — variable template：`template<class T> constexpr T pi`（C++14）
- **条件显式** — explicit(bool)：构造函数据条件切换隐式转换许可（C++20）

## 动机

本书最后五章是"模板语言层"的收拢：CTAD 回答"类模板能不能像 auto 一样省掉实参"；
推导指引回答"隐式规则推错/推不出时如何手工介入"；SFINAE 与概念是同一问题的两代答案——
**如何在编译期筛选重载候选并把报错说人话**；第 42 章则是编译器实现史的小额还债
（`>>>` 词法、friend 模板形参、实例化控制、变量模板、explicit(bool)）。

## 机制（编译器视角）

- **CTAD = 先造"伪构造函数候选集"再做重载分辨率**：编译器为类模板的每个构造函数生成
  一条隐式指引 `C(args)->C<类实参>`（模板类则外层参数与构造函数参数联合推导），
  `Box b(42)` 实例化出的就是 `Box<int>`——实测 `static_assert(is_same_v<decltype(b), Box<int>>)` 通过（见下）。
  两条工程红线：**explicit 构造函数不参与普通列表 CTAD**（`std::vector v{1,2}` 是 int 列表而非
  size/value，`v(1,2)` 才是 1 个 2）；**`Box b1(42); Box b2 = b1;` 不推成 `Box<Box<int>>`**——
  拷贝初始化优先用"同类型源"候选（实测 gnu++17 该 static_assert 干净通过）。
- **别名模板与聚合的推导都是 C++20 补丁**（38.4/38.5）：`std::less{}`（别名 → 特化）
  与无构造函数聚合体（下例 `Pair p{1,2}`）在 C++17 一律"推不动"——
  实测 gnu++17 报 `class template argument deduction failed`，gnu++20 输出 `pair=1 2`。
  lambda 类型（38.3）的用途同理靠推导链路打通：`decltype([]{})` 之类不可写类型名，
  只能靠 auto/CTAD 承载（呼应文件 05 的闭包类）。
- **推导指引（39 章）是"改形状"的钩子**：隐式指引只会照抄构造函数签名，
  需要"从迭代器对推出 `Range<It>`、从 `T*` 推出值类型"这类**非照抄**关系时手写一条
  `Range(It, It) -> Range<It>;`——它与隐式指引同池竞争，失败可回退；
  聚合类没有构造函数可抄，指引几乎是唯一入口（39.2）。
- **SFINAE 的"替换"发生在候选签名层面**：编译器对每个候选用推导出的实参**只替换一次签名**，
  立即上下文（参数列表/返回类型/默认模板参数）内出现非法类型 → 静默剔除候选；
  替换过程外部（函数体实例化、非直接使用的嵌套 typedef 展开深处）的失败是硬错误。
  `enable_if_t<!cond>` 故意让"不满足"变成"无类型"，把布尔判定伪装成替换失败——
  实测报错误直插 `<type_traits>` 头文件内部（见下），这正是它被概念取代的病灶。
- **概念 = 一等公民的编译期谓词**（41 章）：`template<std::integral T>` 或
  `requires integral<T>` 把"筛选条件"从签名花招提升为独立语法；重载消歧用**约束包含
  （subsumption）**偏序——更严格的可行候选胜出，这在 SFINAE 时代做不到（同名候选全打平）；
  requires 表达式四形态：简单（表达式合法）、类型（`typename T::value_type`）、
  复合（`{e} -> std::same_as<bool>` 带 noexcept）、嵌套（`requires C<T>`）。
  原子约束把每个具名 concept 调用记为一个不可分单元，是"编译器内部比较约束"的最小颗粒（41.5）。
- **第 42 章杂项的编译器底色**：
  ① `extern template class std::pair<int,int>;`——告诉实例化器"别在本 TU 生成，链接期去找"，
  实测 gnu++20 编译通过，这是模板实例化去重（减少 bloat/构建时间）的原始武器；
  ② `>>>` 词法：C++98 词法器最大前缀匹配把 `>>` 咬成移位 token，实测 gnu++98 报
  `'>>' should be '> >' within a nested template argument list`，C++11 起模板上下文中可再拆；
  ③ friend 声明自带模板形参表（C++11 前必须先有命名域声明），实测 gnu++11 编译运行通过、
  经 ADL 可见；gnu++98 下 GCC 15.2 未对此样本设卡（⚠️ 历史限制以标准文本为准，如实登记实测）；
  ④ 变量模板与 ⑤ `explicit(!storeable<T>)` 见下方实测。

## 权衡

- CTAD 省的是**调用侧噪音**，代价是**类型不再自证**：头文件/接口里暴露 `Box b(...)` 的下游
  全部隐式绑定推导规则，标准库容器因此补了大量指引；公共 API 仍宜写明实参（Google 风格
  对"推导歧义"敏感），库内实现才享受 CTAD。
- SFINAE 通用但诊断差、且"默认参数技巧"可被 `= void` 撞车——需要标签分发等补丁；
  概念可读性好、诊断精确，但**约束写得太宽等于没写**（`requires sizeof(T)>0` 这类
  空洞概念不提供 subsumption 信息）。迁移期库普遍双轨（range-v3/folly）。
- `enable_if_t` 用在返回类型会污染签名、用在默认参数不占 ABI——位置不同报错形态与
  重载集行为不同，这是 40.2 规则细节日志的来源。

## 相邻概念对比

| 维度 | 旧一代 | 新一代 | 分界 |
| --- | --- | --- | --- |
| 类模板实参 | 手写 `Box<int> b(42)` | CTAD `Box b(42)` | C++17（聚合/别名再等 C++20） |
| 推导改形状 | 静态工厂函数模板 `make_X` | 推导指引 | C++17 后工厂可退场 |
| 候选筛选 | SFINAE/`enable_if` | concept/requires | C++20 |
| 实例化控制 | 全隐式 | `extern template` + 显式实例化 | C++11 |
| 条件 explicit | 代理类型/`delete` 重载 | `explicit(bool)` | C++20 |

## 🔧 实测样例（已实测 g++ 15.2）

CTAD + 用户自定义指引 + 聚合对照（gnu++17 / gnu++20）：

```cpp
template<class T> struct Box{ T val; Box(T v): val(v){} };
template<class It> struct Range{ It b, e; Range(It x, It y): b(x), e(y) {} };
template<class It> Range(It, It) -> Range<It>;      // 用户自定义推导指引
template<class T> struct Pair { T a, b; };          // 无构造函数聚合体
int main(){
  Box b(42);      static_assert(std::is_same_v<decltype(b), Box<int>>);
  int arr[4] = {1,2,3,4};
  Range r(arr, arr+4); static_assert(std::is_same_v<decltype(r), Range<int*>>);
  int s=0; for (auto* p = r.b; p != r.e; ++p) s += *p; printf("range sum=%d\n", s);
  Pair p{1, 2};   // 聚合 CTAD：C++17 编译失败，C++20 通过
}
```

gnu++17：`Box`/`Range` 两行断言通过、运行输出 `range sum=10`，`Pair p{1, 2}` 实测报：

```text
error: class template argument deduction failed:
error: no matching function for call to 'Pair(int, int)'
```

同一文件换 gnu++20 编译运行输出 `pair=1 2`。另实测拷贝初始化不套娃：
`Box b1(42); Box b2 = b1;` 的 `is_same_v<decltype(b2), Box<int>>` 在 gnu++17 干净通过。

SFINAE vs 概念的报错形态（同一意图，`legacy_sfmate(3.5)` / `modern(3.5)`，均 gnu++20）：

```text
// SFINAE：错误钻进 <type_traits> 头文件内部
error: no matching function for call to 'legacy_sfmate(double)'
note: candidate 1: 'template<class T, class> T legacy_sfmate(T)'
.../include/c++/type_traits: In substitution of '... enable_if_t [with bool _Cond = false; _Tp = void]':
.../type_traits:2837:11: error: no type named 'type' in 'struct std::enable_if<false, void>'
// 概念：候选行自带约束，末行点名失败表达式（行数相近，但每行都指向用户代码/约束本体）
error: no matching function for call to 'modern(double)'
note: candidate 1: 'template<class T>  requires  integral<T> T modern(T)'
note: constraints not satisfied
.../concepts:109:24: note: the expression 'is_integral_v<_Tp> [with _Tp = double]' evaluated to 'false'
```

（如实登记：概念版行数并不更少，差别在**信息指向**——SFINAE 要用户自己从
`enable_if<false>` 反推"哪个 trait 不满足"，概念直接给出失败谓词与实参。）

第 42 章杂项合样（gnu++20 编译运行通过，静态断言全部成立）：

```cpp
template<class T> constexpr T pi = T(3.14159265358979323846L);   // 变量模板
template<class T> constexpr bool storeable = sizeof(T) <= 8;
template<class T> struct Wrapper{
  explicit(!storeable<T>) Wrapper(T v): val(v) {} T val;          // explicit(bool)
};
extern template class std::pair<int,int>;                          // 外部模板
```

实测输出：

```text
pi<float>=3.14 pi<long double>=3.1415926536
w=5
```

（`Wrapper<short> w = 5;` 隐式转换成立——short 可存储 → explicit(false)；
`long double` 版则被 `!is_convertible` 断言锁死。）`>>>` 词法与 friend 模板形参实测见
「机制」节 verbatim 错误。

## 最新演进与工业实践

- **C++23 三件套本机实测（g++ 15.2，-std=gnu++23）**：`std::expected` 单算子链
  （P2505R5，实测 302）、`std::generator` 协程产流（提案号见文件 14；标题机读 ⚠️ 未提取成功，
  仅引库设施名）、P0847R7 deducing this（实测 302）同框编译运行：
  `expected=8 / gen sum=6 / deducing-this=1.5`——deducing this 让 `Pt::dist(this const Pt&)`
  这样的成员函数模板式手写多态成为过去，也是概念时代 CRTP 的减重方案。
- **CTAD 的后续**：`std::type_identity`（C++20，P0846R0 实测 302 附带）关闭推导占位需求；
  本书第 38/39 章设施在 C++23/26 未再扩，属"已定稿"特性。
- **概念生态**：P0898R2（std::concepts，实测 302）是 41 章标准库概念集出处；
  C++26 反射 P2996R13（实测 302，注意**不是** P2562——勘误见文件 00）有望把"手写
  聚合约束"换成结构化反射校验。GSL 与 range-v3 已全面 concepts 化；folly 仍保留
  `FOLLY_REQUIRES` 双轨宏；abseil 以 C++17 为底线、SFINAE 为主（`ABSL_INTERNAL` 系），
  是"约束写法迁移成本"的活样本。
- **SFINAE 的退役姿势**：新代码用概念；`requires` 表达式的 SFINAE 等价物
  （`decltype(void(f(x)), int())` 探测串）仅维护旧库时保留——诊断差异见上实测。
- **工程纪律**：CTAD 在头文件中慎用于跨 TU 暴露的模板（推导规则变更=静默 ABI 变更）；
  `extern template` 与 `-fno-implicit-templates` 组合仍是大型工程（Chrome/LLVM 级别）
  控制模板 bloat 的手段，配合 `__clang__/libstdc++` 的实例化统计工具链使用。

## 互链

- auto/decltype 推导总论：[03-类型占位符与推导.md](03-类型占位符与推导.md)
- 聚合体与列表初始化（CTAD 撞车现场）：[06-初始化家族与聚合类型.md](06-初始化家族与聚合类型.md)
- 隐式指引的"构造函数"来源：[07-特殊成员函数与继承构造.md](07-特殊成员函数与继承构造.md)
- lambda 类型与 std::function：[05-lambda表达式与闭包.md](05-lambda表达式与闭包.md)
- 变参模板的约束化消费端：[15-可变参数模板与模板参数优化.md](15-可变参数模板与模板参数优化.md)
- 纵深对照（概念与约束全书版）：[../C++20模板元编程/06-概念和约束.md](../C++20模板元编程/06-概念和约束.md)、
  [../C++20模板元编程/05-类型特征和条件编译.md](../C++20模板元编程/05-类型特征和条件编译.md)、
  [../深入应用C++11/03-type_traits与可变参数模板.md](../深入应用C++11/03-type_traits与可变参数模板.md)
- 回 [00 总览](00-总览与阅读地图.md)
