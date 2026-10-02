# 01 · About Python

> 一句话定位：为什么选 Python——语言哲学、优势与改进方向，建立「该不该用」的判断。
> 原书 pp. 英文 4e 第 1 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 1.1 | 为何用 Python | 易用/表达力强/可读 |
| 1.2 | Python 擅长什么 | 脚本/数据/生态 |
| 1.3 | 改进方向 | 速度/类型/移动 |
| 1.4 | 小结 | 选型参考 |

## 核心精讲

```
# 教学示意，不参与构建
# 可读性即生产力：同一意图的多种写法偏清晰者
def greet(name: str) -> str:
    return f'Hello, {name}'
```

- Python 设计哲学（import this）：可读性、简洁、明确优于隐式。
- 「电池已包含」：标准库覆盖文件/网络/压缩/日期等常见需求。
- 跨平台、免费、生态丰富（PyPI 50 万+ 包）。

## 版本演进

- 4e 覆盖 Python 3.13；速度持续提升（Faster CPython 3.11+）。
- free-threading（PEP 703）实验性进入 3.13t/3.14t。
- 类型标注从可选变主流（PEP 484 系列）。

## 经典论文与原始文献

- Python 之禅（PEP 20）；Python 设计哲学文档。
- Python 官方「About Python」：https://www.python.org/about/

## 近年研究与工业界开源实践（2015–2026）

- CPython 专项提速（3.11 起）让纯 Python 接近 PyPy 早期水平。
- AI 编码助手（Copilot/Cursor）改变入门方式，但理解语义仍关键。
- 类型系统（pyright/mypy）成大型项目标配。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 「Python 慢所以不用」 | 多数脚本/IO 场景瓶颈不在 CPU；热点用 C 扩展/Numba |
| 认为无类型即弱 | 渐进类型 + 静态检查可达强类型体验 |
| 🔧 4e 新增 AI 工具章节 | 以官方 notebook 为准 |

## 与其他章 / 其他书的联系

- 标准库全景见[第19章 Using Python libraries](19-Using Python libraries.md)。
- 类型实践见 [`Effective Python（第2版）/00-总览与阅读地图.md`](../Effective Python（第2版）/00-总览与阅读地图.md)。
