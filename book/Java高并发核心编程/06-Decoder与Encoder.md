# 第 6 章 Decoder 与 Encoder 核心组件（卷1）

> Netty 编解码：`ByteToMessageDecoder`（半包/黏包）、`MessageToByteEncoder`、`LengthFieldBasedFrameDecoder`（长度字段拆包）、`ReplayingDecoder`、自定义协议（魔数/版本/长度/数据）。本书独有「自定义私有协议」实战。

## 一、本章地图

| 组件 | 用途 |
| --- | --- |
| ByteToMessageDecoder | 字节→消息，处理半包 |
| LengthFieldBasedFrameDecoder | 按长度字段拆包（主流） |
| MessageToByteEncoder | 消息→字节 |
| 私有协议 | 魔数+版本+长度+体 |

## 二、核心精讲

### 2.1 🔧 半包/黏包根因
- TCP 是字节流，无消息边界；发送端 Nagle、接收端内核缓冲、MTU 都会导致「一个 write 被拆、多个 write 黏」（🔧 解决：定长、分隔符、或**长度字段**——`LengthFieldBasedFrameDecoder` 最通用）。

### 2.2 自定义协议帧
- 典型：`[魔数4][版本1][长度4][数据N]`；解码先读长度再累加（🔧 防超长包攻击：设 `maxFrameLength` 拒绝畸形帧，避免 OOM）。

## 三、版本演进 / 论文 / 前沿

- 论文/规范：TCP RFC 793（字节流语义）；HTTP/2 帧、`WebSocket` 帧同为长度前缀思路。
- 工业界：Netty `codec`/`codec-http`；gRPC 用 HTTP/2 + Protobuf；Dubbo 私有协议。
- 开源 stars（2026-09）：netty 34k / grpc-java 11k / dubbo 41k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "TCP 有消息边界" | 字节流，需拆包 |
| 2 | "分隔符拆包通用" | 二进制用长度字段 |
| 3 | "不限制 maxFrameLength" | 畸形包 OOM 攻击 |
| 4 | "手写 decode 不累加" | 半包要缓存累积 |
