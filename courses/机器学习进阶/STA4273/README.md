# U Toronto STA 4273：Minimizing Expectations（最小化期望：推断与控制的统一）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | University of Toronto STA 4273 (C14): Minimizing Expectations — Winter 2021 |
| 学校 | University of Toronto（矢量所/DSP，David Duvenaud 等亦在该系；本课主讲 Chris Maddison） |
| 主讲 | Chris Maddison（AlphaGo 创始成员，NeurIPS 2014 最佳学生论文） |
| 教材 | 无固定教材；课程讲义 + 论文（score function/pathwise 梯度、变分推断、最优控制经典文献） |
| csdiy 路径 | 机器学习进阶 → U Toronto STA 4273 Winter 2021: Minimizing Expectations |
| 最新期次 | Winter 2021（csdiy 页面 2023-12-16） |
| 状态 | 骨架已建，待逐讲填充笔记 |
| 课程网站 | https://www.cs.toronto.edu/~cmaddis/courses/sta4273_w21/ |
| 难度 | 🌟🌟🌟🌟🌟🌟🌟（PhD 研究课程） |

## 为什么学

- 核心问题极尖锐：**当你想最小化一个"期望"而不是"求和"时，一切自动微分和优化都会碎掉**——本课系统研究含期望目标（ELBO、RL 目标、随机控制泛函）的梯度估计理论。
- 把**统计推断（VAE/变分）与随机控制/强化学习统一到同一数学框架**：score-function 与 pathwise 两大梯度族、控制变量、Rao-Blackwellization 在两边反复出现。
- Maddison 是 Gumbel-Softmax、梯度估计（REINFORCE 改进）、连续松弛方向的创造者之一，课程材料即一手研究脉络。
- 学完后能读懂：变分推断论文中的方差约简技巧、RLHF 中 GRPO 的基线设计、扩散模型训练目标的得分函数推导。

## 先修与知识联系

- 先修：贝叶斯推断、强化学习；扎实的测度论级概率直觉与优化基础。
- 联系：
  - 上游：CMU10-708（变分推断/MCMC）、CS285（策略梯度=REINFORCE）、STAT8201（VAE 应用层）。
  - 平行：MIT6.S184（SDE/得分函数视角与之互为镜像）。
  - 下游：CS229M（理论保证）、随机控制/扩散模型科研；RLHF 系统课（11-868）的算法根基。

## 讲义章节目录（Winter 2021 按官网主题周整理，以官网 schedule 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：期望最小化问题族（ELBO、策略梯度、自由能）与困难根源 | 课程 notes §1 |
| L2 | 蒙特卡洛基础：估计器无偏性、方差、CLT 与控制变量的必要性 | Robert & Casella 选章 |
| L3 | 两大梯度恒等式：score-function（REINFORCE）与 pathwise（重参数化） | Papamakis/Titsias; Kingma VAE § |
| L4 | score-function 梯度优化：基线、控制变量、Rao-Blackwellization | Greensmith et al.；Roeder REINFORCE leave-one-out |
| L5 | pathwise 梯度深入：重参数化代数、非重参数化分布处理 | Feroze & Durwardani 连续松弛 |
| L6 | 离散与约束问题：Gumbel-Softmax、straight-through、梯度无偏性权衡 | Maddison Mnist? 论文：Jang Gumbel-Softmax、Maddison CONCRETE |
| L7 | 变分推断即期望优化：ELBO 族（α-/IMSELBO/RAI）、推断网络梯度 | Mohamed et al. 监控 variational objectives |
| L8 | 随机最优控制：Pontryagin、HJB、值函数与策略 | Bertsekas 选章；Abendroth 讲义 |
| L9 | 推断-控制对偶：相对熵控制（Kappen/Toussaint）、路径积分、soft value | Levine RL as inference |
| L10 | 序贯模型与控制推断：滤波、粒子控制、逆 RL 的期望目标 | Toussaint 综述 |
| L11 | 随机优化的统一语言：自然梯度、方差缩减、自适应基线 | Martens; Titsias & Blundell 样本平均 |
| L12 | 前沿专题与展示：扩散训练目标=得分匹配的期望优化、RLHF 梯度病理 | 当期论文（学生自选） |

> 注：本课为 PhD 研究课，官网含讲义 PDF 与每周阅读；上表主题骨架依据课程描述"inference and control 的关系"与 Maddison 研究线整理。
