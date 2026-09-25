# CMU 10-708 论文清单

## 经典论文（图模型、推断与变分方法）

| 主题 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| 总纲 | Probabilistic Graphical Models: Principles and Techniques（Koller & Friedman 教材） | 2009 | 全课骨架 |
| 精确推断 | Decision-Theoretic Principles in Bayesian Networks (Shachter) | 1986 | L6 junction tree |
| 精确推断 | Understanding the Bethe Approximation (Yedidia/Freeman/Weiss) | 2003 | L5 BP 与自由能 |
| MAP | An Exact Algorithm for MAP Inference with Graph Cuts (Boykov, Kolmogorov, Zabih) | 2001 | L7 |
| MAP 松弛 | Tree Approximations and LP Decoding (Werner; Komodakis) | 2007 | L7 对偶分解 |
| 变分 | A Tutorial on Variational Inference / Jordan CAVI 原始 (Saul, Jordan) | 1999 | L9 |
| 平均场 | Mean Field Theory in ML（Bishop ch10 + Parise 教程） | 2016 | L9 |
| 结构化预测 | Conditional Random Fields (Lafferty, McCallum, Pereira) | 2001 | L10 |
| 结构化预测 | Structured Perceptron (Collins) | 2002 | L10 |
| MCMC | Stochastic Relaxation (Geman) / MCMC 综述 (Geyer) | 1984/1992 | L11 |
| MCMC | MCMC using HMC (Neal) | 2011 | L12 |
| MCMC | The No-U-Turn Sampler (Hoffman & Gelman) | 2014 | L12 |
| EM | Maximum Likelihood from Incomplete Data (Dempster, Laird, Rubin) | 1977 | L14 |
| 结构学习 | Constraint-Based Causal Discovery: PC (Spirtes et al.) | 1990 | L15 |
| 结构学习 | A Bayesian Approach to Learning BN Networks (Heckerman) / Chickering 等价类 | 1995/1996 | L15-L16 |
| 因果 | Causality (Pearl) 选章 + do-calculus | 2009 | L17 |
| 时序 | A Tutorial on HMMs and Selected Applications (Rabiner) | 1989 | L18 |
| RL 推断 | Reinforcement Learning as Probabilistic Inference: A Unifying Review (Levine) | 2018 | L19 |
| RL 推断 | Path Integral Control (Kappen) / REIC (Toussaint) / PI²Control (Theodorou) | 2005-2010 | L19 |
| IRFL | Maximum Entropy IRL (Ziebart et al.) | 2008 | L19 |
| VAE | Auto-Encoding Variational Bayes (Kingma & Welling) | 2013 | L20 |
| 深度潜变量 |DRAW / Deep Exponential Families 一类 | 2016-17 | L20 |
| GP | Gaussian Processes for ML（Rasmussen & Williams） | 2006 | L21 |
| 稀疏 GP | Inducing Point Methods (Titschias; Snelson & Ghahramani) | 2003-05 | L21 |
| DP | Blackwell & MacQueen CRP / Ferguson DP | 1973/1974 | L22 |
| DP | Exchangesability and Consistency (Blei, Jordan) / LDA (Blei et al.) | 2003 | L22 |
| IBP | The IBP as Graphical Model (Griffiths & Gharmani) | 2005 | L23 |
| IBP | The Beta Process (Hjort et al.) | 2010 | L23 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| 扩散模型作为潜变量链推断（与 L20 统一） | 2022-25 | Score/SDE 视角重审 EM/变分 |
| 图神经网络与 BP/消息传递关系再证明 | 2021-24 | 深度 GNN=可学习 BP，连接 L5 |
| 变分推断规模化（SVI、Stein 变分） | 2021-24 | L9 现代 |
| NUTS/采样器在贝叶斯 DL 中应用（BNN） | 2021-24 | L12 落地 |
| 结构学习的 LLM 时代：因果发现×语言先验 | 2023-25 | L15-L17 新变量 |
| 概率编程进化（Pyro/NumPyro/InferPy/Turing） | 2021-25 | L11-L12 工具栈 |
| 神经组合优化推断（MAP×GNN） | 2022-25 | L7 延伸 |
| 非参数贝叶斯的深度学习应用（无限宽、NTK/GP） | 2021-24 | L21-L23 |
| LLM 推理即图上推断（ToT/搜索） | 2023-25 | L24 总结视角 |
| 粒子滤波/MCMC 在 LLM 解码中的应用 | 2024-25 | L11-L12 现代案例 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| VE/BP/junction tree | pgmpy、pyAgrum | 精确推断模块 |
| MRF/Ising | OpenGM、maxsum 库 | 组合优化 |
| 变分推断 | Pyro (Uber)、NumPyro、edward2 | ELBO/CAVI |
| MCMC/HMC-NUTS | Stan、PyMC、emcee | L11-L12 |
| 结构学习 | pgmpy、causal-learn、bnlearn(R) | PC/GES/BDeu |
| 因果推断 | DoWhy、CausalNex、dagitty | do-calculus |
| HMM/LDS | hmmlearn、filterpy、pykalman | L18 |
| GP | GPyTorch、scikit-learn GP、GPflow | L21 |
| LDA/非参数 | gensim、pyLDAvis | L22-L23 |
| 深度潜变量/VAE | torch VAEGAN 生态、diffusers（潜变量视角） | L20 |
| RL 推断 | d4rl/MBRL 中的 PI²-Control、Habitat（soft value） | L19 |
| 概率编程总栈 | Pyro/Stan 教程直接对应作业 | 全课 |
