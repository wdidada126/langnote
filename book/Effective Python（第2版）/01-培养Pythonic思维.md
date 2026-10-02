# 第 1 章 培养 Pythonic 思维（原书 pp.约 1–36）

> 条目 1–10。本章确定「什么是 Pythonic」的基线：版本意识、风格、bytes/str、f-string、解包、enumerate/zip、海象运算符。

## 本章地图

| 条 | 标题 | 结论 |
|---|---|---|
| 1 | 查询自己使用的 Python 版本 | 先 `python --version` / `sys.version_info`，再决定能用哪些语法 |
| 2 | 遵循 PEP 8 风格指南 | 一致性优先；用 linter（flake8/ruff）而非记规则 |
| 3 | 了解 bytes 与 str 的区别 | 文本用 str（Unicode），二进制用 bytes；显式 encode/decode |
| 4 | 用 f-string 取代 C 风格格式串与 str.format | 可读性最佳，3.12+ 支持 `=` 自文档、`{x:.2f}` 调试 |
| 5 | 用辅助函数取代复杂表达式 | 一行塞太多逻辑 → 抽成函数，便于测试与命名 |
| 6 | 把数据结构直接拆分到多个变量里 | 多重赋值/`*` 解包优于下标访问 |
| 7 | 尽量用 enumerate 取代 range | 同时需要下标与元素时 `for i, v in enumerate(...)` |
| 8 | 用 zip 同时遍历两个迭代器 | 并行迭代用 zip；3.10+ `zip(..., strict=True)` 防长度不一 |
| 9 | 不要在 for/while 后写 else 块 | `for...else` 语义反直觉，几乎总该避免 |
| 10 | 用赋值表达式减少重复代码 | `:=`（海象，3.8）在条件/推导中复用子表达式 |

## 核心精讲

```python
# 教学示意，不参与构建
# 条目 3：bytes 与 str 显式转换
def to_str(text):
    if isinstance(text, bytes):
        value = text.decode("utf-8")          # bytes -> str
    else:
        value = text                          # 已是 str
    return value

# 条目 4：f-string（3.12+ 支持 = 自文档）
count = 3
print(f"{count=}")                            # count=3
print(f"{count*10=}")                         # count*10=30

# 条目 6：多重赋值 / 解包
snack_calories = {"chips": 140, "popcorn": 80}
key, value = next(iter(snack_calories.items()))
first, *middle, last = [1, 2, 3, 4, 5]        # first=1, middle=[2,3,4], last=5

# 条目 10：海象运算符
fresh_fruit = {"apple": 10, "banana": 8}
if (count := fresh_fruit.get("apple", 0)) >= 4:
    make_cider(count)
```

## 版本演进

- 3.6：f-string 引入（PEP 498）；3.8 海象 `:=`（PEP 572）；3.10 `zip(strict=)`（PEP 618）。
- 3.12：f-string 语法放宽（可任意嵌套、可复用引号，PEP 701）；错误追迹改进（PEP 657）。
- 3.14：f-string 内部实现进一步稳定（🔧 以 3.14 文档为准）。

## 经典论文与原始文献

- PEP 8 — Style Guide for Python Code（条目 2 的权威来源）。
- PEP 498 — Literal String Interpolation（f-string，条目 4）。
- PEP 572 — Assignment Expressions `:=`（条目 10）。
- PEP 618 — Add Optional Length-Checking to zip（条目 8）。
- PEP 701 — Syntactic Formalization of F-Strings（3.12，条目 4 增强）。
- 官方文档 `docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals`。

## 近年研究与工业界开源实践（2015–2026）

- Ruff（2022–）已成事实标准 linter/formatter，取代 flake8+black 组合，极快（Rust 实现）。
- `python --version` 之外，依赖解析用 `importlib.metadata.version("pkg")`。
- 2024 年起 3e 已把本章拆成「Pythonic Thinking / Strings and Slicing / Loops and Iterators」三章（条目 1–9 重排），但 2e 的 10 条仍是稳固基线。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 以为 `for...else` 的 else 在循环「正常结束」时执行 | 实际只在「未被 break」时执行；语义反直觉，条目 9 建议直接避免 |
| 把 bytes 当 str 拼进文本 | 必须显式 decode；网络/文件读到的多是 bytes |
| 用 `%` 或 `.format` 拼长串 | 3.12+ f-string 能力最强，统一用 f-string（🔧 极老环境 3.5 以下才需回退） |
| 海象 `:=` 滥用 | 仅当同一子表达式需复用两次才值得，否则降低可读性 |

## 与其他章 / 其他书的联系

- 解包（条目 6）在 [02-列表与字典.md](02-列表与字典.md) 的 `*` 解包拾残继续出现。
- bytes/str（条目 3）与 [08-稳定与性能.md](08-稳定与性能.md) 的 `memoryview`/`bytearray` 互补。
- 风格与 lint 见 [10-协作开发.md](10-协作开发.md) 的虚拟环境与静态分析。
- 进阶主线：[../流畅的python2/00-总览与阅读地图.md](../流畅的python2/00-总览与阅读地图.md)。
