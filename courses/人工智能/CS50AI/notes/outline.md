# CS50AI 提纲

> 骨架级要点，正文笔记待逐讲展开。

## L1 Search
- 状态空间建模：state / action / transition / goal，问题即图。
- 无信息搜索：BFS（最优最短）、DFS（省内存可循环）、UCS（代价最优）。
- A*：f = g + h，h 可采纳 ⇒ 最优；h 一致 ⇒ 无需重开闭集。

## L2 Logic
- 命题逻辑：真值表、CNF/DNF、归结（resolution）反证式推理。
- 谓词逻辑与合一（unification）：表达"所有人类必死"级别知识。
- 推理引擎：前向链（数据驱动）vs 后向链（目标驱动），与 Prolog 思想。

## L3 Uncertainty
- 概率公理、条件概率、贝叶斯定理、全概率公式。
- 贝叶斯网络：D-separation 与条件独立，joint 分布因式分解。
- 推断：枚举、变量消元、似然加权采样。

## L4 Optimization
- 约束满足与优化：cryptography（constraint 分配）、n-queens 局部搜索。
- 爬山法与局部最优问题；模拟退火的温度调度直觉。
- 应用题：minesweeper 中的概率推理 + 决策优化。

## L5 Learning
- 监督学习流程：模型类、损失、训练/测试集与泛化。
- 决策树（信息增益/熵）、kNN（非参数、距离度量）。
- 神经网络前向与梯度；强化学习：值迭代 → Q-learning（exploit vs explore）。

## L6 Language
- 词袋与朴素贝叶斯文本分类（假设特征条件独立）。
- 马尔可夫文本生成与联合概率链式法则；句子合法性判断。
- 词嵌入与 Transformer/注意力：从 Markov 到 LLM 的叙事线。

## L7 Perception
- 图像检索 pipeline：parsing → 特征提取 → 匹配。
- 边缘检测（梯度幅值 + 非极大值抑制 + 滞后阈值）、Hough 变换找直线。
- 作业：reversi/图像搜索，OpenCV 基本用法。

## L8 Ethics
- 偏见来源：数据偏见与算法放大；公平性度量（demographic parity vs equalized odds）。
- 隐私（人脸识别）、自动化决策的可解释性与问责。
- 案例：犯罪预测、招聘筛选等高风险应用的争议。

## 期末项目
- 选型：搜索/AI 游戏/分类器/计算机视觉/生成均可。
- 报告规范：清晰描述算法设计与评估结果。
