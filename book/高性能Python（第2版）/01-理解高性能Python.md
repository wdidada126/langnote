# 01 理解高性能 Python

> 原书 pp. 1–20（英文 2e；中文版页码以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 基础计算机系统 | 计算单元 / 内存 / 通信层 | 性能 = 在「理想计算」与「真实硬件」之间取舍 |
| Python 虚拟机 | 字节码 / 对象模型 / GIL | CPython 用统一对象抽象换来了易用性，也带来开销 |
| 为何还用 Python | 开发效率 vs 运行效率 | 用 Python 写原型，用编译/扩展扛热点 |
| 高效能程序员素养 | 基准 / 剖析 / 单元测试 | 优化前先有可复现的测量与回归保护 |

## 核心精讲

本章不堆代码，而是建立「性能心智模型」。

**1. 理想计算 vs Python 虚拟机。** 理想计算机是连续地址空间 + 无限快的 ALU；真实硬件有缓存层级（L1/L2/L3）、分支预测、预取。CPython 额外在中间插了一层：一切皆 `PyObject*`，每次属性访问都要走 `tp_getattro`、哈希查找、引用计数。这层抽象让 Python 慢，但也让它安全、动态、易嵌入。

```python
# 教学示意，不参与构建
import sys
class Point:
    pass
p = Point()
# 每个对象都带 ob_refcnt / ob_type / ob_size 等头部开销
print(sys.getsizeof(p))   # 即便空对象也有几十字节
```

**2. 计算单元与内存单元解耦。** 现代 CPU 比内存快一个数量级，瓶颈常不在 ALU 而在「内存墙」（带宽 + 延迟）。这就是为什么第 6 章（NumPy 向量化）和第 11 章（省内存）如此关键——减少内存往返比减少指令数更划算。

**3. So Why Use Python？** 作者的答案：快速迭代 + 巨大生态。把 5% 的热点用 Cython/Numba/多进程加速，剩下的 95% 享受开发效率。

**4. 工程纪律。** 优化三件套：可复现基准、剖析定位、优化全程跑单元测试保正确。没有基准的「优化」是迷信。

## 版本演进

- 原书以 Python 3.7 为例；3.10+ 的错误链（`raise ... from`）、3.11 更快的解释器（「Faster CPython」专项，PEP 659 自适应解释器）让同一段纯 Python 在 3.11–3.14 上明显变快，无需改代码。
- 「Faster CPython」计划（2021 起，由 Mark Shannon 等推动，Python 3.11/3.12/3.13 连续提速，累计纯 Python 约 1.6×）属于原书出版后的重大红利，详见 [concepts/性能剖析工具链.md](concepts/性能剖析工具链.md)。
- 3.13 引入实验性 free-threading 构建（PEP 703），见 [concepts/GIL与free-threading.md](concepts/GIL与free-threading.md)。

## 经典论文与原始文献

- O'Reilly 原书第 1 章「The Fundamental Computer System」。
- 「Faster CPython」计划主页与 PEP 659（Adaptive Interpreter，3.11）。
- PEP 703（Making the Global Interpreter Lock Optional，3.13 起实验）。

## 近年研究与工业界开源实践（2015–2026）

- CPython 3.11–3.14 连续多个版本纯 Python 提速（专项计划），是「不重写也能变快」的最佳证据。
- PyPy 的 JIT 仍是最成熟的「零改动加速」方案之一（2026 已支持至 3.10 语法）。
- 工业界普遍采用「Python 编排 + 编译内核」架构：PyTorch/TensorFlow/JAX 底层是 C++/CUDA，Python 只做胶水。

## 常见误区与本书需修正之处

- 🔧 误：原书暗示「Python 3 比 2 慢」的语境已过时；3.11 起纯 Python 已显著快于 3.7，应在「版本演进」中补充。
- 误：把「GIL 让 Python 不能并行」当成绝对结论——I/O 并发（asyncio、多线程等待 socket）不受 GIL 阻塞；且 3.13t/3.14t 提供 no-GIL 实验构建。
- 误：以为「优化 = 换更快的算法」就够了；在数值场景，内存布局（连续 vs 碎片）常常比算法阶数更决定实测快慢。

## 与其他章 / 其他书的联系

- 「为何用 Python」的代价分析 → 第 7 章（编译到 C）给出具体解法。
- 对象模型开销 → 接 [`CPython Internals`](../CPythonInternals.md)（🔧 待深度展开）的字节码与对象头讲解。
- 缓存与内存墙 → 第 6 章（NumPy）、第 11 章（省内存）。
