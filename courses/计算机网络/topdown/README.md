# Computer Networking: A Top-Down Approach（自顶向下方法 · Kurose & Ross 配套课）【CORE】

> 状态：**全量（2026-09）**——notes/ 24 讲中文笔记、papers.md 论文与 RFC 总表、projects/ 7 个配套 Python 项目均已完成。

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Computer Networking: A Top-Down Approach（教材配套课程） |
| 学校 | University of Massachusetts Amherst / 马萨诸塞大学（作者归属） |
| 主讲 | Jim Kurose、Keith Ross（教材作者亲自录制的网课） |
| 教材 | Computer Networking: A Top-Down Approach（第 7 版；中文版：机械工业出版社） |
| csdiy 路径 | 计算机网络/topdown |
| 最新期次 | 教材第 7 版配套站（gaia.cs.umass.edu/kurose_ross，持续更新） |
| 状态 | 全量（2026-09） |

## 为什么学

- 计算机网络领域最经典教材《自顶向下方法》的官方配套课：两位作者精心制作了课程网站，并**公开了自己录制的网课视频、交互式在线章节测试、以及利用 Wireshark 的抓包分析 lab**。
- 自顶向下的教学顺序（应用层→传输层→网络层→链路层）最符合认知规律：先见到 HTTP/DNS 这些「用得着」的东西，再逐层向下挖掘。
- 唯一遗憾是没有硬核编程作业——csdiy 明确指出可用 Stanford CS144 弥补；中文授课版可搭配 USTC 郑烇课程（同目录 topdown_ustc）。

## 先修与知识联系

- 先修要求：有一定的计算机系统基础；难度 🌟🌟🌟；预计学时 40 小时；无指定语言。
- 知识联系：与 topdown_ustc（中文视频版）同源互参；CS168（架构视角）、CS144（实现视角）构成计算机网络三件套。

## 讲义全章节目录（按教材第 7 版；配套讲座视频章节以官网 lectures 页为准）

### Chapter 1 — Computer Networks and the Internet
- 1.1 Network Edge：hosts、access networks、guided/unguided media、traces of the Internet
- 1.2 Network Core：circuit switching、packet switching、queueing/delay、throughput
- 1.3 Layering、Services, and Protocols：layer models、encapsulation
- 1.4 Networks Networks、Internetworks、WANs
- 1.5 Addresses：IP、DNS names
- 1.6 Performance
- 1.7 A Day in the Life of a Web Server / History & Structuring

### Chapter 2 — Application Layer
- 2.1 Application-Layer Principles：protocols、client-server、P2P
- 2.2 Web and HTTP：requests、connections、caching/CDN
- 2.3 DNS：name servers、records、attacks
- 2.4 Programming with TCP/UDP（socket 入门）
- 2.5 Video Streaming & Content Distribution（DASH）
- 2.6 File Distribution：BitTorrent（P2P 案例）

### Chapter 3 — Transport Layer
- 3.1 Overview and Transport-Layer Services
- 3.2 Multiplexing and Demultiplexing
- 3.3 Connectionless Transport: UDP（含可靠传输原则）
- 3.4 Principles of Reliable Data Transfer（rdt0–rdt3.0）
- 3.5 Connection-Oriented Transport: TCP — structure、flow control、RTT、loss recovery
- 3.6 TCP Congestion Control：TCP Tahoe/Reno、公平性
- 3.7 An Introductory Look at Transport Layer in OS / 活动与演进（TLS、QUIC）

### Chapter 4 — The Network Layer: Data Plane
- 4.1 Introduction（forwarding vs routing）
- 4.2 Routers and Forwarding：input/output ports、switching fabric、lookup、NAT
- 4.3 Data-Plane IP Forwarding：longest prefix matching、hardware
- 4.4 IPv4 / IPv6：datagram format、fragmentation、addresses、subnetting、DHCP、mobility basics
- 4.5 Link Layer Basics as Needed for Forwarding（ARP）
- 4.6 Data-Plane Troubleshooting（traceroute/ping）

### Chapter 5 — The Network Layer: Control Plane
- 5.1 Routing Algorithms：link-state (Dijkstra)、distance-vector (Bellman-Ford)、comparison
- 5.2 Route Selection：BGP basics、policy、iBGP/eBGP、route reflectors
- 5.3 The Legacy Control Plane：OSPF、RIP、SDN control plane (OpenFlow/ONOS)
- 5.4 ICMP（error & query）
- 5.5 Control-Plane Troubleshooting（looking-glass、BGP monitors、looking up routes）

### Chapter 6 — Link Layer and LANs
- 6.1 Introduction：framing、reliable delivery over links
- 6.2 Error Detection and Correction：parity、checksum、CRC、海明码
- 6.3 Multiple Access Protocols：FDMA/TDMA/CDMA、ALOHA、CSMA/CA、interleaving
- 6.4 Ethernet：history、frame format、switches、self-learning、bridging、broadcast/STP
- 6.5 Interface Cards & Link Layer in OS
- 6.6 XPON（GPON 接入）

### Chapter 7 — Wireless and Mobile Networks
- 7.1 Wi-Fi：802.11 architecture（ad-hoc/infrastructure、channels、frame format、associations）、DSSS/FHSS/OFDM、CSMA/CA、hidden terminal/RTS-CTS、802.11 security
- 7.2 Wi-Fi Networks：handoffs、enterprise、mesh、VoIP
- 7.3 Cellular Networks：architecture、data services、mobility management、4G LTE/5G
- 7.4 Mobile Architecture：network layer mobility（care-of address、tunneling）、transport mobility（TCP 分片、indirect TCP）、handoffs

### 在线补充（第 7 版起移出纸质书，官网可下载）
- Security in Computer Networks：密码学基础、认证、完整性、TLS/SSL、防火墙、VPN、DoS
- 各章 Interactive Practice / Quiz（官网 onlineCquizzes）

## Lab 与测试资源（官方）

- Wireshark labs：https://gaia.cs.umass.edu/kurose_ross/wireshark.php （HTTP/DNS/TCP/UDP/IP/以太网/802.11 等抓包实验）
- 课程网站/视频：https://gaia.cs.umass.edu/kurose_ross/index.php 、…/lectures.php
- 资源汇总：PKUFlyingPig/Computer-Network-A-Top-Down-Approach（GitHub）

## 目录产出说明

- `notes/`：24 讲中文笔记（README.md 为索引），每讲含核心概念、协议字段/状态机/公式、封装栈与前后讲联系、跨课程联系（CSAPP/6.S081/CS162/MIT6.824/CS144/topdown_ustc）、开源项目应用、按讲次 RFC 延伸阅读与自查题。
- `papers.md`：经典论文/RFC 表 + 近 5 年（2021–2026）动态表 + 知识点↔开源项目映射表（Linux、DPDK/VPP、quiche/lsquic、Nginx/Envoy、Wireshark、io_uring 等）。
- `projects/`：7 个纯标准库 Python 项目（HTTP 服务器、DNS 查询器、ARQ 模拟、TCP/UDP 双版聊天、拥塞控制模拟、路由器模拟、以太网/CRC/交换机模拟），各含源码、README、run.bat/run.sh（内置 py_compile 自检）；总表见 `projects/README.md`。本轮代码只写未编译，首次使用请先跑 run 脚本自检。
