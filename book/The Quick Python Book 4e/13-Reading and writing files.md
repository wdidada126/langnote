# 13 · Reading and writing files

> 一句话定位：`open`/`with`/`pathlib` 读写文本与二进制——IO 基本功。
> 原书 pp. 英文 4e 第 13 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 13.1 | `open` | 模式 |
| 13.2 | `with` | 自动关闭 |
| 13.3 | 读写方法 | read/write |
| 13.4 | `pathlib` | 便捷方法 |
| 13.5 | 编码 | UTF-8 |

## 核心精讲

```
# 教学示意，不参与构建
from pathlib import Path
p = Path('a.txt')
p.write_text('hello', encoding='utf-8')
print(p.read_text(encoding='utf-8'))
with p.open('a', encoding='utf-8') as f:
    f.write('\nmore')
```

- 文本模式显式 `encoding='utf-8'` 避免平台默认（Windows 易乱码）。
- `with` 离开块自动 `close`。
- `pathlib` 的 `read_text/write_text` 最简洁。

## 版本演进

- `pathlib`（PEP 428）；`Path.read_text` 等（3.6+）。
- 旧书 `shelve` 持久化 → 现代用 `json`/`sqlite3`。

## 经典论文与原始文献

- PEP 428；Python `io`/`pathlib` 文档。
- Python 教程「Reading and Writing Files」。

## 近年研究与工业界开源实践（2015–2026）

- `orjson` 高速 JSON；`tomllib`（3.11）读 TOML。
- `filelock` 跨进程锁。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 不指定编码 | 始终 `utf-8` |
| `shelve` 持久化 | 用 `json`/`sqlite3` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 路径见[第12章](12-Using the filesystem.md)；异常见[第14章 Exceptions](14-Exceptions.md)。
- 见 [`Automate the Boring Stuff with Python 3e/08-读写文件.md`](../Automate the Boring Stuff with Python 3e/08-读写文件.md)。
