# 23 · Saving data

> 一句话定位：把程序结果持久化——JSON/SQLite/（谨慎）pickle。
> 原书 pp. 英文 4e 第 23 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 23.1 | JSON | 可移植 |
| 23.2 | SQLite | 关系型 |
| 23.3 | `pickle` | 仅信任源 |
| 23.4 | 文件锁 | 并发 |
| 23.5 | 选型 | 数据规模 |

## 核心精讲

```
# 教学示意，不参与构建
import sqlite3, json
with sqlite3.connect('app.db') as con:
    con.execute('CREATE TABLE IF NOT EXISTS t(id INTEGER PRIMARY KEY, v TEXT)')
    con.execute('INSERT INTO t(v) VALUES(?)', ('hi',))
json.dump({'k': 1}, open('c.json', 'w', encoding='utf-8'))
```

- JSON 跨语言可读，适合配置/交换。
- SQLite 内嵌关系库，零服务，适合结构化数据。
- `pickle` 可序列化任意对象但**只用于信任源**（反序列化执行代码，安全风险）。

## 版本演进

- `sqlite3` 长期稳定；`tomllib`（3.11）读配置。
- `filelock` 跨进程锁。

## 经典论文与原始文献

- Python `sqlite3`/`pickle`/`json` 文档。
- SQLite 官方文档。

## 近年研究与工业界开源实践（2015–2026）

- `orjson`/`msgspec` 快 JSON；`duckdb` 分析型内嵌库。
- `sqlmodel` 在 `sqlite`/`sqlalchemy` 上加类型。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 用 `pickle` 存外部数据 | 用 JSON/SQLite，pickle 仅信任源 |
| 大文件用 JSON 数组 | 用 SQLite/列式 |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 数据文件见[第21章 Processing data files](21-Processing data files.md)。
- 见 [`Python for Data Analysis 3e`](#) 与 [`Python数据科学手册 2e`](#)。
