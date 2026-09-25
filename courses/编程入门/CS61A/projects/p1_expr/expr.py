"""expr.py —— P1 整数/布尔表达式完整实现（对应讲义 L01-L02、L04、L20 的前哨）。

一个迷你算术-逻辑表达式语言：
    expr   := or_expr            （or / and / not 短路，语义与 Python 一致）
    or_expr:= and_expr ('or' and_expr)*
    and_expr:= not_expr ('and' not_expr)*
    not_expr:= 'not' not_expr | cmp
    cmp    := arith (('<'|'>'|'<='|'>='|'=='|'!=') arith)*   （链式比较）
    arith  := term (('+'|'-') term)*
    term   := power (('*'|'/'|'//'|'%') power)*
    power  := unary ('**' power)?      （右结合）
    unary  := ('+'|'-') unary | atom
    atom   := NUMBER | 'True' | 'False' | '(' expr ')'

'/' 产生精确 Rat（见 rat.py）；'//' '%' 采用 Python 的地板除/余数语义（L01）。
词法/递归下降解析是 L20 解释器一讲的最初练手。

自检：python -m py_compile expr.py
"""

import re

from rat import Rat

TOKEN_RE = re.compile(r"""
    \s*(?:
        (?P<num>\d+(?:\.\d+)?)
      | (?P<op>\*\*|//|<=|>=|==|!=|[+\-*/%()<>])
      | (?P<name>[A-Za-z_][A-Za-z0-9_]*)
    )""", re.VERBOSE)


class ParseError(Exception):
    pass


class EvalError(Exception):
    pass


def tokenize(src):
    """词法分析：字符串 → (kind, value) 列表。"""
    tokens, pos = [], 0
    while pos < len(src):
        if src[pos].isspace():
            pos += 1
            continue
        m = TOKEN_RE.match(src, pos)
        if not m:
            raise ParseError(f'无法识别的字符: {src[pos]!r} @ {pos}')
        pos = m.end()
        if m.group('num'):
            text = m.group('num')
            value = float(text) if '.' in text else int(text)
            tokens.append(('num', value))
        elif m.group('op'):
            tokens.append(('op', m.group('op')))
        else:
            tokens.append(('name', m.group('name')))
    tokens.append(('end', None))
    return tokens


class Parser:
    """递归下降：语法即代码（对照 L20 §1.3）。"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def take(self, kind, value=None):
        k, v = self.peek()
        if k != kind or (value is not None and v != value):
            raise ParseError(f'期望 {value or kind}，得到 {v or k}')
        self.i += 1
        return v

    def parse(self):
        tree = self.or_expr()
        if self.peek()[0] != 'end':
            raise ParseError(f'多余内容: {self.peek()[1]}')
        return tree

    def or_expr(self):
        node = self.and_expr()
        while self.peek() == ('name', 'or'):
            self.take('name', 'or')
            node = ('or', node, self.and_expr())
        return node

    def and_expr(self):
        node = self.not_expr()
        while self.peek() == ('name', 'and'):
            self.take('name', 'and')
            node = ('and', node, self.not_expr())
        return node

    def not_expr(self):
        if self.peek() == ('name', 'not'):
            self.take('name', 'not')
            return ('not', self.not_expr())
        return self.cmp()

    def cmp(self):
        node = self.arith()
        while self.peek()[0] == 'op' and self.peek()[1] in \
                ('<', '>', '<=', '>=', '==', '!='):
            op = self.take('op')
            node = ('cmp', op, node, self.arith())
        return node

    def arith(self):
        node = self.term()
        while self.peek()[0] == 'op' and self.peek()[1] in ('+', '-'):
            op = self.take('op')
            node = ('bin', op, node, self.term())
        return node

    def term(self):
        node = self.power()
        while self.peek()[0] == 'op' and self.peek()[1] in ('*', '/', '//', '%'):
            op = self.take('op')
            node = ('bin', op, node, self.power())
        return node

    def power(self):
        base = self.unary()
        if self.peek() == ('op', '**'):
            self.take('op', '**')
            return ('bin', '**', base, self.power())   # 右结合
        return base

    def unary(self):
        if self.peek() == ('op', '-'):
            self.take('op', '-')
            return ('neg', self.unary())
        if self.peek() == ('op', '+'):
            self.take('op', '+')
            return self.unary()
        return self.atom()

    def atom(self):
        k, v = self.peek()
        if k == 'num':
            self.take('num')
            return ('lit', v)
        if k == 'name' and v in ('True', 'False'):
            self.take('name')
            return ('lit', v == 'True')
        if k == 'op' and v == '(':
            self.take('op', '(')
            node = self.or_expr()
            self.take('op', ')')
            return node
        raise ParseError(f'非法原子: {v!r}')


# ---------------- 求值 ----------------

def _floordiv(a, b):
    if isinstance(a, Rat) or isinstance(b, Rat):
        q = Rat(a) / Rat(b) if isinstance(b, Rat) else a / b
        import math
        return math.floor(q)
    return a // b


def _mod(a, b):
    if isinstance(a, Rat) or isinstance(b, Rat):
        return Rat(a) - _floordiv(a, b) * Rat(b)
    return a % b


def _as_rat(x):
    return x if isinstance(x, Rat) else (Rat(*x.as_integer_ratio()) if isinstance(x, float) else Rat(x))


def _binop(op, a, b):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            raise EvalError('除数为 0')
        if isinstance(a, int) and isinstance(b, int) and a % b == 0:
            return a // b                      # 精确整除保持 int
        if isinstance(a, float) or isinstance(b, float):
            return a / b
        return _as_rat(a) / _as_rat(b)         # 真除法 → 精确分数
    if op == '//':
        return _floordiv(a, b)
    if op == '%':
        return _mod(a, b)
    if op == '**':
        if isinstance(a, int) and isinstance(b, int) and b >= 0:
            return a ** b                      # 任意精度整数幂（L01）
        if isinstance(a, int) and isinstance(b, int):
            return _as_rat(a) ** b
        return a ** b
    raise EvalError(f'未知运算符 {op}')


_CMP = {'<': lambda a, b: a < b, '>': lambda a, b: a > b,
        '<=': lambda a, b: a <= b, '>=': lambda a, b: a >= b,
        '==': lambda a, b: a == b, '!=': lambda a, b: a != b}


def evaluate(node):
    """求值 AST。or/and 短路且返回操作数本身（L01 §1.4）。"""
    tag = node[0]
    if tag == 'lit':
        return node[1]
    if tag == 'neg':
        return -evaluate(node[1])
    if tag == 'bin':
        return _binop(node[1], evaluate(node[2]), evaluate(node[3]))
    if tag == 'cmp':
        _, op, left, right = node
        a, b = evaluate(left), evaluate(right)
        return _CMP[op](a, b)
    if tag == 'not':
        return not evaluate(node[1])
    if tag == 'and':
        a = evaluate(node[1])
        return evaluate(node[2]) if a else a
    if tag == 'or':
        a = evaluate(node[1])
        return a if a else evaluate(node[2])
    raise EvalError(f'未知节点 {tag}')


def calc(src):
    """字符串 → 值。"""
    return evaluate(Parser(tokenize(src)).parse())


def _selftest():
    assert calc('1 + 2 * 3') == 7
    assert calc('2 ** 2 ** 3') == 256                  # 右结合
    assert calc('-7 // 2') == -4 and calc('-7 % 2') == 1   # L01 地板除
    assert calc('7 / 2') == Rat(7, 2)                  # 真除法 → 精确分数
    assert str(calc('1/3 + 1/6')) == '1/2'
    assert calc('2 ** 100 % 1000') == 376              # bignum
    assert calc('1 < 2 < 3') is True                   # 链式比较
    assert calc('0 or 42') == 42 and calc('1 and 2') == 2   # 短路/返回操作数
    assert calc('not 0') is True
    assert calc('(1 + 2) * 3') == 9
    assert str(calc('1.5 + 2')) == '3.5'
    print('expr selftest OK')
    for line in ('1+1', '7/2', '2**10', '1 < 2 and 3 > 2 or False'):
        print(f'  {line:24s} => {calc(line)!r}')


if __name__ == '__main__':
    _selftest()
