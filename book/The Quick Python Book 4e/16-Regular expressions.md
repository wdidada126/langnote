# 16 · Regular expressions

> 一句话定位：`re` 模块模式匹配——在文本中找结构。
> 原书 pp. 英文 4e 第 16 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 16.1 | `re` 基础 | search/match |
| 16.2 | 元字符 | `.`/`\d`/`\w` |
| 16.3 | 分组 | `()` |
| 16.4 | 量词 | `*`/`+`/`?` |
| 16.5 | `sub` | 替换 |

## 核心精讲

```
# 教学示意，不参与构建
import re
m = re.search(r'(\d{4})-(\d{2})', '2026-10')
print(m.groups())                 # ('2026', '10')
print(re.sub(r'\s+', ' ', 'a  b')) # 'a b'
```

- `re.search` 全串搜；`re.findall` 全部匹配。
- 原始串 `r'...'` 避免转义冲突。
- 分组 `()` 提取；`sub` 替换。

## 版本演进

- `re` 稳定；第三方 `regex` 支持递归/Unicode 属性。
- `re.VERBOSE` 提升可读性。

## 经典论文与原始文献

- Python `re` 文档；Jeffrey Friedl《Mastering Regular Expressions》。
- 正则官方 HOWTO。

## 近年研究与工业界开源实践（2015–2026）

- `regex` 库支持 `\p{Han}` 中文匹配。
- `pyparsing`/`lark` 复杂解析替代正则。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 漏原始串 | 用 `r'...'` |
| 贪心吞过多 | 非贪心 `?` |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 文本见[第06章 Strings](06-Strings.md)。
- 进阶见 [`Python Cookbook（第3版）中文版/00-总览与阅读地图.md`](../Python Cookbook（第3版）中文版/00-总览与阅读地图.md) 正则章。
