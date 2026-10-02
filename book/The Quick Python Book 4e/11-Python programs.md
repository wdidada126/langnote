# 11 · Python programs

> 一句话定位：从片段到可运行程序——`__main__`、`argparse`、组织多文件。
> 原书 pp. 英文 4e 第 11 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 11.1 | `__main__` | 入口守卫 |
| 11.2 | 命令行参数 | `argparse` |
| 11.3 | 多文件组织 | 包/模块 |
| 11.4 | `if __name__` | 可导入可运行 |

## 核心精讲

```
# 教学示意，不参与构建
import argparse
def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('name')
    print('hi', p.parse_args().name)
if __name__ == '__main__':
    main()
```

- `if __name__ == '__main__':` 让模块既可导入又可运行。
- `argparse` 解析命令行参数（现代可用 `typer`）。
- 程序由多个模块/包组合。

## 版本演进

- `argparse` 标准库；`typer`/`click` 用标注生成 CLI。
- `tomllib`（PEP 680，3.11）读配置。

## 经典论文与原始文献

- Python `argparse` 文档；`__main__` 文档。
- PEP 680 — tomllib。

## 近年研究与工业界开源实践（2015–2026）

- `typer` 成 CLI 首选；`rich` 美化输出。
- `pyproject.toml` 定义入口点。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 顶层执行无入口守卫 | 加 `if __name__` |
| 手搓参数解析 | 用 `argparse`/`typer` |
| 🔧 4e 提 notebook 组织 | 以官方为准 |

## 与其他章 / 其他书的联系

- 模块见[第10章](10-Modules and scoping rules.md)；包见[第18章 Packages](18-Packages.md)。
- 工程化见 [`Serious Python`](#) 与 [`Robust Python`](#)。
