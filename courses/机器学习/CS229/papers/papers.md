# CS229 论文清单与开源生态映射

> 配套 notes/L01-L23 与 projects/。经典表按讲次排列（论文是"该讲的原始出处"），
> 近五年表（2021-2026）收录与 CS229 主题直接相关的后续演进；均为真实文献，已核对作者/venue。

## 1. 经典论文表（按讲次）

| 讲次 | 论文 | 贡献一句话 | 建议读法 |
| --- | | --- | --- |
| L03 | Cox 1958, *The regression analysis of binary sequences* (JRSS-B) | 逻辑回归的统计学奠基（logit 链接） | 只需知道出处，读现代教材版 |
| L04 | Nelder & Wedderburn 1972, *Generalized Linear Models* (JRSS-A) | GLM 统一框架原文 | 读引言与算法框 |
| L05 | Maron 1961, *Automatic indexing: An experimental inquiry* | 朴素贝叶斯用于文本检索的首次系统实验 | 配 Langley et al. 1994 (*Why "naive" Bayes works* 类讨论) |
| L05 | Ng & Jordan 2001, *On Discriminative vs. Generative Classifiers* (NeurIPS) | 生成 vs 判别的样本效率理论（收敛速率 O(1/m) vs O(log d/m)） | 全读，短 |
| L06-L07 | Boser, Guyon & Vapnik 1992, *A training algorithm for optimal margin classifiers* (COLT) | 最大间隔 + 核技巧原型（手写识别） | §1-2 + 算法 |
| L07 | Cortes & Vapnik 1995, *Support-Vector Networks* (MLJ) | 软间隔 SVM 标准形 | 全读（符号需映射到 Notes 版） |
| L07 | Platt 1998/1999, *Sequential Minimal Optimization*（微软 TR，收录于 Schölkopf 文集） | SMO：对偶 QP 的解析双变量分解 | §12.3（Chang & Lin 的 LIBSVM 实现更该读） |
| L07 | Aronszajn 1950; Kimeldorf & Wahba 1971 | RKHS 与表示定理（核方法的泛函分析底座） | 进阶选读 |
| L08 | Rosenblatt 1958, *The perceptron* (Psychological Review) | 感知机与收敛定理原始出处 | 读定理陈述即可 |
| L08 | Pearson 1901, *On lines and planes of closest fit...*; Hotelling 1933 | PCA（几何版/统计版） | 历史兴趣 |
| L10 | Vapnik & Chervonenkis 1971, *On the uniform convergence of relative frequencies...* (Dokl. Math.) | VC 维与一致收敛界 | 读陈述，证明看 Shalev-Shwartz 教材 |
| L10 | Blumer, Ehrenfeucht, Haussler & Warmuth 1989 (IPL) | PAC 可学 ⟺ VC 维有限 | 短论文 |
| L11 | Quinlan 1986, *Induction of decision trees* (MLJ) | ID3 / 信息增益 | 全读 |
| L11 | Breiman, Friedman, Olshen & Stone 1984, **CART**（专著） | 基尼 + 代价复杂度剪枝（§1.3 原始版） | ch.9-10 |
| L12 | Breiman 2001, *Random Forests* (MLJ) | bagging + 随机特征 = 森林；强度-相关界 | 全读，前 3 节 |
| L12 | Freund & Schapire 1997, *A decision-theoretic generalization of on-line learning...* | AdaBoost + 提升定理 | §1 + 定理 |
| L12 | Friedman 2001, *Greedy function approximation: A gradient boosting machine* (Ann. Stat.) | GBDT 与线搜索式步长 | 全读 |
| L12 | Chen & Guestrin 2016, *XGBoost* (KDD) | 二阶泰勒 + 显式叶正则 | §3 逐公式（p05 蓝本） |
| L12 | Ke et al. 2017, *LightGBM* (NeurIPS) | 直方图/Leaf-wise/GOSS | §4 工程 |
| L13 | Rumelhart, Hinton & Williams 1986 (Nature) | 反向传播 | 1 页短文 |
| L13 | Ioffe & Szegedy 2015, *Batch Normalization* (ICML)；Srivastava et al. 2014, *Dropout* (JMLR) | 现代训练两神器 | 各读动机节 |
| L13 | He et al. 2015/2016, *Delving deep into rectifiers* / *ResNet* (ICCV/CVPR) | 初始化方差守恒 + 残差 | He 2015 全读 |
| L15 | Hochreiter & Schmidhuber 1997, *Long Short-Term Memory* (Neural Comp.) | LSTM 原文（梯度消失动机） | 全读，短 |
| L15 | Vaswani et al. 2017, *Attention Is All You Need* (NeurIPS) | Transformer | 全读 + 配 p01 attention 扩展 |
| L16 | Lloyd 1982 (原 1957 TR), *Least squares quantization in clustering* | k-means 标准出处（IEEE TIT） | §1-2 |
| L16 | Arthur & Vassilvitskii 2007, *k-means++* (SODA) | D² 初始化与 O(log k) 近似 | 定理与算法 |
| L16 | Dempster, Laird & Rubin 1977, *Maximum Likelihood from Incomplete Data via the EM Algorithm* (JRSS-B) | EM 总纲（本讲全部推导的祖先） | 全读 |
| L17 | Kingma & Welling 2014, *Auto-Encoding Variational Bayes* (ICLR) | VAE + 重参数化 | §1-3 + 附录 B |
| L17 | Blei, Kucukelbir & McAuliffe 2017, *Variational Inference: A Review...* (JASA) | 变分推断综述（EM→VI 谱系） | 前 3 节 |
| L18 | Hyvärinen 1998 (*FastICA*, ICANN) / Hyvärinen & Oja 2000 (IEEE TNN) | ICA 算法与负熵理论 | FastICA 论文的迭代推导 |
| L18 | Shi & Malik 2000, *Normalized cuts and image segmentation* (TPAMI) | 谱聚类母论文 | §2-3 |
| L18 | Ng, Jordan & Weiss 2001/02, *On spectral clustering: Analysis and an algorithm* (NIPS) | 随机游走拉普拉斯版谱聚类（本讲符号版） | 全读，短 |
| L18 | Liu, Ting & Zhou 2008, *Isolation Forest* (ICDM) | 树集成做异常检测（L12×L18 合流） | 全读 |
| L19 | Rabiner 1989, *A tutorial on HMMs* (Proc. IEEE) | 前向/后向/Viterbi/Baum-Welch 最清晰教程 | §2-3（p09 蓝本） |
| L19 | Geman & Geman 1984; Metropolis et al. 1953; Hastings 1970 | Gibbs/MCMC 三件套 | 配合 p09 |
| L20 | Bellman 1957（专著）；Howard 1960, *Dynamic Programming and Markov Processes* | DP 与策略迭代原始 | 历史兴趣 |
| L21 | Watkins & Dayan 1992, *Q-learning* (ML) | Q-learning 与收敛定理 | §2-3 |
| L21 | Kalman 1960, *A new approach to linear filtering and prediction problems* | LQR/控制线（Riccati 现代版） | 选读 |
| L22 | Rosenblatt 1956 / Parzen 1962 | KDE 原始（随机逼近视角） | 读陈述 |
| L22 | Neal 1996, *Priors for infinite networks* (NIPS) / Rasmussen & Williams 2006（书） | NN→GP 极限与 GP 教材 | 书 ch.2 |
| L22 | Schapire & Singer 1999, *Improved boosting schemes using a tighter bound...* (COLT) | boosting 间隔理论 | 选读 |
| L23 | Abbeel, Coates & Ng 2010, *Autonomous helicopter flight via reinforcement learning*（IJRR；另见 Ng et al. 2006 *Policy search for autonomous helicopter flight*） | 课程招牌项目原始论文 | 全读——L23 模板出处 |
| 生态 | Pedregosa et al. 2011, *scikit-learn: ML in Python* (JMLR) | API 哲学的论文化表述 | 引言+接口节 |

## 2. 近五年论文表（2021-2026，与讲次主题对应）

| 讲次关联 | 论文 | 为什么值得读 |
| --- | --- | --- |
| L12 表格模型 | Grinsztajn, Oyallon & Varoquaux 2022, *Why do tree-based models still outperform deep learning on tabular data?* (NeurIPS D&B) | 给"表格默认 GBDT"（L12 §1.3）第一次严肃实证回答；代码随论文 |
| L12/L04 新基线 | Hollmann, Müller, dos Santos & Hutter 2023, *TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second* (ICLR) | 先验数据拟合网络挑战 GBDT 默认地位（表格 Transformer 线开端） |
| L12 生态 | Prokhorenkova & Gorsky 2020 (NeurIPS), *Boost then convolve: gradient boosting with priors...* 及 CatBoost 系列（Prokhorenkova et al. 2018 ECML） | ordered boosting 显式处理"目标泄漏"（L11 陷阱 3 的解法）；sklearn 1.x `HistGradientBoosting` 的动机文献 |
| L13/L14 优化 | Liu et al. 2023, *Machine Learning in a Liver: Heuristic Search of Optimizer Designs using A100 GPUs*（LION, arXiv 2302.06671） | Adam 之后"优化器也是搜索对象"的现代案例（L02 GD 家族的进化树） |
| L15 架构 | Liu et al. 2021, *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows* (ICCV) | CNN 局部先验回流 Transformer（L15 "架构=归纳偏置"的最新证据） |
| L15 生态 | Touvron et al. 2023, *LLaMA: Open and Efficient Foundation Language Models* (arXiv 2302.13971)；后续 LLaMA-2/3 报告（2023-2025） | 用开源技术报告复现 §1.3 全部训练配方（Pre-LN/warmup/调度器） |
| L17 生成 | Song, Sohlberg... 2021, *Score-Based Generative Modeling through Stochastic Differential Equations* (ICLR)；Ho, Jain & Abbeel 2020, *Denoising Diffusion Probabilistic Models* (NeurIPS) | VAE/ELBO 之外的生成主线；与 L16 去噪分数视角可对照（score matching = 无归一化 MLE） |
| L19 图模型 | Jang, Gu & Poole 2017, *Categorical Reparameterization with Gumbel-Softmax* (ICLR)；回看 Grover 等 2022 *High-Precision Differentiable Greedy* 线（Argmax 可微化） | 离散隐变量梯度的现代补丁（L19 Gibbs 的可微替代） |
| L20-L21 RL | Hafner et al. 2023, *Mastering Diverse Domains through World Models (DreamerV3)* (arXiv 2301.04104；2025 Nature 版) | "学到的模型 + 值迭代"即 L20 GPI 的端到端现代版；单套超参的鲁棒性叙事 |
| L21 RL 应用 | Chen et al. 2021, *Decision Transformer: Reinforcement Learning via Sequence Modeling* (NeurIPS) | 把 RL 重写成 L15 序列建模——图模型/架构/控制三线合流 |
| 生态工具 | McIntosh et al. 2024/2025, *MLX: A Flexible and Lightweight Framework for Machine Learning Research*（Apple, arXiv 2312.11903 及后续版本） | numpy 风格统一内存模型——本仓库 p01-p09 实验在 Apple Silicon 的官方载体 |
| 生态工具 | Optuna: Miyaki et al. 2023, *Optuna: A Next-generation Hyperparameter Optimization Framework*（回看 Akiba 2019 KDD） | L14 §1.3 超参搜索（TPE/ASHA）的开源标准 |

> 注：scikit-learn `HistGradientBoosting*`（1.0 引入、1.4+ `monotonic_cst` 扩展）无独立论文，
> 其方法与实验依据见 LightGBM(Ke 2017)、CatBoost(Prokhorenkova 2018)、HGB 的 sklearn 文档与 issue RFC，
> 以及 Grinsztajn 2022 的横向评测。

## 3. 知识点 ↔ 开源项目映射表

| CS229 知识点 | 讲次 | 首选开源实现 | 关键类/函数 | 备注 |
| --- | --- | --- | --- | --- |
| 线性回归/正规方程 | L02 | numpy / sklearn | `np.linalg.lstsq`、`Ridge(CV)` | 永不 `inv`；sklearn 走 SVD |
| GD/SGD/动量 | L02-L03 | numpy / sklearn | `SGD(loss='squared_error')` | p01 手写对照 lr/动量 |
| 逻辑回归/交叉熵/牛顿 | L03 | sklearn / statsmodels | `LogisticRegression(newton-cholesky)`、`GLM` | IRLS 可读 statsmodels 源码 |
| GLM/Poisson | L04 | sklearn / statsmodels | `TweedieRegressor(power=1)`、`glm()` | 链接/族对象 = 本讲公式 |
| GDA/朴素贝叶斯/LDA | L05 | sklearn | `GaussianNB`、`MultinomialNB`、`LinearDiscriminantAnalysis` | 注意其默认判别式解法 |
| SVM/对偶/核 | L06-L07 | sklearn / LIBSVM | `SVC(kernel, C, gamma)`、`NuSVC`、`KernelRidge` | 大数据：`LinearSVC`/`SGD(hinge)` |
| PCA | L08/L18 | sklearn | `PCA(svd_solver='randomized')`、`IncrementalPCA` | 白化/解释方差直接可用 |
| 偏差-方差/正则/交叉验证 | L09 | sklearn | `learning_curve`、`RidgeCV`、`KFold` | p02 复刻其曲线 |
| VC/间隔理论 | L10 | —（研究代码） | 蒙特卡洛打碎计数玩具（numpy 20 行） | 见 notes 第 5 节 |
| 决策树/剪枝 | L11 | sklearn | `DecisionTreeClassifier(ccp_alpha=)`、`export_text` | `ccp_alpha` = CART 的 α |
| 随机森林/bagging | L12 | sklearn | `RandomForestClassifier(oob_score=True)` | OOB 免费验证集 |
| AdaBoost/GBDT | L12 | sklearn/xgboost/lightgbm/catboost | `AdaBoostClassifier`、`HistGradientBoosting*`、`xgb.train` | 表格数据军备竞赛主场 |
| 特征重要性/解释 | L12/L23 | SHAP | `TreeExplainer` | TreeSHAP = 集成定理的工程红利 |
| MLP/反向传播 | L13 | sklearn 起步 | `MLPClassifier` → PyTorch/JAX/MLX | p01 扩展：numpy 两隐层 |
| 训练工程/调参 | L14 | PyTorch Lightning / MLflow / W&B / Optuna | `Trainer`、`mlflow.log_params`、`optuna.create_study` | 可复现四件套 |
| CNN/RNN/Transformer | L15 | torchvision/timm / HF transformers | `ResNet`、`AutoModel`、`pipeline` | 概念对照表见 notes |
| k-means/MoG/EM | L16 | sklearn | `KMeans`、`GaussianMixture(covariance_type=)` | 从 spherical 滑到 full 即"从 k-means 滑向 MoG" |
| 因子分析 | L17 | sklearn | `FactorAnalysis` | EM 迭代数/噪声方差全暴露 |
| VAE | L17 | PyTorch/diffusers | `AutoencoderKL`（SD 压缩 VAE） | numpy 不可行，读源码即可 |
| ICA/盲源分离 | L18 | sklearn | `FastICA` | 符号/顺序不可辨识要"对齐" |
| 谱聚类 | L18 | sklearn | `SpectralClustering(affinity='rbf')` | σ 决定一切（L18 陷阱 2） |
| 异常检测 | L18/L22 | sklearn | `EllipticEnvelope`、`IsolationForest`、`KernelDensity` | 马氏/森林/密度三路对照 |
| HMM/Baum-Welch/Viterbi | L19 | hmmlearn | `GaussianHMM` | sklearn 已移除 HMM 至 hmmlearn |
| 贝叶斯网/Gibbs/NUTS | L19 | pgmpy / PyMC / NumPyro | `DiscreteBayesianNetwork`、`pm.sample` | p09 手写版与其自相关图对照 |
| 值迭代/策略迭代/Q-learning | L20-L21 | Gymnasium + numpy | `frozen_lake.FrozenLakeEnv(.P)` | p08 直接读 env 转移张量 |
| DQN/现代 RL | L21 | stable-baselines3 | `DQN`、`PPO` | buffer/tau/双 Q 逐参数对应陷阱 |
| LQR/Riccati | L21 | scipy / control | `scipy.linalg.solve_discrete_are` | 与 p08 网格贪心互证 |
| 高斯过程/贝叶斯优化 | L22 | GPyTorch / BoTorch / skopt | `GPRegression`、`optimize_acqf` | 调参科学化（L14 闭环） |
