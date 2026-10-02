# 13 GIL 与线程

> 原书 pp. 第 13 章（具体页码以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| GIL 是什么 | 进程级锁 | 单进程内字节码串行 |
| 为何有 GIL | 引用计数安全 | 历史取舍 |
| 线程并发 | I/O 等待释放 | 多线程 I/O 有效 |
| no-GIL 构建 | PEP 703 | 3.13t/3.14t 实验 |
| free-threading 影响 | 扩展需受限 API | 兼容性注意 |

## 核心精讲

**1. GIL 本质**。`_PyRuntimeState` 持有 GIL；同一进程内任意时刻只有一个线程执行 Python 字节码。它让引用计数等无需额外加锁，但限制同进程多线程 CPU 并行。

**2. 何时释放**。`time.sleep`、`socket.recv`、调用释放 GIL 的 C 扩展（NumPy/OpenBLAS、Pillow 等）时释放 GIL → I/O 密集多线程有效，纯 Python CPU 密集无效（需多进程或 no-GIL）。

**3. no-GIL 构建（PEP 703）**。3.13 起提供 `--disable-gil` 实验构建（3.13t），3.14 延续改进，默认仍带 GIL。线程可真正并行 Python 代码，但需无数据竞争设计，且 C 扩展要用受限 API 或标记线程安全。

**4. 子解释器（PEP 554，3.12）**。`interpreters` 模块创建隔离解释器，各自状态独立、潜在并行，是「单机多隔离执行」的第三路径（见第 14 章）。

## 版本演进

- 3.13 实验性 no-GIL（PEP 703）；`PYTHON_GIL=0` 可关。
- 3.12 子解释器成熟（PEP 554）、`sys.monitoring`（PEP 669）。
- 3.12 immortal 对象（PEP 683）是 no-GIL 的前置依赖。

## 经典论文与原始文献

- GIL 实现（`Python/ceval_gil.h`、`_PyRuntimeState`）。
- PEP 703（Making GIL Optional，3.13 实验）、PEP 554（Subinterpreters，3.12）、PEP 683（Immortal，3.12）。

## 近年研究与工业界开源实践（2015–2026）

- 3.13/3.14 的 free-threading 是近年最大底层变革；PyPy/GraalPy 也在探索无 GIL。
- 工业界多数仍用多进程（multiprocessing/Ray/Dask）绕 GIL，no-GIL 用于特定 CPU 密集。

## 常见误区与本书需修正之处

- 🔧 误：原书（3.10 基线）未含 PEP 703 no-GIL——这是 2026 必补的核心变更。
- 误：以为「Python 不能并行」——多进程/释放 GIL 的扩展/异步 I/O 均可并行。
- 误：以为「no-GIL 让旧多线程代码自动变快」——还需无竞争设计 + 扩展兼容。

## 与其他章 / 其他书的联系

- GIL 与并发模型总论 → [concepts/GIL与no-GIL构建.md](concepts/GIL与no-GIL构建.md)。
- 多进程/异步实践 → [`高性能Python（第2版）/00-总览与阅读地图.md`](../高性能Python（第2版）/00-总览与阅读地图.md) 第 8/9 章。
- 子解释器 → 第 14 章（异步与并发）。
