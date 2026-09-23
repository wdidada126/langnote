# More Effective C++




## 精读补写（系统整理，2026-09-23）

### 版本与 ISBN
- 《More Effective C++：35 个改善编程与设计的有效方法（中文版）》，Scott Meyers 著，**侯捷 译**，电子工业出版社（"传世经典书丛"），**ISBN `978-7-121-12570-6`**（2011 年出版，2020 年重印，317~336 页，¥59）。
- 英文原版 *More Effective C++: 35 New Ways to Improve Your Programs and Designs*（Addison-Wesley, 1996，ISBN `0-201-63371-X`）。**英文版没有第 2 版**（作者说明：本书写作时 C++ 标准已近定案）。
- 姊妹篇：《Effective C++》第 3 版（2005，ISBN `0-321-33487-6`）；进阶：**《Effective Modern C++》**（2014，ISBN `978-1-491-90399-5`，讲 C++11/14）——**现代 C++ 实践应以后者为主，本书用于理解"设计动机"**。

### 主线脉络（35 条款，6 个议题）
1. **基础议题**：区分指针与引用；优先 C++ 风格转型（`static_cast`/`const_cast`/`dynamic_cast`/`reinterpret_cast`）；绝不以多态方式处理数组；非必要不提供默认构造函数。
2. **操作符**：警惕用户自定义类型转换函数；区分 `operator++` 的前缀与后缀形式；**不要重载 `&&`、`||`、逗号运算符**（会丢失短路/求值顺序语义）。
3. **异常**：用对象（RAII）管理资源以防泄漏；在构造函数中防止资源泄漏；理解"抛出异常"与"传递参数"/"调用虚函数"的差异；**按引用捕获异常**；审慎使用异常规格。
4. **效率**：80-20 法则；考虑懒惰计算（lazy evaluation）；分期摊还预期计算；理解临时对象来源与返回值优化（RVO）；协助编译器完成返回值优化；通过重载避免隐式类型转换；优先使用 `op=` 而非单独 `op`；考虑用程序库（如 STL）替换手写实现；理解虚函数、多继承、虚基类与 RTTI 的成本。
5. **技术（高阶 patterns）**：virtual constructor / clone；智能指针（auto_ptr → 现已被标准库取代）；引用计数；代理类（proxy class）；双分派（double dispatch）；让函数根据多个对象类型虚拟化。
6. **杂项讨论**：未来时态设计、将非尾端类设计为抽象类、如何在同一程序中混合 C++ 与 C、让自己习惯标准 C++ 语言。

### 经典论文与原始文献根基
- **Stroustrup**《The Design and Evolution of C++》(1994) 与《The C++ Programming Language》——理解条款背后"语言为什么这样设计"。
- **Sutter**《Exceptional C++》(2000) 与《More Exceptional C++》(2002)——异常安全与异常规格议题的深入讨论，是本书第 3 议题的最佳补充。
- **Alexandrescu**《Modern C++ Design》(2001)——策略（policy）与 typelist，本书"技术"议题中 proxy/双分派思想的模板化升级。
- **Gamma 等《设计模式》**(GoF, 1994)——virtual constructor、proxy、双分派等条款对应的模式原文。
- **C++ 标准与提案**：`std::auto_ptr` 的设计缺陷与弃用（C++11 起由 `unique_ptr` 取代）、异常规格的移除（C++17，JTC1/SC22/WG21 P0003 系列）均有明确标准演进文档可查。

### 最新研究与产业进展（C++11/14/17/20/23 对本书条款的更新）
- **智能指针已被标准库接管**：条款中的手写引用计数、auto_ptr 已过时；现代代码应使用 `std::unique_ptr` / `shared_ptr` / `weak_ptr`，并注意 `make_shared`/`make_unique` 与循环引用（配合 `weak_ptr`）。
- **移动语义与完美转发**（C++11）：改变"临时对象/返回值"的取舍；RVO/NRVO 与 copy elision 在 C++17 起对纯右值成为**强制优化**（guaranteed copy elision），条款中"协助编译器完成 RVO"的必要性下降。
- **异常规格已移除**（C++17）：`throw()` 之外改用 `noexcept`（既是优化提示也是契约）；C++23 的 `std::expected` 为"可预期的失败"提供了异常之外的替代路径。
- **转型条款依然成立**，但现代补充：`std::variant`/`std::any` 与 `std::visit` 可减少 `dynamic_cast` 的使用；C++20 `concepts` 与 `requires` 让模板约束优于 SFINAE 技巧。
- **代理类/双分派**：C++17 `std::variant` + `std::visit`、C++23 的 pattern matching 提案（P1371 等）正在把"多重分派"变成语言级能力，手写 double dispatch 的必要性降低。

### 常见误区 / 纠错
- **本书出版于 1996 年，部分条款已被现代 C++ 取代**：阅读目标是"理解设计的动机与代价"，实践应优先采用标准库与 C++11 之后的惯用法（即《Effective Modern C++》）。
- **不要重载 `&&`/`||`/逗号** 的理由至今成立：重载后失去短路求值与内建求值顺序保证，会导致难以察觉的语义 bug。
- **"引用一定比指针安全"需限定语境**：引用不可为空、不可重绑定，但也可能悬垂（绑定到已销毁对象）；智能指针与生命周期管理才是根本解法。
- 日常笔记若把本书当作"现代 C++ 最佳实践清单"引用，建议同步标注"1996 年语境"，以免误导。
