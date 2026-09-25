# CSE365 论文与开源应用映射

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| The Internet Worm: Analysis and Lessons (Morris 蠕虫报告, Spafford) | 1989 | 首个大规模网络蠕虫的复盘：误用 + 溢出 + 信任链 | L1–L2 |
| "Smashing the Stack for Fun and Profit" (Aleph One) | 1996 | 栈溢出与 shellcode 的启蒙文档 | L6–L7 |
| Efficient Software-Based Fault Isolation (Wahbe et al.) | 1993 | 用软件检查实现隔离：防御侧经典 | L3, L7 |
| Security of the World Wide Web? / GSI: A Scalable Distributed Approach to SQL Injection | 1998 | SQL 注入的系统化防御（查询签名）开山 | L11 |
| XSS 攻击与防御的早期系统性文档（CERT/OWASP 时代） | 2000s | XSS 分类与输出编码防御范式 | L10 |
| HTTP Cookie/会话机制标准演化 (RFC 2109 → RFC 6265) | 1997/2011 | 浏览器状态管理即攻击面的制度化记录 | L4 |
| New Directions in Cryptography (Diffie & Hellman) | 1976 | 公钥密码：L9 信任问题的数学解 | L9 |
| Insider Threat: A Cyber Kill Chain Methodology (Hutchins, Cloppert & Amin) | 2011 | 网络攻击链模型：侦察到横移的通用框架 | L12 |

## 近 5 年论文（2021–2026）

| 标题 | 年份/出处 | 一句话贡献 | 关联讲次 |
|---|---|---|---|
| CTF 教育效果测量研究（"Do Jeopardy CTFs Help?" 及后续工作） | 2021–2023 | 以数据验证 CTF 教学法的习得效果 | L1–L12 |
| Got SAML? Security Auditing of Web Applications with Cross-Framework Data-Flow Analysis | USENIX Sec 2021 | SSO/SAML 实现级漏洞批量发现 | L10–L11 |
| 真实 Web 生态注入漏洞存续测量（CMS/插件 SQLi 长期研究） | 2021–2023 | 注入漏洞在互联网上的暴露周期与修复经济学 | L11 |
| Hertzbleed: Power Side-Channel → Timing Attack | USENIX Sec 2022 | 侧信道新类别，密码库的现实威胁 | L9 |
| DARPA AIxCC（AI Cyber Challenge）技术报告 | 2024–2025 | LLM/自动系统发现与修补真实漏洞的竞赛化评测 | L12 |
| 后量子混合密钥交换部署测量（X25519Kyber 等 TLS 试验报告） | 2022–2024 | Web/TLS 生态 PQ 迁移进度审计 | L9 |

## 知识点在开源项目中的应用

> 安全课映射要求：pwn.college / CTF / Syzkaller 生态优先。

| 知识点（讲次） | 开源项目 | 应用方式 |
|---|---|---|
| Linux 滥用与提权（L1–L3） | pwn.college（平台本体）、gtfobins、pspy、linpekas? → LinPEAS | dojo 关卡即攻击面演练；提权枚举工具 |
| CTF 基础设施 | CTFd、picoCTF、ctf-shell? → shellctl | 赛题平台与入门题库 |
| Web 基础与代理（L4–L5） | Burp Suite Community、OWASP ZAP、mitmproxy | 拦截代理抓包与协议实验 |
| 汇编与调试（L6–L7） | GDB + pwndbg/GEF、pwntools、radare2 | 单步调试、脚本化交互 |
| 密码学（L8–L9） | OpenSSL、cryptography (Python)、hashcat（口令哈希实验用自建样例） | 加密 API 对照与哈希成本测量 |
| 命令注入/XSS（L10） | OWASP Juice Shop、DVWA、badstore (OWASP) | 合法靶场复现攻击与修复 |
| SQL 注入（L11） | sqlmap（对本地靶使用）、libinjection（WAF 检测引擎） | 注入验证与检测规则学习 |
| 综合攻击链（L12） | Syzkaller（内核 fuzzing 生态入口）、Metasploit Framework（防御视角研读） | 自动化漏洞研究范式预览 |
