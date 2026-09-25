# 第 12 章 SSL/TLS 核心原理与实战（卷1）

> TLS 握手（RSA/ECDHE）、证书链、对称/非对称、Netty `SslHandler`、ALPN（协商 HTTP/2）、单向/双向认证。本书把「加密传输」讲透，是公网 IM 的必需。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 握手 | ECDHE 密钥交换（前向安全） |
| 证书 | CA 链、X.509、域名校验 |
| 对称加密 | AES-GCM（记录层） |
| Netty | `SslHandler` + `SslContext` |
| ALPN | 协商 HTTP/1.1/2 |

## 二、核心精讲

### 2.1 🔧 ECDHE 前向安全
- 用临时椭圆曲线密钥交换，会话密钥不依赖长期私钥（🔧 即使服务器私钥泄露，历史流量仍安全；RSA 密钥交换无此前向安全，已淘汰）。

### 2.2 `SslHandler` 位置
- 必须放 Pipeline **最前**（入站先解密、出站最后加密）（🔧 Netty `SslContextBuilder` 配证书；双向认证（`needClientAuth`）用于内网 mTLS）。

### 2.3 ALPN
- TLS 握手中用 ALPN 协商应用协议（h2/http1.1），避免额外往返（🔧 HTTP/2 必备）。

## 三、版本演进 / 论文 / 前沿

- 规范：TLS 1.2 RFC 5246、TLS 1.3 RFC 8446（0-RTT/1-RTT，弃 RSA 交换）；X.509、ALPN RFC 7301。
- 工业界：OpenSSL、BoringSSL（Google）、Netty `SslHandler`、Let's Encrypt（免费证书）。
- 开源 stars（2026-09）：netty 34k / nginx 25k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "RSA 密钥交换 OK" | 无前向安全，用 ECDHE |
| 2 | "SslHandler 随便放" | 必须 Pipeline 最前 |
| 3 | "TLS 1.1 够用" | 用 TLS 1.3 |
| 4 | "证书不过期" | 自动化续期（Let's Encrypt） |
