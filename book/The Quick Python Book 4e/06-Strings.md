# 06 · Strings

> 一句话定位：字符串的不可变本质、常用方法与格式化——文本处理支柱。
> 原书 pp. 英文 4e 第 6 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 6.1 | 不可变 | 方法返回新串 |
| 6.2 | 方法 | split/join/strip |
| 6.3 | 格式化 | f-string/format |
| 6.4 | 编码 | UTF-8 |
| 6.5 | 原始串 | 正则/路径 |

## 核心精讲

```
# 教学示意，不参与构建
s = '  hi  '
print(s.strip().upper())          # 'HI'
parts = 'a,b,c'.split(',')        # ['a','b','c']
print('-'.join(parts))            # 'a-b-c'
raw = r'C:\new'                   # 不转义
```

- 字符串不可变；所有方法返回新串。
- `split/join` 是文本拆分合并核心。
- `f-string` 首选格式化；`removeprefix/removesuffix`（3.9）。

## 版本演进

- f-string（PEP 498）3.6；`=` 自文档（3.8）；3.12 嵌套引号。
- `str.removeprefix/removesuffix`（3.9）。
- `str` 模板 `t-string`（PEP 750，3.14 实验）。

## 经典论文与原始文献

- PEP 498 / PEP 750；Python `string`/`textwrap` 文档。
- Unicode 与 UTF-8 规范。

## 近年研究与工业界开源实践（2015–2026）

- `rich` 彩色文本；`regex` 库高级匹配。
- `unidecode` 做 ASCII 折叠。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 循环 `+` 拼大串 | 用 `join` |
| 漏 `encoding='utf-8'` | 始终显式 |
| 路径忘原始串 | 用 `r'...'` 或 `pathlib` |
| 🔧 4e 提 3.13 字符串 | 以官方为准 |

## 与其他章 / 其他书的联系

- 正则见[第16章 Regular expressions](16-Regular expressions.md)。
- 路径见 [`Automate the Boring Stuff with Python 3e/concepts/文件路径与pathlib.md`](../Automate the Boring Stuff with Python 3e/concepts/文件路径与pathlib.md)。
