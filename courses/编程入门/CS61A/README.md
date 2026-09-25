# UCB CS61A：计算机程序的构造和解释（Structure and Interpretation of Computer Programs）

> **【CORE 核心课程】** 本文件为完整版 README（含全章节目录）。状态：**全量（2026-09）**——`notes/` L01-L26 逐讲中文笔记、`papers.md` 文献与开源映射、`projects/` 六套可运行配套项目均已就位（见下文各表链接）。

## 一、课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 / 课程号 | Structure and Interpretation of Computer Programs / CS 61A（UCB EECS 入门核心课，CS61 系列第一课） |
| 学校 | UC Berkeley |
| 主讲 | Josh Hug（近数学期；历期含 Paul Hilfinger 等） |
| 教材 | 主教材 *Composing Programs*（官方电子书，作者 Chris Pritchard 等）；**中文译本**（composingprograms 中文翻译版）；进阶参考 SICP（Abelson & Sussman，MIT 6.001 原教材，有中译本《计算机程序的构造和解释》） |
| csdiy 路径 | `编程入门/Python/CS61A`（csdiy.wiki） |
| 最新期次 | 课程页面备份列 **spring2026**；作业与视频以 **fall2024** 为准（csdiy 推荐）；另备份 spring2022/fall2022/fall2020 |
| 状态 | **全量（2026-09）**：README + L01-L26 笔记 + papers.md + 六套配套项目 |

- 课程网站：官网 site 见 csdiy「课程网站」链接（学期站形如 `https://<term>.cs61a.org`；spring2026/fall2024 等有页面备份）
- 课程视频：YouTube 合集（spring2024 / fall2022 / fall2020 全套公开）
- 课程教材：Composing Programs 电子书 + 中文翻译（csdiy 提供双链接）
- 课程作业：fall2024 全套 HW/Lab/Project 公开，评分器 okpy 可用
- csdiy 标注：先修无 ｜ 语言 Python, Scheme, SQL ｜ 难度 🌟🌟🌟 ｜ 预计 50 小时
- 资源汇总：PKUFlyingPig/CS61A、InsideEmpire/CS61A（GitHub，含全部作业实现）

## 二、为什么学

- 它**不是 Python 语法课**，而是伯克利计算机专业的灵魂入门课：以"抽象"为主线，学会用程序构造解决实际问题，而不纠结硬件细节。
- 一学期内完成三种语言（Python → Scheme → SQL）的跨越，并在 **Project 4 亲手用 Python 实现一个 Scheme 解释器**，直抵"语言如何被解释执行"的本质——这是与所有速成课的根本区别。
- 承上启下：向下衔接 CS61B（Java 大型项目）、CS61C（RISC-V 与 CPU），构成伯克利 CS61 核心三部曲；向上为 SICP 原著 readers 铺路。
- 作业体系（4 Project + 9 Lab + 8 HW + Disc）质量极高且全部免费开源，练完即拥有可写进简历的解释器项目。

## 三、先修与知识联系

- 先修：无官方先修。csdiy 提示：完全零基础直接学需要较强自律；可先修 Harvard **CS50x** 或 **CS50P / MIT 6.100L** 过渡（本仓库均已收录于同分类）。
- 知识联系：
  - → CS61B（数据结构，Java）、CS61C（体系结构）：CS61 系列接力；
  - → SICP / MIT 6.001、Stanford CS107、各编译原理课：解释器与元循环求值是共同核心；
  - ← Missing Semester：工程工具链（git/命令行）建议同步掌握以完成作业。

## 四、讲义目录（26 讲，每周 2 讲 × 13 周；按 spring2025/2026 稳定主题组织）

> 讲次编号 L01-L26 与 [notes/](notes/) 下笔记文件一一对应；官方学期站按 week 排列，主题结构一致。

| 讲次 | 标题 | 阅读材料 | 配套项目 |
| --- | --- | --- | --- |
| [L01](notes/L01.md) | 课程导论：程序的构造与解释；整数与布尔表达式 | CP §1.1；SICP 视频 1A | — |
| [L02](notes/L02.md) | 编程元素：表达式求值、名字与环境模型 | CP §1.2 | [p1_expr](projects/p1_expr/README.md) |
| [L03](notes/L03.md) | 函数抽象：def、参数、返回值与调试入门 | CP §1.3/§1.5；Debugging Guide | [p2_abstraction](projects/p2_abstraction/README.md) |
| [L04](notes/L04.md) | 函数设计与控制流：条件、域假设与声明式风格 | CP §1.4-1.5 | p2 |
| [L05](notes/L05.md) | 高阶函数 I：函数作为参数 | CP §1.6.1-1.6.2 | p2 |
| [L06](notes/L06.md) | 高阶函数 II：返回值、currying、闭包与装饰器 | CP §1.6.3-1.6.4 | p2 |
| [L07](notes/L07.md) | 递归函数：分治、树递归与递归调试 | CP §1.7；SICP §1.2.1 | p2/p3 |
| [L08](notes/L08.md) | 两类过程：迭代与递归；增长阶（Big O） | SICP §1.2；CP §1.7.4 | p3 |
| [L09](notes/L09.md) | 期中 1 复习：从函数到过程 | Practice Midterm 1 | 复盘 p1/p2 |
| [L10](notes/L10.md) | 数据抽象：复合数据与抽象屏障 | CP §2.1；SICP §2.1 | [p3_data](projects/p3_data/README.md) |
| [L11](notes/L11.md) | 序列：list/tuple/range 与高阶序列操作 | CP §2.2；itertools 教程 | p3 |
| [L12](notes/L12.md) | 迭代器协议与生成器函数 | CP §2.2.4 | [p5_streams](projects/p5_streams/README.md) |
| [L13](notes/L13.md) | 可变数据、对象与链表 | CP §2.3；Linked Lists 文章 | p3（linked.py） |
| [L14](notes/L14.md) | 面向对象 I：类、实例、属性 | CP OOP 章；Objects 参考 | p3 |
| [L15](notes/L15.md) | 面向对象 II：继承、MRO 与表示切换 | Week8 Inheritance 讲义 | p3 |
| [L16](notes/L16.md) | 树与字典：数据结构的组织与效率 | CP §2.4；Efficiency 讲义 | p3（trees/odict/minisql） |
| [L17](notes/L17.md) | 期中 2 复习 + 语言建模选读 | Practice Midterm 2；LLM 讲义 | 复盘 p3 |
| [L18](notes/L18.md) | 排序与效率精化：选择、插入、归并 | Week9 讲义；CP §1.7 | p3 |
| [L19](notes/L19.md) | Scheme 入门与计算器：语言的骨架 | CP §4.1；SICP §4.1 预览 | [p4_scheme](projects/p4_scheme/README.md) |
| [L20](notes/L20.md) | 写解释器 I：词法、语法分析与 eval/apply 循环 | CP §4.1.2-4.1.3 | p4（utils.py） |
| [L21](notes/L21.md) | 写解释器 II：环境、特殊形式与过程对象 | CP §4.2 | p4（scheme.py） |
| [L22](notes/L22.md) | 元循环求值、尾递归与宏 | CP §4.4；SICP §4.1/§5.2 | p4（--test 尾递归/宏） |
| [L23](notes/L23.md) | 流与惰性求值 | SICP §3.5 | p5_streams + p4 cons-stream |
| [L24](notes/L24.md) | SQL 与关系查询 | 官网 SQL primer；SQL Lab | p3（minisql.py）对照 |
| [L25](notes/L25.md) | 并发与多处理：线程、进程与 GIL | Concurrency 讲义 | [p6_concurrency](projects/p6_concurrency/README.md) |
| [L26](notes/L26.md) | 期末复习与总结：抽象的三个高度 | Practice Final | 全项目回归 |

- 文献与开源映射：[papers.md](papers.md)
- 项目总览（讲次→项目→知识点 + 快速回归命令）：[projects/README.md](projects/README.md)

## 五、考核与配套结构（fall2024）

| 类型 | 编号 → 主题 |
| --- | --- |
| Project 1 | Hog（骰子游戏：函数与随机性） |
| Project 2 | Penguins（数据抽象与地图绘制） |
| Project 3 | Comments（社交网络：OOP + 链表/树 + 解释器前置） |
| Project 4 | Scheme：用 Python 实现 Scheme 解释器（课程毕业项目） |
| Lab | Lab01 入门 → Lab06 OOP → Lab07 链表 → Lab08 可变树 → Lab09 Scheme（+SQL Lab） |
| HW | HW01–HW08（Python 基础 → 高阶 → 递归/复杂度 → OOP → 链表/树 → Scheme） |
| Disc | Disc01–Disc09（讨论课习题，含 Scheme、SQL 专集） |

## 六、教材全章节目录对照

### Composing Programs（官方教材，含中文译本）
- 第 1 章 为函数构造抽象：1.1 起步；1.2 编程元素；1.3 定义新函数；1.4 函数设计；1.5 控制流；1.6 高阶函数；1.7 递归函数
- 第 2 章 为数据构造抽象：2.1 引言；2.2 序列；2.3 复合数据（链表/树/对象与 OOP、消息传递）＋附录示例
- 解释器部分（第 4 讲章体系）：Scheme、计算器解释器、惰性流与宏
- 参考 SICP 原典章节：1 用过程抽象构造、2 用数据抽象构造、3 模块化对象与状态、4 元语言抽象

### 中译本
- 《计算机程序的构造和解释》（SICP 中译，MIT Press 授权版）——course 后半程（解释器/流/宏）逐章对照阅读。
