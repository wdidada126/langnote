# Stanford CS346 — Database System Implementation（数据库系统实现 · RedBase）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS346: Database System Implementation |
| 学校 | Stanford University |
| 主讲 | Stanford 教学团队（公开版为 2015 春季；以课程官网为准） |
| 教材 | 无；参照 Garcia-Molina 等《Database Systems: The Complete Book》及课程讲义 |
| csdiy 路径 | 数据库系统/CS346 |
| 最新期次 | 2015 春季公开版（web.stanford.edu/class/cs346/2015） |
| 状态 | 骨架（notes / papers / projects 待后续填充） |

## 为什么学

- 核心项目 **RedBase**：一个结构高度良好的简易关系型数据库系统，整个项目天然划分为 4 个功能组件 + 1 个扩展（同时就是 4 个需要完善的 lab）——代码量不多，可以按需精读和扩展，非常适合作为「第二次造数据库」的载体。
- csdiy 定位：适合在学完 CMU 15-445 之后继续深入数据库其他组件（记录管理、系统目录/DDL、自研查询语言）；纯 C++ 编写，还能顺便练现代 C++。
- 与 CS122 的取舍：CS346 更小而完整（含 DDL/元数据管理/命令行），CS122 更侧重查询优化器。

## 先修与知识联系

- 先修要求：无硬性（建议先修 15-445/CS186 其一）；语言 C++；难度 🌟🌟🌟🌟🌟；预计学时 150 小时。
- 知识联系：RedBase 的四组件与 15-445 Project 1–4 一一呼应（存储/B+ 树/执行/系统层），但要求你亲手补上 445 有意略去的 SQL/DDL 壳。

## 讲义章节目录（按 RedBase 组件与主题整理）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 课程导论与 RedBase 架构总览 | 课程讲义 + redbase 源码结构 |
| L02 | 记录管理组件（Record Management）：记录格式、RID | Project 1 Handout |
| L03 | 页与表空间管理：paged file、DB 文件布局 | Project 1 Handout |
| L04 | B+ 树索引组件（Index）：插入/删除/游标 | Project 2 Handout |
| L05 | 索引与记录层联动：二级索引、聚簇索引 | Project 2 Handout |
| L06 | 系统管理组件：DDL 语句解析与执行 | Project 3 Handout |
| L07 | 命令行工具与数据加载命令 | Project 3 Handout |
| L08 | 元数据管理（catalog/schema 持久化） | Project 3 Handout |
| L09 | 查询语言组件：RQL 设计 | Project 4 Handout |
| L10 | RQL select/insert/delete/update 实现 | Project 4 Handout |
| L11 | 表达式求值与谓词过滤 | Project 4 Handout |
| L12 | 扩展专题导引：Blob 类型 | Extension 资料 |
| L13 | 扩展专题导引：网络模块 / 连接算法 | Extension 资料 |
| L14 | 扩展专题导引：CBO 优化器 / OLAP / 事务 | Extension 资料 |
| L15 | 总结：从 RedBase 看真实 DBMS 的差距 | Architecture of a DB System 论文 |

## 资源

- 课程网站：https://web.stanford.edu/class/cs346/2015/ ；课程代码：https://github.com/junkumar/redbase.git
- 作业：4 Projects + 1 Extension（教材：无，csdiy 标注）
