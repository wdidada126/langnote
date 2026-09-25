# CS188 论文与文献清单

> 与 `notes/` 各讲"延伸阅读"对应；按讲次整理的经典文献 + 近五年（2021-2026）前沿 + 知识点↔开源项目映射。
> 不确定的出处一律标注"待核实"，引用前请自行核对原文。

## 一、经典论文 / 文献（按讲次）

| 讲次 | 文献 | 要点 |
| --- | --- | --- |
| L02-L03 搜索 | Hart, Nilsson & Raphael, *"A Formal Basis for the Heuristic Determination of Minimum Cost Paths"*, IEEE SSC-5(2), 1968 | A* 原始论文，可采纳+图搜索最优性 |
| L02-L03 | Dijkstra, *"A Note on Two Problems in Connexion with Graphs"*, Numerische Mathematik, 1959 | UCS 的单源最短路特例 |
| L04 局部搜索 | Metropolis, Rosenbluth, Rosenbluth, Teller & Teller, *"Equation of State Calculations by Fast Computing Machines"*, J. Chem. Phys., 1953 | 退火采样原型（MH 算法同年独立发表） |
| L04 | Kirkpatrick, Gelatt & Vecchi, *"Optimization by Simulated Annealing"*, Science 220, 1983 | SA 正式提出 + VLSI 布局应用 |
| L04 | Holland, *Adaptation in Natural and Artificial Systems*, 1975 | 遗传算法理论奠基 |
| L05 对抗搜索 | Shannon, *"Programming a Computer for Playing Chess"*, Philosophical Magazine, 1950 | 博弈树、评估函数、10^120 状态数（Shannon 数） |
| L05 | von Neumann, *"Zur Theorie der Gesellschaftsspiele"*, Math. Annalen, 1928 | minimax 定理（零和混合策略） |
| L05 | Knuth & Moore, *"An Analysis of Alpha-Beta Pruning"*, Artificial Intelligence 6, 1975 | α-β 剪枝复杂度分析（最佳着法序 b^(d/2)）。注：α-β 最早实现归于 McMullen 1959 未发表报告、Hart&Nilsson 1963 棋赛（**待核实**），发表文献一般引 Knuth-Moore |
| L05/L21 | Silver et al., *"Mastering the Game of Go without Human Knowledge"*, Nature 550, 2017 | AlphaZero：MCTS+NN eval（现代 minimax） |
| L06 CSP | Mackworth, *"Consistency in Networks of Relations"*, AI 8, 1977 | 弧一致性（AC-3 理论前身） |
| L06 | Haralick & Elliott, *"Towards Fast Intelligent Backtracking"*, IJCAI 1980 | forward checking 与动态变量序 |
| L07 | Dechter & Pearl, *"Tree Clustering and Cycle Cutset Conditioning Schemes for Constraint Networks"*, AI 42, 1989 | 树分解/割集条件化开山 |
| L09-L10 | Pearl, *Probabilistic Reasoning in Intelligent Systems*, Morgan Kaufmann, 1988（专著） | 贝叶斯网络与 belief propagation |
| L10 | Cooper, *"The Computational Complexity of Probabilistic Inference"*, AI 48, 1990 | 精确 BN 推断 NP-hard |
| L11 | Dempster, Laird & Rubin, *"Maximum Likelihood from Incomplete Data via the EM Algorithm"*, JRSS-B 39, 1977 | EM 原始论文 |
| L11 | Ng & Jordan, *"On Discriminative vs. Generative Classifiers"*, NeurIPS 2001 | NB vs LR 渐近比较 |
| L12 MDP | Bellman, *Dynamic Programming*, Princeton, 1957（专著） | 最优方程与值迭代雏形 |
| L12 | Howard, *Dynamic Programming and Markov Processes*, MIT, 1960（专著） | 策略迭代 |
| L13 RL | Sutton, *"Learning to Predict by the Methods of Temporal Differences"*, Machine Learning 3, 1988 | TD 学习 |
| L13 | Watkins & Dayan, *"Q-learning"*, Machine Learning 8, 1992 | Q-learning 原始论文（Watkins 1989 博士论文，**待核实**发表细节） |
| L13→L14 | Mnih et al., *"Human-level Control through Deep Reinforcement Learning"*, Nature 518, 2015（DQN 原版 2013/2015） | 深度 Q-learning（Atari） |
| L14 | Williams, *"Simple Statistical Gradient-Following Algorithms for Connectionist RL"* (REINFORCE), Machine Learning 8, 1992 | 策略梯度原始形式 |
| L14 | Sutton et al., *"Policy Gradient Methods..."*, NeurIPS 1999/2000 | 策略梯度定理 |
| L14 | Kingma & Ba, *"Adam: A Method for Stochastic Optimization"*, ICLR 2015 (arXiv 2014) | 通用优化器（近似 RL 与 DL 共用） |
| L14 | Mnih et al., *"Asynchronous Methods for Deep RL"* (A3C), ICML 2016 | 异步策略梯度/并行 rollout |
| L14 | Schulman et al., *"Proximal Policy Optimization Algorithms"*, arXiv 1707.06347, 2017 | 现代 PG 默认算法（RLHF 底座） |
| L15 效用 | von Neumann & Morgenstern, *Theory of Games and Economic Behavior*, 1944（专著） | 期望效用公理化 |
| L16 VoI | Howard, *"Information Value Theory"*, IEEE SSC-2(1), 1966 | VoI 奠基 |
| L16/L08 信息论 | Shannon, *"A Mathematical Theory of Communication"*, Bell System Tech. J., 1948 | 熵/信息增益的数学源 |
| L17 HMM | Baum & Sellke / Baum, Petrie, Soules & Weiss, 1970 及更早技术报告（**待核实**：Baum-Welch 最早见 1966 UCLA 报告与 1967/1970 Ann. Math. Statist. 系列） | HMM 参数估计 EM |
| L17 | Rabiner, *"A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition"*, Proc. IEEE 77(2), 1989 | 滤波/平滑/Viterbi 标准教程 |
| L17 | Viterbi, *"Error Bounds for Convolutional Codes..."*, IEEE Trans. IT, 1967 | Viterbi 算法 |
| L18 采样 | Arulampalam et al., *"A Tutorial on Particle Filters for Online Nonlinear/Non-Gaussian Bayesian Tracking"*, IEEE TSP, 2002 | 粒子滤波教程 |
| L18 | Doucet, Freedman & Gordon (eds.), *Sequential Monte Carlo Methods in Practice*, 2001（专著） | SMC 系统化 |
| L19 感知机 | Rosenblatt, *"The Perceptron: A Probabilistic Model for Information Storage and Destruction in the Brain"*, Psych. Review, 1958 | 感知机原始论文 |
| L19 | Minsky & Papert, *Perceptrons*, MIT, 1969（2e 1988） | XOR 不可分 → 第一次 AI 寒冬 |
| L20 神经网络 | Rumelhart, Hinton & Williams, *"Learning Representations by Back-propagating Errors"*, Nature 323, 1986 | 反向传播普及 |
| L20 | Cybenko, *"Approximation by Superpositions of a Sigmoidal Function"*, Math. Control Signals Systems 2, 1989 | 通用近似定理 |
| L21 博弈论 | Nash, *"Equilibrium Points in N-Person Games"*, PNAS 36, 1950 | 纳什均衡存在性 |
| 规划补充 | Fikes & Nilsson, *"STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving"*, IJCAI 1971 | 经典规划建模语言 |
| 规划补充 | Blum & Furst, *"Fast Planning Through Planning Graph Analysis"*, AI 90, 1997 | GraphPlan |
| 规划补充 | Hoffmann & Nebel, *"The FF Planning System"*, AI Magazine 2001 | FF 启发式（层图 + relaxed plan） |
| 规划补充 | Helmert, *"The Fast Downward Planning System"*, JAIR 6, 2006 | 本项目 `planning` 思想来源、PDDL 竞赛常胜基座 |
| 课程哲学 | Turing, *"Computing Machinery and Intelligence"*, Mind 59, 1950 | 图灵测试 |
| 课程哲学 | Searle, *"Minds, Brains, and Programs"*, BPS 3, 1980 | 中文房间 |

> "PEBL"、"Hansel and Gray" 等检索线索未找到可靠对应文献，按任务要求不收录；如需扩展请先自行核实（**待核实**）。

## 二、近五年文献（2021-2026，LLM 时代的搜索 / 推断 / 规划）

| 年份 | 文献 | 与本课讲次的呼应 |
| --- | --- | --- |
| 2021 | Chen et al., *"Decision Transformer: RL as Sequence Modeling"*, NeurIPS 2021 | L12-L14：用 Transformer 条件生成轨迹替代策略梯度 |
| 2022 | Wang et al., *"EfficientZero: Mastering Atari with Limited Data and Interventions"*, ICLR 2022 | L05+L12：AlphaZero 后继，样本高效 MCTS（UCT 学习版） |
| 2023 | Yao et al., *"ReAct: Synergizing Reasoning and Acting in Language Models"*, ICLR 2023 | L01+规划：思维链+动作 = agent loop 的语言模型实例 |
| 2023 | Yao et al., *"Tree of Thoughts: Deliberate Problem Solving with LLMs"*, NeurIPS 2023 | L02-L03：在"想法空间"跑 BFS/DFS/A*-like 搜索，教科书级现代回响 |
| 2023 | Somepalli et al., *"LATS: Language Agent Tree Search"*, arXiv 2310.04406（ICML 2024 版本**待核实**） | L05+L18：MCTS/UCT 用于 LLM 推理 |
| 2023 | Wang et al., *"Voyager: An Open-Ended Embodied Agent with LLMs"*, TMLR 2024 | L01+L12+规划：技能库=经验回放+课程式探索 |
| 2023 | Mankowitz et al. (DeepMind), *"AlphaDev: Faster sorting algorithms discovered using AI"*, Nature 617, 2023 | L04：搜索/进化式算法发现（LLM+assembly 树搜索） |
| 2024 | Besta et al., *"Graph of Thoughts"*, AAAI 2024 | L02-L03：推理状态图与图上搜索的推广 |
| 2024 | Romera-Paredes et al., *"Mathematical discoveries from program search with LLMs"* (FunSearch), Nature 625, 2024 | L04：GA 的现代版（LLM 作变异算子） |
| 2024 | Trinh & Luong, *"AlphaGeometry: An Efficient Fire-Time Solver for Olympiad-Level Geometry"*, ICLR 2024 | L02-L03+逻辑：神经候选 + 符号搜索（DP） 混合 |
| 2024 | Shao et al., *"DeepSeekMath: Pushing the Limits of Math Reasoning"* (GRPO), arXiv 2402.03300 | L14：组内相对基线的策略梯度（o1 风格 RL 公开化） |
| 2020（边界收录） | Schrittwieser et al., *"Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model"* (MuZero), Nature 588, 2020 | L12+L05：模型学习 + MCTS 规划（AlphaZero 续篇） |
| 2025+ | o1/R1 测试时计算扩展（*"s1: Simple test-time scaling"*, arXiv 2501.19393 等） | L02-L03：搜索/采样换智能 = test-time compute 的朴素实现（2025 年该方向论文快速更迭，引用前**待核实**最新版本） |

## 三、知识点 ↔ 开源项目映射表

| 知识点（讲次） | 官方/教学实现 | 工业级实现 | 备注 |
| --- | --- | --- | --- |
| 搜索/启发式（L2-L3） | **pyAIMA `search.py`**（aimacode/aima-python，AIMA 官方代码，与教材逐节对应）；本项目 `projects/search` | **NetworkX**（bfs/ucs/astar）、ROS Nav2、Recast/Detour | 课内 Pacman P1 |
| 局部搜索（L4） | 本项目 `projects/local_search` | **OR-Tools**（SA/禁忌）、DEAP、pymoo、Optuna | 邻域设计是灵魂 |
| 对抗搜索（L5） | 本项目 `projects/adversarial` | **Stockfish**（α-β+NNUE）、python-chess、OpenSpiel | 期望搜索见 OpenSpiel expectimax |
| CSP（L6-L7） | **python-constraint**（教学级 AC-3） | **OR-Tools CP-SAT**、MiniZinc、Gecode、Z3 | 数独/排课 |
| 概率与 BN（L8-L10） | **pyAIMA `probability.py`**；本项目 `projects/bayes` | **pgmpy**（VE/BP/LW 全实现）、pomegranate、Hugin/GeNIe | d-separation 可用 pgmpy 验证 |
| 朴素贝叶斯/EM（L11） | scikit-learn `MultinomialNB`、pgmpy ParameterEstimator | 工业 spam：fastText（线性后代） | EM 教程实现遍地，选一个手写 |
| HMM（L17） | **pomegranate `HiddenMarkovModel`**、hmmlearn | 生物信息：Biopython/HMMER；语音：Kaldi（已含 WFST 搜索） | Rabiner 1989 配代码练 |
| 采样/粒子滤波（L18） | 本项目可扩 **filterpy** | 机器人定位：ROS AMCL（MCL 粒子） | Pacman P5 原型 |
| MDP（L12） | 本项目 `projects/mdp`；Gymnasium `FrozenLake/PointEnv` | **Mosek/pymdptoolbox**（带约束 MDP） | 值迭代/策略迭代对照 |
| Q-learning/RL（L13-L14） | 本项目 `projects/rl`；gym_toy_txt | **stable-baselines3**（DQN/PPO）、**Ray RLlib**（PPO/APPO/Sac）、Tianshou、Acme | SB3/RLlib 为 CS188→CS285 标准接口 |
| 效用/决策网络（L15-L16） | pyAIMA 无完整影响图 → 教学库 **UnBBE**（待核实活跃度） | Bayes Server（商业） | VoI 手算比跑库更涨功力 |
| 感知机/神经网络（L19-L20） | **micrograd / NeuralNets-ZeroToHero**（纯 python autograd） | PyTorch/JAX；LLM 训练：torchtitan/Megatron | 手写一遍 > 调库十次 |
| 博弈论（L21） | **Nashpy**（双矩阵 NE） | **OpenSpiel**（均衡求解/CFR/league training） | 配 L05 项目对照实验 |
| 规划（L2 补充 + 项目） | 本项目 `projects/planning`（GrapeWorld 简化）；**Pyperplan**（教学） | **Fast Downward**（Helmert，PDDL 主流）、**FF**、VAL 校验器；Prolog 生态：**SWI-Prolog**（逻辑规划）、RDF/知识表示：**RDFLib / Apache Jena**（本课 23 讲表未含逻辑/RDF 讲次，列为延伸，**待核实**是否归入其他学期大纲） | 课内不教 PDDL，自学推荐 |
| 综合 | 官方 Pacman 框架（edstem 分发，GitHub 有历史 mirror **待核实**版权） | — | 6 个 Project 对应上表多行 |

## 四、使用建议

1. 每讲笔记读完后，从表一挑 1 篇原文（多为 5-15 页），对照笔记的"关键公式"看原始记号——训练读文献能力。
2. 表二用于写"技术选型/前沿报告"：任选一项回答"它把本课哪个算法搬到了什么介质上？"（如 ToT：搜索→思维空间）。
3. 表三与本地项目互证：本项目是"裸算法"，跑通一个库版做数值对照（如 `projects/bayes` vs pgmpy VE 结果一致即验证实现）。
