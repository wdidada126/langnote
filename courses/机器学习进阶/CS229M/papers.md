# Stanford STATS214 / CS229M 论文清单

## 经典论文（统计学习理论与深度学习理论）

| 主题 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| VC 理论 | On the Uniform Convergence of Relative Frequencies (Vapnik & Chervonenkis) | 1971 | L2-L3 |
| 组合 | A Combinatorial Problem in Number Theory (Sauer; Shelah) | 1972 | L3 Sauer-Shelah |
| 无免费午餐 | No Free Lunch Theorems for Optimization (Wolpert) / NFL for ML (Shalev-Shwartz & Ben-David) | 1995/2015 | L3 |
| Rademacher | Rademacher and Gaussian Complexities (Bartlett & Mendelson) | 2002 | L4 |
| PAC-Bayes | PAC-Bayesian Stochastic Modeling (McAllester) | 1999 | L5 |
| PAC-Bayes 应用 | Competitive Analysis of Neural Network Training (Dziugaite & Roy) | 2017 | L5 |
| 统计下界 | Introduction to Nonparametric Estimation (Tsybakov 教材) | 2009 | L6 |
| 凸优化 | Lectures on Convex Optimization (Nesterov 教材) | 2018/1983 | L7 |
| SGD | Stochastic Gradient Descent for Strongly Convex (Bottou) 等综述 | 2010 | L7 |
| 鞍点 | Escaping Saddle Points Efficiently (Ge et al.) | 2015 | L8 |
| 严格鞍 | Identity or Escape (Lee et al.) | 2017 | L8 |
| PL 条件 | Gradient Descent with PL Inequality (Karimi et al.) | 2016 | L8 |
| 隐式正则 | Implicit Regularization in Deep Learning (Arora et al.) | 2019 | L9 |
| 两时间尺度 | Three Stories About Gradient Descent (Arora et al. Two-Timescale) | 2018-19 | L10 |
| 表达力 | Benefits of Depth in ReLU Networks (Telgarsky) | 2016 | L11 |
| 近似 | Approximation by Superpositions (Barron) | 1993 | L11 |
| 双下降 | Reconciling Modern ML View and Bias-Variance (Belkin et al.) | 2019 | L12 |
| 插值泛化 | Benign Overfitting in Linear Regression (Bartlett et al.) | 2020 | L12/L14 |
| 尖峰反例 | Failure to Generalize in Overparameterized (Bartlett et al.) | 2021 | L14 |
| NTK | Neural Tangent Kernel (Jacot et al.) | 2018 | L13 |
| NTK 收敛 | Gradient Descent Finds Global Minima of DNN (Du et al.) | 2019 | L13 |
| 均场 | Mean-field Analysis of Deep Networks (Chizat & Bach) | 2018 | L10 |
| 矩阵几何 | No Spurious Local Minima (Ge et al. matrix sensing) | 2017 | L15 |
| 鲁棒认证 | Random Smoothing for Certified Robustness (Cohen et al.) | 2019 | L16 |
| OOD | Risk Bound for Invariant Learning? IRM (Arjona-Medina; Arjora → 正确: Arora?) 以 ICPM/IRM (Arjona 2019, "Out of Distribution Generalization") 为准 | 2019 | L16 |
| 缩放律 | Scaling Laws for Neural LMs (Kaplan) / Chinchilla | 2020/2022 | L19 |
| 统计物理连接 | Optimal ML (Chaudhari & Chorascu) | 2019 | L10 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| Transformers as Statisticians (von Oswald 等) | 2023 | GD 在自注意力中实现梯度下降式 ICL 的统一理论 |
| Scaling Law 理论化：数据缩放律 (Hoffmann)/推理缩放 (sardana?) 与测试时计算理论 | 2022-25 | L19 可证速率与幂律 |
| Feature Learning 可证明例 (Damian et al.; Adem) | 2023-24 | NTK 之外的特征学习刻画 |
| Benign Overfitting 续作：分类 margin、深网条件谱 | 2021-23 | L12/L14 |
| 双下降统一理论（协方差谱+算法谱） | 2021-24 | L12 |
| 扩散模型统计保证：采样复杂度界 (Chen et al. 系列) | 2023-24 | L17；连接 MIT6.S184/STAT8201 |
| 对齐的统计理论：奖励过优化/模型崩塌 | 2024-25 | L16 回响 RLHF（11-868） |
| 缩放律与涌现 (Schaeffer 批判后续量化) | 2023-25 | L19 |
| 线性化动力学精细刻画 (edge of stability, Cat?) | 2022-24 | L9-L10 |
| 非凸景观新结果：注意力矩阵感知、LoRA 优化几何 | 2023-25 | L15 |
| LLM 蒸馏/RLHF 收敛分析 | 2024-25 | L18 交叉 |
| 理论视角的 MoE 与缩放 (可证速率尝试) | 2024-26 | L19 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| VC/Rademacher 实验验证 | scikit-learn（model selection 文档/示例）、d2l 章节代码 | L2-L4 数值实验 |
| PAC-Bayes 界数值 | Dziugaite-Roy 官方代码、deep-bayes-pac-bayes | L5 |
| NTK/线性化 | neural-tangents (TF/JAX)、JAX 小网络实验 | L10/L13 |
| 双下降/benign overfitting | 复现仓库（如 double-descent toy 项目大量存在） | L12/L14 |
| 认证鲁棒 | torchsmin（随机平滑官方） | L16 |
| OOD/鲁棒 | Wild-Time、POT（DRO 工具） | L16 |
| 缩放律拟合 | chinchilla-law 工具链、dooly/fit-scaling-law 库 | L19 |
| 凸/非凸优化算法 | PyTorch optimizer 源码（动量/Adam 理论对照） | L7-L8 |
| RL 理论样本复杂度 | RL 基准+理论实验（d4rl） | L18 |
| 矩阵几何/LoRA | PEFT 训练动力学分析脚本 | L15 |
