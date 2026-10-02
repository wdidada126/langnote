# 第 15 章 Python和Web（原书 pp.256-272）

> 一句话定位：本章覆盖「抓别人的页面」与「自己产生页面」两个方向。**前者今天照样成立（换工具即可），后者整节已被时代推翻**——CGI 与 `cgi`/`cgitb` 模块已在 Python 3.13 被移除。基线：原书 Python 3.5；本目录按 3.12+ 校验。
> 对应英文章名：Python and the Web

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 15.1.1 Tidy 和 XHTML 解析 | 先用 Tidy 把脏 HTML 整理成 XHTML，再用 XML 解析器读 | 🔧 这条路线今天已无必要：现代解析器（`html.parser`、`lxml`、Beautiful Soup）直接容错 |
| 15.1.2 Beautiful Soup | 容错解析 + 遍历/搜索/CSS 选择 | **仍是事实标准**，配合 `httpx` 使用 |
| 15.2.1–15.2.3 准备 Web 服务器 / 添加 `#!` 行 / 设置文件权限 | CGI 部署三件套 | 🔴 **CGI 已退出**：`cgi`/`cgitb` 模块在 Python 3.13 被移除（PEP 594） |
| 15.2.4–15.2.8 CGI 安全风险、简单脚本、`cgitb`、`cgi` 模块、简单表单 | `cgi.FieldStorage` 读表单 | 🔴 改用 WSGI（PEP 3333）/ ASGI 框架；安全风险改为 XSS/注入/CSRF 三件套 |
| 15.3 使用 Web 框架 | 框架把 URL 路由、模板、表单接管 | 2026 主流：**FastAPI**（ASGI）/ **Flask** / **Django** |
| 15.4.1 RSS | 解析聚合 feed | 仍在用（Atom 更常见），`xml.etree.ElementTree` 或 `feedparser` |
| 15.4.2 XML-RPC | `xmlrpc.client` / `xmlrpc.server` | 模块仍在标准库，但**基本淘汰** → JSON-RPC / gRPC |
| 15.4.3 SOAP | 复杂企业 Web 服务 | 衰落；只在遗留系统集成中遇到 |
| 15.5 小结 | 新函数速查 | —— |

## 核心精讲

> 教学示意，不参与构建：标注「需安装」的片段请先按给出的命令装依赖；其余只用标准库，可离线运行。

### 1. 屏幕抓取：`httpx` + Beautiful Soup（需安装）

```bash
pip install httpx beautifulsoup4
```

```python
import httpx
from bs4 import BeautifulSoup

with httpx.Client(timeout=10, follow_redirects=True,
                  headers={"User-Agent": "langnote-demo"}) as client:
    resp = client.get("https://books.toscrape.com/")
    resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
print("标题:", soup.title.string)
print("前三个链接:", [a.get("href") for a in soup.select("a")][:3])
print("正文前 80 字:", soup.get_text(strip=True)[:80])
```

三点纪律：**先查 `robots.txt` 与站点条款**、**设超时与限速**（不要并发猛打）、**标明 UA 与联系方式**。原书没提合规，这是 2026 年必须补的一条。

```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.parse("User-agent: *\nDisallow: /private/\n".splitlines())
print("可抓 /private/x 吗:", rp.can_fetch("*", "https://a.example/private/x"))
print("可抓 /public/x 吗:", rp.can_fetch("*", "https://a.example/public/x"))
```

### 2. 不装第三方也能抓：标准库 `HTMLParser`

```python
from html.parser import HTMLParser


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href"))


p = LinkCollector()
p.feed('<a href="https://a.example">A</a><a href="/rel">B</a>')
print("收集到:", p.links)
```

需要 CSS 选择器、容错修复与大规模抓取时，用 `bs4` + `lxml`（或 Scrapy 生态的 `parsel`）；`HTMLParser` 适合零依赖的小脚本。原书「先 Tidy 成 XHTML 再解析」的额外步骤，今天已不需要——**解析器本身就容错**。

### 3. 从 CGI 到 WSGI/ASGI

原书 15.2 的三步（`#!` 行 → `chmod` → 放进 `cgi-bin`）与其安全模型（每个请求 fork 一个进程）在 2026 年都不该再照做。取而代之的是**应用服务器 + 框架**：

| 代 | 形态 | 规范 |
| --- | --- | --- |
| CGI | 每请求起一个进程 | 无（HTTP 环境变量 + stdout） |
| WSGI | 一个可调用对象 `app(environ, start_response)` | **PEP 3333**（2010） |
| ASGI | `async def app(scope, receive, send)`，支持长连接 | ASGI 规范（社区） |

最小 WSGI 应用——**可以不启服务器就单测**：

```python
from wsgiref.util import setup_testing_defaults


def app(environ, start_response):
    setup_testing_defaults(environ)
    name = environ.get("QUERY_STRING") or "world"
    body = f"Hello, {name}!".encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8"),
                              ("Content-Length", str(len(body)))])
    return [body]


captured = {}
def fake_start_response(status, headers, exc_info=None):
    captured["status"], captured["headers"] = status, headers


print("响应体:", app({"QUERY_STRING": "langnote"}, fake_start_response))
print("状态与头:", captured["status"], captured["headers"])
```

生产部署：WSGI 用 Gunicorn/waitress，ASGI 用 Uvicorn/Hypercorn，前面挂 Nginx/Caddy。

### 4. FastAPI：今天的默认演示（需安装）

```bash
pip install "fastapi[standard]"      # 或 pip install fastapi uvicorn
uvicorn main:app --reload            # 运行
```

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.get("/hello")
def hello(name: str = "world") -> dict[str, str]:
    return {"message": f"Hello, {name}"}


@app.post("/items")
def create(item: Item) -> Item:
    return item                       # 请求体由 pydantic 校验，自动出 OpenAPI 文档
```

对比原书的「手写 CGI + `cgi.FieldStorage` + 手工拼 HTML」：框架接管了路由、校验、序列化、文档与错误处理；**模板自动转义**（Jinja2）也从根上缓解了第 26 章那种 XSS。

### 5. RSS 与聚合：依然有效

```python
import xml.etree.ElementTree as ET

rss = """<?xml version="1.0"?><rss version="2.0"><channel>
<title>示例频道</title>
<item><title>第一条</title><link>https://a.example/1</link></item>
<item><title>第二条</title><link>https://a.example/2</link></item>
</channel></rss>"""

for item in ET.fromstring(rss).iter("item"):
    print(item.findtext("title"), "->", item.findtext("link"))
```

RSS/Atom 仍是订阅与聚合的主流格式（播客更是强依赖）；实际项目用 `feedparser`（`pip install feedparser`）处理各种不规范的 feed。**永远不要用 `xml.etree` 解析不可信 XML 而不设防护**——实体展开类攻击（billion laughs）需限制或换 `defusedxml`。

### 6. XML-RPC 与 SOAP：现状

| 技术 | 模块 | 2026 状态 |
| --- | --- | --- |
| XML-RPC | `xmlrpc.client` / `xmlrpc.server`（**仍在标准库**，本机 3.13 验证） | 基本淘汰；新项目用 **JSON-RPC** 或 **gRPC**（`pip install grpcio`） |
| SOAP/WSDL | 无标准库支持 | 衰落；只在银行、电信、政务等遗留系统对接中遇到，可用 `zeep` |
| REST + JSON | `json` / `httpx` | 事实标准 |
| GraphQL | `strawberry` / `ariadne` | 特定场景（前端聚合查询） |

原书 15.4 把 XML-RPC/SOAP 当作「更高级的抓取」，今天这个位置属于 **OpenAPI 描述的 REST 接口**与 **gRPC**。

## 版本演进

| 版本 | 与本章相关的变化 |
| --- | --- |
| 3.5（原书基线） | `cgi`、`cgitb` 仍在标准库但已显老旧；`xmlrpc` 可用 |
| 3.7–3.9 | `cgi` 文档标注「不推荐新项目使用」；Web 生态全面转向 WSGI/ASGI 框架 |
| 3.10–3.11 | 🔧 `cgi` 进入弃用预警期；`asyncio` 生态成熟，ASGI 成为新项目默认 |
| 3.12 | 🔴 PEP 594 的第一批移除完成（`smtpd`、`asyncore`、`asynchat` 等） |
| 3.13 | 🔴 **PEP 594：`cgi` 与 `cgitb` 模块正式移除**——原书 15.2 全节代码无法运行（本机 3.13 实测 `ModuleNotFoundError`） |
| 3.14 | 🔧 继续清理；`urllib` 与 `http` 相关模块的行为微调以官方 What's New 为准 |
| 生态侧 | FastAPI（2018 起）成为新 API 的首选；Django 5 / Flask 3 提供 ASGI 支持；`httpx` 提供同步+异步统一 API |

## 经典论文与原始文献

> Python 生态以 **PEP 与官方文档**为权威口径，以下均为**规范文档，非同行评审论文**。

| 文献 | 标题 / 年份 | URL |
| --- | --- | --- |
| PEP 3333 | Python Web Server Gateway Interface v1.0.1（2010） | https://peps.python.org/pep-3333/ |
| PEP 594 | Removing Dead Batteries from the Standard Library（2018，Python 3.13） | https://peps.python.org/pep-0594/ |
| PEP 492 | Coroutines with async and await syntax（2015，Python 3.5）——ASGI 的语言基础 | https://peps.python.org/pep-0492/ |
| 官方文档 | `urllib.robotparser`（抓取合规） | https://docs.python.org/3/library/urllib.robotparser.html |
| 官方文档 | `xml.etree.ElementTree`（RSS/Atom 解析） | https://docs.python.org/3/library/xml.etree.elementtree.html |
| 官方文档 | `wsgiref` — WSGI Utilities and Reference Implementation | https://docs.python.org/3/library/wsgiref.html |
| 规范文档 | ASGI Specification（ASGI 官方文档，非 PEP） | https://asgi.readthedocs.io/ |
| 规范文档 | robots.txt / RFC 9309（Robots Exclusion Protocol，2022） | https://www.rfc-editor.org/rfc/rfc9309 |

## 近年研究与工业界开源实践（2015–2026）

- **FastAPI + pydantic**：把「类型注解即校验规则」变成主流，自动产出 OpenAPI 文档；它是本章 CGI 示例最直接的精神继承者（工具文档，非同行评审）。
- **ASGI 与长连接**：WebSocket / SSE / HTTP 流式响应在 WSGI 下无法实现，这解释了为什么新项目默认 ASGI 服务器（Uvicorn/Hypercorn）。
- **抓取与合规**：大型站点普遍提供官方 API；社区侧形成「先看 API、再看 robots.txt、最后才解析 HTML」的优先级共识，`Scrapy`/`parsel` 提供限速、重试与去重的基础设施。
- **结构化数据优先**：目标页面常内嵌 JSON-LD / `__NEXT_DATA__`，直接取结构化数据比解析 DOM 稳定得多，这是近年抓取实践的重要经验。
- **RPC 的迭代**：XML-RPC/SOAP → REST+JSON → gRPC（二进制、强 schema、流式）；JSON-RPC 在区块链与内部工具链里仍有稳定生态。
- 以上均为**工业界实践或工具文档，非同行评审论文**。

## 常见误区与本书需修正之处

| # | 原书说法 / 常见误区 | 问题 | 2026 正确写法 |
| --- | --- | --- | --- |
| 1 | 🔴 用 `cgi` / `cgitb` 写动态网页 | **Python 3.13 已移除**（PEP 594），原书 15.2 全节代码无法运行 | FastAPI / Flask / Django（WSGI PEP 3333 或 ASGI），由 Uvicorn/Gunicorn 托管 |
| 2 | 🔴 用 Tidy 把 HTML 转成 XHTML 再解析 | 多余且易碎 | `BeautifulSoup(html, "html.parser"|"lxml")` 直接容错解析 |
| 3 | 用 `urllib.request` 手写重试/超时/编码 | 样板多、易漏 | `httpx`（同步/异步同 API）；`requests` 亦可 |
| 4 | 抓取不看 robots.txt 与服务条款 | 法律与封禁风险 | `urllib.robotparser` 先判；限速、标 UA；优先用官方 API |
| 5 | 用 `xml.etree` 解析任意外部 XML | 实体展开/外部实体类攻击 | 限制解析或换 `defusedxml`；feed 用 `feedparser` |
| 6 | 把用户输入直接拼进 HTML 输出 | XSS（原书第 26 章公告板直接中招） | 模板引擎自动转义（Jinja2），或显式转义；输出编码永远跟着上下文 |
| 7 | 依赖 `xmlrpc` 做新系统 | 生态停滞、无流式、无强 schema | JSON-RPC 或 gRPC（`pip install grpcio`）；`xmlrpc` 仅维护旧系统 |
| 8 | SOAP 作为「更高级」的方向 | 已衰落，工具链沉重 | 遗留对接才用（`zeep`）；新系统用 REST + OpenAPI |
| 9 | 自己拼 HTML 字符串生成页面 | 转义与结构易错 | 模板（Jinja2）或前端渲染 + JSON API |
| 10 | 在请求处理中做阻塞 I/O | 吞吐被单请求拖垮 | `async def` + 异步客户端（`httpx.AsyncClient`）；ASGI 服务器 |
| 11 | 认为「WSGI/ASGI 只是框架的事」 | 不懂它就无法排查部署问题 | 掌握 `app(environ, start_response)` 契约（PEP 3333），手写一次最小 app |

## 与其他章 / 其他书的联系

- 本册：第 10 章 [10-开箱即用.md](10-开箱即用.md)（`urllib` 与模块生态）；第 11 章 [11-文件.md](11-文件.md)（抓取结果的落盘）；第 13 章 [13-数据库支持.md](13-数据库支持.md)（Web 后端的数据层）；第 14 章 [14-网络编程.md](14-网络编程.md)（`socket`/`asyncio` 是本章的网络底座）；第 22 章 [22-项目3：万能的XML.md](22-项目3：万能的XML.md)（`html.parser` 的项目级用法）；第 23 章 [23-项目4：新闻汇总.md](23-项目4：新闻汇总.md)（RSS 抓取与报告）；第 25/26 章 [25-项目6：使用CGI进行远程编辑.md](25-项目6：使用CGI进行远程编辑.md)、[26-项目7：自建公告板.md](26-项目7：自建公告板.md)（**CGI 项目必须改写为 FastAPI**）；第 27 章 [27-项目8：使用XML-RPC共享文件.md](27-项目8：使用XML-RPC共享文件.md)（XML-RPC → gRPC/JSON-RPC）。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)
