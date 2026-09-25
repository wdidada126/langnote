# SEED Labs 论文与开源应用映射

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| A Short Report on the ARPANET Email Worm (Morris & Thompson) | 1979 | 溢出 + 信任滥用的第一次全网演习 | L1, L6 |
| "Smashing the Stack for Fun and Profit" (Aleph One) | 1996 | 栈溢出/shellcode 原理文档，L1–L3 的原文语境 | L1–L3 |
| Efficient Software-Based Fault Isolation (Wahbe et al.) | 1993 | 软件级隔离思想：现代沙箱源头 | L24 |
| The Protection of Information in Computer Systems (Saltzer & Schroeder) | 1975 | 最小特权/完全中介等原则，权限 Lab 的纲领 | L6, L11 |
| Security of Computer Systems: Towards a Language of Access Control? — Harrison-Ruzzo-Ullman | 1976 | 访问矩阵可判定性，OS 安全理论根基 | L11 |
| A Security Problem in TCP: Connection Spoofing Using Predicted Sequence Numbers (Chase) | 1994 | TCP 序列号可预测性攻击的理论基础 | L14 |
| DNS 缓存投毒修复与源端口随机化 (Kaminsky 方案, RFC 5452) | 2008 | 事务 ID/源端口熵不足导致投毒的修复范式 | L12, L21 |
| Cryptanalysis of MD5 Compress (Stevens et al.) / SHA-1 chosen-prefix (2020) | 2008/2020 | 碰撞攻击实证：SHA-1 证书伪造 | L10, L21 |
| Randomness Requirements for Security (Eastlake et al., RFC 1750) | 1994 | CSPRNG 要求的标准化起点 | L8 |
| Cache Attacks and Countermeasures: the Case of AES (Osvik et al.) | 2006 | 缓存侧信道系统化开山 | L23 |
| Spectre Attacks: Exploiting Speculative Execution (Kocher et al.) | 2019 | 推测执行打破沙箱边界，L23 前沿篇 | L23 |
| SQL Injection Web Services? 奠基: "The SQL injection phenomenon"? — 学术源头: Martin 1998 GSI 论文 | 1998 | SQLi 与查询签名防御的首篇系统研究 | L18 |

> 注：带 ? 标记的条目在教学材料引用中常被口语化，填充笔记时按 DOI/原刊名核对。

## 近 5 年论文（2021–2026）

| 标题 | 年份/出处 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| 大规模 Log4Shell（Log4j JNDI 注入）生态测量研究 | 2022 | 反序列化 RCE 在真实互联网 24h 内的扩散画像 | L18 |
| CopyFail (CVE-2025-0927)：OverlayFS 竞态本地提权披露 | 2025 | 竞态利用直接改写 backing file 拿 root 的新样本 | L5 |
| DirtyPipe (CVE-2022-0847) 分析与检测研究 | 2022 | 管道缓冲区未初始化写 → 任意文件覆写提权 | L5, L6 |
| DARPA AIxCC 决赛技术报告 | 2024–2025 | LLM/自动系统对真实代码库的漏洞发现与修补 | L24 |
| 弱 PRNG 在 IoT/固件中的持续测量研究 | 2021–2023 | 随机数缺陷仍是量产级根因 | L8 |
| Side-channel 攻防在云/SGX 上的新载体（如 TLBlade, USENIX Sec 2024） | 2024 | 共享微结构泄露持续演进 | L23 |

## 知识点在开源项目中的应用

> 按要求映射 pwn.college / CTF / Syzkaller 生态。

| 知识点（讲次） | 开源项目 | 应用方式 |
|---|---|---|
| 溢出/ROP/竞态（L1–L5） | pwn.college、pwntools、how2heap、syzkaller 竞态 PoC 库 | 靶题链练习；内核竞态样本研读 |
| 权限滥用（L6, L11） | Linux man-pages（setuid 语义）、gtfobins、pspy | 提权枚举与机制文档对照 |
| 密码学 Lab（L7–L10） | OpenSSL、libsodium、hashpump、John the Ripper | API 与攻击实现双向验证 |
| 网络攻防（L13–L17） | Scapy、Wireshark、Snort/Suricata、strongSwan、mitmproxy | 报文构造、IDS 规则、IPsec、TLS 拦截 |
| Web（L18–L21） | OWASP Juice Shop、sqlmap（本地靶）、Certbot/mini-CA、ZAP | 注入靶场与证书链实验 |
| DNS 基础设施（L12, L21） | BIND 9、Unbound、dnsdiag? → dnsmasq 测试 | 权威/递归/校验全栈动手 |
| 移动（L22） | Mobsf、Android-x86 靶镜像 | 静态扫描与权限审计 |
| 侧信道（L23） | 学术复现套件（libflush+reload PoC 群）、Spectre 演示仓库 | 计时/缓存攻击复现 |
| 前沿与防御（L24） | OSS-Fuzz、AFL++、KernelCTF 靶、gVisor | 从 Lab 通往工业漏洞研究 |
