# projects/ — UCB EE C126 配套小项目计划（本轮只列计划，不写代码）

语言：**Python + Jupyter Notebook**（与 Walrand 教材官方 notebook 一致），排队/仿真部分用纯 Python 脚本即可。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L1–L2 公理与贝叶斯 | Python | `bayes_medical_test.py`：不同基率/灵敏度下的后验概率扫描，画 ROC | `python bayes_medical_test.py` |
| L3–L6 离散 RV | Python | `indictor_counting.py`：随机排列不动点、哈希冲突数的指示器法期望 vs 蒙特卡洛 | `python indictor_counting.py` |
| L7–L8 极限定理 | Python | `lln_clt_lab.ipynb`：n 递增时样本均值分布收窄，验证 CLT 与 1/√n | `jupyter nbconvert --execute lln_clt_lab.ipynb`（或直接打开运行） |
| L9–L12 连续 RV 与变换 | Python | `rv_transform.py`：逆变换抽样生成指数/柯西样本，数值验证雅可比换元 | `python rv_transform.py` |
| L13 MMSE 与滤波 | Python | `mmse_kalman.py`：手写一维 Kalman 滤波跟踪噪声轨迹，对比 MMSE 理论值 | `python mmse_kalman.py` |
| L15–L17 马尔可夫链 | Python | `pagerank_lab.py`：从邻接矩阵构造随机矩阵，幂迭代求平稳分布并与 `numpy.linalg.eig` 对拍，算谱隙 | `python pagerank_lab.py` |
| L18 泊松过程 | Python | `poisson_arrival.py`：生成非齐次泊松到达流，检验间隔指数性与合并/稀释性质 | `python poisson_arrival.py` |
| L19 鞅与随机行走 | Python | `gambler_ruin.py`：赌徒破产吸收概率数值解 vs 理论公式；Azuma 界松紧 | `python gambler_ruin.py` |
| L20 排队论 | Python | `mm1_sim.py`：离散事件仿真 M/M/1，验证 Little 定律与利用率-延迟关系 | `python mm1_sim.py --rho 0.9` |
| L21–L23 估计与检验 | Python | `mle_testing.py`：高斯/泊松 MLE、CRLB 曲线、N–P 最优检验与似然比 ROC | `python mle_testing.py` |
| L24 HMM | Python | `viterbi_digit.py`：小型连续数字识别（合成特征），实现前向算法 + Viterbi | `python viterbi_digit.py` |
| L25 MDP | Python | `gridworld_bellman.py`：4×4 网格上值迭代/策略迭代，观察 Bellman 算子收敛 | `python gridworld_bellman.py` |

约定：
- 依赖见 `projects/requirements.txt`（numpy、scipy、matplotlib、pandas、jupyter）；
- 每个文件顶部注明对应讲次与教材章节，随机种子固定以便复现；
- **本轮不写代码、不编译**，由用户后续集中执行。
