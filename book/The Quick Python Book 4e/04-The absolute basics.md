# 04 · The absolute basics

> 一句话定位：数字、字符串、变量、运算符——最小可用语法地基。
> 原书 pp. 英文 4e 第 4 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 4.1 | 数字 | int/float/complex |
| 4.2 | 运算符 | 算术/比较/逻辑 |
| 4.3 | 字符串基础 | 字面量与拼接 |
| 4.4 | 变量与赋值 | 名绑定对象 |
| 4.5 | 类型转换 | 显式 |

## 核心精讲

```
# 教学示意，不参与构建
x = 3 + 4.0          # float
y = int('42')        # 显式转换
name = 'Ada'
msg = f'{name} = {y}' # f-string
print(msg)
```

- 整数任意精度（`int` 无溢出）；`float` 是双精度；`complex` 复数。
- 运算符优先级同数学；`**` 乘方。
- 字符串用 f-string 插值（3.6+）。

## 版本演进

- f-string（PEP 498）3.6；3.12 支持嵌套引号/多行。
- `int.bit_count()`（3.10）统计二进制 1 的个数。
- `math` 模块持续扩展。

## 经典论文与原始文献

- PEP 498 — f-string；Python 数字类型文档。
- Python 教程「An Informal Introduction」。

## 近年研究与工业界开源实践（2015–2026）

- `decimal`/`fractions` 做精确计算（金融）。
- 类型标注 `int | float` 表达数值联合。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 浮点相等用 `==` | 用 `math.isclose` |
| int 会溢出 | Python int 任意精度 |
| 拼接混类型 | 先转字符串 |
| 🔧 4e 提 3.13 新数值 | 以官方为准 |

## 与其他章 / 其他书的联系

- 字符串详述见[第06章 Strings](06-Strings.md)。
- 与 [`Automate the Boring Stuff with Python 3e/04-列表.md`](../Automate the Boring Stuff with Python 3e/04-列表.md) 基础互通。
