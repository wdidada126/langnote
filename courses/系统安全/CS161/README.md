# UCB CS161 计算机安全（Computer Security）

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | UC Berkeley CS161: Computer Security |
| 学校 | University of California, Berkeley |
| 主讲 | 安全教研组（公开版为 2020 夏季学期，Antonia Tabiu/Dawn Song 体系延续） |
| 教材 | 官方在线教材 https://textbook.cs161.org/（课程自编） |
| csdiy 路径 | `系统安全/CS161`（csdiy 页面归类于「计算机系统安全」） |
| 最新期次 | Su2020 全开源（录影+作业），教材持续更新 |
| 状态 | 骨架 |

- 课程网站：https://su20.cs161.org/ （后续届次入口同名规律）
- 作业：7 个在线 HW + 3 个 Lab + 3 个 Project（Project 2 用 Go 实现安全文件分享系统，>3k 行）
- csdiy 资源汇总：PKUFlyingPig/UCB-CS161

## 为什么学

- 五,module 结构覆盖「设计原则 → 内存安全 → 密码学 → Web → 网络」，是广度与动手平衡最好的安全入门系统课之一。
- Project 2 密集开发一个真实安全系统（认证、密钥管理、传输安全全自己扛），一次性打通多块知识。
- 承接 CS61A/B/C 与 CS162，是走向 6.858、CSE466、SEED Labs 等攻防深水区的最平滑台阶。

## 先修与知识联系

- 先修：CS61A、CS61B、CS61C（含 C 与汇编、缓存/虚拟内存）；建议学过 CS162/OS 基础。
- 联系：CSAPP 的缓冲区/栈帧知识在此变成攻击面；密码学部分上承 CS70 概率数论，下接 6.1600（理论更强）；Web/网络部分与 CS162/CS168 协议内容互为表里；与 6.858、SEED Labs 构成「原则→攻防→实验」互补。

## 讲义章节目录（按 Su2020 + textbook.cs161.org 五部分整理）

| 讲次 | 标题 | 阅读材料 |
|---|---|---|
| **Part 1 安全设计原则** | | |
| L1 | 导入：威胁模型、攻击者/防御者视角 | 教材 Ch.1 |
| L2 | 安全设计原则（完备性、最小特权、失效安全…） | Saltzer & Schroeder (1975)；教材 Ch.2 |
| L3 | 访问控制：IBAC / RBAC / 能力 | 教材 Ch.3 |
| L4 | 案例：选举安全 / Kerberos 与密钥管理 | 教材 Ch.4–6；Kerberos (Steiner 1988) |
| **Part 2 内存安全** | | |
| L5 | C 语言与不安全内存：越界、UAF、整数溢出 | 教材 Ch.7 |
| L6 | 栈溢出攻击：shellcode 与返回地址劫持 | Aleph One (1996)；教材 Ch.8 |
| L7 | 防御：canary、ASLR、DEP/CFI 与内存安全语言 | 教材 Ch.9 |
| **Part 3 密码学** | | |
| L8 | 对称加密：AES、分组模式与其误用 | 教材 Ch.10；Katz-Lindell 节选 |
| L9 | 非对称加密：RSA、Diffie-Hellman、混合加密 | DH (1976)、RSA (1978)；教材 Ch.11 |
| L10 | 完整性：哈希、MAC、数字签名 | 教材 Ch.12 |
| L11 | 密钥分发与 PKI / TLS | 教材 Ch.13 |
| **Part 4 Web 安全** | | |
| L12 | Web 基础与同源策略 | 教材 Ch.14 |
| L13 | 注入类：SQLi、命令注入；XSS 与 CSRF | 教材 Ch.15–16 |
| L14 | 项目评审：安全文件分享系统设计 | Project 2 规格 |
| **Part 5 网络安全** | | |
| L15 | DNS 安全与劫持 | DNSSEC (2017 更新) |
| L16 | BGP/路由层攻击 | BGP hijacking 案例材料 |
| L17 | DoS、Side Channel 与课程总结 | 教材相应章节 |
| L18 | 前沿讲座/评审周 | 当期安排 |

> 注：各届讲次略有出入，以 textbook.cs161.org 章节为主线填充笔记。

## 作业与项目（概览）

HW1–7（概念与协议分析）、Lab1（缓冲溢出小实验）、Lab2（加密练习）、Lab3（Web 攻击）、Project 1（设计文档/原则应用）、Project 2（Go 文件分享系统）、Project 3（攻防综合）。详见 `projects/README.md`。
