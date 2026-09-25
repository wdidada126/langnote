# p6 并发与多处理：竞态 / 锁 / 消息传递 / GIL 实测

> 对应讲次：L25（并发与多处理）。官方课程以讨论课+讲义呈现（spring 特色周）；
> 本项目给出三个**可跑**的最小实证。

## 文件

| 文件 | 内容 |
| --- | --- |
| `race.py` | 无锁累加复现竞态（读-改-写被切）；`Lock` 修复并演示"缩小临界区"（局部计数一次入账）；`Queue` 消息传递替代共享内存（CP §2.4 → Actor）。 |
| `gil_demo.py` | CPU 密集：串行 vs 线程池 vs 进程池计时对比；I/O 密集：sleep 等待重叠演示；结论打印 + 3.13t 展望。 |
| `main.py` | 依次跑两者。 |

## 运行

```bash
python main.py
python gil_demo.py      # 只跑 GIL 基准（CPU 数影响结论，建议 4 核+）
```

`run.bat` / `run.sh`；自检：`python -m py_compile race.py gil_demo.py main.py`

## 知识点对照

- L25 §1.2：`+=` 非原子——GIL 存在依然有 race（3.10+ 小整数循环仍可能被切）；
- L25 §1.3：CPU 密集线程无收益/进程有收益；I/O 密集线程有效——一句话选型表；
- L25 §1.4：消息传递（Queue）与 OOP 消息传递（L13/L14）的概念血缘；
- L12/L23 预告：I/O 重叠的极致是协程事件循环（asyncio），本 demo 是它的进程/线程前身。
