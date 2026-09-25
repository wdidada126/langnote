# CS229 配套项目总表（projects/）

> 语言：Python；**唯一第三方依赖 = numpy**（各源码注释中已声明）。
> 数据全部合成（`default_rng(seed)` 可复现），本轮只写不编译：
> `run.sh` / `run.bat` 第一步均为 `python -m py_compile` 语法自检，随后逐文件运行。
> 终端输出即报告（表格 + ASCII 曲线），不引入 matplotlib；需要出版级图时按各 README
> "可扩展实验"接 matplotlib 即可。

| 项目 | 讲次 | 内容 | 文件 | 运行 |
| --- | --- | --- | --- | --- |
| `p01_linear_logistic` | L01-L03 | LMS/GD/SGD/正规方程与数值解法；交叉熵/Newton-IRLS；**学习率×动量实验**（含 α>2/L 发散） | `common.py` `linear.py` `gd_momentum.py` `logistic.py` | `bash run.sh` |
| `p02_regularization_bias_variance` | L04/L09 | 多项式容量/λ 扫描/学习曲线/KFold；B-V 恒等式蒙特卡洛逐项验证 | `poly_ridge.py` `bv_decomp.py` | `bash run.sh` |
| `p03_lda_naive_bayes` | L05 | GDA=LR 殊途同归、QDA 方差反噬；NB 平滑扫描/零概率/下溢 | `gda_qda.py` `naive_bayes.py` | `bash run.sh` |
| `p04_svm` | L06-L07 | hinge 次梯度 + 感知机对照；**简化 SMO**（核化对偶、KKT 角色统计，玩具复杂度 O(m³) 级已标注） | `hinge_sgd.py` `smo_toy.py` | `bash run.sh` |
| `p05_trees_forest` | L11-L12 | 纯 numpy CART（基尼/熵、ccp 后剪枝）+ 随机森林/OOB + AdaBoost 桩 + 迷你 GBDT | `tree.py` `ensemble.py` | `bash run.sh` |
| `p06_clustering_em` | L16-L17-L22 | k-means(k++/单调性/违约演示)；GMM-EM(球形极限≡k-means/BIC)；FA-EM(主角度)；KDE 带宽 | `kmeans.py` `em_gmm.py` `fa_kde.py` | `bash run.sh` |
| `p07_pca` | L08-L18 | PCA 双路径/中心化/白化/×k-means 协同；FastICA 鸡尾酒会；谱聚类 σ 扫描 | `pca.py` `ica_spectral.py` | `bash run.sh` |
| `p08_rl_gridworld` | L20-L21 | 自建网格 MDP：值迭代/策略迭代（同解验证）→ Q-learning（衰减/ε₀/学习曲线/胜率） | `gridworld.py` `qlearn.py` | `bash run.sh` |
| `p09_gibbs` | L19 | HMM 前向后向(log域)+Viterbi+Baum-Welch；Gibbs：GMM 标签链 + Ising(临界慢化/ESS) | `hmm.py` `gibbs.py` | `bash run.sh` |

## 跨项目复用关系
```
p01 common.py ──> p03 gda_qda.py（数据 + Newton-IRLS）
p06 kmeans.py ──> p06 em_gmm.py / p07 ica_spectral.py / p07 pca.py（k-means 与一致率工具）
p06 kmeans 数据 ─> p06 fa_kde.py（同主题：混合/子空间）
```

## 与 notes 的对应
每讲笔记第 1 节公式 → 对应项目 README"观察点"给出可数值验证的条目；
"可扩展实验"即 L23 迷你报告选题库。
