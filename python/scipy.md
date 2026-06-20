# scipy

SciPy（发音 /ˈsaɪpaɪ/，"Sigh Pie"）是 Python 生态中最核心的科学计算库，专为数学、科学、工程和数据分析设计，完全建立在 NumPy 之上，提供了大量工业级、高效、经过验证的数值算法。

### 一、核心定位与特点
- 全称：Scientific Python
- 定位：Python 科学计算的核心工具包，对标 MATLAB、GNU Octave
- 基础：强依赖 NumPy，所有数据输入输出均为 NumPy 数组 (`ndarray`)
- 语言：接口用 Python，核心算法用 Fortran / C / C++ 编写，速度极快
- 协议：BSD 开源协议，免费商用、可修改
- 特点：
  - 功能极全：覆盖数学、统计、信号、图像处理、优化、线性代数等
  - 高效可靠：算法来自 LAPACK、ODEPACK、FFTPACK 等经典库
  - 接口简洁：Pythonic API，一行代码调用复杂算法
  - 生态完整：与NumPy、Matplotlib、Pandas、Scikit-learn无缝集成

### 二、常用子模块（按领域）
SciPy按功能划分为子模块，按需导入即可：

| 子模块 | 英文 | 核心功能 | 典型用途 |
|:--- |:--- |:--- |:--- |
| `scipy.stats` | Statistics | 概率分布、统计检验 | 正态/泊松/二项分布、T检验、卡方检验、描述统计 |
| `scipy.optimize` | Optimization | 优化、求根、拟合 | 函数最小值、方程求解、最小二乘曲线拟合 |
| `scipy.linalg` | Linear Algebra | 线性代数 | 矩阵分解、特征值、线性方程组、行列式 |
| `scipy.integrate` | Integration | 数值积分、微分方程 | 定积分、ODE 求解（如物理运动方程） |
| `scipy.interpolate` | Interpolation | 数据插值 | 缺失数据补全、曲线平滑、样条插值 |
| `scipy.signal` | Signal Processing | 信号处理 | 滤波、卷积、傅里叶变换、时频分析 |
| `scipy.ndimage` | N-dimensional Image | 多维图像处理 | 滤波、边缘检测、形态学操作、重采样 |
| `scipy.fft` | Fast Fourier Transform | 快速傅里叶变换 | 频域分析、信号/图像去噪 |
| `scipy.spatial` | Spatial Algorithms | 空间几何 | 距离计算、KD树、凸包、最近邻搜索 |
| `scipy.constants` | Physical Constants | 物理常数 | 光速、引力常数、单位转换 |

### 三、与 NumPy 的关系（必懂）
- NumPy：提供数据结构（多维数组 `ndarray`）+ 基础运算（加减乘除、索引、排序）
- SciPy：提供科学算法（积分、优化、统计、信号处理），必须用 NumPy 数组
- 通俗理解：
  - NumPy = 计算器（提供数字和基础运算）
  - SciPy = 科学计算器/数学手册（提供微积分、线性代数、统计公式）

### 四、安装与基本使用
#### 1. 安装
```bash
pip install scipy numpy  # 必须同时装 numpy
```

#### 2. 基本用法（以泊松分布为例）
```python
import numpy as np
from scipy.stats import poisson  # 导入统计模块的泊松分布

# 平均发生次数 λ
lambda_ = 3
# 求 P(X=2)
p = poisson.pmf(k=2, mu=lambda_)
print(f"P(X=2) = {p:.4f}")  # 输出：0.2240
```

### 五、典型应用场景
1. 概率论/统计：你正在做的泊松分布、正态分布、假设检验
2. 机器学习：Scikit-learn 底层大量使用 `scipy.optimize`、`scipy.sparse`
3. 工程优化：求函数最小值、参数拟合、路径规划
4. 信号/音频处理：滤波、去噪、FFT 频域分析
5. 物理/力学：求解微分方程、积分、动力学模拟
6. 图像处理：医学图像滤波、图像增强、特征提取

### 六、总结
SciPy是Python科学计算的“算法引擎”。
- 做概率论、统计、数值计算，必用 `scipy.stats`、`scipy.integrate`
- 你整理的泊松分布工程，核心就是 `scipy.stats.poisson`
- 配合 NumPy（数据）+ Matplotlib（画图），就是完整科研/数据分析环境

需要我把你之前的泊松分布代码，整理成一个完整可运行的SciPy工程模板（含英文注释、README、依赖文件、绘图）吗？
