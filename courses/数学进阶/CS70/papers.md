# papers.md — UCB CS70 经典与前沿文献

> CS70 是"理论 ↔ 算法"的课程，本表按模块挑出对应的里程碑论文；近 5 年条目为线索，精读前请核对元数据。

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Gale & Shapley, *College Admissions and the Stability of Marriage* | 1962 | 提出稳定匹配与 GS 算法，构造性证明存在性并拿下诺奖 | L24 |
| Rivest, Shamir & Adleman, *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems* | 1978 | RSA：基于因子分解困难的非对称密码与签名 | L8, L10, L11 |
| Diffie & Hellman, *New Directions in Cryptography* | 1976 | 开创公钥密码与密钥交换概念，引入 trapdoor 函数 | L11, L12 |
| Shannon, *Communication Theory of Secrecy Systems* | 1949 | 定义完美保密、证明 OTP 与密钥长度下界 | L12 |
| Reed & Solomon, *Polynomial Codes over Certain Finite Fields* | 1960 | RS 码：有限域上多项式编码达到 Singleton 界 | L13–L16 |
| Shamir, *How to Share a Secret* | 1979 | 拉格朗日插值构造阈值秘密共享 | L13, L14 |
| Carter & Wegman, *Universal Classes of Hash Functions* | 1979 | 通用哈希族与两两独立，奠定哈希分析的代数基础 | L32 |
| Carter, Wegman et al., *The Classic Version of Universal Hashing / 负载均衡* | 1986 | "2 选择 1"（power of two choices）把最大负载降到 O(log log n) | L31, L32 |
| Erdős, *On the Evolution of Random Graphs* | 1960 | 概率方法研究图性质：存在性证明的新范式 | L19, L23 |
| Hoare, *An Axiomatic Basis for Computer Programming* | 1969 | 用谓词逻辑给程序规约，把 L4 的推理规则工程化 | L2–L4, L22 |
| Cooley & Tukey, *An Algorithm for the Machine Calculation of Complex Fourier Series* | 1965 | FFT：单位根对称性带来的分治加速 | L17 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| NIST 后量子标准化：CRYSTALS-Kyber (FIPS 203) / Dilithium (FIPS 204) / SPHINCS+ | 2022–2024 | 基于模格/哈希的公钥密码取代 RSA 的现实迁移 | L11, L12 |
| *Efficient Polynomial-Commitment Schemes*（KZG/Inner-Product 论族的后续）与 ZK-SNARK 工程 | 2021–2025 | 多项式承诺 = 插值/有限域知识的直接变现 | L13–L16 |
| Erasure-coding at scale（云存储 LRC/Regenerating code 运维论文，OSDI/NSDI/ATC 一族） | 2021–2024 | RS/LRC 码在真实数据中心的修复带宽与尾延迟优化 | L16 |
| *Locality-Sensitive Hashing / MinHash* 在 LLM 语料去重中的应用（如 ACL 2022 数据去重工作及其后续） | 2021–2024 | 用哈希冲突概率做十亿级文档相似性判定 | L31, L32 |
| 尾概率不等式的算法化使用（differential privacy 的 RDP 分析、moment accounting） | 2021–2023 | 把 Chebyshev/Chernoff 式的矩分析推广到隐私预算组合 | L30 |
| 一致性哈希与去中心化系统的负载/迁移证明（SOSP/OSDI 存储系统论文族） | 2021–2025 | 虚拟分片 + 随机性给出可证明的均衡与有界迁移 | L32, L33 |
| 匹配市场机制设计新实践（GS 算法变体：带上下界、动态配额） | 2021–2025 | 稳定匹配在疫苗分配、在线平台中的可扩展变体 | L24, L25 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 扩展欧几里得 / 模逆 / 快速幂 | `openssl/openssl`（BN_mod_*）, `GMPlib/GMP`（GNU GMP）, Rust `crypto-bigint` | RSA/ECDSA 底层大数模运算 |
| RSA 与非对称密码 | `gnupg/gnupg`, `pyca/cryptography`, `briansmith/ring` | 密钥生成、签名、混合加密 |
| 后量子密码 | `open-quantum-safe/liboqs` | Kyber / Dilithium 参考实现 |
| 秘密共享与多项式插值 | `hashicorp/vault`（Shamir unseal key sharing）, `scipy.interpolate` | 主密钥拆分、门限重构、插值实验 |
| Reed–Solomon / 纠删码 | `klauspost/reedsolomon`（Go）, `jerasure`, `intel/isa-l`, Ceph EC 后端 | 备份分片、RAID-6、QR 码、对象存储 |
| 稳定匹配 | `networkx`（含 GS/匹配算法）, `boostorg/graph` | 课程与住宿分配、拍卖清算 |
| 通用哈希与数据结构 | `abseil/abseil-cpp`（SwissTable）, `rust-lang/hashbrown`, Go `runtime/map.go` | 开放寻址 + 扰动哈希的负载控制 |
| MinHash / LSH | `ekzhu/datasketch`, `facebookresearch/faiss`, `spotify/annoy` | 近重复检测、向量近似检索 |
| 图与偏序 | `networkx`, `boostorg/graph`（BGL）, `graphviz`（DAG 拓扑排序与布局） | 依赖图、任务调度、可视化 |
| FFT / 单位根 | `FFTW`, `kissfft`, `JuliaMath/AbstractFFTs.jl` | 信号处理与大整数乘法 |
| 概率分析与尾界 | `spark`（HyperLogLog / approximate quantiles）, `DataDog/sketches-go` | 基数估计、分位数与误差保证 |
