"""utils.py —— P4 Scheme 解释器的裸金属（对应讲义 L13/L19-L20）。

Pair：Scheme 的 cons 单元（L13 链表可变体）；nil 是约定 first/rest 均为 None 的 Pair。
Symbol：名字（求值时查环境），与字符串 "..."（自求值）严格区分。
scheme_tokens / scheme_read：词法+语法分析（L20：递归下降镜像语法规则）。
自检：python -m py_compile utils.py
"""


class SchemeSyntaxError(Exception):
    pass


class Pair:
    """一个 cons 单元：first=car，rest=cdr。"""

    __slots__ = ('first', 'rest')

    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def is_nil(self):
        return self.first is None and self.rest is None

    def to_pylist(self):
        out, cur = [], self
        while isinstance(cur, Pair) and not cur.is_nil():
            out.append(cur.first)
            cur = cur.rest
        return out

    def sexp(self):
        items, cur = [], self
        while isinstance(cur, Pair) and not cur.is_nil():
            items.append(display(cur.first))
            cur = cur.rest
        if isinstance(cur, Pair) and cur.is_nil():
            return '(' + ' '.join(items) + ')'
        return '(' + ' '.join(items) + ' . ' + display(cur) + ')'

    def __repr__(self):
        return self.sexp()

    def __eq__(self, other):
        return (isinstance(other, Pair) and self.first == other.first
                and self.rest == other.rest)


class Symbol:
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(('sym', self.name))


nil = Pair(None, None)          # Scheme 的 ()


def sym(x):
    return Symbol(x)


def is_nil(v):
    return isinstance(v, Pair) and v.is_nil()


def display(v):
    """Scheme 值的书写形式。"""
    if isinstance(v, Symbol):
        return v.name
    if isinstance(v, str):
        return f'"{v}"'
    if v is True:
        return '#t'
    if v is False:
        return '#f'
    if v is None:
        return '<unspecified>'
    return repr(v)


# ---------------- 词法 ----------------

def scheme_tokens(src):
    """字符串 → token 列表：`(` `)` `'` 独立；字符串整体一个 token；其余按分隔符切。"""
    tokens, i, n = [], 0, len(src)
    while i < n:
        ch = src[i]
        if ch.isspace():
            i += 1
        elif ch in '()\'':
            tokens.append(ch)
            i += 1
        elif ch == ';':                          # 行注释
            while i < n and src[i] != '\n':
                i += 1
        elif ch == '"':
            j = i + 1
            buf = ['"']
            while j < n and src[j] != '"':
                buf.append(src[j])
                j += 1
            if j >= n:
                raise SchemeSyntaxError('未闭合的字符串')
            buf.append('"')
            tokens.append(''.join(buf))
            i = j + 1
        else:
            j = i
            while j < n and not src[j].isspace() and src[j] not in '()\'"':
                j += 1
            tokens.append(src[i:j])
            i = j
    return tokens


# ---------------- 语法分析（递归下降） ----------------

class Reader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def advance(self):
        tok = self.peek()
        self.i += 1
        return tok

    def read(self):
        tok = self.advance()
        if tok is None:
            raise SchemeSyntaxError('意外的输入结束')
        if tok == "'":
            operand = self.read()
            return Pair(Symbol('quote'), Pair(operand, nil))
        if tok == '(':
            items = []
            while True:
                nxt = self.peek()
                if nxt is None:
                    raise SchemeSyntaxError('括号不匹配')
                if nxt == ')':
                    self.advance()
                    break
                if nxt == '.':                   # improper 点对
                    self.advance()
                    tail = self.read()
                    if self.advance() != ')':
                        raise SchemeSyntaxError('非法的点对形式')
                    for item in reversed(items):
                        tail = Pair(item, tail)
                    return tail
                items.append(self.read())
            result = nil
            for item in reversed(items):
                result = Pair(item, result)
            return result
        if tok == ')':
            raise SchemeSyntaxError('多余的 )')
        return self.atom(tok)

    @staticmethod
    def atom(tok):
        if tok == '#t':
            return True
        if tok == '#f':
            return False
        try:
            return int(tok)
        except ValueError:
            pass
        try:
            return float(tok)
        except ValueError:
            pass
        if len(tok) >= 2 and tok[0] == '"' and tok[-1] == '"':
            return tok[1:-1]
        return Symbol(tok)


def scheme_read(src):
    """源码（恰好一个表达式）→ Scheme 数据。"""
    reader = Reader(scheme_tokens(src))
    expr = reader.read()
    if reader.peek() is not None:
        raise SchemeSyntaxError(f'多余内容: {reader.peek()}')
    return expr


def read_all(src):
    """多表达式源码 → Python 列表。"""
    reader = Reader(scheme_tokens(src))
    exprs = []
    while reader.peek() is not None:
        exprs.append(reader.read())
    return exprs


def _selftest():
    expr = scheme_read('(+ 1 (* 2 3))')
    assert expr.first == Symbol('+')
    assert expr.rest.first == 1
    assert repr(scheme_read("(define (f x) 'a)")) == '(define (f x) (quote a))'
    assert scheme_read('()').is_nil()
    assert repr(scheme_read('(1 . 2)')) == '(1 . 2)'
    assert Pair(1, Pair(2, nil)).sexp() == '(1 2)'
    assert scheme_read('"hi there"') == 'hi there'
    assert len(read_all('1 (+ 1 2) (define x 3)')) == 3
    assert scheme_tokens("(a ; c\n b)") == ['(', 'a', 'b', ')']
    print('utils selftest OK')


if __name__ == '__main__':
    _selftest()
