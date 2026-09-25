# CMU 10-708 讲义骨架（outline）

> 骨架级要点；填充时对照 K&F 教材章节与官网 notes 推导定理证明。

## L1 导论
- 图模型=概率分布的图语言：用稀疏依赖结构对抗维度灾难
- 三问题框架：表示、推断、学习——全课目录
- 应用史：语音/视觉/生物信息/对话系统；与深度学习的现代关系
- 记号约定：随机变量、势函数、指数簇

## L2 贝叶斯网络
- DGM 语义：局部马尔可夫性、祖先/后代、链式分解 p(x)=∏p(xi|pa_i)
- d-分离定理：独立性判定的图算法（ Moralization / Bayes-ball）
- v-结构（对撞）的非直观行为：explaining away
- 例：朴素贝叶斯、专家系统、因果图入门

## L3 马尔可夫网络
- Hammersley-Clifford 定理：正分布 ↔ 团势分解
- 参数化：log-linear、Ising/Potts、伪似然
- I/II/III 型马尔可夫性；与 DGM 的相互表达（多树 DGM）
- 例：纹理建模、约束满足

## L4 因子图与独立结构
- 因子图统一 DGM/UGM：变量节点×因子节点
- 条件独立的三种图判据一致化；消除图与填充
- 诱导宽度 = 推断复杂度之根
- 部分定向图（PDAG）与 Amb 图：混合模型独立性

## L5 精确推断：VE 与 BP
- 变量消除：动态规划视角、复杂度=诱导宽度
- sum-product 信念传播：树上精确、图上迭代
- 环上 BP 的收敛条件（对角占优）与高斯 BP
- 与 max-sum 的平行结构

## L6 Junction Tree
- 团树构造：三角化→极大团→SEP 分割集
- clique potential 吸收、collect/distribute 两趟消息
- Shafer-Shenoy vs HUGIN 参数化；存储与数值问题
- 精确推断的工程实现与查询复用

## L7 MAP 推断
- 图上最长路径/最小割：子模二元势的 graph-cut 解
- LP 松弛：MRRF/local polytope、对偶分解（MAP-ADMM）
- 树加权松弛（TWS）与局部搜索
- 复杂性与近似难度（APX-hard 视角）

## L8 MRF 参数化与最大熵
- 指数族：充分统计量、配分函数 A(θ) 的核心地位
- 最大熵对偶：矩匹配与自然参数
- 矩匹配/伪似然/MCMC 似然近似（Boltzmann 机对比散度）
- 平均场自由能与变分界预告

## L9 变分推断
- ELBO 推导：log p ≥ E_q[log p] - KL(q||p)；三等价形式
- mean-field 分解与坐标上升更新
- CAVI/FactorVA：结构约束下的变分族
- 与 EM 的关系；预告 amortized（L20 VAE）

## L10 结构化预测
- 判别式模型：最大熵、CRF（链式/格状）与对数配分
- 结构化感知机、结构化 SVM 与切割平面
- 平均结构/参数估计；松弛与近似解码
- 应用：NER、语义分割

## L11 蒙特卡洛与 MCMC 基础
- MC 估计方差与 CLT；重要性采样与权重退化
- Gibbs 采样与 Metropolis-Hastings：细致平衡定理
- Potts 采样、并行回火
- 何时 MCMC 可行/不可行（混合时间概念预告）

## L12 MCMC 进阶
- 混合时间、耦合从与自混合界（简介）
- HMC：测度-动量、 leapfrog、接受率；NUTS 自适应
- 连续松弛与梯度方法连接 GAN/扩散的直觉
- Stan/PyMC 实践要点与诊断（R-hat、ESS）

## L13 有向模型参数学习
- MLE 与贝叶斯 MAP：完全数据分解
- 共轭先验：Dirichlet-Multinomial、Normal-InverseWishart
- 等价样本量与先验设计
- 缺失数据的困难：潜变量使似然不可分解（引出 L14）

## L14 EM 与潜变量模型
- EM 的 Jensen/ELBO 双推导；单调收敛保证
- GMM、隐因子模型、mixtures of experts
- 变分 EM：推断用 q 替代精确后验
- 失败模式：局部最优、坍缩；annealed EM

## L15 结构学习：评分与约束
- BDeu/BIC/BIC-based score decomposition；结构先验
- GES 贪心等价搜索、K2 链
- 约束方法：PC/IC 算法、分离集与 v-结构定向
- 两派对比 + 因果可识别性初步

## L16 结构学习进阶
- DAG 空间组合优化：order search、DynDAG
- 等价类计数与 Chickering 定理
- 高维一致性、ℓ1 正则结构学习（与图模型选择）
- 基准数据与实践陷阱（score 噪声、搜索退化）

## L17 因果推断
- Pearl 三元组：关联/干预/反事实；do-calculus 三规则
- 后门/前门判据与识别公式
- 因果发现与图模型学习的关系（FCI）
- 工具变量与 ATE 估计概览

## L18 时序与动态模型
- HMM：滤波/平滑/Viterbi 三问题与 Baum-Welch
- 卡尔曼滤波与 LDS：高斯推断的递推代数
- DBN/SLDS：非线性滤波、EKF/UKF 直觉
- 粒子滤波预告（连接控制推断）

## L19 图模型与强化学习
- 因果图视角的 MDP/部分可观测：滤波即推断
- RL as probabilistic inference：最大熵对偶与 soft value
- 相对熵逆控制（REIC）、路径积分（PI²-Control）
- 逆 RL：最大熵 IRF（Abbeel/Ng、Ziebart 线）

## L20 深度潜变量模型
- VAE 完整推导：amortized 编码、重参数化、后验坍缩
- 深度 latent variable model：分层潜变量、DILVA/扩散模型=时间潜变量链
- 与图模型的对应：DGM 骨架+神经网络势函数
- NPE/normalizing flow 与推断网络族；评估困惑度陷阱

## L21 高斯过程
- 核函数=先验平滑性假设；GP 回归闭式后验
- GP 分类：拉普拉斯/变分/预测似然（EP 连接 L9）
- 稀疏 GP：诱导点 Nystrom 近似与复杂度
- 深度学习联系：无限宽网络 = NTK/GP

## L22 Dirichlet 过程
- DP 定义：有限维分布一致性、CRP  stick-breaking
- Dirichlet 过程混合模型：聚类数自动确定
- Gibbs/聚焦-不集中采样与折叠构造
- 主题模型 LDA：plate notation 规范

## L23 IBP 与非参数因子模型
- Indian Buffet Process：泊松-伽马构造、后验
- beta 过程与重叠聚类、潜在特征学习
- 非参数矩阵补全/事实分解应用
- 与深度表示学习的联系（特征选择）

## L24 总结与前沿
- 知识地图：表示→推断→学习→因果 四轴线
- 图模型在 LLM 时代的位置：扩散=潜变量链、注意力=完全图势、推理=图上规划
- 现代混合：神经符号、图神经网络=消息传递/ BP 推广
- 项目/考试复盘与延伸阅读清单
