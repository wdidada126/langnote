# L14 强化学习 II：近似 Q-Learning 与策略梯度

> 对应 AIMA Ch.21.3 + CS285 延伸；Klein 讲义 "Approximate RL / Policy Search"。官方 P4 主题。

## 1. 核心概念

- **函数逼近动机**：表格 Q(s,a) 在连续状态（Pacman 坐标）或高维（像素）下不可存——用参数化 Q̂(s,a;w)（线性特征或网络）。
- **特征设计（本课）**：f(s,a) = [到最近豆距离、是否贴墙、鬼在视野…]；Q̂ = w·f。
  - **C-Learning**（Klein）：在线学习 w，用 L13 的 TD 误差做次梯度更新 w ← w + α·δ·∇Q̂。
- **DQN 三件套（深度版）**：经验回放（破坏相关性）+ 目标网络（稳定 bootstrapping）+ 梯度裁剪——三件都针对"数据非独立/目标移动"。
- **策略搜索动机**：Q-learning 策略贪心=不可微，且连续动作/随机策略难处理 → 直接参数化 π(a|s;θ)，**对 J(θ)=E[U] 做梯度上升**。
- **REINFORCE / 策略梯度定理**（Williams 1992 / Sutton 2000）：
  - ∇_θ J = E_{τ~π_θ}[ (Σ_t γ^t ∇_θ log π_θ(a_t|s_t)) · U(τ) ]
  - log-derivative 技巧：∇P = P·∇log P（期望里不再含分布梯度，可采样）。
  - **baseline/优势 A = U − b(s)**：不改变期望梯度、只降方差（与 L13 TD 误差同源）。
- **方差问题**：REINFORCE 梯度噪声大 → actor-critic（学 V̂ 当 baseline）、GAE、PPO（信任域防策略崩塌）。

## 2. 关键伪码

```
Policy-Gradient (REINFORCE):
  for iter:
      τ ← rollout(π_θ)
      for t: θ ← θ + α·γ^t·∇log π_θ(a_t|s_t)·(U_t − b(s_t))
Approximate Q (C-learn):
  sample (s,a,s',r): δ = r + γ·max_a' Ŵ(s',a') − Ŵ(s,a); w += α·δ·∇Ŵ
```

## 3. 直觉例子

- 2D 车摆（cartpole）：线性特征（sin/cos 径向基）即可让近似 Q 学好；表格版直接写不下。
- "为什么 PG 乘整条轨迹回报？"——早期动作对后期结果负责，log-π 加权即信用分配（credit assignment）；对比 TD 把信用沿 bootstrap 传播。

## 4. 前后讲联系

- 前承 L11（参数学习/梯度）与 L13；后接 L20（神经网络 = 逼近器本体）、L12（模型已知→DP，未知→RL，不可微→PG 的三段论）。
- 与 L04 局部搜索：策略梯度就是参数空间爬山 + 期望算子；与 L21：多智能体 PG 是 MARL 基础。

## 5. 跨课程联系

- **CS285**（官方后续）：本讲两节课压缩版在 CS285 是 5 周内容（TRPO/PPO/SAC 全家桶）。
- **CS229/CS231n**：反向传播 = ∇logπ 的自动微分；RLHF 训练 LLM 用的就是 PPO/GRPO——策略梯度是"LLM 对齐"的底层算法。
- **6.006**：次梯度法与凸优化附录互认。
- **MIT6.824**：rollout 并行 = 无协调的 map-only 作业，梯度聚合 = reduce（A3C 的异步架构是教科书式 map-reduce RL）。
- **DDCA**：RL 硬件加速器（模拟域 memristor 做 ∇logπ）正在把 PG 搬进芯片。

## 6. 开源项目应用

- **stable-baselines3**：`PPO/DQN/A2C`；`gymnasium` 自定义特征环境。
- **RLlib**：工业级 PG 族（PPO/Sac/IMPALA），支持分布式 rollout。
- **Tianshou / trlx / OpenRLHF**：后两者展示 PG 在 LLM 对齐中的现代形态（RLHF）。
- 项目实战：`projects/rl` 附带 REINFORCE 迷你实现（纯 python，一维环境）。

## 7. 延伸阅读

- CS188 Note "Approximate RL"；Sutton & Barto ch.9-13；Levine CS29 RL 讲义（policy gradient 一节公认最佳）。
- Williams "Simple Statistical Gradient-Following" (1992)；Mnih DQN (2015)；Schulman PPO (2017)；Silver DDPG (2014)。
