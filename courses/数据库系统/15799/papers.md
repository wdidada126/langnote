# 15-799 论文与应用清单（papers.md）

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Self-Driving Database Management Systems (Pavlo & Curry) | 2017 | 自治 DBMS 的纲领性综述，全课总纲 | L01 |
| Automatic Database Management System Tuning Through Large-scale Machine Learning (Van Aken et al., OtterTune) | 2017 | DBMS 参数调优的代表系统 | L07 |
| AutoAdmin: Self-Tuning Index Management in the Cloud (Chaudhuri et al.) | 2018 | 物理索引设计自动演化的工业级框架 | L05 |
| Spanner: Google's Globally-Distributed Database (Corbett et al.) | 2012 | NewSQL 分布式数据库标杆，自治决策要服务的对象 | L11 |
| Pregel: A System for Large-Scale Graph Processing (Malewicz et al.) | 2010 | F2013 期 Graph DB 主题核心论文 | F2013 对照 |
| PowerGraph: Distributed Graph-Parallel Computation on Natural Graphs (Gonzalez et al.) | 2011 | 幂律图上的 GAS 编程模型 | F2013 对照 |
| MillWheel: Fault-Tolerant Stream Processing (Akidau et al.) | 2013 | F2013 期 Streaming 主题代表作 | F2013 对照 |
| The Log-Structured Merge-Tree (O'Neil et al.) | 1996 | LSM：写优化存储结构，自治调优常动的「旋钮」之一 | L05 |
| Architecture of a Database System (Hellerstein et al.) | 2007 | 全栈架构视角，定位自治层可干预的所有部件 | L01 |

> 校正说明：作者署名以正式出版版本为准，填笔记时逐条核对。

## 近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Bao: Making Learned Query Optimization Practical (Marcus, Papaemmanouil) | 2021 | 用提示集让学习型优化器可落地、可回退 | L06/L10 |
| Lero: A Learning-to-Rank Query Optimizer (Zhu et al.) | 2023 | 免训练数据依赖的计划排序，规避基数估计误差 | L06/L10 |
| Automated Reasoning at AWS (Narasimhan et al., CIDR) | 2021 | 云数据库策略与运维正确性的形式化验证 | L09/L11 |
| What Goes Together comes Together: Automatic Physical Design Selection in Cloud Databases (Hilprecht et al.) 及后续评测 | 2020–2022 | 联合索引/分区/物化视图的自治物理设计与失败模式分析 | L05/L07/L10 |
| 面向 LLM 的数据库运维辅助 (Database-Tuning-as-a-Service / DB-GPT 类工作) | 2023–2024 | 大模型进入调优回路：自然语言→诊断→动作 | L14 |

## 知识点在开源项目中的应用

| 知识点 | 开源项目 | 说明 |
| --- | --- | --- |
| Self-Driving 全栈 | CMUDB/noisepage（Pilot 子系统） | 本课官方实验载体 |
| 手动调优观测面 | PostgreSQL（pg_stat_*, EXPLAIN, auto_explain） | 任务一平台 |
| 云自治对照 | AWS Aurora（自动调优）、Azure SQL DB (Query Processing Tuning)、TiDB（智能统计/索引 advisor） | L05/L07/L11 工业实现 |
| 索引 advisor 思路 | Microsoft autoAdmin/DTA、Oracle Automatic Workload Repository | L05 |
| 学习型优化 | OtterTune 开源版、DBMind（openGauss 自治组件） | L06–L10 |
