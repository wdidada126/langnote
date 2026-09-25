# Harvard CS50P（2022）— 笔记大纲（骨架）

## L0 Functions, Variables
- `print`/`input`、注释、`snake_case` 命名规范与 `camelCase` 对照。
- 变量作用域初步、参数传递与 `return`。
- `def` 函数定义、文档字符串；主函数 `if __name__ == "__main__"` 惯例。
- 作业锚点：turtle 绘图（函数分解图形）。

## L1 Conditionals
- `if/elif/else`、布尔表达式与 `and/or/not`、`==` 与 `is` 的区别。
- `match-case`（Python 3.10 结构模式匹配）。
- `while True` + 条件退出的循环防御。
- 作业锚点：fuel（分数/百分比转换与异常输入）。

## L2 Loops
- `for i in range()`、`while`、`break/continue/pass`。
- 多重循环与嵌套打印图案；`enumerate`。
- `get_int` 式输入校验循环模式。
- 作业锚点：plates（`*` 堆叠与循环计数）。

## L3 Exceptions
- `try/except/else/finally` 结构与异常类型选择。
- `raise` 主动抛出、自定义异常类。
- "异常不是控制流"的边界讨论。
- 作业锚点：profit（复利公式 + ValueError 处理）。

## L4 Libraries
- 标准库巡礼：`sys`（argv）、`os/pathlib`、`random`、`math`、`json`、`requests` 等。
- `import` 机制、`pip` 安装第三方包、虚拟环境意识启蒙。
- 命令行参数解析（`argv`、`argparse` 简介）。
- 作业锚点：battle/日历类库应用练习。

## L5 Unit Tests
- `pytest` 基础：test 函数、`assert`、fixture。
- `--target`/`expect` 风格与 TDD 最小闭环。
- 覆盖率（coverage）概念与边界用例思维。
- 作业锚点：tests（给既有函数补测试）。

## L6 File I/O
- `open()` 模式与 `with` 上下文管理器。
- 逐行读取、`strip` 清洗、写文件与追加。
- `csv`/`json` 模块的结构化读写。
- 作业锚点：lines（输入输出文件转换）。

## L7 Regular Expressions
- `re.search/match/findall/sub`；`[] . * + ? ^ $ \d \w` 核心语法。
- 贪婪 vs 非贪婪、分组与后向引用；f-string 与正则的转义坑（raw string）。
- `validate` 库对邮箱/URL/TCP 的现成正则。
- 作业锚点：adieu（姓名正则清洗）。

## L8 Object-Oriented Programming
- `class`、`__init__`、实例方法与 `self`。
- magic methods：`__str__`/`__repr__`/`__eq__`/`__lt__`。
- 继承与多态、`super()`、`@property`、`@classmethod`。
- 作业锚点：rooms（类建模与迭代/校验）。

## L9 Et Cetera
- 参数解包：`*args/**kwargs`、iterables/unpack。
- `os.walk`、类型注解（type hints）、`pyfiglet` 等趣味库收尾。
- 综合方法：如何读文档、如何继续学 Python（官方 tutorial/PEP8）。
- 毕业：Final Project（自选主题，提交 spec + 代码）。
