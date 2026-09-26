# 补编 B：从 MEC++ 到 Loki——定制技法谱系（CRTP 与策略类）

> 本文件**不是原书章节**，是补编：把本书"技术"部分（Item 25–31）放进 1996→2001→今天
> 的**定制技法（customization）谱系**里看——为什么 Meyers 的代理/智能指针/计数对象
> 会演化成 Alexandrescu 的 policy-based design，又如何在 C++11/17/20 中被标准件收编。
> 任务预设的 8 部分划分中 "Customization" 一名即对应这里（原书并无该 Part，官方目录核实为
> Basics/Operators/Exceptions/Efficiency/Techniques/Miscellany 六部分，见
> [00-总览与阅读地图.md](00-总览与阅读地图.md) 的核实记录）。

## 核心概念速览（中英对照）

- **奇异递归模板模式** — Curiously Recurring Template Pattern (CRTP)：派生类把自己作为模板参数传给基类，令基类在编译期"知道"具体类型。
- **静态多态** — static polymorphism：用 CRTP 把虚调用换成编译期展开，零 vtable、可内联。
- **策略类** — policy class：把类的可变行为拆成若干模板参数（每个是一个小类/struct），组合出指数级的行为空间。
- **策略库 Loki** — Loki：Andrei Alexandrescu《Modern C++ Design》(2001) 的配套模板库，policy-based design 的原始实现。
- **类型列表** — typelist：编译期链表（`Typelist<H,T>`），Loki 泛型元编程的地基；C++11 变参模板之后退役。
- **抽象基于具体** — "abstract should depend on concrete"：CRTP 逆转了"依赖倒置"的方向，用具体类型给基类注入实现。
- **概念约束** — concepts（C++20）：把 policy 的"契约"从报错地狱升级为可声明、可检查的接口。

## 动机：Item 25–31 共同未竟的问题——"如何定制而不付运行期代价"

本书技术部分的每个工件都在问同一件事：智能指针的**清理策略**（delete？free？引用计数递减？）、
代理的**转换目标**、计数器的**归属粒度**——这些都需要按使用场景定制。1996 年的答案是
继承 + 虚函数或手工抄改模板；Alexandrescu 2001 年的答案是"把定制点升格为模板参数"。
沿这条线重读本书，能看清 policy-based design 不是凭空出现，而是 Meyers 一批人惯用法工作的收敛。

## 机制精讲

### 1. CRTP：Item 26 计数问题的编译期解

书中 Item 26 用 `type_info` 查表解决"基类静态成员全家族共享"；CRTP 一行解决：
`class Derived : Counted<Derived>` 使基类模板**每个派生类实例化一份**，静态成员天然独立。
🔧 已实测（g++ 15.2，`-std=gnu++23`，实录输出）：

```text
alive before=0 sizeof(Widget)=1
Widget#2 of 2 alive
alive after scope=0
```

（基类静态成员独立计数 + 对象销毁后归零；且 `sizeof(Widget)=1` 不含 vptr——印证"CRTP 零空间开销"。）
静态多态侧：基类里 `static_cast<Derived&>(*this)` 即可回调派生实现，无间接调用、可全量内联——
这就是 Item 24 "热路径避免虚函数"的制度化答案。标准库近亲：`std::enable_shared_from_this`
（运行期版）与 ranges 适配器管道（编译期版）。

### 2. 策略类：Item 28 智能指针的完全体

本书 Item 28 的 `SmartPtr` 已含"清理策略"参数化雏形（以模板/继承表达 ⚠️ 具体形态未逐字核对原书）；
Loki 把它推到极限——`SmartPtr<T, Ownership, RefCounting, Dereferencing, MemberAccess>`，
"拥有权（排他/共享/深层拷贝）× 计数（侵入/非侵入/无）× 解引用（check/nothrow/fast）"
组合出几十种指针，而每种组合只实例化需要的那份。这是 **MEC++ 的 OOP 定制路线与
模板定制路线的分水岭**：Meyers 用对象组合行为，Alexandrescu 用类型组合行为。
代价：错误信息天书、编译时间爆炸、无法跨 DLL 边界——1996 与 2001 的硬件都为此买了单。

### 3. typelist → 变参模板：元编程载体的更替

Loki 的 `Typelist`、`Select`、`MostDerived` 等编译期容器在 C++11 变参模板 + `std::tuple`
（以及 `std::type_identity`、C++17 折叠表达式、C++20 递归聚合展开）之后彻底退役；
Abrahams/Gurtovoy 的 MPL 同理。今天写"策略集合"用 `template<class... Policies> struct Lib`
+ 继承打包（pack expansion），三行顶 Loki 三百行。参考：
[../C++模板元编程.md](../C++模板元编程.md)（MPL 时代）、[../C++20模板元编程.md](../C++20模板元编程.md)（现代形态）。

### 4. concepts：policy 契约的可检查化

policy-based 的痛点是"契约只能靠误用时的一屏错误"。C++20 concepts（核心提案
[P0898](https://wg21.link/p0898)，提案号已实测可达）允许预先声明
`template <class P> concept RefCounter = requires(P p) { p.add_ref(); p.release(); }`，
把 Loki 文档里口头约定的 policy 要求变成编译器强制 + 清晰诊断。这是"定制技法谱系"
的当前终点站：**运行期虚分派（1996）→ 编译期模板（2001）→ 带契约的编译期模板（2020）**。

### 5. 现代最小 policy 骨架：变参打包 + `[[no_unique_address]]`

🔧 用 2020 年代语法重写"Item 28 智能指针的清理策略"这一件事（教学示意，未实测）：

```cpp
template <class T> struct DefaultDelete {          // policy：如何销毁
    void operator()(T* p) const { delete p; }
};
template <class T> struct NoDelete {               // policy：只看不管（借用场景）
    void operator()(T*) const {}
};
template <class> struct LogPolicy { static void destroyed() {} };
template <class T, class Destroyer = DefaultDelete<T>, class Logger = LogPolicy<T>>
class Ptr : private Logger {                       // 空策略零体积：C++20 属性收编
    T* p_;
public:
    ~Ptr() { Logger::destroyed(); Destroyer{}(p_); }
};
static_assert(std::same_as<decltype(Ptr<int>{}.~Ptr()), void>);  // concept 让误用在此处即报错
```

对比 Loki 的 `SmartPtr<T, ownership, threading, lifetime, pointee_storage, ...>`：
今天同样的定制点只需要一个变参模板 + 两三行 concept 约束；编译期错误从"三屏天书"
缩到"一行约束不满足"。Meyers 若在今天修订 Item 28，大概率就长这样。

### 6. NVI：CRTP 与虚函数谱系的中间站

Item 33"非尾端类抽象化"还有一个书中未展开的配套惯用法——**非虚接口（NVI）**：
公开函数非虚且不可改（`final` 语义的手工版），内部转调受保护的纯虚钩子：

```cpp
class Shape {
public:
    void draw(std::ostream& os) const { os << "---\n"; this->do_draw(); os << "---\n"; }
protected:
    virtual void do_draw() const = 0;   // 派生类只许定制"洞"，不许破坏"框架"
};
```

NVI 把 Item 32（面向未来：留出前后处理扩展点）与 Item 33（中间节点抽象化）缝合成
一条可执行纪律；Sutter 将其系统化为设计准则（《Exceptional C++》语境 ⚠️ 未逐字核对），
GCC/Clang 的 `-Wnon-virtual-dtor` 一类的警告则是它的执法工具（本目录 [03-异常.md](03-异常.md)
析构规则的同款帮手）。

## 权衡与相邻概念对比

| 定制手段 | 绑定时机 | 成本 | 典型场景 |
| --- | --- | --- | --- |
| 虚函数/继承（本书主流） | 运行期 | vtable + 阻碍内联 | 开放类型集、跨 DLL |
| CRTP（静态多态） | 编译期 | 代码膨胀（每类型一份） | 热循环、无堆分配 |
| policy 模板（Loki） | 编译期 | 组合爆炸、诊断难 | 组件库的"行为菜单" |
| 类型擦除（`std::function`/`any`） | 运行期 | 一次分配 + 间接调用 |  heterogeneous 容器、回调 |
| concepts 约束（C++20） | 编译期检查 | 几乎为零 | 给以上三者立契约 |

**相邻概念对比**：类型擦除（Sutter 语境的 "generic programming done other way"）与 policy
是同一枚硬币的两面——前者把定制藏进值语义，后者把定制抬进类型系统。
本书 Item 30 代理正是类型擦除的原始形态。

## 最新演进与工业实践

- **C++26 deducing this（[P0847](https://wg21.link/p0847)，提案号实测可达，已被采纳进 C++26）**：
  `void f(this auto& self)` 让"基类知道派生类型"不再需要 CRTP 样板——CRTP 的两大动机
  （静态多态、链式调用保型）一半被语言吸收。
- **Loki 的历史定位**：其成果大量渗入标准与工业库——`std::unique_ptr` 的删除器即微型 policy、
  `SmallVector` 系（LLVM/Abseil `inlined_vector`）的容量策略、fmt 的 compile-time format
  检查（<https://github.com/fmtlib/fmt>）是"CRTP 式技巧 + constexpr"的后裔；
  Loki 源码归档于 <http://loki-lib.sourceforge.net/>。
- **fmt 是当代 policy-based 的示范**：`formatter<T, Char>` 特化 = 按类型注册策略，
  `FMT_COMPILE_STRING` 类技巧把校验搬进编译期——Alexandrescu 路线在 2020 年代的工业化生存样本。
- **`[[msvc::no_unique_address]]` / `[[no_unique_address]]`（C++20）**：策略打包成员零空间化，
  治愈 policy 组合的另一笔旧账（空策略占字节）。
- 本仓库延伸：策略模式在 C++20 概念下的重构见 [../C++20设计模式.md](../C++20设计模式.md)；
  Alexandrescu 书目的原版信息可经 InformIT 检索（未在本笔记建外链处标 ⚠️ 处自行核实）。

## 交叉互链

- 谱系上游（本书技术部分原件）：[05-技术.md](05-技术.md)
- 成本论证的原始出处：[04-效率.md](04-效率.md)（Item 24）
- 智能指针的标准化终局：[07-补编-35条现代继承对照表.md](07-补编-35条现代继承对照表.md)
- 单文件原大纲：[../More%20Effective%20C++.md](../More%20Effective%20C++.md)
- 模板谱系书目：[../C++模板元编程.md](../C++模板元编程.md)、[../深入实践C++模板编程.md](../深入实践C++模板编程.md)
- 现代条款对照：[../Effective_Modern_C++.md](../Effective_Modern_C++.md)、[../C++CoreGuidelines解析.md](../C++CoreGuidelines解析.md)
