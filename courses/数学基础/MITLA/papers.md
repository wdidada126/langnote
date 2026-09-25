# papers.md — 线性代数（MIT 18.06）经典与前沿文献

> 说明：18.06 本身不要求论文。本表挑的是**把课程里的矩阵思想推向算法与工程**的里程碑工作。
> 近 5 年条目为骨架级线索，精读前请核对 DOI/发表信息。

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Householder, *Unitary Triangularization of a Nonsymmetric Matrix* | 1958 | 用反射变换做正交三角化，QR 分解成为数值标准工具 | L9, L10, L20 |
| Golub & Kahan, *Calculating the Singular Values and Pseudo-Inverse of a Matrix* | 1965 | 给出稳定的 SVD/伪逆算法（Golub–Kahan–Reinsch 一族） | L18, L19 |
| Eckart & Young, *The Approximation of One Matrix by Another of Lower Rank* | 1936 | 证明最优低秩近似由截断 SVD 给出 | L19 |
| Hestenes, *Methods of Iteration for Linear and Non-Linear Problems*（共轭梯度前身） | 1949/1952 | 迭代法求解大型稀疏方程组，开启现代数值线性代数 | L2, L20 |
| Lanczos, *An Iteration Method for the Solution of the Eigenvalue Problem* | 1950 | 把对称特征值问题投影到小 Krylov 子空间 | L12, L15, L20 |
| Brin & Page, *The Anatomy of a Large-Scale Hypertextual Web Search Engine* | 1998 | PageRank = 随机矩阵主特征向量，幂迭代在工业规模落地 | L13, L21 |
| Pearson, *On Lines and Planes of Closest Fit to Systems of Points* | 1901 | PCA 的原始形式：最小二乘意义下的最优低维子空间 | L10, L17 |
| Jolliffe, *Principal Component Analysis*（专著） | 1986 | 把协方差矩阵对角化系统化为数据分析的标准方法 | L15, L17 |
| Fiedler, *Algebraic Connectivity of Graphs* | 1973 | 图拉普拉斯第二小特征值控制连通性，谱聚类理论起点 | L21 |
| Turing, *Checking a Large Routine* | 1949 | 最早讨论线性方程组求解中的舍入误差，条件数概念萌芽 | L20 |

## 二、近 5 年（2021–2026）论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Halko–Martinsson–Tropp 后续与随机 SVD 工程化（如 *Randomized Numerical Linear Algebra* 综述, Tygert 等） | 2021–2023 | 用采样/草图把大矩阵特征与 SVD 降到近线性时间 | L19, L20 |
| LoRA: *Low-Rank Adaptation of Large Language Models* (Hu et al., ICLR) | 2021 | 冻结大矩阵、只学低秩增量 —— 低秩近似的直接工业应用 | L19 |
| *FlashAttention* (Dao et al., NeurIPS 2022 及其后 v2/v3) | 2022–2024 | 把注意力矩阵分块计算避免物化，本质是矩阵乘法的存储层级优化 | L2, L20, L21 |
| 大模型中的矩阵分解压缩与量化（SVD/QTIP 一族） | 2023–2024 | 用谱方法/格量化压缩权重矩阵，延续 Eckart–Young 思路 | L18, L19 |
| 二阶优化与 Hessian 近似在深度学习的复兴（K-FAC、Shampoo 等） | 2023–2025 | 用 Kronecker 积/矩阵预条件近似二阶信息，需要正定与对角化直觉 | L16, L17, L21 |
| 谱方法与图神经网络（GCN 作为谱图滤波）后续工作 | 2021–2024 | 图拉普拉斯特征基上的滤波 = 对称对角化的应用 | L15, L21 |
| 数值线性代数的 GPU/分布式实现（MAGMA、ScaLAPACK 后继、cuSOLVER 论文族） | 2021–2025 | 分块、通信避免与混合精度下的稳定性重估 | L2, L9, L20 |

## 三、知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 具体用法 |
| --- | --- | --- |
| 消元与 LU/Cholesky | `Reference-LAPACK/lapack`, `dr-issac/lsqr`（迭代最小二乘）, `libigl/eigen` | 稀疏/稠密直接求解器，优化与仿真内核的基础 |
| 正交化与 QR | `libigl/eigen`（Householder/QR）, `scipy.linalg.qr`, `xianyi/OpenBLAS` | 最小二乘与特征值算法的数值骨架 |
| 最小二乘 / 正规方程 | `scikit-learn`（`LinearRegression`, `Ridge`）, `cvxpy/cvxpy` | 线性回归、岭回归、拟合与近端算子 |
| 特征值与谱定理 | `ARPACK-ng/ARPACK-ng`（经 `scipy.sparse.linalg.eigsh`）, `petsc/slepc` | 大规模稀疏特征值、谱聚类、振动模态 |
| SVD / 低秩近似 | `facebookresearch/faiss`（PCA/量化前置）, `RandomizedSVD.jl`（Julia）, `implicit`（推荐系统） | 向量检索降维、推荐矩阵分解、图像压缩 |
| 条件数与范数 | `numpy.linalg.cond`, `Krylov.jl`, `OSQP`（预条件） | 迭代法收敛性诊断与预条件设计 |
| PageRank / 幂迭代 | `apache/spark` MLlib Graph, `networkx`, `igraph` | 中心性度量、图嵌入、链接分析 |
| 图拉普拉斯与谱聚类 | `scikit-learn` SpectralClustering, `graph-tool`, `DGL/PyG` | 社区发现、GCN 的归一化拉普拉斯 |
| 矩阵乘法分块与 Strassen | `OpenBLAS`, `BLIS`, `MAGMA`, `eigen` | CPU/GPU 上的高性能线性代数内核 |
