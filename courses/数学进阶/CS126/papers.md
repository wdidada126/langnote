# papers.md — EE C126 概率论与随机过程文献

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Page, Brin, Motwani & Winograd, *The PageRank Citation Ranking* | 1999 | 把链接结构建模为马尔可夫链，用主特征向量做网页排序 | L15, L16 |
| Neyman & Pearson, *On the Problem of the Most Efficient Tests of Hypotheses* | 1933 | 给出固定虚警下最优检验（N–P 引理），频率派统计基石 | L22 |
| Kolmogorov, *Über das analytische Problem der Mechanik* / 概率论基础著作 | 1933 | 用测度论给概率论公理化，L1 的 (Ω,F,P) 由此而来 | L1, L9 |
| Markov, *Extension of the law of large numbers* | 1906 | 引入相依序列（马尔可夫链），打破独立性假设 | L15 |
| Erlang, *Solution of the Local Telephone Problem* | 1909 | 排队论与话务量模型的起源，Poisson 到达 + 服务台数 | L18, L20 |
| Little, *A Proof for the Queuing Formula L = λW* | 1961 | 用守恒论证给出与分布无关的排队恒等式 | L20 |
| Kalman, *A New Approach to Linear Stochastic Filtering Problems* | 1960 | 递推最优滤波：把条件期望变成可计算的矩阵递推 | L13, L24 |
| Baum, Petrie, Soules & Weiss, *A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains* | 1970 | HMM 参数学习（Baum–Welch/EM 特例） | L24 |
| Rabiner, *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition* | 1989 | 前向/后向/Viterbi 三算法系统化，语音识别标准教材 | L24 |
| Doob, *Stochastic Processes*（专著）/ 鞅论奠基 | 1953 | 鞅与停时的现代框架 | L19 |
| Chernoff, *A Measure of Asymptotic Efficiency for Tests* | 1952 | 指数尾界（Chernoff 界），随机算法分析核心工具 | L7, L8, L19 |
| Metropolis, Rosenbluth, Rosenbluth, Teller & Teller, *Equation of State Calculations by Fast Computing Machines* | 1953 | MCMC 起点：用马尔可夫链从平稳分布采样 | L16, L23 |
| Bellman, *Dynamic Programming*（专著/论文） | 1957 | 最优性原理与 Bellman 方程，MDP 的数学内核 | L25 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Score-Based Generative Modeling through SDEs (Song et al., ICLR 2021) 及其后续 | 2021–2023 | 把扩散模型写成连续时间随机过程，用 score 函数替代似然 | L10, L19, L24 |
| MCMC 理论现代化（如 *Near-optimal MCMC sampling conductance* 一族、Gibbs 在 LLM 解码中的应用） | 2021–2025 | 用谱隙/收敛率给出采样算法的可证明复杂度 | L16, L19 |
| 强化学习中的浓度不等式与样本复杂度分析（finite-time MDP 界族） | 2021–2025 | 用 Azuma/Bernstein 型界给 RL 算法的样本量保证 | L7, L19, L25 |
| LLM 解码的随机性分析（temperature/top-p、self-consistency 的蒙特卡洛解释） | 2022–2025 | 把采样策略与估计偏差/方差联系起来 | L4, L8, L21 |
| 数据中心与云计算负载建模论文（SOSP/NSDI 一族：请求到达的重尾与突发） | 2021–2024 | 指出 Poisson 假设在真实系统失效，改用重尾/自相似过程 | L14, L18, L20 |
| 变分推断与归一化流中的密度变换（连续变量似然计算） | 2021–2024 | 雅可比行列式换元在现代生成模型中的工业级使用 | L12, L23 |
| 假设检验的现代化（conformal prediction 与可控错误率） | 2021–2024 | 给出模型无关、有限样本的置信/错误率控制 | L21, L22 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 马尔可夫链 / 平稳分布 | `apache/spark` MLlib（PageRank/PowerIterationClustering）, `networkx`（中心性与随机游走） | 链接分析、图嵌入、node2vec 式随机游走 |
| MCMC / 采样 | `pymc-devs/pymc`, `stan-dev/stan`（NUTS）, `blackjax-devs/blackjax`（JAX） | 后验采样、R̂/有效样本量等收敛诊断 |
| 条件期望与滤波 | `rogeliog/filterpy`（Kalman/粒子滤波）, `pykalman` | 目标跟踪、状态估计、机器人定位 |
| HMM / Viterbi | `hmmlearn/hmmlearn`, `pomegranate`（Bengio） | 语音/序列标注、生物信息 |
| 排队论与性能建模 | `simpy`（离散事件仿真）, `queueing`（SAFMIR 排队公式库） | 吞吐/延迟仿真、容量规划、M/M/1 与 M/G/1 计算 |
| 蒙特卡洛积分与方差缩减 | `scipy.stats.qmc`（Sobol/拉丁超立方）, `PyMC`, `DifferentialEquations.jl` 随机积分后端 | 高维积分、不确定性传播 |
| MLE / 统计推断 | `statsmodels`, `scipy.optimize`, `arviz` | 参数估计、置信区间、模型比较 |
| 假设检验与保形预测 | `statsmodels`（多重检验校正 `multipletests`）, `mgz101` 的 Auto-Conformalized-Multiple-Testing | FDR/FWER 控制、模型无关预测集 |
| 鞅与浓度不等式（算法实现） | `scikit-learn`（随机森林的方差分析、`partial_dependence`）, `datasketch`（HyperLogLog 误差界） | 概率数据结构的误差上界 |
| RL 中的 MDP | `Stable-Baselines3`, `ray-project/ray`(RLlib), `Acme` | Bellman 迭代、策略梯度的概率基础 |
