# CS285 论文与应用清单

## 经典论文（课程直接对应）

| 论文 | 年份 | 关联讲次 | 一句话要点 |
| --- | --- | --- | --- |
| Simple Statistical Gradient-Following Algorithms (REINFORCE, Williams) | 1992 | L3 | 策略梯度原始推导 |
| Policy Gradient Methods (Jordan et al. 自然策略梯度) | 1999/2000 | L4 | 信息几何视角 |
| A3C (Asynchronous Methods in Deep RL) | 2016 | L4/L7 | 并行 actor-critic 开源标杆 |
| Trust Region Policy Optimization (TRPO) | 2015 | L4 | 单调改进保证 |
| PPO | 2017 | L4/L16 | 剪裁目标，现役默认算法 |
| Playing Atari with Deep RL (DQN) | 2013 | L6 | 深度值函数起点 |
| Deterministic Policy Gradient (DDPG) | 2016 | L7 | 连续动作确定性 AC |
| Soft Actor-Critic (SAC) | 2018 | L7 | 最大熵连续控制 SOTA |
| Generative Adversarial Imitation Learning (GAIL) | 2016 | L5 | 对抗式模仿 |
| DAgger | 2010 | L5 | 聚合消除分布偏移 |
| Hindsight Experience Replay (HER) | 2017 | L15 | 失败轨迹变废为宝 |
| MAML | 2017 | L14 | 元 RL 代表方法 |
| CQL (Conservative Q-Learning) | 2020 | L10 | 离线 RL 保守下界 |
| MBPO | 2019 | L11 | 模型基短 rollout |
| Dreamer v3 | 2023 | L12 | 世界模型通用配方 |
| MuZero | 2019 | L13 | 学习模型+树搜索 |
| InstructGPT / RLHF | 2022 | L17 | LLM 对齐 RL 化 |

## 近 5 年（2021-2026）论文

| 论文 | 年份 | 关联知识点 |
| --- | --- | --- |
| IQL (Offline RL with Implicit Q-learning) | 2021 | L10 期望回归免 OOD 查询 |
| Diffusion Policy | 2023 | L20 多模态动作分布生成 |
| Decision Transformer | 2021 | L10-L11 序列建模做控制 |
| DPO | 2023 | L17 免 RM 偏好优化 |
| GRPO (DeepSeekMath) 与 DeepSeek-R1 | 2024-2025 | L17-L18 组相对策略优化/推理 RL |
| π0 / RT-2（VLA 模型） | 2023-2024 | L21 视觉-语言-动作 |
| Grokking / RL scaling laws（Kaplan 后续） | 2021-2024 | L16 规模经验律 |
| Gymnasium/MinAtar 环境与基准更新 | 2022-2024 | L9/L14 评估设施 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 策略梯度/PPO（L3-L4） | CleanRL / stable-baselines3 / Tianshou / rl_games | 单文件与库级 PPO 实现 |
| DQN 家族（L6-L7） | RLkit / tf-agents | 值方法教学实现 |
| 模仿/离线 RL（L5/L10） | D4RL 数据集 + official IQL/CQL repos / minari | 离线基准与复现 |
| 世界模型（L11-L12） | DreamerV3 官方 / daydreamer | RSSM 想象训练 |
| RLHF（L17） | TRL / OpenRLHF / veRL / slime | RM/PPO/GRPO 训练环 |
| 推理 RL（L18） | OpenAI Gym-RL 类玩具、DeepSeek-PRIME、verl-GRPO | 可验证奖励管线 |
| 机器人（L19-L21） | diffusers(Diffusion Policy)、Isaac Lab / mujoco / LeRobot | 仿真-真机-开源机械臂栈 |
