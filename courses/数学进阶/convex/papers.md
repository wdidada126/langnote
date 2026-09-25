# papers.md — EE364A 凸优化文献

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Kuhn & Tucker, *Nonlinear Programming* | 1951 | 给出约束最优的一阶条件（KKT），对偶理论的算法化起点 | L7–L9 |
| Dantzig, *Maximization of Linear Functions of Indeterminate Variables*（单纯形法） | 1949 | 线性规划单纯形法，虽最坏指数但开启 LP 工业应用 | L4, L6, L19 |
| Karmarkar, *A New Polynomial-Time Algorithm for Linear Programming* | 1984 | 射影内点法证明 LP 多项式可解，引发凸优化算法革命 | L14 |
| Nesterov & Nemirovski, *Interior-Point Polynomial Methods in Convex Programming*（专著/论文） | 1989/1994 | 把内点法推广到一般凸锥规划并给出复杂度理论 | L14 |
| Boyd, Ghaoui, Feron & Balakrishnan, *Linear Matrix Inequalities in System and Control Theory* | 1994 | LMI/SDP 成为控制与系统综合的标准工具 | L4, L11 |
| Cortes & Vapnik, *Support-Vector Networks* | 1995 | SVM = 凸二次规划 + 对偶 + 核技巧的工业级胜利 | L10 |
| Tibshirani, *Regression Shrinkage and Selection via the Lasso* | 1996 | L1 正则凸化产生稀疏解，机器学习与统计的桥梁 | L16, L10 |
| Grant & Boyd, *Graph Implementations for Disciplined Convex Programming*（CVX 论文） | 2006 | DCP 规则与 CVX 建模框架：让"会写凸问题"变成工程 | L4–L5 |
| Goemans & Williamson, *Improved Approximation Algorithms for Maximum Cut* | 1995 | SDP 松弛 + 随机超平面舍入的 0.878 近似比 | L19 |
| Rockafellar, *Convex Analysis*（专著） | 1970 | 共轭、次微分、对偶的系统化，本课数学语言的来源 | L3, L7 |
| Bertsekas & Tsitsiklis, *Parallel and Distributed Computation*（含对偶分解） | 1989 | 对偶分解/分布式优化，6.824 式系统的优化基础 | L10, L15 |
| Parikh, Boyd, Jiang & Ehrenberg, *Distributed Optimization and Statistical Learning via ADMM* | 2011/2014 | ADMM 综述，把分解方法带回大规模机器学习 | L15 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| O'Donoghue, *CVXPYlayers / Differentiable Convex Optimization* 后续（含 Miller et al. 的加速与扩展） | 2021–2023 | 把凸求解器变成可微层，嵌入端到端网络训练 | L4, L9, L12 |
| Argueny, Bailey & O'Donoghue, *Clarabel: An Interior-Point Solver for Conic Programs with Generalized Asymmetric Cones* | 2022–2024 | Rust 实现的高性能锥规划内点求解器，支持指数锥 | L14 |
| 大规模一阶方法与 GPU 加速凸优化（proximal/ADMM on GPU 一族） | 2021–2025 | 用算子分裂 + 并行归约突破求解规模瓶颈 | L15 |
| 混合整数凸规划与凸松弛在 ML 中的应用（验证神经网络的 LP/SDP/SOS 松弛） | 2021–2025 | 用凸松弛给 DNN 鲁棒性/可达性可证明界 | L19 |
| 最优控制的 MPC 求解器加速（OSQP 后继、code generation 一族） | 2021–2024 | 把 QP 序列编译为嵌入式代码，毫秒级闭环 | L12–L15 |
| 组合优化的机器学习增强（学习舍入、学习割平面） | 2021–2025 | 用学习指导分支定界，保留凸松弛的证书 | L19 |
| LLM 训练优化器的凸/非凸理论分析（收敛速率、预条件设计，如 Muon/Shampoo 后续） | 2023–2025 | 二阶信息与谱方法优化器的现代复兴与界 | L12–L13 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| DCP 建模与问题规范化 | `cvxpy/cvxpy`, `cvxgrp/cvx`（MATLAB） | 把用户写的凸表达式编译为标准锥形式 |
| LP/QP 求解 | `ERGO-Code/HiGHS`, `OSQP/OSQP`, `glpk` | 调度、网络流、模型预测控制内核 |
| 锥规划（SOCP/SDP/指数锥） | `oxfordcontrol/Clarabel.rs`, `cvxgrp/cvxopt`, `cmpielke/cvxgen` | 控制综合、鲁棒优化、近似算法 |
| 内点法核心数值 | `cvxgrp/cvxopt`, `ERGO-Code/HiGHS`, `OSQP/OSQP` | 每次迭代的 KKT 线性系统求解与预处理 |
| ADMM 与分布式优化 | `scikit-learn`（ElasticNet / SAGA）, `dmlc/xgboost`（分布式一阶） | 大规模回归、联邦式参数聚合 |
| 可微分优化层 | `cvxpy/cvxpylayers`, `jax-ml/jax`（隐式微分） | 端到端学习中的约束求解层 |
| 二阶/预条件优化器 | `microsoft/DeepSpeed`（ZeRO + Adam）, `NVIDIA/Megatron-LM`（分布式优化状态） | 预条件与优化器状态管理的工业实现 |
| 组合优化与松弛 | `ERGO-Code/HiGHS`（MIP）, `coin-or/Cbc`, `scipopt/SCIP` | 用 LP/SDP 松弛 + 分支定界求整数解 |
| 鲁棒与分布鲁棒优化 | `cvxpy` 鲁棒优化示例集, `robustpulp` | 不确定性集合与锥可处理性 |
| 金融与资源分配 | `riskfolio-lib`, `cvxpy` portfolio 示例 | 均值-方差与 CVaR 组合优化 |
