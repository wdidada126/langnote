# 12 · Using the filesystem

> 一句话定位：`pathlib` 与目录操作——以现代方式描述路径。
> 原书 pp. 英文 4e 第 12 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 12.1 | `pathlib` | 路径对象 |
| 12.2 | 遍历 | `glob`/`rglob` |
| 12.3 | 属性 | 存在/类型 |
| 12.4 | 创建 | `mkdir` |

## 核心精讲

```
# 教学示意，不参与构建
from pathlib import Path
p = Path.home() / 'data' / 'x.txt'
print(p.exists(), p.suffix, p.resolve())
for f in Path('.').rglob('*.py'):
    print(f)
p.parent.mkdir(parents=True, exist_ok=True)
```

- `pathlib.Path`（PEP 428）面向对象路径。
- `/` 拼接、`glob`/`rglob` 遍历、`read_text` 便捷读写。
- `resolve` 解析绝对路径，`expanduser` 展开 `~`。

## 版本演进

- `pathlib`（3.4）；`Path.walk`（3.12）递归。
- `os`/`shutil` 仍可用，但新代码优先 `pathlib`。

## 经典论文与原始文献

- PEP 428 — pathlib；Python `pathlib` 文档。
- Python `os`/`shutil` 文档。

## 近年研究与工业界开源实践（2015–2026）

- `pathlib` 成标准路径写法。
- `send2trash` 安全删除。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 字符串拼路径 | 用 `pathlib` |
| `~` 不展开 | 用 `Path.home()`/`expanduser` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 读写文件见[第13章 Reading and writing files](13-Reading and writing files.md)。
- 路径专篇见 [`Automate the Boring Stuff with Python 3e/concepts/文件路径与pathlib.md`](../Automate the Boring Stuff with Python 3e/concepts/文件路径与pathlib.md)。
