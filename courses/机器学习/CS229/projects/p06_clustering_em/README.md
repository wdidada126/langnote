# p06 k-means / GMM-EM / 因子分析 / KDE（L16-L17-L22）

## 讲次与知识点
- **L16** k-means 坐标下降与单调性、k-means++ D² 初始化、MoG、EM（logsumexp 责任度、
  对数似然单调）、"球形共享 Σ ⟹ EM≡k-means"、BIC 选 k
- **L17** 因子分析 EM（条件高斯矩 E 步 + 闭式 M 步）、FA vs PCA 子空间（主角度比较、旋转不可辨识）
- **L22** 核密度估计：带宽-偏差-方差、`h*∝m^{-1/5}` 趋势

## 文件
| 文件 | 内容 |
| --- | --- |
| `kmeans.py` | 随机 vs k++ 重启、J 单调核对、各向异性簇横切灾难、肘部法 |
| `em_gmm.py` | 全协方差 GMM-EM + tied-spherical 特例 + BIC + 模糊责任度 |
| `fa_kde.py` | FA-EM（主角度验证恢复）+ KDE 带宽/m 扫描 |

## 运行
```
bash run.sh          # Windows: run.bat
python kmeans.py
python em_gmm.py
python fa_kde.py
```
依赖：**numpy（唯一第三方依赖）**。合成数据 `make_blobs_2d_clusters` 含一对 45° 长条椭圆簇——
专为演示"k-means 假设违约 → GMM 治愈"设计。

## 观察点
1. `em_gmm.py` 实验 2：把协方差锁死为共享球形，E 步 argmax 逐位等于最近中心（L16 §1.3 定理的数值证书）。
2. 实验 3：loglik 单调升 vs BIC 在 k=3 见底——无监督也要结构风险（L09）。
3. `fa_kde.py`：FA 主角度 ≈0° 而 Φ̂ 与 Φ_true 对齐——"PCA 不建模的那一半信息"被找回。
4. `kmeans.py` 实验 2：`np.diff(J)` 出现正值即你的实现有 bug（M 步未对固定分配取 argmin）。

## 可扩展实验
- MoG 的变分版（MAP + Dirichlet 先验，VB-GMM）；
- Mean-Shift 聚类（KDE 梯度爬山，L22 §1.1 预告）；
- 对 GMM 责任度做后验熵直方图 → 软聚类质量诊断。
