# projects/ — UCB CS70 配套小项目计划（本轮只列计划，不写代码）

语言：**Python**（贴近课程 discussion）为主；数论/哈希性能实验用 **C**，让常数与量级可见。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L2–L5 逻辑与证明 | Python | `proof_check.py`：真值表 + 文法解析小型命题公式，自动判定重言式与等价 | `python proof_check.py "(a | !a)"` |
| L6–L8 模运算 | Python | `modmath.py`：扩展欧几里得、模逆、平方-乘快速幂，附正确性断言与计时 | `python modmath.py` |
| L10–L11 RSA | Python | `mini_rsa.py`：生成 512-bit RSA 密钥、加解密与签名，并演示"分解 N 即可解密" | `python mini_rsa.py`（用 `sympy` 做素性测试） |
| L13–L16 多项式与 RS 码 | Python | `rs_code.py`：在 GF(2⁸) 上实现 Reed–Solomon 编/译码，做丢包恢复实验 | `python rs_code.py --erasures 3` |
| L14 秘密共享 | Python | `shamir.py`：k-of-n 门限方案 CLI，验证 k−1 个份额信息量为 0 | `python shamir.py split/restore` |
| L20–L22 归纳与递推 | Python | `recurrence_lab.py`：递归式猜解 + `sympy` 验证（归并排序、汉诺塔、斐波那契） | `python recurrence_lab.py` |
| L23–L27 图与匹配 | Python | `stable_match.py`：Gale–Shapley + Hall 定理反例搜索（小规模穷举验证） | `python stable_match.py data.json` |
| L28–L31 概率 | Python | `dice_lab.py`：指示器变量法算期望、蒙特卡洛验证生日悖论与 Chebyshev 界松紧 | `python dice_lab.py` |
| L32 哈希与负载均衡 | C | `hash_load.c`：万能哈希族 vs 2-choice vs 随机投放，统计最大桶负载 | `gcc -O2 hash_load.c -o hash_load && ./hash_load 1000000 1000` |
| L33 随机行走 | Python | `randwalk.py`：一维/二维随机行走回归性与 hitting time 估计 | `python randwalk.py` |

约定：
- 依赖写入 `projects/requirements.txt`（numpy、sympy、matplotlib）；
- 每个脚本注释标注对应讲次与 Notes 章节；
- **本轮不写代码、不编译**，由用户后续集中执行。
