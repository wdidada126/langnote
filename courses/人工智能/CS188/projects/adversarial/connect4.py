# -*- coding: utf-8 -*-
"""L05 对抗搜索项目：Connect-4 的 Minimax / Alpha-Beta / Expectimax（纯标准库）

运行:  python connect4.py
对应 notes/L05-对抗搜索-minimax与alpha-beta.md

内容:
  1) 深度 3-6 的节点评估数对比表: alpha-beta 剪枝省多少 (最佳着法序近似 b^(d/2));
  2) alpha-beta 自博弈 vs 随机走子, 展示终盘;
  3) expectimax: 对手"均匀随机"(Pacman 随机鬼)时的期望搜索, 与 minimax 悲观假设对比.
棋盘: 6 行 x 7 列, 列栈表示 (落子=append, 悔棋=pop). P1=X=MAX, P2=O=MIN/机会节点.
"""
import random

ROWS, COLS = 6, 7
INF = 10 ** 9
P1, P2 = 1, -1


def new_board():
    return [[] for _ in range(COLS)]


def legal_moves(board):
    return [c for c in range(COLS) if len(board[c]) < ROWS]


def apply_move(board, col, player):
    board[col].append(player)
    return len(board[col]) - 1


def undo_move(board, col):
    board[col].pop()


def cell(board, r, c):
    return board[c][r] if 0 <= r < ROWS and 0 <= c < COLS and r < len(board[c]) else None


def winner(board):
    """返回 P1 / P2 / None (draw 需另判满盘)."""
    dirs = ((0, 1), (1, 0), (1, 1), (1, -1))
    for r in range(ROWS):
        for c in range(COLS):
            p = cell(board, r, c)
            if p is None:
                continue
            for dr, dc in dirs:
                if all(cell(board, r + dr * k, c + dc * k) == p for k in range(4)):
                    return p
    return None


def is_terminal(board):
    return winner(board) is not None or len(legal_moves(board)) == 0


def terminal_value(board, ply):
    w = winner(board)
    if w == P1:
        return INF - ply            # 越快赢越好
    if w == P2:
        return -INF + ply
    return 0                        # 平局


SCORE_WINDOW = [0, 1, 12, 160]      # 窗口内己方 0/1/2/3 子(无对方子)的分值


def evaluate(board):
    """启发式评估: 所有 4 连窗口 + 中心控制 (eval = L03 的 h 在博弈中的化身)."""
    score = 0
    dirs = ((0, 1), (1, 0), (1, 1), (1, -1))
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in dirs:
                cells = [cell(board, r + dr * k, c + dc * k) for k in range(4)]
                if any(x is None for x in cells) or r + dr * 3 < 0:
                    continue
                if r + dr * 3 >= ROWS or not (0 <= c + dc * 3 < COLS):
                    continue
                n1 = sum(1 for x in cells if x == P1)
                n2 = sum(1 for x in cells if x == P2)
                if n1 and n2:
                    continue
                if n1:
                    score += SCORE_WINDOW[n1]
                elif n2:
                    score -= SCORE_WINDOW[n2]
    score += 4 * sum(1 for r in range(ROWS) if cell(board, r, 3) == P1)
    score -= 4 * sum(1 for r in range(ROWS) if cell(board, r, 3) == P2)
    return score


def leaf_value(board, ply):
    if is_terminal(board):
        return terminal_value(board, ply)
    return evaluate(board)


def minimax(board, depth, player, ply, stats):
    stats["minimax"] += 1
    if depth == 0 or is_terminal(board):
        return leaf_value(board, ply)
    moves = legal_moves(board)
    if player == P1:
        v = -INF
        for m in moves:
            apply_move(board, m, P1)
            v = max(v, minimax(board, depth - 1, P2, ply + 1, stats))
            undo_move(board, m)
        return v
    v = INF
    for m in moves:
        apply_move(board, m, P2)
        v = min(v, minimax(board, depth - 1, P1, ply + 1, stats))
        undo_move(board, m)
    return v


def alpha_beta(board, depth, player, alpha, beta, ply, stats):
    stats["alpha_beta"] += 1
    if depth == 0 or is_terminal(board):
        return leaf_value(board, ply)
    moves = sorted(legal_moves(board), key=lambda c: -abs(3 - c))  # 中心优先: 近似最佳着法序
    if player == P1:
        v = -INF
        for m in moves:
            apply_move(board, m, P1)
            v = max(v, alpha_beta(board, depth - 1, P2, alpha, beta, ply + 1, stats))
            undo_move(board, m)
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v
    v = INF
    for m in moves:
        apply_move(board, m, P2)
        v = min(v, alpha_beta(board, depth - 1, P1, alpha, beta, ply + 1, stats))
        undo_move(board, m)
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v


def best_move_alpha_beta(board, depth):
    stats = {"alpha_beta": 0}
    alpha, best_v, best_m = -INF, -INF, None
    for m in sorted(legal_moves(board), key=lambda c: -abs(3 - c)):
        apply_move(board, m, P1)
        v = alpha_beta(board, depth - 1, P2, alpha, INF, 1, stats)
        undo_move(board, m)
        if v > best_v:
            best_v, best_m = v, m
        alpha = max(alpha, v)
    return best_m, best_v, stats["alpha_beta"]


def best_move_minimax(board, depth):
    stats = {"minimax": 0}
    best_v, best_m = -INF, None
    for m in legal_moves(board):
        apply_move(board, m, P1)
        v = minimax(board, depth - 1, P2, 1, stats)
        undo_move(board, m)
        if v > best_v:
            best_v, best_m = v, m
    return best_m, best_v, stats["minimax"]


def expectimax(board, depth, player, ply, stats):
    """P2 为随机对手 => 机会节点取期望(不可剪枝, 见笔记 L05)."""
    stats["expectimax"] += 1
    if depth == 0 or is_terminal(board):
        return leaf_value(board, ply)
    moves = legal_moves(board)
    if player == P1:
        vals = []
        for m in moves:
            apply_move(board, m, P1)
            vals.append(expectimax(board, depth - 1, P2, ply + 1, stats))
            undo_move(board, m)
        return max(vals)
    total = 0.0
    for m in moves:
        apply_move(board, m, P2)
        total += expectimax(board, depth - 1, P1, ply + 1, stats)
        undo_move(board, m)
    return total / len(moves)


def best_move_expectimax(board, depth):
    stats = {"expectimax": 0}
    best_v, best_m = -INF, None
    for m in legal_moves(board):
        apply_move(board, m, P1)
        v = expectimax(board, depth - 1, P2, 1, stats)
        undo_move(board, m)
        if v > best_v:
            best_v, best_m = v, m
    return best_m, best_v, stats["expectimax"]


def show(board):
    lines = []
    for r in range(ROWS - 1, -1, -1):
        row = ""
        for c in range(COLS):
            v = cell(board, r, c)
            row += {P1: "X", P2: "O", None: "."}[v] + " "
        lines.append(row)
    lines.append("1 2 3 4 5 6 7")
    return "\n".join(lines)


def demo_pruning_table():
    print("=" * 62)
    print("Part 1  minimax vs alpha-beta 评估节点数 (开局空盘, 对称性略)")
    print(f"{'depth':<8}{'minimax':<14}{'alpha-beta':<14}{'根值一致?':<10}")
    for d in (3, 4, 5, 6):
        board = new_board()
        _, v1, n1 = best_move_minimax(board, d)
        _, v2, n2 = best_move_alpha_beta(board, d)
        assert v1 == v2, "alpha-beta 必须保持 minimax 值不变"
        print(f"{d:<8}{n1:<14}{n2:<14}{'yes' if v1 == v2 else 'NO':<10}")


def demo_self_play(depth=4):
    print("\n" + "=" * 62)
    print(f"Part 2  alpha-beta(depth={depth}) P1=X  vs  随机 P2=O 自博弈")
    rng = random.Random(188)
    board = new_board()
    ply = 0
    while not is_terminal(board) and ply < 60:
        m, _, _ = best_move_alpha_beta(board, depth)
        apply_move(board, m, P1)
        if is_terminal(board):
            break
        m2 = rng.choice(legal_moves(board))
        apply_move(board, m2, P2)
        ply += 1
    print(show(board))
    w = winner(board)
    print("结果:", "P1(X) 胜" if w == P1 else ("P2(O) 胜" if w == P2 else "未分胜负/满盘"))


def demo_expectimax():
    print("\n" + "=" * 62)
    print("Part 3  expectimax(对手均匀随机) 选点示例")
    board = new_board()
    for i, m in enumerate([3, 4, 2, 1]):
        apply_move(board, m, P1 if i % 2 == 0 else P2)
    print(show(board))
    m1, v1, n1 = best_move_expectimax(board, 5)
    m2, v2, n2 = best_move_alpha_beta(board, 5)
    print(f"expectimax: 最佳列={m1 + 1} 值={v1:.1f} 节点={n1}")
    print(f"alpha-beta(悲观对手): 最佳列={m2 + 1} 值={v2} 节点={n2}")
    print("讨论: 对手随机时期望搜索更贴合实际; 对手强时 minimax 假设才安全.")


if __name__ == "__main__":
    demo_pruning_table()
    demo_self_play()
    demo_expectimax()
