# CS106L 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| Rvalue References: Move Semantics in C++ | A. Chamberlain & B. Stroustrup, 2010 | L10 | 移动语义的原始提案文稿 |
| Exception Safety in C++ | B. Stroustrup, 1994 (Exceptional C++ 由 M. Sutter 展开) | L9 | RAII 与异常安全的关系 |
| The Standard Template Library | A. Stepanov & M. Lee, 1994 | L6–L8 | STL/迭代器/泛型算法设计源头 |
| Generic Programming and the STL | D. Musser & A. Stepanov, 1989 | L6 | 迭代器抽象的由来 |
| C++ Coding Standards | S. Sutter & A. Alexandrescu, 2004 | 全课 | 规范型经典 |

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| C++ Core Guidelines（isocpp 持续修订） | 2021–2024 活跃 | 全课 | 现代化课程内容的官方风格基线 |
| P2588/P2743 等 std::expected 与 std::generator (C++23/26) 提案 | 2022–2024 | L6/L8 | 迭代器与错误处理在标准中的演进 |
| cppreference "C++11/14/17/20 feature support" 表 | 持续更新 | 全课 | 编译器支持矩阵 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| auto/范围 for (L2) | LLVM | 代码风格强制 `for (auto *BB : successors(BB))` 式遍历 |
| STL 迭代器 (L6) | abseil-cpp / Folly | 重新实现并扩展容器/迭代器，接口对齐 std |
| lambda (L8) | REBOUND: Catch2 | 测试框架以 lambda 作为用例体与断言回调 |
| RAII/智能指针 (L9) | Chromium | `std::unique_ptr`/`raw_ptr` 所有权规范文档 |
| 移动语义 (L10) | serde 类库对比: nlohmann/json | 大对象传输零拷贝设计 |
| HashMap 作业 (L6/L7) | Redis dict / Go map 实现 | 开放寻址 vs 链地址工程取舍 |
