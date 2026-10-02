# 概念专篇：NumPy 内存布局与向量化

> 跨章概念：与第 3 章（列表/元组）、第 6 章（矩阵与向量计算）、第 11 章（省内存）强相关。
> 校准到 2026（NumPy 2.0）。

## 1. 连续内存为何快

`np.ndarray` 是**单块连续内存** + `dtype` + `stride` + `shape`。好处：
- CPU 缓存预取命中高（顺序访问相邻字节）。
- 向量化算子（ufunc）在 C 层一次循环，无逐元素解释器开销。
- SIMD（AVX 等）可被 BLAS 利用。

对比 `list of lists`：指针数组的数组，每行独立分配、非连续、每元素 `PyObject*`，缓存差且解释器逐元素开销大。

## 2. 视图 vs 拷贝（Copies and Views）

- 切片、`transpose`、`reshape`（多数情况）返回**视图**（共享缓冲，零拷贝）。
- `np.copy`、类型转换（`astype`）、`np.array(..., copy=True)` 产生**拷贝**。
- 原地操作（`+=`、`out=` 参数、`arr *= 2`）避免临时数组，省内存与带宽。

```python
# 教学示意，不参与构建
import numpy as np
a = np.arange(1_000_000.0)
b = a[::2]            # 视图，零拷贝
c = a + b * 2         # 两个临时数组 + 结果
np.add(a, b * 2, out=a)  # 原地，省临时
```

## 3. 广播（Broadcasting）

不同形状自动对齐（从尾部维对齐，维长为 1 或相等则广播），免显式 `tile`/复制，省内存。规则：尾维对齐、缺失维补 1、长度为 1 的维拉伸。

## 4. NumPy 2.0 须知（2024+）

- 移除大量 1.x 别名：`np.float`/`np.int`/`np.bool` 等 **已删除**，改用 `np.float64`/`np.int64`/`np.bool_`。
- NEP 50 类型提升规则更严格可预测。
- `numpy.typing.NDArray[np.float64]`（3.9+）做类型标注。
- 与 Pandas 2.x（默认 PyArrow 后端）、Polars 协同：列式/Arrow 内存同样追求连续与零拷贝。

## 5. 常见误区

- 误：认为「向量化一定快」——小数组 ufunc 调用开销可能盖过收益；超大数组受内存带宽限制。
- 误：`np.array(list_of_lists)` 不指定 dtype 得到 `object` 数组，毫无性能优势。
- 误：链式 `a+b+c+d` 反复产生临时数组；用 `np.add(..., out=)` 或 `numexpr` 合并。
- 误：盲目 `copy` 视图，白吃内存与带宽。
