# p08 玩具 RL：值迭代 → 策略迭代 → Q-learning（L20-L21）

## 讲次与知识点
- **L20** MDP 五元组与转移张量 `P[s,a,s']`、Bellman 备份、值迭代（γ 压缩映射）、
  策略迭代（`(I−γP^π)V=r^π` 线性求解 + 策略改进）、策略改进定理数值验证
- **L21** Q-learning TD 更新、ε-greedy 离策略探索、Robbins-Monro 衰减条件、
  "值迭代（已知模型）= Q-learning（采样）"的信息量对照

## 文件
| 文件 | 内容 |
| --- | --- |
| `gridworld.py` | 4×5 双出口网格 MDP（20% 打滑）+ 值迭代 + 策略迭代 + 策略字符画 |
| `qlearn.py` | Q-learning：衰减/固定超参、ε₀ 扫描、学习曲线、与 V* 的 L∞ 误差 + 胜率 |

## 运行
```
bash run.sh          # Windows: run.bat
python gridworld.py
python qlearn.py
```
依赖：**numpy（唯一第三方依赖）**——环境、转移采样、蒙特卡洛胜率全部自建，
刻意不用 Gymnasium（其 `FrozenLake` 与本环境同构，学完可移情）。

## 观察点
1. 两算法的 `‖V_vi − V_pi‖∞ ≈ 0`：不同路径同一不动点（L20 §1.2 Banach）。
2. `qlearn.py` 实验 2：ε₀=0.05 时误差反而大——不是探索越多越好，也不是越少越快（覆盖 vs 方差）。
3. 随机策略的 `V^π ≤ V*` 逐点成立——策略改进定理的免费体检。
4. 打滑 SLIP 从 0.2 调到 0：最优策略在陷阱走廊边"贴墙走"还是"绕远路"？风险敏感性出现。

## 可扩展实验
- SARSA 对照（悬崖行走版）：`max` 换 `Q[s',a']`，比较学到的路径保守性（L21 §1.2）；
- 把 `policy_evaluation` 的线性求解换成 200 次迭代备份 → 广义策略迭代（GPI）实验；
- LP 方法：用对偶单纯形（或幂迭代替代）解 `min ηᵀv s.t. v ≥ Bellman 不等式`（L21 §1.3，
  numpy-only 下可用"值迭代即近似解"做对照）。
