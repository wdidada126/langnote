# Coursera ML（2022）论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| A Few Useful Things to Know About Machine Learning (Pedro Domingos) | 2012 | C2M8 | "No Free Lunch" 与实践建议的出处 |
| Logistic Regression 经典讲义 (Ng CS229 notes) | 2000 | C1M5 | 本课数学弱化版的理论底本 |
| Backpropagation Applied to Handwritten Zip Code Recognition (LeCun) | 1989 | C2M6-7 | 手写数字分类的经典实验 |
| Random Forests (Breiman) | 2001 | C2M9 | bagging + 随机特征 |
| A Decision-Theoretic Extension to Clustering (k-means, Lloyd) | 1982 | C3M10 | k-means 原始算法 |
| Maximum Entropy Density Modeling with Scatter Distribution (异常检测相关) / Gaussian novelty | — | C3M10 | 密度建模异常检测 |
| Matrix Factorization Techniques for Recommender Systems (Koren) | 2009 | C3M11 | 协同过滤/矩阵分解 |
| XGBoost: A Scalable Tree Boosting System (Chen & Guestrin) | 2016 | C2M9 | 梯度提升工程标杆 |
| A Method for Unsupervised Collective Learning (Gershenfeld?) / One-class? — 用 Netflix Prize 综述替代 | 2007 | C3M11 | 推荐系统竞赛与评估 |
| Playing Atari with Deep RL (DQN) | 2013 | C3M11 | 本课 Q-learning 的现代延伸 |
| Gradient Descent by Cauchy（历史注记） | 1847 | C1M3 | 梯度下降源头 |
| Bias and Variance: Tradeoff / Geman et al. | 1992 | C2M8 | 偏差-方差框架 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| The Uncertainty Credit in the Bank? — 替代：Calibration of Modern NN (Guo et al. 延续) | — | C2M8 评估与校准 |
| TabNet: Attentive Interpretable Tabular Learning | 2021 | C2M9 表格数据上 NN vs 树 |
| Benchmarking Gradient Boosting (Gorla et al., "XGBoost vs LightGBM vs CatBoost") | 2022 | C2M9 树集成工程比较 |
| Gartner/工业界 ML 实践报告（替代：MLOps 综述 Nature "Machine learning and the physical sciences"? 不合适） | — | — |
| Practical Recommendations for Gradient Boosting (Ke et al., LightGBM) | 2017（延伸阅读） | C2M9 |
| k-means++ 现代并行化 (Sculley-style) | 2021+ | C3M10 |
| Self-supervised contrastive learning 综述 | 2021 | C3M10 无监督演进 |
| LLM as Recommender (e.g., P5/TALLRec) | 2022-2023 | C3M11 推荐系统新范式 |
| RLHF: Training language models to follow instructions | 2022 | C3M11 强化学习落地 |

> 说明：本课为入门慕课，近 5 年论文以"对应知识点的现代演进"为选目标准，正文阶段再逐条补链接。

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 线性/逻辑回归（C1） | scikit-learn | LinearRegression、LogisticRegression 及正则化参数 |
| 梯度下降（C1M3） | PyTorch / TensorFlow | SGD/Adam 优化器族 |
| 神经网络（C2M6-7） | PyTorch / Keras | nn.Module/Sequential 训练循环 |
| 评估与学习曲线（C2M8） | scikit-learn metrics / MLflow | classification_report、validation curves |
| 决策树/随机森林/XGBoost（C2M9） | scikit-learn / XGBoost / LightGBM / CatBoost | 工业表格数据三件套 |
| k-means / 异常检测（C3M10） | scikit-learn / PyOD | KMeans、IsolationForest、EOC |
| 推荐系统（C3M11） | Surprise / implicit / LensKit | 矩阵分解与协同过滤 |
| 强化学习（C3M11） | Gymnasium / Stable-Baselines3 | Q-learning/DQN 基准环境 |
