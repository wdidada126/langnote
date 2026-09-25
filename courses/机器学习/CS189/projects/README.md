# CS189 配套项目计划

> 原则：每章一个可运行小项目，本轮只规划代码与 build 方式、不写代码。语言以 Python + numpy 为主（课程 homework 即 numpy/Jupyter 风格），深度学习部分用 PyTorch 对照。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2-3 线性模型 | Python (numpy) | 正规方程解回归 + 感知机/logistic 手写数字分类 | `python linear/fit.py`；`pytest test_lstsq.py` |
| L4 正则化 | Python (numpy) | Ridge/Lasso 路径 + 交叉验证选 λ，画偏差-方差曲线 | `python reg/path.py --l1 --l2` |
| L5-6 优化与 SVM | Python (numpy) | 手写梯度下降族 + SMO 解 SVM 对偶，对齐 sklearn | `python svm/smo.py`；`pytest test_smo.py` |
| L7 核方法 | Python (numpy) | 核技巧实现 RBF 分类 + reproducer 定理可视化 | `python kernels/rbf.py` |
| L8 树与集成 | Python (numpy/sklearn) | 手写决策树增益分裂；XGBoost 表格竞赛 baseline | `python trees/fit.py` |
| L9-11 非参/聚类/降维 | Python (numpy/sklearn) | 手写 k-means + kNN/KDE + PCA 人脸识别(特征脸) | `python cluster/kmeans.py`、`python pca/eigenfaces.py` |
| L12-13 图模型与 EM | Python (numpy) | 手写 GMM-EM 与 HMM 前向-后向/Viterbi | `python em/gmm.py`、`python hmm/forward_backward.py` |
| L14-15 深度学习 | Python (PyTorch) | 手写反向传播后搭 mini-CNN + Transformer 块 | `python dl/train_cnn.py`；CPU 可跑 |
| L16 采样 | Python (numpy) | Metropolis-Hastings 采样 2D 高斯，对比解析 | `python mc/mh.py` |
| L17 强化学习 | Python | 表格 Q-learning 解 GridWorld + 策略梯度玩具 | `python rl/grid_q.py` |
| L18 公平/解释 | Python (numpy) | 在小数据集上实现 SHAP 近似 + 公平性度量报告 | `python explain/shap_approx.py` |
| 期末 | Python | 自选数据集完整 ML pipeline（含报告） | `python final/run.py` |
