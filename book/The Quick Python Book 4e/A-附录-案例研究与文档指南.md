# A · 附录 — 案例研究与 Python 文档指南

> 一句话定位：把前 24 章串成一个小项目，并学会查官方文档。
> 原书 pp. 英文 4e 附录 A（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| A.1 | 案例研究 | 综合小项目 |
| A.2 | 官方文档 | docs.python.org |
| A.3 | `help`/`dir` | 交互查文档 |
| A.4 | 类型标注辅助 | 编辑器/CI |

## 核心精讲

```
# 教学示意，不参与构建
# 案例：批量整理下载目录 + 汇总 CSV
from pathlib import Path
import shutil, csv
src = Path.home() / 'Downloads'
rows = []
for f in src.iterdir():
    if f.is_file():
        shutil.move(f, src / 'sorted' / f.name)
        rows.append({'name': f.name, 'size': f.stat().st_size})
with open('summary.csv', 'w', encoding='utf-8', newline='') as fh:
    csv.DictWriter(fh, fieldnames=['name', 'size']).writerows(rows)
```

- 案例综合：路径(`pathlib`)、文件整理(`shutil`)、CSV(`csv`)、异常(第14章)。
- 查文档：`help(obj)`/`dir(obj)` 交互；`docs.python.org/3/` 权威。
- `pydoc` 命令行生成文档；类型标注让 IDE 自动补全。

## 版本演进

- `pdoc`/`mkdocstrings` 生成 API 文档。
- 4e 附录 A 即「guide to Python's documentation」。

## 经典论文与原始文献

- Python 官方文档：https://docs.python.org/3/
- `pydoc` 模块文档。

## 近年研究与工业界开源实践（2015–2026）

- `mkdocs` + `mkdocstrings` 写项目文档。
- AI 助手辅助查文档，但需核对官方。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 只搜博客不查官方 | 以 docs.python.org 为准 |
| 不读异常回溯 | 回溯指向根因 |
| 🔧 4e 案例以官方 notebook 为准 | 以实体书为准 |

## 与其他章 / 其他书的联系

- 全 24 章的综合应用。
- 工程化见 [`Serious Python`](#) 与 [`Robust Python`](#)。
