# UCB CS189: Introduction to Machine Learning 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS189 / EECS C189: Introduction to Machine Learning |
| 学校 | UC Berkeley（伯克利） |
| 主讲 | Jon Barron & Joseph E. Gonzalez（经典完整公开期） |
| 教材 | 无单一教材；官方课程 notes（eecs189.org 逐讲 PDF）+ PRML/ESL 参考 |
| csdiy 路径 | `机器学习/CS189: Introduction to Machine Learning`（页面更新：2022-04-03） |
| 最新期次 | eecs189.org 持续更新（Fall 2022 为资料最全公开期；每学期轮换） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 100 小时；先修：CS188、CS70；语言 Python |

## 为什么学

- 与 CS229 并称"自学 ML 理论双璧"，且比 CS229 更好的是：所有 homework 代码与 Gradescope autograder 全部开源，旁听体验完整。
- 课程 notes 讲得相当理论且深入，csdiy 作者将其作为工具书长期查阅。
- 视角偏统计学习 + 系统实践结合：从最小二乘的几何到核与正则化理论，再到深度学习与公平性，覆盖面现代。
- 作业为 numpy/Jupyter 风格的手写实现，做完即拥有可展示的 ML 基础库。

## 先修与知识联系

- 先修：CS70（离散与概率）、CS188（AI 入门，含概率图与基础 ML 章节）；线代/微积分/概率过硬。
- 前导：Coursera ML（直觉版，快速过）。
- 平级对照：CS229（Stanford 版，理论密度相近；两课 notes 互为补充阅读）。
- 后续：CS285（深度 RL，承接 L17）、CS224n/CS231n（承接深度学习部分）、STATS214/CS229M（理论再深化）。
- 知识输出：核方法/正则化 → scikit-learn 内核；优化 → PyTorch 优化器；公平性/可解释性 → Fairlearn/SHAP 生态。

## 讲义章节目录（对应 eecs189.org 公开讲次，Fall 2022 资料最全集）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程导论 + 线性回归 | Lecture Note 1；BOS Ch.1-3 |
| L2 | 线性模型的几何：最小二乘、投影、基展开 | Note 2；PRML 3.1 |
| L3 | 线性模型做分类：感知机、logistic 回归、softmax | Note 3；ESL 4.4 |
| L4 | 过拟合与控制：偏差-方差、正则化路径、交叉验证 | Note 4；ESL 7 |
| L5 | 优化 I：凸性、梯度下降族、线搜索 | Note 5；Boyd Ch.9 |
| L6 | 优化 II：对偶理论、KKT、SVM  primal/dual | Note 6；ESL 4.2 + EE364A |
| L7 | 核与表示：再生核希尔伯特空间、reproducer 定理、核技巧 | Note 7；PRML 6 |
| L8 | 树模型与结构化预测：决策树、随机森林、提升、图模型入门 | Note 8；Hastie Ch.9/15 |
| L9 | 最近邻与非参数方法：核密度估计、局部回归 | Note 9；PRML 2.5/6.4 |
| L10 | 聚类：k-means、谱聚类、层次聚类 | Note 10；ESL 14 |
| L11 | 降维：PCA、ICA、随机投影 | Note 11；PRML 12 |
| L12 | 概率图模型：有向/无向、团分解、变量消元 | Note 12；Koller Ch.3-9 选 |
| L13 | 推断与学习：EM、GMM、HMM、变分推断入门 | Note 13；PRML 9-10/13 |
| L14 | 深度学习 I：前馈网络、反向传播、优化器 | Note 14；DL Book Ch.6 |
| L15 | 深度学习 II：CNN、序列模型、注意力概览 | Note 15；DL Book Ch.9-10 |
| L16 | 采样与蒙特卡洛：重要性采样、MCMC 概览 | Note 16；PRML 11 选 |
| L17 | 强化学习：bandit、MDP、值函数与策略梯度概览 | Note 17；Sutton & Barto 选 |
| L18 | 公平性、可解释性与伦理：度量、审计、因果概览 | Note 18；Barocas et al. 2019 |

> 注：讲次以 eecs189.org 各学期 Syllabus 为准（学期间顺序有调整），骨架阶段允许微调；配套 homework 共 7-8 次 + 期末项目。

## 课程资源（摘自 csdiy）

- 课程网站：https://www.eecs189.org/
- 课程视频：https://www.youtube.com/playlist?list=PLOOm2AoWIPEyZazQVnIcaK2KnezpGZV-X
- 课程教材/笔记/作业：均见 eecs189.org
