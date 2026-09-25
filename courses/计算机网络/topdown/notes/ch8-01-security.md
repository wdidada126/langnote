# 第 24 讲 · 在线补充：网络安全——密码学基础、认证、TLS/SSL 与防火墙/VPN

> 章节：第 7 版在线 Chapter 8（Security in Computer Networks）
> 中文对照：topdown_ustc 第 8 章（网络安全）；与 MIT6.858/CS161 交叉

## 1. 核心概念

- **威胁模型四件事**：保密性（confidentiality）、完整性（integrity）、可用性（DoS，第 12 讲拥塞的恶意版）、端点认证/否认性。攻击者能力分级：窃听→主动插入/篡改→中间人→共谋（第 6 讲 DNS、第 18 讲 BGP 的攻击面在安全层复现）。
- **密码学积木（只要求"会用"级别）**：
  - 对称（AES）：快、需共享密钥——密钥分发问题引出公钥。
  - 公钥（RSA/ECDSA/DH）：`y=EK(x)`、签名 `SK(m, H(m))`；DH 交换（`g^a mod p, g^b → g^ab`）实现"未谋面先约定"。
  - 哈希与 MAC：`H(m)` 抗原像/抗碰撞；`MAC_K(m)` 给对称完整性；AEAD（AES-GCM）合并加密+完整性——"先加密后 MAC"的顺序陷阱教学案例。
  - 随机性：CSPRNG； nonce/IV 唯一性（WEP 之殇，第 22 讲回环）。
- **认证**：口令→密钥派生（盐+慢哈希）；证书链（CA 信任锚、X.509）与吊销（CRL/OCSP→OCSP stapling）；公钥基础设施的信任根是"因特网最大的社会工程"。
- **TLS/SSL 协议栈（重点）**：
  - TLS 1.2 握手：ClientHello（版本、随机数、密码套件列表）→ ServerHello+证书+ServerKeyExchange → 密钥协商 → Finished（完整性证明）——**1-RTT、可选会话恢复**。
  - TLS 1.3（RFC 8446）：精简为 (EC)DHE-only、1-RTT + 0-RTT（early data 的重放风险）、删除 CBC/RSA 密钥交换等历史包袱；与 QUIC 集成（第 12 讲：TLS1.3 是 QUIC 的强制组件）。
  - 应用：HTTPS=HTTP(第 5 讲) over TLS over TCP；SNI（多证书一 IP）、HSTS、证书透明 CT（Let's Encrypt 生态前提）。
- **防火墙与 VPN**：包过滤（五元组，第 9 讲分用的反向利用：内核 netfilter/nftables）、状态防火墙（连接跟踪=第 15 讲 NAT 表同构）、应用代理（WAF）；VPN：IPsec（隧道模式 AH/ESP）、WireGuard（现代：公钥+UDP+内核模块极简）、TLS-termination 代理（云 LB）。DoS：SYN 洪水（第 11 讲）、放大反射（第 6 讲 DNS/memcached）、慢速攻击（第 7 讲每连接线程模型的弱点）。

## 2. 关键对照表

| 目标 | 工具 | 出现讲次 |
| --- | --- | --- |
| 保密 | AES/ChaCha20 | 本讲 |
| 完整性 | 哈希/MAC/AEAD | 第 20 讲 CRC 的"恶意对手版"（CRC 无线性密码学强度） |
| 认证 | 签名/证书链 | 第 18 讲 RPKI、第 22 讲 802.1X |
| 密钥交换 | DH/ECDHE | 本讲 |
| 端到端加密位置 | TLS（表示层）/ QUIC 内置 / SSH(应用层) / IPsec(网络层) / 链路层(WPA2) | 封装栈五层各有一处——**"加密放哪层"是分层思想的终极考题** |

## 3. 层次间与前后讲联系

- 本讲几乎每个攻击面都在前面出现过：DNS 投毒（6）、BGP 劫持（18）、HTTP 无状态被 Cookie 窃取（5）、WEP（22）、SYN 洪水（11）；安全=把"尽力而为"升级为"可验证"。
- CRC/校验和（14/20）vs MAC：前者防信道噪声、后者防对手——这是全课对"差错 vs 篡改"的统一澄清。

## 4. 跨课程联系

- **MIT6.858/CS161**：6.858 从 Web 安全攻防视角重讲 TLS/证书；本课只到"协议正确+威胁意识"，想深挖读其教材与 Lab（可选路径）。
- **CSAPP**：`arc4random`/OpenSSL EVP API 的工程使用；CSAPP 的"缓冲区溢出即安全"与本讲"协议设计即安全边界"互补。
- **6.S081**：内核 crypto API 框架与 WireGuard 模块（`drivers/net/wireguard`）是"加密进网络栈"的样本。
- **MIT6.824**：Raft/MapReduce 的认证通常交给 TLS 或部署假设——"安全边界划在哪"与本讲分层选择同一方法论。
- **topdown_ustc**：郑烇老师 RSA 数字小演算 + TLS1.3 状态机板书。

## 5. 开源项目应用

- **OpenSSL / BoringSSL / mbedTLS**：TLS 参考/嵌入式三形态；`openssl s_client -tls1_3` 手验握手。
- **Wireshark**：`keylog` 解密 HTTPS（SSLKEYLOGFILE 环境变量——官方 lab 的做法）；TLS 扩展字段 dissect。
- **Nginx/Envoy/Caddy**：TLS 终结、证书自动化（Caddy 的 Let's Encrypt 全流程）、mTLS 服务网格（SPIFFE 线）。
- **WireGuard / strongSwan / Tailscale**：VPN 三代产品谱系；`wg show` 看会话密钥轮换。
- **Linux**：`nftables` 状态防火墙、`xt_conntrack`、内核 crypto；Let's Encrypt + certbot（部署证书的事实标准）。

## 6. 延伸阅读

- RFC 8446（TLS1.3）、RFC 5280（X.509）、RFC 4346（TLS1.1 历史）、RFC 6101（DTLS，QUIC 之外 UDP 加密）、RFC 8484（DoH，安全×DNS）、RFC 9110 的 `Strict-Transport-Security`、RFC 8729（WireGuard 协议）
- Rescorla《SSL and TLS: Designing and Building Secure Systems》（经典专著，可选）；先读 Kurose 在线 §8.1–8.7 全文

## 7. 自查问题

1. 为什么 TLS 记录层需要 AEAD 而不是"加密+校验和"？重放保护靠什么（记录序号）？
2. 1.3 的 0-RTT 与"会话恢复票据"的信任差异在哪（重放窗口）？
3. 状态防火墙与 NAT 表在数据结构上的同/异（超时、方向性）？
4. "把加密放在链路层（WPA2）vs 传输层（TLS）vs 应用层（PGP）"三选一的场景题各举一例。
5. 用 SSLKEYLOGFILE 抓一次真实 HTTPS：识别 ClientHello 的 supported_groups/key_share、证书链与 OCSP。

## 8. 本讲一句话

因特网的"尽力而为"不承诺任何安全属性；TLS 家族在端系统上用握手+AEAD+证书把不可信网络变成"可验证信道"——这是端到端原则最成功的第二次胜利（第一次是 TCP 可靠性）。
