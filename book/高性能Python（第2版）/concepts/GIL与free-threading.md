# 概念专篇：GIL 与 free-threading

> 跨章概念：与第 7 章（编译到 C）、第 8 章（异步 I/O）、第 9 章（multiprocessing）强相关。
> 本文校准到 2026（Python 3.12–3.14）。

## 1. GIL 是什么

CPython 的 **Global Interpreter Lock** 是一把进程级互斥锁，保证任意时刻只有一个线程在执行 Python 字节码。它简化了 CPython 内部的内存管理与对象模型（引用计数、GC 不用额外加锁），代价是：同一进程内多线程无法真正并行执行 Python 代码。

## 2. GIL 阻塞什么、不阻塞什么

- **被阻塞**：CPU 密集型的多线程（纯 Python 计算）——多线程不会更快，甚至因锁竞争更慢。
- **不被阻塞**：
  - I/O 等待（socket/磁盘）：线程在 `await`/`recv` 时释放 GIL，异步/多线程并发有效（第 8 章）。
  - 调用释放 GIL 的 C 扩展：NumPy/OpenBLAS、Pillow、lxml、大部分 `numpy`/`pandas`/`torch` 的算子内部释放 GIL，多线程向量化有效（第 6 章）。
  - 多进程：每个进程独立 GIL（第 9 章）。

## 3. free-threading（PEP 703）

- **目标**：让 CPython 可选择「无 GIL」构建，使多线程能真正并行 CPU 计算。
- **落地节奏**：3.13（2024）提供实验性 `--disable-gil` 构建（常称 3.13t）；3.14（2025）延续并改进，但默认仍带 GIL，no-GIL 为实验通道。
- **含义变化**：在 3.13t/3.14t 下，原书「CPU 密集必须多进程」结论部分失效——多线程也可并行，但要小心数据竞争（需 `threading.Lock`/无锁结构）。
- **扩展作者注意**：编译型扩展（Cython/Numba/C 扩展）在 no-GIL 下需用「受限 C API」（PEP 683 永久对象、PEP 689 临时 API）或显式标注线程安全，否则行为未定义。

## 4. 决策表（2026）

| 场景 | 首选 | 原因 |
|---|---|---|
| I/O 密集 | asyncio / 多线程 | GIL 在等待时释放 |
| CPU 密集 + 向量化库 | 多线程（库内释放 GIL） | NumPy 等已并行 |
| CPU 密集 + 纯 Python | 多进程 / no-GIL 构建 / 编译 | 绕开或消除 GIL |
| 单机→多机 | 任务队列（Celery/Dask/Ray） | 第 10 章 |

## 5. 常见误区

- 误：「Python 不能并行」——能，只是默认 GIL 限制了同进程内多线程 CPU 并行；多进程、释放 GIL 的 C 扩展、异步 I/O 都能并行/并发。
- 误：「PyPy 无 GIL」——PyPy 同样有 GIL；其 JIT 加速单线程，不解决多核 CPU 并行。
- 误：「no-GIL 构建能自动让旧多线程代码变快」——还需无数据竞争设计，且扩展兼容性要验证。
