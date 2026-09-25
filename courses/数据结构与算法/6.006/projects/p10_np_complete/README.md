# p10 NP 完全体验（SAT & TSP）

- 对应讲次：6.006 表内 26 讲止于字符串/随机化，本项目为**衔接 6.046 L11–L15 / CS170** 的延伸件；用到本课 L08（位掩码 DP）、L09（图）、L13（口径：经验≠保证）。
- 知识点：随机 3-SAT 的可满足性阈值（α≈4.26 相变与 DPLL 代价峰）；暴力枚举 vs 回溯剪枝；TSP 的 Held-Karp O(2ⁿn²) 精确 DP、最近邻、MST 加倍 2-近似（Prim+DFS 前序+三角不等式短路）。
- 文件：`main.py`（sat_brute/sat_dpll/random_3cnf、tsp 三实现、40+25 组对拍、两张实验表）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：暴力与 DPLL 判定一致；MST 加倍实测比值 ≤2（经验 ≈1.2–1.5）；SAT 表在 α=4.25 附近可满足率穿越 0.5、节点数达峰。
- 延伸：把 3-SAT 解作为独立集 gadget 验证归约（6.046 主场）；给 TSP 加 2-opt 局部搜索对比"无保证但强"。
