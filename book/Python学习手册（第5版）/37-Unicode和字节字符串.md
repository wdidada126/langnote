# 37 Unicode和字节字符串（原书 pp. 英文 5e 第 37 章，中文版页次以实体书为准 🔧）

## 本章地图
| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.x 字符串模型 | `str`=Unicode、`bytes`=字节 | 显式编解码 |
| 字符串基础 | 见 7 章 | 已覆盖 |
| 编解码 | `encode`/`decode` | UTF-8 默认 |
| `bytearray` | 可变字节 | 少量场景 |
| 文本/二进制文件 | `t`/`b` 模式 | 见 9 章 |

## 核心精讲
3.x 彻底统一为：文本用 `str`（Unicode 码点），二进制用 `bytes`；二者必须显式编解码，不能混运算。

```
教学示意，不参与构建
s = "你好"
b = s.encode("utf-8")          # bytes
assert b == b"\xe4\xbd\xa0\xe5\xa5\xbd"
back = b.decode("utf-8")        # str
ba = bytearray(b)               # 可变字节数组
ba[0] = 0x48
```

- 2.x 的 `str`/`unicode` 双模型在 3.x 消失；原书关于 2.x 的篇幅在 3.x 已无意义。
- 文件：`open(..., "r", encoding="utf-8")` 读文本；`"rb"` 读字节（见 [09-元组文件及其他](09-元组文件及其他.md)）。

## 版本演进
- 3.0 字符串模型革命（PEP 3131/PEP 358 等系列）；`str` 即 Unicode。
- 3.9 `str.removeprefix`/`removesuffix`（PEP 616）。
- 3.x `unicodedata` 做归一化（`NFC`/`NFKC`）。

## 经典论文与原始文献
- PEP 3131 *Supporting Non-ASCII Identifiers*（3.0，允许 Unicode 标识符）。
- 官方 `codecs`、`unicodedata`、`str.encode/decode` 文档。

## 近年研究与工业界开源实践（2015–2026）
- Web/JSON 默认 UTF-8；`orjson`/标准 `json` 透明处理。
- `ftfy` 修复「乱码」（mojibake）文本。

## 常见误区与本书需修正之处
| 误区 | 修正 |
| --- | --- |
| 2.x `str`/`unicode` 双模型 | 3.x 只有 `str`(Unicode) 与 `bytes`，务必显式编解码 |
| 不指定文件编码 | 3.x 默认依赖 locale，常非 UTF-8；显式 `encoding="utf-8"` |
| `bytes` 与 `str` 拼接 | `TypeError`；先 `decode`/`encode` 统一类型 |

## 与其他章 / 其他书的联系
- 字符串基础见 [07-字符串基础](07-字符串基础.md)；文件见 [09-元组文件及其他](09-元组文件及其他.md)。
- 文本处理对照 [../Python Cookbook（第3版）中文版/02-字符串和文本.md](../Python Cookbook（第3版）中文版/02-字符串和文本.md)。
