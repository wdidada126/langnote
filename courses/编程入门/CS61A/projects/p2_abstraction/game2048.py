"""game2048.py —— P2 函数式 2048 逻辑层（对应讲义 L03-L08）。

只用标准库、全部纯函数（不可变棋盘 = 16 元组 int，行主序）。
官方课程 P2 Penguins 的主题是"数据抽象+地图"；本迷你版用 2048 的
滑动/合并逻辑演练同一批知识点：递归、高阶函数、序列变换、增长直觉。

核心设计（每条注释标注知识点讲次）：
- merge_line：一次向左合并，纯函数（L05 高阶思维：把"规则"写成可组合的小函数）
- transpose / reverse_rows：用"表示变换"把 4 个方向归约到 1 个（L10 数据抽象）
- next_move / play：随机性只通过传入的 rng 注入，逻辑层保持纯（L07 递归+测试性）

自检：python -m py_compile game2048.py
"""

import random

Board = tuple   # (16,) 0 表示空格

# ---------- 棋盘工具 ----------

def empty_board():
    return tuple([0] * 16)


def get(b, r, c):
    return b[r * 4 + c]


def set_cell(b, r, c, v):
    """不可变"更新"：返回新棋盘（对比 L13 可变版本的副作用写法）。"""
    lst = list(b)
    lst[r * 4 + c] = v
    return tuple(lst)


def rows(b):
    return [b[i * 4:i * 4 + 4] for i in range(4)]


def cols(b):
    return [tuple(b[r * 4 + c] for r in range(4)) for c in range(4)]


def from_rows(rs):
    return tuple(x for row in rs for x in row)


# ---------- 一维合并（游戏的心脏） ----------

def slide(row):
    """去掉 0（保序）。L11 序列过滤。"""
    return tuple(v for v in row if v)


def merge_adjacent(row):
    """对已无 0 的行从左两两合并（每个元素至多用一次），返回 (新行, 得分)。"""
    out, score, i = [], 0, 0
    while i < len(row):
        if i + 1 < len(row) and row[i] == row[i + 1]:
            out.append(row[i] * 2)
            score += row[i] * 2
            i += 2
        else:
            out.append(row[i])
            i += 1
    return tuple(out), score


def merge_line(line):
    """一行/一列向左滑并合并：slide → merge_adjacent → 补零。"""
    merged, score = merge_adjacent(slide(line))
    merged = merged + (0,) * (4 - len(merged))
    return merged, score


# ---------- 方向归约：只写一个方向 ----------

def transpose(b):
    return from_rows(cols(b))


def reverse_rows(b):
    return from_rows([tuple(reversed(r)) for r in rows(b)])


def move_left(b):
    results = [merge_line(r) for r in rows(b)]
    return from_rows([merged for merged, _ in results]), \
        sum(sc for _, sc in results)


def move_right(b):
    rev = reverse_rows(b)
    moved, score = move_left(rev)
    return reverse_rows(moved), score


def move_up(b):
    tp = transpose(b)
    moved, score = move_left(tp)
    return transpose(moved), score


def move_down(b):
    tp = transpose(b)
    moved, score = move_right(tp)
    return transpose(moved), score


MOVES = {'L': move_left, 'R': move_right, 'U': move_up, 'D': move_down}


# ---------- 随机注入口（纯逻辑层唯一"外部世界"） ----------

def spawn(b, rng):
    """在随机空格放 2（90%）或 4（10%）。rng 由调用方传入以便复现（L04 契约）。"""
    zeros = [i for i, v in enumerate(b) if v == 0]
    if not zeros:
        return b
    pos = rng.choice(zeros)
    val = 2 if rng.random() < 0.9 else 4
    lst = list(b)
    lst[pos] = val
    return tuple(lst)


def legal_moves(b):
    """返回所有会使棋盘变化的方向。"""
    return [k for k, fn in MOVES.items() if fn(b)[0] != b]


def is_over(b):
    return not legal_moves(b)


def play(seed=42, max_turns=1000):
    """无头自对局：贪心选"合并得分最高"的方向。返回 (棋盘, 得分, 回合数)。"""
    rng = random.Random(seed)
    b = spawn(spawn(empty_board(), rng), rng)
    total = 0
    for turn in range(max_turns):
        moves = legal_moves(b)
        if not moves:
            return b, total, turn
        # 一步贪心：对每个方向看直接得分
        def gain(k):
            return MOVES[k](b)[1]
        k = max(moves, key=gain)
        b, score = MOVES[k](b)
        total += score
        b = spawn(b, rng)
    return b, total, max_turns


def render(b):
    return '\n'.join('  '.join(f'{v:>4}' if v else '   .' for v in row)
                     for row in rows(b))


# ---------- 自检 ----------

def _selftest():
    assert slide((0, 2, 0, 4)) == (2, 4)
    assert merge_line((2, 2, 2, 2)) == ((4, 4, 0, 0), 8)
    assert merge_line((2, 2, 4, 0)) == ((4, 4, 0, 0), 4)
    assert merge_line((4, 2, 2, 0)) == ((4, 4, 0, 0), 4)   # 4 不与新 4 再合并
    assert merge_line((0, 0, 0, 2)) == ((2, 0, 0, 0), 0)

    b = set_cell(set_cell(empty_board(), 0, 0, 2), 0, 1, 2)
    nb, sc = move_left(b)
    assert get(nb, 0, 0) == 4 and sc == 4 and get(nb, 0, 1) == 0

    b = set_cell(set_cell(empty_board(), 3, 3, 8), 1, 0, 8)
    nb, sc = move_down(b)      # 第 3 列 8 落到底？(3,3) 不动，(1,0) 在第 0 列下移
    assert sc == 0
    assert get(nb, 3, 0) == 8 and get(nb, 3, 3) == 8

    # 贪心自对局可完赛
    _, score, turns = play(seed=7)
    assert turns >= 5 and score > 0
    print(f'2048 selftest OK (demo game: {turns} turns, score {score})')


if __name__ == '__main__':
    _selftest()
