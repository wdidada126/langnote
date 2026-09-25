# UCB CS285: Deep Reinforcement Learning 学习笔记

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS285 / Deep RL: Deep Reinforcement Learning（UW 亦以 CSE 599/laptop 名义镜像开课） |
| 学校 | University of California, Berkeley（Rail Lab） |
| 主讲 | Sergey Levine |
| 教材 | 无指定教材；Sutton & Barto《Reinforcement Learning: An Introduction》为事实标准伴读 |
| csdiy 路径 | `深度学习/CS285`（页面更新：2022-11-10） |
| 最新期次 | 每年 Fall 更新（csdiy 记录 22Fall 翻转课堂模式；YouTube 完整播放列表含全部视频内容） |
| 状态 | 骨架已建，正文待写 |
| 难度/学时 | csdiy 标注 🌟🌟🌟🌟，约 80 小时；先修：CS188（MDP/搜索）、CS189（ML 基础），公式密度高 |

## 为什么学

- 深度强化学习领域的事实标准课程：Levine 本人即是该方向奠基人之一（CMA/半正定策略梯度、AWR、离线 RL、RLHF 相关研究）。
- 课程内容随最新研究每年更新：从策略梯度到扩散策略、RLHF/推理模型 RL、具身智能，覆盖 RL 全谱。
- 5 个编程作业=复现经典算法 + 横向对比（模仿学习→IQL/离线 RL→模型基 RL），框架已给、按 hint 填空，上手无门槛、理解有深度。
- 翻转课堂设计：视频自学 + 课上 Q&A，公开视频已含全部讲解内容，自学体验完整。

## 先修与知识联系

- 先修：CS188（MDP/贝尔曼方程/搜索）、CS189（机器学习）、概率论与线性代数；多变量微积分（梯度/期望推导）。
- 纵向：课程是 LHY 旧版 RL Lab 与 CS224n 对齐章节（RLHF）的理论上游。
- 横向：模型基 RL 与世界模型衔接 MIT 6.S184（SDE 生成视角）；RL scaling 部分衔接大模型课程群。

## 讲义章节目录（按近年 Fall 课表整理，以官网为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 引言：RL 与最优控制 | Sutton ch.1-3（自学） |
| L2 | 数学基础：MDP、值函数与贝尔曼最优方程 | Sutton ch.4；讲义推导 |
| L3 | 策略梯度 I：REINFORCE 与基线 | Williams 1992；课程 notes |
| L4 | 策略梯度 II：实现与变分视角（CMA-ES 关联） | TRPO 论文节选 |
| L5 | 模仿学习与逆向 RL | DAgger、AIRL、GAIL |
| L6 | Q-learning 与值函数学习入门 | DQN 论文 |
| L7 | 高级值学习：SAC/TD3 与 actor-critic 家族 | Soft Q-learning 论文 |
| L8 | 探索 I：内在动机与计数 | 伪计数/UCB 讲义 |
| L9 | 探索 II：表示学习与捷径问题 | RND、状态抽象 |
| L10 | 离线强化学习 | CQL、IQL、BEAR |
| L11 | 模型基 RL：MPC 与 Dyna | MBPO、PlaNet |
| L12 | 模型学习 II：世界模型与想象训练 | Dreamer v1-v3 |
| L13 | 决策时规划与推理 | MuZero、树搜索+学习 |
| L14 | 部分可观测与元强化学习 | POMDP、MAML |
| L15 | 深度多任务/分层 RL | 选项框架、HIRO |
| L16 | 大规模训练：RL 的缩放定律 | GPT/PPO scaling 论文 |
| L17 | LLM 的 RL 对齐与微调：RLHF/DPO/GRPO | InstructGPT、DeepSeek-R1 |
| L18 | 推理与 test-time compute 的 RL | o1/R1 技术解读 |
| L19 | 机器人学习 I：感知与操作 | 课程机器人笔记 |
| L20 | 机器人学习 II：扩散策略与 flow matching | Diffusion Policy |
| L21 | 具身智能与视觉-语言-动作模型 | RT-2、π0 |
| L22 | 前沿专题与项目展示 | 当季论文列表 |

> 作业线（5 个）：HW1 模仿学习（行为克隆/DAgger）→ HW2 IQL 离线 RL → HW3 模型基（MLE+Dyna）→ HW4 探索与目标条件 → HW5 自由项目 + 报告。每年随研究更新。
