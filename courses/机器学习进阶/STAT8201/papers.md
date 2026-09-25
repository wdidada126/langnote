# Columbia STAT 8201 论文清单

## 经典论文（深度生成模型全谱系）

| 路线 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| 自回归 | PixelRNN/PixelCNN (van den Oord) | 2016 | L2 |
| 自回归 | WaveNet (Oord et al.) | 2016 | L2/L5 |
| VAE | Auto-Encoding Variational Bayes (Kingma & Welling) | 2013 | L3 |
| VAE | IWAE (Burda et al.) | 2015 | L4 |
| VAE | β-VAE (Burgess et al.) | 2018 | L4 |
| VAE | Hierarchical VAE / Ladder Variational Networks (Sonderby, Maaløe) | 2016 | L4 |
| Flow | Variational Inference with Normalizing Flows (Rezende & Mohamed) | 2015 | L5 |
| Flow | RealNVP (Dinh et al.) | 2016 | L5 |
| Flow | Glow (Kingma & Dhariwal) | 2018 | L5 |
| Flow | WaveFlow (Lu et al.) | 2019 | L5 |
| GAN | Generative Adversarial Nets (Goodfellow et al.) | 2014 | L6 |
| GAN | f-GAN (Nowozin et al.) | 2016 | L6 |
| GAN | WGAN / WGAN-GP (Arjovsky; Gulrajani) | 2017 | L6 |
| GAN | Progressive GAN / StyleGAN / StyleGAN2 / StyleGAN3 (Karras) | 2017-2021 | L7 |
| EBM | What Energy-Based Models Can Do (LeCun) | 2006/2022 宣言 | L8 |
| EBM | Training Energy-Based Networks with Persistent Contrastive Difference (Tieleman) | 2008 | L8 |
| EBM | InfoNCE / Representation Learning with Contrastive Predictive Coding (van den Oord) | 2018 | L8 |
| Score | Noise Conditional Score Matching (Song & Ermon NCSN) | 2019 | L10 |
| Diffusion | Denoising Diffusion Probabilistic Models (Ho et al.) | 2020 | L10 |
| Diffusion | Score-Based Generative Modeling through SDEs (Song et al.) | 2021 | L10 |
| Diffusion | DDIM (Song et al.) | 2021 | L10 |
| Flow Matching | Flow Matching for Generative Modeling (Lipman et al.) | 2023 | L11 |
| 离散潜变量 | Neural Discrete Representation (VQ-VAE, van den Oord) | 2017 | L13 |
| 离散潜变量 | Residual VQ / SoundStream / EnCodec | 2021-22 | L13 |
| 离散生成 | MaskGIT (Chang et al.) | 2022 | L13 |
| 评估 | 似然评估批判与 FID (Heusel et al.) | 2017 | L12 |
| 图模型连接 | 深度潜变量×图模型（Cunningham 组论文轮值） | - | 全课 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| ADM：Diffusion Models Beat GANs on Image Synthesis | 2021 | 扩散超越 GAN 的标志 |
| Stable Diffusion / Latent Diffusion (Rombach) | 2022 | 潜空间扩散 + VQGAN 组合 |
| EDM (Karras et al.) | 2022 | 扩散设计空间系统消融 |
| Consistency Models (Song et al.) | 2023 | 少步生成 |
| Sora（视频扩散/流匹配） | 2024 | 生成模型规模化样本 |
| SD3 + Rectified Flow/MMDiT | 2024 | 流匹配进入旗舰 |
| 离散扩散（D3PM, Sinkhorn 离散扩散） | 2024 | L13 前沿 |
| JEPA/嵌入预测架构（LeCun 路线） | 2023-25 | EBM 复兴主张 |
| 等变扩散用于蛋白（RFdiffusion） | 2023 | 科学生成 |
| Stein 变分/采样器改进与 NUTS 应用 | 2021-24 | 统计推断交叉 |
| 自回归图像生成统一（VAR, autoregressive next-scale） | 2024 | 回归路线复兴 |
| GAN 在视频/3D（如 EG3D/GEN3C）| 2023-24 | GAN 的 3D 应用 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| ELBO / VAE 族 | torch VAE 教程、diffusers AutoencoderKL | VAE=潜空间接口层 |
| Normalizing Flow | nflow、FrEIA、Glow 官方实现、sparkflow | L5 复现 |
| GAN | StyleGAN2-ADA / StyleGAN3 (NVlabs)、PGGAN 复现 | L6-L7 |
| EBM / 对比 | torchebml、JEPA 官方（PyTorch）、VICReg | L8 |
| Score/扩散 | diffusers、NVlabs EDM/edm2、open_clip 的对比成分 | L10 |
| 流匹配 | diffusers FlowMatchEulerDiscreteScheduler、Stable-Diffusion-3 | L11 |
| 离散潜变量 | vector-quantize-pytorch、audiocraft (EnCodec) | L13 |
| 似然/评估 | torch-fidelity (FID)、PRDC 估计、流估计 | L12 |
| 统计推断栈 | Pyro/NumPyro 的概率编程视角 | L9 |
