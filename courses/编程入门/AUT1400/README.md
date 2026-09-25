# AmirKabir AP1400-2 高级程序设计 (C++)

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Amirkabir University of Technology AP1400-2: Advanced Programming |
| 学校 | Amirkabir University of Technology (Tehran Polytechnic) |
| 主讲 | 未公开（csdiy 页面未给出；课程无公开主页） |
| 教材 | 无指定教材，作业源码见 GitHub `courseworks` 组织下 `AP1400-2-HW` 系列仓库 |
| csdiy 路径 | https://csdiy.wiki/编程入门/cpp/AUT1400/ （页面更新 2024-04-14） |
| 最新期次 | 1400-2 学期（伊朗历，约 2022 春季） |
| 难度/学时 | 🌟🌟🌟🌟🌟 / 约 50 小时 |
| 状态 | 骨架 |

## 为什么学

- 课程 7 个 homework 质量很高：相互独立、结构简单、配有完善单元测试，是纯 C++ 编程训练的好材料。
- 作业覆盖 Matrix/BST/智能指针/STL 等核心主题，等于把 C++ 关键特性逐个"造轮子"实现一遍。
- csdiy 中难度评级最高的入门级 C++ 课（5 星），适合在 CS106L/CS106B 之后检验真实编码能力。

## 先修与知识联系

- 先修：无 formally 要求；实践上建议先完成 CS106L（标准 C++ 特性）与 CS106B/X（抽象与数据结构）。
- 联系：HW4 实现 SharedPtr/UniquePtr 直接衔接 CS106L 的 RAII/移动语义；HW3 BST、HW6 STL 与 CS106B/X 数据结构部分重叠；课程整体可作为 CS110 (Stanford 系统课) 的 C++ 前置练习。

## 最新年份讲义章节目录（1400-2，按 7 个 Homework 组织）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | HW1：实现 Matrix 类及相关函数 | 运算符重载、类设计（cppreference Matrix 相关章节） |
| L2 | HW2：加密货币客户端/服务端模拟程序 | 基础网络/协议模拟、字符串处理 |
| L3 | HW3：实现二叉搜索树 (BST) | 递归、指针、模板 |
| L4 | HW4：实现 SharedPtr 与 UniquePtr 智能指针 | RAII、引用计数、移动语义（CS106L 讲义） |
| L5 | HW5：继承与多态实现多个类 | 虚函数、vtable |
| L6 | HW6：使用 STL 解决 4 个问题 | `<algorithm>`、容器与迭代器 |
| L7 | HW7：Python 项目（选做） | 语言对比、脚本实践 |

> 注：本课无公开课程主页与讲义，上表按 GitHub 作业源码（AP1400-2-HW）与 csdiy 页面描述整理。
