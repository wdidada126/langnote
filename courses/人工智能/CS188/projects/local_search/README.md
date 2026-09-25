# 项目 2：local_search —— n-皇后爬山与模拟退火（`nqueens_local.py`）

## 对应讲次

- **L04 局部搜索与优化**；对照 **L06**（n-皇后同时是 CSP 经典实例）。

## 算法

| 组件 | 说明 |
| --- | --- |
| 状态编码 | `state[i]=第 i 列皇后的行`，每列一后 → 免列冲突 |
| 增量评估 | 移动一列只需 `col_conflicts` O(n)，总冲突变化=该列冲突变化（6.006 增量/摊销视角） |
| `hill_climb` | 最陡爬山：枚举全部 n(n−1) 邻居取最优，不改善即停（局部极小） |
| `random_restart_hc` | SIDA 随机重启爬山，统计成功率 |
| `simulated_annealing` | Metropolis 接受 `exp(-Δ/T)`，几何冷却 T*=0.997，t0 随 n 缩放 |

输出：n∈{8,12,20} 时 HC 与 SA 的成功率/步数对照表 + 20-皇后解盘可视化。

## 运行方式

```bash
cd projects/local_search
python3 nqueens_local.py     # 或 ./run.sh / run.bat（含 py_compile 自检）
```

纯标准库（math/random），固定随机种子保证可复现。

## 思考题

1. 把 SA 的 alpha 调到 0.5（骤冷）与 0.999（极慢）分别看成功率——冷却调度为什么是 SA 的生命线？
2. HC 用"最陡"而非"首个改善"，重启次数需求会怎样变化？
3. 改用 min-conflicts（只随机选一个冲突皇后换行）——即数独求解器做法，与 CSP 的 L06 联系。

## 延伸阅读

- notes/L04-*.md；Kirkpatrick 1983（papers/papers.md 表一）；OR-Tools `routing` 的 SA 选项。
