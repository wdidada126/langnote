# 11 noexcept 与确定求值顺序

> 对应原书 **第21章 noexcept关键字（C++11 C++17 C++20）· 第28章 确定的表达式求值顺序（C++17）**
> 导航：[系列索引](../C++系列·总索引.md) ｜ [单文件笔记](../现代C++语言核心特性解析.md) ｜ [00 总览](00-总览与阅读地图.md)

## 核心概念速览（中英对照）

- **noexcept 说明符** — noexcept specifier：承诺不抛异常；`noexcept(expr)` 条件式承诺（C++17）
- **noexcept 运算符** — noexcept operator：`noexcept(表达式)` 在编译期问"会抛吗"
- **异常规范（旧）** — dynamic exception specifications（`throw(T)/dynamic noexcept`）：C++11 弃用、C++17 移除
- **移动的条件承诺** — conditional noexcept：隐式移动操作以"成员全 noexcept 移动"为条件
- **terminate 路径** — 违反 noexcept 承诺 = 构造展开被禁，直接 std::terminate
- **栈展开** — stack unwinding：抛出后析构局部对象的回程；noexcept 边界截断它
- **求值顺序** — evaluation/sequencing order：C++17 把一批"实现自由"改写为"强制顺序"
- **副作用（side effect）更新序** — sequencing of side effects：标准用 strongly/weakly sequenced 描述
- **`std::uncaught_exceptions()`** — C++17：析构内判断是否在展开（再抛的守门数）

## 动机

两章共同主题是"**把不确定的执行语义钉死**"：noexcept 钉死"会不会有异常路径"
（编译器据此省略展开表、库据此决定移动/拷贝、人据此决定契约强度），
C++17 求值顺序钉死"子表达式谁先跑"（`f()+g()` 型 UB/实现差异是 C++98 到 14 的
慢性病——`v[i] = i++` 家族）。

## 机制（编译器视角）

- **noexcept 的三段人生**：
  1. **类型层**（C++17 起 noexcept 是函数类型的一部分）：`void() noexcept` 与
     `void()` 是不同类型，可互转方向唯一（普通→noexcept 禁止）；实测
     `is_nothrow_move_constructible_v` 直接读这个位。
  2. **代码生成层**：GCC 为可能抛的函数生成 `.eh_frame` 展开信息；noexcept 边界
     生成"展开即 terminate"的 personality routine 检查——**帧表变小、抛出路径变直**，
     MSVC 的 `/EHsc` 语义差异同理（⚠️ 帧尺寸数字未实测，只述机制）。
  3. **决策输入层**：标准库到处探测它。`vector` 增长搬移**只敢用 nothrow-move**——
     实测对比（🔧）：无 `noexcept` 移动构造的 `emplace_back` 增长 15 次**全拷贝**，
     加上 `noexcept` 后**全移动**。这一条是"写移动构造必写 noexcept"的全部理由。
- **隐式操作的 noexcept 推导**：默认构造/平凡析构/移动等隐式函数带
  "隐式 noexcept 说明符"，条件由成员/基类推导（成员全 nothrow-move → 类 nothrow-move）。
  这就是"移动构造问题"的标准解：你给成员加了会抛的操作，类的承诺自动降级，
  容器策略跟着降级——**承诺沿合成结构向上传播**。
- **`noexcept(expr)`（C++17）**：把承诺条件化，完美转发包装器的正统写法
  `noexcept(T(std::forward<Args>(args)...))`——标准库自身（make_unique、swap 家族）如此用。
- **throw() 与 dynamic specifications 之死**：`throw(int)` 从"承诺"到"违背即 terminate"
  的语义早被证明无用，C++11 弃用、**C++17 移除**（P0003R5，wg21.link 实测 302；
  库内《C++语言程序设计5》笔记同样实测过该判决——"判处死刑"口径互证）；
  语法残留 `noexcept(false)` 是显式"可抛"。
- **求值顺序的 C++17 钉板清单**（编译器的序列约束变厚）：
  移位两侧、关系链、赋值右侧先于左侧、函数调用**参数求值仍 unspecified**（注意！）、
  新表达式、`<<` 重载链按书写序（`operator<<` 现在左操作数先于右操作数求值）、
  `?:` 条件先于操作数、`static_cast` 等转换先于操作数。
  **实测诚实记录**：`std::cout << f() << g()` 与 `f()+g()` 在本机 g++ 15.2 的
  -std=gnu++11/17/20 三种模式下输出**完全一致**（`f 先`→`g 后`）——
  现代 GCC 早已按"从左到右"生成这两个形态，**标准差异在本机不可见**；
  它的意义在于把"另一个编译器/老版本会反序"变成非法实现（网络传说的
  "换标准就反序"在 g++ 15 上**复现失败**，如实记录 ⚠️）。

## 权衡

- `noexcept` 用多了会**锁死演化空间**：承诺之后，实现里加一行可能抛的代码
  等于埋 terminate；库接口上的 noexcept 是 API 契约，不是性能贴纸。
- 不写 noexcept 的移动构造在容器里静默退化为拷贝——**性能回归无声**，
  而错误回归有声（terminate 巨大声）；两种失败模式的不对称是本章的核心工程判断。
- 求值顺序"部分钉死"意味着**剩下的 unspecified 依然存在**（函数实参！）——
  跨实参有副作用仍是地雷，规范上禁止比语法上指望更现实。

## 相邻概念对比

| 写法 | 含义 | 命运 |
| --- | --- | --- |
| `throw(int)` | 只抛 int? | C++17 移除（P0003R5 实测 302） |
| `throw()` | 不抛 | C++17 移除；C++11 起等价 noexcept |
| `noexcept` | 不抛 | 现役；且进函数类型 |
| `noexcept(expr)` | 条件不抛 | C++17 起；标准库推导式声明的主战场 |
| `noexcept(true/false)` | 显式布尔 | 等价两种形态 |

## 🔧 实测样例（已实测 g++ 15.2）

**noexcept 决定容器搬移策略**（-std=gnu++17，核心两行）：

```cpp
struct NoNoex{ int v; NoNoex(int i):v(i){} NoNoex(NoNoex&& o):v(o.v){ ++moves; }
               NoNoex(const NoNoex& o):v(o.v){ ++copies; } /* 赋值略 */ };
struct WithNoex{ /* 同上, 但 */ WithNoex(WithNoex&& o) noexcept: v(o.v){ ++moves; } };
std::vector<NoNoex> a;   a.reserve(1);  for(int i=0;i<16;++i) a.emplace_back(i);
std::vector<WithNoex> b; b.reserve(1);  for(int i=0;i<16;++i) b.emplace_back(i);
```
实测输出：

```text
无 noexcept 移动构造: moves=0 copies=15 (vector 增长只敢用拷贝)
有 noexcept 移动构造: moves=15 copies=0
```

（libstdc++ 判据：`is_move_constructible && (is_nothrow_move_constructible ||
!is_copy_constructible)`——不承诺 noexcept 且可拷贝 → 拷贝更"安全"，
因为移动抛异常会把容器留在半搬移状态。这就是强异常安全与 noexcept 的真实挂钩。）

**求值顺序本机一致性取证**（-std=gnu++11 / gnu++17 / gnu++20 三模式同一输出）：

```cpp
int f(){ puts("f 先"); return 1; }
int g(){ puts("g 后"); return 2; }
int main(){ int r = f() + g(); printf("r=%d\n", r); }
```
三模式均输出 `f 先`/`g 后`/`r=3`（如实记录：本机看不到标准差异）。

## 最新演进与工业实践

- **C++20 的续作**：`operator new` 家族隐式 noexcept 规则细化；`std::vector`
  增删接口普遍加 `noexcept` 条件承诺；**`std::erase/std::erase_if`（C++20）** 的
  强异常保证文档直接依赖成员承诺（链 C++标准库 04 容器）。
- **C++23/26 方向**：P3273?（constexpr placement new 的 noexcept 面）未实测不引 ⚠️；
  真正在途的是把**函数类型里的 noexcept 作为约束推导输入**的持续细化。
- **工业库姿势**：folly 的 `FOLLY_NOEXCEPT`/`folly::checked_divide`?（细节 ⚠️ 不逐引）；
  abseil 规范"移动操作必须 noexcept"为强制 code review 条款；GSL 的
  `Guidelines: R.11/R.12`——"不要返回悬垂/移动操作 noexcept"（编号凭记忆 ⚠️）。
- **静态检查**：clang-tidy `performance-no-automatic-move`（成员有非 noexcept 析构时
  警告移动退化拷贝）——把本章实测的"15 copies"变成 CI 可拦截项。
- 支持矩阵：noexcept 表达式形态 GCC 4.9/Clang 3.3/MSVC 19.0；求值顺序新规则
  GCC 7 起（按 C++17 模式，clang-tidy `readability-*`? 不引）——⚠️ 版本号未逐装验证，
  仅本机 g++ 15.2 行为实测如上。

## 互链

- 移动语义与五法则（noexcept 推导的输入）：[04-右值引用移动语义与完美转发.md](04-右值引用移动语义与完美转发.md)、
  [07-特殊成员函数与继承构造.md](07-特殊成员函数与继承构造.md)
- 异常现代化专题：[../现代C++实战30讲/05-异常与错误处理的现代化.md](../现代C++实战30讲/05-异常与错误处理的现代化.md)
- vector 增长的实现视角：[../C++标准库/04-容器.md](../C++标准库/04-容器.md)
- 条款判断（移动必 noexcept 等）：[../Effective_Modern_C++/05-右值移动完美转发.md](../Effective_Modern_C++/05-右值移动完美转发.md)
- 回 [00 总览](00-总览与阅读地图.md)
