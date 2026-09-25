"""gil_demo.py —— GIL 行为演示：CPU 密集 vs I/O 密集，线程 vs 进程（对应讲义 L25）。

结论预览（在多数 CPython 3.9+ 桌面机上）：
  CPU 密集：线程池 ≈ 串行（甚至更慢）；进程池 ≈ 近线性加速
  I/O 密集：线程池 ≈ 并行等待（明显加速）；进程池也行但开销大
GIL 锁的是"字节码解释循环"，不是你的计算库/IO 等待。
自检：python -m py_compile gil_demo.py
"""

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

N = 3_000_000


def cpu_task(n=N):
    return sum(i * i for i in range(n))


def io_task(seconds=0.4):
    time.sleep(seconds)          # sleep 期间 GIL 被释放 → 线程真并行等待
    return seconds


def timed(label, fn):
    t0 = time.perf_counter()
    result = fn()
    dt = time.perf_counter() - t0
    print(f'{label:34s} {dt:6.2f}s  {result if not isinstance(result, list) else ""}')
    return dt


def run_threads(fn, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(fn, args))


def run_processes(fn, args, workers):
    with ProcessPoolExecutor(workers) as ex:
        return list(ex.map(fn, args))


def main():
    print('== CPU 密集（纯 Python 平方和 x4） ==')
    t_seq = timed('串行 1x', lambda: cpu_task())
    t_thr = timed('线程池 4x', lambda: run_threads(cpu_task, [N] * 4, 4))
    t_pro = timed('进程池 4x', lambda: run_processes(cpu_task, [N] * 4, 4))
    print(f'  线程/串行 = {t_thr/t_seq:.2f}（总工作量是串行 4 倍：比值≈4 即毫无并行收益，GIL 所致）；'
          f'进程/串行 = {t_pro/t_seq:.2f}（明显 <4 即多核收益，还要扣启动/序列化开销）\n')

    print('== I/O 密集（sleep 0.4s x8） ==')
    t_io_seq = timed('串行 8x', lambda: [io_task() for _ in range(8)])
    t_io_thr = timed('线程池 8x', lambda: run_threads(
        io_task, [0.4] * 8, 8))
    print(f'  线程/串行 = {t_io_thr/t_io_seq:.2f}（等待可重叠 → 接近 1/8）\n')

    print('提示：3.13+ 的 free-threaded CPython（PEP 703, python3.13t）下'
          'CPU 线程池可获得真并行——GIL 正在成为历史选项。')


if __name__ == '__main__':
    main()
