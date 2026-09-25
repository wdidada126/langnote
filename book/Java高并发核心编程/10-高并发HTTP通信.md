# 第 10 章 高并发 HTTP 通信的核心原理（卷1）

> 客户端高并发 HTTP：连接池（`PoolingHttpClientConnectionManager`）、keep-alive 复用、HTTP/2 多路复用、队头阻塞、DNS/超时/重试。本书补「调用方视角」的高并发，与 9 章服务端互补。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 连接池 | 最大连接/每路由上限/空闲回收 |
| HTTP/2 | 多路复用单连接多流 |
| 超时 | connect/read/conn acquire |
| 重试 | 幂等才重试，避双写 |

## 二、核心精讲

### 2.1 🔧 连接池参数
- 设「总连接上限 + 每路由（host）上限」，否则单 host 占满池拖垮其他（🔧 Apache `HttpClient`/`OkHttp` 都需配；`connectionRequestTimeout` 防等池死锁）。

### 2.2 HTTP/2 多路复用
- 单 TCP 上多「流」并行，去 HTTP/1.1 队头阻塞（🔧 gRPC/HTTP2 默认开启；但单连接若 TCP 层丢包仍阻塞全部流——HTTP/3 改 QUIC/UDP 解）。

### 2.3 重试与幂等
- 仅 GET/幂等 POST 重试；非幂等重试会双扣（🔧 用幂等键 idempotency-key + 去重表）。

## 三、版本演进 / 论文 / 前沿

- 规范：HTTP/2 RFC 7540、HTTP/3 RFC 9114（QUIC）、HPACK（头压缩）。
- 工业界：OkHttp（Android/Java）、Apache HttpClient、WebClient（Reactor/Netty）、gRPC。
- 开源 stars（2026-09）：okhttp 47k / grpc-java 11k / netty 34k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "不配连接池上限" | 每路由上限防饿死 |
| 2 | "非幂等也重试" | 双写，用幂等键 |
| 3 | "不分 connect/read 超时" | 各自独立设 |
| 4 | "HTTP/2 无线头阻塞" | TCP 层丢包仍阻塞 |
