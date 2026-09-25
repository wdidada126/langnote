# 第 5 讲 · HTTP：报文、连接、缓存与 CDN

> 章节：Chapter 2 §2.2
> 中文对照：topdown_ustc 第 2 章（Web 与 HTTP）；配套项目 projects/ch2_http_server

## 1. 核心概念

- **HTTP 是无状态的应用层协议**，运行在 TCP 之上；Web 页 = 基对象 + 引用对象，每个对象是一次"TCP 连接建立 + 请求/响应往返"（HTTP/1.0 非持续）或复用连接（HTTP/1.1 持续）。
- **两种模式的 RTT 数学（必会）**：
  - 非持续：每个对象 `2RTT + d_trans` → n 个对象 = `n·(2RTT+传输)`。
  - 持久（流水线）：`1 RTT（握手）+ RTT（请求响应）+ 传输`，n 对象约 `2RTT + n·传输`。
  - 这就是"持久连接提速 ~40%"的经典结论，也是 CDN 用 TCP 优化进一步提速的空间。
- **报文结构**：
  - 请求：请求行 `GET /index.html HTTP/1.1` + 头（Host、User-Agent、If-Modified-Since、Accept-Encoding）+ 空行 + 体（POST）。
  - 响应：状态行 `HTTP/1.1 200 OK` + 头（Content-Type/Length、Cache-Control、ETag、Connection）+ 体。
  - 状态码五类：1xx/2xx/3xx/4xx/5xx，重点 304（条件 GET）、404、503。
- **Cookie/Session vs HTTP 无状态**：状态是服务端/客户端存储+ID 的"叠加层"。
- **缓存与验证**：强缓存 `Cache-Control: max-age`；协商缓存 `Last-Modified/If-Modified-Since`、`ETag/If-None-Match`。
- **CDN**：把内容推到边缘（POP）并用 DNS/GSLB 引导就近；origin 回源、缓存命中率是成本关键（第 8 讲深入 DASH/流式分发）。

## 2. 关键字段/机制

- `Content-Length` vs `Transfer-Encoding: chunked`（解决动态内容的长度未知+连接复用）。
- `Connection: keep-alive` 与管线化（pipelining，因实现坑多而基本废弃，被 HTTP/2 多路复用取代）。
- HTTP/2：二进制分帧、单连接多流、头部压缩 HPACK——动机仍是本讲"连接数与队头阻塞"问题；HTTP/3 把可靠性搬进 UDP/QUIC（第 12 讲）。

## 3. 层次间与前后讲联系

- 封装栈：HTTP 报文→TCP 段→IP→以太帧；Wireshark lab 能看到"一个 GET 被拆成几个 TCP 段、帧如何跨 MTU"。
- 下一讲 DNS 解释"域名如何变成 HTTP 用的 IP"；第 7 讲 socket 用代码重走一遍本讲流程；第 10 讲 rdt 原则解释 HTTP over TCP 里"为什么不用自己重传"。

## 4. 跨课程联系

- **CSAPP**：tiny.c 处理请求行解析+CGI——对应本项目 ch2_http_server 的路由表设计。
- **MIT6.824**：MapReduce 主从交互是自定义 HTTP JSON RPC，理解本讲后再看 6.824 lab1 的"HTTP 即 RPC 载体"会非常顺。
- **CS144**：HTTP 段进入其 reassembler 后字节流重组再交给应用，印证"TCP 无边界、HTTP 自定界"。
- **topdown_ustc**：中文对照重点讲"对象获取时间公式"，考试常考。

## 5. 开源项目应用

- **Nginx**：`location` 路由表 ≈ 本项目 ch2 的简易路由实现；`proxy_cache` 是 CDN 单机模拟。
- **Envoy**：LB + 连接池 + HTTP/2 终结，生产侧本讲所有概念的集大成。
- **Wireshark**：HTTP 抓包 lab（官网官方实验）；观察 304、chunked、keep-alive 关闭时机。
- **Caddy / httpbin**：httpbin 是验证头部语义的活文档。

## 6. 延伸阅读

- RFC 9110（HTTP 语义）、RFC 9112（HTTP/1.1 连接管理）、RFC 9113（HTTP/2）
- RFC 8297（101 Early Hints——把缓存资源提示提前到响应头前）
- 官网 Wireshark lab: HTTP + interactive quiz 2.2

## 7. 自查问题

1. 一个含 15 个嵌入对象、域名 3 个的页面，非持续 vs 持久流水线各需几个 RTT？
2. If-Modified-Since 与 ETag 各自缺陷（1s 粒度 / 内容相同但 ETag 变化）？
3. 为什么 chunked 只用于响应不用于请求？
4. CDN 边缘缓存命中率下降 10%，为什么对回源带宽的影响远大于 10%？
5. 用 telnet/nc 手写一个非法 HTTP 请求，观察状态码。

## 8. 本讲一句话

HTTP 的全部演进都在对抗两件事：连接开销（持久/复用/0-RTT）与传输冗余（缓存/压缩/CDN）。
