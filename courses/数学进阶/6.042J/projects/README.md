# projects/ — MIT 6.042J 配套小项目计划（本轮只列计划，不写代码）

语言：**Python** 为主（数论/概率模拟）；证明训练用 **Lean 4**（可选，体会"机器可检查的证明"）。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L1–L5 证明与归纳 | Lean 4 | `Proofs.lean`：把 5 个求和/不等式命题写成 Lean 证明，体验结构归纳 | `lake env lean Proofs.lean`（需 `lake update`） |
| L2, L19 图与着色 | Python | `coloring_lab.py`：贪心/回溯着色比较色数上界，对一个真实 CFG 做寄存器分配模拟 | `python coloring_lab.py cfg.json` |
| L7 鸽笼原理 | Python | `pigeon_hash.py`：给定哈希函数族统计必然冲突，验证下界 | `python pigeon_hash.py` |
| L8 稳定匹配 | Python | `gs_stable.py`：实现 Gale–Shapley，穷举小规模验证"对提议方最优"并统计不稳定对 | `python gs_stable.py men.json women.json` |
| L9 Hall 定理 | Python | `hall_check.py`：暴力枚举子集验证 Hall 条件，并与最大匹配结果对比 | `python hall_check.py` |
| L10–L11 偏序与调度 | Python | `topo_cpm.py`：DAG 拓扑排序 + 关键路径（最早/最晚开始、松弛） | `python topo_cpm.py tasks.json` |
| L12–L14 数论 | C | `modpow.c`：扩展欧几里得、模逆、平方-乘模幂，并做 10⁶ 次计时 | `gcc -O2 modpow.c -o modpow && ./modpow` |
| L15–L16 RSA 与素性测试 | Python | `rsa_prime.py`：生成密钥、加解密签名；实现 Miller–Rabin 并测错误率随轮数下降 | `python rsa_prime.py --bits 1024` |
| L17–L18 生成函数 | Python | `genfunc_recurrence.py`：用 `sympy` 从生成函数解斐波那契/卡塔兰/快排递推 | `python genfunc_recurrence.py` |
| L20–L22 概率 | Python | `expectation_sim.py`：指示器法算 balls-into-bins 期望；分支过程灭绝概率模拟 vs 不动点解 | `python expectation_sim.py` |

约定：
- 依赖写入 `projects/requirements.txt`（numpy、sympy、matplotlib、networkx）；Lean 部分单独说明 `lakefile.lean`；
- 每个文件顶部标注讲次；
- **本轮不写代码、不编译**，由用户后续集中执行。
