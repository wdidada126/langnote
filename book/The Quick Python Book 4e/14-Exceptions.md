# 14 · Exceptions

> 一句话定位：`try/except` 错误处理——用异常表达「出错了」而非返回码。
> 原书 pp. 英文 4e 第 14 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 14.1 | `try/except` | 捕获 |
| 14.2 | `else/finally` | 清理 |
| 14.3 | `raise` | 抛出 |
| 14.4 | 异常层次 | 基类 |
| 14.5 | 异常组 | PEP 654 |

## 核心精讲

```
# 教学示意，不参与构建
try:
    n = int(input())
except ValueError:
    print('不是数字')
else:
    print('ok', n)
finally:
    print('清理')
```

- 精确捕获具体异常，勿裸 `except:`（会吞 `KeyboardInterrupt`）。
- `else` 在无异常时执行；`finally` 总执行（清理资源）。
- `raise ... from` 链式异常保留根因。

## 版本演进

- `breakpoint()`（PEP 553，3.7）。
- `ExceptionGroup`/`except*`（PEP 654，3.11）一次传播多异常。

## 经典论文与原始文献

- PEP 553 / PEP 654；Python 内建异常层次文档。
- Python 教程「Errors and Exceptions」。

## 近年研究与工业界开源实践（2015–2026）

- `rich.traceback` 彩色回溯。
- `tenacity` 做重试装饰器。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 裸 `except:` | 捕获具体异常 |
| `assert` 当校验 | `-O` 下移除，用异常 |
| 🔧 4e 标 ExceptionGroup | 3.11+ 多错误处理 |

## 与其他章 / 其他书的联系

- 调试见 [`Automate the Boring Stuff with Python 3e/10-调试.md`](../Automate the Boring Stuff with Python 3e/10-调试.md)。
- 见 [`Effective Python（第2版）/00-总览与阅读地图.md`](../Effective Python（第2版）/00-总览与阅读地图.md) 异常条目。
