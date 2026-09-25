# CMU 10-708 配套项目计划

> 本轮只登记计划，不写代码；每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一执行。对应课程 homework 主题。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2-L4 表示 | Python | d-分离判定器 + 从 DGM/UGM 生成因子图并可视化 | `python dseparation.py` |
| L5-L6 精确推断 | Python | 手写 VE 与 junction tree 计算器，对比诱导宽度耗时 | `python ve_jt.py` |
| L7 MAP | Python (C++ 可选) | 子模能量图割求解 vs 局部松弛；最大权独立集对照 | `python map_graphcut.py` |
| L9-L10 变分与结构化 | Python | mean-field/CAVI 解 Ising + CRF 词性标注小系统 | `python vi_meanfield.py` / `python crf_pos.py` |
| L11-L12 MCMC | Python | 手写 Gibbs/Hastings、实现简化 HMC，在 GMM 后验对比混合 | `python mcmc_bench.py` |
| L13-L14 EM | Python | GMM 的 EM 与 VEM 实现、坍缩演示 | `python em_gmm.py` |
| L15-L16 结构学习 | Python | PC 算法 + BDeu 贪心搜索在小 DAG 上对比真图 | `python structure_learn.py` |
| L17 因果 | Python (R 可选) | 后门判据 ATE 估计；模拟混杂数据 | `python causal_ate.py` / R 版 `Rscript causal.R` |
| L18 时序 | Python | HMM 三问题 + 卡尔曼/粒子滤波轨迹跟踪 | `python kalman_pf.py` |
| L19 RL 推断 | Python | soft value iteration 与 PI²-Control 在倒立摆玩具环境 | `python rl_inference.py` |
| L20 VAE | Python + PyTorch | 分层 VAE 于 MNIST；后验坍缩诊断与退火 | `python train_hvae.py` |
| L21 GP | Python | GP 回归前后验可视化 + 诱导点稀疏化 | `python gp_sparse.py` |
| L22-L23 DP/IBP | Python | CRP 采样无限高斯混合；IBP 伯努利矩阵推断 | `python crp_gmm.py` / `python ibp_bernoulli.py` |
| L24 综合项目 | Python | 选题示例：把扩散模型写成潜变量图并实现 EM 风格推断 | `python final_project/` 入口脚本 |
