# projects/ — MIT 18.06 配套小项目计划（本轮只列计划，不写代码）

语言选择：**Python（NumPy）** 为主，可选 **Julia** 对照（与 18.330 共用环境）。目标是"自己实现一遍，再和库函数对拍"。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L2–L3 消元 | Python | `my_lu.py`：带行交换的高斯消元与 LU 分解，解随机方程组并与 `numpy.linalg.solve` 对比误差 | `python my_lu.py` |
| L4–L8 子空间与秩 | Python | `four_subspaces.py`：给定随机 A，数值给出 R、零空间基、行/列空间正交性验证并画图 | `python four_subspaces.py` |
| L9–L10 正交与最小二乘 | Python | `fit_house.py`：用正规方程与 QR 两种方法做多项式拟合房价数据，比较条件数与精度 | `python fit_house.py` |
| L11 行列式 | Python | `det_props.py`：用初等变换求 det，验证 det(AB)=detA·detB 与体积解释 | `python det_props.py` |
| L12–L14 特征值与幂迭代 | Python | `pagerank.py`：手写幂迭代（含 dangling node 处理）求 200 节点图 PageRank，与 `numpy.linalg.eig` 对拍 | `python pagerank.py` |
| L15–L17 对称矩阵 / PCA | Python | `pca_faces.py`：对低维数据集（或 MNIST 子集）中心化后做 PCA，画特征值谱与重构误差 | `python pca_faces.py` |
| L18–L19 SVD | Python / Julia | `svd_compress.py`：图像按奇异值截断压缩，画出 σ 衰减曲线与 5%/10% 能量重构图 | `python svd_compress.py` |
| L20 条件数 | Python | `condition_lab.py`：对病态 Vandermonde/Hilbert 矩阵比较求逆 vs QR vs SVD 的解误差 | `python condition_lab.py` |
| L21 谱方法 | Python | `spectral_cluster.py`：构造图拉普拉斯，用 Fiedler 向量做二分社区发现 | `python spectral_cluster.py` |
| 综合 | C++（可选） | `matmul_lab.cpp`：朴素三重循环 vs 分块矩阵乘，测缓存效应，呼应 15-418/CS61C | `g++ -O2 -march=native matmul_lab.cpp -o matmul_lab && ./matmul_lab` |

约定：
- 依赖集中在 `projects/requirements.txt`（numpy、matplotlib、scipy、scikit-learn）；
- 每个脚本自带 `if __name__ == "__main__"` 与中文注释说明对应讲次；
- **本轮不写代码、不编译**，由用户后续集中执行。
