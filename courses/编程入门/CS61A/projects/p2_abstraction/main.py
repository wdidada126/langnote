"""main.py —— P2 演示入口。运行：python main.py

打印一局贪心自对局的开局若干步与终局；再演示关键纯函数。
自检：python -m py_compile game2048.py main.py
"""

import random

from game2048 import (empty_board, spawn, move_left, move_right, move_up,
                      move_down, legal_moves, render, play, merge_line)


def demo_moves():
    print('== 单次方向合并演示 ==')
    b = spawn(spawn(empty_board(), random.Random(1)), random.Random(2))
    for name, fn in (('left', move_left), ('right', move_right),
                     ('up', move_up), ('down', move_down)):
        nb, sc = fn(b)
        print(f'--- {name} (+{sc}) ---\n{render(nb)}\n')


def demo_line():
    print('== merge_line 一维规则（游戏的心脏） ==')
    for line in [(2, 2, 2, 2), (2, 2, 4, 0), (0, 4, 0, 4), (2, 4, 2, 4)]:
        print(f'  {line} -> {merge_line(line)}')


def demo_game(seed):
    print(f'== 贪心自对局 seed={seed} ==')
    b, score, turns = play(seed=seed)
    print(render(b))
    print(f'回合数={turns}  总得分={score}  最大块={max(b)}  '
          f'可动方向={"".join(sorted(legal_moves(b))) or "无（终局）"}')


def main():
    demo_line()
    demo_moves()
    for seed in (7, 2024, 61):
        demo_game(seed)
        print()


if __name__ == '__main__':
    main()
