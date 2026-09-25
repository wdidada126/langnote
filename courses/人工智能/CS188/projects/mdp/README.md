# 项目 4：mdp —— 4x4 网格世界值迭代/策略迭代（`grid_mdp.py`）

## 对应讲次

- **L12 MDP**（值迭代、策略迭代、策略提取）；对照 **L02-L03**（MDP 是随机化最短路）与 **L13**（本项目给出"标准答案"，Q-learning 向它收敛）。
- 对应官方 Pacman Project 2（Pup-Transition）/ Project 3（Value Iteration）的合成环境版。

## 模型

- 状态：4x4 格去墙(1,1)/(2,2)与终端(0,3)=+10、(1,3)=−10，共 12 个非终端状态。
- 动作：N/S/E/W，0.8 执行、0.1+0.1 左右滑移（碰墙原地）——**随机性来源**。
- 奖励：步代价 −0.04 + 终端值；γ=0.95。

## 算法

| 组件 | 说明 |
| --- | --- |
| `value_iteration` | Bellman 最优算子反复赋值，报告收敛迭代数与最大变化量 |
| `policy_extraction` | 对 V* 每状态一次贪心（笔记强调：提取=每状态一个 argmax） |
| `policy_evaluation` | 固定 π 的 Bellman 期望方程迭代求解 V^π |
| `policy_iteration` | 评估+改进交替；与 VI 策略做一致率比对 |

## 运行方式

```bash
cd projects/mdp
python3 grid_mdp.py     # 或 ./run.sh / run.bat（含 py_compile 自检）
```

## 思考题

1. 把 γ 从 0.95 降到 0.5，最优策略在陷阱附近如何变化？（短视/远视）
2. 把滑移概率改为 0（确定性世界），值迭代是否等价于 6.006 的 Bellman-Ford？
3. 策略迭代轮数 vs 每轮评估迭代数——为什么 PI"次数少每次贵"？

## 延伸阅读

- notes/L12-*.md；Sutton & Barto ch.4；Bellman 1957 / Howard 1960（papers/papers.md）。
