# 第 3 站 · STL 总览：六件套的世界观（原书第 6 章）

> 覆盖原书第 6 章「标准模板库」：组件、容器分类、迭代器、算法与区间、迭代器适配器、
> 元素必要条件、value vs reference 语义、STL 内部错误、扩展 STL。
> 第 6 章是全书的「宪法」：之后四站（04–07）分别在它授权的领地里细究。

## 核心概念速览（中英对照）

- **STL 六组件** — STL Components：容器、迭代器、算法、函数对象、适配器、分配器——正交组合是设计核心。
- **区间** — Range：`[begin, end)` 左闭右开协议；一切算法以「一对迭代器」为输入输出界面。
- **多重区间** — Multiple Ranges：`mismatch/equal/lexicographical_compare/set_*` 类算法吃两个区间。
- **输出迭代器** — Output Iterator：只保证「写一次、单向走」；`ostream_iterator` 是其标准形态。
- **迭代器类别** — Iterator Category：input/output → forward → bidirectional → random access 的能力偏序。
- **适配器** — Adapter：改变另一组件接口而不改变行为的包装——迭代器/函数/容器三类适配器。
- **元素必要条件** — Element Requirements：可拷贝构造/可析构是底线；不同操作追加可比较、可交换等要求。
- **值语义 vs 引用语义** — Value vs Reference Semantics：容器**持有元素副本**；想「存引用」必须走指针/`reference_wrapper`。
- **异常保证** — Exception Guarantee：从「无保证」到强保证（操作要么成功要么回滚，如 `vector::insert` 单元素版）。
- **泛型函数** — User-Defined Generic Function：以迭代器为参数写算法，是扩展 STL 的第一姿势。

## 动机：为什么是「正交分解」而不是 N 个容器配 N×M 个功能

STL 的乘法结构：**C 个容器 × I 类迭代器 × A 个算法**，只要每样实现一次，组合免费获得。
若按朴素 OOP 思路（每个容器自带 sort/search/merge），代价是 C×A 且互不通用。
STL 用迭代器做「解耦层」：算法不认识容器，只认识迭代器类别承诺的能力。
这是第 6 章反复出现的论证（6.1 组件图、6.6 自定义泛型函数），也是读 STL 与读普通类库的根本姿势差异。

## 机制

### 1. 容器地图（6.2 节，细节在第 4 站）

```text
序列式     array(定长) vector deque list forward_list  ← 位置决定一切
关联式     set multiset map multimap                   ← 排序准则决定位置
无序       unordered_{set,multiset,map,multimap}        ← 哈希决定桶（C++11 新增，6.2.3）
其他       string（也是容器）/ C 数组(可当容器) / 适配器 stack queue priority_queue
```

### 2. 区间与半开约定（6.4.1）

- `end` 永远「不可解引用」，但它**可参与比较与算术**——这是 `find` 返回 `end` 表示「没有」仍能判定的原因。
- 空区间合法：`begin == end`。一切算法对空区间安静返回，不需要特判。
- 两区间算法（6.4.2）：第二区间通常只需 `[beg2, ...)` 起点（长度由第一区间决定，如 `equal`），
  或双端点（`set_intersection`）。**第二区间不够长是 UB**——标准不做边界检查。

### 3. 迭代器类别速查（6.3.2，第 5 站细讲）

| 类别 | 能做什么 | 典型 |
| --- | --- | --- |
| output | `*i++ = v` 一次 | `ostream_iterator`、插入迭代器 |
| input | 读一次、单向 | `istream_iterator` |
| forward | 读多次、单向 | 前向链表、`unordered_*` 迭代器 |
| bidirectional | 双向 | list、set/map |
| random access | +算术/比较 | vector/deque/array/string |

算法按「最弱需要」声明要求：`sort` 要 random access，`reverse` 要 bidirectional，`find` 只要 input。

### 4. 容器元素的必要条件（6.11.1）

- **底线**：可拷贝构造（C++11 起：移动构造亦可满足多数操作）、可析构、（比较类操作）可比较。
- 不可拷贝但可移动的类型（如包 `unique_ptr`）可进 `vector`，但 `size` 增长类操作要求更强——
  书中 6.11 的表格是排错时的速查表。
- 引用不能作元素：`vector<T&>` 编译失败（引用不可赋值/默认构造）；官方出口是 `vector<reference_wrapper<T>>`
  （`std::ref` 造）或指针（5.4.3/6.11.2 两处交汇）。

### 5. STL 的错误与异常（6.12）

| 错误形态 | 例子 | 防御 |
| --- | --- | --- |
| UB（不检测） | 越界 `operator[]`、失效迭代器、两区间算法第二区间过短 | 迭代器调试宏（libstdc++ `-D_GLIBCXX_DEBUG` ⚠️ 实现相关） |
| 抛标准异常 | `at()` 越界抛 `out_of_range`（`operator[]`/`front`/`back` 则 UB，不检查）；分配失败 `bad_alloc` | 边界不确定处用 `at` |
| 返回失败值 | 关联容器 `insert` 返回 `pair<iterator,bool>` | 检查 `.second` |
| 强异常保证 | 单元素 `insert/erase`：抛出则容器原样 | 依赖它需读文档，多数操作「无保证」 |

## 扩展 STL：三条正门与一条侧门（6.6、6.13）

- **正门一：写泛型函数**（6.6）——参数取迭代器对，内部用 traits/类别分发，等于自造一个小算法。
- **正门二：让用户自定义类型满足元素必要条件**（6.13.1）——补 `operator<`/哈希/拷贝即可入容器；
  注意 ADL 让 `swap` 可被重载捕获（02 站辅助函数、EMC++ 条款 30 同一件事）。
- **正门三：自定义分配器/准则**——插槽分别在第 8.10 与第 19 章（本目录第 10 站）。
- **侧门（不推荐）：派生自 STL 类型**（6.13.2）——容器无虚析构，经基类指针 delete 是 UB；
  私有继承 + using 放行的「受限接口」写法书中示众，现代替代是组合与自由函数。

## 权衡

- **泛型 vs 成员**：`std::count` 对任何区间可用，但 `list::remove` 能真删（拿到节点）。
  6.7.3「算法 vs 成员函数」的结论表（本书名句）：**成员优先**——更快且语义更对（能改容器本身），
  算法覆盖「不属于特定容器的通用组合」。
- **迭代器 vs 索引**：索引在 vector 上更直观，但迭代器是跨容器协议；调试版 STL 对迭代器有范围检查而 `[]` 无。
- **区间协议 vs 容器对象**：`[beg,end)` 灵活（子区间、原生数组）但可错配（两个容器的迭代器凑一对 = UB）。
  C++20 ranges 把协议升格为对象，正是对这一历史妥协的清算（见演进节）。

## 相邻概念对比

- **适配器三兄弟**：迭代器适配器（reverse/insert/stream/move，6.5）改「游标语义」；
  容器适配器（stack/queue，第 12 章）改「接口面」；函数适配器（bind/`mem_fn`，第 10 章）改「可调用体签名」。
- **TR1 与本书 6.2.3**：unordered 容器在 TR1（2005）先行、C++11 收编——书中 1.5「目前发展情势」交代了这段；
  今天 TR1 已死，但理解「先扩展后标准」的节奏有助于读任何新库提案。

## 最新演进与工业实践

- **C++17（执行策略是 C++17 增补，本书没有）**：`std::execution::par/seq` 作为算法首参
  （P0024R2，提案存在已核 `wg21.link` 302）；并行归约/排序进入标准。第 7 站给出可运行例子。
- **C++20 · ranges 革命**（P0896R4「The One Ranges Proposal」，已核）：
  - 区间 = 对象：`std::ranges::sort(v, std::less<>{}, &Person::age)` 一次给容器 + 投影。
  - 视图 `views::filter/transform/take/join/…` 惰性组合，替代手写泛型函数。
  - 迭代器概念改由 **concepts** 定义（P0898R3，已核），`sentinel` 把「end 不必是迭代器」合法化。
- **C++23**：`ranges::to`（P2415R2，已核）与 `from_range` 构造函数族（P1206R7，已核）联手终结
  「range 转容器」的样板；`views::zip`（P2609R3，已核）。
- **工业实践**：
  - 主流库全面转向 ranges：[llvm/llvm-project](https://github.com/llvm/llvm-project) 的 libc++ 与
    ranges 实现、[gcc-mirror/gcc](https://github.com/gcc-mirror/gcc) 的 libstdc++ 均把 P0896 族列为旗舰特性；
    folly/range、abseil（[abseil/abseil-cpp](https://github.com/abseil/abseil-cpp)）的 `absl::c_*` 是标准化之前的同一诉求。
  - cppreference 的 [Algorithm library](https://en.cppreference.com/w/cpp/algorithm) 页是本书 11.2 概览表的当代活页，
    查「某算法需要哪类迭代器」以它 + 所用实现文档为准。

## 联系

- 展开：容器 → [04-容器.md](04-容器.md)；迭代器 → [05-迭代器.md](05-迭代器.md)；
  函数对象/lambda → [06-函数对象与Lambda.md](06-函数对象与Lambda.md)；算法 → [07-算法.md](07-算法.md)。
- 实现视角（容器/迭代器的 SGI 源码）：[../STL源码剖析.md](../STL源码剖析.md)。
- ranges 深读：[../C++20模板元编程.md](../C++20模板元编程.md)；对照短讲：
  [../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md](../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md)。
- 系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)；单文件大纲：[../C++标准库.md](../C++标准库.md)。
