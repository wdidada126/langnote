# papers.md — MacKay 信息论、模式识别与神经网络文献

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Shannon, *A Mathematical Theory of Communication* | 1948 | 熵、信道容量与两大编码定理，全课程的根 | L4, L9, L10 |
| MacKay, *Information-based Objective Functions for Training Belief Networks* | 1992 | 把信息论目标用于网络训练，沟通推断与学习 | L23, L24 |
| Mackay, *Information Networks for Nonlinear Blind Signal Separation* | 1995 | 信息最大化做盲源分离，ICA 路线的起点之一 | L30 |
| MacKay, *A Bayesian Methods Workshop / Ensemble Learning*（MacKay 等, Neural Computation） | 1995–1999 | 集成学习与贝叶斯视角下的经验性洞察：多模型平均优于单模型 | L23, L26 |
| MacKay & Neal, *Near Shannon Limit Performance of Low Density Parity Check Codes* | 1995/1996 | 复活 Gallager 的 LDPC 并证明可逼近信道容量 | L15, L21 |
| Neal & Hinton, *A New View of Statistical Inference that is Partially Bayesian and Partially Frequentist* | 1998 | 最小二乘视角统一推断与学习，自由能分解的解释 | L37 |
| Pearl, *Reverend Bayes on Inference Engines: A Historical Introduction to Bayesian Networks* | 1982 | 贝叶斯网与消息传递（信念传播）的起源 | L17, L18 |
| Dempster, Laird & Rubin, *Maximum Likelihood from Incomplete Data via the EM Algorithm* | 1977 | EM 算法系统化，L29 的直接来源 | L29, L31 |
| Metropolis et al., *Equation of State Calculations by Fast Computing Machines* | 1953 | MCMC 起点，为不可解积分提供随机方案 | L21 |
| Vitter, *Arithmetic Coding / Optimal Prefix Codes*（及 Rissanen 的算术编码） | 1976–1987 | 算术编码让实际压缩逼近熵 | L7 |
| Berrou, Glavieux & Thitimajshima, *Near Shannon Limit Error-Correcting Coding and Modulation: Turbo-Codes* | 1993 | Turbo 码开启迭代译码时代 | L14 |
| Gallager, *Low-Density Parity-Check Codes*（博士论文/专著） | 1963 | LDPC 原始构造与稀疏图译码分析 | L15 |
| Hinton, Osindero & Teh, *A Fast Learning Algorithm for Deep Belief Nets* | 2006 | 变分/信度传播式逐层训练，深度学习复兴的数学底座之一 | L26, L37 |
| Rabiner, *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition* | 1989 | HMM 三算法的工程标准化 | L31 |
| Bell & Sejnowski, *An Information-Maximization Approach to Blind Separation* | 1995 | 信息最大化 ICA 与神经科学动机 | L30 |

> 注：表中有一条为编者整理时的合并条目（MacKay 的集成学习与复杂度相关论文），精读前请核对原始出处与年份；其余条目为可直接检索的标准文献。

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| 5G-Advanced/6G 信道编码演进论文（LDPC 度分布优化、URLLC 短码性能） | 2021–2025 | LDPC 在短包低时延场景继续逼近有限码长界 | L15, L10 |
| 深度学习辅助物理层（DeepJSCC、神经网络译码器、学习型调制） | 2021–2025 | 用网络近似最优联合编码调制，突破分离架构 | L14–L16, L33 |
| 扩散模型作为消息传递/变分推断的连续化（score SDE 与自由能视角） | 2021–2024 | ELBO/变分下界成为生成模型训练目标的核心 | L26, L29, L37 |
| GNN 作为图上近似推断（amortized BP / 神经 belief propagation） | 2021–2025 | 把和积算法可学习化，处理带环图 | L18, L20, L27 |
| LLM 的压缩视角：*Language Modeling Is Compression*（Delétang 等） | 2023 | 证明预测能力与压缩率在算术编码意义下等价 | L2, L7, L23 |
| 有限码长与信息几何在短包通信中的应用（Polyanskiy 学派的后续） | 2021–2024 | 把 Shannon 渐近界细化到块长 n 的可达界 | L9, L10 |
| 贝叶斯深度学习可扩展近似推断（变分/蒙特卡洛混合，SVI on GPU） | 2021–2025 | 把 L21/L26 的方法推到十亿参数规模 | L21, L26 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 熵与 Huffman | `zstd`（FSE/Huffman 后端）, `libvpx`, `brotli` | 无损压缩的最终熵编码阶段 |
| 算术编码 / 上下文建模 | `libaom`（AV1 的 ML 熵编码）, `OpenEXR` | 视频/图像编码的近熵比特打包 |
| LDPC / Turbo 译码 | `srsran/srsRAN_4G`（5G NR LDPC 链路）, `libfec` | 基带 PHY 的软判决迭代译码 |
| 因子图与信念传播 | `pgmpy`, `gtsam`（Borg Lab 因子图 SLAM） | 概率图推断、机器人同时定位与建图 |
| 变分推断 / ELBO | `PyMC`, `stan-dev/stan`（ADVI）, `scikit-learn`（变分高斯混合） | 后验近似、模型证据下界 |
| EM / 混合模型 | `scikit-learn`（`GaussianMixture`）, `hmmlearn` | 聚类、密度估计、序列模型 |
| MCMC / HMC | `stan-dev/stan`（NUTS）, `blackjax-devs/blackjax`, `pymc-devs/pymc` | 不可解积分的高精度采样 |
| ICA / 稀疏编码 | `scikit-learn`（`FastICA`, `DictLearning`）, `mne-tools/mne-python` | 盲源分离、脑电去伪迹、特征学习 |
| PCA / 低秩 | `scikit-learn`, `facebookresearch/faiss` | 降维、向量索引前置变换 |
| 神经网络与反向传播 | `pytorch/pytorch`, `jax-ml/jax`, `tensorflow/tensorflow` | 计算图 + 链式法则的工业实现 |
| 混合密度 / 生成模型 | `tensorflow/probability`（分布与 VI 工具） | 多峰条件密度建模 |
| 信息论度量 | `scikit-learn.metrics`（log loss、`mutual_info_score`）, `arviz` | 模型评分、特征选择、后验比较 |
