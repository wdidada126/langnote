# 第 19 章 Python并发模型（原书 pp.537–569）

> 一句话定位本章：并发有三种口味——线程（受 GIL 限 CPU）、进程（绕过 GIL）、协程（单线程事件循环）；本章用同一个「旋转指针」示例把三者讲清，并诚实面对 GIL。
> 基线：原书 Python 3.10；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| 19.1 本章新增内容（p.538） | 第 2 版改动 | 🔴 必须补 free-threading（PEP 703） |
| 19.2 全景概览（p.538） | 并发三件套 | 线程/进程/协程各有适用面 |
| 19.3 术语定义（p.539） | 并发 vs 并行、任务/作业 | 概念先行，避免混淆 |
| 19.4 演示并发的 Hello World（p.541） | 三版旋转指针 | 同一功能用线程/进程/协程各写一遍 |
| 19.4.1 线程 spinner（p.541） | `threading.Thread` | I/O 并发常用线程 |
| 19.4.2 进程 spinner（p.544） | `multiprocessing.Process` | CPU 密集可绕过 GIL |
| 19.4.3 协程 spinner（p.545） | `asyncio` | 单线程高并发 I/O |
| 19.4.4 对比 supervisor（p.548） | 三种编排对比 | 协程代码最像顺序、并发度最高 |
| 19.5 GIL 真正的影响（p.549） | GIL 限什么不限什么 | 🔴 I/O 不受 GIL 限；CPU 受 |
| 19.6 自建进程池（p.552） | 手动多进程算素数 | 展示多核收益 |
| 19.7 多核世界中的 Python（p.559） | 各领域的并发策略 | Web/数据科学/系统管理各有选法 |
| 19.8 本章小结（p.565） | 并发选型地图 | 「I/O 用协程/线程，CPU 用进程或 free-threaded」 |
| 19.9 延伸阅读（p.566） | GIL 论文、各并发库 | 官方与社区资源 |

## 核心精讲

### 19.4 三版 spinner（节选）

```python
# 教学示意，不参与构建 —— 线程版
import threading, itertools, time

def spinner():
    for ch in itertools.cycle("|/-\\"):
        print(ch, end="\r", flush=True)
        time.sleep(0.1)

t = threading.Thread(target=spinner, daemon=True)
t.start()
time.sleep(1)            # 主线程干别的活，spinner 同时转
```

```python
# 教学示意，不参与构建 —— asyncio 版（3.12+）
import asyncio, itertools

async def spinner():
    for ch in itertools.cycle("|/-\\"):
        print(ch, end="\r", flush=True)
        await asyncio.sleep(0.1)

async def main():
    asyncio.create_task(spinner())
    await asyncio.sleep(1)

asyncio.run(main())
```

## 版本演进

- 🔴 **PEP 703 — Making the GIL Optional（3.13 实验性 free-threaded 构建，3.14 官方支持）**：这是本章**必须修正的头号结论**。原书按「GIL 不可移除」写，今天：3.13 提供 `python3.13t`（或 `PYTHON_GIL=0` 开关，🔧 具体开关名以官方文档为准）可跑无 GIL 构建；3.14 起 free-threaded 成为官方支持的一等构建。CPU 密集型代码在 free-threaded 下可真正并行。
- **PEP 684 — A Per-Interpreter GIL（3.12）**：每个子解释器有独立 GIL，是「绕过 GIL」的另一条路径，配合 `multiprocessing` 的子解释器 API。
- **PEP 734 — Multiple Interpreters in the Stdlib（3.14）**：把子解释器 API 正式化，提供 `interpreters` 模块，是 free-threaded 之外的并发新选择。
- **PEP 574 — Pickle protocol 5（🔧 以官方为准）**：进程间大数据传输（`multiprocessing`）更高效，间接提升 19.6 进程池。
- 3.11 Faster CPython 让单线程更快，部分「用多进程只为加速」的场景可回到单线程（非同行评审，speed.python.org）。
- 3.13 实验性 JIT（`PYTHON_JIT=1`，🔧 以官方为准）对 CPU 密集代码有额外收益。

## 经典论文与原始文献

- PEP 703 — Making the Global Interpreter Lock Optional in CPython（3.13 实验）。https://peps.python.org/pep-0703/ 。规范文档，🔴 free-threaded 来源。
- PEP 684 — A Per-Interpreter GIL（3.12）。https://peps.python.org/pep-0684/ 。规范文档，子解释器 GIL。
- PEP 734 — Multiple Interpreters in the Standard Library（3.14）。https://peps.python.org/pep-0734/ 。规范文档，多解释器 API。
- PEP 3156 — Async IO Support Rebooted（3.4）。https://peps.python.org/pep-3156/ 。规范文档，`asyncio` 基础。
- PEP 3148 — `concurrent.futures`（3.2）。https://peps.python.org/pep-3148/ 。规范文档，执行器抽象。
- Python 文档「Concurrency」章节（threading / multiprocessing / asyncio 对比）。https://docs.python.org/3/library/asyncio-dev.html 。官方文档。

## 近年研究与工业界开源实践（2015–2026）

- **free-threaded C 扩展生态**：NumPy、`pyarrow`、`regex` 等陆续发布 `--disable-gil` 兼容构建，free-threaded 才真正可用（非同行评审，项目公告）。
- **`uvloop` / `asyncio` 在高并发网关**：单线程事件循环在 I/O 密集型服务（代理、网关）上性能极佳（非同行评审，工业实践）。
- **`ray` / `dask` 在分布式 CPU 计算**：多进程/分布式调度绕开 GIL，是数据科学默认（非同行评审）。
- **`py-spy` / `scalene` 做并发性能剖析**：定位「是被 GIL 卡住还是被 I/O 卡住」的现代工具（非同行评审）。

## 常见误区与本书需修正之处

| 原书说法 / 习惯 | 问题 | 2026 正确写法 |
| --- | --- | --- |
| 「GIL 永远不能移除」 | 3.13 free-threaded 实验、3.14 官方支持 | 🔴 更新为「GIL 可禁用，3.14 起官方支持 free-threaded 构建」 |
| 线程能加速 CPU 密集任务 | CPython 线程受 GIL，CPU 密集仍串行 | CPU 密集用 `ProcessPoolExecutor` 或 free-threaded 构建 |
| 进程一定比线程好 | 进程有序列化/pickling 开销，I/O 场景反而重 | I/O 密集优先协程/线程；CPU 密集才进程 |
| 协程「更快」 | 协程单线程，CPU 密集一样被 GIL 限 | 协程适合 I/O 并发；CPU 密集仍需进程/禁用 GIL |
| 🔴「多核 Python 无解」 | PEP 703/684/734 提供三条出路 | 多核可用：free-threaded、子解释器、多进程 |
| 🔧 具体禁用 GIL 的开关名 | `python3.13t` / `PYTHON_GIL=0` / 构建标志可能随版本调整 | 以官方 What's New / 安装文档为准 |

## 与其他章 / 其他书的联系

- [20-并发执行器.md](20-并发执行器.md)：`concurrent.futures` 把线程/进程池统一封装，是本章概念的执行层。
- [21-异步编程.md](21-异步编程.md)：协程 spinner 的深入；`asyncio` + free-threaded 的关系。
- [17-迭代器、生成器和经典协程.md](17-迭代器、生成器和经典协程.md)：协程的来路。
- 跨书：对应 [C++并发编程实战2/](../C++并发编程实战2/) 的多线程/锁模型（无 GIL，靠 `std::mutex`），以及 [Python基础教程_第3版_9787115474889/16-测试基础.md](../Python基础教程_第3版_9787115474889/16-测试基础.md) 的并发测试。
