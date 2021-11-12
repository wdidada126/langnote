# python


- Python编程 从入门到实践（第2版）
- 利用Python进行数据分析
- Python数据科学手册
- 流畅的Python
- Python编程快速上手
- Python源码剖析
- Python核心编程（第二版）





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

python 元编程 metaclass
python基本数据结构
dict
triple
list


python元编程详解
https://www.jianshu.com/p/644d309b504e


[python log to file](https://www.cnblogs.com/nancyzhu/p/8551506.html)

[urllib2](https://docs.python.org/2/library/urllib2.html)



[Python-100-Days](https://github.com/jackfrued/Python-100-Days/blob/master/Day91-100/100.Python面试题集.md)



python tag符号和空格不能混用，否则会报错


Anaconda3-5.3.1-Windows-x86_64
pycharm 设置

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

yum -y install python3

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