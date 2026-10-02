# 14 · CSV 与 JSON

> 一句话定位：表格数据用 `csv`、结构化数据用 `json`——程序间交换的通用格式。
> 原书 pp. 英文 3e 第 14 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 14.1 | 读 CSV | `csv.reader` |
| 14.2 | `DictReader` | 按列名 |
| 14.3 | 写 CSV | `csv.writer` |
| 14.4 | JSON 读写 | `json.dump/load` |
| 14.5 | `tomllib` | 只读 TOML |

## 核心精讲

```
# 教学示意，不参与构建
import csv, json
with open('data.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        print(row['name'], row['price'])
data = {'users': [{'name': 'Alice'}]}
with open('out.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

- `csv` 用 `DictReader` 按表头访问；写用 `DictWriter`，注意 `newline=''` 防空行。
- `json.dump/load` 处理基本类型与嵌套；`ensure_ascii=False` 保留中文。
- `tomllib`（3.11，PEP 680）只读 TOML；写用 `tomli_w`/`pyproject.toml`。

## 版本演进

- `tomllib`（PEP 680，3.11）进入标准库，配置优先 TOML 替代 `configparser`/JSON。
- `json` 长期稳定；`orjson`/`msgspec` 提供更快编解码。
- `csv` 需显式 `encoding='utf-8'` 与 `newline=''`（Windows）。

## 经典论文与原始文献

- PEP 680 — tomllib；JSON 规范 RFC 8259。
- Python `csv`/`json`/`tomllib` 文档。

## 近年研究与工业界开源实践（2015–2026）

- `pandas.read_csv/to_csv` 是数据分析主力；`polars` 更快。
- `pydantic` 把 JSON 校验为强类型模型。
- `msgspec` 同时支持 JSON/MessagePack，性能极高。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 写 CSV 出现空行 | 打开用 `newline=''` |
| JSON 中文变 `\uXXXX` | `ensure_ascii=False` |
| 用 JSON 存配置 | 现代用 TOML（`pyproject.toml`） |
| 🔧 本书未提 `tomllib` | 3.11+ 配置优先 `tomllib` |

## 与其他章 / 其他书的联系

- 字典是 JSON 内存模型，见[第05章 字典与结构化数据](05-字典与结构化数据.md)。
- 数据框见 [`Python for Data Analysis 3e`](#) 与 [`Python数据科学手册 2e`](#)。
