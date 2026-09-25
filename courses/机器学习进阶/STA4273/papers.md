# U Toronto STA 4273 论文清单

## 经典论文（期望梯度、变分推断与推断-控制统一）

| 主题 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| 策略梯度 | Policy Gradient Methods for RL (Williams, REINFORCE) | 1992 | L3 score-function |
| 策略梯度 | Deterministic Policy Gradient (Silver et al.) | 2014 | L3 pathwise 侧 |
| 基线/控制变量 | Variance Reduction in Policy Gradients (Greensmith et al.) | 2004 | L4 |
| 基线 | Backprop RA-RL (Rao-Blackwellised, Titsias & Lawrence) | 2010 | L4 |
| 基线 | Revisiting REINFORCE Style Estimation (Roeder et al.) | 2017 | L4 |
| 重参数化 | Auto-Encoding Variational Bayes (Kingma & Welling) | 2013 | L3/L5/L7 |
| 松弛 | Categorical Reparameterization with Gumbel-Softmax (Jang et al.) | 2017 | L6 |
| 松弛 | The Concrete Distribution (Maddison et al.) | 2017 | L6 |
| 松弛 | Congruent for Training Gumbel (Yilmaz & Oztop? 及 straight-through Wilson) | 2017-18 | L6 |
| 精确离散 | Constructing Straight-Through Estimators (Bengio STE) | 2013 | L6 |
| 变分目标 | Monitoring Fluent Objectives (Yin & Zhou) / α-divergence (Korattiti?) | 2018 | L7 |
| 双层推断 | Amortized Inference Revisited / RAI (Kim & Mnih? Titsias von Mises) | 2018 | L7 |
| 最优控制 | Stochastic optimal control 综述（Bertsekas 教材选章） | 2019 | L8 |
| 推断-控制 | Path Integral Control (Theodorou et al.) | 2010 | L9 |
| 推断-控制 | Relative Entropy Policy Search? 原 REIC (Kappen 2005; Peters et al. 2010) | 2005-2010 | L9 |
| 推断-控制 | Reinforcement Learning as Probabilistic Inference (Ziebart; Levine) | 2008/2018 | L9 |
| 滤波梯度 | Backpropagation through filters (Arjovsky?) / 粒子平滑 (FFBS, Doucet et al.) | 1996-2002 | L10 |
| 自然梯度 | New Insights and Perspectives on the Natural Gradient (Martens) | 2020 | L11 |
| 隐变量 | Auxiliary Skill Discovery (Eysenbach?) —作为期望优化示例 | 2019 | L10 |
| 得分匹配 | Score Matching (Hyvärinen) / SSM (Vincent) | 2005/2011 | L3/L12 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| 扩散训练目标即得分匹配期望恒等式 | 2022-24 | L12：与 6.S184 数学同构 |
| GRPO / DeepSeekMath-R1 中的组基线策略梯度 | 2024-25 | L4 控制变量的 LLM 时代再现 |
| 离散潜变量精确梯度（DISLO/GRU 系） | 2022-23 | L6 续作 |
| 松弛估计器改进（gumbel 噪声结构、温度退火理论） | 2021-24 | L6 |
| 双层/隐函数推断（hyper-gradient、DETR 类 amortization） | 2022-25 | L7 |
| 随机最优控制的神经求解（HJB PINN、MCK） | 2022-25 | L8-L9 交叉 |
| 推断作为控制应用于机器人（Diffusion Policy） | 2023 | L10 现代回响 |
| 粒子变分推断（SVGD 系）与自适应基线 | 2021-25 | L11 |
| RLHF 梯度病理分析与方差控制 | 2023-25 | L4/L11 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| REINFORCE/基线 | Stable-Baselines3、RLlib、veRL（GRPO） | L4：PPO 优势基线代码 |
| 重参数化/VAE | Pyro/NumPyro、torchtune VAE 教程 | L5/L7 |
| Gumbel-Softmax | torch GumbelSoftmax、tensorflow ST-Gumbel 生态 | L6 |
| 精确离散梯度 | pyro gru 实现、Maddison 组参考代码 | L6 |
| 变分目标族 | Pyro ElkiBo 风格教程、edward2 | L7 |
| 推断-控制 | Path Integral Control 开源实现（python-sokoban PI²）、iCEM | L9 |
| 粒子滤波/FFBS | particles、filterpy、pysde 库 | L10 |
| 自然梯度 | optuna? 更准：kfac（TF/PyTorch KFAC）、Haar 优化器 | L11 |
| 得分匹配/扩散 | diffusers（ε-损失=score 期望）、score_sde | L12 |
