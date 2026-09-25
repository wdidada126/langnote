# Stanford CS144 — Computer Network（计算机网络）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Stanford CS144: Computer Network |
| 学校 | Stanford University |
| 主讲 | Nick McKeown（网络领域巨擘，每章末采访业界/学界大咖）、Keith Winstein 等 |
| 教材 | 无固定教材；以课程讲义 + RFC（791/793/1122 等）+ 《Computer Networks: A Systems Approach》风格内容参照 |
| csdiy 路径 | 计算机网络/CS144 |
| 最新期次 | 2024（24 Winter/Spring 公开版；课程仓库每年清空，2024 版存档见 Wayback：web.archive.org/web/2024120904804/https://cs144.github.io/） |
| 状态 | 骨架（notes / papers / projects 待后续填充） |

## 为什么学

- csdiy 难度标星 🌟🌟🌟🌟🌟、约 100 学时：用 C++ 循序渐进搭建**整个 TCP/IP 协议栈**，是网络工程实现能力的天花板级训练。
- 8 个 checkpoint 串起完整栈：webget/字节流（CP0）→ 标准兼容的 TCP（CP1–3）→ 替换内核 socket 跑真实网络并做流量可视化分析（CP4）→ NetworkInterface/ARP（CP5）→ IP Router（CP6）→ 端到端互联（CP7）。
- csdiy 观点：与其说是网络课，不如说是「年轻人最好的现代 C++ 入门课」；精华在框架代码，逐行读懂才能回答「三次握手去哪了/多线程怎么办」这类问题——「计算机的世界里没有魔法」。

## 先修与知识联系

- 先修：一定的计算机系统基础（CSAPP 级别）、CS106L（现代 C++）。
- 语言：C++（C++17）；预计学时：100 小时。
- 知识联系：理论线承接自顶向下/CS168（协议语义），工程线打通 OS（socket、内核旁路）、并发（线程安全的字节流）、现代 C++（智能指针、move 语义、variants）。与 MIT 6.S081 网络栈章节互相印证。

## 讲义章节目录（2024 期，按主题周整理；具体以当期 schedule 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 课程导论：从短信到互联网、datagram/封装/复用 | CS144 Notes Lecture 1 |
| L02 | 物理链路：编码、带宽 vs 时延、Shannon 极限 | Lecture 2 |
| L03 | 以太网：帧、CRC、MAC 地址 | Lecture 3；IEEE 802.3 概览 |
| L04 | Wi-Fi：802.11、CSMA/CA | Lecture 4 |
| L05 | 交换：学习型交换机、生成树 | Lecture 5 |
| L06 | 网络服务与 IP：尽力而为、前缀、转发 | Lecture 6；RFC 791 |
| L07 | IP 路由：RIP/OSPF/BGP 速览、路由表查找 | Lecture 7 |
| L08 | ICMP、DHCP、NAT | Lecture 8 |
| L09 | 链路层与网络层之间：ARP 与转发实战 | Lecture 9（对应 CP5） |
| L10 | 可靠传输协议理论：滑动窗口、GBN/SR | Lecture 10 |
| L11 | TCP 概览：RFC 793 状态机与选项 | Lecture 11；RFC 793/1122 |
| L12 | TCP 机制：序号、重传、流量控制 | Lecture 12（对应 CP1–3） |
| L13 | TCP 拥塞控制总览：慢启动、AIMD | Lecture 13；RFC 5681 |
| L14 | TCP 拥塞控制细节：快重传/恢复、CUBIC | Lecture 14 |
| L15 | 真实网络中的 TCP：AQM、bufferbloat、流量数据分析 | Lecture 15 + CP4 数据分析 |
| L16 | 数据中心网络基础 | Lecture 16 |
| L17 | 中间盒与 NAT Traversal | Lecture 17 |
| L18 | 内容分发与流媒体：CDN、视频 | Lecture 18 |
| L19 | 网络安全：TLS 概览 | Lecture 19 |
| L20 | 测量与前沿：主动/被动测量、结课 | Lecture 20 |

## 资源

- 课程网站：https://cs144.github.io/ ；作业即 8 个 Project checkpoint（CP0–CP7）+ Labs（telnet/netcat、tcpdump/Wireshark）。
- 视频（MOOC 开源版）：YouTube 列表（csdiy 页面链接）。
- 资源汇总：PKUFlyingPig/Lexssama/xzhseh 等博客与 libsponge 等库实现（见 csdiy 页面资源列表）；入门/通关指南推荐 xzhseh 的 CS144 (24 Winter) 通关文。
