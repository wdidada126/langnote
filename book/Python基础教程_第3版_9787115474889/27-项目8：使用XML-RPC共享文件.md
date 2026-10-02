# 第 27 章 项目8：使用XML-RPC共享文件（原书 pp.401-416）

> 一句话定位本章：把一台机器上的目录通过 **XML-RPC** 暴露成「可被别人点名下载」的节点，并写一个命令行客户端去取——这是全书唯一一次实现**分布式（P2P）**结构的项目。
> 基线：原书 Python 3.5；本目录按 3.12+ 校验。
> 对应英文章名：Project 8: File Sharing with XML-RPC

## 本章地图

| 小节 | 内容 | 结论 |
| --- | --- | --- |
| 27.1 问题描述 | 每个节点既做服务器（发布自己的目录）又做客户端（取别人的文件） | 对称的 P2P 结构：同一份代码两种角色 |
| 27.2 有用的工具 | `xmlrpc.server`、`xmlrpc.client`、`cmd`、`os.path` | 标准库即可完成，但 XML-RPC 在 2026 年已边缘化 |
| 27.3 准备工作 | 约定 URL 格式（`http://host:port/RPC2`）、共享目录、密钥 | 「共享目录的根」是唯一的信任边界 |
| 27.4 初次实现 | 实现简单节点（`hello` / `list` / `fetch`），并尝试使用 | RPC 的第一课：**方法名即公共 API** |
| 27.5 再次实现 | 客户端界面（`cmd.Cmd`）、引发异常、验证文件名、再次尝试 | 三件补强：**可用性、错误语义、路径安全** |
| 27.6 进一步探索 | 加密、鉴权、断点续传、节点发现 | 再往前就是 BitTorrent / IPFS 一类真正的 P2P |

## 核心精讲

> 以下代码均为**教学示意，不参与构建**：示例用于对齐概念与 API 形态，不对外暴露服务。

### 27.3–27.4 初次实现：一个能跑的节点

```python
# node_server.py —— 教学示意，不参与构建
# 纯标准库，Python 3.12+
# 运行：python node_server.py            （默认共享 ./shared，端口 8000）
from __future__ import annotations

import os
import sys
from pathlib import Path
from socketserver import ThreadingMixIn
from xmlrpc.client import Fault
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)          # 只接受这一个路径，缩小暴露面

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    daemon_threads = True

class Node:
    """一个 P2P 节点：对外发布自己的共享目录。"""

    def __init__(self, root: str | os.PathLike, secret: str) -> None:
        self.root = Path(root).resolve()
        self.secret = secret

    # —— 27.5「验证文件名」：唯一真正的安全防线 ——
    def _full(self, query: str) -> Path:
        path = (self.root / query).resolve()
        if not path.is_relative_to(self.root):      # Python 3.9+
            raise Fault(1, f"非法路径：{query!r} 指向共享目录之外")
        return path

    def hello(self, peer_url: str) -> str:
        """记录一个已知对等节点；原书用 urlfile 持久化，这里只回执。"""
        return f"已收到你的地址：{peer_url}"

    def list(self) -> list[str]:
        return sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*") if p.is_file())

    def fetch(self, query: str, secret: str) -> bytes:
        """XML-RPC 只有 base64 这种二进制类型：大文件会整份进内存。"""
        if secret != self.secret:
            raise Fault(2, "密钥不匹配")
        path = self._full(query)
        if not path.is_file():
            raise Fault(3, f"文件不存在：{query}")
        data = path.read_bytes()
        if len(data) > 8 << 20:                     # 8 MiB 上限，避免打爆内存
            raise Fault(4, "文件过大，XML-RPC 不适合传大文件")
        return data

    def _dispatch(self, method: str, params: tuple):
        """SimpleXMLRPCServer 的钩子：自定义方法分发与未知方法的错误语义。"""
        func = getattr(self, method, None)
        if func is None or method.startswith("_"):
            raise Fault(5, f"未知方法：{method}")
        return func(*params)

def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "shared")
    root.mkdir(exist_ok=True)
    secret = os.environ.get("NODE_SECRET", "change-me")   # 演示用；生产请走密钥管理
    with ThreadingXMLRPCServer(
        ("127.0.0.1", 8000), RequestHandler, allow_none=True, logRequests=False
    ) as server:
        server.register_instance(Node(root, secret))
        print(f"节点已启动：http://127.0.0.1:8000/RPC2  共享目录 {root}")
        server.serve_forever()

if __name__ == "__main__":
    main()
```

要点：**①** `rpc_paths` 限定路径；**②** 用 `ThreadingMixIn` 让并发请求不必排队（原书单线程，一个慢请求会阻塞所有人）；**③** `Fault` 是 XML-RPC 唯一的正规错误通道，抛普通异常在客户端看到的是「不透明」的 `ProtocolError`。

### 27.5 再次实现：客户端界面（`cmd.Cmd`）+ 异常 + 文件名校验

```python
# node_client.py —— 教学示意，不参与构建
# 运行：python node_client.py http://127.0.0.1:8000/RPC2
from __future__ import annotations

import cmd
import os
import sys
from pathlib import Path
from xmlrpc.client import Fault, ProtocolError, ServerProxy

class Client(cmd.Cmd):
    intro = "输入 help 查看命令；exit 退出。"
    prompt = "peer> "

    def __init__(self, url: str, secret: str, outdir: str = "downloads") -> None:
        super().__init__()
        self.proxy = ServerProxy(url, allow_none=True)
        self.secret = secret
        self.outdir = Path(outdir)

    def do_hello(self, arg: str) -> None:
        print(self.proxy.hello(arg or "http://127.0.0.1:9000/RPC2"))

    def do_list(self, _arg: str) -> None:
        for name in self.proxy.list():
            print(" ", name)

    def do_fetch(self, arg: str) -> None:
        if not arg.strip():
            print("用法：fetch <相对路径>")
            return
        try:
            data: bytes = self.proxy.fetch(arg.strip(), self.secret)
        except Fault as exc:                    # 服务端的业务错误，带 faultCode/faultString
            print(f"[{exc.faultCode}] {exc.faultString}")
            return
        except ProtocolError as exc:            # 传输层错误（连不上、非 200、XML 坏了）
            print(f"连接错误：{exc.errmsg}")
            return
        dest = (self.outdir / Path(arg.strip()).name).resolve()
        if not dest.is_relative_to(self.outdir.resolve()):
            print("拒绝写入：目标路径越界")
            return
        self.outdir.mkdir(exist_ok=True)
        dest.write_bytes(data.data if hasattr(data, "data") else data)
        print(f"已保存到 {dest}（{len(dest.read_bytes())} 字节）")

    def do_exit(self, _arg: str) -> bool:
        return True

    do_EOF = do_exit

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/RPC2"
    sys.exit(Client(url, os.environ.get("NODE_SECRET", "change-me")).cmdloop())
```

三处补强的意义：

| 补强项 | 没有它会怎样 | 做法 |
| --- | --- | --- |
| 客户端界面 | 每次调用都要写一遍 `ServerProxy` 样板 | `cmd.Cmd` 提供 REPL，`do_*` 即命令 |
| 引发异常 | 客户端只能看到 `ProtocolError`，不知道是「没这文件」还是「密钥错」 | 服务端抛 `Fault(code, msg)`，客户端按 `faultCode` 分支 |
| 验证文件名 | `fetch("../../etc/passwd")` 直接读穿整个磁盘 | `Path.resolve()` + `is_relative_to()`，双向都要校验（服务端 + 客户端落盘路径） |

### 27.6 进一步探索与「2026 年等价做法」

| 方向 | 说明 |
| --- | --- |
| 加密与鉴权 | XML-RPC 走明文 HTTP；必须放到 TLS（反向代理）之后，或改为带鉴权的 RPC |
| 大文件 | base64 编码使体积膨胀约 33% 且整份进内存；改用 HTTP 分块下载 |
| 节点发现 | 广播/种子节点/中心目录；原书用「交换 URL 文件」的朴素方式 |
| 完整性 | 传输后校验哈希（SHA-256） |

| 原书环节 | 原书做法 | 2026 年等价做法 |
| --- | --- | --- |
| RPC 协议 | XML-RPC | gRPC（HTTP/2 + Protobuf）、JSON-RPC、或 FastAPI + HTTPS + 鉴权 |
| 服务器 | `SimpleXMLRPCServer`（标准库仍在，但已边缘化） | `uvicorn` + FastAPI；需要流式就用 `StreamingResponse` |
| 客户端 | `ServerProxy` | `httpx`（同步/异步一致）、`grpcio` |
| 错误语义 | `Fault` | HTTP 状态码 + 结构化 JSON 错误体 |

## 版本演进

| 版本 | 与本章相关的变化 |
| --- | --- |
| 3.5（原书基线） | `xmlrpc.server` / `xmlrpc.client` 为标准做法；`SimpleXMLRPCServer` 单线程 |
| 3.7 | `dataclasses`（PEP 557）适合描述节点元数据 |
| 3.9 | 🔴 `Path.is_relative_to()` 可用，路径校验一行搞定（此前要 `os.path.commonpath`） |
| 3.10 | `match`（PEP 634/635/636）便于按 `faultCode` 分支 |
| 3.11 | `ExceptionGroup`（PEP 654）便于聚合多个节点的并发失败 |
| 3.12 | `datetime.utcnow()` 等弃用提醒；标准库开始大规模清理 |
| 3.13 | 🔴 同批死电池被移除（PEP 594）；`xmlrpc` 保留但明确边缘化 |
| 3.14 | 🔧 XML 相关模块的默认安全策略与清理继续演进，以官方 What's New 为准 |

## 经典论文与原始文献

> 以下均为**规范文档，非同行评审论文**。

| 编号 / 名称 | 标题 | 年份 | URL |
| --- | --- | --- | --- |
| XML-RPC 规范 | XML-RPC Specification（UserLand，Dave Winer 等） | 1999 起，持续修订 | http://xmlrpc.com/spec.md |
| PEP 594 | Removing dead batteries from the standard library | 2020 提出，3.13 落地 | https://peps.python.org/pep-0594/ |
| PEP 3156 | asyncio（现代 RPC 客户端的并发底座） | 2012 提出，3.4 落地 | https://peps.python.org/pep-3156/ |
| PEP 654 | Exception Groups and except*（多节点并发失败的聚合） | 2020 提出，3.11 落地 | https://peps.python.org/pep-0654/ |
| CWE-611 | XML 外部实体引用 / 实体膨胀（Billion Laughs）类问题族 | 持续更新 | https://cwe.mitre.org/data/definitions/611.html |
| gRPC 文档 | gRPC Core Concepts（HTTP/2 + Protobuf 的现代 RPC） | 持续更新 | https://grpc.io/docs/what-is-grpc/core-concepts/ |

## 近年研究与工业界开源实践（2015–2026）

- **gRPC**：以 Protobuf 定义契约、HTTP/2 多路复用、内建流式与截止时间（deadline），已成为跨服务 RPC 的事实标准；Python 侧由 `grpcio` 提供。
- **JSON-RPC**：轻量替代，适合浏览器与脚本客户端。
- **FastAPI + HTTPS**：把「RPC 方法」降级为普通 HTTP 端点，换取网关、观测、限流等一整套现成能力。
- **`defusedxml`**：解析**不可信** XML 时的加固库，针对实体膨胀与外部实体引用类问题；🔧 具体防护范围以其官方文档为准。
- **`httpx`**：现代 HTTP 客户端，取代 `ServerProxy` 的手写调用与错误处理。
- **分布式文件共享的工业实践**：BitTorrent（分块 + 哈希校验 + 交换中心）、IPFS（内容寻址）分别代表了「分块传输」与「内容寻址」两条路线，可视为本章「进一步探索」的终局形态。
- 🔧 各项目版本号以官方文档为准；本目录不锁定版本。

## 常见误区与本书需修正之处

| # | 原书写法 / 常见误区 | 问题 | 2026 年正确写法 |
| --- | --- | --- | --- |
| 1 | 🔧 认为 XML-RPC 仍是主流 RPC | 已边缘化；标准库保留但社区不再推荐 | gRPC / JSON-RPC / FastAPI + HTTPS |
| 2 | 🔧 明文 HTTP 传输 + 密钥明文做参数 | 抓包即得密钥与文件内容 | TLS（反向代理终止）+ 正式鉴权（mTLS/OAuth2） |
| 3 | 🔧 解析外部 XML 不做加固 | 实体膨胀类攻击（CWE-611 族）耗尽内存 | `defusedxml`；限制请求体大小 |
| 4 | 🔧 `fetch` 不校验文件名 | `../../etc/passwd` 读穿磁盘 | `resolve()` + `is_relative_to()`；**服务端与客户端都要校验** |
| 5 | 🔧 用普通 `Exception` 表达业务错误 | 客户端收到不透明的 `ProtocolError` | 服务端抛 `Fault(code, msg)`，客户端按 code 分支 |
| 6 | 🔧 单线程服务器 | 一个慢请求阻塞所有节点 | `ThreadingMixIn`（或彻底改用 ASGI） |
| 7 | 🔧 用 XML-RPC 传大文件 | base64 膨胀 ~33%，且整份进内存 | HTTP 分块/流式下载；限制上限 |
| 8 | 🔧 共享密钥写死在源码里 | 泄露即全面失守 | 环境变量 / 密钥管理服务 |
| 9 | 🔧 相信对等节点发来的文件名 | 落盘时同样可能被穿越到系统目录 | 保存端也做白名单校验（示例中的 `dest` 校验） |
| 10 | 🔧 认为 P2P 不需要服务器 | 节点发现、NAT 穿透仍需协调者 | 明确「种子节点 / 目录服务」的信任模型 |

## 与其他章 / 其他书的联系

- 本书：**[14-网络编程.md](14-网络编程.md)**（socket 层原理，`xmlrpc` 之下的那层）、[24-项目5：虚拟茶话会.md](24-项目5：虚拟茶话会.md)（同样是「服务器 + 多会话」，但走长连接）、[28-项目9：使用GUI共享文件.md](28-项目9：使用GUI共享文件.md)（本章节点的 GUI 化）、[26-项目7：自建公告板.md](26-项目7：自建公告板.md)（不可信输入的另一种形态）、[10-开箱即用.md](10-开箱即用.md)（`os`、`shelve` 与反序列化风险）。
- 他书：分布式系统的系统性讨论建议读《数据密集型应用系统设计》（本仓库暂无笔记 🔧）；RPC 契约设计可对照 gRPC 官方文档。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)
