# 第 14 章 处理 CSV 和 JSON 文件（原书 pp.约351–约370）

> `csv`/`json` 模块做表格与数据交换。基线：原书 Python 3.8；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论 |
|---|---|---|
| 14.1 csv | `reader`/`DictReader`/`writer` | 现代用 pandas |
| 14.2 json | dump/load | 配置/API 交换 |
| 14.3 嵌套 | JSON↔dict 互转 | 类型映射 |

## 核心精讲

教学示意，不参与构建：

```python
import json, csv
from pathlib import Path

data = {"name": "ada", "tags": [1, 2]}
Path("c.json").write_text(json.dumps(data, ensure_ascii=False, indent=2),
                           encoding="utf-8")
back = json.loads(Path("c.json").read_text(encoding="utf-8"))

with Path("t.csv").open(encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        print(row)
```

## 版本演进

- 现代读 CSV 用 `pandas.read_csv`；`pathlib` 替代字符串路径。
- 🔧 UTF-8 模式默认化未定案，写文件显式 `encoding="utf-8"`。

## 经典论文与原始文献

- `csv`/`json` 文档：https://docs.python.org/3/library/ 规范文档。
- pandas 文档：https://pandas.pydata.org/docs/ 规范文档。

## 近年研究与工业界开源实践（2015–2026）

- 类型安全配置用 `pydantic`/`TypedDict` 包 JSON。
- TOML（3.11 `tomllib`）补 JSON 做人类可编辑配置。

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
|---|---|---|
| 手写 csv 解析 | 慢/错 | pandas |
| json 中文乱码 | 默认 ascii | ensure_ascii=False |

## 与其他章 / 其他书的联系

- 见 [../Python编程：从入门到实践（第3版）/09-文件和异常.md](../Python编程：从入门到实践（第3版）/09-文件和异常.md)、[16-下载数据.md](../Python编程：从入门到实践（第3版）/16-下载数据.md)。
