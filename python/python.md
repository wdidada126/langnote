# python

Ip2region (2.0 - xdb) is a offline IP address manager framework and locator, support billions of data segments, ten microsecond searching performance. xdb engine implementation for many programming languages

https://github.com/lionsoul2014/ip2region

而且数分用Python需要掌握的是Numpy、pandas这些数据分析的工具和统计学的知识，后端则是Flask或者Django这些框架以及web相关的知识，这是两个领域的知识。

selenium是爬虫的

python依赖库乱的一比，哪怕指定了版本，两年后，不处理都不一定还能跑

### Python学习路径
python方向 人工智能
爬虫
自动化
Web
科学计算

- Python编程 从入门到实践（第2版）
- 利用Python进行数据分析
- Python数据科学手册
- 流畅的Python
- Python编程快速上手
- Python源码剖析
- Python核心编程（第二版）

[【Python 训练营】Python 每日一练 ---- 第 31 天: k 倍区间](https://xie.infoq.cn/article/87f2f8859c800d72c2275b731)

[python 方法——defaultdict详解](https://xie.infoq.cn/article/6d7ec0675e2c673985a5ba5ec)

Python-Advanced-Program

解决TypeError:'twophase' is an invalid keyword argumet for this function（附：pandas连接oracle）

https://blog.csdn.net/DYyunzhongxian/article/details/102521288/

报错内容：TypeError: expected bytes-like object, not str

例：

```python
a = base64.b64encode(temp)
```

改为：

```python
a = base64.b64encode(bytes(temp, 'utf-8'))
```

python-3.6.14-docs-pdf-a4.zip
https://docs.python.org/zh-cn/3.6/download.html
可以选择语言

python 元编程 metaclass type
python基本数据结构
dict
triple
list


python元编程详解
https://www.jianshu.com/p/644d309b504e
下面这些框架就很好的使用到了元类，他们帮助你在编程过程中，书写更少的代码。

Django
SQLAlchemy
Flask
Theano


[python log to file](https://www.cnblogs.com/nancyzhu/p/8551506.html)

[urllib2](https://docs.python.org/2/library/urllib2.html)



[Python-100-Days](https://github.com/jackfrued/Python-100-Days/blob/master/Day91-100/100.Python面试题集.md)

python tag符号和空格不能混用，否则会报错


Anaconda3-5.3.1-Windows-x86_64
pycharm 设置

最近，由于原有Anaconda环境中的部分第三方库出现了冲突的情况，且基于“Anaconda Prompt (anaconda3)”也无法升级Anaconda与相关库了，因此决定将其卸载并重新安装。参考Anaconda官方网站给出的卸载方法，成功完成了其的卸载与随后的重装工作。首先，我们打开“Anaconda Prompt (anaconda3)”。

https://www.anaconda.com/download

链接：https://www.zhihu.com/question/393199176/answer/2872327488


Python是面向对象的

python build工具
绑定c/c++
哪些常用的库



D:\ProgramData\Anaconda3

python
python3
pip
pip3



AS4314 中国电信
AS4538 教育网


python3

sudo yum -y install python3
centos 7.9升级python3.6到3.8
sudo yum -y install rh-python38
scl enable rh-python38 bash

pip show socketio
查看安装的socketio版本信息

setuptools

whl
pytl打包工具
类似rar zip格式的压缩包 7zip可以打开

pkg打包www

IUS软件源

https://ius.io/



https://www.cnblogs.com/iam-ironman/articles/10969663.html

```python
from selenium import webdriver
options = webdriver.ChromeOptions()
out_path = r'D:\Projects\Spiders'  # 是你想指定的路径
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(executable_path=r'D:\Repo 3\chromedriver.exe', chrome_options=options)
```

python里：单引号‘’和双引号“”外面的r和f的意思
'r'是防止字符转义
如果路径中出现'\t'的话 不加r的话\t就会被转义 而加了'r'之后'\t'就能保留原有的样子
在字符串赋值的时候 前面加'r'可以防止字符串在时候的时候不被转义 原理是在转义字符前加'\'

print字符串前面加f表示格式化字符串，

转义字符 \n



pyc -> .class

python也是虚拟机

try:
    ...
except SomeException:
    tb = sys.exc_info()[2]
    raise OtherException(...).with_traceback(tb)


BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning

Python生成requirements.txt方法
requirements.txt可以通过pip命令自动生成和安装，这种情况更适用于此项目是单独的虚拟python环境
生成requirements.txt文件

pip freeze > requirements.txt
pip3 freeze > requirements.txt
安装requirements.txt依赖

pip install -r requirements.txt
pip3 install -r requirements.txt


pip install requests==2.6.0
pip uninstall xx

python
整数不分类型，或者说它只有一种类型的整数。Python 整数的取值范围是无限的，不管多大或者多小的数字，Python 都能轻松处理。

[python api](https://docs.python.org/3/library/)

Mac:Python 3.7.5

boolean数据操作
and, or, not

int, float, complex

list, tuple, range
string
bytes, bytearray, memoryview
set, frozenset
dict

func语法

def关键字 跨好 冒号
函数体回车

list包含以下函数:

序号	函数
1	len(list)
列表元素个数
2	max(list)
返回列表元素最大值
3	min(list)
返回列表元素最小值
4	list(seq)
将元组转换为列表
Python包含以下方法:

序号	方法
1	list.append(obj)
在列表末尾添加新的对象
2	list.count(obj)
统计某个元素在列表中出现的次数
3	list.extend(seq)
在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
4	list.index(obj)
从列表中找出某个值第一个匹配项的索引位置
5	list.insert(index, obj)
将对象插入列表
6	list.pop([index=-1])
移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
7	list.remove(obj)
移除列表中某个值的第一个匹配项
8	list.reverse()
反向列表中元素
9	list.sort( key=None, reverse=False)
对原列表进行排序
10	list.clear()
清空列表
11	list.copy()
复制列表


Python的tuple元组与List类似，不同之处在于元组的元素不能修改。
元组使用小括号，列表使用方括号。
元组创建很简单，只需要在括号中添加元素，并使用逗号隔开即可。

truple	方法及描述
1	cmp(tuple1, tuple2)
比较两个元组元素。
2	len(tuple)
计算元组元素个数。
3	max(tuple)
返回元组中元素最大值。
4	min(tuple)
返回元组中元素最小值。
5	tuple(seq)
将列表转换为元组。

python for操作，跟c、java、js都不一样

### python sys模块

Dynamic objects:

argv -- command line arguments; argv[0] is the script pathname if known
path -- module search path; path[0] is the script directory, else ''
modules -- dictionary of loaded modules

displayhook -- called to show results in an interactive session
excepthook -- called to handle any uncaught exception other than SystemExit
  To customize printing in an interactive session or to install a custom
  top-level exception handler, assign other functions to replace these.

stdin -- standard input file object; used by input()
stdout -- standard output file object; used by print()
stderr -- standard error object; used for error messages
  By assigning other file objects (or objects that behave like files)
  to these, it is possible to redirect all of the interpreter's I/O.

last_type -- type of last uncaught exception
last_value -- value of last uncaught exception
last_traceback -- traceback of last uncaught exception
  These three are only available in an interactive session after a
  traceback has been printed.

Static objects:

builtin_module_names -- tuple of module names built into this interpreter
copyright -- copyright notice pertaining to this interpreter
exec_prefix -- prefix used to find the machine-specific Python library
executable -- absolute path of the executable binary of the Python interpreter
float_info -- a struct sequence with information about the float implementation.
float_repr_style -- string indicating the style of repr() output for floats
hash_info -- a struct sequence with information about the hash algorithm.
hexversion -- version information encoded as a single integer
implementation -- Python implementation information.
int_info -- a struct sequence with information about the int implementation.
maxsize -- the largest supported length of containers.
maxunicode -- the value of the largest Unicode code point
platform -- platform identifier
prefix -- prefix used to find the Python library
thread_info -- a struct sequence with information about the thread implementation.
version -- the version of this interpreter as a string
version_info -- version information as a named tuple
__stdin__ -- the original stdin; don't touch!
__stdout__ -- the original stdout; don't touch!
__stderr__ -- the original stderr; don't touch!
__displayhook__ -- the original displayhook; don't touch!
__excepthook__ -- the original excepthook; don't touch!

Functions:

displayhook() -- print an object to the screen, and save it in builtins._
excepthook() -- print an exception and its traceback to sys.stderr
exc_info() -- return thread-safe information about the current exception
exit() -- exit the interpreter by raising SystemExit
getdlopenflags() -- returns flags to be used for dlopen() calls
getprofile() -- get the global profiling function
getrefcount() -- return the reference count for an object (plus one :-)
getrecursionlimit() -- return the max recursion depth for the interpreter
getsizeof() -- return the size of an object in bytes
gettrace() -- get the global debug tracing function
setcheckinterval() -- control how often the interpreter checks for events
setdlopenflags() -- set the flags to be used for dlopen() calls
setprofile() -- set the global profiling function
setrecursionlimit() -- set the max recursion depth for the interpreter
settrace() -- set the global debug tracing function



python name __filter__

https://blog.csdn.net/weixin_35684521/article/details/81396434

## Python 综合笔记（截至 2026-08）

### 定位与版本边界

Python 的优势是表达力、生态和开发速度，不是“所有场景都比编译型语言快”。它适合自动化、数据处理、Web/API、AI、测试平台、运维工具和胶水层；CPU 密集型核心循环、极低尾延迟和高频二进制处理应先 profile，再考虑 NumPy/Numba/Cython、扩展模块、进程并行或将热点移到 C/C++/Rust/Java。

截至 2026-08，官方稳定文档为 Python 3.14 系列。3.14 将 free-threaded CPython 作为受支持但可选的构建，标准库提供 `concurrent.interpreters` 与 `InterpreterPoolExecutor`；官方 Windows/macOS 包也包含实验性 JIT。它们不是“升级后所有 Python 代码自动多核加速”：第三方 C 扩展可能未适配而重新启用 GIL，free-threaded 构建也有内存和单线程开销，JIT 仍不建议直接用于生产承诺。

官方参考：

- Python 3.14 新特性：https://docs.python.org/3.14/whatsnew/3.14.html
- free-threaded Python：https://docs.python.org/3.14/howto/free-threading-python.html
- 标准库：https://docs.python.org/3/library/

### 运行时、对象模型与并发

CPython 先编译源码为字节码，再由解释器执行；对象主要以引用计数管理，并用循环 GC 处理循环引用。变量名绑定对象而非保存值，`list`、`dict`、`set` 是可变对象，`tuple`、`str`、`int` 等常用对象不可变。函数默认参数在定义时求值，可变默认参数会在多次调用间共享，这是常见 bug。

```python
# 错误：所有调用共享同一个列表
def append_bad(value, items=[]):
    items.append(value)
    return items

# 正确：每次调用按需创建
def append_ok(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items
```

| 工作负载 | 首选工具 | 关键限制 |
| --- | --- | --- |
| I/O 密集并发 | `asyncio`、异步客户端、任务组 | `await` 之间可切换，阻塞 I/O/CPU 代码会卡住事件循环。 |
| CPU 密集并行 | `multiprocessing`、进程池、向量化/原生扩展 | 序列化、进程启动和数据复制有成本。 |
| 常规线程 | `threading`、`ThreadPoolExecutor` | 默认 CPython 的 GIL 不让 Python 字节码 CPU 并行；I/O 仍有效。 |
| 多核解释器隔离 | `InterpreterPoolExecutor`、多解释器 | 隔离和数据传递语义不同于线程，生态仍在适配。 |
| free-threaded CPython | 适配后的多线程 CPU 程序 | 显式加锁，不依赖 `dict`/`list` 的当前内部锁实现。 |

`asyncio` 解决的是协作式 I/O 并发，不是自动并行。`async def` 中调用同步数据库驱动、`requests`、文件大读取或 CPU 密集 JSON/压缩，会阻塞整个 event loop；应使用异步库，或通过 `asyncio.to_thread()`/进程池隔离。取消也要按资源边界设计：使用 `async with`、超时和幂等操作，不能只在任务顶层捕获 `Exception` 后吞掉 `CancelledError`。

### 类型、接口与错误处理

Python 是动态语言，但生产项目应将 type hints 当作可执行设计文档，使用 `pyright`、mypy 或 IDE 静态检查提前发现边界错误。类型提示不在运行时自动验证；对 HTTP、MQ、配置等外部输入仍要用显式校验或 Pydantic 等工具，并将领域对象与传输 DTO 分离。

```python
from collections.abc import Iterable

def total(values: Iterable[int]) -> int:
    return sum(values)

class DomainError(Exception):
    pass

try:
    amount = total([1, 2, 3])
except (TypeError, ValueError) as exc:
    raise DomainError("invalid amount") from exc
```

异常处理原则：只捕获能恢复的具体异常；保留异常链 `raise ... from exc`；日志记录上下文而非密码/token/完整个人数据；不要用裸 `except:` 吞掉 `KeyboardInterrupt`、`SystemExit` 或取消信号。资源使用 `with`/`async with` 管理，避免依赖 `__del__` 或进程退出完成关闭。

### 依赖、构建与可复现环境

旧笔记中“指定版本后两年也可能跑不起来”的现象真实存在，根因通常是解释器版本、平台 wheel、间接依赖、系统库、私有索引和构建后端没有一起被固定。`requirements.txt` 的 `pip freeze` 是环境快照，不一定是可维护的顶层依赖声明。

推荐将项目定义放入 `pyproject.toml`，明确 Python 支持范围、直接依赖、构建后端、lint/test/type-check 配置；再由 pip-tools、Poetry、uv 等工具生成带哈希或精确版本的 lock/requirements 产物。CI 要从干净虚拟环境安装并测试，而不是只在开发者已有的 Conda 环境中运行。

```text
pyproject.toml: 直接依赖与项目元数据
lock/requirements: 解析后的可复现版本集合
venv: 每个项目隔离解释器与 site-packages
CI: 干净环境安装、测试、类型检查、漏洞扫描
容器/部署: 固定基础镜像、系统库与运行用户
```

实践要点：每项目使用 `python -m venv .venv`；安装/执行优先 `python -m pip`、`python -m pytest`，避免 PATH 指向另一套 Python；库开发者避免把所有依赖锁死，应用开发者应锁定完整传递依赖；升级 Python 或主要依赖时跑完整测试与性能基线。

### Web、数据与安全

Web 服务区分 WSGI（同步）和 ASGI（异步）部署路径。FastAPI/Starlette 等 ASGI 应用需要 ASGI server；Django/Flask 的同步视图也不应因套了 `async` 就假定其所有依赖都非阻塞。生产 API 应有请求超时、连接池上限、结构化日志、健康检查、指标、限流、鉴权、数据库迁移和优雅关闭。

数据处理优先向量化和批处理：Pandas 的 Python 级 `apply` 常比列运算慢；大数据不应盲目一次 `read_csv` 全量读入内存。用采样、数据类型、分块、Parquet/Arrow、数据库下推或分布式计算降低内存与序列化成本。对不可信输入禁止 `pickle.loads`、不把 `eval`/`exec` 当解析器、不反序列化来源不明的 YAML；密钥放环境变量或密钥服务，不提交到仓库和日志。

### 学习与排障路线

1. 语言基础：数据模型、作用域、迭代器/生成器、上下文管理器、异常、包与导入。
2. 工程基础：`venv`、`pyproject.toml`、pytest、ruff/formatter、type hints、logging、调试和 profile。
3. 并发基础：线程/GIL、asyncio、进程池、取消、超时和资源池。
4. 方向专项：后端看 HTTP/ASGI/数据库；数据看 NumPy/Pandas/统计；自动化看 requests/浏览器自动化/系统接口；AI 看 PyTorch/推理与数据管线。

仓库中的 [CPython](cpython.md)、[venv](venv.md)、[PEP](pep.md)、[SQLAlchemy](sqlalchemy.md) 可作为下一步。排查线上“Python 慢”时先区分 CPU、I/O、锁、GC、数据库和外部服务，用 `py-spy`、`cProfile`、tracemalloc、指标和 trace 定位，禁止先靠盲目加线程或重写语言解决。
