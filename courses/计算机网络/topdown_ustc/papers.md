# USTC 计算机网络（自顶向下）论文与应用清单（papers.md）

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| A Brief History of the Internet (Leiner, Cerf, Clark et al.) | 2009 | 互联网编年史：分层与包交换设计选择的由来 | L01 |
| Ethernet: Distributed Packet Switching for Local Computer Networks (Metcalfe & Boggs) | 1976 | 以太网与 CSMA/CD 原始论文 | L13/L14 |
| Congestion Avoidance and Control (Van Jacobson) | 1988 | 慢启动/AIMD/快重传，TCP 拥塞控制奠基 | L08 |
| Analysis and Simulation of a High-Speed TCP (Floyd) | 1994 | Reno/SACK 丢包恢复的定量建模 | L07 |
| Random Early Detection (Floyd & Jacobson) | 1993 | AQM：路由器主动给出拥塞信号 | L08 |
| DiffServ Architecture (RFC 2475, Blake et al.) | 1998 | 粗粒度服务质量体系 | L08 |
| A Domain Name System (Mockapetis) | 1987 | 层次化分布式命名服务 | L04 |
| RFC 791 IP / RFC 793 TCP (Postel) | 1981 | 网络层与传输层协议规范基础 | L06–L10 |
| RIP: A Routing Protocol Based on Distance Vector (RFC 1058) | 1988 | 距离向量路由的原始定义与计数到无穷问题 | L11 |
| OSPF Specification (RFC 2328, Moy) | 1998 | 链路状态域内路由工业标准 | L11 |
| A Border Gateway Protocol 4 (RFC 4271) | 2006 | 策略驱动的域间路由标准 | L12 |
| Multicast Routing in Internetworks and Extended LANs (Deering & Cheriton) | 1990 | DVMRP：组播路由思想的开山之作 | L12 |
| Wireless LANs: IEEE 802.11 标准 | 1997 | CSMA/CA 与无线接入机制 | L15 |
| IP Mobility Support (RFC 3344, Johnson) | 2002 | 移动 IP：转交地址与隧道 | L16 |
| End-to-End Arguments in System Design (Saltzer, Reed, Clark) | 1984 | 端到端原则，分层设计思想根基 | L01/L12 |

## 近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| QUIC: A UDP-Based Multiplexed and Secure Transport (RFC 9000) | 2021 | 用户态可靠传输+加密，改写传输层格局 | L05/L07 |
| Evaluating BBRv2 Under Real-World Network Conditions (Calderón et al., WWW) | 2021 | 新一代模型驱动拥塞控制的现实网络实测 | L08 |
| PLB: Congestion Signals Are Simple and Effective for Network Load Balancing | 2022 | 端侧信号绕开数据中心热点 | L08/L13 |
| SDCP: Software Congestion Control with Predictors | 2021 | 主机侧预测实现超低时延传输 | L08 |
| Inband Network Telemetry 系列后续部署论文 | 2021–2023 | 数据平面可观测性支撑网络诊断（traceroute 的现代化） | L09–L10/L13 |

## 知识点在开源项目中的应用

| 知识点 | 开源项目 | 说明 |
| --- | --- | --- |
| HTTP/DNS/CDN | Nginx / bind9 / Unbound | L03/L04 生产落地 |
| UDP/QUIC | quic-go / lsquic | L05 现代传输 |
| TCP 拥塞控制 | Linux 内核（CUBIC/BBR，`net/ipv4/tcp_bbr.c`） | L07/L08；`ss -ti`、`iperf3` 观测 |
| 路由/转发 | FRRouting（OSPF/BGP）/ Linux 路由子系统 | L09–L12 |
| NAT | netfilter conntrack / iptables | L10 |
| 交换/以太网 | Linux bridge / Open vSwitch | L13 学习转发与 STP |
| Wi-Fi/移动 | hostapd / mac80211 / Open5GS（5G 核心网开源实现） | L15/L16 |
| 抓包分析 | Wireshark / tcpdump / Scapy | 全课程 lab 工具（对应官方 WireShark labs） |
