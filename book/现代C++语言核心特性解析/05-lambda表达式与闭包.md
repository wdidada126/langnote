# 05 lambda 表达式与闭包

> 对应原书 **第7章 lambda表达式（C++11～C++20）**
> 导航：[系列索引](../C++系列·总索引.md) ｜ [单文件笔记](../现代C++语言核心特性解析.md) ｜ [00 总览](00-总览与阅读地图.md)

## 核心概念速览（中英对照）

- **闭包类型** — closure type：编译器为每个 lambda 合成的唯一匿名类（C++11 起"每个 lambda 一个类型"）
- **闭包对象** — closure object：闭包类型的实例，`auto f = [](int x){...};` 的 f
- **捕获列表** — capture list：`[=]/[&]/[x]/[this]` 声明哪些外围名字成为闭包成员
- **初始化捕获（广义捕获）** — init-capture：`[p = std::move(up)]`，C++14 把移动塞进闭包构造
- **按值/按引用捕获** — by-value / by-reference capture：拷贝进闭包 vs 存引用（悬垂边界）
- **无状态 lambda** — stateless lambda：无捕获时可隐式转函数指针
- **泛型 lambda** — generic lambda：`[](auto x){}`，C++14，实现为"闭包 operator() 是模板"
- **捕获 this / *this** — capture this / capture *this：`[=,this]`(C++17) 显式化；`[*this]`(C++17) 拷贝宿主对象进闭包
- **mutable 说明符** — mutable：解除"operator() 默认 const"，按值捕获可变
- **constexpr lambda** — C++20：满足条件即可参与常量求值
- **模板语法 lambda** — template-parameter lambda：`[](auto... xs){}` 之外 `[]<class T>(T x){}`，C++20

## 动机

在 lambda 之前，"把一小段逻辑连同其环境交给算法"需要：定义 functor 类 + 手写成员与
构造函数 + 实例化传参——三行意图被摊成十五行样板。函数指针又带不了环境。lambda 的
设计目标就是**把 functor 的样板压缩成表达式**，且零额外开销（它本来就是 functor）。

## 机制（编译器视角）——本书卖点章

编译器把 lambda **lowering 成一个闭包类**，本节全部用实测取证（g++ 15.2）：

1. **类合成**：`adder` 里的 `[base](int x){return x+base;}` 变成
   `struct closure{ int __base; int operator()(int x) const { return x + __base; } };`
   捕获变量成为**成员**（`__base`），参数成为 `operator()` 形参。
   证据 A（`objdump -d --demangle` 真实符号）：
   `adder(int)::{lambda(int)#1}::operator()(int) const` 是 exe 里一个**实打实的函数符号**。
   证据 B（`-fdump-tree-all` 的 GIMPLE original dump）：
   `const int base [value-expr: __closure->__base];`——`base` 被替换为**闭包指针取成员**，
   `operator()` 的第一个隐藏参数就是 `__closure`。
2. **sizeof 即成员之和**：实测 `sizeof(f)=4`（一个 int 捕获）、`sizeof(g)=8`（捕获 int&，
   存的是 8 字节引用/指针）、`sizeof(stateless)=1`（空类最小 1 字节）。
3. **无状态转换**：闭包类带 `operator int(*)(int)()` constexpr 隐式转换 →
   `int (*fp)(int) = stateless;` 实测 `fp(100)` 通过函数指针调用成功。
   代价：函数指针路径上优化器丢失内联机会，STL 算法优先直接传闭包对象。
4. **mutable 是签名手术**：默认 `operator() const`；`mutable` 去掉 const，按值成员才可改。
5. **泛型 lambda = 成员模板**：`[](auto x){}` 编译为闭包类的 `template<class T> operator()(T)`
   ——与函数模板同一套推导，因此它**不是** `std::function`（后者需要具体签名，实测
   捕获+多态并存时 sizeof 仍只算捕获，模板参数不占对象空间）。
6. **init-capture 直接构造成员**：`[p=std::move(up)]` 把 up 的指针窃取**写进闭包构造的
   成员初始化列表**，C++11 靠 `[&]{ p2=std::move(up); }` 的绕行方案寿终正寝。
7. **捕获 `this` vs `*this`**：`[this]` 存对象指针（悬垂=悬垂对象）；`[*this]`(C++17)
   整体拷贝宿主（闭包膨胀但自治）。C++17 起裸 `[=]` 隐式捕获 this 被弃用（P0806 语境），
   C++20 报错——本书 7.9 节专门处理。⚠️ 原书小节措辞未逐字核实，语义按标准描述。

## 权衡

- **捕获即拷贝/引用，闭包生命期 > 作用域时引用捕获是悬垂重灾区**：返回 lambda、
  存进回调表、线程任务，三条经典事故线都踩中"栈帧死了、引用成员还活着"。
- `std::function` 类型擦除：堆分配（大闭包 SBO 之外）+ 间接调用；`auto` 持闭包、
  模板传参是零开销正解——只有需要"存进异构容器/跨 ABI 边界"才付 type-erasure 税
  （C++标准库 06 章有 function 的实现侧成本分析）。
- 递归 lambda：闭包类型不完整不能自捕获，需要 `y_combinator`/`std::function` 或
  C++23 deducing-this 直接写（见文件 16 实测 `this auto` 样例）。

## 相邻概念对比

| 载体 | 带环境 | 可内联 | 可存容器 | 转换函数指针 | 典型成本 |
| --- | --- | --- | --- | --- | --- |
| 函数指针 | ✗ | ✗(间接) | ✓ | — | 间接跳转 |
| functor 类 | ✓ | ✓ | ✓ | ✓(可写) | 样板代码 |
| lambda/闭包 | ✓(捕获=成员) | ✓ | auto 可、function 需类型擦除 | 仅无状态 | 近乎零 |
| std::function | ✓ | ✗(虚/间接) | ✓ | ✗ | 分配+间接 |

## 🔧 实测样例（已实测 g++ 15.2，-std=gnu++17）

```cpp
#include <cstdio>
auto adder(int base){ return [base](int x){ return x + base; }; }
int main(){
  int n = 7;
  auto f = adder(10);                    // 捕获 int base（拷贝）
  auto g = [&n](int x){ return x + n; }; // 捕获 int& n
  auto stateless = [](int x){ return x; };
  printf("f(5)=%d g(5)=%d sizeof(f)=%zu sizeof(g)=%zu sizeof(stateless)=%zu\n",
     f(5), g(5), sizeof(f), sizeof(g), sizeof(stateless));
  int (*fp)(int) = stateless;            // 无状态 → 函数指针
  printf("via fnptr: %d\n", fp(100));
}
```
实测输出：

```text
f(5)=15 g(5)=12 sizeof(f)=4 sizeof(g)=8 sizeof(stateless)=1
via fnptr: 100
```

lower 取证（同一 TU）：

```text
$ objdump -d --demangle a.exe | grep operator
000...440 <adder(int)::{lambda(int)#1}::operator()(int) const>:
000...464 <main::{lambda(int)#1}::operator()(int) const>:
$ grep base s04.cpp.*.original          # -fdump-tree-all
  const int base [value-expr: __closure->__base];
```

`sizeof(f)=4`（闭包=int 成员）、`sizeof(g)=8`（引用成员=指针宽度）、空闭包 1 字节——
**"lambda 就是那个类"被 sizeof 直接量出来了**。

## 最新演进与工业实践

- **C++20**：模板参数 lambda `[]<class T>(T a, T b){...}`；constexpr lambda；`[=, this]` 
  成为强制写法；P0780R2 **init-capture 中允许包展开** `[...xs = std::move(args)]`
  （wg21.link/p0780 实测 302，落地标题 "Allow pack expansion in lambda init-capture"，
  与文件 15 变参模板直接相关）。
- **C++23**：P2809 折叠进 lambda 捕获?（⚠️ 未实测号不引）；实质可用的是
  **deducing this（P0847R7，实测 302）** 终结递归 lambda hack：
  `auto sum = [](this auto&& self, int n){ return n ? n + self(n-1) : 0; };`
- **libstdc++/libc++/MSVC 支持面（谨慎矩阵）**：泛型 lambda 三家自 C++14 模式即全；
  `[=,this]` GCC 8.1/Clang 7/MSVC 19.23；constexpr lambda GCC 9.1/Clang 6/MSVC 19.2x
  ——以上版本号出自编者记忆与编译器文档综合，未逐版验证 ⚠️；本机 g++ 15.2 对
  C++20 全部 lambda 特性实测通过（gnu++20 模式编译无警告）。
- **工业库**：range-v3 的视图管道 `ranges::views::filter([](auto x){...})` 把泛型 lambda
  用成了"第二语法"；folly::coro 协程体里 lambda 捕获生命周期有专门文档条款（悬垂任务=
  捕获引用+co_await 的经典事故组合，呼应文件 14）；GTest 的 `MATCHER` 宏底层也是闭包。
- STL 侧（[../C++标准库/06-函数对象与Lambda.md](../C++标准库/06-函数对象与Lambda.md)）：
  算法+lambda 是 C++11 后标准库最大的组合拳；`for_each_n`/`transform` 的谓词形参
  文档都假设你能读闭包语义。

## 互链

- 值类别是捕获拷贝/移动的根：[04-右值引用移动语义与完美转发.md](04-右值引用移动语义与完美转发.md)
- constexpr lambda 在常量体系中的位置：[10-静态断言与常量表达式体系.md](10-静态断言与常量表达式体系.md)
- 条款实践：[../Effective_Modern_C++/06-lambda表达式.md](../Effective_Modern_C++/06-lambda表达式.md)
- 库实现视角：[../C++标准库/06-函数对象与Lambda.md](../C++标准库/06-函数对象与Lambda.md)、[../现代C++实战30讲/09-函数对象lambda与函数式编程.md](../现代C++实战30讲/09-函数对象lambda与函数式编程.md)
- 函数调用符语意学（operator() 的底层）：[../深度探索C++对象模型/04-Function语意学.md](../深度探索C++对象模型/04-Function语意学.md)
- 回 [00 总览](00-总览与阅读地图.md)
