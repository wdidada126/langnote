# Columbia STAT 8201 配套项目计划

> 本轮只登记计划，不写代码；每项目独立目录 + 独立 build 脚本，集中编译由用户后续统一执行。研讨班特色：每个项目附带一份"论文领读报告"。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L2 自回归 | Python | 像素级自回归（含排列平均）建模 2D 玩具数据并算精确 NLL | `python ar_nll.py` |
| L3-L4 VAE | Python + PyTorch | MNIST 标准 VAE → IWAE 收紧界 → 分层 VAE，报告后验坍缩 | `python train_vae.py --model {vae,iwae,hvae}` |
| L5 Flow | Python + PyTorch | RealNVP/Glow 在 2D 环形流上训练，画密度演化 | `python flow_2d.py` |
| L6-L7 GAN | Python + PyTorch | DCGAN→WGAN-GP 模式覆盖对比；StyleGAN2 推理复现语义操控 | `python train_gan.py` / StyleGAN2 官方 `python torch_run.py` |
| L8 EBM | Python + PyTorch | 短朗之万链 EBM 玩具密度 + InfoNCE 对比小实验 | `python ebm_toy.py` |
| L9 MCMC 生成 | Python | Langevin/吉布斯采样器对比得分匹配采样 | `python langevin_vs_sm.py` |
| L10 扩散 | Python + PyTorch | DDPM 复现（对照 6.S184 Lab，重点写论文领读） | `python ddpm_mnist.py` |
| L11 流匹配 | Python + PyTorch | OT-CFM vs DDPM 同预算采样质量曲线 | `python cfm_vs_ddpm.py` |
| L12 评估 | Python | FID/IS/桥接似然估计实现 + 统计不确定性分析 | `python eval_suite.py` |
| L13 离散潜变量 | Python + PyTorch | VQ-VAE 图像/tokenizer + MaskGIT 式并行解码 | `python vqvae.py && python maskgit.py` |
| L14 期末研讨 | Python | 自选前沿论文复现 + 谱系图报告（如等变扩散/离散扩散） | `python final_repro/main.py` |
