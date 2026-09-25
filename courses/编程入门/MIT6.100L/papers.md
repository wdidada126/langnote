# MIT 6.100L — 论文与工程实践对照（骨架）

## 一、经典论文 / 奠基文献

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Introductory Programming（Dijkstra, CACM 图灵演讲） | 1973 | 论证编程应作为一门科学来教，入门课教学法源头 | L1 |
| Go To Statement Considered Harmful（Dijkstra） | 1968 | 结构化控制流宣言，对应只教分支/循环的课程设计 | L4–L5 |
| The Python Tutorial（van Rossum，一手文献） | 1995 起 | 语言官方叙述，L2–L12 语法的权威口径 | L2–L12 |
| Program Development by Stepwise Refinement（Wirth, 图灵演讲） | 1971 | 逐步求精方法论，对应 Labs 的迭代实现路径 | L8/L14 |
| Introduction to Algorithms（CLRS，经典教材视同一手资料） | 1990 | 排序/搜索/复杂度的标准语言与证明风格 | L15–L17 |
| Why Programs Fail（Zeller，专著视同一手资料） | 2009 | 科学调试法：观察-假设-最小化复现的完整流程 | L14 |

## 二、近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| To Type or Not to Type: Quantifying Detached Type Annotations in Python | 2021 | Python 类型注解的实证收益与成本 | L19–L21 |
| Studying Students' Misconceptions on Aliasing/Mutability（SIGCSE 系列实证） | 2021–2024 | 入门学习者对别名与可变性错误概念的实证研究 | L10–L11 |
| AI Pair Programming in Introductory CS（LLM 助教实验） | 2023–2024 | 大模型作为入门课辅导助手的可行性证据 | 全课 |
| Empirical Benchmarks of Python Sorting Implementations | 2022 | Timsort 与手写排序的实测复杂度对照 | L16–L17 |

## 三、知识点在开源项目中的应用

| 课程知识点 | 开源项目案例 | 说明 |
| --- | --- | --- |
| 求值与替换模型 | CPython `dis` 模块 | 反汇编观察字节码，验证 L2–L3 心智模型 |
| aliasing / 可变性 | NumPy 视图（view vs copy） | 可变性别名陷阱的高性能版本 |
| 字典 / 集合 | CPython dict、collections.Counter | 哈希表应用一线案例 |
| 测试与调试 | pytest、coverage.py | L14 工具链标准件 |
| 排序与复杂度 | Python `sorted`（Timsort） | 归并 + 插入混合的工程实现 |
| OOP | dataclasses / attrs | 以装饰器简化 L19–L20 样板代码 |
| 绘图与模拟 | matplotlib、networkx 示例集 | L22–L23 的直接应用场 |
