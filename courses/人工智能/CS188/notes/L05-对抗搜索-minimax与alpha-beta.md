# L05 对抗搜索：Minimax、α-β 剪枝、Expectimax

> 对应 AIMA Ch.5；Klein 讲义 "Adversarial Search"。项目 `projects/adversarial`（Connect4）实现本讲。

## 1. 核心概念

- **多智能体 + 竞争**：对手也理性 → 不能假设它"帮你"，取最坏情况。零和、完全信息、回合制。
- **Minimax**：MAX 层取 max、MIN 层取 min 的递归博弈树求值；叶子用 eval 函数（非终局即启发式估值——L03 的 h 在博弈中的化身）。
- **Expectimax**：机会节点（掷骰子/随机鬼）取概率加权平均；**不能剪枝**（无有序界可传播，只有 CUTOFF 上下界技巧）。
- **α-β 剪枝**：minimax 值不变前提下剪掉无关子树。
  - α = MAX 已保证的下界；β = MIN 已保证的上界；α ≥ β 时剪。
  - 最佳次序（先搜最好的着法）：复杂度从 O(b^m) 降到 O(b^{m/2})——等效深度翻倍。

## 2. 关键伪码

```
function ALPHA-BETA-SEARCH(s, α=-∞, β=+∞, depth):
    if TERMINAL(s) or depth==0: return EVAL(s)
    if MAX node:
        v ← -∞
        for a in ACTIONS(s):
            v ← max(v, ALPHA-BETA-SEARCH(succ(s,a), α, β, depth-1))
            α ← max(α, v); if α ≥ β: break
        return v   # (MIN 层对称，用 β)
```

- **Shannon 数**：国际象棋博弈树 ~10^120，无法穷尽 → 深度限制 + 评估函数是工程必然（Deep Blue/AlphaZero 皆然）。

## 3. 直觉例子

- Tic-tac-toe 可完整 minimax 求解（先手最优 = 平局）；Connect4 深度 6-7 的 α-β 已可实战（本项目）。
- Pacman 随机鬼：用 expectimax 对鬼的均匀随机动作取期望，比 minimax 的"假设鬼完美"更符合实际。

## 4. 前后讲联系

- 前承 L03（eval≈启发式）；后接 L21（随机化/多智能体博弈论，minimax 是零和特例）、L12（MDP 是"对手=环境分布"的 expectimax 无限地平线版）、L14（AlphaZero：policy 做 move ordering + value 做 eval + MCTS 搜索）。

## 5. 跨课程联系

- **6.006**：α-β 是"分支限界 branch-and-bound"的典型实例（与背包/排程同一框架）。
- **CS229/CS231n**：AlphaZero/Stockfish NN eval = 学习的评估函数；LLM 时代 ReFT/RLHF 中的对手是奖励模型（可视为博弈视角）。
- **MIT6.824**：博弈树评估天然可并行（如 Fischer 并行 α-β）——剪枝依赖搜索顺序 ⟹ 并行化难点类似"顺序依赖导致共识困难"。
- **DDCA**：α-β 的界传播像比较器链/裁剪电路（clip 单元），硬件加速器直接固化 min/max 树。

## 6. 开源项目应用

- **python-chess** + 自制 α-β/Quiescence 引擎；**Stockfish**（NNUE eval）、**GNU Backgammon**（双路 expectimax 的巅峰）。
- **OpenSpiel**（DeepMind）：统一接口跑 minimax/α-β/MCTS 于数百种博弈。
- **MCTS/UCT**：`projects/adversarial` 可扩展 UCT 对照 α-β。

## 7. 延伸阅读

- AIMA 4e §5.2-5.6；CS188 Note "Adversarial Search / Alpha-Beta Details"。
- Shannon "Programming a Computer for Playing Chess" (1950)；Knuth & Moore α-β 分析 (1975)；Silver et al. AlphaZero (Science 2018)。
- 项目实战：`projects/adversarial`（Connect4：minimax vs α-β 节点计数对比）。
