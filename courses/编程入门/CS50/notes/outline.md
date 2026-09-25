# Harvard CS50x（2025）— 笔记大纲（骨架，L0–L10）

## L0 Scratch
- 用块编程理解：变量、条件、循环、函数、事件。
- 抽象的第一个样本：把角色行为组合成"我的程序"。
- 与文本语言的映射关系：块 ↔ if/for/def。

## L1 C 语言基础
- 编译流水线：cpp→cc1→as→ld；`make` 的角色。
- `printf/scanf`、cs50.h 的 `get_int`；类型与格式符。
- 整数溢出与"计算机里的数是有界的"。
- 作业锚点：Mario 金字塔（嵌套循环）。

## L2 Arrays
- 数组与字符串（char 数组 + `\0`）；遍历模式。
- `const`、命令行参数 `argc/argv`。
- 浮点数误差与 cents 化整（Cash 的核心教训）。
- 函数封装与返回类型设计。

## L3 Algorithms
- 线性 vs 二分查找；O(n) 与 O(log n) 直觉（撕黄页演示）。
- 选择排序、冒泡排序：交换最小化视角；O(n²)。
- 运行时间记号：Ω、Θ、O；问题规模与资源（时间/空间/并行）。
- 作业锚点：跑通两套排序并解释不变式。

## L4 Memory
- 地址与指针：`&`、`*`；swap 的指针版本。
- `malloc/free`、栈与堆、内存泄漏与悬挂指针。
- 结构体与指针配合；`typedef`。
- 作业锚点：Filter（BMP 图像字节级处理）。

## L5 Data Structures
- 数组 → 链表：动态增长的代价与指针拼接。
- 栈/队列、哈希表（桶与冲突）、树（BST 遍历）、Trie、图。
- 每种结构的读写复杂度对照表。

## L6 Python
- 把 L1–L4 的 C 程序逐个"翻译"为 Python：f-string、切片、dict/set。
- 异常、`main()` 惯用法、标准库。
- 作业锚点：用 Python 重写 DNA 匹配。

## L7 SQL
- 表/主键/外键与关系模型；`SELECT/JOIN/GROUP BY`。
- SQLite 命令行与 Python `sqlite3` 联动。
- 视图、触发器、索引概念初识。

## L8 HTML, CSS, JavaScript
- HTML 结构 → CSS 样式 → JS 行为的三层分离。
- DOM 操作与事件；fetch 调用 API。
- 用 Flask 模板渲染动态页面的伏笔。

## L9 Flask
- 路由、模板、会话与登录（Jinja2 + SQL 集成）。
- ORM（Flask SQL）与表单校验（WTForms）。
- 作业锚点：Finance（股票买卖全栈应用）。

## L10 The End
- 全课知识地图复盘：从 0/1 到全栈。
- CS 学习路线与后续课程（CS50P/W/AI）选择。
- Final Project：自选主题完成端到端小系统。
