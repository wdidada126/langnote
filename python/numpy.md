# numpy

https://numpy.org/doc/

array()

sum()

NumPy 本质上也是 Python 对底层 C 代码的绑定（Binding）。

NumPy 并非纯 Python 库，其核心是一个 C 语言扩展模块。它的性能关键部分，比如多维数组对象（ndarray）和底层的数值运算，都是用 C 语言实现的。

https://github.com/edidada/test_py_numpy

### NumPy 2.0.0 官方网址与功能速览

官方发布说明（Release Notes）：
https://numpy.org/doc/2.0/release/2.0.0-notes.html 

版本发布日期：2024 年 6 月 16 日 

这是 NumPy 自 2006 年以来的首个重大版本（major release），包含大量新功能与破坏性变更 。

### 核心新功能

1. 新的字符串 DType 与 `numpy.strings` 命名空间

引入了可变长度的 `StringDType`，并新增 `numpy.strings` 命名空间，提供高性能的字符串操作 ufunc 。

2. FFT 支持 float32 和 longdouble

所有 `numpy.fft` 函数现在都支持 `float32` 和 `longdouble` 类型 。

3. 全面支持 Array API 标准

主命名空间（`numpy.*`）现已兼容 Array API 标准（v2022.12），新增了 13 个标准别名（如 `acos`、`asin`、`atan2`、`concat`、`permute_dims` 等），以及 `isdtype`、`astype`、`unique_all`、`unique_counts`、`unique_inverse`、`unique_values` 等标准函数 。

4. 新的 dtype：`numpy.long` 与 `numpy.ulong`

新增了映射到 C 语言 `long` 和 `unsigned long` 的整数类型 。

5. `numpy.linalg` 新函数

新增 `numpy.linalg.diagonal`、`numpy.linalg.trace` 和 `numpy.linalg.svdvals`（后者等价于 `svd(x, compute_uv=False)`）。

6. 新的 tracing 与 introspection API

新增 `numpy.lib.introspect.opt_func_info`，可以追踪和查询当前 CPU 启用了哪些 SIMD 优化内核 。

7. 性能改进

排序函数（`sort`、`argsort`、`partition`、`argpartition`）使用 Intel x86-simd-sort 和 Google Highway 库进行了加速，在支持的硬件上可获得大幅提速；macOS 上支持 Accelerate 框架，线性代数运算性能显著提升，且二进制 wheel 体积缩小约 3 倍 。

---

### 重要变更（破坏性）

1. Python API 清理

约 100 个主命名空间成员被移除或迁移，主命名空间对象数量减少约 10%。例如 `np.float_` 改用 `np.float64`，`np.cast` 改用 `np.asarray`，`np.alltrue` 改用 `np.all`，`np.geterrobj`/`np.seterrobj` 改用 `np.errstate` 上下文管理器 。

2. C ABI 破坏

所有依赖 NumPy C API 的下游包必须重新编译才能兼容 NumPy 2.0。使用旧版 ABI 的包在导入时会报 `ImportError` 。

3. 类型提升规则变更（NEP 50）

采纳 NEP 50，修复了此前类型提升行为依赖输入数据值（而非仅依赖 dtype）的问题。这可能导致混合 dtype 运算的输出 dtype 和精度发生变化 。

4. Windows 默认整数类型变更

Windows 上的默认整数类型从 `int32` 改为 `int64`，与其他平台保持一致 。

5. 最大维度数扩展

数组最大维度数从 32 扩展到 64 。

6. `copy` 关键字语义变更

`asarray` 和 `array` 的 `copy` 参数现在支持 `True`（始终复制）、`False`（从不复制，需要时抛 `ValueError`）、`None`（仅在必要时复制）。

7. 支持的 Python 版本

仅支持 Python 3.9 至 3.12 。


### 补充说明

由于 2.0.0 是重大版本，官方专门提供了 《NumPy 2.0 迁移指南》（Migration Guide），列出了所有 API 移除项及其替代方案，建议升级前务必查阅 。

一句话：NumPy 是 Python 科学计算的“地基”，几乎所有数据分析、机器学习、工程计算库都直接或间接依赖它。

它的核心使命就一件事：让 Python 能像 MATLAB 一样高效地做数组和矩阵运算。

### 它主要解决什么问题？

1. 高性能多维数组（`ndarray`）

Python 原生的 `list` 做数值计算又慢又占内存。NumPy 提供了一个 `ndarray` 对象，底层是连续内存块 + C 语言实现，运算速度可以快几十到上百倍。

```python
import numpy as np

# Python list 需要循环
a = [1, 2, 3, 4]
b = [i * 2 for i in a]

# NumPy 直接向量化运算
a = np.array([1, 2, 3, 4])
b = a * 2  # 一行搞定，底层是 C 循环
```

2. 向量化运算（Vectorization）

不用写 `for` 循环，直接对整个数组做加减乘除、三角函数、指数对数等运算。这是 NumPy 最核心的价值。

3. 线性代数

矩阵乘法、求逆、特征值、SVD、解线性方程组等，`numpy.linalg` 全包了。底层调用 BLAS/LAPACK 这类高度优化的库。

4. 随机数生成

`numpy.random` 提供了各种概率分布的随机采样（正态、泊松、均匀等），是做模拟和统计的基础。

5. 广播（Broadcasting）

不同形状的数组可以自动对齐做运算，不用手动扩展维度，极大简化了代码。

6. 索引与切片

比 Python list 更强大的索引方式，支持布尔索引、花式索引、多维切片，数据筛选非常方便。

7. 傅里叶变换、统计、排序、IO

`numpy.fft`、`numpy.stats`（部分）、`numpy.sort`、`numpy.save/load` 等，覆盖了科学计算的常见需求。

### 它在生态里的位置

NumPy 是整个 Python 科学计算栈的底层依赖：

| 上层库 | 用途 | 与 NumPy 的关系 |
|---|---|---|
| Pandas | 表格数据分析 | 底层用 ndarray 存储 |
| SciPy | 科学计算（优化、积分、信号） | 直接基于 NumPy |
| Matplotlib | 绘图 | 输入输出都是 ndarray |
| scikit-learn | 机器学习 | 数据格式就是 ndarray |
| PyTorch / TensorFlow | 深度学习 | API 设计模仿 NumPy |
| OR-Tools / PuLP | 优化求解 | 数据准备常用 NumPy |

没有 NumPy，这些库要么不存在，要么得各自重造轮子。

### 一句话总结

NumPy 不是“某个科学计算工具”，而是 Python 做科学计算的“通用语言”和“性能底座”。 你用它来准备数据、做数值运算、处理矩阵；然后把这些数组喂给 Pandas 分析、喂给 sklearn 训练、喂给 Matplotlib 画图。