# 02 · 不透明指针与 Pimpl（原书 3.1）

> 对应中文目录（已核实）：第 3 章 模式 → 3.1 Pimpl 惯用法
> （3.1.1 使用 Pimpl / 3.1.2 复制语义 / 3.1.3 Pimpl 与智能指针 / 3.1.4 Pimpl 的优点 /
> 3.1.5 Pimpl 的缺点 / **3.1.6 C 语言的不透明指针**——不透明指针在原书中是 Pimpl 节的小节，并非独立章）。
> 英文原小节题 ⚠️ 推定："The Pimpl Idiom" / "Opaque Pointers in C"。
> 另含两节**补编**（智能指针版 Pimpl 的现代写法；Qt d-pointer 案例）——不在已核实目录中，不冒充原书小节。

## 核心概念速览（中英对照）

- **指向实现的指针** — Pointer to implementation (Pimpl)：公有类只持有一个指向私有实现类的前向声明指针，把实现细节从头文件里整个搬走。
- **不透明指针** — opaque pointer / handle：`typedef struct X* XHandle` 式接口，调用者只见指针类型名、不可解引用，C 时代的物理隐藏。
- **编译防火墙** — compile firewall：Pimpl 的另一个名字——头文件不再携带实现依赖，`#include` 传染链在此截断。
- **Impl 嵌套类** — nested Impl class：`class Widget::Impl` 把实现类锁在外类的名字域内，符号不污染全局。
- **值语义** — value semantics：Pimpl 后对象仍是普通成员/栈对象/容器元素，复制行为需在 3.1.2 手工定义。
- **深拷贝** — deep copy：复制 Widget 时为每个副本新建独立 Impl（书给出的缺省选择），区别于共享。
- **写时复制** — copy-on-write (COW)：复制只增引用计数、写时才分家；3.1.2 提及的替代方案，代价见 [08-API性能.md](08-API性能.md)。
- **自引用成员** — self-referential member：Impl 里存回指外壳 Widget 的指针（窗口与渲染器相互持有），析构顺序与悬垂风险陡增。
- **虚表间接层** — vtable indirection：用抽象基类 + 工厂替代 Pimpl 的实现隐藏路线（与句柄式 API 对比见本节末）。
- **ABI 兼容** — ABI compatibility：改私有成员不破坏已编译用户的二进制布局承诺——Pimpl 的头号卖点。

## 动机：private 为什么藏不住

`private:` 只约束「语义上谁能碰」，不约束「编译时谁知道」：

```text
class Widget {            // v1 头文件
    int fValue;           // private 也在 sizeof/成员偏移里
    std::string fName;    // 还把 <string> 拖进了每个用户 TU
};
// 加一个 private double fExtra → sizeof 变了、偏移变了、include 传染变了
// → 所有预编译的下游 .o/.lib 与新库**链接得动、跑起来错**（静默 ABI 破坏）
```

3.1.4 的优点清单全部来自「头文件里只剩一个指针」这一个事实；3.1.5 的缺点清单全部来自
「对象内部多了一次堆分配和一跳间接」。先立靶再看箭。

## 机制：已实测 g++ 15.2 的 ABI 行为

以下为本机 MinGW g++ 15.2.0 (x86_64-win32-seh) 实测（临时件在仓库外 `D:\develops\tmp\cppsnippets_api\`，仓库内无产物）：

```cpp
// 🔧 widget.hpp —— Pimpl 版公有头文件：全部实现依赖 = 一个指针 + 一个前置声明
class Widget {
public:
    Widget();
    ~Widget();
    int  value() const;
    void setValue(int v);
private:
    struct Impl;        // 名字在库外不可解引用（甚至不知道它有多大）
    Impl* fImpl;
};
```

```cpp
// 🔧 widget.cpp —— 库内部：想塞什么塞什么，头文件永不因此更改
struct Widget::Impl { int fValue = 0; std::string fName; double fExtra; };
Widget::Widget()  : fImpl(new Impl) {}
Widget::~Widget() { delete fImpl; }
int  Widget::value() const   { return fImpl->fValue; }
void Widget::setValue(int v) { fImpl->fValue = v; }
```

实测结果（同一用户 TU 分别对三种库形态编译）：

| 场景 | sizeof(Widget) | 用户 .o 的 undefined 符号 | 内部加成员后 |
| --- | --- | --- | --- |
| 朴素 v1 头（int 成员） | 4 | 内联方法**编进用户 .o**（无外部引用） | v2 sizeof=16，旧 .o 静默错乱 |
| 朴素 v2 头（int+double） | 16 | 同上 | —— |
| Pimpl 头（v1→v2 不改） | **恒 8** | 仅 `Widget::{ctor,dtor,value,setValue}` 4 个函数名 | 用户 .o 与 sizeof **零变化**，旧 .o 直接可用 |

Pimpl 版 `nm -C` 还显示 `Widget::Impl::{Impl,~Impl}` 只存在于库的目标文件里（T），
用户侧完全不可见——「隐藏实现类」（已核实小节 2.2.5 的三级隐藏里最顶的一级）至此闭环。

**复制语义（3.1.2）**：默认拷贝构造/赋值会复制裸指针 → 双释放。书的选项：
(a) 手写深拷贝（每个副本独立 Impl）；(b) 干脆 `delete` 掉拷贝操作（声明不可复制）；
(c) COW 共享到写。已实测的指针版里，析构必须**出体外定义**（`~Widget();` 在头里只声明），
否则用户 TU 实例化析构时 `Impl` 不完整、`delete` 编译失败——这是指针版最常见的踩点。

**C 不透明指针（3.1.6）**：

```c
/* 🔧 widget.h —— C 路线：类型本体不出现在头文件 */
typedef struct Widget Widget;          /* 或 typedef void* WidgetHandle; */
Widget* widget_create(void);
void    widget_destroy(Widget*);
int     widget_value(const Widget*);
```

与 C++ Pimpl 的差别：C 路线天然 ABI 稳定（调用者从未接触布局）且跨编译器/跨语言，
代价是没有构造/析构/重载/RAII，错误处理全靠返回值——现代工程把它用作「库的稳定外壳」，
内壳才用 C++（对应实测：MinGW 下 DLL 导出表恰好只有 `extern "C" + dllexport` 的三个符号
`c_add/widget_create/widget_destroy`，C++ 类函数不标导出就不出现，见 [07-C++用法与符号导出.md](07-C++用法与符号导出.md)）。

## 权衡：ABI 收益 vs 二次分配成本

| 维度 | 收益 | 成本 |
| --- | --- | --- |
| ABI/二进制 | 私有成员随便加，sizeof 恒定 | 类不能再被内联成员访问；`alignas` 之类布局承诺失效 |
| 编译期 | 头文件依赖清空，增量重编译大缩水 | 方法不能定义在头里（模板类**不能** Pimpl，见 3.1.5 末的例外） |
| 运行期 | —— | 每对象一次 `new`（二次分配）+ 每次访问多一跳指针（缓存局部性变差） |
| 语义 | 值语义可自由定义（深拷贝/COW/不可复制） | 特殊成员函数要手工成套维护（Rule of 0/3/5 的账） |
| 调试 | 库内断点集中 | 步进时多一层跳转，核心转储里 Impl 内容不透明 |

「二次分配 + 间接」的量级判断：对「少量长生命周期对象 + 方法内多次成员访问」几乎免费；
对「百万级小对象 + 每方法只读一个字段」则不可接受——此时回到朴素布局或数组化设计（SoA），
见 [08-API性能.md](08-API性能.md)。

## 相邻概念对比

- **Pimpl vs 纯虚接口（抽象基类）**：接口路线给「多态 + 隐藏」，但把值语义变成指针语义
  （容器装 `unique_ptr<Widget>`），且虚表布局自此成为 ABI 的一部分（加虚函数即破坏，见 09 章）。
- **Pimpl vs 句柄层级**：句柄（int 索引/C 指针）可以跨进程传递、易做安全版本化；Pimpl 仍是类型化 C++ 对象，易用性好。
- **Pimpl vs 前置声明**：前置声明是 Pimpl 的原料；只前置声明不搬成员，隐藏不完（sizeof 仍暴露）。
- **不透明指针 vs `typedef void*`**：前者保类型检查（不同句柄不可互传），后者彻底退化为整数——书的立场是保结构体的命名句柄。

## 补编 · 智能指针版 Pimpl（书后主流写法，非原书小节）

```cpp
// 🔧 C++11 起的标准形态（已实测同布局：sizeof 仍为 8）
class Widget {
public:
    Widget();
    ~Widget();                          // 仍必须库内定义（unique_ptr 需要完整类型）
    Widget(const Widget&);              // 深拷贝语义照旧要手写
    Widget& operator=(const Widget&);
    Widget(Widget&&) noexcept;          // 移动 = 偷指针，天然廉价
private:
    struct Impl;
    std::unique_ptr<Impl> fImpl;        // 异常安全自动兜底（裸指针版构造中途抛异常即泄漏）
};
```

`unique_ptr` 消灭了「忘记 delete」一族 bug；`shared_ptr` 版则把 COW 变成引用计数共享
（对应已核实小节 3.1.3「Pimpl 与智能指针」，⚠️ 原书成文于 C++03/过渡期，示例形态与今日不同）。

## 补编 · 案例：Qt 的 d-pointer（非原书小节）

Qt 全系列用 `QWidgetPrivate* d_ptr`（宏 `Q_D(QWidget)` 取用）：既是二进制兼容手段，也是
「同一套私有数据在 QWidget/QMainWindow 派生链共享」的手段（shared d-pointer）。
它的工程注脚值得记：每个 Qt 对象都固定背一次堆分配——Qt 社区自己也在性能敏感处
（QVector 的隐式共享）反复权衡过。仓库内可对照 [../wxWidgets跨平台程序开发.md](../wxWidgets跨平台程序开发.md)（同类 GUI 框架的对象模型权衡）。⚠️ 本条案例为业界通识，非原书内容。

## 最新演进与工业实践

- **C++11 特殊成员函数规则让 Pimpl「可默认」**：`=default`/`=delete` 可精确控制五件套的生成位置；
  「析构必须出体外」成为 new-faq 级常识（Scott Meyers 的讨论与 Effective Modern C++ item 相关，
  对照 [../Effective_Modern_C++.md](../Effective_Modern_C++.md)）。
- **`std::is_copy_constructible` / type traits** 可在编译期测试 Pimpl 类的语义完整性（concepts 时代用
  `static_assert(std::movable<Widget>)`，见 C++20 concepts，[../C++20模板元编程.md](../C++20模板元编程.md)）。
- **对齐与新式隐藏**：`std::pmr` 多态分配器可以让 Impl 跟随外壳分配（缓解二次分配），属于书后方案 ⚠️ 无标准背书。
- **工业样本**：libclang/LLVM 的 `LLVMModuleRef` 等 typedef 不透明句柄家族（C API 稳定层的标准手段）；
  Chromium 的 `base::` 对象一般**不**用 Pimpl，而是靠「接口即边界 + 严格评审」——同一问题的另一路线，
  呼应 [../C++API设计.md](../C++API设计.md) 2020-08 摘录的 Chromium base 评价。
- **header-only 的反潮流**：cpp-httplib/doctest/stb 干脆放弃编译防火墙，以「复制一个头」替代 ABI 承诺——
  Pimpl 成本账（分发库 vs 分发源码）的另一端，见 [06-API风格.md](06-API风格.md)。

## 与其他章 / 其他笔记的联系

- ← [01-API简介与通用问题.md](01-API简介与通用问题.md)：2.2.5「隐藏实现类」在此兑现。
- → [03-单例与工厂.md](03-单例与工厂.md)：Impl 内部对象经工厂/单例获得全局资源。
- → [08-API性能.md](08-API性能.md)：二次分配的实测视角与 COW 全章。
- → [09-版本控制与ABI.md](09-版本控制与ABI.md)：Pimpl 是 ABI 兼容工具箱的一员（它救不了虚函数布局）。
- → [../深度探索C++对象模型.md](../深度探索C++对象模型.md)：sizeof/偏移/vptr 的机器级底账。
- → [../C++标准库.md](../C++标准库.md)：智能指针三件套的标准库视角。
- → [../C++系列·总索引.md](../C++系列·总索引.md)｜[../C++API设计.md](../C++API设计.md)

## 思考题

1. 解释为什么「析构函数在头文件里 `= default`」会让指针版 Pimpl 编译失败（提示：实例化点与完整类型）。
2. 对一个含 12 个成员函数的模板类，Pimpl 失效——给出两条现实退路（显式实例化进库 / 接受头文件即 ABI）。
3. 用本节的对照表论证：GUI 控件类（少量、长寿、成员多）与粒子系统（百万、短命、字段少）各该不该 Pimpl。
