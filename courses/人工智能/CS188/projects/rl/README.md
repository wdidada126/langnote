# 项目 5：rl —— 无模型 Q-Learning + REINFORCE（`q_learning.py`）

## 对应讲次

- **L13 强化学习 I**（TD/Q-Learning/ε-greedy）、**L14 强化学习 II**（策略梯度/baseline）。
- 与 `projects/mdp`（L12）共用同一个 4x4 网格世界——**模型已知 vs 未知** 的对照实验。
- 对应官方 Pacman Project 4/综合 RL 项目的合成环境版。

## 算法

| 组件 | 说明 |
| --- | --- |
| `sample_step` | 按 0.8/0.1/0.1 采样 (s', r)——agent 只见样本不见分布 |
| `q_learning` | 表格 Q + ε-greedy(0.2) + α=0.1，TD 误差 `r+γmaxQ'−Q`；中途输出胜率学习曲线 |
| `solve_optimal` | 内嵌值迭代（老师），用于策略一致率比对 |
| `reinforce` | 语境化赌博机上的单样本策略梯度：`θ += α·(r−b)·(1[a=act]−π)`，移动平均 baseline |

## 运行方式

```bash
cd projects/rl
python3 q_learning.py     # 或 ./run.sh / run.bat（含 py_compile 自检）
```

8000 episodes × ≤200 步纯 python 约数秒~几十秒；调低 episodes 可加速调试。

## 思考题

1. ε 从 0.2 改 0：Q 表会在陷阱边界"学错"——exploration 饥饿如何体现？
2. 把 Q 初始化为乐观值（+10 而不是 0）：exploration 行为怎样变化（optimism in face of uncertainty）？
3. REINFORCE 去掉 baseline(b=0)：收敛变慢但期望方向不变——从方差角度解释（笔记 L14）。

## 延伸阅读

- notes/L13-*.md、notes/L14-*.md；Watkins & Dayan 1992；Sutton & Barto ch.6/13；升级到深度版见 stable-baselines3/RLlib。
