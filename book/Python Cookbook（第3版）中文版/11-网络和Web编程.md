# 11 章 网络和 Web 编程（原书 pp.约 605–649）

## 本章地图
| 节 | 内容 | 结论 |
|---|---|---|
| 11.1 | HTTP 客户端 | `urllib.request`/第三方 `requests` |
| 11.2–11.3 | TCP/UDP 服务器 | `socket` |
| 11.4 | CIDR 生成 IP 集 | `ipaddress` |
| 11.5 | REST 接口 | `http.server`/`Flask` |
| 11.6–11.8 | XML-RPC、解释器间、远程方法 | 过时 RPC 方案 |
| 11.9–11.11 | 客户端认证、SSL、socket 传递 fd | `ssl`/`socket` |
| 11.12 | 事件驱动 IO | `selectors` |
| 11.13 | 发送/接收大数组 | 结构化协议 |

## 核心精讲
- 11.1 现代 HTTP 客户端优先 `requests`/`httpx`（🔧 第三方，比 `urllib` 友好）；`urllib.request` 仍标准库。
- 11.2 TCP 回显服务器：`socket.socket` + `bind`/`listen`/`accept` 循环。
- 11.4 `ipaddress.ip_network('192.168.0.0/24')` 生成地址集（3.3+ 内置，原书用 `IPy` 第三方）。
- 11.5 简单 REST 用 `http.server` 或 `Flask`/`FastAPI`。
- 11.12 `selectors` 事件驱动（3.4+ 替代旧 `select` 模块写法）。

```python
# 教学示意，不参与构建
import ipaddress, socket
net = ipaddress.ip_network("192.168.0.0/24")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8080)); s.listen()
```

## 版本演进
- **3.4 PEP 0315 / `selectors`**：事件驱动 IO 用 `selectors` 抽象（11.12 升级）。
- **3.7 `asyncio`**：HTTP/服务器多改用 `aiohttp`/`httpx` 异步（与第 12 章并发互补）。
- **3.9 `zoneinfo`** 等无关；`ssl` 默认上下文更严格（11.10 防降级）。
- **3.13 PEP 594**：`telnetlib` 等移除；部分旧协议示例需替换。
- 🔧 XML-RPC（11.6）/`SimpleXMLRPCServer` 已不推荐，现代用 JSON/REST/gRPC。

## 经典论文与原始文献
- `socket`/`ssl`/`selectors` 标准库；RFC 791/793（IP/TCP）。
- PEP 0315 `selectors` 模块（3.4）；`asyncio` 设计（PEP 3156，3.4）。
- 🔧 具体编号/年份以 https://peps.python.org/ 为准。

## 近年研究与工业界（2015–2026）
- `httpx` 支持 HTTP/2 + 异步；`FastAPI` 成主流 REST 框架。
- `gRPC`/`GraphQL` 取代 XML-RPC 场景。
- 服务网格/云原生让底层 `socket` 多被框架封装。

## 常见误区与本书需修正之处
| 误区 | 修正 |
|---|---|
| 用 `urllib` 写客户端 | 优先 `requests`/`httpx` |
| XML-RPC 做 RPC | 改用 REST/gRPC/GraphQL |
| 裸 `socket` 写服务器 | 现代用 `asyncio`/`FastAPI` |
| IP 段用第三方 `IPy` | 3.3+ 用内置 `ipaddress` |
| 自签 SSL 不校验 | `ssl` 默认验证，关验证仅测试 |

## 与其他章 / 其他书的联系
- 异步 IO 与 [12-并发.md](12-并发.md) 互补；事件驱动（11.12）与第 12 章 selectors 相关。
- REST/Web 与 [../Python极客项目编程/00-总览与阅读地图.md](../Python极客项目编程/00-总览与阅读地图.md) 项目实践呼应。
- JSON（[06-数据编码与处理.md](06-数据编码与处理.md)）是 Web 载荷基础。
