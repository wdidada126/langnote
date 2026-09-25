"""rat.py —— P1 玩具分数（对应讲义 L01：整数/精确算术；CP §1.1/§2.1 数据抽象）。

只用标准库。Rat 是不可变有理数：构造时自动约分、分母恒正，
实现 SICP 练习 2.1 的"域假设归构造函数负责"。
自检：python -m py_compile rat.py
"""

from math import gcd


class Rat:
    """精确有理数 p/q。支持 + - * / ** 幂(整数指数) 与比较。"""

    __slots__ = ('p', 'q')

    def __init__(self, p, q=1):
        if q == 0:
            raise ZeroDivisionError('Rat 分母不能为 0')
        if q < 0:                      # 符号归一到分子
            p, q = -p, -q
        g = gcd(abs(p), q)
        object.__setattr__(self, 'p', p // g)
        object.__setattr__(self, 'q', q // g)

    def __setattr__(self, k, v):       # 不可变
        raise AttributeError('Rat is immutable')

    # ---- 与 int 互转 ----
    @staticmethod
    def _coerce(x):
        if isinstance(x, Rat):
            return x
        if isinstance(x, int):
            return Rat(x)
        if isinstance(x, float):
            return Rat(*x.as_integer_ratio())   # 二进制精确展开
        return NotImplemented

    # ---- 算术 ----
    def __add__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return Rat(self.p * o.q + o.p * self.q, self.q * o.q)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return Rat(self.p * o.p, self.q * o.q)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        if o.p == 0:
            raise ZeroDivisionError('division by zero')
        return Rat(self.p * o.q, self.q * o.p)

    def __rtruediv__(self, other):
        return self._coerce(other).__truediv__(self)

    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError('Rat 仅支持整数指数')
        if n < 0:
            return Rat(self.q ** -n, self.p ** -n)
        return Rat(self.p ** n, self.q ** n)

    def __neg__(self):
        return Rat(-self.p, self.q)

    # ---- 比较 ----
    def __eq__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return self.p == o.p and self.q == o.q

    def __lt__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        return self.p * o.q < o.p * self.q

    def __le__(self, other):
        return self == other or self < other

    def __hash__(self):
        return hash((self.p, self.q))

    def __float__(self):
        return self.p / self.q

    def __repr__(self):
        return f'{self.p}/{self.q}' if self.q != 1 else str(self.p)


def _selftest():
    assert repr(Rat(4, 6)) == '2/3'
    assert Rat(-1, -2) == Rat(1, 2)
    assert Rat(1, 2) + Rat(1, 3) == Rat(5, 6)
    assert Rat(2, 3) * 3 == 2
    assert Rat(1, 2) / Rat(1, 4) == 2
    assert Rat(1, 2) ** -2 == 4
    assert Rat(1, 3) < Rat(1, 2)
    assert float(Rat(1, 2)) == 0.5
    assert 0.1 + 0.2 != 0.3                       # float 的坑……
    assert Rat(1, 10) + Rat(2, 10) == Rat(3, 10)  # ……Rat 无此坑
    print('rat selftest OK')


if __name__ == '__main__':
    _selftest()
