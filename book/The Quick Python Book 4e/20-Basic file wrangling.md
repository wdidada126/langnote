# 20 · Basic file wrangling

> 一句话定位：复制、移动、重命名、批量整理文件——`shutil`/`os`/`pathlib`。
> 原书 pp. 英文 4e 第 20 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 20.1 | `shutil` | 复制/移动 |
| 20.2 | `os` | 重命名/删 |
| 20.3 | 遍历 | `rglob` |
| 20.4 | 安全删除 | `send2trash` |

## 核心精讲

```
# 教学示意，不参与构建
import shutil
from pathlib import Path
src = Path('a.txt'); dst = Path('bak/a.txt')
shutil.copy(src, dst)
for f in Path('.').rglob('*.log'):
    f.rename(f.with_suffix('.old'))
```

- `shutil.copy/move/copytree` 复制移动。
- `Path.replace` 跨平台移动；先收集再操作避免遍历混乱。
- 安全删除用 `send2trash` 进回收站。

## 版本演进

- `pathlib.Path.replace`（3.x）；`shutil.copytree(dir_exist_ok=)`（3.8）。
- `send2trash` 第三方安全删除。

## 经典论文与原始文献

- Python `shutil`/`os`/`pathlib` 文档。
- RPA 概念。

## 近年研究与工业界开源实践（2015–2026）

- `watchdog` 监听目录变化触发整理。
- `rich`/`tqdm` 批量进度条。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| `os.rename` 目标存在报错 | 用 `Path.replace`/`shutil.move` |
| 硬删重要文件 | 用 `send2trash` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 路径见[第12章 Using the filesystem](12-Using the filesystem.md)。
- 流水线专篇 [concepts/数据文件处理流水线.md](concepts/数据文件处理流水线.md)。
- 见 [`Automate the Boring Stuff with Python 3e/09-组织文件.md`](../Automate the Boring Stuff with Python 3e/09-组织文件.md)。
