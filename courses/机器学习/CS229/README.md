# Stanford CS229: Machine Learning 学习笔记（【CORE】完整版目录）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS229: Machine Learning |
| 学校 | Stanford（斯坦福） |
| 主讲 | Andrew Ng（吴恩达；课程 notes 以 Ng 手写讲义为核心） |
| 教材 | 无指定教材；官方课程 Notes（blue book，9 章 + 附录）质量极高，即为教材 |
| csdiy 路径 | `机器学习/CS229: Machine Learning`（页面更新：2024-09-14） |
| 最新期次 | 每季度滚动开课（Autumn/Winter/Spring/Summer）；公开资源以经典版 notes + B 站完整视频为准 |
| 状态 | 全量（2026-09）：notes/L01-L23 中文笔记、papers/papers.md（经典+近五年+开源映射）、projects/p01-p09（numpy-only）已完成 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 100 小时；先修：高数、概率论、Python，需较深厚数学功底 |

## 为什么学

- 吴恩达讲授的研究生版机器学习：与 Coursera ML 同源主题，但偏重数学理论，是"不满足于调包、想深入算法本质"的标准路线。
- 课程网站提供所有 notes，写得非常专业且理论：从 LMS 推导到 GLM 指数族、从 SVM 对偶到 VC 理论、从 boosting 到 EM/HMM/RL，是自学 ML 理论的最佳单一文献之一。
- 与 Coursera ML 形成"直觉 ↔ 证明"的互补：C1 的每个"照做即可"在 CS229 都有拉格朗日对偶与一致性证明。
- 经典项目制：autonomous helicopter（斯坦福无人直升机）等传统 project 选题是把理论落地成论文的跳板。

## 先修与知识联系

| 方向 | 关联课程/知识 |
| --- | --- |
| 先修 | EE364A（凸优化）、EE363（最优控制，Part III 用）、概率论与线代（CS70/MIT18.06 级别）、Python |
| 前导 | Coursera ML / 机器学习/ML（直觉版，可并行对照）、CS188（概率与 RL 部分） |
| 平级互补 | CS189（伯克利版，开源作业与 autograder；理论深度相近风格不同） |
| 后续 | CS229M/STATS214（ML 理论）、CS224n/CS231n/CS285（应用方向）、CS15-779/LLM 系统课（MLSys 方向） |
| 知识输出 | SVM/核方法 → scikit-learn；树集成 → XGBoost/LightGBM；EM/GMM → 语音与生物信息；RL → Gymnasium/SB3 |

## 最新年份讲义全章节目录（对应官方 Notes 合订本 9 章 + 附录，映射经典讲次）

| 讲次 | 标题 | 阅读材料（Notes 章节） |
| --- | --- | --- |
| L1 | 监督学习问题设定、假设空间与代价 | Notes Ch.1 导言部分 |
| L2 | 线性回归：LMS、批量/随机梯度下降、正规方程与概率解释 | Notes Ch.1 (Linear Regression and Least Squares) |
| L3 | 分类与逻辑回归：假设函数、交叉熵损失、Newton/IRLS | Notes Ch.2 (Logistic Regression and Other GLMs) |
| L4 | 广义线性模型：指数族、Poisson 回归、GLM 拟合算法 | Notes Ch.2 |
| L5 | 生成式学习算法：高斯判别分析 GDA、朴素贝叶斯、LDA/QDA | Notes Ch.3 (Generative Learning Algorithms) |
| L6 | 判别学习 I：最大间隔分类器、函数间隔与几何间隔 | Notes Ch.4 (Discriminative Learning Algorithms) |
| L7 | 判别学习 II：SVM 对偶形式、KKT 条件、核方法 | Notes Ch.4 |
| L8 | 判别学习 III：感知机、排序学习；特征降维 PCA | Notes Ch.4 |
| L9 | 学习理论 I：偏差-方差、经验风险最小化 ERM、一致性 | Notes Ch.5 (Learning Theory) |
| L10 | 学习理论 II：VC 维、有限假设类界 | Notes Ch.5 + 附录 (VC Dimension) |
| L11 | 树与集成：决策树、特征选择、剪枝 | Notes Ch.6 (Tree Ensembles) |
| L12 | 随机森林与 boosting：bagging、AdaBoost、XGBoost/GBDT | Notes Ch.6 |
| L13 | 神经网络基础：前馈、反向传播、激活与损失 | Notes Ch.7 (Deep Learning) |
| L14 | 深度学习实践：PyTorch/TensorFlow、架构设计、调参 | Notes Ch.7 |
| L15 | CNN 与序列模型：卷积、RNN/LSTM、Transformer 概览 | Notes Ch.7 + CS224n/CS231n 延伸 |
| L16 | 无监督学习 I：k-means、Mixture of Gaussians 与 EM | Notes Ch.8 (Clustering and Unsupervised Learning) |
| L17 | 无监督学习 II：变分自编码器 VAE（导论级）、因子分析 | Notes Ch.8 + 附录 |
| L18 | 无监督学习 III：PCA/ICA、谱聚类、异常检测 | Notes Ch.8；Lecture Notes ( PCA / ICA / Anomaly Detection) |
| L19 | 概率图模型：有向/无向图、HMM、前向-后向、Viterbi | 附录/讲义 (Graphical Models and HMM) |
| L20 | 强化学习 I：MDP、值迭代与策略迭代、策略搜索 | Notes Ch.9 (Reinforcement Learning and Control) |
| L21 | 强化学习 II：Q-learning、线性规划、最优控制 LQR 概览 | Notes Ch.9 + 附录 (LQR) |
| L22 | 进阶专题：核密度估计、高斯过程、Boosting 理论（历年 Guest/选读） | 附录 (KDE / Gaussian Processes) |
| L23 | 课程项目（Project）：自主直升机/自选课题，撰写论文式报告 | 课程项目要求 |

> 附录工具线（随讲次穿插）：线性代数、概率论与信息论、导数与范数、凸优化与 Lagrange 对偶、指数族与损失函数——已并入各讲笔记的推导与"跨课程联系"小节（L02/L04/L05/L07/L21/L23）。

## 本目录产出（全量 2026-09）

- [notes/L01-L23](notes/)：23 讲中文笔记（推导要点/直觉与陷阱/前后讲联系/跨课程联系/开源应用/延伸阅读）
- [papers/papers.md](papers/papers.md)：经典论文表 + 2021-2026 近年表 + 知识点↔开源项目映射
- [projects/](projects/)：p01-p09 九个 numpy-only 配套项目（各含源码/README/run.bat/run.sh），总表见 [projects/README.md](projects/README.md)

## 课程资源（摘自 csdiy）

- 课程网站：http://cs229.stanford.edu
- 课程视频：https://www.bilibili.com/video/BV1JE411w7Ub（经典版完整搬运）
- 课程教材：无，课程 notes 写得非常好（官方 Notes + Lecture Notes 两套）
- 课程作业：不对公众开放
- 资源汇总：PKUFlyingPig/CS229（GitHub，资源与作业实现）
