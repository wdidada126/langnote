# Stanford CS110L 系统安全编程 (Rust)

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Stanford CS110L: Safety in Systems Programming |
| 学校 | Stanford University |
| 主讲 | Ryan Berhardt（reberhardt.com） |
| 教材 | 无指定教材；官方 slides + Rust Book；补充可读 CS242 Fall2019 第 6–9 周 Rust 讲义 |
| csdiy 路径 | https://csdiy.wiki/编程入门/Rust/CS110L/ （页面更新 2024-04-14） |
| 最新期次 | Spring 2020（2021 版页面补充 Futures Trait 视频；2022 起未再开源作业源码） |
| 难度/学时 | 🌟🌟🌟 / 约 30 小时 |
| 状态 | 骨架 |

## 为什么学

- 用 Rust 理解"系统编程的安全性"：在保留 C 级效率与底层控制的同时，用所有权/类型系统在编译期消灭整类内存错误。
- 后半程系统比较多种并发范式：多进程、多线程、消息传递、事件驱动/futures——这些是 OS、网络编程课程的共同地基。
- 两个 Project 含金量高：用 Rust 写一个类 GDB 的 debugger、写一个负载均衡器；清华 rCore 操作系统实验同样基于 Rust，学完可直接衔接。

## 先修与知识联系

- 先修：一定编程背景 + 计算机系统初步认识（CS106L/CS106B/X 或 CSAPP 级别）。
- 联系：与 CS107/CS110（C 系统课）互补——Rust 重新审视同一批系统问题；所有权模型对照 C++ 智能指针（CS106L L9）；并发部分直通 15-418/CS149 与 CS144；KAIST cs220（练习强化）、cs431（并发理论深化）是本课的自然后继。

## 最新年份讲义章节目录（Spring 2020，约 10 周；6 Lab + 2 Project）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | Rust 导论与安全系统编程动机 | Course slides W1；Rust Book ch.1 |
| L2 | 类型、表达式与控制流（Lab1） | Slides W2；Rust Book ch.3–4 |
| L3 | 所有权与借用 | Slides W3；Rust Book ch.4 |
| L4 | Trait 与泛型 | Slides W4；Rust Book ch.10 |
| L5 | 数据结构与枚举：Vec、Option、Result（Lab2/3） | Slides W5；Rust Book ch.6/8 |
| L6 | 闭包、迭代器与作用 | Slides W6；Rust Book ch.13 |
| L7 | 智能指针与内部可变性：Box/Rc/RefCell | Slides W7；Rust Book ch.15 |
| L8 | 线程与消息通道；共享状态（Lab4/5，Project1: debugger） | Slides W8；Rust Book ch.16 |
| L9 | Futures 与异步并发；错误处理 | Slides W9 + 2021 补充视频；Rust Book ch.17 |
| L10 | 事件驱动/actor 并发与范式对比（Project2: load balancer） | Slides W10；CS242 W6–9 Rust 讲义 |
