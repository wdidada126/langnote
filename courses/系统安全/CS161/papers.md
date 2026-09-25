# CS161 论文与开源应用映射

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| The Protection of Information in Computer Systems (Saltzer & Schroeder) | 1975 | 提出沿用至今的安全设计原则体系 | L2 |
| Hints for Computer System Design (Lampson) | 1983 | 含「攻击者-防御者不对称」等影响深远的设计箴言 | L2 |
| Email Worm: The Foundation of Internet Security (Morris & Thompson) | 1979 | 首个网络蠕虫，暴露信任与缓冲区双重弱点 | L1, L6 |
| "Smashing the Stack for Fun and Profit" (Aleph One, Phrack) | 1996 | 栈溢出利用的系统化启蒙文档 | L6 |
| New Directions in Cryptography (Diffie & Hellman) | 1976 | 公钥密码与密钥交换思想的开山之作 | L9 |
| A Method for Obtaining Digital Signatures (Rivest, Shamir, Adleman) | 1978 | RSA：第一个实用公钥加密与签名方案 | L9, L10 |
| Using Encryption for Authentication (Needham & Schroeder) | 1978 | 认证协议范式，其缺陷催生形式化分析领域 | L4 |
| An Attack on a Protocol for Mutually Authentication (Lowe) | 1995 | 揭示中间人攻击并修正 NS 协议 | L4 |
| Kerberos: A Authentication Server (Steiner et al.) | 1988 | 可信第三方票据系统的工业标准 | L4 |
| DNSSEC 协议族 (RFC 4033/4034/4035, 及 2017 算法更新 RFC 8080) | 1997–2017 | DNS 来源真实性的密码学签名链 | L15 |

## 近 5 年论文（2021–2026）

| 标题 | 年份/出处 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| Got SAML? Security Auditing of Web Applications with Cross-Framework Data-Flow Analysis | USENIX Sec 2021 | 大规模审计 SSO 协议实现漏洞 | L13 |
| Hertzbleed: Turning Power Side-Channel Attacks Into Timing Attacks | USENIX Sec 2022 | CPU 功耗调频把功率侧信道变成远程计时攻击 | L17 |
| TLBlade: Prefetch-based TLB 侧信道攻击 | USENIX Sec 2024 | 通过 TLB 预取通道实现跨隔离边界的密钥提取 | L17 |
| FIPS 203/204/205：后量子密码标准化（ML-KEM/ML-DSA/SLH-DSA） | NIST 2024 | 抗量子密钥封装、签名与哈希标准落地 | L9, L10, L11 |
| ret2page: A New Page-Face — 页缓存侧信道削弱内核 ASLR | 2022 | 新型缓解绕过：从页复用提取熵 | L7 |
| Speculative Probing: 浏览器跨源数据泄露 | USENIX Sec 2023 | 推测执行使同源策略在 Spectre 时代失效 | L12, L17 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 应用方式 |
|---|---|---|
| RBAC/访问控制（L3） | Kubernetes、Casbin、OPA | K8s RBAC 策略对象；OPA/Casbin 策略引擎 |
| Kerberos/票据认证（L4） | MIT Kerberos (krb5)、Apache Hadoop Security | HDFS/YARN 组件间 Kerberos 双向认证 |
| 栈溢出与加固（L6–L7） | pwn.college、glibc、Chromium sandbox | CTF 靶题链；CFI/PAC 在 libc/浏览器落地 |
| 内存安全语言（L7） | Rust for Linux、Android (AOSP Rust) | 内核与系统组件用 Rust 重写以根除整类漏洞 |
| 对称/AEAD 加密（L8） | OpenSSL、libsodium、BoringSSL | TLS 记录层与磁盘加密（LUKS2）的 XChaCha20/AES-GCM |
| PKI/TLS（L11） | Let's Encrypt、Caddy、Certificate Transparency | ACME 自动签续；CT 日志公开审计证书签发 |
| Web 攻击防御（L13） | OWASP Core Rules (ModSecurity)、Keycloak | WAF 规则拦截 SQLi/XSS；OIDC 反 CSRF 流程 |
| DNS 安全（L15） | Unbound+DNSSEC、dnsdist、nextdns DoH | RR 校验、DoH/DoT 解析器 |
| BGP 安全（L16） | RPKI 工具链（FRR/outreach BGP toolkit）、BGPStream | ROV 部署验证与劫持检测 |
| DoS/侧信道（L17） | Cloudflare 开源栈 (eBPF/Ahoy?)、Linux 内核 BPF | eBPF/XDP 限速清洗；侧信道检测研究 |
