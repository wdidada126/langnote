# CS50AI 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| A Formal Basis for the Heuristic Determination of Minimum Cost Paths (Hart/Nilsson/Raphael) | 1968 | L1 | A* 算法原始论文 |
| Programming Games with Minimax and Alpha-Beta Pruning (Shannon 1950 奠基, Newborn 整理) | 1950/1997 | L1/L5 | 博弈树搜索与剪枝，下棋 AI 基础 |
| Backend Reasoning in Prolog (Kowalski) / Resolution in First-Order Logic (Robinson) | 1965 | L2 | 归结推理与逻辑编程 |
| Probabilistic Reasoning in Intelligent Systems (Pearl) | 1988 | L3 | 贝叶斯网络与信念传播 |
| Optimization by Simulated Annealing (Kirkpatrick/Gelatt/Vecchi) | 1983 | L4 | 模拟退火经典 |
| Induction of Decision Trees ID3 (Quinlan) | 1986 | L5 | 信息增益决策树 |
| Learning from Delayed Rewards (Watkins, Q-Learning) | 1989 | L5 | Q-Learning 原始论文 |
| A Tensor-Based Algorithm for High-Level Image Search (Sivic & Zisserman) | 2003 | L7 | 局部特征图像检索 |
| A Computational Approach to Edge Detection (Canny) | 1986 | L7 | Canny 边缘检测 |
| A Simple Framework for Contrastive Learning (SimCLR) | 2020 | L7 | 对比学习图像表征（延伸） |
| Efficient Estimation of Word Representations (Mikolov, Word2Vec) | 2013 | L6 | 词嵌入 |
| Attention Is All You Need | 2017 | L6 | Transformer 与 LLM 基础 |
| Bias in Criminal Risk Scores (Angwin/ProPublica 报告, Barocas & Selbst 2016 综述) | 2016 | L8 | 算法偏见与公平性 |

## 近 5 年（2021-2026）相关论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| AlphaGeometry (Trinh et al., Nature) | 2024 | L2 神经+符号几何推理 |
| AlphaTensor | 2022 | L4 以强化学习发现矩阵乘法算法 |
| Chain-of-Thought Prompting (Wei et al.) | 2022 | L6 语言模型推理能力 |
| LLaMA / LLaMA-2 / LLaMA-3 | 2023-2024 | L6 开源 LLM 主线 |
| Segment Anything (SAM) | 2023 | L7 图像感知基座 |
| DPO: Direct Preference Optimization | 2023 | L5/L6 对齐新范式 |
| MiniMax/Alpha-Beta Revisited (DL 时代棋类延伸) | 2023 | L1/L5 博弈搜索现代视角 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| A* / 图搜索（L1） | NetworkX / game AI 库 / ROS Navigation | 路径规划核心算法 |
| 逻辑与约束（L2） | Prolog / Z3 / OR-Tools CP-SAT | 自动推理与约束求解 |
| 贝叶斯网络（L3） | pgmpy / PyMC3 | 概率编程与推断 |
| 模拟退火（L4） | scikit-learn(simulated_annealing) / SciPy optimize | 组合优化求解 |
| Q-Learning（L5） | Gymnasium + Stable-Baselines3 | RL 智能体训练 |
| 决策树/kNN（L5） | scikit-learn | RandomForest、KNeighborsClassifier |
| 朴素贝叶斯/词嵌入（L6） | scikit-learn / gensim / spaCy | 文本分类与 NLP 特征 |
| 边缘/特征检测（L7） | OpenCV / scikit-image | Canny、Hough、特征匹配 |
