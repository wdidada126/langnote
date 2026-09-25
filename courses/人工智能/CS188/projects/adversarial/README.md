# 项目 3：adversarial —— Connect-4 对抗搜索（`connect4.py`）

## 对应讲次

- **L05 对抗搜索：Minimax、α-β、Expectimax**；对照 **L21**（零和博弈与极小极大）。

## 算法

| 组件 | 说明 |
| --- | --- |
| 棋盘 | 6x7 列栈表示，落子 append / 悔棋 pop（原地撤销免拷贝） |
| `evaluate` | 4 连窗口计分 + 中心控制——评估函数即 L03 启发式的博弈版 |
| `best_move_minimax` | 深度受限 minimax（悲观对手） |
| `best_move_alpha_beta` | α-β 剪枝，中心优先着法排序近似"最佳次序"；`assert` 与 minimax 根值一致 |
| `expectimax` | P2 为均匀随机对手（Pacman RandomGhost 假设），机会节点取期望、不可剪枝 |

输出：深度 3-5 的评估节点数对比表（α-β 节省量≈指数减半；代码里放开 depth=6 需数十秒，属预期现象）、α-β vs 随机自博弈终盘、expectimax 与 minimax 同局面选点差异。

## 运行方式

```bash
cd projects/adversarial
python3 connect4.py     # 或 ./run.sh / run.bat（含 py_compile 自检）
```

纯标准库。depth=6 的纯 minimax 约需十几秒以上，属预期现象（b^d 爆炸本身即教学点）。

## 思考题

1. 关掉着法排序（改为列号序），α-β 节点数增加多少？验证"最佳次序 b^(d/2)"论断对次序的依赖。
2. 把 `terminal_value` 的 `INF - ply` 改成固定 `INF`，引擎会怎样"偷懒"？（快赢偏好消失）
3. 给 expectimax 加概率（对手 70% 贪心 30% 随机），选点如何变化——对应 Pacman P1 的 Ghost 类型。

## 延伸阅读

- notes/L05-*.md；papers/papers.md：Shannon 1950、Knuth & Moore 1975；Stockfish/OpenSpiel 对照。
