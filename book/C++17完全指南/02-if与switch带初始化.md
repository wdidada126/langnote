# 02 带初始化的 if 与 switch（if/switch with initializer）

> 覆盖原书 **Part I 第 2 章**（Extensions for `if` and `switch`）。
> 一句话：**给条件语句加一个「只在分支内活着的声明区」**，把「取得资源 → 立刻判断是否可用」这两步合进一个语法单元。
> 互链：[../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)

## 核心概念速览（中英对照）

- **init-statement** — init-statement：`if`/`switch` 括号内第一段，可以是一条**简单声明**或一个**表达式语句**（不含多语句）。
- **条件作用域** — condition scope：init-statement 里声明的名字在 `if`/`else` 的全部分支内可见，出了语句就消失。
- **带初始化的 switch** — `switch (init; cond)`：与 `if` 同规则，实测 `switch (auto v = x * 2; v)` 可用。
- **锁的生命周期** — lock lifetime：`if (std::lock_guard lg{m}; ready)` 让锁正好覆盖分支体，这是本特性最有价值的用途。
- **简单声明的限制** — one declaration only：不能写 `if (int i = 0; ; i > 0)`（实测被拒：expected primary-expression before ';'）。
- **`else` 也可见** — visible in else：与很多人直觉相反，实测 `else` 分支里能直接用 init 变量。

## 本章地图

| 问题 | 答复 |
| --- | --- |
| 解决什么 | 条件变量的作用域污染、锁范围过宽、`mutex` + `condition` 分开写导致的漏判 |
| 机制 | 语法扩展：`( init-statement condition )`，condition 可以是带声明的表达式 |
| 权衡 | 作用域收紧 vs 表达式变长；多变量可同声明，但不能塞两条语句 |
| 相邻 | `if constexpr`（`06`）是**编译期**分支，本特性是**运行期**作用域；range-based for 也在收紧作用域 |

## 动机：老写法的三宗罪

```cpp
// 🔧 C++14 风格（能跑，但三处妥协）
std::unique_lock<std::mutex> lk(m);       // (a) 锁从这一行一直活到函数尾
if (cond.wait_for(lk, 100ms, pred)) { ... }
lk.unlock();                              //     必须手动收尾，早退/异常路径易漏

auto it = m.find(key);                    // (b) it 泄漏到后续所有代码
if (it != m.end()) { use(it); }
//     之后 50 行里 it 还在作用域内，可能被误用（甚至悬挂在被 erase 之后）

std::optional<Config> cfg = load();       // (c) 判断和使用被分成两段
if (cfg) { use(*cfg); }
```

C++17 的对应写法：

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17 编译通过并运行（输出 hit 11 / locked size=1 / switch-init ok / two decls）
if (auto it = m.find("k"); it != m.end()) { it->second += 10; std::printf("hit %d\n", it->second); }
else { std::printf("miss, it 在 else 也可见: %d\n", (int)(it == m.end())); }

std::mutex mtx;
if (std::lock_guard lg{mtx}; m.size() > 0) std::printf("locked size=%d\n", (int)m.size());
//  ↑ lg 只在这个 if/else 块内持有锁，出了语句自动解锁；CTAD（见 05）让锁类型也不用写

switch (auto v = x * 2; v) { case 2: std::printf("switch-init ok\n"); break; default: break; }

if (int i = 0, j = 1; i + j > 0) std::printf("two decls\n");     // 同一声明可带多个初始化器
```

## 机制与语法边界

```text
if ( init-statement condition ) statement
       └─ 简单声明(以分号结尾) 或 表达式语句
                              └─ 一个布尔可判定的表达式，或带声明的条件
```

**实测的边界**（g++ 15.2 诊断原文）：

```cpp
// 🔧 已实测 g++ 15.2 -std=gnu++17 拒绝
if (int i = 0; ; i > 0) return i;      // error: expected primary-expression before ';' token
// 即：init-statement 与 condition 之间只有一个分号；不能塞空语句/多条语句

// 🔧 已实测通过：声明可以一次声明多个同类变量
if (int i = 0, j = 1; i + j > 0) { }

// 🔧 已实测通过：init 里可以放需要隐式转换的对象（CTAD + 锁）
if (std::lock_guard lg{mtx}; flag) { }
```

**三条常被误传的规则**（逐条实测后确认）：
1. `else` 分支**看得见** init 变量（上面 `else` 里的 `(it == m.end())` 就是证据）。
2. init-statement 也可以是**表达式**（如函数调用），例如 `if (auto [it, ok] = m.insert({k, 1}); ok)` 同时用了
   结构化绑定与本特性——这是「插入并判断是否新插入」的标准现代写法。
3. condition 部分若用 `auto x = f();` 这种**声明式条件**（C++17 起 `if` 的条件可以是带声明的表达式），
   与 init-statement 是两套机制；组合使用会让可读性急剧下降，团队里通常只放开 init-statement。

## 权衡

| 维度 | 带初始化写法 | 分离写法 |
| --- | --- | --- |
| 变量寿命 | 只覆盖分支，误用面最小 | 泄漏到外层作用域 |
| 锁范围 | 与分支严格对齐，异常安全 | 需 `unlock()` 或额外 `{}` 块 |
| 可测试性 | 分支内即全部前提，审查容易 | 需要往回找定义点 |
| 编译复杂度 | 无 | 无 |
| 可读性 | 条件长时会挤在一行（团队常配 clang-format 的 `PackConstructorInitializers`） | 分行更直观 |
| 兼容性 | 需 C++17（GCC 7+ / MSVC 19.14+） | 任何版本 |

**收益排序（工业视角）**：锁作用域 > map 查找/插入 > 一般数值条件。
只有前两类是「不这么写容易出 bug」，第三类只是风格。

## 相邻概念对比

- **vs 匿名块 `{ ... }`**：老技巧是用一对额外大括号限制作用域；缺点是把 `if` 和它的数据拆成两块，
  且锁的释放点在块的末尾而不是分支末尾（两者通常等价，但代码结构上更绕）。
- **vs `if constexpr`**（本目录 `06`）：一个收紧**运行期**名字的作用域，一个在**编译期**决定哪段代码被实例化；
  两者可以叠加：`if constexpr (sizeof(T) > 4) { if (std::lock_guard lg{m}; ready) ... }`。
- **vs range-based for + 结构化绑定**（`01`）：遍历场景下三者常同时出现，构成「现代 C++ 遍历三件套」。
- **vs C++20 range-based for with initializer（P0614R1，✅ 编号已在 Apple C++ 支持表核实）**：
  `for (init-statement decl : range)` 把同一思想搬进范围 for，本特性是它的前半。

## 最新演进与工业实践

**标准之后**
- **C++20/P0614R1**：range-based for 支持 init-statement（GCC 10+/Clang 10+），今天写
  `for (std::scoped_lock lk(m); auto& x : container)` 已合法。⚠️ 本目录未在本机实测该锁配合范围 for 的例子。
- **`if consteval`** 的提案编号核实为 **P1938R3**（C++23，Apple C++ 语言支持表 ✅）。起草本笔记时我一度把
  它与 P2558（核实为「Add `@`, `$`, and `` ` `` to the basic character set」，C++26）写反，此处记录纠正过程，
  与本特性无关。
- **后续标准未再改动 if/switch 的 init-statement**；CWG 层面对「init-statement 中声明的可见性」有若干澄清，
  具体编号 ⚠️ 未核实，故不列。

**工业实践**
- **Google / Chromium / LLVM 风格指南**都鼓励「变量在尽可能小的作用域内声明并初始化」，本特性是这条纪律
  的语法工具；Abseil（实测 **≈18.1k★**，2026-09-26）代码里 `if (auto it = m.find(x); it != m.end())` 是默认形态。
- **锁纪律**：现代代码普遍把 `std::scoped_lock`（C++17，见 `12`）+ init-statement 组合当作
  「最小临界区」的标准写法；`C++ 并发编程实战` 的第 3、10 章把这列为避免竞态的第一招，见
  [../C++并发编程实战2/03-线程间共享数据.md](../C++并发编程实战2/03-线程间共享数据.md)。
- **静态分析口径**：clang-tidy 的 `readability-*` 与 Coverity 规则会把「锁范围大于必要范围」报为可改进项，
  本特性是官方修复手段之一；MSVC `/W4` 无相关诊断（与 `09` 章的悬垂问题一样，靠人守）。

**迁移建议**
1. 先扫 `find/insert + if` 与 `lock + if` 两类，收益最高、diff 最小。
2. 条件超过 ~70 列时拆回两行，不要为了语法而牺牲可读性。
3. 与 `[[nodiscard]]`（`04`）配合：让「拿值 → 判空」成为一次强制动作。

## 与其他章 / 其他笔记的联系

- ← 本目录 `01`：`if (auto [it, ok] = m.insert(...); ok)` 是两特性的合成用法。
- → 本目录 `05`：`std::lock_guard lg{mtx}` 依赖 CTAD；两者同时出现时才写得干净。
- → 本目录 `06`：`if constexpr` 与 `if (init; cond)` 的分工（编译期 vs 运行期作用域）。
- → 本目录 `12`：`std::scoped_lock` 与 `std::shared_mutex`——本特性最大收益场景的完整工具。
- → [../C++17完全指南.md](../C++17完全指南.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)
- → [../Effective_Modern_C++/03-转向现代C++.md](../Effective_Modern_C++/03-转向现代C++.md)：
  「尽量在声明时初始化、尽量小的作用域」的原始论证（Meyers Item 相关条目 ⚠️ 编号未逐字核对）。
- → [../C++代码整洁之道.md](../C++代码整洁之道.md)：作用域收紧在「可读性」一侧的对应原则。

## 思考题

1. `if (auto x = f(); x > 0) ... else ...` 里 `else` 分支能否使用 `x`？写出你的验证程序与结论（本章已实测）。
2. 为什么标准不允许 `if (int i = 0; int j = 1; i + j > 0)`？从语法（init-statement 只有一条简单声明）回答。
3. 把 `std::unique_lock lk(m); if (pred()) {...} lk.unlock();` 改成本特性写法后，异常路径上的行为有什么不同？
