# 第 9 章 HTTP 原理与 Web 服务器实战（卷1）

> HTTP/1.1 报文、请求/响应、Cookie/Session、用 Netty 写 Web 服务器、与 Tomcat/Jetty 对照。本书把「HTTP 协议 + Netty 实现」打通，是 HTTP 服务的网络层基础。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 报文 | 请求行/头/体；状态行 |
| 连接 | keep-alive（复用 TCP） |
| Web 服务器 | Netty HttpServerCodec + 路由 |
| 对照 | Tomcat/Jetty（Servlet 容器） |

## 二、核心精讲

### 2.1 🔧 keep-alive 与连接复用
- HTTP/1.1 默认持久连接，多请求复用一条 TCP（🔧 省去 TCP 握手 + TLS 开销；但队头阻塞：同连接串行；HTTP/2 多路复用解决，见 10 章）。

### 2.2 Netty 写 HTTP 服务
- `HttpServerCodec`（合并 `HttpRequestDecoder`+`HttpResponseEncoder`）+ `HttpObjectAggregator`（聚合整包）+ 业务 Handler（🔧 注意 `LastHttpContent` 标记体结束）。

## 三、版本演进 / 论文 / 前沿

- 规范：HTTP/1.1 RFC 2616→7230；HTTP/2 RFC 7540；HTTP/3 RFC 9114（QUIC/UDP）。
- 工业界：Tomcat、Jetty、Netty（网关/代理层）、Undertow（WildFly）。
- 开源 stars（2026-09）：netty 34k / tomcat 8k / jetty 4k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "每请求新连接" | 用 keep-alive 复用 |
| 2 | "HTTP/1.1 无队头阻塞" | 同连接串行，HTTP/2 解 |
| 3 | "手写 HTTP 服务" | 多数用 Tomcat/网关 |
