# CMU 17-803: Empirical Methods 实证研究方法（软件工程方向）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | CMU 17-803 Empirical Methods for Software Engineering（面向软工/HCI 实证研究的博士生方法课） |
| 学校 | Carnegie Mellon University（HCI Institute / Software Engineering Institute 方向） |
| 主讲 | Bogdan Vasilescu（开源软件与开发者生产力实证研究代表人物） |
| 教材 | 无统一出版教材（每节课前指定阅读材料：Creswell《Research Design》、Wohlin 等《Experimentation in Software Engineering》、Angrist & Pischke《Mostly Harmless Econometrics》、Cohen《Statistical Power Analysis》等章节组合） |
| csdiy 路径 | https://csdiy.wiki/软件工程/17803/ （页面更新 2024-04-14） |
| 最新期次 | csdiy 推荐 Spring 2024（课件 + 录像公开；另有 Fall 2022 / Spring 2021 / Fall 2018 版本） |
| 先修/语言/难度 | 面向博士生，无硬性先修但需一定计算机基础；分析语言不限（课程实际使用 R 与 Python）；难度 🌟🌟🌟；预计学时 100 小时 |
| 状态 | 骨架 |

## 为什么学

- 补上技术向课程共同的空白：**如何科学地评估一个工具/算法/流程到底有没有用**。6.031/CS169 教你怎么做，这门课教你怎么证明它更好。
- 方法谱系完整：定性与定量并举——访谈、观察、扎根理论与定性编码、问卷设计、档案数据（GitHub/Stack Overflow）挖掘、实验设计、统计建模、因果推断、社交网络分析、文本与序列分析。
- 由该领域一线研究者授课，示例大量来自真实的开源与开发者生产力研究（Vasilescu 的结对编程/性别与生产力/开发者流失等工作）。
- 强落地：学完能独立设计并复现一篇 EMSE/MSR/ICSE-SEIP 级别的实证研究，也具备批判阅读这类论文的能力。
- 对工程实践的回馈：学会区分"相关"与"因果"，避免被 A/B 测试、效能度量与工具宣传误导。

## 先修与知识联系

- 先修：概率与统计基础（CS70 / 6.042 级别）、一门脚本语言（Python 或 R）、基本 Git/仓库概念。
- 建议并行：机器学习方法课（CS229/CS189）——回归、分类、嵌入与主题模型在此课被当作分析工具而非研究对象；6.042J/统计课补假设检验与混合模型。
- 与前课关系：6.031（代码质量概念）与 CS169（敏捷流程与度量）提供"值得研究的问题"；算法课（6.046/CS170）提供"评估新算法的动机"。
- 输出方向：直接衔接 MSR / EMSE / ICSE-SEIP 方向的科研训练与论文写作（本课最后一单元即预注册、开放材料与传播）。
- 伦理与合规部分（IRB、GDPR、匿名化）与所有涉及真实用户数据的课程（Web 开发、数据库、AI）相互呼应：采集人类数据的研究都受此约束。

## 最新年份讲义章节目录（Spring 2024，按课程模块整理为 24 讲）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：什么是实证研究、研究问题与贡献的类型 | Creswell《Research Design》Ch.1；课程 syllabus |
| L2 | 研究设计与效度威胁：内部/外部/构念/结论效度 | Shadish, Cook & Campbell《Quasi-Experimentation》选章；Wohlin Ch.4 |
| L3 | 文献工作与批判性阅读：如何读完并拆解一篇 SE 论文 | 课堂拆解模板 + 指定的 2 篇 ICSE/EMSE 论文精读 |
| L4 | 系统与映射研究：检索策略、纳入排除、PRISMA | Kitchenham (2004)；Petersen 等 mapping study 指南 |
| L5 | 定性研究入门：观察、访谈类型与访谈提纲设计 | Seaman (1999)；Brickman & Chao 访谈与观察方法章节 |
| L6 | 扎根理论与定性编码：开放/主轴/选择性编码，代码手册 | Strauss & Corbin (1990) 选章；代码本示例 |
| L7 | 编码一致性与信度：编码者间一致性（Cohen's κ）、分歧处理 | Miles & Huberman 分析框架选章；课堂双人编码练习 |
| L8 | 问卷与调查设计：构念测量、量表、预测试与认知访谈 | Dillman/Smyth/Christian 调查方法设计章节 |
| L9 | 抽样与偏差：招募渠道、响应偏差、自选择与幸存者偏差 | Westlander (1993) 软件项目中的访谈研究；课堂复析一篇高引论文的抽样问题 |
| L10 | 描述统计与数据清洗：分布、缺失、异常值与可视化规范 | Wickham《R for Data Science》选章；课程讲义 |
| L11 | 假设检验基础：效应量、置信区间、p 值误用与多重比较 | Cohen (1988)；Ioannidis (2005) |
| L12 | 功效分析与样本量：G*Power 思路、最小可检测效应 | Wohlin Ch.4 实验有效性；Hult 等 SE 功效指南 |
| L13 | 线性模型 I：OLS、稳健标准误、模型诊断与交互项 | Fox & Weisberg《An R Companion to Applied Regression》选章 |
| L14 | 线性模型 II：逻辑回归与广义线性模型（计数/过离散） | Agresti《Categorical Data Analysis》选章；Zhou 等计数模型论文 |
| L15 | 混合效应模型：聚类、随机斜率、开发者/项目内相关 | Gelman & Hill《Data Analysis Using Regression and Multilevel Models》选章 |
| L16 | 档案数据与仓库挖掘 I：GitHub/Stack Overflow 数据获取（GH Archive、GHTorrent、BigQuery） | Gousios (2013)；Kalliamvakou 等 (2014/2016) |
| L17 | 档案数据与仓库挖掘 II：构念代理、度量定义与陷阱（生产力/质量/流失） | Bird et al. (2011) 代码所有权研究；课程度量定义讲义 |
| L18 | 相关 ≠ 因果：混杂、选择效应与因果图（DAG） | Hernán & Robins《Causal Inference》选章 |
| L19 | 因果推断方法：匹配/倾向得分、DID、工具变量、断点回归 | Angrist & Pischke (2009) 选章 |
| L20 | 准实验与田野实验：随机化单位、干预设计、预注册 | Wohlin 实验分类；OSF 预注册模板 |
| L21 | 社交网络分析：中心性、社区、同质性与时间网络 | Borgatti 等网络方法章节；Wasserman & Faust 选章 |
| L22 | 文本与序列分析：词频/主题模型/嵌入、过程与序列分析 | 课程 reading；GrIM/序列分析论文 |
| L23 | 研究者伦理：IRB/知情同意、隐私与匿名化、GDPR、AI 时代的数据使用 | CMU IRB 指南；SE 实证研究伦理与隐私论文（如 mining 数据的同意问题） |
| L24 | 可复现、写作与传播：开放材料/数据/代码、审稿应对、研究项目展示 | ACM 复现与 Artifact 徽章政策；ML/artifact evaluation 指南；学员提案 |

> 说明：17-803 各学期按"模块 + 讲次"推进，L16–L17（仓库挖掘）与 L18–L20（因果）可能互换顺序或合并；作业与期末项目未公开，本课的骨架笔记以**方法 + 复现练习**为主线组织。

## 课程资源（摘自 csdiy）

- 课程网站：Spring 2024 / Fall 2022 / Spring 2021 / Fall 2018
- 课程视频：Spring 2024、Fall 2022（公开录像）
- 课程教材：未公开统一教材，每节课前有指定阅读材料
- 课程作业：未公开（自学建议以"复现一篇论文 + 设计自己的研究提案"替代）
- 资源汇总：bvasiles/empirical-methods（GitHub，课程全部材料与示例）
