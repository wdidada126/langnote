# 03 · The quick Python overview

> 一句话定位：一章看全 Python——语法、数据结构、函数、类、异常「速览」，建立全局地图。
> 原书 pp. 英文 4e 第 3 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 3.1 | 语法速览 | 缩进/变量 |
| 3.2 | 数据结构 | list/dict/set |
| 3.3 | 函数与类 | def/class |
| 3.4 | 异常 | try/except |
| 3.5 | 模块 | import |

## 核心精讲

```
# 教学示意，不参与构建
# 一页看全：列表推导 + 函数 + 异常
def even_squares(nums):
    return [n * n for n in nums if n % 2 == 0]

try:
    print(even_squares([1, 2, 3, 4]))
except TypeError as e:
    print('类型错误', e)
```

- 缩进即块；变量动态类型但建议标注。
- 列表推导、dict 推导表达力强。
- 一切皆对象，函数/类/模块都是对象。

## 版本演进

- 海象 `:=`（3.8）、匹配 `match`（3.10）让速览更现代。
- PEP 695 类型参数（3.12）简化泛型。

## 经典论文与原始文献

- Python 教程总览：https://docs.python.org/3/tutorial/
- PEP 8 风格指南。

## 近年研究与工业界开源实践（2015–2026）

- 类型标注让「速览」更易维护。
- `rich`/`typer` 让小工具即专业。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 速览后即够用 | 后续章深挖语义细节 |
| 动态类型=随意 | 渐进标注更稳 |
| 🔧 4e 加 notebook/quick-check | 以官方为准 |

## 与其他章 / 其他书的联系

- 细化为后续[第04章](04-The absolute basics.md)–[第24章](24-Exploring data.md)。
- 风格见 [`Effective Python（第2版）/00-总览与阅读地图.md`](../Effective Python（第2版）/00-总览与阅读地图.md)。
