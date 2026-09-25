# p01 线性/逻辑回归 + 梯度下降家族（L01-L03）

## 讲次与知识点
- **L01** 监督学习设定（`common.py` 的数据生成即假设空间样本）
- **L02** LMS 损失/梯度、batch GD、SGD（洗牌+衰减 lr）、正规方程、`inv/solve/lstsq/pinv` 数值对比、高斯噪声 MLE 解释
- **L03** 交叉熵（稳定 log 域实现）、GD vs Newton/IRLS、类不平衡诊断、log-sigmoid 下溢
- 专题：**学习率 × 动量实验**（`gd_momentum.py`，含 α>2/λmax 发散演示与 β 记忆窗口）

## 文件
| 文件 | 内容 |
| --- | --- |
| `common.py` | 合成数据（良态/病态回归、各向同性/各向异性 blob）、标准化、ASCII sparkline |
| `linear.py` | 实验 L02 四连：GD/SGD/正规方程、条件数、数值解法、σ̂² |
| `gd_momentum.py` | L02 §1.2：α 网格 + momentum β∈{0,0.9,0.98} 曲线 |
| `logistic.py` | L03：GD vs Newton-IRLS 收敛、不平衡、数值稳定 |

## 运行
```
cd projects/p01_linear_logistic
bash run.sh        # 或 Windows: run.bat
# 手动：python linear.py && python gd_momentum.py && python logistic.py
```
依赖：**numpy（唯一第三方依赖）**，绘图用终端 ASCII，不引入 matplotlib。

## 观察点（对照 notes）
1. `gd_momentum.py` 中 α=2.2/L 是否如理论发散？β=0.98 为何震荡？
2. `logistic.py` 实验 1：Newton 通常 <10 步到 1e-8，GD 400 步仍未到——为什么逻辑回归"没有闭式解却有超快二阶法"？
3. 把 `make_blobs_2d(anisotropic=True)` 接入 `logistic.py`，边界仍线性——与 p03 的 GDA 崩塌对照（L05）。

## 可扩展实验（L23 报告素材）
- mini-batch 大小 {1, 32, 全量} 的"单位墙钟时间-损失"曲线；
- λI 对角加载量 vs 条件数的数值稳定性扫描；
- 用 `logistic.py` 的 θ 复算 GDA 闭式参数验证 L05 §1.2 等价性。
