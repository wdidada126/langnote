# L13 强化学习 I：时序差分与 Q-Learning

> 对应 AIMA Ch.21（RL）；Klein 讲义 "Reinforcement Learning / Q-Learning"。项目 `projects/rl` 实现本讲。官方 P3/P4 主题。

## 1. 核心概念

- **动机**：L12 的值迭代需要 T 和 R。现实：要么太大（Atari 状态 10^6），要么未知（迷宫从没走过）→ **无模型学习**，从经验样本 (s,a,s',r) 学。
- **主动学习要素**：agent 的动作改变数据分布 ⟹ 探索问题（区别于监督学习的 i.i.d.）。
- **时序差分 TD(0)**：用一次样本更新价值 V(s) ← V(s) + α[r + γV(s') − V(s)]；TD 误差 δ 是自举（bootstrap）残差。
- **Q-Learning**（Watkins 1992，off-policy）：
  - Q(s,a) ← Q(s,a) + α[r + γ max_{a'} Q(s',a') − Q(s,a)]
  - 更新目标用 max（学 Q*），执行用 ε-greedy（行为策略≠目标策略 ⟹ off-policy）。
  - 收敛定理： Robbins-Monro 条件 Σα=∞, Σα²<∞ + 每个 (s,a) 无限访问 ⟹ Q→Q*（与执行策略无关，只要还在探索）。
- **SARSA**（on-policy）：目标用实际选择的 a'，学的是 Q^π；更保守（避开不确定区），策略评估视角。
- **探索策略**：ε-greedy、softmax（温度）、UCB（对不确定性乐观）、**内在奖励**（count-based 1/N(s)，新颖性驱动）。

## 2. 关键伪码

```
Q ← 0  # 乐观初始化：未知即希望（optimism in face of uncertainty）
loop episode:
    s ← s0
    while not terminal:
        a ← ε-greedy(Q[s])
        s', r ← env.step(a)
        Q[s,a] ← Q[s,a] + α( r + γ·max_a' Q[s',a'] − Q[s,a] )
        s ← s'
```

## 3. 直觉例子

- 本项目 4x4 网格：ε=0.2、α=0.1、γ=0.95，约 2-5k episode 后贪心策略与 L12 值迭代最优策略一致——**模型未知也能逼近 L12 的答案**，两项目对照是本讲作业精髓。
- 陷阱边界的"犹豫现象"：转移随机性使边界 Q 值方差大，学习后期 ε 小导致采样不足——exploration 饥饿。

## 4. 前后讲联系

- 前承 L12（同一环境去掉 T/R）、L08（期望→样本均值）、L11（在线学习/平滑视角）；后接 L14（表格 Q 存不下 → 函数逼近；Q-learning 不可微 → 策略梯度）。
- TD 误差 δ 同时是 L14 actor-critic 的 critic 信号——"一个残差喂两个模块"。

## 5. 跨课程联系

- **6.006**：表格 Q 空间 O(|S||A|) = 状态显式列举的最后阵地；对比 Dijkstra 需要全图已知。
- **CS229**：Q-learning = 带 max 的在线 SGD（非凸、非平稳目标，收敛性证明是额外功课）。
- **CS231n**：DQN（2015）把 Q 换成 CNN，是 L14→L20 的桥梁；Atari 是"RL 的 ImageNet 时刻"。
- **MIT6.824**：多 agent 各自 Q-learning 时环境对每个 agent 非平稳（学习周期不同步）——与分布式系统中"时钟漂移导致状态不一致"神似。
- **DDCA**：Q 表查表延迟 = 内存墙；**类比学习电路（comparison learning, Barto-Sutton Anderson 1981）当年就是用硬件实现 RL 的**。

## 6. 开源项目应用

- **Gymnasium**：`FrozenLake-v1` 即本讲环境（is_slippery=True 对应转移随机）。
- **stable-baselines3**：`DQN` 是表格版深度化；表格版用 `gym_ple`/自制。
- **RLlib**：`DQN/QNF` 算法族 + 自定义 Env 接口。
- 项目实战：`projects/rl`（与 `projects/mdp` 同环境，Q-learning 结果与值迭代最优策略自动比对）。

## 7. 延伸阅读

- AIMA 4e §21.1-21.2；CS188 Note "Q-Learning"；Sutton & Barto §6。
- Watkins & Dayan "Q-learning" (1992)；Mnih et al. "Human-level Control through DRL" (2015)；Lecture Note 细节：Tsitsiklis 1994 异步 QP 收敛。
