# CS189 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| An Algorithm that Learns What's in a Tree (ID3, Quinlan) | 1986 | L8 | 信息增益决策树 |
| Random Forests (Breiman) | 2001 | L8 | bagging + 随机子空间 |
| Greedy Function Approximation: A Gradient Boosting Machine (Friedman) | 2001 | L8 | 函数空间梯度提升 |
| Regression Shrinkage and Selection via the Lasso (Tibshirani) | 1996 | L4 | ℓ1 正则与稀疏选择 |
| Support-Vector Network (Boser/Guyon/Vapnik) | 1992 | L6 | 最大间隔 + 核技巧起源 |
| A Training Algorithm for Optimal Margin Classifiers (Cortes & Vapnik) | 1995 | L6 | 软间隔 SVM |
| Statistical Learning Theory (Vapnik) | 1998 | L4 | VC 理论与结构风险最小化 |
| Reproducing Kernel Hilbert Space ... (Kimeldorf & Wahba) | 1971 | L7 | Representer 定理 |
| A Tutorial on Spectral Clustering (von Luxburg) | 2007 | L10 | 谱聚类系统讲解 |
| Fast Algorithms for Mining Elastic Data / k-means++ (Arthur & Vassilvitskii) | 2007 | L10 | k-means++ 初始化 |
| An Introduction to Kernel and Nearest-Neighbor Density Estimation (Parzen/Rosenblatt) | 1962 | L9 | 核密度估计 |
| Independent Component Sampling (ICA, Comon / Hyvärinen) | 1994 | L11 | 非高斯独立源分离 |
| Maximum Likelihood from Incomplete Data via EM (Dempster/Laird/Rubin) | 1977 | L13 | EM 算法 |
| Pattern Recognition and Machine Learning (Bishop) | 2006 | 多讲 | 概率视角教材 |
| Learning Representations by Back-propagating Errors (Rumelhart et al.) | 1986 | L14 | 反向传播 |
| ImageNet Classification with Deep CNNs (AlexNet) | 2012 | L15 | 深度学习引爆点 |
| Long Short-Term Memory (Hochreiter & Schmidhuber) | 1997 | L15 | 门控序列模型 |
| Revisiting Distributed Computing in the Age of GPUs / —（替代：A Few Useful ... Domingos） | — | — | — |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| The Happy Few: Compressing Probabilistic Models? / —（替代：核方法复兴综述） | — | L7 核与 NN 关系 |
| NTK 与双下降（Understanding Deep Learning Requires Rethinking Generalization / Double Descent, Belkin et al.） | 2019/2021 延伸 | L4 泛化新图景 |
| XGBoost 大规模分布式（Chen & Guestrin 工程演进 / LightGBM Ke et al.） | 2017（延伸） | L8 |
| Kernel Methods in Deep Learning 综述 | 2021 | L7 |
| The Lottery Ticket Hypothesis (Frankle & Carlini 后续) | 2019-2021 | L15 |
| Fairness Measurement and Auditing 综述（Mitchell et al.) | 2021 | L18 |
| SHAP: A Unified Approach to Interpreting Model Predictions (Lundberg & Lee) | 2017（延伸 2020+ 应用） | L18 |
| An Image is Worth 16x16 Words (ViT) | 2020 | L15 Transformer 视觉 |

> 说明：本课为理论向入门 ML 课，近 5 年选目侧重"课程理论主题的现代回响"，正文阶段逐条补全链接与卷期。

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 最小二乘/Ridge/Lasso（L2/L4） | scikit-learn / glmnet-py | LinearRegression、Ridge、Lasso |
| 逻辑回归/softmax（L3） | scikit-learn | LogisticRegression(multinomial) |
| 优化器（L5） | PyTorch / TensorFlow | SGD/Momentum/Adam |
| SVM/核方法（L6-7） | scikit-learn | SVC + kernel='rbf' |
| 树集成（L8） | scikit-learn / XGBoost / LightGBM | GradientBoosting、随机森林 |
| kNN/密度估计（L9） | scikit-learn / scipy.stats | KNeighbors、GaussianKDE |
| 聚类/谱聚类（L10） | scikit-learn | KMeans、SpectralClustering |
| PCA/ICA（L11） | scikit-learn / FastICA | PCA、FastICA |
| EM/HMM（L13） | hmmlearn / pomegranate | GaussianHMM、EM |
| 图模型（L12） | pgmpy | 贝叶斯网络推断 |
| 强化学习（L17） | Gymnasium / Stable-Baselines3 | 策略梯度/Q-learning |
| 可解释性（L18） | SHAP / LIME / Fairlearn | 特征归因与公平性审计 |
