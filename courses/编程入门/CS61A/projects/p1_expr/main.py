"""main.py —— P1 演示入口（L01-L02 + L20 前哨）。运行：python main.py

自检命令：python -m py_compile rat.py expr.py main.py
"""

from expr import calc, ParseError, EvalError
from rat import Rat

EXPRS = [
    '1 + 2 * 3',
    '2 ** 2 ** 3',
    '(1 + 2) * 3 - 9',
    '-7 // 2',
    '-7 % 2',
    '7 / 2',
    '1/3 + 1/6',
    '2 ** 64',
    '2 ** 100 % 1000',
    '1 < 2 < 3',
    '0 or 42',
    '1 and 2',
    'not (1 == 2)',
    '0.1 + 0.2 - 1/10 - 1/5',   # float 噪声演示
]

BROKEN = ['1 +', '(1 + 2', '1/0', 'hello']


def main():
    print('== P1 表达式求值演示 ==')
    for src in EXPRS:
        try:
            v = calc(src)
            note = ''
            if isinstance(v, Rat):
                note = f'  (float≈{float(v):g})'
            print(f'{src:28s} = {v!r}{note}')
        except (ParseError, EvalError, TypeError) as e:
            print(f'{src:28s} ! {e}')

    print('\n== 非法输入（异常被捕获，不崩溃） ==')
    for src in BROKEN:
        try:
            calc(src)
            print(f'{src:28s} = 不应到达')
        except (ParseError, EvalError) as e:
            print(f'{src:28s} ! {type(e).__name__}: {e}')


if __name__ == '__main__':
    main()
