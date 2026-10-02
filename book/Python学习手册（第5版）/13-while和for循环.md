# 13 while和for循环（原书 pp. 英文 5e 第 13 章，中文版页次以实体书为准 🔧）

## 本章地图
| 节 | 内容 | 结论 |
| --- | --- | --- |
| while 循环 | 条件驱动 | 通用 |
| for 循环 | 迭代序列/可迭代 | 首选 |
| break/continue/pass | 控制流 | 配合 else |
| 循环惯用法 | 枚举/压缩/切片 | `enumerate`/`zip` |
| 推导式 | 见 14 章 | 更 Pythonic |

## 核心精讲
`for` 遍历可迭代对象（推荐）；`while` 用于条件循环。`for`/`while` 可带 `else`（正常结束即执行，遇 `break` 跳过）。

```
教学示意，不参与构建
for i, v in enumerate(["a", "b"]):     # (0,'a'),(1,'b')
    print(i, v)
for x, y in zip([1, 2], [3, 4]):       # (1,3),(2,4)
    print(x + y)
n = 0
while n < 3:
    n += 1
else:
    print("loop done without break")
```

- `enumerate`/`zip` 替代手写下标；`reversed`/`sorted` 生成器。
- 不要为遍历下标而 `for i in range(len(x))`，优先直接迭代元素。

## 版本演进
- 3.x `range` 返回惰性对象（2.x `xrange` 已并入 `range`）。
- 3.10 `zip` 支持 `strict=True` 检查长度一致（🔧 以官方为准）。

## 经典论文与原始文献
- 官方 *Tutorial*「Looping Techniques」（`enumerate`/`zip`/`items`）。
- 迭代协议见 [14-迭代和推导](14-迭代和推导.md)。

## 近年研究与工业界开源实践（2015–2026）
- `itertools` 提供 `chain`/`islice`/`groupby` 等惰性组合子；`more-itertools` 扩展常用模式。

## 常见误区与本书需修正之处
| 误区 | 修正 |
| --- | --- |
| 下标遍历 `range(len())` | 优先 `for item in seq` 或 `enumerate` |
| `for...else` 难懂 | 习惯后很实用；也可改用标志变量，可读性优先 |
| 在遍历中修改列表 | 应遍历副本或建新列表，避免跳过元素 |

## 与其他章 / 其他书的联系
- 迭代器/生成器见 [14-迭代和推导](14-迭代和推导.md)、[20-推导式和生成器](20-推导式和生成器.md)。
- 算法分析见 [../像计算机科学家一样思考Python（第2版）/21-算法分析.md](../像计算机科学家一样思考Python（第2版）/21-算法分析.md)。
