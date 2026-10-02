# 第 4 章 Unicode文本和字节序列（原书 pp.88–119）

> 一句话定位本章：把「字符」和「字节」彻底分开，建立一套永远不出乱码的处理习惯（显式 encoding、规范化、NFC 比较、正确的排序）。
> 基线：原书 Python 3.10；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| 4.1 本章新增内容（p.89） | 第 2 版改动 | 补 Unicode 新版本的表述；`casefold` 的比重提高 |
| 4.2 字符问题（p.89） | 字符 vs 码位 vs 字素簇 | `len(s)` 数的是**码位**，不是你眼睛看到的字 |
| 4.3 字节概要（p.90） | `bytes` / `bytearray` / `memoryview` | `b[0]` 给 int，`b[:1]` 给长度 1 的 bytes |
| 4.4 基本的编码解码器（p.92） | `encode` / `decode`、`errors=` | 出海不做异常处理就是埋地雷 |
| 4.5 处理编码和解码问题（p.93） | Encode/Decode 错误、BOM、嗅探 | 三类错误各有各自的正确处理策略 |
| 4.5.1 处理 UnicodeEncodeError（p.94） | `errors=` 四种常用处理器 | `xmlcharrefreplace` 用于 HTML，`ignore` 基本是错误的答案 |
| 4.5.2 处理 UnicodeDecodeError（p.95） | `replace` / 跳过坏字节 | 解码失败是数据问题，要先记录再降级 |
| 4.5.3 模块加载时的 SyntaxError（p.95） | 源文件编码声明 | Python 3 源文件默认 UTF-8；此坑基本只存在于遗留代码 |
| 4.5.4 如何找出字节序列的编码（p.96） | 编码嗅探 | 嗅探是**概率性**的：只能做最后一招，且要在 UI 层允许人工纠正 |
| 4.5.5 BOM：有用的鬼符（p.97） | `utf-8-sig` | UTF-8 不需要 BOM；读到带 BOM 的文件用 `utf-8-sig` |
| 4.6 处理文本文件（p.98） | `open(encoding=...)`、换行、UTF-8 模式 | **永远显式写 `encoding=`**，这是本章最重要的一条纪律 |
| 4.7 为了正确比较而规范化 Unicode 字符串（p.105） | NFC/NFD/NFKC/NFKD | 比较前先 `unicodedata.normalize('NFC', s)` |
| 4.7.1–4.7.3 大小写同一化、实用函数、去掉变音符（p.107–111） | `casefold`、剃标记 | 同一化用 `casefold`（会把 ß 折叠为 ss），不是 `lower` |
| 4.8 Unicode文本排序（p.111） | `locale.strxfrm` / PyICU | `sorted()` 只按码位排，人类可读排序必须靠 locale 或 ICU |
| 4.9 Unicode数据库（p.113） | `unicodedata` 模块 | name / lookup / numeric / category / combining 是处理文本的瑞士军刀 |
| 4.10 支持 str 和 bytes 的双模式 API（p.117） | re、os 的双模式 | str 模式 ⇒ Unicode 语义；bytes 模式 ⇒ 字节语义，二者不能混 |
| 4.11 本章小结 / 4.12 延伸阅读（p.119） | 纪律清单 | 「三明治」模型：入 bytes → 立刻 decode → 一路 str → 出口 encode |

## 核心精讲

### 4.2–4.3 字符、码位、字节

```python
# 教学示意，不参与构建
s1 = 'café'                # U+00E9（单一码位）
s2 = 'cafe\u0301'          # e + U+0301 组合重音符
print(len(s1), len(s2))    # 4 5 —— len 数的是码位
print(s1 == s2)            # False —— 看起来相同，字节不同
import unicodedata as ud
print(ud.normalize('NFC', s2) == s1)     # True：NFC 之后再比才是真正的等价
print(list(map(hex, map(ord, s2))))

b = b'caf\xc3\xa9'
print(b, len(b), b[0], b[:1])            # bytes 索引给 int，切片给 bytes
print('café'.encode('utf-8'), 'café'.encode('utf-16'))
print('café'.encode('ascii', errors='xmlcharrefreplace'))
```

必须区分三层概念：

- **码位**（code point）：Unicode 编号，`ord()` 的返回值，Python `str` 的元素。
- **字素簇**（grapheme cluster）：人眼看到的「一个字」，可能由多个码位组成（emoji 家族、`é` 的组合形式更极端）。
- **字节**：编码后的物理表示，同一个 `str` 在不同编码器下字节完全不同。

### 4.4–4.5 编解码：错误处理的四个层次

```python
# 教学示意，不参与构建
raw = ' café'.encode('utf-16')
print(repr(raw.decode('utf-16')))                       # 正确：用对了编码器
print(repr(raw.decode('utf-8', errors='replace')))      # 错：U+FFFD 替换坏字节
print(repr(raw.decode('utf-8', errors='ignore')))       # 错上加错：静默丢数据
print(repr(raw.decode('utf-8', errors='backslashreplace')))   # 调试友好：保留原字节痕迹

print(repr(' café'.encode('ascii', errors='xmlcharrefreplace')))   # HTML/XML 场景
for enc in ('utf-8', 'utf-16', 'utf-8-sig'):
    data = ' café'.encode(enc)
    print(enc, data[:6])
```

四条守则（比原书更严格）：

1. **程序边界立刻解码**：`open(..., encoding=...)`、`json.loads(bytes)` 都要显式给编码。
2. `errors='ignore'` 在生产代码里视为缺陷——它把数据损坏变成静默行为。
3. 不知道编码时的顺序是：① 优先协议声明（`Content-Type`、`<?xml encoding=...>`）② 问来源 ③ 才轮到嗅探。
4. UTF-8 文件都不要写 BOM；读别人的文件若带 BOM，用 `utf-8-sig`。

### 4.5.4 编码嗅探：概率工具，不是答案

```python
# 教学示意，不参与构建 —— 需 charset-normalizer（pip install charset-normalizer）；本机实测 3.4.1
from charset_normalizer import from_bytes, detect

sample = '中文 Newton'.encode('gb18030')       # 故意用 GB18030 编码
best = from_bytes(sample).best()
print(best.encoding if best else None, repr(best.output() if best else ''))
print(detect(sample))
print(from_bytes('中文 Newton'.encode('utf-8')).best().encoding)
```

本机实测结果值得放进笔记：**gb18030 编码的文本被判定为 Big5，置信度 1.0**——嗅探器完全可以「自信地猜错」。
所以嗅探输出只能用于「给人看的默认建议」，任何自动化流水线都必须允许用户覆盖。

### 4.6 处理文本文件：显式 encoding 与 UTF-8 模式

```python
# 教学示意，不参与构建
import locale
import sys
import tempfile
from pathlib import Path

print(sys.getdefaultencoding(), sys.getfilesystemencoding(), sys.flags.utf8_mode)
print(locale.getpreferredencoding(False))

tmp = Path(tempfile.gettempdir()) / 'fluent_py4_demo.txt'
tmp.write_text('第一行\n第二行\n', encoding='utf-8')      # ✅ 显式指定的写
print(repr(tmp.read_text(encoding='utf-8')))              # ✅ 显式指定的读
print(repr(tmp.read_bytes()))                             # 边界图景：字节永远是字节
tmp.unlink()
```

「默认编码」的现状（务必核对自己的运行环境）：

| 场景 | 决定因素 | 我们的建议 |
| --- | --- | --- |
| `str.encode()` 默认 | UTF-8（不必依赖） | 显式写出来：`s.encode('utf-8')` |
| `open()` 缺 `encoding=` | 依赖 locale；开启 UTF-8 模式时为 UTF-8 | 显式写出 `encoding=`（或用 `-X warn_default_encoding` 把遗漏变成告警 🔧） |
| 源文件读取 | Python 3 默认 UTF-8 | 老项目中的编码声明行按遗留语法理解即可 |
| 文件名 | 文件系统编码 + surrogateescape | 一律 `os.fsdecode` / `os.fsencode` 转换 |

其中 **UTF-8 模式**来自 PEP 540（3.7）：用 `PYTHONUTF8=1` 或 `-X utf8` 开启，`sys.flags.utf8_mode` 可以查看。
本机实测 `sys.flags.utf8_mode == 1`，说明这台机器已经全局开启。

### 4.7 规范化、大小写同一化、剃标记

```python
# 教学示意，不参与构建
import unicodedata as ud

def nfc_equal(s1, s2):
    return ud.normalize('NFC', s1) == ud.normalize('NFC', s2)

def fold_equal(s1, s2):
    return ud.normalize('NFC', s1).casefold() == ud.normalize('NFC', s2).casefold()

print(nfc_equal('café', 'cafe\u0301'))            # True
print(fold_equal('Straße', 'strasse'))            # True —— casefold 才是「同一化」
print('Straße'.lower(), 'Straße'.casefold())

def shave_marks(txt):
    return ''.join(c for c in ud.normalize('NFD', txt) if not ud.combining(c))

print(shave_marks('café τυρκικά'))                 # 去掉变音符：做搜索索引用
```

规范化的四种形态：`NFC`（合成，存储/交换的推荐形态）、`NFD`（分解，做字符处理时的过渡形态）、
`NFKC`/`NFKD`（「兼容」形态，会把全角字符、上标、`ﬁ` 连字等拆成普通字符，会丢语义，慎用于标识符比较）。

### 4.8–4.9 排序与 Unicode 数据库

```python
# 教学示意，不参与构建
import locale
import unicodedata as ud

fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
print(sorted(fruits))                       # 码位序：'cajá'排在'atemoia'之后……不直觉
try:
    locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
except locale.Error:
    print('（本机没有该 locale，改用自己的系统 locale）')
    locale.setlocale(locale.LC_COLLATE, '')
print(sorted(fruits, key=locale.strxfrm))

print(ud.name('€'), ud.numeric('½'), ud.lookup('ROCKET'))
print(ud.category('①'), ud.combining('\u0301'))
```

`locale.strxfrm` 依赖系统 locale，**进程全局**且不线程安全；生产环境的正确选择通常是 PyICU（ICU 的 Python 绑定），
它提供真正的 CLDR 排序规则与断词。🔧 具体绑定包的安装与 API 以各自官方发布说明为准。

### 4.10 双模式 API

```python
# 教学示意，不参与构建
import os, re

print(re.findall(rb'\w+', 'hello wörld'.encode('utf-8')))   # bytes 模式：\w 等同 [a-zA-Z0-9_]
print(re.findall(r'\w+', 'hello wörld'))                    # str 模式：Unicode 词字符生效
print(os.fsdecode(os.fsencode('路径')), os.fsencode('路径')[:3])
```

规则：**一个函数只在「一种模式」里工作**。要么全程 `str`（文本语义，Unicode 类、规范化），
要么全程 `bytes`（协议/二进制语义），中间的 `.encode()` / `.decode()` 只在**边界**出现。

## 版本演进

| 主题 | 原书基线 3.10 | 3.11 | 3.12 | 3.13 / 3.14 |
| --- | --- | --- | --- | --- |
| 字符串内部表示 | PEP 393（3.3）的灵活字符串表示：Latin-1/UCS-2/UCS-4 三档 | 不变 | 不变 | 不变；仍是「越窄越省内存」的实现细节 |
| UTF-8 模式 | `-X utf8` / `PYTHONUTF8=1`（PEP 540，3.7） | 稳定 | 稳定 | 稳定 |
| 🔧 默认编码走向 | 原书暗示 UTF-8 会越来越主输出 | — | — | **「UTF-8 模式将成为默认值」目前不是定案**，属社区提案/讨论层面，**以官方 What's New 与 CPython 文档为准**，不要写进代码假设 |
| f-string | 旧词法 | — | 🔴 PEP 701 语法自由化 | 稳定 |
| 模板 | 只有 `%` / `str.format` / f-string / `string.Template` | — | — | 🔴 PEP 750 t-string（3.14）：`t'Hello {name}'` 返回 `Template` 对象，可先做转义再渲染 |
| 死电池清理 | — | — | — | PEP 594（3.13）移除了部分旧模块；与文本处理相关的周边 API 需按 What's New 复核 🔧 |
| 新出新: 多解释器 | — | — | PEP 684 per-interpreter GIL | PEP 734（3.14）多解释器进标准库；对本章无直接影响 |

> t-string 的语法示意（**需 Python 3.14，本机 3.13 无法运行**，仅示意）：
>
> ```text
> template = t'<h1>{title}</h1>'     # 返回 Template，不立刻拼成 str
> html = escape_angles(template)     # 可先把插值项做转义，再交给渲染器
> ```

## 经典论文与原始文献

> 均为**规范文档，非同行评审论文**，无 DOI；年份为 PEP 创建年份。清单外一律标 🔧「以官方文档为准」。

| 编号 | 标题 | 年份 | 链接 | 与本章的关系 |
| --- | --- | --- | --- | --- |
| PEP 393 | Flexible String Representation | 2011 | https://peps.python.org/pep-0393/ | `str` 用 1/2/4 字节档位存储，解释了 `sys.getsizeof('a')` 不如预期的现象 |
| PEP 540 | Add a new UTF-8 Mode | 2016 | https://peps.python.org/pep-0540/ | 4.6 节 UTF-8 模式 / `PYTHONUTF8` / `-X utf8` |
| PEP 750 | Template Strings | 2024 | https://peps.python.org/pep-0750/ | 3.14 t-string：插值的惰性模板，HTML/SQL 注入防护的新工具 |
| PEP 701 | Syntactic Formalization of f-strings | 2023 | https://peps.python.org/pep-0701/ | 3.12 起 f-string 里可含复杂表达式、嵌套同型引号 |
| PEP 684 | A Per-Interpreter GIL | 2022 | https://peps.python.org/pep-0684/ | 多解释器路线，与 locale 全局状态（4.8 排序）的冲突背景 |
| PEP 594 | Removing dead batteries from the standard library | 2018 | https://peps.python.org/pep-0594/ | 3.13 起分批移除旧标准库模块 |
| 🔧 Unicode Standard / UAX 文本 | Unicode 15/16 标准与 UAX #15（规范化形式） | — | https://www.unicode.org/versions/ | NFC/NFD/NFKC/NFKD 的**权威定义**；Python 版本对应的 Unicode 版本以官方 docs 的 `unicodedata.unidata_version` 为准 |

## 近年研究与工业界开源实践（2015–2026）

| 实践 | 时间 | 内容 | 与本章的联系 | 性质 |
| --- | --- | --- | --- | --- |
| `charset-normalizer` 取代 `chardet` | 2020 起 | 纯 Python/PyPy 友好、MIT 许可，速度更快 | 4.5.4 编码嗅探的现役默认选择；本机实测 3.4.1 | 开源项目文档 🔧 |
| `ftfy`（fix text for you） | 2015 起 | 修 mojibake（乱码还原）链 | 接在本章「闻到乱码」之后使用的修复工具 | 项目文档 🔧 |
| 第三方 `regex` 模块 | 2016 起 | 支持 `\X` 字素簇、`\p{...}` Unicode 属性 | `re` 处理不了「一个 emoji 是多个码位」的问题 | 项目文档 🔧 |
| PyICU / CLDR 排序 | 长期 | ICU 绑定，locale 无关的可重复排序 | 4.8 节生产环境的答案 | 项目文档 🔧 |
| 面向 work-in-progress 的 UTF-8 普及 | 2020 起 | 现代 Web/数据栈几乎全是 UTF-8 | 使「边界立刻 decode」纪律变得更容易执行 | 行业趋势 🔧 |

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 年的正确写法 |
| --- | --- | --- |
| 4.2 隐含「一个字符一言一个码位」 | 组合字符与 emoji 会占多个码位 | 需要按「用户感知字符」处理时用 `regex` 的 `\X` 或 `grapheme` 库；存储/比较仍用 NFC 归一化 |
| 4.4/4.6 示例代码有时省略 `encoding=` | 示例可跑，生产出事故 | 永不省略 `encoding=`；CI 里加 `-X warn_default_encoding`（🔧 该选项的具体行为以官方文档为准）查漏 |
| 4.5.4 推荐 `chardet` | 现役生态已换默认 | 首选 `charset-normalizer`；两者都只做「建议」而非确定性判断（实测 gb18030 被判成 Big5） |
| 4.6 顺口提到「UTF-8 模式将来会默认开启」 | 🔧 这是**未定案**的社区讨论，不是既定路线 | 明确：只能写「以官方 What's New / CPython 文档为准」。代码里不要假设 `-X utf8` 已开 |
| 4.7.1 用 `lower()` 做大小写比较 | 对德语 ß、土耳其语 İ 等不等于大小写折叠 | 一律 `casefold()`；再做 NFC 归一化 |
| 4.8 给 locale 排序为主 | `setlocale` 是进程全局、非线程安全 | 生产用 PyICU；单线程脚本可以用 `locale.strxfrm` |
| 4.5.5 让人记住 BOM 的处理 | 未强调「不要产出 BOM」 | UTF-8 一律不写 BOM；只在读他人文件时用 `utf-8-sig` |
| 4.7.3 shave_marks 的激进用法 | 把 Æ/Ø 等「真字符」也误伤 | 剃标记只用于搜索索引；展示与身份比较一律保留原字符 |
| 🔧 全书对 emoji/ZWJ 序列 | Python 3 时代的 `unicodedata` 版本在持续更新 | 具体 Unicode 版本（`unicodedata.unidata_version`）和新增字符支持以官方 docs 为准 |
| 4.10 双模式混用 | 混写会在 str/bytes 边界抛 TypeError | 明确三明治模型：入口 decode → 全程 str → 出口 encode |

## 与其他章 / 其他书的联系

- **对象模型**：Python 3 的 `str` 是不可变序列，`bytes` 是扁平序列——分类见 [第 2 章 丰富的序列](02-丰富的序列.md)；两者的对象不可变性见 [第 6 章 对象引用、可变性和垃圾回收](06-对象引用、可变性和垃圾回收.md)。
- **文本 I/O 的另一半**：文件的打开方式与上下文管理、写入刷新见 [第 18 章 with、match和else块](18-with、match和else块.md) 的上下文管理器小节。
- **编码与协议**：网络打交道时的 bytes↔str 边界，见 [第 21 章 异步编程](21-异步编程.md)；服务端框架通常已帮你做了 decode。
- **数据表述**：把文本行解析成有结构的记录，交给 [第 5 章 数据类构建器](05-数据类构建器.md)。
- **跨书**：[《Python基础教程（第3版）》03-使用字符串](../Python基础教程_第3版_9787115474889/03-使用字符串.md) 是本章的前置知识；
  [11-文件](../Python基础教程_第3版_9787115474889/11-文件.md) 讲文件读写的分工与本书互补。
- **回到总览**：[00-总览与阅读地图.md](00-总览与阅读地图.md)。
