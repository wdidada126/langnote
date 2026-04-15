# sqlalchemy

https://github.com/sqlalchemy/sqlalchemy

# 1. 装依赖
sudo apt install python3-dev git build-essential
pip install wheel

# 2. 下载
git clone https://github.com/sqlalchemy/sqlalchemy
cd sqlalchemy

# 3. 编译 whl
pip wheel . -w dist

# 4. 安装
pip install dist/*.whl


我给你最准确、最直白的答案，一句话先讲透：

# 核心结论
`pip wheel . -w dist` 打包的是：源代码（`.py`），不会自动打包 `.pyc`！

# 详细说明（你一定关心）
## 1. 最终 `.whl` 里面有什么？
打开你生成的 `sqlalchemy-xxx.whl`，你会看到：
```
sqlalchemy/
  __init__.py
  engine.py
  ... 所有 .py 源文件
```
✅ 只有 .py 源码
❌ 没有 .pyc 编译文件

## 2. 那什么时候会有 .pyc？
只有运行时 Python 才会自动生成 .pyc
- 安装 whl 后第一次运行
- Python 自动把 `.py` 编译成 `.pyc` 放 `__pycache__`
- 不是打包时放进去的

## 3. 那 SQLAlchemy 为什么有 .so/.pyd 文件？
因为它有 C 语言加速扩展
- 编译时会生成：
  - Linux：`xxx.so`
  - Windows：`xxx.pyd`
- 这些是C扩展二进制，不是 Python 字节码 `.pyc`

# 你真正想问的我帮你总结
### 你运行：
```bash
pip wheel . -w dist
```
### 得到的 whl 内容：
1. 纯 Python 源码 `.py`
2. 编译好的 C 扩展二进制（.so/.pyd）
3. 没有 .pyc

# 如果你想强制打包 .pyc（几乎没人这么做）
需要用专门工具，比如：
- `pyinstaller`（打包成可执行）
- `cx_Freeze`
- 或手动编译 + 替换

但标准 Python 包、whl 都不会这么做！

# 最终超级记忆版
✅ pip wheel = 打包 .py 源码
✅ 安装时自动生成 .pyc
✅ C 扩展会编译成 .so
❌ 不会把 .pyc 打进 whl

---
需要我教你 怎么打开 whl 看里面到底有什么 吗？超级简单！


# 一句话终极答案
Python 3.3+ 不再强制需要 `__init__.py`！
但做库、发布包、规范工程、兼容旧版本 → 必须要有！

我给你分最清晰、最实用的版本

# 1. 什么时候 不需要 `__init__.py`
Python 3.3+ 引入了 命名空间包（Namespace Package）
只要你满足：
- 只是本地运行脚本
- 不发布成库
- 不用 `setup.py` / `pyproject.toml` 打包

那么完全可以没有，照样能 import：
```
my_project/
  main.py
  utils/
    a.py   可以直接 import utils.a
    b.py
```

# 2. 什么时候 必须要有 `__init__.py`
只要你是做库、发布包、工程化项目 → 必须加！

必须加的原因：
1. 声明这是一个 Python 包（Package）
2. 打包工具（pip、poetry、setuptools）识别它
3. 控制导出哪些模块（`__all__`）
4. 初始化代码
5. 兼容所有 Python 版本
6. IDE 识别、自动补全正常

没有它，打包 whl 时会丢文件！

# 3. 标准库、知名库全都有
- Flask
- SQLAlchemy
- requests
- aiohttp
- pandas
- numpy

全部都带 `__init__.py`
这是工业界标准。

# 4. 最简单的 `__init__.py` 长啥样？
空文件就行！
```python
# 空的 __init__.py 完全合法
```

或者加导出控制（推荐）：
```python
__all__ = ["DB", "User", "Post"]
```

# 5. 超级总结（必背）
- 本地脚本 → 可无
- 做库 / 发包 / 工程 → 必须有
- 空文件就够
- 没有会导致打包失败、IDE报错、导入异常

### 你现在的场景：SQLAlchemy 类库
必须要有 __init__.py！
没有它，你的包无法正常编译、无法正常导入。

需要我告诉你 如何自动给所有子目录生成 __init__.py 吗？

__init__.py python库必须有这个文件吗？
