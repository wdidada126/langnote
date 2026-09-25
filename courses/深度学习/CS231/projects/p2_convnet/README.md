# P2 · ConvNet（naive→fast 卷积、BatchNorm、小型 CNN 训练循环）

> 对应讲次：L04（反向传播）、L05（卷积/池化/尺寸公式/im2col）、L06（BN 与架构积木）、
> L07（训练策略：初始化/学习率/早停）。对标 Assignment 2 的 `fast_layers.py` +
> `layers.py` + `cs231n/classifiers/cnn.py`（numpy 部分）。

## 知识点 ↔ 文件

| 文件 | 知识点 | 讲次 |
| --- | --- | --- |
| `data.py` | 程序化绘制形状合成数据（位置/尺度/亮度抖动考验卷积先验） | L05 |
| `layers.py` | affine/relu/softmax 层、spatial BN 前反向、naive 4 重循环卷积、im2col+GEMM 快速卷积、max-pool 前反向 | L04-L06 |
| `model.py` | CONV→BN→ReLU→POOL ×2 + FC：手动逐层反传装配、He 初始化、SGD+momentum | L05-L07 |
| `gradient_check.py` | naive vs fast 等价性、模型端到端数值梯度检查 | L05-L07 |
| `main.py` | 等价性 → 检查 → 快慢计时 → 短训练循环 | 全流程 |

数据全部由 numpy 合成（16×16 圆/方/十字），**不下载数据集**。

## 运行

需要 Python ≥ 3.8 与 `numpy`。

- Linux / macOS：`./run.sh`（py_compile 语法校验）→ `python3 main.py`（真实演示，CPU 秒级）
- Windows：`run.bat` → `python main.py`

## 观察与练习

1. `naive-vs-fast` 各项相对误差应为 ~1e-15，且 fast 明显更快（batch 越大差距越大）；
2. BN 的 `g1` 梯度检查通过 = 你真正理解了 1/N 交叉项（L06 难点）；
3. 把 `model.py` 里 BN 顺序挪到 ReLU 之后（CONV→ReLU→BN）会怎样？—— 原版 ResNet 就这么干，训练更慢；
4. 加深到 3 个 conv 块后 val 准确率不升反降？—— 这正是 L06 残差连接要解决的"退化"问题。
