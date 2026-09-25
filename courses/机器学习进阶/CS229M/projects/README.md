# Stanford STATS214 / CS229M 配套项目计划

> 本轮只登记计划，不写代码；每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一执行。理论课项目定位：数值实验验证定理与反例。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2-L3 VC | Python | 随机二分计数估增长函数；验证半空间/阈值的 VC 维界 | `python growth_function.py` |
| L4 Rademacher | Python | 经验 Rademacher 复杂度蒙特卡洛估计 vs 泛化间隙散点 | `python rademacher.py` |
| L5 PAC-Bayes | Python + PyTorch | 训练小网并数值计算 PAC-Bayes 界（Dziugaite-Roy 简化） | `python pacbayes.py` |
| L6 速率 | Python (NumPy) | LinReg 的 MSE~d/n 速率实测；稀疏回归 Lasso 速率 | `python rates.py` |
| L7-L8 优化 | Python | GD/动量/SGD 在强凸与非凸玩具上的收敛率对比；扰动梯度逃鞍点 | `python opt_rates.py` |
| L9 隐式正则 | Python + PyTorch | 对角线性网络的 min-norm 验证；margin 最大化测量 | `python implicit_bias.py` |
| L10-L13 NTK | Python (JAX/PyTorch) | 有限宽 vs NTK 回归差异；边缘稳定性（edge of stability）实验 | `python ntk_vs_net.py` |
| L12-L14 双下降 | Python | LinReg 的 MSE 随 n/d 非单调曲线 + benign overfitting 条件检验 | `python double_descent.py` |
| L15 低秩几何 | Python + PyTorch | 矩阵感知的局部极小景观扫描；LoRA 训练动力学 | `python landscape.py` |
| L16 鲁棒/OOD | Python + PyTorch | 随机平滑认证半径；Wild-Time 风格偏移评估 | `python cert_robust.py` |
| L17 生成理论 | Python + PyTorch | Score 估计误差→Wasserstein 采样误差的玩具验证 | `python score_bounds.py` |
| L18 RL 理论 | Python | bandit/线性 MDP 样本复杂度实验与速率拟合 | `python rl_sample.py` |
| L19 缩放律 | Python + PyTorch | 小模型扫描拟合幂律，对比 Chinchilla 分配 | `python scaling_fit.py` |
| L20 期末 | Python | 选题示例：对齐奖励过优化的统计界复现；特征学习 vs NTK 区分实验 | `python final_project/main.py` |
