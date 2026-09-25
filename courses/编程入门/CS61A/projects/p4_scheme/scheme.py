"""scheme.py —— P4：用 Python 解释 Scheme（最小元循环解释器，对应讲义 L19-L22）。

结构（对照 CP §4 / SICP §4.1）：
    源码 → utils.scheme_read → AST(Pair/Symbol) → scheme_eval/apply → 值
核心特性：
  * 特殊形式：define / set! / lambda / if / cond / let(顺序绑定, 同 P4) /
    begin / quote / define-macro / cons-stream
  * 词法作用域：Frame 链，parent 指向**定义处**（L02/L06/L21）
  * 尾调用 O(1) Python 栈：scheme_eval 为 while 状态机——官方 P4 用 TailCall
    数据对象 + 外层蹦床；这里是与之等价的"内联蹦床"写法（L22）
  * 宏：define-macro 在**求值前**做"表达式→表达式"变换（L22）
  * 流：cons-stream 的 cdr 位为 memoized Thunk（delay/force，L23）
用法：
    python scheme.py              # REPL
    python scheme.py --test       # 内建测试
    python scheme.py demo.scm     # 跑脚本
自检：python -m py_compile utils.py scheme.py
"""

import sys

from utils import (Pair, Symbol, nil, is_nil, scheme_tokens, read_all,
                   display, SchemeSyntaxError)


# ---------------- 错误与环境 ----------------

class SchemeError(Exception):
    pass


class Frame:
    """一个作用域：名字→值 + 父框架指针（L02 环境图的代码化）。"""

    def __init__(self, parent=None):
        self.mapping = {}
        self.parent = parent

    def lookup(self, name):
        frame = self
        while frame is not None:
            if name in frame.mapping:
                return frame.mapping[name]
            frame = frame.parent
        raise SchemeError(f'未绑定的名字: {name.name}')

    def define(self, name, value):
        self.mapping[name] = value

    def assign(self, name, value):
        frame = self
        while frame is not None:
            if name in frame.mapping:
                frame.mapping[name] = value
                return
            frame = frame.parent
        raise SchemeError(f'set! 目标未定义: {name.name}')


# ---------------- 过程 / 宏 / 惰性对象 ----------------

class BuiltinProcedure:
    def __init__(self, fn, name):
        self.fn, self.name = fn, name

    def apply(self, args):
        return self.fn(*args)

    def __repr__(self):
        return f'#<procedure {self.name}>'


class Procedure:
    """复合过程：参数符号 + 体表达式列表 + 闭合环境（L06 闭包三件套）。"""

    def __init__(self, params, body, env, name='lambda'):
        self.params, self.body, self.env, self.name = params, body, env, name

    def __repr__(self):
        return f'#<procedure {self.name}>'


class Macro:
    def __init__(self, params, body, env, name):
        self.params, self.body, self.env, self.name = params, body, env, name

    def __repr__(self):
        return f'#<macro {self.name}>'


class Thunk:
    """delayed 表达式：memoized force（L23）。"""

    def __init__(self, expr, env):
        self.expr, self.env = expr, env
        self.value, self.forced = None, False

    def force(self):
        if not self.forced:
            self.value = scheme_eval(self.expr, self.env)
            self.forced = True
        return self.value

    def __repr__(self):
        return f'#<promise {display(self.expr)}>'


def force_if_thunk(v):
    return v.force() if isinstance(v, Thunk) else v


# ---------------- 参数绑定（支持点参数 a b . rest） ----------------

def bind_params(params, arg_values, frame, what):
    names = []
    cur = params
    while isinstance(cur, Pair) and not cur.is_nil():
        names.append(cur.first)
        cur = cur.rest
    if isinstance(cur, Symbol):                       # 变长
        if len(arg_values) < len(names):
            raise SchemeError(f'{what}: 参数太少')
        rest = nil
        for a in reversed(arg_values[len(names):]):
            rest = Pair(a, rest)
        frame.define(cur, rest)
        for p, a in zip(names, arg_values):
            frame.define(p, a)
    elif is_nil(cur):                                 # 精确元数
        if len(arg_values) != len(names):
            raise SchemeError(f'{what}: 需 {len(names)} 参，得 {len(arg_values)}')
        for p, a in zip(names, arg_values):
            frame.define(p, a)
    else:
        raise SchemeError(f'{what}: 参数表 {display(params)} 不合法')


# ---------------- 求值主循环（while 状态机 = 内联蹦床） ----------------

class _Jump:
    """特殊形式把"尾位置表达式"交还给主循环：不增加 Python 栈（L22）。"""

    __slots__ = ('expr', 'env')

    def __init__(self, expr, env):
        self.expr, self.env = expr, env


def scheme_eval(expr, env):
    while True:
        if isinstance(expr, (bool, int, float, str)):
            return expr
        if isinstance(expr, Symbol):
            return force_if_thunk(env.lookup(expr))
        if not isinstance(expr, Pair):
            raise SchemeError(f'无法求值: {expr!r}')
        if expr.is_nil():
            raise SchemeError('空组合式 () 无法求值')

        head = expr.first
        operand_exprs = expr.to_pylist()[1:]

        if isinstance(head, Symbol) and head.name in SPECIAL_FORMS:
            outcome = SPECIAL_FORMS[head.name](operand_exprs, env)
            if isinstance(outcome, _Jump):
                expr, env = outcome.expr, outcome.env
                continue
            return outcome

        # 组合式：应用序 —— 先运算符，再运算目，后应用（L02）
        proc = scheme_eval(expr.first, env)
        if isinstance(proc, Macro):
            expr = macro_expand(proc, operand_exprs)   # 展开后继续循环（尾位置）
            continue
        args = [scheme_eval(a, env) for a in operand_exprs]
        if isinstance(proc, BuiltinProcedure):
            return proc.apply(args)
        if not isinstance(proc, Procedure):
            raise SchemeError(f'不可调用: {display(proc)}')
        frame = Frame(proc.env)                        # parent=闭合环境（L06）
        bind_params(proc.params, args, frame, proc.name)
        for e in proc.body[:-1]:                       # begin 语义
            scheme_eval(e, frame)
        expr, env = proc.body[-1], frame               # 末项在尾位置：尾递归 O(1)


def macro_expand(macro, operand_exprs):
    """宏体在参数=**未求值表达式**的框架里求值 → 产物代码。"""
    frame = Frame(macro.env)
    bind_params(macro.params, operand_exprs, frame, macro.name)
    result = None
    for e in macro.body:
        result = scheme_eval(e, frame)
    return result


# ---------------- 特殊形式 ----------------

def sf_quote(operands, env):
    if len(operands) != 1:
        raise SchemeError('quote 需要 1 个参数')
    return operands[0]


def sf_define(operands, env):
    if not operands:
        raise SchemeError('空 define')
    target = operands[0]
    if isinstance(target, Symbol):                     # (define x expr)
        if len(operands) < 2:
            raise SchemeError('define 缺少值')
        env.define(target, scheme_eval(operands[1], env))
        return target
    if isinstance(target, Pair):                       # (define (f . p) body...)
        name = target.first
        if not isinstance(name, Symbol):
            raise SchemeError('define 过程名必须是符号')
        env.define(name, Procedure(target.rest, operands[1:], env, name))
        return name                                    # 先绑壳：递归即刻可用（L21）
    raise SchemeError('define 目标非法')


def sf_set(operands, env):
    if len(operands) != 2 or not isinstance(operands[0], Symbol):
        raise SchemeError('set! 需要 (set! 名字 值)')
    env.assign(operands[0], scheme_eval(operands[1], env))
    return operands[0]


def sf_lambda(operands, env):
    return Procedure(operands[0], operands[1:], env)


def sf_if(operands, env):
    if len(operands) < 2:
        raise SchemeError('if 需要谓词与分支')
    pred = scheme_eval(operands[0], env)
    branch = operands[1] if pred else \
        (operands[2] if len(operands) > 2 else None)
    return _Jump(branch, env) if branch is not None else None


def sf_cond(operands, env):
    for clause_expr in operands:
        if not isinstance(clause_expr, Pair) or clause_expr.is_nil():
            raise SchemeError('cond 子句非法')
        parts = clause_expr.to_pylist()
        pred = parts[0]
        hit = (isinstance(pred, Symbol) and pred.name == 'else') or \
            bool(scheme_eval(pred, env))
        if hit:
            body = parts[1:]
            for e in body[:-1]:
                scheme_eval(e, env)
            return _Jump(body[-1], env) if body else None
    return None


def sf_begin(operands, env):
    for e in operands[:-1]:
        scheme_eval(e, env)
    return _Jump(operands[-1], env) if operands else None


def sf_let(operands, env):
    """(let (b1 b2 ...) body...)：按顺序在 new frame 求值绑定（P4 风格）。"""
    frame = Frame(env)
    for binder in operands[0].to_pylist():
        parts = binder.to_pylist()
        if len(parts) != 2 or not isinstance(parts[0], Symbol):
            raise SchemeError(f'let 绑定非法: {display(binder)}')
        frame.define(parts[0], scheme_eval(parts[1], frame))
    body = operands[1:]
    for e in body[:-1]:
        scheme_eval(e, frame)
    return _Jump(body[-1], frame) if body else None


def sf_define_macro(operands, env):
    name, params, body = operands[0], operands[1], operands[2:]
    if not isinstance(name, Symbol):
        raise SchemeError('define-macro 名字必须是符号')
    env.define(name, Macro(params, body, env, name))
    return name


def sf_cons_stream(operands, env):
    if len(operands) != 2:
        raise SchemeError('cons-stream 需要 2 个参数')
    head = scheme_eval(operands[0], env)               # car 严格
    return Pair(head, Thunk(operands[1], env))         # cdr 惰性 + memo（L23）


def sf_and(operands, env):
    result = True
    for e in operands:                                 # 短路（L01 语义）
        result = scheme_eval(e, env)
        if not result:
            return result
    return result


def sf_or(operands, env):
    result = False
    for e in operands:
        result = scheme_eval(e, env)
        if result:
            return result
    return result


SPECIAL_FORMS = {
    'quote': sf_quote, 'define': sf_define, 'set!': sf_set,
    'lambda': sf_lambda, 'if': sf_if, 'cond': sf_cond, 'begin': sf_begin,
    'let': sf_let, 'define-macro': sf_define_macro,
    'cons-stream': sf_cons_stream, 'and': sf_and, 'or': sf_or,
}


# ---------------- 内建过程 ----------------

def _pair_car(x):
    if not isinstance(x, Pair) or x.is_nil():
        raise SchemeError('car: 需要非空表')
    return x.first


def _pair_cdr(x):
    if not isinstance(x, Pair) or x.is_nil():
        raise SchemeError('cdr: 需要非空表')
    return force_if_thunk(x.rest)


def _list(*items):
    out = nil
    for it in reversed(items):
        out = Pair(it, out)
    return out


def _append(*lists):
    result = lists[-1] if lists else nil
    for lst in reversed(lists[:-1]):
        for e in reversed(lst.to_pylist()):
            result = Pair(e, result)
    return result


def _quotient(a, b):
    if b == 0:
        raise SchemeError('quotient 除数为 0')
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q           # 截断除法


def _modulo(a, b):
    if b == 0:
        raise SchemeError('modulo 除数为 0')
    return a - (a // b) * b                            # 地板除 → 欧几里得 mod（L01）


def _true_div(a, b):
    if b == 0:
        raise SchemeError('/ 除数为 0')
    if isinstance(a, int) and isinstance(b, int):
        from fractions import Fraction
        return Fraction(a, b)                          # 精确真除法（L01）
    return a / b


def _chain_cmp(a, rest, op):
    cur = a
    for x in rest:
        if not op(cur, x):
            return False
        cur = x
    return True


def _scheme_error(*m):
    raise SchemeError(' '.join(str(display(x)) for x in m))


def _display(v):
    sys.stdout.write(v if isinstance(v, str) else display(v))
    return None


def _mul(*a):
    out = 1
    for x in a:
        out *= x
    return out


def _divn(a, *rest):
    if not rest:
        return _true_div(1, a)
    out = a
    for x in rest:
        out = _true_div(out, x)
    return out


BUILTIN_DEFS = {
    '+': lambda *a: sum(a),
    '-': lambda a, *r: -a if not r else sum([a] + [-x for x in r]),
    '*': _mul,
    '/': _divn,
    'quotient': _quotient, 'modulo': _modulo,
    'abs': abs, 'min': min, 'max': max,
    'expt': lambda a, b: a ** b,
    '=': lambda a, *r: _chain_cmp(a, r, lambda x, y: x == y),
    '<': lambda a, *r: _chain_cmp(a, r, lambda x, y: x < y),
    '>': lambda a, *r: _chain_cmp(a, r, lambda x, y: x > y),
    'not': lambda a: not a,
    'cons': Pair, 'car': _pair_car, 'cdr': _pair_cdr,
    'list': _list, 'append': _append,
    'null?': is_nil,
    'pair?': lambda x: isinstance(x, Pair) and not x.is_nil(),
    'eq?': lambda a, b: a is b or a == b,
    'equal?': lambda a, b: a == b,
    'symbol?': lambda x: isinstance(x, Symbol),
    'number?': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
    'string?': lambda x: isinstance(x, str),
    'string-length': lambda x: len(x),
    'string-append': lambda *xs: ''.join(xs),
    'string=?': lambda a, b: a == b,
    'display': _display,
    'newline': lambda: (print(), None)[1],
    'force': force_if_thunk,
    'boolean?': lambda x: isinstance(x, bool),
    'error': _scheme_error,
}


def make_global_env():
    env = Frame(None)
    for name, fn in BUILTIN_DEFS.items():
        env.define(Symbol(name), BuiltinProcedure(fn, name))
    env.define(Symbol('nil'), nil)
    return env


PRELUDE = """
(define (map f xs)
  (if (null? xs) '()
      (cons (f (car xs)) (map f (cdr xs)))))
(define (filter keep? xs)
  (cond ((null? xs) '())
        ((keep? (car xs)) (cons (car xs) (filter keep? (cdr xs))))
        (else (filter keep? (cdr xs)))))
(define (foldl f init xs)
  (if (null? xs) init (foldl f (f init (car xs)) (cdr xs))))
(define (stream-ref s n)
  (if (= n 0) (car s) (stream-ref (cdr s) (- n 1))))
(define (list-ref xs n)
  (if (= n 0) (car xs) (list-ref (cdr xs) (- n 1))))
(define (integers-from n) (cons-stream n (integers-from (+ n 1))))
"""


def run_exprs(src, env):
    last = None
    for expr in read_all(src):
        last = scheme_eval(expr, env)
    return last


# ---------------- 测试 ----------------

def _test():
    from utils import Symbol as S
    env = make_global_env()
    run_exprs(PRELUDE, env)

    def ev(src):
        return run_exprs(src, env)

    assert ev('(+ 1 2 (* 3 4))') == 15
    assert ev('(- 10)') == -10 and ev('(- 10 1 2)') == 7
    assert ev('(* 2 3 4)') == 24
    assert ev('(/ 8 2)') == 4 and str(ev('(/ 1 3)')) == '1/3'      # Fraction
    assert ev('(expt 2 100)') == 2 ** 100                          # bignum
    assert ev('(quotient 7 2)') == 3 and ev('(modulo -7 2)') == 1
    assert ev('(define (fact n) (if (= n 0) 1 (* n (fact (- n 1)))))') == S('fact')
    assert ev('(fact 10)') == 3628800
    ev('(define (loop n acc) (if (= n 0) acc (loop (- n 1) (+ acc 1))))')
    assert ev('(loop 200000 0)') == 200000                         # 尾递归不死
    assert ev('((lambda (x) (+ x 1)) 41)') == 42
    assert ev('(let ((x 1) (y (+ x 1))) (+ x y))') == 3
    assert ev('(define c 0) (set! c (+ c 41)) (set! c (+ c 1)) c') == 42
    assert ev('\'a') == S('a') and ev('"(hello)"') == '(hello)'
    assert ev('(car (cdr \'(1 2 3)))') == 2
    assert ev('(append \'(1 2) \'(3))') == _list(1, 2, 3)
    assert ev('(define f2 (lambda xs xs)) (f2 1 2 3)') == _list(1, 2, 3)
    assert ev('(map (lambda (x) (* x x)) \'(1 2 3))') == _list(1, 4, 9)
    assert ev('(filter number? \'(1 a "s" 2))') == _list(1, 2)
    assert ev('(foldl + 0 \'(1 2 3))') == 6
    # 宏（L22）：when
    ev("(define-macro when (pred . rest) (cons 'if (cons pred (list (cons 'begin rest)))))")
    assert ev('(when (> 3 2) 40 42)') == 42           # begin 语义：末项为值
    assert ev('(when (< 3 2) 999)') is None
    # 流（L23）
    ev('(define ones (cons-stream 1 ones))')
    assert ev('(car ones)') == 1 and ev('(car (cdr (cdr ones)))') == 1
    ev('(define ints (integers-from 1))')
    assert ev('(stream-ref ints 100)') == 101
    print('scheme selftest OK')


# ---------------- REPL ----------------

def _depth(tokens):
    return sum(1 for t in tokens if t == '(') - sum(1 for t in tokens if t == ')')


def repl():
    env = make_global_env()
    run_exprs(PRELUDE, env)
    print('P4 mini-Scheme —— Ctrl-C / Ctrl-D 退出；测试用 python scheme.py --test')
    buf = ''
    while True:
        try:
            line = input('> ' if not buf.strip() else '  ')
        except (EOFError, KeyboardInterrupt):
            print()
            break
        buf = (buf + '\n' + line) if buf.strip() else line
        if not buf.strip():
            continue
        try:
            d = _depth(scheme_tokens(buf))
        except SchemeSyntaxError as e:
            print(f'语法错误: {e}')
            buf = ''
            continue
        if d > 0:
            continue                                   # 等待右括号
        if d < 0:
            print('语法错误: 括号多余')
            buf = ''
            continue
        try:
            exprs = read_all(buf)
        except SchemeSyntaxError as e:
            print(f'语法错误: {e}')
            buf = ''
            continue
        buf = ''
        for expr in exprs:
            try:
                result = scheme_eval(expr, env)
            except SchemeError as e:
                print(f'错误: {e}')
                continue
            if result is not None:
                print(display(result))


def main(argv):
    if '--test' in argv:
        _test()
        return
    files = [a for a in argv if not a.startswith('-')]
    env = make_global_env()
    run_exprs(PRELUDE, env)
    if files:
        for path in files:
            with open(path, encoding='utf-8') as f:
                run_exprs(f.read(), env)
        return
    repl()


if __name__ == '__main__':
    main(sys.argv[1:])
