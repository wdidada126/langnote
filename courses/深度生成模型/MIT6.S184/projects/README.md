# MIT 6.S184 配套项目计划

> 本轮只登记计划，不写代码；后续每个小项目独立目录 + 独立 build 脚本，最后集中编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L2 概率与DL基础 | Python | 2D 高斯混合分布的采样与极大似然拟合小实验 | `pip install -r requirements.txt && python main.py` |
| L3 ODE/CNF | Python + PyTorch | 1D→2D 双月玩具数据的连续标准化流（学速度场 + trace 散度） | `python cnf_toy.py`（依赖 torchdiffeq） |
| L4-L5 SDE/Score | Python + NumPy | Euler-Maruyama 模拟 OU 前向 SDE，验证 Fokker-Planck 边缘分布 | `python sde_sim.py` |
| L6 DDPM | Python + PyTorch | 从零实现 MNIST 扩散模型（加噪闭式、ε 预测损失、反向采样）——即课程 Lab 1 | `python train_ddpm.py && python sample.py` |
| L7 SDE 统一框架 | Python + PyTorch | 同一模型切换 VP/VE-SDE 与概率流 ODE 采样对比 | `python unified_sde.py` |
| L8 采样加速 | Python + PyTorch | DDIM 步数-质量曲线实验 + classifier-free guidance 演示（Lab 2） | `python ddim_scan.py` |
| L9 Flow Matching | Python + PyTorch | OT-CFM 在 8 高斯环流上的 2D 生成 + rectified flow 一轮重直线化 | `python flow_matching.py` |
| L10 综合实验 | Python + PyTorch | 课程 Lab 3：图像数据集上训练小型 UNet 扩散/流模型并 FID 评估 | `python train_unet.py --model {ddpm,cfm}` |
| L11-L12 应用 | Python | 复现 Diffusion Policy 简化版（Push-T 环境 1D 版）或分子二面角扩散 | `python policy.py` / `python dihedral_diffusion.py` |
