# 第 12 章 处理 Excel 电子表格（原书 pp.约296–约320）

> `openpyxl` 读写 `.xlsx`。基线：原书 Python 3.8；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论 |
|---|---|---|
| 12.1 打开/读取 | `load_workbook` | 按单元格取 |
| 12.2 写 | 建表/赋值/保存 | `wb.save` |
| 12.3 公式/样式 | 单元格格式 | 轻量处理 |

## 核心精讲

教学示意，不参与构建（需 `pip install openpyxl`）：

```python
from openpyxl import Workbook, load_workbook

wb = load_workbook("data.xlsx")
ws = wb.active
print(ws["A1"].value)
ws["B2"] = 42
wb.save("data.xlsx")

# 新建
wb = Workbook()
ws = wb.active
ws.append([1, 2, 3])
wb.save("new.xlsx")
```

## 版本演进

- `openpyxl` 持续维护；旧 `xlrd` 只读 `.xls` 且不读 `.xlsx`。
- 大数据用 `pandas.read_excel` 一次性成 DataFrame。

## 经典论文与原始文献

- openpyxl 文档：https://openpyxl.readthedocs.io/ 规范文档。
- pandas 文档：https://pandas.pydata.org/docs/ 规范文档。

## 近年研究与工业界开源实践（2015–2026）

- 批量表格处理用 `pandas` + `openpyxl` 引擎；样式/图表用 `openpyxl` 原生。

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
|---|---|---|
| xlrd 读 xlsx | 已不支持 | openpyxl |
| 手循环写格 | 慢 | pandas/append |

## 与其他章 / 其他书的联系

- CSV/JSON 见 [14-CSV与JSON.md](14-CSV与JSON.md)；数据分析见 [../PythonForDataAnalysis3e.md](../PythonForDataAnalysis3e.md)。
