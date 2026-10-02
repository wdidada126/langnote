# 21 · Processing data files

> 一句话定位：CSV/JSON/XML/配置——解析与生成结构化数据文件。
> 原书 pp. 英文 4e 第 21 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 21.1 | CSV | `csv` 模块 |
| 21.2 | JSON | `json` |
| 21.3 | XML | `xml.etree` |
| 21.4 | TOML | `tomllib` |
| 21.5 | 配置 | `configparser` |

## 核心精讲

```
# 教学示意，不参与构建
import csv, json
with open('d.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        print(row['name'])
data = json.loads('{"a": 1}')
print(json.dumps(data, ensure_ascii=False))
```

- `csv.DictReader` 按表头；写用 `newline=''` 防空行。
- `json` 保 `ensure_ascii=False` 留中文。
- `tomllib`（3.11）只读 TOML；XML 用 `xml.etree.ElementTree`。

## 版本演进

- `tomllib`（PEP 680，3.11）入标准库。
- `orjson`/`msgspec` 更快 JSON。

## 经典论文与原始文献

- PEP 680；JSON RFC 8259；Python `csv`/`json`/`tomllib` 文档。
- XML 标准。

## 近年研究与工业界开源实践（2015–2026）

- `pandas.read_csv` 主导表格；`polars` 更快。
- `pydantic` 把 JSON 校验为模型。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 写 CSV 空行 | `newline=''` |
| JSON 中文乱码 | `ensure_ascii=False` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 持久化见[第23章 Saving data](23-Saving data.md)。
- 流水线专篇 [concepts/数据文件处理流水线.md](concepts/数据文件处理流水线.md)。
- 数据见 [`Python for Data Analysis 3e`](#) 与 [`Python数据科学手册 2e`](#)。
