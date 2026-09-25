# U Toronto STA 4273 配套项目计划

> 本轮只登记计划，不写代码；每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一执行。本课数学密度高，项目以"实验验证定理"为导向。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2 蒙特卡洛 | Python | 重要性采样/分层采样在可算目标上的方差对比表 | `python mc_variance.py` |
| L3 两恒等式 | Python | 同一高斯期望的 score vs pathwise 梯度估计器，方差-偏差曲线 | `python grad_identities.py` |
| L4 基线约简 | Python | REINFORCE：无基线/均值基线/最优基线/leave-one-out 对比 | `python rl_baseline.py` |
| L5 重参数化代数 | Python | 手写截断正态/Gamma 重参数化采样器与一致性检验 | `python reparam_dist.py` |
| L6 离散梯度 | Python + PyTorch | VAE 离散潜变量：STE/Gumbel-τ/精确梯度三方对比（训练+ELBO 质量） | `python discrete_vae.py` |
| L7 变分目标 | Python + PyTorch | α-divergence/IMSELBO 在小模型上的梯度噪声对比 | `python vi_objectives.py` |
| L8-L9 控制对偶 | Python | 1D 双井势自由能：相对熵控制求解；验证与反向 SDE 等价 | `python rec_control.py` |
| L10 序贯推断 | Python | FFBS 粒子平滑：梯度估计的滤波版实现 | `python ffbs_grad.py` |
| L11 自然梯度 | Python + PyTorch | Fisher 度量下比较 SGD/自然梯度（KFAC）对期望目标的收敛 | `python nat_grad.py` |
| L12 扩散回响 | Python + PyTorch | 证明 ε-损失与 score-matching 损失的恒等式并在 MNIST 验证 | `python score_vs_eps.py` |
| 期末综合 | Python | 选题示例：GRPO 基线=控制变量的实验分析；路径积分控制+神经网络值函数 | `python final_project/main.py` |
