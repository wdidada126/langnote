# 第 12 章 加速 Python（原书 pp. 255–258，英文 2e；中文版页次以实体书为准 🔧）

> 一句话定位：原书这一章（仅 4 页）在 2026 年已严重过时——这里整体按今天的工具链重写：剖析、向量化、编译、并行与无 GIL。

## 一、本章地图

| 小节 | 主题 | 页码 |
|---|---|---|
| 12.1 | 先剖析，再优化 | 255 |
| 12.2 | 向量化：NumPy | 256 |
| 12.3 | 编译：Cython / Numba / mypyc | 257 |
| 12.4 | 替代解释器与并行：PyPy / free-threading | 258 |

## 二、核心精讲

### 12.1 剖析优先
永远先 `cProfile` 找热点，再动手；盲优化常无效。

```python
# 教学示意，不参与构建
# python -m cProfile -s cumtime script.py
import cProfile, pstats

def hot(n: int) -> int:
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with cProfile.Profile() as pr:
        hot(1_000_000)
    pstats.Stats(pr).sort_stats("cumtime").print_stats(10)
```

### 12.2 NumPy 向量化（替代纯 Python 循环）
数值密集算法（DP 内层、距离矩阵）用 `numpy` 二维数组 + 广播，常数可降一到两个数量级。

### 12.3 编译加速
- `Cython`：3.0+ 默认语言级别提升，类型标注后编译接近 C。
- `Numba`：`@njit` JIT 编译数值循环，改动最小。
- `mypyc`：把带类型的 Python 编译为 C 扩展（mypy 附带）。

### 12.4 并行与无 GIL
- PyPy：带 JIT，纯 Python 长循环显著加速（但 C 扩展生态弱）。
- 🔴 **free-threading（PEP 703）**：Python 3.13 起实验性「无 GIL」解释器（`python3.13t`），3.14 继续完善；CPU 密集多线程不再被 GIL 串行化，是本书 2014 年完全无法设想的。

## 三、版本演进

| 年份 | 变化 | 对本章影响 |
|---|---|---|
| 2014（原书） | 讲 C 扩展、Cython、PyPy、基础剖析 | 基线 |
| 2020 | NumPy 稳定、`numba` 流行 | 向量化/JIT 成为首选 |
| 🔴 2024–2025 | NumPy 2.0（API 变更）；3.13 free-threading 实验；3.14 增强 | 原书「GIL 是铁律」结论被打破 |
| 2025 | CPython 持续专项提速（3.11–3.14 累计显著） | 「Python 慢」需重新措辞 |

## 四、经典论文与原始文献

- PEP 703: *Making the Global Interpreter Lock Optional in CPython*（free-threading，2023 接受，3.13+ 实验）。
- PEP 684: *Per-Interpreter GIL*（3.12，子解释器各自 GIL）。
- Van Rossum 等. *Cython* / *Numba* 官方文档（工具，非论文）。

## 五、近年研究与工业界前沿（2020–2026）

- 工业界共识（非同行评审）：「先 NumPy/向量化，再 Numba/Cython，最后才上 Rust/C 扩展」。
- free-threading 已由实验走向可用，但扩展生态（NumPy 等）需逐步适配无 GIL 构建。
- 异构计算：`cupy`（CUDA）、`jax`（XLA）把数值算法搬到 GPU；远超原书想象的加速比。

## 六、常见误区与本书需修正之处

- 🔴 原书称「Python 的 GIL 让多线程无法并行」——在 3.13+ 的 free-threading 构建下已不成立；但默认解释器仍带 GIL，需显式用 `python3.13t`。
- 🔧 原书推荐的某些 C 扩展写法在 Python 3.12+ 的受限 API / 稳定 ABI 下需调整；优先 Cython/mypyc 减少手工 C。
- NumPy 2.0（2024）有破坏性 API 变更，原书时代代码可能需 `np.float_` → `float` 等改名。

## 七、跨语言对照

- 与 C++/Rust 相比，Python 用「胶水 + 编译内核」策略达到近似性能；与 Go/Java 相比，无 GIL 前的多线程并行是 Python 的传统短板，正被 free-threading 补上。详见 [`高性能Python（第2版）`](../高性能Python（第2版）.md) 与 [`CPython设计与实现`](../CPython设计与实现.md)。
