# Cornell CS3110 OCaml 编程：正确 · 高效 · 美

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Cornell CS3110: OCaml Programming: Correct + Efficient + Beautiful |
| 学校 | Cornell University |
| 主讲 | Michael R. Clarkson |
| 教材 | 课程自编写在线教材：https://cs3110.github.io/textbook （2018 年起编写，持续更新） |
| csdiy 路径 | https://csdiy.wiki/编程入门/Functional/CS3110/ （页面更新 2024-04-14） |
| 最新期次 | 教材最新版（2e，2024 修订）；视频为 2021 秋季全学期（YouTube/B站） |
| 难度/学时 | 🌟🌟🌟 / 约 40 小时 |
| 状态 | 骨架 |

## 为什么学

- csdiy 评价为 "modern SICP"：SICP 之后最好的函数式入门进阶课，让人体会到什么叫"正确、高效和美"。
- 不止 OCaml 语法：覆盖语言基础、数据结构与算法、测试开发、形式证明、语言特性实现，内容递进互补不割裂。
- 康奈尔打磨 20 余年的课程：源于 MIT 6.001 (SICP)，2008 年更名并改用 OCaml，2018 年开始编写教材。
- 主讲用词简单、表述清晰，视频甚至可当英语听力材料。

## 先修与知识联系

- 先修：了解一门命令式/类 C 语言。
- 联系：与 CS61A 同属 SICP 谱系（Scheme vs OCaml，可互相印证环境模型）；代数数据类型/模式匹配与 cs220 (Rust) 直接对照（Option/Result ≅ Option/Result）；解释器章节衔接 CS420/CS143 编译原理；类型检查章节衔接 CS242； Monad? 副作用与 Haskell MOOC 呼应。

## 最新年份讲义章节目录（按 cs3110.github.io/textbook 现行版本，六大部分）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | Part I 起步：Introduction、Strings and Numbers | Textbook ch.1–2 |
| L2 | 函数式列表处理 | Textbook ch.3 |
| L3 | 函数与高阶函数 | Textbook ch.4 |
| L4 | 代数数据类型与模式匹配 | Textbook ch.5–6 |
| L5 | Option/Result 与错误处理 | Textbook ch.7 |
| L6 | 测试与调试、整洁代码 | Textbook ch.8–10 |
| L7 | Part II 抽象数据类型：Set/Map 接口与实现 | Textbook ADT 章节 |
| L8 | 效率、渐近分析、下界与摊还分析 | Textbook Efficiency/Asymptotics 章节 |
| L9 | Part III 可变状态与副作用：refs、可变数据结构、缓存与备忘 | Textbook Mutable 章节 |
| L10 | Part IV 模块系统：抽象、签名与函子 (Functors) | Textbook Modules 章节 |
| L11 | Part V 类型检查：类型推理与健全性直觉 | Textbook Type Checking 章节 |
| L12 | Part VI 解释器与语言实现：环境模型 | Textbook Interpreters 章节 |
| L13 | 语言特性实现：静态检查、命令式、惰性求值、并发 | Textbook 对应章节 |
| L14 | 附录：证明（关联性与正确性论证） | Textbook Appendix Proofs |

> 教材习题 1–4 星自选，注意 3 星到 4 星难度跨越很大。
