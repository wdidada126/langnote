# 24 · Exploring data

> 一句话定位：用 `numpy`/`pandas` 做探索性数据分析——从文件到洞察。
> 原书 pp. 英文 4e 第 24 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 24.1 | `numpy` | 数组/向量化 |
| 24.2 | `pandas` | DataFrame |
| 24.3 | 清洗 | 缺失/类型 |
| 24.4 | 聚合 | groupby |
| 24.5 | 可视化 | matplotlib |

## 核心精讲

```
# 教学示意，不参与构建
import pandas as pd
df = pd.read_csv('data.csv')
print(df.describe())
print(df.groupby('cat')['val'].mean())
```

- `numpy` 数组向量化运算远快于 list 循环。
- `pandas.DataFrame` 是表格分析核心：`read_csv`/`describe`/`groupby`。
- `matplotlib`/`seaborn` 可视化。

## 版本演进

- NumPy 2.0（2024）移除旧别名（`np.float` 等，NEP 50）。
- `polars` 提供更快 DataFrame 引擎。
- `pandas` 1.x/2.x 持续演进。

## 经典论文与原始文献

- NumPy / pandas 官方文档。
- Wes McKinney《Python for Data Analysis》；Jake VanderPlas《Python Data Science Handbook》。

## 近年研究与工业界开源实践（2015–2026）

- `polars` 多线程/惰性执行；`duckdb` SQL on DataFrame。
- `plotly` 交互可视化。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 用 list 循环算数值 | 用 `numpy` 向量化 |
| `np.float`/`np.int` | NumPy 2.0 已移除，用 `float`/`int` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 网络数据见[第22章 Data over the network](22-Data over the network.md)。
- 数据科学深讲见 [`Python for Data Analysis 3e`](#) 与 [`Python数据科学手册 2e`](#)。
