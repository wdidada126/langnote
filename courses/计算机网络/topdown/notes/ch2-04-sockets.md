# 第 7 讲 · Socket 编程入门：UDP/TCP 双风格与并发模型

> 章节：Chapter 2 §2.4
> 中文对照：topdown_ustc 实验一/二（UDP、TCP socket）；配套项目 projects/ch2_http_server、projects/ch3_chat

## 1. 核心概念

- **API 全景**：
  - UDP：`socket(AF_INET, SOCK_DGRAM)` → 服务端 `bind` 后即可 `sendto/recvfrom`（无连接，每报文自带目的地址）；客户端 `connect` 可选（过滤对端+简化错误）。
  - TCP：服务端 `socket→bind→listen(backlog)→accept→read/write→close`；客户端 `socket→connect（触发三次握手）→write/read→close`。
- **socket 是内核对象，不是文件描述符的同义词而是"话术"**：fd 是统一句柄，`read/write` 走 VFS→socket ops→内核协议栈——这解释了 CSAPP 把网络称为"IO 的一种"。
- **并发模型的工程三选一**（本讲与项目重点）：
  - 多进程：隔离好、开销大（传统 inetd/早期 Apache prefork）。
  - 多线程：共享状态方便（本项目 HTTP 服务器用 `threading.Thread` 每连接一线程）；GIL 下 CPU 密集不划算但 IO 密集够用。
  - 单线程事件循环：`select/poll/epoll`（Linux）、`selectors`（Python 跨平台）——Nginx/Node/Redis 的路线。
- **字节流陷阱**：`recv(4096)` 可能返回 1 个字节也可能返回半个请求——"读到分隔符/读满 N 字节"必须应用层自己写循环（本项目 HTTP 解析先读到 `\r\n\r\n`）。
- **地址与端口**：`0.0.0.0`（INADDR_ANY 监听所有接口）、`127.0.0.1`（回环）、`SO_REUSEADDR` 避免 TIME_WAIT 重启失败。

## 2. 关键代码骨架（本讲必须能默写）

```python
# TCP 服务端核心五步
s = socket(AF_INET, SOCK_STREAM)
s.bind(("", 6777)); s.listen(16)
conn, addr = s.accept()          # 已完成三次握手
data = conn.recv(1024)           # 可能短读，循环补
conn.sendall(response)
conn.close()
```

## 3. 层次间与前后讲联系

- 本讲是"用代码验证第 5/6 讲协议"的工具箱：HTTP 服务器=第 5 讲；DNS 查询器=第 6 讲手工报文。
- 向下承接第 3 章：`connect` 即 TCP 状态机（第 11 讲）的用户可见事件；`SO_RCVBUF/SO_SNDBUF` 对应流量控制（第 11 讲）；`TCP_CORK/TCP_NODELAY` 对应 Nagle（第 12 讲拥塞演进段）。
- 封装栈位置：应用进程通过系统调用跨入运输层，是"分层边界"最实感的体现。

## 4. 跨课程联系

- **CSAPP 第 11 章**：同一 API 的 C 版本（`open_clientfd/open_listenfd`），其 rio 包处理的"短读/信号中断"正是本讲字节流陷阱的完整解法——强烈建议对照读。
- **6.S081**：xv6 TCP 不存在，但其 socket 层（`sys_socket.c`）演示 fd→file→devsw 分发；labs 用 UDP echo 实验。
- **CS162**：把 socket 作为内核/用户边界讲，引出零拷贝 sendfile/io_uring（见开源应用）。
- **MIT6.824**：所有 RPC 都建立在 `net/http`/自定义 TCP 上，其超时重试的坑（重复请求）与本讲 `SO_REUSEADDR` 同样属于"工程常识清单"。
- **CS144**：其 stream 重组等价于你在本项目手写的"循环补读"。
- **topdown_ustc**：实验讲义给 C 版本，Python 版可逐行对照。

## 5. 开源项目应用

- **Nginx**：epoll 事件循环+每 worker 多连接，对比本项目"每连接一线程"的规模极限。
- **Python**：`asyncio`（事件循环+协程）、`selectors`（标准库多路复用门面）；gunicorn 的 sync/thread/gevent worker 谱。
- **io_uring / DPDK**：两条"绕过 recvfrom/syscall 开销"的路线——前者保持内核栈，后者用户态栈（与 QUIC 用户态可靠传输殊途同归，第 12 讲）。
- **Wireshark**：给自己的 chat/HTTP 程序抓包，与官方 lab 的字段核对。

## 6. 延伸阅读

- RFC 5066（传输控制块 API，理解 socket 对象本质，进阶）
- Stevens《UNIX Network Programming》Vol.1（§1.5-1.9、§6.3 短读语义；经典中的经典）
- `man 7 socket` / `man 7 tcp` / `man 2 epoll`（Linux 手册页是最权威的"字段表"）
- 官网 Python socket 代码（UDP/TCP 各一）与配套 Wireshark lab

## 7. 自查问题

1. `listen(16)` 的 16 溢出时客户端 connect 表现？（SYN 被丢弃/延迟，非立即拒绝——与 backlog 两队列有关）
2. 为什么 UDP 服务端不需要 accept，但 connect 仍可选用？
3. 多线程服务器如何优雅关闭并保持 keep-alive 语义？
4. `sendall` 与 `send` 区别；`recv` 返回空字节意味着什么？
5. 本项目 HTTP 服务器遇到慢客户端（honor slowloris）会怎样？事件循环版为何更抗？

## 8. 本讲一句话

socket API 是教材与真实系统之间唯一的强制接口：所有第 3~6 章的"纸面状态机"最终都映射到这里几个系统调用上。
