# MIT 6.S184 论文清单

## 经典论文（深度生成模型四大路线）

| 路线 | 论文 | 年份 | 与本课关系 |
| --- | --- | --- | --- |
| VAE | Auto-Encoding Variational Bayes (Kingma & Welling) | 2013 | ELBO 推导是 DDPM 损失前身 |
| GAN | Generative Adversarial Nets (Goodfellow et al.) | 2014 | 对照：无似然的对抗式生成 |
| Flow | Variational Inference with Normalizing Flows (Rezende & Mohamed) | 2015 | 密度可算路线；CNF 是其无限深极限 |
| Flow | Density estimation using Real NVP (Dinh et al.) | 2016 | 离散流基线 |
| Flow | Glow: Generative Flow with Invertible 1x1 Convolutions (Kingma & Dhariwal) | 2018 | 图像流 SOTA |
| CNF | Neural Ordinary Differential Equations (Chen et al.) | 2018 | L3 直接来源：instantaneous change of variables |
| Score | Generative Modeling by Estimating Gradients of the Data Distribution (Song & Ermon, NCSN) | 2019 | L5 核心 |
| Diffusion | Denoising Diffusion Probabilistic Models (Ho, Jain, Abbeel) | 2020 | L6 核心 |
| Diffusion | Score-Based Generative Modeling through SDEs (Song et al.) | 2021 | L7 统一框架，本课教材骨架 |
| Diffusion | Denoising Diffusion Implicit Models (DDIM, Song et al.) | 2021 | L8 少步采样 |
| Diffusion | Image Super-Resolution via Iterative Refinement (SR3) | 2021 | ε-prediction 参数化与 guidance |
| Diffusion | Classifier-Free Guidance (Ho & Salimans) | 2022 | L8 条件生成标配 |
| Flow Matching | Flow Matching for Generative Modeling (Lipman et al.) | 2023 | L9 核心 |
| Flow Matching | Stochastic Interpolants (Albergo & Vanden-Eijnden) | 2023 | 与 FM 等价性的另一视角 |
| Rectified Flow | Flow Straight and Fast (Liu, Gong, Yan) | 2023 | OT 路径直线化 |
| 蒸馏 | Consistency Models (Song et al.) / Progresive Distillation (Salimans & Ho) | 2022-23 | 采样加速延伸 |

## 近 5 年（2021-2026）重要进展

| 论文/系统 | 年份 | 要点 |
| --- | --- | --- |
| ADM (Dhariwal & Nichol, Diffusion Models Beat GANs) | 2021 | 扩散质量超越 GAN 的转折点 |
| Stable Diffusion / Latent Diffusion (Rombach et al.) | 2022 | 潜空间扩散，工业标配 |
| EDM (Karras et al., Elucidating the Design Space) | 2022 | 扩散设计空间系统消融，本课推导直接可解释 |
| DiT (Scalable Diffusion Models with Transformers) | 2023 | Transformer 骨干统一视觉生成 |
| Sora (OpenAI 技术报告, High-Res Video w/ Spatio-Temporal Transformers) | 2024 | 视频扩散/流匹配路线，patch 时空 token |
| SD3 (MMDiT + Rectified Flow) | 2024 | 流匹配进入旗舰产品 |
| Scaling Rectified Flow (Meta, "StreamingT5"类) | 2024-25 | FM 缩放律研究 |
| Consistency Distillation /LCM, sCM | 2024 | 1-4 步实时生成 |
| Diffusion Forcing / CauselM 类 | 2024-25 | 扩散与自回归融合，序列生成 |
| 流匹配理论新进展（OT-CFM 变体、离散流匹配） | 2024-26 | L9 延伸 |

## 知识点在开源项目中的应用

| 课程知识点 | 开源项目 | 对应实现 |
| --- | --- | --- |
| DDPM 训练/采样循环 | Hugging Face diffusers | DDPMScheduler、DDIMScheduler |
| SDE 统一视角 | NVlabs edm / score_sde (Song) | 训练脚本即课内公式 |
| Flow Matching / OT-CFM | diffusers FlowMatchEulerDiscreteScheduler、Stable Diffusion 3 | SD3/MMDiT 默认调度器 |
| Classifier-free guidance | diffusers guidance scale 参数、CFG++ | 所有文生图 pipeline |
| 概率流 ODE / CNF | torchdiffeq | ODE 求解器库 |
| Consistency/少步蒸馏 | diffusers consistency models、LCM-LoRA | 实时生成 |
| 潜空间扩散 | Stable Diffusion / ComfyUI | VAE + UNet/DiT |
| Diffusion Policy（机器人） | diffusion-policy 官方实现 | 动作轨迹去噪 |
| 分子等变扩散 | torchmd-net、RFdiffusion 生态 | 科学应用 |
