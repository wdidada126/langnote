# Stanford CS106L 标准 C++ 编程

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Stanford CS106L: Standard C++ Programming |
| 学校 | Stanford University |
| 主讲 | Stanford 授课组（csdiy 页面未指名；课程网页 owner 为 Chris Gregg 等，历史主讲 Keith Schwartz） |
| 教材 | 课程自编 Reader：http://web.stanford.edu/class/cs106l/full_course_reader.pdf（无正式出版教材） |
| csdiy 路径 | https://csdiy.wiki/编程入门/cpp/CS106L/ （页面更新 2024-04-14） |
| 最新期次 | 春季学期开课（Reader/作业以最新版为准；csdiy 作者完成于 2020 前后版本） |
| 难度/学时 | 🌟🌟🌟 / 约 20 小时 |
| 状态 | 骨架 |

## 为什么学

- 把"C 语言 + cin/cout"式的伪 C++ 升级为真正的标准 C++：auto binding、统一初始化、lambda、移动语义、RAII 等现代特性系统过一遍。
- 核心作业实现一个类似 `unordered_map` 的 HashMap，把全课知识串联起来，iterator 实现极具挑战。
- Stanford 后续多门课（CS144 计算机网络、CS143 编译器）的项目都基于 C++，本课是这些课的直接前置。

## 先修与知识联系

- 先修：最好掌握至少一门编程语言；与 CS106B/X 互补——CS106B 讲抽象与数据结构，CS106L 专讲 C++ 语言本身。
- 联系：RAII/智能指针 → AUT1400 HW4、CS110L 的所有权思想（对比 Rust 借用检查）；模板 → CS61B Java 泛化的对照；本课 HashMap → CS106B 的哈希表章节。

## 最新年份讲义章节目录（按 Reader/课程大纲，Spring 版本约 10 讲）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论与 C++ 回顾（从 CS106B 视角看"旧" C++） | Reader Ch.1 |
| L2 | auto 类型推导与范围 for 循环 | Reader Ch.2–3 |
| L3 | 统一初始化与数组、vector | Reader Ch.4 |
| L4 | 引用、函数参数传递（by value/by reference/const ref） | Reader Ch.5 |
| L5 | 面向对象：类、继承、虚函数复习 | Reader Ch.6 |
| L6 | STL 容器与迭代器（vector、 iterators 类别） | Reader Ch.7–8 |
| L7 | 关联容器 map/set 与自定义比较 | Reader Ch.9 |
| L8 | 函数对象与 lambda 表达式 | Reader Ch.10 |
| L9 | 智能指针与 RAII（unique_ptr/shared_ptr） | Reader Ch.11 |
| L10 | 移动语义与右值引用、课程总结 | Reader Ch.12；作业2：HashMap 文档 |

> 作业：Assignment1 WikiRacer 小游戏；Assignment2 类 STL 的 HashMap（github.com/snme/cs106L-assignment1、-assignment2）。
