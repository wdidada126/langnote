# 19 · Using Python libraries

> 一句话定位：标准库「电池」与常用第三方库——站在巨人肩上。
> 原书 pp. 英文 4e 第 19 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 19.1 | 标准库亮点 | collections/itertools |
| 19.2 | 日期时间 | datetime/zoneinfo |
| 19.3 | 数据格式 | json/tomllib |
| 19.4 | 第三方 | numpy/pandas/requests |
| 19.5 | 选型 | 何时造轮子 |

## 核心精讲

```
# 教学示意，不参与构建
from collections import Counter, defaultdict
c = Counter('abracadabra')
print(c.most_common(2))            # [('a', 5), ('b', 2)]
from datetime import datetime
from zoneinfo import ZoneInfo
print(datetime.now(ZoneInfo('UTC')))
```

- 标准库覆盖广：`collections`/`itertools`/`functools`/`pathlib`/`datetime`/`json`。
- `zoneinfo`（3.9）标准时区；`tomllib`（3.11）读 TOML。
- 第三方：`numpy`/`pandas`/`requests`/`rich`。

## 版本演进

- `zoneinfo`（PEP 615）；`tomllib`（PEP 680）。
- `itertools.batched`（3.12）分批迭代。

## 经典论文与原始文献

- Python 标准库文档：https://docs.python.org/3/library/
- PyPI：https://pypi.org/

## 近年研究与工业界开源实践（2015–2026）

- `rich`/`typer`/`polars`/`pendulum` 等现代库。
- `uv` 管理依赖。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 手写 Counter/defaultdict | 用 `collections` |
| 用 `pytz` | 3.9+ 用 `zoneinfo` |
| 🔧 4e 提 AI 工具库 | 以官方为准 |

## 与其他章 / 其他书的联系

- 包见[第18章 Packages](18-Packages.md)。
- 数据见[第21章 Processing data files](21-Processing data files.md)与 [`Python for Data Analysis 3e`](#)。
