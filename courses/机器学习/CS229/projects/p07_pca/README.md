# p07 PCA / 特征分解 / ICA / 谱聚类（L08-L18）

## 讲次与知识点
- **L08** PCA 两种解法（协方差 eigh ⟺ SVD）、中心化、解释方差、重构-投影互补、白化
- **L18** FastICA（负熵/log cosh 非线性、符号与排列不可辨识、高斯源无解）、
  谱聚类（RBF 图、`L_sym = I − D^{-1/2}WD^{-1/2}`、行归一化 + k-means、Ncut）
- 跨讲协同：PCA 去噪助产 k-means（对接 p06）

## 文件
| 文件 | 内容 |
| --- | --- |
| `pca.py` | 双路径一致性、未中心化之害、互补恒等式、白化条件数、PCA×k-means |
| `ica_spectral.py` | 正弦×方波鸡尾酒会（对齐相关矩阵 + 峰度）、双半月谱切分（σ 扫描） |

## 运行
```
bash run.sh          # Windows: run.bat
python pca.py
python ica_spectral.py
```
依赖：**numpy（唯一第三方依赖）**；通过 `sys.path` 复用 p06 的 `kmeans` 与本项目 `pca`。

## 观察点
1. `pca.py` 实验 5：8 维噪声把信噪比稀释后 k-means 一致率崩塌，PCA-1D 复原——维度灾难的欧氏距离表达。
2. `ica_spectral.py`：对齐矩阵每行每列恰一个大值（≈1）；把方波换成高斯重跑 → 得分跌到随机水平（L18 定理）。
3. 谱聚类 σ 三联扫描：碎图 → 恰够 → 完全图，λ₂（Fiedler 值）同步由大变小。

## 可扩展实验
- 核 PCA（`K_centered` 的特征分解，对"同心圆"数据 vs 线性 PCA）；
- TruncatedSVD 在合成词袋上的稀疏版 PCA；
- 随机投影（Johnson-Lindenstrauss）对比 PCA 去噪的距离保持率。
