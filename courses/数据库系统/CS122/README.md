# Caltech CS122 — Database System Implementation（数据库系统实现）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS122: Database System Implementation |
| 学校 | California Institute of Technology（加州理工学院） |
| 主讲 | Caltech CMS/EE 教学团队（以课程官网为准；公开版为 2019 冬季学期） |
| 教材 | 无；参照 Silberschatz/Graefe 优化器教材与课程讲义 |
| csdiy 路径 | 数据库系统/CS122 |
| 最新期次 | Spring 2019 公开版（gitlab.caltech.edu/cs122-19wi） |
| 状态 | 骨架（notes / papers / projects 待后续填充） |

## 为什么学

- 与 15-445 的差异化定位（csdiy 原话）：15-445 不提供 SQL 层，而 **CS122 的 Lab 侧重 SQL 层的实现**——查询优化器全模块：SQL 解析、Translate、Join 实现、统计信息与代价估计、子查询、Agg/Group By，外加 B+ 树与 WAL 实验。
- 基于教学数据库 **NanoDB**（Java），代码量适中、结构清晰，适合在学完 15-445 之后专攻查询优化方向的同学。
- csdiy 难度 🌟🌟🌟🌟🌟、约 150 学时：7 Assignments + 2 Challenges，从「能跑」到「跑得快」的完整训练。

## 先修与知识联系

- 先修要求：无硬性（实际建议先学 15-445 或 CS186 建立存储/索引/事务基础）；语言 Java（推荐 IDEA + Maven 构建，注意日志配置）。
- 知识联系：承接 15-445 的内核层（buffer pool/B+树），主攻执行与优化层；与 CS346 RedBase（C++）目标相似、语言/规模不同；优化器理论对应 Selinger/Graefe 论文线。

## 讲义章节目录（按课程主题与 Assignment 映射整理）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 数据库系统总览与 NanoDB 架构导引 | 课程讲义 Ch1 |
| L02 | 存储与页管理：磁盘页、记录格式、堆表 | 讲义 + NanoDB Storage 源码 |
| L03 | Buffer Pool 管理与 pin/unpin | 讲义；对应 A1 任务 |
| L04 | DML 执行路径：insert/delete/update（A1：delete/update 支持、性能提升防膨胀） | Assignment 1 Handout |
| L05 | SQL 解析与翻译：Parse → Translate | 讲义 + Parser 代码 |
| L06 | 计划生成：从代数到可执行计划（A2：简单计划生成器） | Assignment 2 Handout |
| L07 | Join 算法与实现：Nested-loop、inner/outer join（A2） | Assignment 2 + 单测要求 |
| L08 | 统计信息收集（A3：表统计） | Assignment 3 Handout |
| L09 | 代价模型：计划节点成本计算（A3） | Assignment 3 |
| L10 | 谓词选择率估计与元组统计传播（A3） | Assignment 3 |
| L11 | B+ 树索引 | 讲义；索引实验 |
| L12 | 聚合与 GROUP BY 实现 | 讲义（Agg/Group By 实验） |
| L13 | 子查询实现与去相关 | 讲义（子查询实验） |
| L14 | 事务与 WAL 日志恢复 | 讲义；WAL 实验 |
| L15 | Challenges：优化器进阶（枚举/更好的代价） | Challenge 1–2 Handout |

## 资源

- 课程网站：http://courses.cms.caltech.edu/cs122/ ；课程代码：https://gitlab.caltech.edu/cs122-19wi
- 作业：7 Assignments + 2 Challenges（A1–A3 功能详述见 csdiy 页/本 README 上表）
- 教材：无（csdiy 标注）
