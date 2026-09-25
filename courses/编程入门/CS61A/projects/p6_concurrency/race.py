"""race.py —— 并发三件套演示：竞态 / 锁 / 消息传递（对应讲义 L25）。

只用标准库。直接运行：python race.py
自检：python -m py_compile race.py gil_demo.py
"""

import threading
import time
from queue import Queue


def demo_race(reps=200_000, n_threads=4, widen=True):
    """无锁累加：读-改-写三步被打断 → 结果 < 期望（GIL 也救不了你！）。

    widen=True 时在"读"与"写"之间插 time.sleep(0) 显式让出——新版 CPython 的
    自然交错窗口很窄，人为放大才能每次复现丢失更新（教学用，竞态本质不变）。
    """
    shared = {'total': 0}

    def worker():
        for _ in range(reps):
            v = shared['total']          # 读
            if widen:
                time.sleep(0)            # 放大交错窗口
            shared['total'] = v + 1      # 改-写（可能覆盖别人的 +1）

    ts = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return shared['total'], n_threads * reps


def demo_lock(reps=200_000, n_threads=4):
    """加锁临界区：正确但更慢（锁的代价）。"""
    shared = {'total': 0}
    lock = threading.Lock()

    def worker():
        local = 0
        for _ in range(reps):
            local += 1
        with lock:                       # 缩小临界区：一次入账而非每步加锁
            shared['total'] += local

    ts = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return shared['total']


def demo_message_passing(n_threads=4, reps=50_000):
    """不共享内存，只发消息（CP §2.4 消息传递对象 → Actor 模型的最小件）。"""
    inbox = Queue()

    def worker(tag):
        for i in range(reps):
            inbox.put((tag, i))

    ts = [threading.Thread(target=worker, args=(k,)) for k in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    count = 0
    while not inbox.empty():
        inbox.get()
        count += 1
    return count


def _selftest():
    got, want = demo_race(reps=50_000)
    # 竞态是概率现象：可能恰好等于期望值，但一旦小于即证明问题
    assert got <= want
    assert demo_lock(reps=50_000) == 4 * 50_000
    assert demo_message_passing(reps=10_000) == 4 * 10_000
    print('race selftest OK (lock/message 结果恒定正确)')


if __name__ == '__main__':
    for trial in range(3):
        got, want = demo_race()
        flag = 'RACE!' if got < want else 'lucky(no interleave)'
        print(f'第 {trial+1} 次无锁 4 线程 x200000: {got}/{want}  <- {flag}')
    print('加锁版:', demo_lock(), '(恒正确)')
    _selftest()
