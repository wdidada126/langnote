# L12 马尔可夫决策过程 MDP：值迭代与策略迭代

> 对应 AIMA Ch.17；Klein/Sutton 讲义 "MDPs"。项目 `projects/mdp` 实现本讲。官方 Pacman P2/P3 主题。

## 1. 核心概念

- **MDP 五元组** (S, s₀, A, T(s,a,s'), R(s,a,s'), γ)：环境**已知**（T、R 白给），求最优策略。
- **马尔可夫性**：未来只依赖当前状态（无记忆）——"状态要包含决策所需一切"。
- **策略 π: S→A**；轨迹回报 U = Σ γ^t R_t；**折扣 γ∈(0,1)**：数学收敛 + 模型不确定性 + 偏好即时。
- **Bellman 最优方程**（本课核心恒等式）：
  - V*(s) = max_a Σ_{s'} T(s,a,s')[R(s,a,s') + γV*(s')]
  - Q*(s,a) = Σ_{s'} T[R + γ max_{a'} Q*(s',a')]
- **值迭代 VI**：以上式作赋值算子反复更新，压缩映射（γ-收缩）⟹ 收敛到唯一不动点；每次迭代 O(|S|²|A|)。
- **策略迭代 PI**：策略评估（解线性方程组/迭代）+ 策略改进（贪心）交替；有限策略集 ⟹ 有限步收敛，通常迭代次数少但每步贵。
- **时不变性（stationarity）**：最优策略不随时间变——γ 与马尔可夫性共同保证（对比 L05 深度限制搜索）。

## 2. 关键伪码

```
VI:  V ← 0; repeat
       for s: V'[s] ← max_a Σ_s' T[R + γV[s']]
     until max|V'−V| < ε
     π(s) ← argmax_a Σ_s' T[R + γV[s']]      # 策略提取=每状态一次贪心
PI:  π random; repeat
       V ← POLICY-EVALUATION(π)               # V^π = Σ T^π[R + γV^π]
       π' ← greedy(V over A); until π'=π
```

## 3. 直觉例子

- 4x4 网格（本项目环境）：墙 + 滑移（80% 执行/20% 侧滑）、陷阱 −10、奖励 +10：
  - 值函数的"山坡"就是最优路线的等高线；γ=0.95 时远处奖励折价，agent 会先避陷阱再冒险。
- Racing car（Klein 经典例）：track 边缘滑移概率大 ⟹ 最优策略是"绕慢弯"——**风险规避从折扣+转移矩阵自然涌现**，无需显式设计。

## 4. 前后讲联系

- 前承 L02-L03（无随机无折扣 + R=−1 ⟹ MDP 退化为最短路；V* 即完美启发式）、L05（expectimax 的有限地平线版 → MDP 无限地平线版）、L08（期望）；后接 L13（T/R 未知时学 Q）、L21（多智能体 MDP/随机博弈）。
- L15 效用理论回答"R 设计对不对"。

## 5. 跨课程联系

- **6.006**：VI = Bellman-Ford 的 max-plus 代数版（每轮全边松弛）；对数变换后最短路是 2-state 无动作 MDP 特例。
- **CS229/CS285**：CS285 整门课从"MDP 已解"起步；L14 近似方法承接。
- **MIT6.824**：Raft 的领导者选择可写成"状态=任期日志"的 MDP（理论圈确有此建模练习）。
- **DDCA**：值迭代每轮是"全状态并行更新"——天然适合 GPU/脉动阵列；硬件调度器（DVFS）在线跑 VI 查找表。

## 6. 开源项目应用

- **Gymnasium `grid_world`/`FrozenLake`**：与本讲环境等价，`P` 转移矩阵直接对应。
- **Mosek/pymdptoolbox**：带约束 MDP（CMDP）求解；**CommonRL-Gym**。
- **pyMDP / rl-games**：玩具 MDP 教学库。
- 项目实战：`projects/mdp`（4x4 网格 VI+PI+策略可视化，纯标准库）。

## 7. 延伸阅读

- AIMA 4e §17.1-17.2；CS188 Note "MDPs, Dynamic Programming"；Sutton & Barto §3-4。
- Bellman《Dynamic Programming》(1957)；Howard "Dynamic Programming and Markov Processes" (1960)。
