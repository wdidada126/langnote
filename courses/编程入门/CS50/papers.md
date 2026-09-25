# Harvard CS50x — 论文与工程实践对照（骨架）

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Computing Machinery and Intelligence（Turing） | 1950 | 提出计算与智能的根本问题，导论课的精神原点 | L0/L10 |
| The C Programming Language（Ritchie, CACM） | 1974 | C 语言官方首述，L1–L5 全部语法与库的出处 | L1–L4 |
| Algorithm 264: Heapsort（Williams） | 1964 | 堆结构经典算法，支撑排序与数据结构周 | L3/L5 |
| Algorithm 63: Partition（Hoare） | 1962 | 划分算法，连接排序与选择问题的桥梁 | L3 |
| A Relational Model of Data for Large Shared Data Banks（Codd） | 1970 | 关系模型奠基，SQL 周的理论来源 | L7 |

> 注：本表骨架版保留 5 条最核心文献（Turing/Ritchie/Williams/Hoare/Codd），正式笔记阶段可按周扩充。

## 二、近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| CS50 Teaches Computing（CS50 团队自身教育研究系列, SIGCSE） | 2021–2024 | 大规模入门课的反转课堂与自动评测实证研究 | 全课 |
| AlphaCode: Competitive Programming at Expert Level | 2022 | LLM 解竞赛编程题，重定义入门编程教育的"何以为证" | L3/L6 |
| SQL-to-Text / Spider 2.0 基准（NL2SQL 演进） | 2023–2024 | 自然语言查询前沿，对照 L7 手写 SQL 的价值 | L7 |
| Web 安全视角下的 Flask 应用漏洞实证研究 | 2022 | 入门全栈框架常见漏洞模式（CSRF/注入） | L9 |

## 三、知识点在开源项目中的应用

| 课程知识点 | 开源项目案例 | 说明 |
| --- | --- | --- |
| C 编译与 make | GNU coreutils、git 源码 | L1 编译流水线在真实小项目中的形态 |
| 指针/内存 | Valgrind、gdb | L4 排障标准工具链 |
| 数据结构库 | glibc（qsort/hsearch）、redis（ziplist/skiplist） | Redis 源码即 L5 结构的工业实现 |
| 排序与二分 | CPython `list.sort`（Timsort）、std::algorithm | L3 算法的生产级版本 |
| SQL/关系 | SQLite（驱动本课）、Postgres | L7 可直接读 SQLite 文档级案例 |
| Flask 全栈 | 本课 PSET9 Finance 本身即模板应用；对照 realpython 示例 | L8–L9 端到端 |
| CS50 工具链 | cs50.vscode 扩展、submit50、autograder（均在 CS50 开源仓库） | 课程基础设施即开源项目 |
