# papers.md — MIT 6.042J 数学 for CS 文献

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Gale & Shapley, *College Admissions and the Stability of Marriage* | 1962 | 稳定匹配的存在性与算法，构造性证明的经典范本 | L8 |
| Hall, *On Representatives and Subsets* | 1935 | 二部图完美匹配的充要条件（Hall 定理） | L9 |
| Rivest, Shamir & Adleman, *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems* | 1978 | RSA：数论工具到密码系统的完整落地 | L12–L15 |
| Miller, *Riemann's Hypothesis and Tests for Primality* | 1976 | 在 GRH 假设下给出多项式时间素性测试（确定性） | L16 |
| Rabin, *Probabilistic Algorithm for Testing Primality* | 1980 | 随机化素性测试：允许极小错误率的实用路线 | L16 |
| Agrawal, Kayal & Saxena, *PRIMES is in P* | 2004 | 无条件多项式时间素性判定（AKS），解析数论入算法 | L16 |
| Cantor, *Über eine elementare Frage der Mannigfaltigkeitslehre* | 1891 | 对角线法证明不可数与幂集定理，可计算性理论源头 | L6 |
| Cayley, *A theorem on trees* | 1889 | 标记树计数 n^{n−2}，生成函数/双计数应用于组合 | L17–L18 |
| Euler, *Solutio problematis ad geometriam situs pertinentis*（柯尼斯堡七桥） | 1736 | 图论第一篇论文：把具体问题抽象为图与迹 | L2 |
| Kuratowski, *Problematyczny problem topologiczny* | 1930 | 平面图可由禁止子式（K5/K3,3）刻画，图论结构性定理范式 | L19 |
| Wilf, *Generatingfunctionology*（专著/论文族） | 1990 | 把生成函数系统化为组合计数标准武器 | L17–L18 |
| Knuth, *The Art of Computer Programming, Vol.1*（混合数学与生成函数章） | 1968 | 用生成函数与概率分析求解递推，算法分析范式确立 | L11, L18, L21 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| 后量子密码标准化文档与配套论文（Kyber/FIPS 203、Dilithium/FIPS 204、SPHINCS+） | 2022–2024 | 用模格/哈希替代整数分解，重写"数论困难问题"这一前提 | L15, L16 |
| 形式化数学突破：*Liquid Tensor Experiment*（Scholze 等，Lean 形式化）及其工具链论文 | 2021–2023 | 把证明当作可机器检查的对象，L1–L5 证明训练的终极工程化 | L1–L5 |
| AlphaProof / 竞赛级定理证明（DeepMind, 2024–2025） | 2024–2025 | 强化学习 + 形式化验证自动搜索证明，机器自动"做归纳证明" | L3–L5, L7 |
| 图着色与 SAT 求解新进展（着色上界算法、CDCL 规模突破的论文族） | 2021–2025 | 寄存器分配/调度等组合问题的求解能力继续提升 | L19, L11 |
| 匹配与拍卖机制的大规模实践（在线平台配额、带上下界匹配） | 2021–2025 | GS 算法在真实市场的可扩展变体与激励性质分析 | L8–L10 |
| 随机图与浓度不等式的算法应用（如 *Random walks on graphs* 与去随机化系列） | 2021–2024 | Reingold 式对数空间游走、哈希族与去随机化技术演进 | L7, L20–L22 |
| 纠删码与分布式存储中有限域算术的加速论文（ISA-L/AVX-512 优化） | 2021–2024 | GF(2^w) 上矩阵运算工程优化，把代数结构变成吞吐 | L13, L15, L18 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 良序/归纳 → 程序验证 | `leanprover/lean4`, `rocq/rocq-prover`（Coq）, `Z3Prover/z3` | 定理证明器与 SMT 求解：把证明变成可检查对象 |
| 稳定匹配 / 二部图匹配 | `networkx`（`hopcroft_karp_matching`, `gale_shapley` 示例）, `boostorg/graph`（LED/IBS 匹配） | 配额分配、任务指派、供应链撮合 |
| 偏序与拓扑排序 | `apache/airflow`, `bazelbuild/bazel`, `ninja-build/ninja` | DAG 调度、构建依赖解析与关键路径 |
| 模运算 / 大数 / 快速幂 | `GMPlib/GMP`, `openssl/openssl`（BN_* 系列）, `RustCrypto/crypto-bigint` | 密码库底层算术 |
| RSA / 素性测试 | `pyca/cryptography`, `gnupg/gnupg`, `libressl` | 密钥生成（素数采样 + Miller–Rabin） |
| 后量子密码 | `open-quantum-safe/liboqs`, `Cloudflare/circl` | Kyber / Dilithium 实现 |
| 生成函数 → 递推求解 | `sympy/sympy`（`rsolve`, `sum`）, `flintlib/flint` | 符号求解递推与组合级数 |
| 图着色 | `google/or-tools`（CP-SAT 图着色）, `networkx.algorithms.coloring` | 寄存器分配、频率/时隙分配 |
| 概率分析与哈希 | `abseil/abseil-cpp`, `rust-lang/hashbrown`, `ekzhu/datasketch` | 冲突概率、HyperLogLog/MinHash 误差界 |
| 分支过程与随机算法 | `tensorflow/probability`, `PyMC`, `numpy.random` | 随机过程建模、灭绝概率与蒙特卡洛估计 |
