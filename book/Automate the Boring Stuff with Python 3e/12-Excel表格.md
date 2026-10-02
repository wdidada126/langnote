# 12 · Excel 表格

> 一句话定位：`openpyxl` 读写 `.xlsx` 单元格、公式、图表——办公自动化最高频场景。
> 原书 pp. 英文 3e 第 12 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 12.1 | 载入与工作簿 | `load_workbook` |
| 12.2 | 单元格读写 | `ws['A1']` |
| 12.3 | 行列遍历 | `ws.iter_rows` |
| 12.4 | 公式 | 写入 `=SUM(...)` |
| 12.5 | 样式与图表 | 字体/填充 |

## 核心精讲

```
# 教学示意，不参与构建
from openpyxl import load_workbook, Workbook
wb = load_workbook('data.xlsx')
ws = wb.active
print(ws['A1'].value)
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
ws['B2'] = '=SUM(A2:A10)'
wb.save('out.xlsx')
```

- `openpyxl` 处理 `.xlsx`（Office Open XML）；旧 `.xls` 用 `xlrd`（已停止支持 xlsx）。
- 单元格坐标 `'A1'` 或 `ws.cell(row=1, column=1)`。
- 公式以字符串写入，Excel 打开时计算；`data_only` 读缓存值。
- 样式：`Font`/`PatternFill`/`Alignment`；图表用 `openpyxl.chart`。

## 版本演进

- `openpyxl` 是当前标准；`xlrd` 自 2.0 仅支持 `.xls`，`xlwt` 停止维护。
- `pandas` 的 `read_excel/to_excel` 底层用 `openpyxl`/`xlsxwriter`，批量处理更方便。
- `xlsxwriter` 在写大文件/复杂图表上更快。

## 经典论文与原始文献

- openpyxl 文档：https://openpyxl.readthedocs.io/
- Office Open XML 标准（ECMA-376）。

## 近年研究与工业界开源实践（2015–2026）

- `pandas` + `openpyxl` 是数据分析标配；`polars` 提供更快引擎。
- `pyxll`/`xlwings` 可驱动本机 Excel 做双向自动化。
- `calamine`（rust）极速读 Excel。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 用 `xlrd` 读 `.xlsx` | `xlrd>=2.0` 不支持；用 `openpyxl` |
| 公式读不到计算值 | `data_only=True` 读缓存，需 Excel 先打开过 |
| 大表用逐格循环 | 用 `pandas` 向量化 |
| 🔧 本书未提 `pandas` 读写 Excel | 批量处理优先 `pandas` |

## 与其他章 / 其他书的联系

- 数据框见 [`Python for Data Analysis 3e`](#) 与 [`Python数据科学手册 2e`](#)。
- CSV 见[第14章 CSV与JSON](14-CSV与JSON.md)。
