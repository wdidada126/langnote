# 02 简单的C++程序

> 系列导航：[C++系列·总索引](../C++系列·总索引.md) ｜ [本书单文件大纲](../工程问题C++语言求解.md) ｜ [总览与阅读地图](00-总览与阅读地图.md)

**对应原书章节**：第 2 章（小节已逐条核实：2.1 程序结构；2.2 常量和变量（含科学记数法/数值/布尔/字符/字符串数据/符号常量）；2.3 C++类（声明/实现）；2.4 操作符（赋值/算术/优先级/上溢下溢/自增自减/缩写赋值）；2.5 标准输入输出（cout/流对象/操纵符/cin）；2.6 使用IDE构建C++解决方案：NetBeans；2.7 标准库基本函数（数学/三角/双曲/字符函数）；2.8 解决应用问题：速率计算；2.9 系统限制）。
**工程挑战**：汽车性能。

---

## 核心概念速览（中英对照）

- **符号常量** — symbolic constant（2.2.6）：`const` 命名的常量，替代魔法数字
- **科学记数法** — scientific notation（2.2.1）：`1.234e20` 形式的浮点字面量
- **上溢 / 下溢** — overflow / underflow（2.4.4）：有限位宽浮点数超出/低于可表示范围
- **操纵符** — manipulator（2.5.3）：`setw/setprecision/fixed/scientific` 等改变流格式化状态的对象
- **流对象** — stream object（2.5.2）：`cin/cout` 背后的 `istream/ostream` 类机制
- **自增/自减操作符** — increment/decrement operator（2.4.5）：`++/--`，本书区分前置/后置
- **优先级与结合性** — precedence and associativity（2.4.3）：表达式求值顺序规则
- **类声明 / 类实现** — class declaration / implementation（2.3）：接口与实现分离的 earliest exposure——本书第 2 章就引入类，是其「object-based」路线的标志
- **基本库函数** — library functions（2.7）：`sqrt/pow/sin`（cmath）与 `isdigit/isalpha`（cctype）两类「拿来就用」的黑盒

## 1. 动机：一周内让工程师「能算东西」

本章的设计目标是：不出现分支和循环，也要能完成有工程意义的计算（2.8 速率计算）。为此它把 C++ 的最小可计算子集压缩进一章：变量、算术、格式化 I/O、若干库函数，外加 2.3 的一小节「类」。这个取舍很工程：**先建立「输入→公式→输出」的完整闭环**，再回头补控制流。

## 2. 机制：本章语法的三条主线

**(a) 数据表示**。布尔、字符（借 ASCII，附录 B）、双精度浮点都是「物理量的机器影子」。2.4.4 的上溢/下溢讨论用 16 位 int 与 IEEE double 的极值表来建立边界直觉。`float/double` 的相对精度差异书中着墨不多，是今天必须自行补课的点（见第 4 节）。

**(b) 表达式求值**。赋值即求值（2.4.1）、`=` 与 `==` 的经典陷阱、优先级表背否两可——现代规范做法是加括号 + 靠 `-Wall -Wextra` 的 `-Wparentheses` 兜底。

**(c) 格式化 I/O**。2.5.3 的操纵符是本章最容易「学了忘」的部分：`setw` 只对下一次输出生效、`setprecision` 在 `fixed/scientific` 下语义从「总位数」切换为「小数位数」、`cout` 状态会一直粘着——这些都是当年作业里的常客。

## 3. 权衡：第 2 章就讲「类」，对不对？

Etter 的立场（object-based，非完整 OOP）：把类当作**用户自定义数据类型**的延伸来讲——2.3 只有声明/实现和成员访问，没有继承没有虚函数，到 6.7 才补方法定义、10.2 才谈操作符重载。好处是数据抽象观念早建立；代价是教学版类样例（带私有数据和一两个访问器）往往「太简单以致看不出为什么要类」。C++ Primer 则把类推迟到第 7/13 章，先建立函数与容器的直觉。两种顺序都自洽，工程读者照本书走更顺手。

## 4. 🔧 自编译样例（已实测 g++ 15.2）

书式 C++98（scientific/fixed 切换 + setw + isdigit）：

```cpp
// 编译：g++ -std=gnu++98 ch02_old.cpp
cout << scientific << big << "  " << small << fixed << endl;
cout << "R=" << setprecision(3) << R_GAS << endl;
cout << setw(10) << 42.71828 << "|" << endl;
char c = '7';
cout << boolalpha << "isdigit('" << c << "')=" << isdigit(c) << " isalpha=" << isalpha(c) << endl;
```

实际输出：

```text
1.234000e+20  5.000000e-15
R=8.314
    42.718|
sqrt(2)=1.414 sin(pi/2)=1.000
isdigit('7')=1 isalpha=0
```

同一组需求的 C++20 写法：`std::format`（编译期检查格式串）+ `<numbers>` 常量：

```cpp
// 编译：g++ -std=gnu++20 ch02_modern.cpp
std::cout << std::format("{:.3e}  {:.3e}\n", 1.234e20, 5.0e-15);
std::cout << std::format("R={:.3f}  width=[{:10.5}]\n", R_GAS, 42.71828);
std::cout << std::format("pi={:.6f} e={:.6f} sqrt2={:.6f}\n",
                         std::numbers::pi, std::numbers::e, std::numbers::sqrt2);
```

实际输出：

```text
1.234e+20  5.000000e-15
R=8.314  width=[    42.718]
pi=3.141593 e=2.718282 sqrt2=1.414214
```

注意对比：`{:.3e}` 一行就取代了 `scientific + setprecision(6)` 的状态管理；`{:10.5}` 用一个说明符同时给出宽度与精度，操纵符体系则需要 `setw(10) << setprecision(5)` 两件事且语义随格式状态漂移。

## 5. 最新演进与工业实践

- **格式化演进链**：`printf` → iostream 操纵符（本书）→ {fmt}（https://github.com/fmtlib/fmt）→ C++20 `std::format` / C++23 `std::print`。工程含义：格式化从「运行期状态机」变成「编译期检查的纯函数」。实测注记：MinGW-Builds 15.2 上 `std::print` 链接失败（`undefined reference to std::__open_terminal`，运行时库版本落后），需退回 `std::cout << std::format(...)`——这是真实工具链差异，值得记住。
- **数学常量**：`<numbers>`（C++20）消灭了全书各章手写的 `const double PI = 3.14159265358979;`。
- **auto 与初始化**：现代风格用 `auto rate = dist / time;` 免写类型、用 `{}` 统一初始化（`int n{5};`）防窄化；本书的 `=` 初始化教学在 C++11 后已有更安全的替代。
- **字符与字符串**：`std::string`/`std::string_view` 完全替代了本书 2.2.5 的「字符串数据」教学（字符数组+`\0` 的讨论今天只在读旧代码时需要）；char8_t（C++20）与 UTF-8 源码执行字符集是本书完全没有的维度。
- **IDE**：2.6 的 NetBeans C++ 教学（Oracle 已停止 NetBeans C++ 支持）今天对应 VS Code + clangd、CLion、或 Visual Studio；工程界普遍配 CMake 管理构建，而非 IDE 私有工程文件。
- **数值素养补课**：读本章时应自行补充 IEEE 754 语义（次正规、舍入模式、`std::numeric_limits`），推荐直接看 https://en.cppreference.com/w/cpp/types/numeric_limits ——这是本书 2.4.4/2.9 的现代增强版。

## 6. 相邻概念对比与易错点

- **const 符号常量 vs #define**：本书正确选择 `const`；补充一点：编译期求值场景今天首选 `constexpr`（见 ch01_modern 的 `static_assert`）。
- **`++i` vs `i++`**：本书按「前置先加后用」教；现代补充：对迭代器后置有额外开销，循环里统一写前置（EMC 风格）。
- **cin 的失败状态**：`cin >> x` 失败后流进入 failbit 且**不会自动恢复**，本书 2.9「系统限制」一带而过，第 5 章文件读取才真正踩到——预习时先记住「读循环条件用流本身」。
- **float vs double**：工程计算默认 `double`；`float` 只在显存/带宽受限时用（GPU/HPC），本书未展开。

## 7. 案例深潜：工程挑战「汽车性能」与 2.8 速率计算

本章应用问题的共同形态是**顺序公式程序**（无分支无循环）：

- **2.8 速率计算**：`rate = distance / time` 的完整流水线——声明双精度变量、cin 读入、公式求值、fixed+setprecision 输出。教学点是「I/O 契约先行」：先画输入表再写代码。
- **工挑·汽车性能**：多次加油求平均油耗。落地形态即上节五步法表格；实现时唯一的新知识点是「累加器模式」（`total = total + x` 重复三次），这为第 4 章循环埋下伏笔。
- **2.3 类的首秀**：以「带私有数据+公共操作」的最小样本（如带半径的圆类）呈现，本章不要求读者会写、只要求会**读**——注意这与 6.7/10.2 的三次回环递进。

阅读建议：把 2.9「系统限制」与《C++标准库》的 numeric_limits 表对读，书里「double 约 15–16 位有效十进制数字」的说法对应 `std::numeric_limits<double>::max_digits10 == 17` 的现代精确表述（17 位保证往返，15–16 位是常用工作区间）。

## 8. 自查清单

- [ ] 我能说出 `setw` 与 `setprecision` 谁是一次性、谁是粘性的吗？
- [ ] `fixed` 状态下 `setprecision(3)` 的语义与默认状态有何不同？
- [ ] 我能解释 `while (cin >> x)` 里流到 bool 的转换链吗（本章 2.5 只给了一半答案，第 5 章给全）？
- [ ] `const double R = 8.314;` 与 `constexpr`、`#define` 三者的可见性/类型检查差异？
- [ ] 我知道 `std::format` 的格式串错误为什么能在编译期爆炸吗（consteval 解析）？
- [ ] 上溢/下溢发生时 IEEE 754 与本书「错误报告」教学分别怎么处理？

## 9. 延伸阅读

- 上一站 [01 导论](01-计算与工程问题求解导论.md)；下一站 [03 控制结构：选择](03-控制结构选择.md)
- 类型推导与 auto 的系统讲解：[../Effective_Modern_C++/01-类型推导.md](../Effective_Modern_C++/01-类型推导.md)
- 标准 I/O 库的权威描述：[../C++标准库/01-导读与一般概念.md](../C++标准库/01-导读与一般概念.md)
