# 02 · Getting started

> 一句话定位：装好 Python、选对版本、跑通第一个交互式与脚本环境。
> 原书 pp. 英文 4e 第 2 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 2.1 | 选哪个 Python | 用 3.12+/3.13 |
| 2.2 | 安装 | 官方/包管理器 |
| 2.3 | 虚拟环境 | `venv` |
| 2.4 | REPL 与 notebook | 交互体验 |
| 2.5 | 编辑器 | 现代 IDE |

## 核心精讲

```
# 教学示意，不参与构建
python -m venv .venv
# Windows 激活：.venv\Scripts\activate
# macOS/Linux 激活：source .venv/bin/activate
python --version
```

- 始终用 Python 3（2 已 EOL）；4e 基于 3.13。
- 虚拟环境隔离依赖：`python -m venv .venv` 后激活。
- REPL 即时试验；notebook（Jupyter/Colab）做交互教学。

## 版本演进

- `venv` 自 3.3 标准库内置（替代 `virtualenv` 基本场景）。
- 启动器 `py`（Windows）选择版本：`py -3.13`。
- `uv`（Astral）成为极速包/环境管理器，渐替 `pip`/`venv`。

## 经典论文与原始文献

- Python 安装指南：https://docs.python.org/3/using/
- venv 文档：https://docs.python.org/3/library/venv.html

## 近年研究与工业界开源实践（2015–2026）

- `uv`/`pdm`/`poetry` 统一依赖与虚拟环境。
- `pyproject.toml`（PEP 518/621）取代 `setup.py`/`requirements.txt` 杂糅。
- `conda`/`mamba` 在科学计算仍流行。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 系统 Python 直接装包 | 用虚拟环境，避免污染系统 |
| 用 `sudo pip` | 危险，用 venv/用户安装 |
| 混用多个全局 Python | 用 `py -3.x` 或 `uv` 明确 |
| 🔧 4e 提 `uv` | 现代起步优先 `uv` |

## 与其他章 / 其他书的联系

- 包管理见[第18章 Packages](18-Packages.md)与[第19章 Using Python libraries](19-Using Python libraries.md)。
- 工程化见 [`Serious Python`](#) 与 [`Robust Python`](#)。
