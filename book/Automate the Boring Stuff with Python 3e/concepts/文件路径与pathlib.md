# 概念专篇 · 文件路径与 pathlib

> 跨章参考：支撑[第08章 读写文件](../08-读写文件.md)与[第09章 组织文件](../09-组织文件.md)的所有路径操作。

## 为什么用 pathlib

- 字符串拼路径易错（`'dir' + '\\' + 'file'`），跨平台不兼容。
- `pathlib.Path` 面向对象，自动用正确分隔符，方法丰富。

## 常用操作

```
# 教学示意，不参与构建
from pathlib import Path
p = Path('data') / 'sub' / 'file.txt'     # 用 / 拼接
print(p.name, p.stem, p.suffix)           # file.txt, file, .txt
print(p.parent, p.resolve())              # 父目录、绝对路径
# 读写
text = p.read_text(encoding='utf-8')
p.write_text(text, encoding='utf-8')
# 遍历
for f in Path('.').glob('*.py'):          # 当前层
    print(f)
for f in Path('.').rglob('*.py'):         # 递归
    print(f)
# 存在/类型
p.exists(); p.is_file(); p.is_dir()
```

## 版本演进

- `pathlib`（PEP 428，3.4）；3.6 起 `Path.read_text/write_text/read_bytes/write_bytes` 可用。
- 3.12 增强：`Path.walk()` 递归遍历（替代 `os.walk`）；`Path.relative_to` 支持 `walk_up`。
- `os`/`shutil` 仍可用，但新代码优先 `pathlib`。

## 编码与陷阱

- 读写文本**始终**指定 `encoding='utf-8'`，否则 Windows 默认 GBK 会乱码。
- `Path('~')` 不展开家目录，用 `Path.home()` 或 `Path('~').expanduser()`。
- 符号链接：`Path.readlink()`（3.9）、`resolve()` 跟随链接。

## 跨章跨书联系

- 主章：[第08章 读写文件](../08-读写文件.md)、[第09章 组织文件](../09-组织文件.md)。
- 标准库总览见 [`Python in a Nutshell 4e`](#) 或 [`Python Distilled`](#)。
- 跨平台脚本细节见 [`Serious Python`](#) 与 [`Robust Python`](#)。
