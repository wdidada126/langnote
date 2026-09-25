# 6.046 配套项目计划（骨架，本轮不写代码）

课程本身**没有编程作业**（作业为算法设计 + 正确性证明）。因此 projects/ 的定位是：把每讲的"设计-证明"用可运行的小实验来验证直觉，并训练把算法写成清晰代码的能力。
主语言：Python 3.11（与课程板书一致）+ Markdown/LaTeX 写证明（Markdown 记录结论）。
约定：每章一个子目录（`ch08_maxflow/`），含 `README.md`（问题-算法-证明要点）、`main.py`、`build.sh`（仅创建 venv + `python -m compileall`，本轮不执行）。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L3 贪心与交换论证 | Python | 区间调度三策略对拍（最早开始/最短区间/最早结束）+ 随机反例生成器，验证只有最早结束恒最优 | `python -m compileall .`；`python main.py --trials 10000` |
| L4 生成树与并查集 | Python | Kruskal + Union-Find（带路径压缩）在 Euclidean 随机点图上的实测复杂度，拟合 c·E log V | compileall + `pytest` |
| L5 最短路 | Python | Dijkstra / Bellman-Ford / A* 三实现 + 负环检测，在小网格地图上对比扩点数量 | compileall + `pytest -q` |
| L6–L7 动态规划 | Python | 编辑距离 + Viterbi（HMM）+ 背包（DP 与 FPTAS 对比近似比/误差曲线） | compileall；`main.py --eps 0.05` 输出误差表 |
| L8–L9 最大流与归约 | Python | Edmonds-Karp 最大流 → 二分图匹配 + 棒球淘汰归约，含"割即证书"的输出 | compileall + `pytest`（对拍小规模枚举解） |
| L10 线性规划与对偶 | Python | 用单纯形（scipy.optimize.linprog）解最大流的原/对偶，打印互补松弛验证 | `python -m venv .venv && pip install scipy`（不装也可跑纯 Python 版） |
| L11–L13 NP 完全归约 | Python | 3-SAT → 独立集 gadget 转换器 + 暴力求解器，验证归约保解集 | compileall + 随机公式测试 |
| L14–L15 近似算法 | Python | 顶点覆盖（极大匹配 2-近似）+ 集合覆盖贪心，在随机图上测经验近似比与理论界差距 | compileall；输出 CSV 供绘图 |
| L16–L17 随机算法 | Python | 随机快排比较次数分布 + 100 万次 Chernoff 实验（样本均值集中性直方图） | compileall + `statistics`/matplotlib 出图 |
| L18 哈希与 Bloom Filter | Python | 自写通用哈希族（随机素数模乘）+ Bloom Filter，实测 FPR vs 理论 (1-e^(-kn/m))^k | compileall + `pytest` |
| L19 在线算法与竞争分析 | Python | 分页模拟：LRU/FIFO/Marked 在栈式访问序列上的缺页计数，画出竞争比曲线 | compileall + 序列生成脚本 |
| L20 算法博弈论 | Python | Braess 悖论小网络：随机需求下的用户均衡 vs 系统最优，计算 PoA | compileall + 蒙特卡洛 |
| L21 密码学算法 | Python | Miller-Rabin 素性测试（含 k 轮错误概率实验）+ RSA 手实现（含 CRT 加速） | compileall；密钥长度 512 位仅用于实验 |
| L22 并行与总结 | Python | work-span 手工分析归并排序/前缀扫描，并用 `concurrent.futures` 测实际加速比 vs T_∞ 预测 | compileall；`main.py --workers 1 2 4 8` |

> 证明类内容不进代码：每章 `README.md` 需保留"定理-证明骨架-反例"三小节，代码只承担验证与直觉建立。
