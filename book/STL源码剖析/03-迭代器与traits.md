# 第 3 章 迭代器概念与 traits 编程技法（Iterators & Traiture programming）

> 覆盖原书第 3 章：迭代器必须具备的附属装置（associated types）、五种迭代器分类、
> `iterator_traits` 的三层抽取技法、SGI STL 如何以「分类标签 + 函数重载」泛化算法。
> 本章回答一个语法问题：**算法怎样在不认识容器的前提下，认识「位置差」「元素类型」这些能力。**
> 机制转述，源码引用镜像 [karottc/sgi-stl](https://github.com/karottc/sgi-stl) `stl_iterator_base.h` / `stl_iterator.h`。

## 核心概念速览（中英对照）

- **迭代器附属类型** — associated types：`value_type / difference_type / pointer / reference / iterator_category` 五件套，算法编译期所需的全部信息。
- **输入迭代器** — input iterator：只能单向读、++ 前进（流语义）。
- **输出迭代器** — output iterator：只能单向写。
- **前向迭代器** — forward iterator：可读可写、多趟遍历、++ 之外无 --（slist 档）。
- **双向迭代器** — bidirectional iterator：可 -- 回退（list/树迭代器档）。
- **随机访问迭代器** — random access iterator：±n、比较大小、O(1) 跳跃（vector/deque/原生指针档）。
- **分类标签** — iterator category tag：空结构体（`input_iterator_tag`…），仅作重载选择用的「能力证书」。
- **萃取机** — `iterator_traits<Iter>`：任何迭代器 → 五件套的统一查表接口（`stl_iterator_base.h`）。
- **基类抽取** — extraction from base：继承 `iterator<Category,T,Distance>` 即自动 typedef 五件套。
- **偏特化兜底** — partial specialization for pointers：`iterator_traits<T*>` 与 `const T*` 让原生指针直接当迭代器用。
- **标签分派** — tag dispatch：`advance(iter, n, random_access_iterator_tag)` 型重载，编译期选最优实现。
- **difference_type 有符号性** — signed distance：`ptrdiff_t` 保证 `last - first` 可为负，`distance()` 返回其类型。

## 动机：指针抽象的「最后一公里」

原生指针天然支持 `*p`、`p+1`、`p2-p1`，但换成 `list<T>::iterator` 类类型后，
`p2-p1` 不存在、`*(p+=n)` 要循环 n 次。算法（`sort` 要 O(1) 跳跃、`find` 只要 ++、
`distance` 想多快就多快）必须同时知道两件事：

1. **这个迭代器能提供什么操作？**（能力档位——决定用哪版实现）
2. **元素类型是什么？距离类型是什么？**（类型信息——决定返回值与临时变量）

_traits 机制就是把这两问都变成**编译期查表**：类型即证书，重载即分派。

## 机制：三层抽取 + 标签分派

### 1. 五个标签（`stl_iterator_base.h`，镜像实测存在）

```cpp
struct input_iterator_tag {};
struct output_iterator_tag {};
struct forward_iterator_tag       : public input_iterator_tag {};
struct bidirectional_iterator_tag : public forward_iterator_tag {};
struct random_access_iterator_tag : public bidirectional_iterator_tag {};
```

**继承链是点睛之笔**：找不到 random_access 版重载时，实参可隐式转为父标签、命中次优版本——
标签体系自带「降级回退」，不需要为每种迭代器写全所有重载。

### 2. iterator_traits 的三层瀑布

```cpp
// 第一层：通用查表——要求迭代器自带五个 typedef（类类型迭代器的义务）
template <class Iter>
struct iterator_traits {
  typedef typename Iter::iterator_category iterator_category;
  typedef typename Iter::value_type        value_type;
  typedef typename Iter::difference_type   difference_type;
  typedef typename Iter::pointer           pointer;
  typedef typename Iter::reference         reference;
};
// 第二层：裸指针偏特化——T* 没有成员 typedef，由 traits 代为声明
template <class T>
struct iterator_traits<T*> {
  typedef random_access_iterator_tag iterator_category;
  typedef T                          value_type;
  typedef ptrdiff_t                  difference_type;
  typedef T*                         pointer;
  typedef T&                         reference;
};
template <class T> struct iterator_traits<const T*> : 同上（value_type 去掉 const）… {};
// 第三层：基类协定——自定义类迭代器继承这个「模板模板参数」基类即自动合规
template <class Category, class T, class Distance = ptrdiff_t,
          class Pointer = T*, class Reference = T&>
struct iterator {
  typedef Category  iterator_category;
  typedef T         value_type;  typedef Distance difference_type;
  typedef Pointer   pointer;     typedef Reference reference;
};
```

侯捷总结的三种迭代器声明法（转述）：① 全部自带 typedef；② 继承 `std::iterator`；
③ 什么都不做、只要 `iterator_traits` 能为它偏特化（vector 的迭代器就是 `T*`，靠第二层兜住）。
⚠️ 「三种法」措辞为机制归纳，非原书逐字。C++17 起 `std::iterator` 被弃用——因为 Distance 手填
易错，且 concepts 路线改要求「直接 typedef」；这是本技法在现代的第一个减分项。

### 3. 标签分派实战：advance / distance

```cpp
// stl_iterator_base.h 形态（转述；__advance 在 :324 起实测）
template <class Iter, class Dist>
inline void advance(Iter& i, Dist n) {
  __advance(i, n, iterator_traits<Iter>::iterator_category());  // 第三实参是「证书」
}
// 三个重载：
void __advance(i, n, input_iterator_tag)          { while (n--) ++i; }
void __advance(i, n, forward_iterator_tag)        { while (n--) ++i; }   // 无法做更多
void __advance(i, n, bidirectional_iterator_tag)  { n>=0 ? while(n--) ++i : while(n++) --i; }
void __advance(i, n, random_access_iterator_tag)  { i += n; }             // O(1)
```

`distance()` 同理：随机访问档 `return last - first;`（O(1)），其他档 ++ 数到黑（O(n)）。
书用 `numeric.h` 的 `accumulate` 说明另一半：结果类型 = **初值类型**
（`T` 由 `init` 推导，`vector<unsigned short>` 配 `int init=0` 得 int 结果），
迭代器只贡献 `value_type` 的「可读性」不贡献算术类型——提醒调用者显式给对初值。

## 权衡

- **收益**：算法头文件零特判。任何满足协议的类型（含第三方、含裸指针）自动接入全部算法；
  这是 C++ 泛型「结构化类型」的雏形（无声明式的 interface，全靠 typedef 协议）。
- **成本 1：协议脆弱**。忘写 typedef → 第一层查表编译失败，报错指向算法内部而非你的类
  （concepts 之前的时代税）。
- **成本 2：证书造假无防线**。把 list 迭代器谎报 random_access，编译照过、运行炸——
  traits 信任开发者。
- **成本 3：五件套粒度粗**。真实需求（contiguous？sized sentinel？）溢出了五档标签，
  于是 C++20 用 `std::contiguous_iterator_tag`（继承 random_access，接上标签继承链的老招）与
  sentinel 概念重划档位。

## 相邻概念对比

- **traits vs 虚函数**：同一问题（运行期多态 vs 编译期多态）的两个时代答案；traits 零开销、
  错误在编译期暴露，代价是不能「装了就走」——选择发生在实例化时。
- **iterator category vs C++20 迭代器概念**：input/output/forward/bidir/random 五档演进为
  `std::input_or_output_iterator / std::iterator / std::sentinel_for` 的公理化体系（约束而非 typedef），
  后者见 [../C++20模板元编程.md](../C++20模板元编程.md)。
- **`std::iterator` vs `std::iterator_traits`**：前者是「交证书的基类」（已弃用），
  后者是「查证书的函数」（永不过时）——现代写法：自己写 typedef，别继承。
- **const 指针 value_type 去 const**：`iterator_traits<const T*>::value_type == T`——
  为的是 `vector<int> a,b; transform` 之类场合拿 value_type 当可变临时类型；这是traits 设计中
  「处处为算法着想」的注脚。

## 最新演进与工业实践

- **`std::iterator` 弃用（C++17）→ 移除议题**：现代代码直接提供五个 typedef；
  cppreference 与三家实现一致标注 deprecated。⚠️ 提案编号未核实，此处不引。
- **C++20 ranges 的迭代器体系**：`std::ranges::iterator_t / range_value_t / range_diff_t`
  把 traits 升级为「约束化关联类型」，`std::iter_swap`/`indirect` 算法族解决「迭代器值类别」
  遗留问题（proxy 迭代器如 `vector<bool>::reference` 终于被正式承认——呼应 04 篇 bit_vector）。
- **工业侧**：写新容器/新迭代器时，业界模板是 folly/ranges-vlib（ericniebler/range-v3，
  C++20 ranges 的前身，github 可达）里的 traits 层；它展示了「不靠继承、只靠 CPO + 关联类型」的
  现代等价物。
- **gsl::span / `std::span`（C++20）**：把「裸指针当随机访问迭代器」合法化、对象化——
  traits 时代指针兜底特化的精神续作。
- **本目录实测**：🔧 已用 g++ 15.2 验证裸指针、`vector<int>::iterator`、自定义类迭代器
  三种来源均能被 `std::iterator_traits` 抽取（详见 07 篇附表；仓库外 `cppsnippets_stl/t4.cpp`）。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | deque 迭代器不是随机访问 | SGI/现代实现都给 random_access（跨块算术在 `stl_deque.h` 里手写，见 04 篇） |
| 2 | `distance(a,b)` 永远 O(1) | 只有随机访问档 O(1)；双向档是数出来的 |
| 3 | value_type 就是「容器里存的类型」 | const 指针偏特化会去 const；它是「可实例化的元素类型」而非存储签名 |
| 4 | 继承 std::iterator 更地道 | C++17 起反向：直接 typedef 更地道 |
| 5 | iterator_traits 是 STL 专利 | 该技法即「policy/traits class」范式的起源案例之一，被 boost/现代库全境继承 |

## 与其他章 / 其他书的联系

- 标签分派在哪被最密集使用：[06-算法仿函数与配接器.md](06-算法仿函数与配接器.md)（sort 家族、merge 家族按标签选路）
- 谁生产这些迭代器：[04-序列式容器.md](04-序列式容器.md)、[05-关联式容器.md](05-关联式容器.md)
- 反向/插入迭代器「改写」分类的方式：[06-算法仿函数与配接器.md](06-算法仿函数与配接器.md)
- traits 技法下游：[../C++模板元编程.md](../C++模板元编程.md)、[../C++20模板元编程.md](../C++20模板元编程.md)
- 上游总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)；单文件版 [../STL源码剖析.md](../STL源码剖析.md)、
  [../STL源码剖析简体中文完整版.md](../STL源码剖析简体中文完整版.md)；导航 [../C++系列·总索引.md](../C++系列·总索引.md)
