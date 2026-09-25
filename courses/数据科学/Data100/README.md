# UCB Data100 - Principles and Techniques of Data Science

## 1. 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Data C100/Data 100: Principles and Techniques of Data Science（UC Berkeley） |
| 所属学校 | University of California, Berkeley |
| 主讲教师 | Joseph Gonzalez、Ion Stoica、Sofia Vergara 等（数据科学教育倡议团队） |
| 课程教材 | Introduction to Data Science（官方在线教材 textbook.ds100.org，现迁移至 learningds.org） |
| csdiy 路径 | `数据科学/Data100`（csdiy.wiki，页面日期 2023-04-24） |
| 最新期次 | 每学期滚动开课（ds100.org 列当期 Summer/Fall 班；教材 2024-2025 修订版） |
| 状态 | 骨架 |
| 先修要求 | Data 8（统计）、CS 61A、线性代数 |
| 难度/学时 | 🌟🌟🌟 / 约 80 小时；编程作业 + Hacker Questions + 期末大项目 |
| 课程网站 | https://ds100.org/ |

## 2. 为什么学

- 伯克利数据科学学位核心入门课：从 Data8/CS61A 通向 188/189/214 等高级课的桥梁。
- 覆盖数据科学完整生命周期：数据获取/清洗 → 特征提取 → 可视化与 EDA → 建模（回归/分类/ML）→ 规模化推理。
- 工具栈即业界标准：Pandas、NumPy、Matplotlib、SQL、Seaborn/Plotly、Scikit-learn，作业全部实做。
- 以"丰富有趣的编程作业 + Hacker Questions（真实开放数据题）"著称，做完即有一手项目经验。

## 3. 先修与知识联系

- **前置**：Data 8（概率与统计推断）、CS 61A（Python 与抽象）、线代。
- **对照**：CS186（数据库 SQL 深度）、15-445（引擎原理）、6.041/概率课。
- **下游**：CS189/CS289（机器学习）、CS214（系统）、CS188（AI）、统计推断进阶。
- **横向**：数据可视化联系前端（D3/Observable）；规模化工具联系 Spark/DuckDB 生态。

## 4. 讲义章节目录（官方教材 learningds.org 21 章版；课程四模块归纳）

> 教材各章即阅读材料；课程排期以当期 ds100.org syllabus 为准。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| Ch1 | The Data Science Lifecycle（数据科学生命周期） | 教材 Ch1 |
| Ch2 | Questions and Data Scope（问题定义与数据范围） | Ch2 |
| Ch3 | Simulation and Data Design（模拟与数据设计） | Ch3 |
| Ch4 | Modeling with Summary Statistics（摘要统计建模） | Ch4 |
| Ch5 | Case Study: Why Is My Bus Always Late?（案例：公交晚点） | Ch5 |
| Ch6 | Working with Dataframes Using pandas | Ch6 |
| Ch7 | Working with Relations Using SQL | Ch7 |
| Ch8 | Wrangling Files（文件解析与摄取） | Ch8 |
| Ch9 | Wrangling Dataframes（清洗与整形） | Ch9 |
| Ch10 | Exploratory Data Analysis | Ch10 |
| Ch11 | Data Visualization | Ch11 |
| Ch12 | Case Study: How Accurate Are Air Quality Measurements? | Ch12 |
| Ch13 | Working with Text（文本处理与特征） | Ch13 |
| Ch14 | Data Exchange（数据序列化/HTTP/JSON） | Ch14 |
| Ch15 | Linear Models（线性模型） | Ch15 |
| Ch16 | Model Selection（模型选择与交叉验证） | Ch16 |
| Ch17 | Theory for Inference and Prediction（推断理论） | Ch17 |
| Ch18 | Case Study: How to Weigh a Donkey | Ch18 |
| Ch19 | Classification（分类） | Ch19 |
| Ch20 | Numerical Optimization（数值优化） | Ch20 |
| Ch21 | Case Study: Detecting Fake News（期末案例） | Ch21 |

### 课程模块视角

模块一 生命周期与数据工程（Ch1-5, Ch8, Ch14）→ 模块二 查询与整形（Ch6-7, Ch9）→ 模块三 EDA 与可视化（Ch10-13）→ 模块四 建模/ML/规模化（Ch15-21）。作业：每模块 lab + homework + 期末团队项目（真实数据集端到端）。

## 5. 笔记进度

- [x] notes/outline.md ｜ [ ] 逐章全文 ｜ [x] papers.md ｜ [ ] projects/ 代码
