# 第 6 章 用户输入和 while 循环（原书 pp.106–124）

> 让程序「等人输入」并「反复做事」。基线：原书 Python 3.11；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论 |
|---|---|---|
| 6.1 `input()` | 读取字符串 | 永远返回 str，需 `int()` 转换 |
| 6.2 while 循环 | 条件为真就重复 | 注意更新条件防死循环 |
| 6.3 标志/break/continue | 控制流 | `break` 跳出，`continue` 跳本轮 |
| 6.4 避免无限循环 | 确保条件会变假 | Ctrl+C 中断 |
| 6.5 移动列表元素 | while 搬运 | 也可用推导式一步到位 |

## 核心精讲

教学示意，不参与构建：

```python
name = input("What is your name? ")   # 返回 str
age = int(input("How old? "))         # 必须显式转 int

# while：数到 5
current = 1
while current <= 5:
    print(current)
    current += 1                       # 必须更新，否则死循环

# break / continue
for n in range(10):
    if n % 2 == 0:
        continue                       # 跳过偶数
    if n > 7:
        break
    print(n)

# 用 while 从 verified 搬到 confirmed
unconfirmed = ['alice', 'brian', 'candace']
confirmed = []
while unconfirmed:
    confirmed.append(unconfirmed.pop())
```

## 版本演进

- 3.8 海象 `:=`（PEP 572）常配合 `while`：`while (line := f.readline()):`。
- 3.10 更清晰的错误提示让缩进/语法错更易定位。
- 输入处理在 CLI 中用 `argparse` 比交互式 `input` 更工程化（见 [07-函数.md](07-函数.md) 延伸）。

## 经典论文与原始文献

- PEP 572 — Assignment Expressions（2018），https://peps.python.org/pep-0572/ 规范文档，非同行评审论文。
- Python 官方 `input()`/`while` 教程：https://docs.python.org/3/tutorial/inputoutput.html 规范文档。

## 近年研究与工业界开源实践（2015–2026）

- 交互输入在脚本里少用，更多用 `argparse`/`click`/`typer` 收命令行参数。
- 无限循环风险用 `for`+迭代器或明确的退出条件规避。

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
|---|---|---|
| `input()` 直接当数字算 | 抛 TypeError | 用 `int(input(...))` 并捕获 ValueError |
| while 搬运列表 | O(n²) 或繁琐 | 能用推导式/切片别用 while |
| `break`/`continue` 滥用 | 控制流难读 | 优先重写循环条件，少用跳转 |
| 交互式 input 做正式程序 | 不可批处理 | 用 CLI 参数或配置文件 |

## 与其他章 / 其他书的联系

- `int()` 类型转换与 [01-变量和简单数据类型.md](01-变量和简单数据类型.md) 的数字呼应。
- 循环模式深讲见 [../流畅的python2/17-迭代器、生成器和经典协程.md](../流畅的python2/17-迭代器、生成器和经典协程.md)。
