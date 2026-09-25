"""main.py —— p6 并发演示入口：先竞态后 GIL。运行：python main.py

自检：python -m py_compile race.py gil_demo.py main.py
"""

import gil_demo
import race


def main():
    print('================ 1. 竞态与锁（race.py） ================')
    race._selftest()
    got, want = race.demo_race(reps=100_000)
    print(f'一次无锁演示: {got}/{want} —— '
          + ('出现 RACE（丢失更新）' if got < want else '本次侥幸未交错'))
    print()
    print('================ 2. GIL 行为（gil_demo.py） ================')
    gil_demo.main()


if __name__ == '__main__':
    main()
