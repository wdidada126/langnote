# 22 · Data over the network

> 一句话定位：HTTP 取数据、调 API——`requests`/`httpx` 与现代网络客户端。
> 原书 pp. 英文 4e 第 22 章（具体页次以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 22.1 | `requests` | GET/POST |
| 22.2 | JSON API | 解析响应 |
| 22.3 | 异步 | `httpx`/`aiohttp` |
| 22.4 | 合规 | 频率/认证 |
| 22.5 | 错误 | 状态码/超时 |

## 核心精讲

```
# 教学示意，不参与构建
import requests
r = requests.get('https://api.github.com', timeout=10)
r.raise_for_status()
print(r.status_code, r.json().get('current_user_url'))
```

- `requests` 同步友好；`raise_for_status()` 检查状态。
- `httpx` 提供异步客户端；`aiohttp` 老牌异步。
- 设 `timeout`、处理 `401/403/429`；遵守 `robots.txt` 与限频。

## 版本演进

- `httpx` 支持 HTTP/2 与异步，渐替 `requests`（同步仍可用）。
- `aiohttp` 异步请求框架。

## 经典论文与原始文献

- Requests 文档；HTTPX 文档。
- RFC 7231（HTTP 语义）。

## 近年研究与工业界开源实践（2015–2026）

- `httpx`/`aiohttp` 异步抓取。
- `tenacity` 重试；API key 走环境变量。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 不检查状态码 | `raise_for_status()` |
| 同步阻塞大量请求 | 用 `httpx` 异步 |
| 🔧 4e 标 3.13 | 以官方为准 |

## 与其他章 / 其他书的联系

- 异常见[第14章 Exceptions](14-Exceptions.md)。
- 抓取见 [`Automate the Boring Stuff with Python 3e/11-网页抓取.md`](../Automate the Boring Stuff with Python 3e/11-网页抓取.md)。
- 并发见 [`Python Concurrency with asyncio`](#) 与 [`高性能Python（第2版）/00-总览与阅读地图.md`](../高性能Python（第2版）/00-总览与阅读地图.md)。
