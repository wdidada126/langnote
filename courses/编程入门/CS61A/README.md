# UCB CS61A：计算机程序的构造和解释（Structure and Interpretation of Computer Programs）

> **【CORE 核心课程】** 本文件为完整版 README（含全章节目录）。`notes/`、`papers/`、`projects/` 目录已建为空，正文笔记由后续专人完成。

## 一、课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 / 课程号 | Structure and Interpretation of Computer Programs / CS 61A（UCB EECS 入门核心课，CS61 系列第一课） |
| 学校 | UC Berkeley |
| 主讲 | Josh Hug（近数学期；历期含 Paul Hilfinger 等） |
| 教材 | 主教材 *Composing Programs*（官方电子书，作者 Chris Pritchard 等）；**中文译本**（composingprograms 中文翻译版）；进阶参考 SICP（Abelson & Sussman，MIT 6.001 原教材，有中译本《计算机程序的构造和解释》） |
| csdiy 路径 | `编程入门/Python/CS61A`（csdiy.wiki） |
| 最新期次 | 课程页面备份列 **spring2026**；作业与视频以 **fall2024** 为准（csdiy 推荐）；另备份 spring2022/fall2022/fall2020 |
| 状态 | CORE 骨架：README 完成，正文待专人填充 |

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

## 四、最新年份（fall2024，学期制 13 周）讲义章节目录

> 讲次编号按每周 2 讲排列（L27 前后为复习/期末）。标题为中文骨架译名，精确表述以学期站 syllabus 为准（spring2026 为最新备份版，主题结构一致）。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论：什么是 CS；程序的构造与解释 | CP 第 1 章 §1.1；SICP §1.1 前言 |
| L2 | 编程元素：表达式、求值与环境图 | CP §1.2（Elements of Programming） |
| L3 | 函数抽象与高阶函数 I（函数作参数） | CP §1.3–1.4 |
| L4 | 高阶函数 II（函数作返回值、currying、装饰器） | CP §1.6 |
| L5 | 递归函数与调试 | CP §1.7；调试指南（官网 Articles） |
| L6 | 树递归与增长阶（Order of Growth） | CP §1.7 树递归节；效率参考表 |
| L7 | 序列与迭代抽象（list/tuple/range） | CP §2.2 Sequences；内置类型参考 |
| L8 | 期中复习与练习（Midterm 1 review） | 历年 midterm 卷（官网 practice exams） |
| L9 | 可变数据与链表（mutable data, linked lists） | CP §2.2/2.3 可变部分；P3 材料 |
| L10 | 面向对象 I：类、实例、属性 | CP OOP 章（class 一节）；Objects 参考 |
| L11 | 面向对象 II：继承与表示 | 官网 Week8 讲义（Inheritance） |
| L12 | 链表、树与调度（links / trees & dispatch） | Week8–9 讲义；Linked Lists 文章 |
| L13 | 效率、分解与数据实例（efficiency & decomposition） | Week9 讲义 |
| L14 | 语言建模选读 + Midterm 2 复习 | Week10 讲义（LLM 选读） |
| L15 | Scheme 语言入门与计算器（Calculator） | Week11 讲义；CP Ch.4（Scheme） |
| L16 | 写解释器 I：evaluate/apply 循环 | CP Ch.4；P4 骨架说明 |
| L17 | 写解释器 II：环境与特殊形式 | CP Ch.4 续 |
| L18 | 元循环求值与语法抽象（Macros） | Week13 讲义（Macros）；CP Ch.4.4 |
| L19 | 流与惰性求值（streams, lazy evaluation） | CP Streams 章；SICP §3.5 |
| L20 | SQL 与关系查询 | 官网 SQL 资源；SQL Lab/Disc |
| L21 | 期末复习与总结 | review 讲义 + practice final |

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
