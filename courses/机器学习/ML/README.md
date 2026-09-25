# Coursera: Machine Learning（Stanford，吴恩达 2022 修订版）学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Machine Learning Specialization（Coursera，Stanford 出品；旧版为 2012 Coursera ML，CS230 前身谱系） |
| 学校 | Stanford（吴恩达在 Coursera 开设） |
| 主讲 | Andrew Ng（吴恩达） |
| 教材 | 无指定教材；2022 新版配套编程作业 notebook 即实践教材 |
| csdiy 路径 | `机器学习/Coursera: Machine Learning`（页面更新：2026-02-22） |
| 最新期次 | 2022 修订版（Machine Learning Specialization，3 门子课 11 个模块，Coursera 持续滚动开班） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟，约 100 小时；先修：AI 入门 + 熟练使用 Python；语言 Python |

## 为什么学

- 吴恩达的成名作之一，Coursera 上数十万付费学习者、白嫖用户数量再高一个量级，是全世界最知名的 ML 入门课。
- 对新手极其友好：能把机器学习讲成 1+1=2 一样直白，线性回归、逻辑回归、神经网络、决策树、无监督、异常检测、推荐系统、强化学习一站覆盖。
- 作业保姆级：代码框架完整、背景多取自生活，学以致用。
- 2022 修订版重构为 3 门子课系列，申请助学金后可免费学习；想深究数学理论再衔接 CS229/CS189。

## 先修与知识联系

- 先修：基本线性代数/微积分直觉、Python；csdiy 建议先过 AI 入门（如 CS50AI）。
- 后续：CS229（研究生版理论深化）、CS189（伯克利版理论+开源作业）、深度学习/CS230（本课 C2 神经网络模块的展开）。
- 横向：与 CS229 共享线性回归/逻辑回归/SVM 等主题但刻意降低数学门槛。
- 知识输出：梯度下降/逻辑回归 → scikit-learn 与一切 ML 工程；推荐系统 → 工业界召回/排序入门；C3 强化学习 → CS188/CS285。

## 讲义章节目录（2022 Specialization，C1-C3 共 11 个模块）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| C1M1 | 机器学习简介：监督 vs 无监督、回归 vs 分类 | 课程视频 Week 1 |
| C1M2 | 线性回归与成本函数：模型表示、平方误差损失 | Notebook: Linear Regression |
| C1M3 | 梯度下降：更新规则、学习率、批量大小（含可视化工具） | Notebook: Gradient Descent |
| C1M4 | 线性回归实践：多特征、特征缩放、normal equation（选学）、numpy | Lab: Python & NumPy |
| C1M5 | 逻辑回归与分类：决策边界、损失函数、正则化 | Notebook: Logistic Regression |
| C1M6 | 神经网络入门：模型表示、前向传播、PyTorch 初步（C2 起） | C2 Week 1 讲义 |
| C2M7 | 神经网络训练：反向传播直觉、损失/激活选择、梯度检查 | C2 Week 2 讲义 |
| C2M8 | 应用 ML 的建议：评估指标、偏差/方差、学习曲线、误差分析 | C2 Week 3 讲义 |
| C2M9 | 决策树：信息增益、剪枝、随机森林与 XGBoost | C2 Week 4 讲义 |
| C3M10 | 无监督学习：聚类（k-means）、异常检测（高斯分布）、降维 | C3 Week 1 讲义 |
| C3M11 | 推荐系统与强化学习：协同过滤/矩阵分解、MCM、Q-learning、策略梯度 | C3 Week 2-3 讲义 |

> 注：2022 版实际结构为 C1（6 模块）/C2（4 模块）/C3（3 模块），上表合并周次为 11 讲骨架，具体模块标题以 Coursera 当前页面为准。

## 课程资源（摘自 csdiy）

- 课程网站：https://www.coursera.org/specializations/machine-learning-introduction
- 课程视频：参见课程网站
- 课程教材：无
- 课程作业：参见课程网站（保姆级编程 notebook）
- 资源汇总：csdiy 注明作者本地实现遗失，但本课资料网上极易获取，Coursera 一应俱全
