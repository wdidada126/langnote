# UCB CS188: Introduction to Artificial Intelligence 学习笔记（【CORE】完整版目录）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | CS188: Introduction to Artificial Intelligence |
| 学校 | UC Berkeley（伯克利） |
| 主讲 | Dan Klein、Sergey Levine 等（课程 notes 由 Klein 主笔，质量极高） |
| 教材 | Artificial Intelligence: A Modern Approach（AIMA，Russell & Norvig，第 3/4 版） |
| csdiy 路径 | `人工智能/CS188: Introduction to Artificial Intelligence`（页面更新：2025-03-23） |
| 最新期次 | Spring 2024（最新一期视频与资料完整、开放旁听 Gradescope；6 个 Pacman Project） |
| 状态 | 全量（2026-09）：notes 23 讲、papers/papers.md、projects 7 项（纯 Python 标准库，run.bat/run.sh 含 py_compile 自检）均已完成 |
| 难度/学时 | csdiy 标注 🌟🌟🌟，约 50 小时；先修：CS70；语言 Python |

## 为什么学

- 伯克利人工智能入门课，课程 notes 写得非常深入浅出，基本不需要观看视频即可自学。
- 内容按经典教材 AIMA 章节顺序展开：搜索与剪枝 → 约束满足 → MDP → 强化学习 → 贝叶斯网络 → 隐马尔可夫 → 基础机器学习与神经网络，知识地图完整。
- 目前 Spring 2024 是最新一期视频与资料完整、开放旁听 Gradescope 的版本，可在线完成书面作业并实时得到测评结果。
- 6 个 Project 质量爆炸，围绕经典吃豆人（Pacman）小游戏：用学到的 AI 知识实现算法，让吃豆人在迷宫里自由穿梭、躲避鬼怪、收集豆子。
- 是 CS50AI 的理论深化版，也是 CS189（ML）、CS285（深度 RL）的官方先修与知识接口。

## 先修与知识联系

| 方向 | 关联课程/知识 |
| --- | --- |
| 先修 | CS70（离散数学与概率论）、CS61A/CS50P 级别 Python |
| 轻量平替/先导 | CS50AI（同主题广度版，编程更浅）；NeuralNets-ZeroToHero（补 L8-L9 神经网络从零实现） |
| 后续 | CS189（机器学习深化，官方建议先修含 CS188）、CS285（深度强化学习，承接 MDP/RL 部分） |
| 横向 | CS189/CS229 承接概率与学习部分；数学基础依赖 CS70 概率与 CS126 |
| 知识输出 | 搜索/A* → 路径规划（ROS/游戏 AI）；MDP/RL → Gymnasium/SB3；HMM/贝叶斯 → pgmpy/语音与生物信息 |

## 最新年份讲义全章节目录（对应 Spring 2024 课程排课 + AIMA 章节）

| 讲次 | 标题 | 阅读材料（AIMA 章节） |
| --- | --- | --- |
| L1 | AI 总览：智能体与理性（Rationality、PEAS） | AIMA Ch.1-2 |
| L2 | 搜索 I：无信息搜索（BFS/DFS/UCS/DFS-TW） | AIMA Ch.3 |
| L3 | 搜索 II：启发式搜索、A*、一致性与支配性 | AIMA Ch.3 |
| L4 | 局部搜索与优化：爬山、模拟退火、遗传算法 | AIMA Ch.4 |
| L5 | 对抗搜索：Minimax、α-β 剪枝、.expectimax | AIMA Ch.5 |
| L6 | 约束满足问题 CSP：回溯、MRV/FC、AC-3 | AIMA Ch.6 |
| L7 | CSP 进阶：树结构分解、GAC、局部推理 | AIMA Ch.6；补充讲义 |
| L8 | 概率基础：条件概率、贝叶斯、随机变量与期望 | AIMA Ch.12-13 |
| L9 | 贝叶斯网络：表示、D-separation、条件独立 | AIMA Ch.14 |
| L10 | 贝叶斯推断：枚举、变量消元、似然加权 | AIMA Ch.15 |
| L11 | 朴素贝叶斯与特征模型；EM/最大似然入门 | AIMA Ch.21 |
| L12 | 马尔可夫决策过程 MDP：值迭代、策略迭代 | AIMA Ch.17 |
| L13 | 强化学习 I：无模型学习、Temporal-Difference、Q-Learning | AIMA Ch.21 |
| L14 | 强化学习 II：近似 Q-Learning、策略搜索/Policy Gradient | AIMA Ch.21；延伸 RL |
| L15 | 价值与效用：效用理论、效用弹性、决策网络 | AIMA Ch.16 |
| L16 | 值 of 信息与感知：VoI、决策论应用 | AIMA Ch.16 |
| L17 | 隐马尔可夫模型 HMM：滤波、平滑、Viterbi | AIMA Ch.15 |
| L18 | 采样与粒子滤波：似然加权、Bootstrap/Particle Filter | AIMA Ch.15；补充讲义 |
| L19 | 机器学习与感知机：分类、决策边界 | AIMA Ch.18；CS189 衔接 |
| L20 | 神经网络与深度学习导论：前馈、反向传播 | AIMA Ch.22；延伸 DL |
| L21 | 游戏理论与多智能体：纳什均衡、极小极大 | AIMA Ch.17 |
| L22 | 哲学与 AI 伦理：图灵测试、意识、AI Safety | AIMA Ch.26-27 |
| L23 | 课程回顾与总结 | 全讲义串讲 |

> 6 个 Project（Pacman 主题）：P1 Search（路径搜索）、P2 Pup-Transition（MDP 建模）、P3 Value-Iteration（值迭代）、P4 Approximate-Q-Learning（特征 Q-Learning）、P5 Tracking（HMM 粒子滤波）、P6 Reinforcement-Learning/Projects 综合；DISC 讨论题 + 在线书面作业走 Gradescope。具体以 Spring 2024 课程网站为准。本仓库配套替代项目见 `projects/README.md`（7 个纯 Python 合成环境项目，讲次映射齐全）。

## 课程资源（摘自 csdiy）

- 课程网站：Spring 2024（eecs.berkeley.edu / inst.eecs 公开课页）
- 课程视频：每节课链接详见课程网站；YouTube 有历史完整版
- 课程教材：Artificial Intelligence: A Modern Approach
- 课程作业：在线测评书面作业和 Projects，详见课程网站
- Notes：Klein 编写，深入浅出，可独立自学
