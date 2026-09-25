# CS106L 讲义要点（骨架，依据 full_course_reader.pdf 章节主题整理）

## L1 导论与 C++ 回顾
- "C with iostream" 不是 C++：本课目标语言是 11/14 标准后的现代 C++。
- 编译链路：预处理、编译、链接；头文件与 include guard。
- 与 Java/Python 的心智模型差异：值语义与栈分配优先。

## L2 auto 与范围 for
- auto 推导规则（指针/引用/const 的组合）。
- 范围 for：`for (const auto& x : v)` 为默认习惯。
- 避免隐式收窄与 `auto` 在初始化中的陷阱。

## L3 统一初始化与 vector
- `{}` 初始化 everywhere，避免 most vexing parse。
- vector 作为默认容器；resize/push_back/initializer_list。
- C 风格数组的遗留问题与替代方案。

## L4 引用与函数
- 传值 vs 传引用 vs 传 const 引用：拷贝成本分析。
- 返回值优化与避免悬垂引用。
- 重载解析基础与 const 正确性。

## L5 面向对象复习
- 类接口/实现对齐；explicit 的意义。
- 继承与虚函数、重写 vs 重载。
- Rule of Three/Five 预告（与 L9/L10 呼应）。

## L6 STL 容器与迭代器
- 迭代器类别（input/output/forward/bidirectional/random access）。
- begin/end 半开区间约定；erase-remove 惯用法。
- HashMap 作业：自写迭代器需处理桶遍历与失效。

## L7 map 与 set
- 有序容器（红黑树）vs 无序容器（哈希）。
- 自定义比较器与 `operator<`。
- `[]`、`at`、`insert_or_assign` 语义差异。

## L8 函数对象与 lambda
- 仿函数 = 带 `operator()` 的对象；lambda 是其语法糖。
- 捕获列表：值捕获/引用捕获及悬垂风险。
- 配合 algorithm（for_each/transform/count_if）写声明式代码。

## L9 智能指针与 RAII
- 资源获取即初始化：用对象生命周期管堆/文件/锁。
- unique_ptr 的所有权唯一性；shared_ptr 引用计数与循环引用。
- 何时仍需要裸指针（非拥有观察者）。

## L10 移动语义
- 右值引用、`std::move` 的真实含义（强制转 xvalue）。
- 移动构造/赋值与 Rule of Five。
- copy-and-swap 与完美移动容器元素；收尾串联 HashMap 作业。
