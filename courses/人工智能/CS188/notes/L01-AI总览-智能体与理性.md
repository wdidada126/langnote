# L01 AI 总览：智能体与理性（Rationality、PEAS）

> 对应 AIMA Ch.1-2；Klein 讲义 "Rational Agents"。全课程的总纲：后面 22 讲都是在本讲框架下填格子。

## 1. 核心概念

- **AI 的四象限**：像人思考（认知建模）/ 像人行动（图灵测试）/ 理性思考（逻辑主义）/ **理性行动**（agent 范式，CS188 主线）。
- **Agent（智能体）**：感知器 percept → 效应器 action 的映射函数 f: percepts* → actions。
  - agent program = 在物理机器上实现 f 的具体程序。
- **Rationality（理性）**：在给定感知序列下，**期望性能度量上最优**地行动——不是"全知全能"，而是在信息有限、计算有限时做最优权衡。
- **PEAS 分析**：描述任务环境的四要素
  - P（Performance measure 性能度量）、E（Environment 环境）、
  - A（Actuators 执行器）、S（Sensors 传感器）。
- **环境属性**：全观测/部分观测、单/多智能体、确定性/随机性、离散/连续、回合制/实时、 episodic/sequential。
- **Agent 类型谱**（由简到繁，恰好对应本课程模块顺序）：
  1. 直接反射型（rule-based）→ 无状态；
  2. 基于模型的反射型 → 维护世界状态 → L2-L7 搜索建模；
  3. 基于目标的 → 需要搜索/规划 → L2-L7, 规划；
  4. 基于效用的 → 概率与决策 → L8-L18；
  5. 学习型 → 从经验改进 → L11, L13-L14, L19-L20。

## 2. 关键框架（伪码）

```
function RATIONAL-Agent(percept, state, model):
    state ← UPDATE-STATE(state, percept)     # 感知→内部模型
    action ← POLICY(state)                    # L2-L7: 搜索; L12-L14: MDP/RL; L15-L16: 决策
    return action
```

理性 = argmax_action E[ PerformanceMetric | percept history, agent program ]。

## 3. 直觉例子：Vacuum World

- 环境：2 格 [A, B]，可能脏；动作：Left/Right/Suck/NoOp。
- 全观测+确定性时最优策略一行代码；**部分观测**（不知道另一格脏否）就需 belief state 或先探测再 Suck——这就是为什么需要概率（L8 起）。
- Pacman：P=吃豆得分−被鬼抓损失，E=迷宫+鬼，A=四方向移动，S=周围视野（局部可观测）。

## 4. 前后讲联系

- 本讲给出"理性 agent"分类树；L2-L7（确定性搜索）、L8-L18（不确定性与决策）、L19-L21（学习与博弈）、L22（反思）沿树展开。
- 与 L12（MDP）呼应最强：MDP 就是"sequential + stochastic + fully/partially observable"环境下的形式化。

## 5. 跨课程联系

- **6.006 / CS61B**：agent 的"决策"本质是在状态图上跑算法，复杂度视角（状态数可达 2^n，如 20 格空格棋盘 10^120）贯穿全课。
- **CS229**：CS229 从统计学习切入"学习型 agent"，本讲是它的动机课。
- **MIT6.824**：agent 在分布式系统中的对应物是"服务进程 + 环境（网络/其他节点）"，策略选择类似容错协议决策。
- **DDCA（数电）**：反射型 agent ≈ 组合逻辑电路（感知直接映射动作）；基于模型的 agent ≈ 带寄存器的时序电路——"状态"概念完全同构。

## 6. 开源项目应用

- **Gymnasium**（OpenAI Gym 社区延续）：`env.step/action_space/observation_space` 就是 PEAS 的工程化接口，本课所有项目环境均可视为迷你 Gym。
- **RLlib / stable-baselines3**：其 `Env` 抽象与本讲 agent-environment loop 一一对应。
- **pyAIMA（aimacode/aima-python）**：AIMA 官方配套代码，`agents.py` 实现了本节全部 agent 类型，可对照阅读。

## 7. 延伸阅读

- AIMA 4e Ch.1-2；Klein CS188 Note 1 "Rational Agents"。
- Russell & Norvig "Roadmap for AI"（AIMA 前言的地图）；Russell《Human Compatible》(2019) 对理性定义的当代反思。
