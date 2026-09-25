"""minisql.py —— P3 迷你 SQL：表 + 选择/投影/排序 + 两种连接（对应 L16/L18/L24）。

- 表 = 行列表（dict），列名有序；
- select/project/order_by：SQL 的关系代数内核（L24）；
- nested_loop_join：朴素 Θ(|A|·|B|)；
- hash_join：用 dict 建索引，Θ(|A|+|B|) 均摊（L16"组织策略决定效率"的实证）。
自检：python -m py_compile minisql.py
"""


class Table:
    def __init__(self, name, columns, rows):
        self.name = name
        self.columns = list(columns)
        for r in rows:
            if set(r) != set(self.columns):
                raise ValueError(f'行 {r} 与列 {self.columns} 不符')
        self.rows = [dict(r) for r in rows]

    def __len__(self):
        return len(self.rows)

    def __repr__(self):
        head = ' | '.join(self.columns)
        body = '\n'.join(' | '.join(str(r[c]) for c in self.columns)
                         for r in self.rows)
        return f'{self.name}:\n{head}\n' + '-' * len(head) + f'\n{body}'


def select(table, pred):
    """σ（WHERE）：逐行过滤。"""
    return Table(table.name + '_σ', table.columns,
                 [r for r in table.rows if pred(r)])


def project(table, cols):
    """π（SELECT 列）：丢列即去重前的裸投影（此处保留重复，与 SQL ALL 一致）。"""
    return Table(table.name + '_π', cols,
                 [{c: r[c] for c in cols} for r in table.rows])


def order_by(table, key):
    """ORDER BY：sorted 稳定排序（L18 Timsort）。"""
    out = Table(table.name + '_τ', table.columns, table.rows)
    out.rows = sorted(out.rows, key=key)
    return out


# ---------- 连接两种 ----------

def nested_loop_join(a, b, on):
    """θ-连接：双重循环。Θ(|A|·|B|)。"""
    cols = [f'{a.name}.{c}' for c in a.columns] + \
           [f'{b.name}.{c}' for c in b.columns]
    rows = []
    for ra in a.rows:
        for rb in b.rows:
            if on(ra, rb):
                row = {f'{a.name}.{k}': v for k, v in ra.items()}
                row.update({f'{b.name}.{k}': v for k, v in rb.items()})
                rows.append(row)
    return Table(f'{a.name}⋈{b.name}', cols, rows)


def hash_join(a, b, key_a, key_b):
    """等值连接：小表建哈希索引 → 大表探测。均摊 Θ(|A|+|B|+输出)。"""
    index = {}
    for rb in b.rows:
        index.setdefault(rb[key_b], []).append(rb)
    cols = [f'{a.name}.{c}' for c in a.columns] + \
           [f'{b.name}.{c}' for c in b.columns]
    rows = []
    for ra in a.rows:
        for rb in index.get(ra[key_a], ()):
            row = {f'{a.name}.{k}': v for k, v in ra.items()}
            row.update({f'{b.name}.{k}': v for k, v in rb.items()})
            rows.append(row)
    return Table(f'{a.name}⋈{b.name}', cols, rows)


# ---------- 社交网络小样（P3 主题：评论树 + 倒排索引） ----------

def users_table():
    return Table('users', ['id', 'name'], [
        {'id': 1, 'name': 'Ada'},
        {'id': 2, 'name': 'Hacker'},
        {'id': 3, 'name': 'Nobody'},
    ])


def comments_table():
    return Table('comments', ['id', 'user_id', 'body', 'likes'], [
        {'id': 10, 'user_id': 1, 'body': 'SICP 永远的神', 'likes': 42},
        {'id': 11, 'user_id': 2, 'body': '元循环求值太美', 'likes': 17},
        {'id': 12, 'user_id': 1, 'body': '蹦床救了我的栈', 'likes': 5},
        {'id': 13, 'user_id': 3, 'body': '围观', 'likes': 0},
    ])


def top_authors(min_likes=10):
    """SQL: SELECT u.name, COUNT(*) FROM comments c JOIN users u
            ON c.user_id = u.id WHERE c.likes >= 10 GROUP BY u.name;
       —— 用我们的算子表达（L24 对照）。"""
    hot = select(comments_table(), lambda r: r['likes'] >= min_likes)
    joined = hash_join(hot, users_table(), 'user_id', 'id')
    counts = {}
    for row in joined.rows:
        name = row['users.name']
        counts[name] = counts.get(name, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])


def _selftest():
    u, c = users_table(), comments_table()
    nl = nested_loop_join(c, u, lambda rc, ru: rc['user_id'] == ru['id'])
    hj = hash_join(c, u, 'user_id', 'id')
    assert len(nl) == len(hj) == 4
    r = select(c, lambda row: row['likes'] > 10)
    assert len(r) == 2
    o = order_by(project(c, ['body', 'likes']), key=lambda x: -x['likes'])
    assert o.rows[0]['body'] == 'SICP 永远的神'
    assert top_authors(10) == [('Ada', 1), ('Hacker', 1)]
    print('minisql selftest OK')


if __name__ == '__main__':
    _selftest()
