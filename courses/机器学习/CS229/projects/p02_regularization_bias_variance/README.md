# p02 正则化与偏差-方差（L04/L09）

## 讲次与知识点
- **L09** 偏差-方差分解恒等式、ERM/结构风险、学习曲线诊断、K-fold 选 λ
- **L02-L04** 岭回归（正规方程 + λI）、不惩罚截距惯例、GLM 骨架复用

## 文件
| 文件 | 内容 |
| --- | --- |
| `poly_ridge.py` | 实验 1 容量扫描 / 2 λ 扫描 / 3 学习曲线 / 4 5-fold CV 选 λ |
| `bv_decomp.py` | 蒙特卡洛逐项验证 `E[(h−y)²] = σ² + Bias² + Var`（按 m、deg、λ 扫） |

## 运行
```
bash run.sh    # Windows: run.bat
python poly_ridge.py
python bv_decomp.py
```
依赖：**numpy（唯一第三方依赖）**；输出全部为终端表格。

## 观察点
1. 实验 1 的 valRMSE 是否呈 U 形？最低点阶数与真函数 `sin(1.5x)` 的"有效复杂度"关系。
2. `bv_decomp.py`：m 增大时 var 缩、bias² 不动——"加数据治 variance、加容量治 bias"的数值证据。
3. 实验 4 CV 选出的 λ 与实验 2 目测谷值是否一致？不一致时说明单次 holdout 的方差（L09）。

## 可扩展实验
- 把 λ 扫描换成 L1 近端算子（soft-threshold）观察稀疏化（L04 延伸，超出本讲）；
- 对 train/val 划分做 20 次随机 seed，报告 valRMSE 的 std——理解"验证集也是一个样本"。
