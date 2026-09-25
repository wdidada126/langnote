# CS188 配套项目总表

> 语言：**Python（仅标准库，无第三方依赖）**；仿 CS188 Pacman 风格但**全部为合成环境**，可独立运行。
> 本轮约定：**只写不编译**，各目录 `run.bat` / `run.sh` 内含 `py_compile` 自检行，集中验证时直接执行即可。
> 通用要求：Python ≥ 3.8；Windows 用 `py -3`，Linux/macOS 用 `python3`。

## 讲次 ↔ 项目 映射

| 讲次 | 主题 | 项目目录 | 核心算法 | 对应官方 Pacman Project |
| --- | --- | --- | --- | --- |
| L02-L03 | 无信息搜索 / A* | [`search/`](search/) `maze_search.py` | BFS/DFS/UCS/Greedy/A*、最近豆与 MST 启发式、bitmask 状态空间 | P1 Search |
| L04 | 局部搜索 | [`local_search/`](local_search/) `nqueens_local.py` | 最陡爬山+随机重启、模拟退火(Metropolis/几何冷却)、增量冲突评估 | （DISC 常见题） |
| L05 | 对抗搜索 | [`adversarial/`](adversarial/) `connect4.py` | Minimax、α-β 剪枝(着法排序/节点计数)、Expectimax(随机对手) | P1 多鬼版思想 |
| L09-L10 | BN 表示与推断 | [`bayes/`](bayes/) `bayes_inference.py` | 全联合枚举、变量消元(因子 restrict/multiply/sum_out)、似然加权 | P5 的确定性前置 |
| L12 | MDP | [`mdp/`](mdp/) `grid_mdp.py` | 值迭代、策略提取、策略评估+策略迭代 | P2 Pup-Transition / P3 Value Iteration |
| L13-L14 | 强化学习 | [`rl/`](rl/) `q_learning.py` | 表格 Q-Learning(ε-greedy/TD 误差)、与 L12 最优策略比对、REINFORCE+baseline | P4 Approximate Q / 综合 RL |
| （L02-L03 应用 + AIMA Ch.10-11 补充） | 经典规划 | [`planning/`](planning/) `grape_world.py` | STRIPS 式前置/效果动作模型、BFS/UCS/GBFS 状态空间规划 | — |

未配项目的讲次及理由：L01/L08/L15/L16（概念与概率地基，笔记内含手算例题）；L06-L07（CSP 练习已并入 L04 n-queens 对照与 `search` 状态空间视角，工业实践推荐直接上手 OR-Tools CP-SAT）；L11（EM 手算两硬币即可，见笔记）；L17-L18（官方 P5 粒子滤波建议以 `bayes` 的 LW 为起点自行扩展，或跑 pomegranate）；L19-L20（衔接邻课 NeuralNets-ZeroToHero / micrograd 手写反传）；L21-L23（理论/总结）。

## 统一运行方式

每个项目目录结构相同：

```
<project>/
  <main>.py     # 单文件、纯标准库、固定随机种子可复现
  README.md     # 讲次 / 算法 / 运行方式 / 思考题
  run.sh        # bash: python3 -m py_compile 自检 + 运行
  run.bat       # Windows: py -3 -m py_compile 自检 + 运行
```

单独运行某项目：`cd <project> && ./run.sh`（或 `run.bat`）；
批量语法自检（不执行）：

```bash
for f in */*.py; do python3 -m py_compile "$f"; done
```

## 学习路线建议（代码阅读顺序 = 讲次顺序）

1. `search` → 读 `graph_search`：一个函数五种算法，体会 frontier 统一视角（L02-L03）。
2. `local_search` → 把 `hill_climb` 的"最陡"改成"首个改善"，再看 `simulated_annealing` 的接受准则（L04）。
3. `adversarial` → 对照 α-β 与 minimax 根值断言，改排序看剪枝率（L05）。
4. `mdp` → 打印每轮值迭代的 V 曲面演化；把 γ 改 0.5/0.99 看策略变化（L12）。
5. `rl` → 同一环境跑 Q-learning，看它与 `mdp` 老师策略的一致率曲线（L13-L14）。
6. `bayes` → 手改消元序看最大因子，对比 pgmpy 数值（L09-L10）。
7. `planning` → 加动作/加房间做状态爆炸实验，读 Fast Downward 论文对照（补充）。

## 与官方 Pacman 项目的关系

本课程项目是**无依赖教学替身**：环境、接口命名（successors/step_cost/transitions/TD 更新）刻意贴近官方
`search.py / reinforcement.py / reasoning.py` 骨架，做完本项目再转官方 Pacman 只需替换环境与可视化。
