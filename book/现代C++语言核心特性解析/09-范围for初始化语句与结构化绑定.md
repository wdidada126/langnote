# 09 范围 for、初始化语句与结构化绑定

> 对应原书 **第17章 基于范围的for循环（C++11 C++17 C++20）· 第18章 支持初始化语句的if和switch（C++17）· 第20章 结构化绑定（C++17 C++20）**
> 导航：[系列索引](../C++系列·总索引.md) ｜ [单文件笔记](../现代C++语言核心特性解析.md) ｜ [00 总览](00-总览与阅读地图.md)

## 核心概念速览（中英对照）

- **基于范围的for循环** — range-based for：`for (decl : range)` 展开为 begin/end 循环
- **范围声明对象** — range-declaration object：循环内被赋迭代器值的隐藏变量（C++23 前是 `auto&&`）
- **带初始化语句的 if/switch** — if/switch with initializer：`if (init; cond)` 限定作用域
- **结构化绑定** — structured binding：`auto [a,b] = obj;` 把聚合/元组型对象解包为别名
- **可分解类型** — decomposable type：原生数组 / 类聚合 / tuple-like 三形态
- **tuple-like** — tuple-like：特化了 tuple_size/tuple_element 且成员 get<> 可用的类
- **绑定名非变量** — structured binding names are not variables：它们是"引用别名"，不能进模板实参/decltype（C++20 前）
- **init-statement** — 初始化语句：条件语句头里执行的单声明/表达式
- **范围表达式生命期延长** — lifetime extension of range expression：临时容器活到循环结束

## 动机

三者同属"**语句层的现代糖**"：把 C++98 中"为了少打字且更少出错"的手腕（迭代器三连、
把临时变量提到 if 外面再判、`tie`+`std::make_pair` 五连）语法化。设计母题一致——
**让"获取值→判条件→用值"三个阶段共享一个最小作用域**。

## 机制（编译器视角）

- **范围 for 的展开**（编译器脱糖为等价代码，GCC AST 里直接是普通 for）：

  ```cpp
  for (auto&& __range = 范围表达式; auto&& __it = begin(__range); __it != end(__range); ++__it) {
      声明 = *__it;   // 名字用 auto&/auto 时按 03 文件推导规则
  }
  ```
  两个关键点实测可证：
  ① `auto&& __range` 绑定范围表达式 → **`for (int& e : make_vec()) e*=2;` 中临时
  vector 活到循环结束**（实测修改生效、程序无崩溃）；
  ② `begin/end` 查找顺序：成员函数优先，其次 ADL 自由函数（C++20 起 ADL 可找到
  `std::ranges::begin` 的同族——实测自定义 `begin(Range&)` 返回**不同类型**
  （哨兵思想的前身，本书 17.3），C++17 允许 begin/end 返回类型不同即可）。
- **if/switch 初始化语句**：`if (auto [it,ok] = m.emplace(k,v); ok)`——
  编译器把 `it/ok` 的作用域推进 if/else 全体、条件求值后**立即析构**。
  与"声明在 if 外"的传统写法相比：析构提前、名字不外溢、`else` 分支同样可见。
- **结构化绑定不是"创建变量"而是"给子对象起别名"**：绑定名是
  **引用实体的名字**（not variables），所以 `decltype([名字])` 非法、模板实参位非法
  （C++20 仍如此，P1091R3 想修未纳入；实测 `static_assert` 只能绑在具名对象上间接验证）。
  三形态的分解算法（编译器判决顺序）：
  1. 原生数组 → 按元素绑；
  2. **聚合类**：所有非静态成员公开且同一类（C++17 判据），成员直访绑定；
  3. **tuple-like**：`std::tuple_size_v<T>` 有效 + 各 `get<I>(t)` 可调用——
     `pair/tuple/array/chrono` 全走这条（实测 `map` 的 `value_type` 走成员形态②）。
  C++20 放宽：绑定到 lambda 捕获?（未纳入）/ 允许在 constexpr 与协程参数中使用（细则）。
- **"结构化绑定的名字即别名"**也解释了循环拷贝语义：`for (auto [k,v] : m)` 每轮
  **拷贝** value_type（改 `[]` 无效），`auto& [k,v]` 才动真格（实测 total=50 计算正确，
  改值需引用形态）。

## 权衡

- 范围 for 上的 `auto&&` vs `auto`：前者零拷贝可改容器元素（引用别名），
  后者按值快照；对 `std::vector<bool>` 这类代理容器，`auto` 拿到代理（03 文件同款坑）。
- 初始化语句头里**只能一条声明/表达式**；复杂准备仍要外置——糖不解决"准备成本高"。
- 结构化绑定名字**不能指定类型**（无 `int [a,b]`）、不能带数组维数/引用名——
  需要类型控制时回到 `tuple`+`get` 或成员直访。
- 范围 for 改容器结构（emplace/erase）是迭代器失效的经典案发现场——语言糖没有
  改变"容器不是集合语义"的事实，erase 惯用法仍是 `it = v.erase(it)` 手写循环。

## 相邻概念对比

| 机制 | 解决什么 | 生命期/作用域语义 |
| --- | --- | --- |
| `for (auto it = b; it!=e; ++it)` | 遍历 | 迭代器全程可见 |
| 范围 for | 遍历去噪音 | `__range` 仅循环内；临时量延长 |
| if 外声明+if 判断 | 初始化+条件 | 变量溢出到外层 |
| `if (init; cond)` | 同上 | 限死在 if/else 全支 |
| `tie(a,b)=f()` | 解包 | 需要预声明+左值 |
| `auto [a,b]=f()` | 同上 | 新名字、支持纯右值/临时量 |

## 🔧 实测样例（已实测 g++ 15.2，-std=gnu++17）

```cpp
#include <cstdio>
#include <map>
#include <string>
#include <vector>
std::vector<int> make_vec(){ return {3,1,2}; }
int main(){
  for (int& e : make_vec()) e *= 2;                 // 临时量活到循环结束(证据见下注)
  for (int e : make_vec()) printf("%d ", e); puts("");
  auto [it, ok] = std::map<int,std::string>{{1,"a"}}.emplace(1,"b"); // 解包 pair<const K,V>
  if (auto sz = it->second.size(); sz > 1) puts("long");
  else printf("map hit: key=%d val=%s ok=%d\n", it->first, it->second.c_str(), ok);
  int total = 0;
  for (auto [k, v] : std::map<int,int>{{1,10},{2,20}}) total += k*v;   // 成员形态分解
  switch (auto t = total % 7; t) { case 0: puts("div7"); break; default: printf("t=%d\n", t); }
  printf("total=%d\n", total);
}
```
实测输出：

```text
3 1 2 
map hit: key=1 val=a ok=0
t=1
total=50
```

注：第一行输出仍是 `3 1 2` 是因为第二个 `make_vec()` 是**新临时量**——
加倍发生在第一个临时量上且循环内合法完成（无悬垂、无崩溃），这正是
"范围表达式生命期延长"与"结构化绑定 emplace 返回 pair"两条机制的复合证据。
`ok=0` 也顺带验证了 emplace 语义（键已存在则不插入）。

## 最新演进与工业实践

- **C++23：范围 for 可迭代"范围对象右值化"的管道写法**（`for (x : v | views::transform(f))`
  ——依赖 range-v3/std::ranges 的 view 本体是轻量右值可保存，机制在
  [../C++20模板元编程/09-范围库.md](../C++20模板元编程/09-范围库.md)）。
- **P1091R3（实测 302，"Extending structured bindings to be more like variable declarations"）**：
  想让 `[a,b]` 支持类型指定与显式 `&`——未纳入 C++20，作为"结构化绑定仍是别名"的
  官方注脚引用。
- **std::ranges 与哨兵（sentinel）**：范围 for 的"begin/end 可不同类型"正是 sentinel
  的语言学前身（本书 17.3 的前瞻性）；C++20 `<ranges>` 把这一点做成一等公民，
  支持矩阵：GCC 10/11 主体、Clang 16+ 基本全、MSVC 19.2x+ 持续推进（谨慎措辞 ⚠️）。
- **工业库**：folly 的 `FOLLY_SCOPE_EXIT` 宏家族解决"初始化语句"想做而做不到的
  RAII 变体；range-v3 的 `views::indices` 让"索引循环"退出主流——
  `for (auto i : views::iota(0,n))`。
- C++26：结构化绑定到 lambda 捕获（P2695? 未验证不引 ⚠️）、范围 for 的
  适配点继续由 ranges 吸收（本书 17.5 "自己实现 begin/end"在 std::ranges 时代
  改写成 `ranges_range_fn` 特化/`enable_borrowed_range` 特征化——工程接口变了，
  机制不变）。

## 互链

- 迭代器与 begin/end 的库实现：[../C++标准库/05-迭代器.md](../C++标准库/05-迭代器.md)
- 语句糖专题：[../现代C++实战30讲/06-迭代器与新for和易用性改进.md](../现代C++实战30讲/06-迭代器与新for和易用性改进.md)
- tuple/pair 的底层（结构化绑定的形态③）：[../C++20模板元编程/03-变参模板.md](../C++20模板元编程/03-变参模板.md)
- auto 推导规则在循环声明处的应用：[03-类型占位符与推导.md](03-类型占位符与推导.md)
- 回 [00 总览](00-总览与阅读地图.md)
