# MIT 6.S184：Generative AI with Stochastic Differential Equations（生成式AI与随机微分方程）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | MIT 6.S184 / 6.S185: Generative AI with Stochastic Differential Equations |
| 学校 | MIT（CSAIL，IAP 小学期） |
| 主讲 | Peter Holderrieth、Ezra Erives（MIT 学生主讲） |
| 教材 | *An Introduction to Flow Matching and Diffusion Models*（课程配套讲义笔记，质量极高，建议精读） |
| csdiy 路径 | 深度生成模型 → MIT 6.S184: Generative AI with Stochastic Differential Equations |
| 最新期次 | 2025 年 IAP（课程页更新至 2025-07-11） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | https://diffusion.csail.mit.edu/ |
| 语言/难度/学时 | Python (PyTorch)；🌟🌟🌟🌟；约 20 学时 |

## 为什么学

- 这是目前最好的**扩散模型与流匹配的数学入门课**：从微分方程（ODE/SDE）这一统一视角推导 DDPM、Score-based、Flow Matching，公式推导完整且不跳跃。
- 短小精悍（4 周 IAP、约 20 学时），是进入生成模型方向**性价比最高的第一门课**。
- 配套三个从零实现扩散模型的实践实验，学完能真正手写训练/采样循环，读懂 diffusers 源码。
- 前沿讲座覆盖分子设计、机器人学等生成模型应用，理解理论如何落地。

## 先修与知识联系

- 先修：深度学习基础（会 PyTorch、懂神经网络训练）、微积分与线性代数；概率论（随机变量、条件分布、期望）有帮助。
- 联系：
  - 上游：CS229 / 11-785（深度学习基础）、数学基础（MIT18.06 线代、概率论）。
  - 平行：机器学习进阶/STAT8201（深度生成模型讨论班）、STA4273（变分推断视角）、CMU10-708（图模型与潜变量）。
  - 下游：大语言模型课程中的扩散语言模型、多模态生成（Sora 类视频生成即扩散/流匹配路线）。

## 讲义章节目录（2025 期，按官网 schedule 与配套教材整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 生成模型概览与概率背景（分布、条件概率、极大似然） | 课程教材 §1-2 |
| L2 | 深度学习基础回顾（神经网络、优化、VAE/自回归/Flow/GAN/扩散分类学） | 教材 §3；Kingma & Welling VAE 综述 |
| L3 | 常微分方程与连续标准化流（CNF） | 教材 §4；Chen et al. Neural ODE |
| L4 | 随机微分方程基础（布朗运动、Ito 引理、Fokker-Planck 方程） | 教材 §5 |
| L5 | Score-based 生成模型（噪声得分匹配、NCSN） | 教材 §6；Song & Ermon Score-based |
| L6 | 扩散模型 DDPM（前向加噪、反向去噪、ELBO 推导） | 教材 §7；Ho et al. DDPM |
| L7 | 扩散的统一 SDE 视角（前向/反向 SDE、概率流 ODE） | 教材 §8；Song et al. SDE 统一框架 |
| L8 | 采样与推断加速（DDIM、分数-步骤、引导 guidance、 classifier-free） | 教材 §9；Ho et al. DDIM |
| L9 | 流匹配 Flow Matching（条件流匹配、OT-CFM、rectified flow） | 教材 §10；Lipman et al. Flow Matching |
| L10 | 扩散与流匹配的实践实验讲评（从零构建扩散模型） | 课程 Lab 1-3 讲义 |
| L11 | 应用讲座 I：分子设计与科学应用 | 官网讲座视频/幻灯片 |
| L12 | 应用讲座 II：机器人与动作轨迹生成 | 官网讲座视频/幻灯片 |

> 注：MIT IAP 每年 1-2 月开课，各年讲次编排略有调整；动手作业为三个实验（从零构建扩散模型并应用），详见官网。
