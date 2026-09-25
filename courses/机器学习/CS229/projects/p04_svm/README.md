# p04 SVM：hinge 次梯度 与 简化 SMO 双路线（L06-L07）

## 讲次与知识点
- **L06** 函数间隔/几何间隔、软间隔与 C、标准化前提
- **L07** 对偶 QP、KKT 与三种 α 角色、核（linear/rbf/poly）、SMO 双变量解析更新、复杂度

## 文件
| 文件 | 内容 | 复杂度 |
| --- | --- | --- |
| `hinge_sgd.py` | 无约束等价形 `(λ/2)‖w‖² + mean hinge` 的随机次梯度；λ 扫描 + 感知机对照 | O(iters·n) 线性 |
| `smo_toy.py` | 核化对偶的玩具 SMO（m≈100）：盒约束/η 检查/b 更新/#SV 统计 | 朴素 O(m³) 级，仅教学 |

## 运行
```
bash run.sh         # Windows: run.bat
python hinge_sgd.py
python smo_toy.py
```
依赖：**numpy（唯一第三方依赖）**。`smo_toy.py` 刻意不用 QP 库——SMO 本身就是"手搓 QP 求解器"。

## 观察点
1. `hinge_sgd.py` 实验 3：感知机解的最小几何间隔 vs λ→0 的 hinge 解——"分对"与"分得最开"。
2. `smo_toy.py`：linear 核在 two-moons 上必然欠拟合（对照 L07 核动机）；rbf 的 #SV 与 test acc 随 C 变化；
   触顶 α=C 的支持向量 = 违例/边界内侧点（KKT 三角色）。
3. 两路线交叉验证：`kind='linear'` 的 SMO 解与 hinge_sgd（λ 小）方向应一致。

## 可扩展实验
- 给 SMO 加 ν-SVM 约束或 ε-SVR（回归版双侧约束，L07 作业）；
- 预计算 Gram 矩阵改 `SVC(kernel='precomputed')` 风格自定义"编辑距离核"（需字符串数据）。
