# 项目 7：planning —— GrapeWorld 简化版状态空间规划（`grape_world.py`）

## 对应讲次

- **L02-L03 搜索**的直接应用；主题为经典规划（AIMA Ch.10-11，本 23 讲表的补充内容，
  csdiy 版 CS188 Spring 2024 大纲中规划未单列讲次，故挂在搜索模块下作为综合练习）。

## 模型（经典 GRAPES 世界极简版）

- 房间 A（机械手 grip + 杯子）/ B（葡萄）；机器人初始在 A。
- 状态 = (位置, 手持集合, 是否已喝到)；动作表见运行输出的 STRIPS 式前置/效果表：
  `Move(1) / PickGrip(1) / PickGrape(2, 需 grip) / Pour(3, 需 grip+grape, 消耗 grape) / Drink(1)`。
- 目标：喝到葡萄汁（done）。规划 = 状态空间上的路径搜索。

## 算法

| 规划器 | 语义 | 结果 |
| --- | --- | --- |
| BFS | 最少步数（无视动作代价） | 6 步 |
| UCS | 最小代价 = 最优计划（Dijkstra 式弹出定案） | 代价 9 |
| GBFS | `h=未完成子目标数` 启发 | 演示"非单调副作用（Pour 消耗 grape）破坏可采纳性"的活教材 |

## 运行方式

```bash
cd projects/planning
python3 grape_world.py     # 或 ./run.sh / run.bat（含 py_compile 自检）
```

## 思考题

1. 加入 `Eat`（在 B 直接吃葡萄，代价 1）后 UCS 计划变不变？（改变目标才变——目标敏感性）
2. 房间扩到 n 个成环、葡萄扩到 k 串：状态数怎么涨？（2·2^{k+2}·…——规划的状态爆炸与 L02 呼应）
3. 阅读 Fast Downward 论文：它的 h_max 如何由本域的"删除放松"算出？

## 延伸阅读

- notes/L02/L03；papers/papers.md 规划四篇（STRIPS 1971 / GraphPlan 1997 / FF 2001 / Fast Downward 2006）；
  逻辑规划延伸：SWI-Prolog（`projects/planning` 的表可写成 Prolog 规则重做一遍）。
