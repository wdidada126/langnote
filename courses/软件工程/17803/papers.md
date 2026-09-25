# 17-803 参考文献与开源应用（骨架）

> 关联讲次对应 README/outline 的 L1–L24。文献分三类：方法学源头、软工实证代表作、可复现/工具性论文。

## 经典论文 / 文献

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Qualitative Methods in Empirical Studies of Software Engineering (C. Seaman, IEEE TSE) | 1999 | 把定性方法（访谈/编码/扎根）引入软工实证的入门必读 | L5–L7 |
| Procedures for Performing Systematic Reviews (B. Kitchenham) | 2004 | 软工系统综述的操作规程与 PRISMA 式流程 | L4 |
| Research Design: Qualitative, Quantitative, and Mixed Methods Approaches (J. W. Creswell) [专著] | 2003+ | 三类研究设计的统一框架，课程主线教材 | L1–L2, L20 |
| Basics of Qualitative Research: Grounded Theory Procedures and Techniques (Strauss & Corbin) [专著] | 1990 | 三级编码与理论饱和的操作性定义 | L6 |
| The Central Role of the Propensity Score in Observational Studies for Causal Effects (Rosenbaum & Rubin) | 1983 | 倾向得分匹配，观察研究因果推断的基石 | L19 |
| Statistical Power Analysis for the Behavioral Sciences (J. Cohen) [专著] | 1988 | 效应量与功效分析的标准化工具箱 | L11–L12 |
| Why Most Published Research Findings Are False (J. Ioannidis) | 2005 | 系统说明偏差、功效不足与灵活分析如何制造假阳性 | L11, L24 |
| Experimentation in Software Engineering (Wohlin, Runeson, Höst, Jorgensen 等) [专著] | 2000/2012 | 把实验设计、效度威胁与度量定义移植到软工场景 | L2, L12, L20 |
| The Psychology of Computer Programming (G. M. Weinberg) [专著] | 1971 | 首批把"人"的因素作为实证对象的研究，程序员行为测量学的起点 | L5, L20 |
| Internet, Mail, and Mixed-Mode Surveys: The Total Design Method (Dillman, Smyth & Christian) [专著] | 1978/2014 | 调查设计、跟进与响应率提升的总设计法 | L8–L9 |
| Mostly Harmless Econometrics (Angrist & Pischke) [专著] | 2009 | 现代因果推断四件套（IV/DID/RDD/匹配）的实操教材 | L18–L19 |
| The Goal/Question/Metric Paradigm (V. Basili 等) | 1994 | 把"你想度量什么"形式化为目标-问题-指标三层 | L10, L17 |
| The GHTorrent Dataset and Tool Suite (G. Gousios) | 2013 | 结构化抓取 GitHub 元数据的公开数据集与工具 | L16 |
| The Promises and Perils of Mining GitHub (Kalliamvakou et al., MSR) | 2014 | 系统指出 GitHub 数据的偏差、缺失与可推广性问题 | L16–L17 |
| The Promises and Perils of Mining Git (Kalliamvakou et al., MSR) | 2016 | Git 本地历史挖掘（含多仓库镜像数据集）的方法与陷阱 | L16–L17 |
| Don't Touch My Code! Examining the Effects of Ownership on Software (Bird et al., ESEC/FSE) | 2011 | 用大规模仓库实证"代码所有权"与缺陷率的关系 | L17, L19 |
| Motivation of Software Developers in Open Source Projects: An Internet-Based Survey of Contributors (Hertel, Niederleber & Herrmann, J. Economic Psychology) | 2003 | 开源参与者动机的经典大规模问卷研究 | L8–L9 |
| A Controlled Experiment for Test-Driven Development: An Impact on Software Quality (George & Williams, IEEE TSE) | 2004 | 现场对照实验评估 TDD 对质量与工时的影响及其局限 | L20 |
| Static Analysis Predictors for Software Defects (Nagappan & Ball, IEEE TSE) | 2005 | 用代码/变更度量做缺陷预测（Vista/Windows 数据），挖掘-预测研究典范 | L13–L15, L17 |

## 近 5 年文献（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The Promise and Perils of Mining Large-Scale Code Data in the LLM Era（数据许可、去标识与再识别讨论系列） | 2021–2024 | 大规模代码语料带来新的隐私/同意/合规问题，重塑 L23 的伦理边界 | L16, L23 |
| Using Large Language Models for Qualitative Coding and Survey Analysis | 2023–2025 | LLM 可做初步编码，但需人工抽检与一致性报告，方法学结论正在收敛 | L6–L7, L22 |
| Registered Reports and Reproducibility Packages in SE Journals（EMSE/TOSEM 政策与实践） | 2021–2024 | 把"分析计划提前固定"制度化，直接对抗结果挑选 | L11–L12, L20, L24 |
| Developer Productivity Measurement Controversies（AI 编码助手的现场实验与批评） | 2022–2024 | 同一问题的多份测量给出冲突结果，示范如何审度效度威胁 | L10–L12, L17 |
| Temporal/Exponential Random Graph Models for Collaboration Networks（软件协作网络新进展） | 2021–2024 | 用时间网络模型区分"同质选择"与"社会影响" | L21 |
| Process Mining for Software Engineering（事件日志与开发流程挖掘） | 2021–2024 | 把过程挖掘引入提交/评审/CI 流程，序列分析的现代形态 | L22 |
| Causal Inference with Observational Software Data（DID/合成控制/事件研究在 SE 中的应用） | 2021–2024 | 因果工具箱进入软工论文标配，识别策略写作成为评审重点 | L18–L20 |
| Measuring Software Quality with Embeddings and Pretrained Models（代码表示用于缺陷/可维护性预测） | 2021–2024 | 用 CodeBERT/大模型提升预测力，同时带来泄漏与过拟合新风险 | L14–L15, L22 |
| Empirical Studies of CI/CD, Code Review Automation and Bot Agents（含 Copilot/ChatGPT 使用研究） | 2021–2025 | 混合方法研究"人机协同"如何改变评审、测试与交付实践 | L20–L22 |
| Data/Code Availability and Artifact Evaluation Outcomes in SE Conferences（AE 委员会统计与改进） | 2021–2025 | 用元研究量化"开放材料"的真实采纳率与效果 | L24 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 系统综述与筛选（L4） | RevMan、ASReview（主动学习筛选）、abm/RevSess 等开源筛选工具 | 主动学习辅助文献筛选、PRISMA 图自动生成 |
| 定性编码（L5–L7） | Taguette、QualCoder、RQDA（R） | 代码本、多人编码与 κ 一致性计算 |
| 问卷与调查（L8–L9） | LimeSurvey、SurveyJS、Qualtrics 开源替代（Formbricks） | 随机化题序、跳转逻辑与响应率跟踪 |
| 描述统计与清洗（L10） | pandas / polars、R tidyverse、Great Expectations | 缺失/异常检测与数据契约校验 |
| 假设检验与功效（L11–L12） | R `pwr`/`simr`、Python `statsmodels`（TTestPower）、G*Power（免费） | 计划样本量与模拟式功效分析 |
| 回归与混合模型（L13–L15） | R `lme4`/`brms`/`fixest`、Python `statsmodels` MixedLM、`pymer4` | 随机斜率、稳健标准误与模型诊断绘图 |
| GitHub 数据获取（L16） | GHTorrent、GH Archive、`gh` CLI、PyGithub、Software Heritage、GitHub BigQuery 公开数据集 | 事件流/关系表抓取、身份归并（SortingHat） |
| 开发者度量与工程分析（L17） | Apache DevLake（CHAI）、GrimoireLab（perceval/elastic） | 从提交/PR/issue 计算周期时间、评审时长等指标 |
| 因果推断（L18–L20） | R `MatchIt`/`CausalImpact`、Python `econml`/`DoWhy`/`causal-learn`、`tidytreatment` | 倾向匹配、DID、合成控制与 DAG 建模 |
| 社交网络分析（L21） | NetworkX、igraph、Gephi、statnet/`ergm`（R）、Snijders 时间网络 | 中心性、社区发现与网络显著性置换检验 |
| 文本与序列分析（L22） | scikit-learn/gensim（LDA）、BERTopic、HuggingFace 代码模型、PM4Py（过程挖掘）、TraMineR | 主题/嵌入/序列对齐与流程挖掘 |
| 伦理与合规（L23） | OSF（预注册/伦理材料）、anonymize/`presidio`（PII 脱敏）、Dataverse 数据分级许可 | 知情同意模板留存、去标识与访问控制 |
| 可复现与传播（L24） | OSF/Zenodo（DOI）、ReproZip/Docker/renv/uv lockfiles、SEART/ACM Artifact Review Badges | 一键复现环境与数据/代码/材料三开放 |
