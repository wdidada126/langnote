# CMU 15-799 — Special Topics in Database Systems（数据库专题）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 15-799: Special Topics in Database Systems（Spring 2022 期主题：Self-Driving Database Management Systems） |
| 学校 | Carnegie Mellon University |
| 主讲 | Andy Pavlo（CMU Database Group；讲座形式） |
| 教材 | 无；每讲以课程指定论文为主（官方页面提供 paper list） |
| csdiy 路径 | 数据库系统/15799 |
| 最新期次 | Spring 2022（历史上仅开两次：Fall 2013 与 Spring 2022） |
| 状态 | 骨架（notes / papers / projects 待后续填充） |

## 为什么学

- 数据库前沿专题课：Fall 2013 讨论 Streaming、Graph DB、NVM 等；Spring 2022 聚焦 **Self-Driving DBMS（自治数据库）**，均配套论文清单。
- csdiy 定位：讲座形式、编程任务较少——对一般同学是开拓视野的最佳材料，对专精数据库的同学是通向 15-721（主存数据库）与工业前沿（自治调优、NewSQL）的桥。
- 任务真实且有工业感：任务一基于 PostgreSQL 手动性能调优；任务二基于 NoisePage Pilot 改进 Self-Driving DBMS（不限特性）。

## 先修与知识联系

- 先修：CMU 15-445（骨架）；语言 C++（NoisePage 源码阅读）；难度 🌟🌟🌟；预计学时 80 小时。
- 知识联系：15-445 内核知识 → 本课自治调优/预测主题；PostgreSQL 调优任务反向巩固 445 的索引/规划器章节；与 15-721（主存数据库）构成 CMU DB 进阶双课。

## 讲义章节目录（Spring 2022 主题骨架；具体论文与周次以官方 page 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 导论：什么是 Self-Driving DBMS 与设计目标 | Pavlo & Curry, *Self-Driving Database Management Systems* (IEEE Data Eng. Bull., 2017) |
| L02 | NoisePage/Pilot 架构巡礼 | CMU DB Group NoisePage 源码与设计文档 |
| L03 | 负载预测 I：时序方法 | 课程论文（workload forecasting 系列） |
| L04 | 负载预测 II：异常检测与分类 | 课程论文（workload classification） |
| L05 | 自动物理设计：索引选择与删除 | Chaudhuri et al., *AutoAdmin* (VLDB 2018) 等 |
| L06 | 自动查询优化与自适应执行 | 课程论文（adaptive query execution 系列） |
| L07 | 参数调优：从控制论到机器学习 | Van Aken et al., *OtterTune* (SIGMOD 2017) |
| L08 | 结构调优：schema/统计的自动演化 | 课程论文 |
| L09 | 调试与可观测性：DBMS 自我诊断 | Garrott? 以课程 paper list 为准（debugging 主题） |
| L10 | 机器学习方法在自治 DB 中的边界 | Hilprecht et al., *What Goes Together Comes Together* (ICDE 2020) 等 |
| L11 | 云与多租户场景下的自治 | 课程论文（serverless/multi-tenant tuning） |
| L12 | PostgreSQL 调优实践工作坊（对应任务一） | PostgreSQL 手册 + pg_stat 文档 |
| L13 | Pilot 改进方案评审（对应任务二） | NoisePage Pilot 源码 |
| L14 | 前沿回顾与结课 | 自选近两年论文 |

### 附：Fall 2013 期主题（对照阅读）

| 主题 | 说明 |
| --- | --- |
| Streaming / Graph DB / NVM / 概率数据库 /  crowdsourcing 查询 | 每主题若干论文讨论（课程页面留存） |

## 资源

- 课程主页：CMU 15-799 Special Topics in Database Systems / Special Topics: Self-Driving Database Management Systems（两个官方页面，见 csdiy 链接）
- 课程视频：暂无；作业：2 Projects + 1 Group Project
- 代码：CMU Database Group/noisepage（GitHub）
