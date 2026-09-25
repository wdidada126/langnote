# Coursera ML（2022）配套项目计划

> 原则：每章一个可运行小项目，本轮只规划代码与 build 方式、不写代码。语言 Python（numpy 手写 + scikit-learn/PyTorch 对照，贴合课程 notebook 风格）。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| C1M2-3 线性回归+GD | Python (numpy) | 手写梯度下降拟合房价，可视化收敛曲线 | `python linear_reg/fit.py --lr 0.01`；`pytest test_gd.py` |
| C1M4 向量化实践 | Python (numpy) | normal equation vs 梯度下降误差与速度对比 | `python linear_reg/compare.py` |
| C1M5 逻辑回归 | Python (numpy) | 手写 sigmoid + 交叉熵做二分类（含决策边界图） | `python logreg/train.py` |
| C2M6-7 神经网络 | Python (PyTorch) | 手写前向/反向后，用 PyTorch 复现 MNIST 子集 | `python nn_mnist/train.py --epochs 5` |
| C2M8 模型评估 | Python (sklearn) | 在带噪数据集上做学习曲线+误差分析报告 | `python eval_study/analyze.py` |
| C2M9 决策树/集成 | Python (sklearn/XGBoost) | 表格数据上 DT vs RF vs XGBoost 对比与特征重要性 | `python trees/run.py` |
| C3M10 聚类/异常检测 | Python (sklearn) | 手写 k-means 与 sklearn 对齐；高斯异常检测 | `python cluster/kmeans.py`、`pytest test_kmeans.py` |
| C3M11 推荐/RL | Python (numpy/sklearn/Gymnasium) | 矩阵分解 recommender + Q-learning 解 GridWorld | `python recsys/mf.py`、`python rl/grid_q.py` |
