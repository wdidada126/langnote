# 第 17 章 使用 API（原书 pp.373–404）

> 调用 Web API 取数据并可视化（Hacker News + Plotly）。基线：原书 Python 3.11；本目录按 3.12+ 校验。

## 本章地图

| 小节 | 内容 | 结论 |
|---|---|---|
| 17.1 请求 API | `requests.get` | 返回 JSON |
| 17.2 处理响应 | `.json()` 解析 | 检查状态码 |
| 17.3 可视化 | Plotly 画交互图 | 比静态图更友好 |
| 17.4 监视 API | 控制速率 | 遵守 `rate limit` |

## 核心精讲

教学示意，不参与构建（需 `pip install requests plotly`）：

```python
import requests

url = "https://hacker-news.firebaseio.com/v0/item/44331713.json"
resp = requests.get(url, timeout=10)
resp.raise_for_status()            # 非 2xx 抛异常
data = resp.json()
print(data.get("title"), data.get("score"))

# 批量取前 N 条
ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json",
                   timeout=10).json()[:10]
articles = [requests.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json",
                         timeout=10).json() for i in ids]
```

## 版本演进

- 🟢 今天客户端优先 `httpx`（支持 HTTP/2、异步）：`import httpx; r = httpx.get(url)`。
- `requests` 仍可用但进入维护模式。
- 异步并发取多个请求用 `httpx.AsyncClient` + `asyncio.gather`（见 [../流畅的python2/21-异步编程.md](../流畅的python2/21-异步编程.md)）。

## 经典论文与原始文献

- PEP 3333 — WSGI（2010），https://peps.python.org/pep-3333/ 规范文档，非同行评审论文。
- requests 文档：https://docs.python-requests.org/ 规范文档。
- httpx 文档：https://www.python-httpx.org/ 规范文档。

## 近年研究与工业界开源实践（2015–2026）

- 调用第三方 API 注意：鉴权（token 放环境变量，勿硬编码）、重试（`tenacity`）、限流、缓存。
- 合规：遵守对方 `robots.txt` 与 ToS；别高频爬。

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
|---|---|---|
| 用 `requests` | 维护模式 | 新项目用 `httpx` |
| 不处理异常 | 网络错即崩 | `raise_for_status` + try |
| 无超时 | 可能挂起 | 加 `timeout=` |
| token 硬编码 | 泄露风险 | 放环境变量/密钥管理 |

## 与其他章 / 其他书的联系

- JSON 见 [09-文件和异常.md](09-文件和异常.md)；异步见 [../流畅的python2/21-异步编程.md](../流畅的python2/21-异步编程.md)。
- Web 框架见 [18-Web应用：Django学习笔记.md](18-Web应用：Django学习笔记.md)。
