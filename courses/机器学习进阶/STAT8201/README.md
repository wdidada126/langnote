# Columbia STAT 8201：Deep Generative Models（深度生成模型）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Columbia University STAT UN8201 (GR8201): Deep Generative Models |
| 学校 | Columbia University |
| 主讲 | John Cunningham（统计系，贝叶斯/图模型方向） |
| 教材 | 无固定教材，以论文研讨为主（VAE/Flow/GAN/扩散/EBM 经典论文集） |
| csdiy 路径 | 机器学习进阶 → Columbia STAT 8201: Deep Generative Models |
| 最新期次 | csdiy 推荐版为 2023-12-16 记录期；课程为哥大常态研讨班（课程页 http://stat.columbia.edu/~cunningham/teaching/GR8201/ ） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | http://stat.columbia.edu/~cunningham/teaching/GR8201/ |
| 难度 | 🌟🌟🌟🌟🌟🌟（PhD 讨论班：每周展示 + 论文讨论） |

## 为什么学

- 深度生成模型的**博士级论文研讨班**：由图模型背景（Cunningham 是 PGM/贝叶斯非参数专家）切入"图模型 × 神经网络"的现代生成体系，视角区别于纯工程课程。
- 组织形式独特：每周由学生展示并领读论文，逼你以研究者方式读 VAE/Flow/GAN/Score-based/EBM 的一手文献——是 CS229/10-708 之后训练"论文品味"的课。
- 主题即当代生成建模正史：从 ELBO 家族到扩散与流匹配、从密度可算到似然无关，学完能画完整方法谱系图。
- 与 MIT6.S184 互补：6.S184 给微分方程推导纵深，本课给横向方法版图与统计建模深度（贝叶斯非参数、潜变量结构）。

## 先修与知识联系

- 先修：机器学习、深度学习、图模型（10-708 或同等）；概率与统计推断基础扎实。
- 联系：
  - 上游：CS229/11-785（ML/DL）、CMU10-708（潜变量与变分推断语言）。
  - 平行：机器学习进阶/STA4273（推断-控制视角更数学）、CS229M（理论保证）；深度生成模型/MIT6.S184（扩散纵深）。
  - 下游：生成模型科研选题；大语言模型课程的自回归生成对照。

## 讲义章节目录（研讨班按主题周组织；下表按历年课程阅读主题整理，以官网 syllabus 为准）

| 讲次 | 主题（周） | 阅读材料 |
| --- | --- | --- |
| L1 | 课程地图：生成建模目标分类学（密度可算/似然无关/潜变量） | 综述 slides；Bishop ch1 扩展 |
| L2 | 自回归模型与信息论视角 | PixelRNN/PixelCNN；高频：链式法则与次序选择 |
| L3 | VAE I：变分下界、重参数化 | Kingma & Welling 2013；Elbo 推导复习 |
| L4 | VAE II：后验坍缩、分层潜变量、Disentangle | Sohn VAE-IWAE；β-VAE；Hierarchical VAE |
| L5 | Normalizing Flows | RealNVP；Glow；WaveFlow；自回归 flow |
| L6 | GAN I：对抗极小极大与理论 | Goodfellow 2014；f-GAN；WGAN |
| L7 | GAN II：稳定训练与现代应用 | StyleGAN2/3；条件生成；与扩散对比 |
| L8 | 能量模型（EBM） | LeCun EBM 宣言；NCE/对比散度；短朗之万链 |
| L9 | 自对抗与伪似然 | MCMC 生成观；噪声对比估计 |
| L10 | Score-based 与扩散 | NCSN；DDPM；SDE 统一（配 MIT6.S184） |
| L11 | 流匹配与最近生成前沿 | Flow Matching；Rectified Flow；Sora/SD3 讨论 |
| L12 | 似然评估与信息内容 | 困惑度、bits/dim；变分界评估的陷阱 |
| L13 | 潜变量模型×LLM：离散隐变量 | VQ-VAE；残差量化；序列生成统一 |
| L14 | 生成模型在科学/推理应用（当期研讨） | 学生自选论文轮值 |

> 注：本课为 PhD 讨论班，每周"展示 + 讨论论文"；具体轮次文献每学期由学生与教授共同确定，上表为方法主线阅读骨架。
