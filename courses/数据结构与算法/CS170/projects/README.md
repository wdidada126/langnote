# CS170 配套项目计划（骨架，本轮不写代码）

课程作业是 13 次 **LaTeX 书面 hw**（无编程作业）。projects/ 因此承担两件事：
1) `hw/` 侧：LaTeX 模板与逐次作业的题目-证明骨架（`main.tex` + `references.bib`）；
2) `code/` 侧：用 Python 3.11 做小规模实验，验证复杂度趋势与近似比，建立"证明 ↔ 实验"的闭环。
约定：每个子目录自带 `build.sh`（LaTeX 用 `latexmk -pdf`，Python 用 `python -m compileall`），本轮只写不编译。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L3 分治 | Python + LaTeX | Karatsuba vs 朴素乘法计时曲线（log-log 拟合指数）；最近点对分治实现 | `latexmk -pdf`；`python -m compileall` + 计时脚本 |
| L4 下界 | Python | 决策树实验：对 n=8..11 枚举排序算法叶子数，验证 log₂(n!) 下界 | compileall；输出表格进 LaTeX |
| L5 随机化 | Python | 随机快排比较次数分布（10⁴ 次重复）+ Randomized Select 中位数误差直方图 | compileall + matplotlib 图 |
| L6–L7 图与最短路 | Python | 路网/网格上的 BFS、Dijkstra、A* 对比"扩展节点数"，含可采纳性反例 | compileall；JUnit 式 `pytest` 断言最优性 |
| L8 MST 与并查集 | Python | Kruskal + Union-Find（有/无路径压缩）在 10⁶ 边上的墙钟差；α(n) 经验曲线 | compileall + 基准脚本 `bench.py` |
| L9 贪心 | Python | 三种区间调度准则的自动反例搜索（小规模穷举找违反最优性的输入） | compileall；生成 LaTeX 反例表 |
| L10–L12 动态规划 | Python | 编辑距离（含 Hirschberg 线性空间）、0-1 背包 DP+FPTAS 误差/时间曲线、位掩码 TSP(n≤14) | compileall；`pytest` 与暴力枚举对拍 |
| L13–L14 LP 与对偶 | Python | 手写单纯形 + 用最大流的原/对偶验证互补松弛（输出对偶证书） | compileall（可选 `pip install scipy` 做对照） |
| L15–L16 网络流 | Python | Edmonds-Karp/Dinic → 二部匹配 + 棒球淘汰归约，割即"不可能性证书"打印 | compileall + 样例数据 |
| L17–L18 难解性 | Python | 3-SAT → 独立集 gadget 转换器 + 暴力求解器；子集和伪多项式 DP 实验 | compileall；随机公式回归测试 |
| L19 近似算法 | Python | 顶点覆盖（匹配/LP 舍入）、集合覆盖贪心、TSP 双倍树 vs Christofides 经验近似比 | compileall + CSV 结果 → LaTeX 图表 |
| L20 概率与哈希 | Python | 通用哈希冲突实验 + Bloom Filter FPR 与理论曲线拟合 + Mini-LSH 近邻检索 | compileall；`pytest` 校验误差界 |
| L21 数论与密码 | Python | Miller-Rabin（错误率实测）+ RSA（含 CRT 加速）+ 扩展欧几里得求模逆 | compileall；仅用实验级 512 位密钥 |
| L22 并行与量子 | Python | work-span 手工分析归并排序 + `concurrent.futures` 测加速比 vs T_∞ 预测；量子线路玩具模拟（2 qubit） | compileall |

> LaTeX 侧统一放 `hw/hw01…hw13/main.tex`，复用课程模板（cs170.org 提供 hw 模板）；每张图由 code/ 脚本产出的 CSV 生成，保证"讲义要点—证明—实验"三者可追溯。
