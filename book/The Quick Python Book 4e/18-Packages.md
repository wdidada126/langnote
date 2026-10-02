# 18 · Packages

> 一句话定位：把模块组织成包、安装第三方库——从脚本到可分发项目。
> 原书 pp. 英文 4e 第 18 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 18.1 | 包结构 | `__init__.py` |
| 18.2 | 相对导入 | `.`/`..` |
| 18.3 | 安装三方 | `pip`/`uv` |
| 18.4 | `pyproject.toml` | 现代配置 |
| 18.5 | 发布 | 打包 |

## 核心精讲

```
# 教学示意，不参与构建
# mypkg/__init__.py
# mypkg/core.py
from .core import run
# 安装
# python -m pip install requests
# 或 uv add requests
```

- 包是含 `__init__.py` 的目录（3.3+ 命名空间包可无该文件）。
- 相对导入 `.`/`..` 在包内使用。
- `pip install` 装三方；现代用 `uv`/`poetry`。

## 版本演进

- `pyproject.toml`（PEP 517/518/621）取代 `setup.py`。
- `uv`（Astral）极速安装/管理。
- 命名空间包（PEP 420，3.3）。

## 经典论文与原始文献

- PEP 517/518/621 — pyproject；PEP 420 — 命名空间包。
- Python 打包教程：https://packaging.python.org/

## 近年研究与工业界开源实践（2015–2026）

- `uv`/`pdm`/`poetry` 统一构建与依赖。
- PyPI 仍是分发主渠道；可信发布（OIDC）。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| `setup.py` 手写 | 用 `pyproject.toml` |
| `sudo pip install` | 虚拟环境/`uv` |
| 🔧 4e 提 `uv` | 现代优先 `uv` |

## 与其他章 / 其他书的联系

- 模块见[第10章 Modules and scoping rules](10-Modules and scoping rules.md)。
- 库使用见[第19章 Using Python libraries](19-Using Python libraries.md)。
- 工程化见 [`Serious Python`](#) 与 [`Robust Python`](#)。
