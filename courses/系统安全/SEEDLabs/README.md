# Syracuse SEED Labs 网络安全实验体系

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | SEED Labs for Cybersecurity Education（Syracuse University） |
| 学校 | Syracuse University |
| 主讲 | Wenliang Du 教授（NSF 约 130 万美元资助的网络安全教育项目） |
| 教材 | Computer Security: A Hands-on Learning Approach（Wenliang Du 编写，印刷为多种语言）+ 全套开源讲义 |
| csdiy 路径 | `系统安全/SEEDLabs` |
| 最新期次 | Lab 手册持续更新（v25/v26 版本滚动发布），2023-09 后 csdiy 页面仍收录 |
| 状态 | 骨架 |

- 课程网站：https://seedsecuritylabs.org/index.html
- 视频：https://www.handsonsecurity.net/video.html
- 教材站：https://www.handsonsecurity.net/index.html
- 实验环境：课程提供开箱即用的 Ubuntu 虚拟机镜像 / VirtualBox 镜像 + Docker 环境
- 全球 1050+ 研究机构使用；csdiy 资源汇总：LaPhilosophie/seedlab

## 为什么学

- 四十多个实验覆盖软件安全、Web、网络、OS、密码、移动、云/物联网/侧信道全主题，是「安全实验的百科全书」。
- 每个 Lab 都有配套教材章节 + 攻击/防御双向任务 + 环境脚本，自学零摩擦。
- 与讲课型课程互补：CS161/6.1600 学的概念，在这里全部要亲手复现一遍攻防。

## 先修与知识联系

- 先修：无硬性要求；建议具备 C/Python 基础与 Linux 使用经验。
- 联系：作为 CS161/6.1600/6.858/CSE365 的实验弹药库最合适；缓冲区溢出 Lab 与 CSE466 内容重叠但更教学化；网络 Lab 与 CS168/CS144 协议学习互证。

## 讲义（实验主题）目录（按官方 Lab 分类整理）

| 讲次 | 标题 | 阅读材料 |
|---|---|---|
| **软件安全（Software Security）** | | |
| L1 | 缓冲区溢出攻击（setuid root 夺壳） | 教材对应章 + Lab Task 手册 |
| L2 | 绕过非执行栈 / 利用 vs 保护 | 同上（含 shellcode 材料） |
| L3 | 绕过 ASLR | 同上 |
| L4 | 格式化字符串攻击 | Lab 手册 |
| L5 | 竞态条件攻击（TOCTOU） | Lab 手册 |
| L6 | SETUID/权限程序滥用与环境变量攻击 | Lab 手册 |
| **密码学（Cryptography）** | | |
| L7 | 加密基础实验（对称/公钥调用） | Lab 手册 |
| L8 | 随机数攻击（弱 PRNG 预测密钥） | Lab 手册 |
| L9 | ECB 模式攻击与密文操纵（含 padding oracle 变体） | Lab 手册 |
| L10 | Hash 长度扩展与 MAC 伪造 | Lab 手册 |
| **OS 安全（System Security）** | | |
| L11 | Linux 启动与 GRUB 密码 / 口令破解实验 | Lab 手册 |
| L12 | DNS 基础设施安全（BIND 加固） | Lab 手册 |
| **网络安全（Network Security）** | | |
| L13 | 网络嗅探与 Spoofing（ARP/ICMP/TCP） | Lab 手册 |
| L14 | TCP RST 注入与会话劫持 | Lab 手册 |
| L15 | 防火墙（iptables/nftables 实验） | Lab 手册 |
| L16 | IDS：Snort 规则与规避 | Lab 手册 |
| L17 | VPN/TLS：MITM 攻击（自签证书）与 VPN 原理 | Lab 手册 |
| **Web 与 PKI** | | |
| L18 | SQL 注入攻击 | Lab 手册 |
| L19 | XSS 与 CSRF | Lab 手册 |
| L20 | 会话管理与劫持 | Lab 手册 |
| L21 | PKI/DNSSEC/HTTPS：证书链与 DNS 欺骗下 HTTPS | Lab 手册 |
| **移动/云/IoT/前沿** | | |
| L22 | Android 权限与 Content Provider 攻击 | Lab 手册 |
| L23 | 侧信道（缓存计时/Speculative） | Lab 手册 |
| L24 | 软件安全防御（ASan/加固）与 云安全/IoT/区块链 选做 | Lab 手册 |

> 注：官方共 40+ labs 且逐年新增（Wireless、Blockchain、Spectre 侧信道、容器逃逸等），本表按主题聚成 24 个学习单元；填充笔记时按当期 seedsecuritylabs.org/labcategories.html 对齐。

## 作业与项目（概览）

作业即各 Lab 任务（攻击+防御+报告）。配套计划见 `projects/README.md`（以环境搭建与主题复刻为主）。
