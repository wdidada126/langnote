# 01 · Hello模板：模板的编译模型（对应原书第 1 章）

> 原书位置：第一部分「模板基础」第 1 章（P2–15）：为什么需要模板 / 初识函数模板 /
> 模板参数自动推导 / 默认参数 / 静态变量 / HPP 还是 CPP / 链接器如何识别重复实例 /
> 尴尬的 Export Template。
> 本文件：机制转述 + 编译器行为层展开 + g++ 15.2 实测。单文件大纲见
> [../深入实践C++模板编程.md](../深入实践C++模板编程.md)。

## 核心概念速览（中英对照）

- **函数模板** — function template：以类型为形参、按调用点批量生成函数的模具
- **模板实参推导** — template argument deduction：从调用实参反推 `T`；按值参数剥引用与顶层 const
- **模板参数默认值** — default template argument：`template <class T = int>`，当年类模板专属，C++11 起函数模板也可
- **实例化** — instantiation：用具体实参生成模板实体；隐式（用到才生成）与显式（手写生成指令）
- **两阶段名字查找** — two-phase name lookup：非依赖名在**定义时**查，依赖名在**实例化时**查
- **依赖名** — dependent name：含模板参数的名字；取其嵌套类型必须写 `typename`
- **每实例一份静态变量** — static per instantiation：`f<int>` 与 `f<double>` 的 static 是两个对象
- **隐式包含模型** — implicit inclusion model：模板定义须对每个使用 TU 可见 → 实现进头文件（HPP）
- **外名模板** — exported template（`export`）：让定义可对他 TU 隐藏的失败机制，C++11 移除
- **显式实例化定义/声明** — explicit instantiation definition/`extern template`：手动控制在哪产码、在哪禁码

## 动机：重载是线性的，模板是对数的

书中开篇的论证（机制转述）：为 `int/short/double` 各写一个 `max` 重载，是**复制粘贴的
类型排列**；每加一种类型都要动源码。函数模板把「类型」从函数签名里抽出来当参数，
一份定义对无穷多类型生效——这是泛型（generic programming）的朴素定义：
**算法与容器元素类型解耦**。

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
template <class T>
T my_max(T a, T b) { return a > b ? a : b; }
// my_max(3, 7)            → 推导 T=int，生成 my_max<int>
// my_max(3, 7.5)          → 编译错误：T 既推成 int 又推成 double，冲突
// my_max<double>(3, 7.5)  → 显式给定 T，实参走常规隐式转换
```

推导规则要点：按值形参 `T` 会**剥掉引用与顶层 const**（`const int&` 实参推出 `T=int`）；
两个形参推出矛盾的 `T` 即候选失效；显式模板实参可封死推导。这些在 2013 年是「经验规则」，
今天有术语表（value category / initialization 各子句，[../Effective_Modern_C++/01-类型推导.md](../Effective_Modern_C++/01-类型推导.md) 系统整理）。

**默认模板参数**：书中演示 `template <class T = int> struct Box;`。当年函数模板不能用默认
模板参数（C++98 限制），C++11 放开；而 C++14 起函数模板默认实参直到**下一次函数声明**
才生效（独立模板不共享默认值），这是个经典坑（⚠️ 原书未提，本目录补记）。

**静态变量**：`f<T>` 里的 `static int n` 是**每个实例化一份**——`f<int>::n` 与 `f<char>::n`
互不相干。机制：static 属于生成的那个具体函数实体。这为 08 章「元函数用枚举常量传值」
与 traits 计数器等惯用法埋下伏笔。

## 机制：一个模板调用在编译器里发生了什么

1. **名字查找分两阶段**（GCC/EDG 等前端严格实现；MSVC 对阶段一曾长期宽松）：
   定义时检查不依赖模板参数的名字；实例化时（依赖名具体化后）再检查依赖部分。
2. **实例化时机**：隐式实例化「用到才做」，在**每个使用它的 TU** 里各做一遍——
   同一段代码会被不同 TU 重复编译生成。
3. **链接期去重**：各 TU 生成的同名同签名实例被放进 **COMDAT 折叠段**（MSVC）或
   **linkonce/弱符号**（ELF/COFF），链接器任选一份、丢弃其余。「链接器如何识别重复模板
   实例」一节讲的就是这套：符号带 weak/COMDAT 属性 + 名称由模板签名修饰（name mangling）
   决定同一性。

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17：两阶段查找的可观察证据
template <class T>
void phase_bad() { int x = notDeclaredAnywhere; (void)x; }
// 只写不实例化，上面这行也立刻报错——非依赖名，定义时（阶段一）就检查

template <class T>
struct Wrapped { typename T::value_type inner; };  // 依赖嵌套类型必须 typename
```

`typename` 的必要性也是阶段一问题的产物：编译器定义期不知道 `T::value_type` 是类型还是
静态成员，默认按「非类型」解析，所以要用 `typename` 显式改判（成员模板定义前加 `template`
关键字改判嵌套模板同理）。

## HPP 还是 CPP：为什么模板实现藏不住

书中设问：把函数模板声明放 H、定义放 CPP，另一个 TU 调用会**链接失败**——
因为定义所在 TU 看不到使用点，不会实例化；使用 TU 看不到定义，也无法实例化；
链接器两头都没有实体。这就是**隐式包含模型**的代价：模板定义必须放进每个使用者
可见的头文件（HPP/inline 进头）。

**Export 之死**：C++98 给了正解——`export template`，让定义藏进 CPP、按需从「模板库」
导出实例。书中第 1.4 节记录了它的尴尬：需要编译器实现「存储/复用编译结果」的完整机制，
复杂度爆炸，主流编译器只有 EDG 前端勉强支持、GCC/MSVC 从未实现，最终 **C++11 把
`export` 关键字废弃**（复用为模块导出）。⚠️ 确切移除提案号本次未核实，机制与年代已核实。
工业界的答案是另一条路：**显式实例化**接管控制——

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17
template <class T> T add(T a, T b) { return a + b; }
template int add<int>(int, int);            // 显式实例化定义：本 TU 强制产码
extern template double add<double>(double, double); // 抑制本 TU 隐式实例化（N1987）
```

`extern template`（C++11, [wg21.link/N1987](https://wg21.link/N1987) 实测可达，
"Adding extern template"）不是 export 的复活：它不导出定义，只做**减法**——告诉本 TU
「别再隐式实例化这个，去链接别的 TU 产好的」。它至今活着，且是治理 06 章代码膨胀的主力。

## 权衡与相邻概念对比

| 方案 | 编译防火墙 | 链接器负担 | 跨 TU 复用编译结果 | 现状 |
| --- | --- | --- | --- | --- |
| 头文件隐式包含 | 无（全暴露） | COMDAT 去重 | 否，每 TU 重编 | 默认主流 |
| export 模板 | 有 | 轻（理想中） | **是**（理想中） | 死亡，C++11 移除 |
| 显式实例化封闭集 | 半（常用类型预实例化） | 轻 | 半（实例化一次） | 活跃：fmt 即如此 |
| **模块（C++20）** | **有** | 轻 | **是（编译结果序列化）** | export 遗志的真正继承者 |

对比要说到编译器行为层面：显式实例化 + `extern template` 组合拳下，编译器对
`extern` 声明的实体**跳过隐式实例化、只留声明**，产码集中在指定 TU；代价是
「没被预实例化的类型」链接失败而不是回落重编——策略从「全自动」变成「白名单」。

## 最新演进与工业实践

- **模块是 export 的精神续作**：C++20 modules 序列化的是语义而非文本，模板的定义可见性
  问题被连根换掉（编译模型层面对比另见 [../C++20模板元编程.md](../C++20模板元编程.md) 的库章节）。
- **显式实例化的工业样板——fmt**：`fmt/base.h` 对 `basic_format_parse_context` 等
  核心类模板用 `FMT_EXTERN_TEMPLATE_API`（即 `extern template`）抑制逐 TU 实例化，
  链接期复用 lib 内实体——正是本章两节的合流应用（github.com/fmtlib/fmt）。
- **两阶段查找的现状**：GCC/Clang 一致严格执行；概念（C++20）引入后依赖名检查时机不变，
  但约束不满足时报错提前到「重载决议淘汰时」并带人话诊断（实测见
  [06-概念与代码膨胀.md](06-概念与代码膨胀.md)）。
- **CTAD 反哺推导**：C++17 类模板参数推导（P0091R3，实测可达）把「从构造实参推 T」
  的机制还给类模板，`std::pair p{1, 2.0};` 不再手抄类型（详见
  [10-变参模板与C++11特性.md](10-变参模板与C++11特性.md)）。

## 自查

- `template <class T> void f(T a, T b)` 用 `f(1, 2.0f)` 调用为何失败？——两形参推导冲突，
  候选在重载决议前就被剔除（这不是 SFINAE 报错，只是不可行）。
- 为什么模板 static 变量能当「编译期计数器」用？每实例化一份的链接属性是什么？
- `extern template` 与 `export` 一字之差，方向差在哪？（减法 vs 导出）

**下一步**：[02-类模板与模板参数.md](02-类模板与模板参数.md)——把同一套编译模型用到类上。
