# 09 multiprocessing 模块

> 原书 pp. 245–310（英文 2e；中文版页码以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 为什么多进程 | 绕开 GIL | CPU 密集用进程 |
| Process / Pool | 基本并发 | Pool.map 简单并行 |
| 进程间通信 | Queue / Pipe / 共享内存 | 传数据有成本 |
| 序列化 | pickle 开销 | 大数据走共享内存 |
| 与线程对比 | I/O vs CPU | 按瓶颈选 |
| 取消与异常 | 进程管理 | 比线程更难取消 |

## 核心精讲

**1. 绕开 GIL。** CPython 的 GIL 让同一进程内多线程无法真正并行执行 Python 字节码。CPU 密集任务用 `multiprocessing` 起多个独立进程，各持有自己的 GIL，从而吃满多核。

**2. Pool 与 map。** `Pool(n).map(func, iterable)` 把可迭代切到 n 个 worker，近似「并行版 map」；`imap`/`imap_unordered` 支持流式与保序权衡。

```python
# 教学示意，不参与构建（需在 __main__ 保护下，Windows 必须）
import multiprocessing as mp

def square(x):
    return x * x

if __name__ == "__main__":
    with mp.Pool() as pool:        # 默认等于 CPU 核数
        print(pool.map(square, range(10)))
```

**3. 进程间通信（IPC）。** `Queue`/`Pipe` 经 pickle 序列化，有开销；大数组优先 `shared_memory`（3.8，`multiprocessing.shared_memory`）或 `multiprocessing.Array`/`Value` 共享内存，避免拷贝。

**4. 取消与异常。** 进程不像线程能随意打断；异常会在 `get()` 时原样抛出到主进程，需显式 `terminate`/`close`。

## 版本演进

- 3.8 起 `multiprocessing.shared_memory` 模块（共享内存段，省序列化）。
- 3.3 起 `concurrent.futures.ProcessPoolExecutor` 高层接口，配 `asyncio.run_in_executor` 很顺手。
- 3.11+ free-threading（PEP 703）：在 no-GIL 构建下，**多线程 CPU 并行首次成为可能**，使「CPU 密集必须多进程」不再是铁律——见 [concepts/GIL与free-threading.md](concepts/GIL与free-threading.md)。
- 子解释器（PEP 554，3.12 起 `interpreters` 模块，实验）提供「隔离状态 + 潜在并行」的第三种路径。

## 经典论文与原始文献

- `multiprocessing` 标准库文档；PEP 371（multiprocessing 进入标准库）。
- PEP 554（Multiple Interpreters in the Stdlib，3.12 实验）；PEP 703（no-GIL）。

## 近年研究与工业界开源实践（2015–2026）

- **joblib**（scikit-learn 默认后端）把 `Parallel(n_jobs=...)` 做成科研标配，自动内存映射大数组。
- **Ray / Dask** 把多进程抽象为「分布式任务图」，本地多核到集群无缝（接第 10 章）。
- 工业界：数值/ML 训练用多进程数据加载（`torch.utils.data.DataLoader(num_workers=...)`）。

## 常见误区与本书需修正之处

- 🔧 误：原书基调「多进程永远优于多线程做 CPU 并行」——在 3.13t/3.14t no-GIL 构建下，多线程也可并行 CPU，结论需按构建类型修正。
- 误：Windows 下忘了 `if __name__ == "__main__":` 保护，会因 spawn 反复 import 主模块而递归/崩溃。
- 误：默认 `fork` 启动（Linux）会复制父进程内存，隐藏状态/文件描述符泄漏；现代倾向 `spawn`/`forkserver`。
- 误：多进程「免费加速」——IPC 与 pickle 开销在大对象上可能抵消并行收益；用共享内存。

## 与其他章 / 其他书的联系

- GIL 真相 → [concepts/GIL与free-threading.md](concepts/GIL与free-threading.md)。
- 扩展到集群 → 第 10 章（集群与任务队列）。
- 对照 [`Python Concurrency with asyncio`](../PythonConcurrencyWithAsyncio.md)（🔧 待深度展开）的并发模型对照表。
