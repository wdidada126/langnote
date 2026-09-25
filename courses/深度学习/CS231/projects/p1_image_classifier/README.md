# P1 · Image Classifier（kNN + 线性 SVM + softmax）

> 对应讲次：L01（管线与数据划分）、L02（kNN/线性分类器/hinge/softmax）、
> L03（SGD/动量/权重衰减/梯度检查）、L04（为 MLP 铺垫）。
> 对标课程作业 Assignment 1 的第一部分（纯 numpy、无框架）。

## 知识点 ↔ 文件

| 文件 | 知识点 | 讲次 |
| --- | --- | --- |
| `data.py` | 合成 blobs、train/val/test 三分、零中心化/归一化、偏置列 | L01, L02 |
| `knn.py` | kNN、向量化成对距离、验证集选 k/度量 | L02 |
| `svm.py` | 多分类 hinge 损失、次梯度、循环版 vs 向量化版 | L02, L03 |
| `softmax.py` | 数值稳定 softmax、`(P-onehot)/N` 梯度、SGD+momentum+L2 | L02, L03 |
| `gradient_check.py` | 中心差商梯度检查 | L03 |
| `main.py` | 完整管线：检查 → 网格调参（只看 val）→ 终报 test | L01-L03 |

数据为 numpy 合成的 4 类高斯团簇（192 维 = 8×8×3 像素拉平），**不下载任何数据集**。

## 运行

需要 Python ≥ 3.8 与 `numpy`。

- Linux / macOS：
  ```bash
  ./run.sh          # 语法检查模式：python3 -m py_compile 全部 .py
  python3 main.py   # 实际运行演示（需已 pip install numpy）
  ```
- Windows：
  ```bat
  run.bat           :: 语法检查模式
  python main.py    :: 实际运行
  ```

`run.sh` / `run.bat` 只做 `python -m py_compile` 语法校验（本轮工程"只写不编译"，
不执行训练），运行演示请自行安装 numpy 后直接执行 `main.py`。

## 你会观察到

1. kNN 在 192 维上距离退化，准确率有限，且每次预测 O(N·D)；
2. softmax 梯度检查相对误差 ~1e-10（OK），SVM hinge 因次梯度仅近似；
3. lr 太小时 300 步欠拟合、太大时 loss 震荡（L03 曲线重现）；
4. 同一数据上 SVM 与 softmax 验证/测试准确率接近，但收敛行为不同。
