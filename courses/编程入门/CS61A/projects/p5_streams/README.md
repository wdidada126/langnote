# p5 流与惰性求值（Streams & Lazy Evaluation）

> 对应讲次：L12（生成器机制）、L23（SICP §3.5 流）。P4 的 `cons-stream` 已给了
> Scheme 侧；本项目在 **纯 Python 标准库** 里做同一件事的两种写法并实测差异。

## 文件

| 文件 | 内容 |
| --- | --- |
| `streams.py` | Stream 类（首值严格 + 尾流 `Thunk` memoized）与组合子 `integers_from/s_map/s_filter/s_take`；生成器双版本；`ones = cons-stream 1 ones` 自引用无穷流。 |
| `sieve.py` | 无穷埃氏筛双实现（流版可重放 / `yield from` 生成器版一次性）；第 101 个素数的"首走 vs memo 重放"计时演示；孪生素数流。 |

## 运行

```bash
python sieve.py         # 主演示（含断言）
python streams.py       # 自测
```

`run.bat` / `run.sh`；自检：`python -m py_compile streams.py sieve.py`

## 知识点对照

- L23 §1.1：`Thunk.force` = delay/force + memo（无 memo 会指数重算）；
- L23 §1.3：生成器 = 语言内建 delay，但**一次性、不可重放**——`s_take` 两次 vs
  `next` 两次的本质区别；
- L08：惰性把"构造无穷结构"的空间账变成"按需支付"；
- L12：`yield from` 递归流（`gen_sieve` 每发现一个素数就多套一层生成器）；
- P4：同一语义在 Scheme 侧（`cons-stream` 特殊形式）与 Python 侧（闭包+对象）的镜像。
