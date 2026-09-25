# AP1400-2 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| A History of C++: 1979−2009 (HOPL III) | B. Stroustrup, 2007 | 全课 | 理解 C++ 特性（含智能指针、模板）的设计动机 |
| The C++ Programming Language (4th Ed.) | B. Stroustrup, 2013 | L1/L4/L6 | 无官方教材时的替代主参考 |
| Exceptional C++ / More Exceptional C++ | M. Sutter, 1999/2002 | L4/L5 | RAII、资源管理、类设计的经典问答式材料 |
| Intrusive vs. Non-Intrusive Smart Pointers | A. Alexandrescu, 1998 (Modern C++ Design 章节) | L4 | 智能指针设计空间 |
| Balancing Binary Trees | G. Adel'son-Velsky & E. Landis, 1962 | L3 | BST 及其平衡化的源头论文 |

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| C++ Core Guidelines（持续更新版） | 2021 修订活跃 | 全课 | 实现 Matrix/智能指针时的现代规范依据 |
| cppreference.com 现代 C++ 特性页 | 持续更新 | L4/L6 | C++17/20 语义查证 |
| "std::shared_ptr 的原子性与数据竞争" 系列 CWG/LWG 讨论 | 2021+ | L4 | 理解引用计数线程安全边界 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| Matrix 运算符重载 (L1) | Eigen | 表达式模板矩阵库，运算符重载极致应用 |
| BST (L3) | RocksDB (memtable) | 跳表/树结构替代，对照学习 |
| 智能指针 (L4) | LLVM | `std::unique_ptr` 管理 IR 节点所有权 |
| 多态 (L5) | Cherry-pick: fmtlib | 类型擦除与虚接口设计 |
| STL 算法 (L6) | Folly (Meta) | 容器/算法增强库，看工业级用法 |
