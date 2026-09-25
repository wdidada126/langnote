# papers.md — 信息论与熵（MIT 6.050J）

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Shannon, *A Mathematical Theory of Communication* (Bell Syst. Tech. J.) | 1948 | 定义熵与信道容量，证明信源/信道两大编码定理，创建信息论 | L2–L12 |
| Hartley, *Transmission of Information* | 1928 | 早于香农给出"信息量 = log 符号组合数"的度量 | L2, L3 |
| Huffman, *A Method for the Construction of Minimum-Redundancy编码 Codes* | 1952 | 给出最优异前缀码的构造算法，压缩的教科书方法 | L7 |
| Hamming, *Error Detecting and Error Correcting Codes* | 1950 | 系统性构造纠错码，引入汉明距离与校验位思想 | L13 |
| Golay, *Note on the Digital Coding of Waves* / BCH 码 (Bose–Chaudhuri–Hocquenghem) | 1949/1960 | 把有限域多项式引入编码，RS/BCH 代数编码路线 | L14 |
| Berger, *The Rate Distortion Function for Certain Communication Systems* (PhD/相关论文) | 1966 | 有损压缩的率失真理论框架 R(D) | L8 |
| Kolmogorov, *Three Approaches to the Quantitative Definition of Information* | 1965 | 用算法复杂度定义信息，随机性的另一条根基 | L6, L8 |
| Landauer, *Irreversibility and Heat Generation in the Computing Process* | 1961 | 证明擦除比特必产生 kT ln2 热量，信息与热力学的桥梁 | L17, L18 |
| Bennett, *Logical Reversibility of Computation* | 1973 | 可逆计算方案，说明 Landauer 下界只针对不可逆操作 | L18 |
| Zurek, *Entropy and the Second Law: Information Theory Meets Statistical Mechanics* | 1989 | 澄清香农熵与热力学熵的概念关系 | L16, L17 |
| Wyner, *The Wire-Tap Channel* | 1975 | 信息论安全（区别于计算安全）的起点 | L15 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Arikan 极化码后续工程化（5G NR 控制信道 LDPC/Polar 编码增益分析族） | 2021–2024 | 容量达成码在实际 5G/6G 信道下的落地与短码优化 | L11, L14 |
| DeepSC / 语义通信（deep joint source-channel coding 综述与系统） | 2021–2024 | 用神经网络联合信源信道编码，挑战"分离定理"在有限码长下的适用 | L6, L11 |
| 大模型压缩与熵：GPTQ/AWQ/Spectral 量化方法族 | 2022–2025 | 以信息量/敏感度视角做权重比特分配，逼近表示熵下界 | L3, L8, L11 |
| 信息瓶颈（IB）与深度学习的严格化工作（如 *Deep Learning as Information Processing* 续篇） | 2021–2023 | 用互信息刻画训练/泛化，把熵变成 ML 分析工具 | L5 |
| 可逆计算与近阈值能效论文族（adiabatic/reversible logic、超低功耗 ASIC） | 2021–2025 | 在真实工艺上验证"比特-焦耳"下限的工程逼近 | L18 |
| 存储系统中的纠删码优化（Azure/Facebook 风格 LRC、Regenerating codes 实践） | 2021–2024 | 降低修复带宽与存储放大，把代数编码跑在云规模 | L13, L14 |
| LLM 熵与困惑度分析（如 *The entropy of natural language* 一类） | 2021–2025 | 用现代模型重新估计自然语言熵率与压缩极限 | L4, L8 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 熵与压缩 | `zstd`（facebook/zstd）, `lz4`, `brotli` | 熵编码（FSE/huffman）作为通用压缩后端 |
| Huffman / 算术编码 | `webm/libvpx`, `png` (libpng deflate), `OpenEXR` (DWAA/DWAB) | 图像/视频编码的最终熵编码打包 |
| 信道编码 | `Open5GS` 生态中的 LDPC/Polar 实现, `srsRAN_4G/5G`, `libfec` | 无线基站的纠错与软判决译码 |
| 纠删码 | `BackendSDK/Azure-erasure-coding`（ISA-L）, `ceph`（Jerasure/ISA-L）, `hdfs erasure coding` | 分布式存储的可靠性与修复代价 |
| 有限域与 RS 码 | `klauspost/reedsolomon`（Go）, `jerasure` | 数据分片容灾、文件完整性恢复 |
| 互信息 / KL | `scikit-learn`（决策树信息增益、`kl_divergence`）, `PyTorch` (`nn.CrossEntropyLoss`, `kl_div`) | 特征选择、损失函数、变分推断 |
| 率失真与量化 | `ffmpeg`/`x264`/`x265` 的 QP-RD 模型, `GPTQ`/`AWQ` | 有损压缩与模型量化的比特分配 |
| 信息论安全 | `monero`（部分原语）、`libsodium`（一次性密钥/AEAD 设计讨论） | 完美保密与现代密码的边界 |
| Landauer / 能耗下限分析 | `gem5`（功耗模型）、`OpenROAD` 后端功耗估计 | 架构与芯片级能耗建模时以"比特擦除"为理论参照 |
