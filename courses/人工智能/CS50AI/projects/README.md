# CS50AI 配套项目计划

> 原则：每章一个可运行小项目，本轮只规划代码与 build 方式、不写代码。语言全部 Python（课程原生），游戏 AI 类作业对齐官方 starter。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1 Search | Python | 8-puzzle：BFS/DFS/UCS/A* 求解并对比节点扩展数 | `python puzzlesolver.py --algo astar`；`pytest test_search.py` |
| L2 Logic | Python | knowledge-based 谜题推理（knights/knaves），实现归结 + 模型检查 | `python knights.py`；官方 crosswords 作业改造 |
| L3 Uncertainty | Python | 贝叶斯网络推断（枚举 + 似然加权），做 minesweeper 概率格 | `python bayes.py --query` |
| L4 Optimization | Python | n-queens 局部搜索 + 模拟退火解 travel 类约束题 | `python nqueens.py --n 100 --anneal` |
| L5 Learning | Python (numpy/sklearn) | 手写决策树/kNN + tic-tac-toe；再实现 Nim 的 Q-learning | `python tictactoe.py`、`python nim/train_q.py` |
| L6 Language | Python | 朴素贝叶斯文本分类 + Markov 句子生成（对照 LLM 输出） | `python sentences.py` |
| L7 Perception | Python (OpenCV) | tiles 图像检索：Canny + Hough 匹配拼图块 | `python tiles.py --target img/` |
| L8 Ethics | Python | 在小数据集上复现公平性度量对比（ACC vs 群体均衡） | `python fairness_report.py` |
| 期末项目 | Python | 自选：AI 游戏/分类器/图像搜索，含设计报告 | `python final/run.py`；附 README 报告 |
