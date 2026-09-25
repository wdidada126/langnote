# projects/ — MacKay 课程配套小项目计划（本轮只列计划，不写代码）

语言：**Python**（NumPy/SciPy/Matplotlib）；压缩与译码类项目对性能敏感，可用 **C** 或 **Julia** 重写核心循环。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L4–L5 熵与 Huffman | Python | `huffman_compress.py`：自建 Huffman 编解码压缩文本，报告熵、平均码长与冗余度 | `python huffman_compress.py sample.txt` |
| L7 算术编码 | Python | `arithmetic_codec.py`：实现二进制算术编码 + 自适应概率模型，与 gzip 对比 | `python arithmetic_codec.py` |
| L2, L23 语言模型即压缩 | Python | `ngram_entropy.py`：n-gram 模型预测分布，用交叉熵估计文本熵率 | `python ngram_entropy.py --n 3` |
| L11–L15 编码与 BP 译码 | Python / C | `ldpc_bpc.py`：构造规则 LDPC，实现和积（BP）译码，画瀑布曲线（BER vs SNR） | `python ldpc_bpc.py --rate 1/2` / `gcc -O2 ldpc_bpc.c -o ldpc_bpc` |
| L9 信道容量 | Python | `capacity_blahut.py`：对 BSC/BEC/AWGN 数值求容量并验证 Blahut–Arimoto 收敛 | `python capacity_blahut.py` |
| L17–L20 图模型推断 | Python | `bayes_net_bp.py`：因子图上的精确和积 + 带环图上的近似 BP（网格 Ising） | `python bayes_net_bp.py` |
| L21 MCMC | Python | `mcmc_lab.py`：Metropolis、Gibbs、HMC 在同一目标上的有效样本量对比 | `python mcmc_lab.py` |
| L28–L29 PCA / GMM / EM | Python | `em_gmm.py`：手写 EM 拟合二维高斯混合，与 `sklearn` 对拍并画下界上升曲线 | `python em_gmm.py` |
| L30 ICA / 稀疏编码 | Python | `fast_ica.py`：FastICA 分离两路合成源 + 字典学习学 Gabor 式基 | `python fast_ica.py` |
| L24–L27 神经网络 | Python | `mdn_sin.py`：小型混合密度网络拟合多峰条件分布，对比 MSE 回归 | `python mdn_sin.py` |
| L31 HMM | Python | `hmm_viterbi.py`：前向算法 + Viterbi 做合成序列解码，画后验边际 | `python hmm_viterbi.py` |
| L37 自由能统一实验 | Python | `free_energy_check.py`：数值验证 −ln P = F + KL 分解（同一模型上三种推断方法对照） | `python free_energy_check.py` |

约定：
- 依赖写入 `projects/requirements.txt`（numpy、scipy、matplotlib、scikit-learn）；
- 每个脚本注释标明教材章号（ITILA Ch.x）；随机实验固定种子；
- **本轮不写代码、不编译**，由用户后续集中执行。
