# 第 11 章 WebSocket 原理与实战（卷1）

> WebSocket：全双工、RFC 6455、握手（HTTP Upgrade）、数据帧、Netty `WebSocketServerProtocolHandler`、心跳 ping/pong、IM 推送。本书把 IM 从「长轮询」升级到「全双工推送」。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 握手 | HTTP `Upgrade: websocket` + Sec-WebSocket-Key |
| 帧 | opcode（文本/二进制/ping/pong/close） |
| 推送 | 服务端主动发（取代轮询） |
| 心跳 | ping/pong 保活 |

## 二、核心精讲

### 2.1 🔧 握手与升级
- 客户端发 `Upgrade: websocket` + `Sec-WebSocket-Key`；服务端回 `101 Switching Protocols` + 签名（🔧 之后同一 TCP 上跑 WS 帧，不再是 HTTP 请求-响应）。

### 2.2 与长轮询对照
- 长轮询：客户端挂起等消息，服务端有消息才返（🔧 仍每次 HTTP 开销，且延迟=轮询间隔）；WebSocket：单连接双向实时，IM/行情首选。

### 2.3 Netty 实现
- `WebSocketServerProtocolHandler` 自动处理握手/帧/pong/close（🔧 业务只需处理 `TextWebSocketFrame`/`BinaryWebSocketFrame`）。

## 三、版本演进 / 论文 / 前沿

- 规范：WebSocket RFC 6455（2011）；`Sec-WebSocket-Version: 13`。
- 工业界：Netty、Socket.IO（含降级）、Spring WebSocket（STOMP）、Nginx WS 反向代理。
- 开源 stars（2026-09）：netty 34k / socket.io 62k / spring-framework 58k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "WS 还是 HTTP 轮询" | 握手后全双工帧 |
| 2 | "WS 不用心跳" | 仍要 ping/pong 保活 |
| 3 | "Nginx 不需特殊配" | 需 Upgrade 头透传 |
| 4 | "WS 替所有 HTTP" | 仅实时双向场景 |
