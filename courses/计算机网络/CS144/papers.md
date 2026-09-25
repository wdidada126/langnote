# CS144 论文与应用清单（papers.md）

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| A Protocol for Packet Network Intercommunication (Cerf & Kahn) | 1974 | 互联网通信协议原始设计，datagram/网关思想的源头 | L01/L06 |
| End-to-End Arguments in System Design (Saltzer, Reed, Clark) | 1984 | 端到端原则：智能放边缘——本课把可靠性放进主机 TCP 的根据 | L01/L12 |
| Ethernet: Distributed Packet Switching for Local Computer Networks (Metcalfe & Boggs) | 1976 | 以太网与 CSMA/CD 原始论文 | L03 |
| Congestion Avoidance and Control (Van Jacobson) | 1988 | 慢启动/AIMD/快重传，TCP 拥塞控制奠基 | L13–L14 |
| Random Early Detection (Floyd & Jacobson) | 1993 | AQM 路由器主动丢包信号 | L14/L15 |
| TCP and IP: RFC 791 / RFC 793 / RFC 1122 (Postel et al.) | 1981 | TCP/IP 协议规范基础（CP1–3 的验收依据） | L06/L11–L12 |
| Wireless LANs: IEEE 802.11 标准 | 1997 | CSMA/CA、ACK、隐终端与 RTS/CTS | L04 |
| Bridging and the Spanning Tree Protocol (IEEE 802.1D, Perlman) | 1985/1990 | 自学习网桥 + 生成树破环 | L05 |
| A Border Gateway Protocol 4 (RFC 4271, Rekhter & Li) | 2006 | 域间路由标准 | L07 |
| CUBIC: A New TCP-Friendly High-Speed TCP Variant (Ha, Rhee, Xu) | 2008 | 高带宽窗口增长函数 | L14 |
| BBR: Congestion-Based Congestion Control (Cardwell et al., SIGCOMM) | 2017 | 用带宽/RTT 模型取代丢包信号，重开设计空间 | L14–L15 |
| OpenFlow: Enabling Innovation in a White Box Switch (McKeown et al.) | 2008 | 转发/控制分离，SDN 起点 | L05/L16 |
| Controlling Queue Delay (Nichols & Jacobson, ACM Queue) | 2012 | 指出过量缓冲（bufferbloat）危害并提出 CoDel AQM | L15 |

## 近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| QUIC: A UDP-Based Multiplexed and Secure Transport (RFC 9000/9002) | 2021 | 用户态重建传输层：CP 风格的可靠传输在工业界的回归 | L10–L12/L18 |
| SDCP: Software Congestion Control with Predictors (Harvard) | 2021 | 主机侧带宽/时延预测实现低时延传输 | L14/L16 |
| Canopy: Cost-Efficient Congestion Control in Datacenters via Inband Network Telemetry | 2021 | INT 遥测驱动数据中心拥塞控制 | L16 |
| PLB: Congestion Signals Are Simple and Effective for Network Load Balancing (Google) | 2022 | 端侧 TCP 信号即可绕开网络热点 | L16 |

## 知识点在开源项目中的应用

| 知识点 | 开源项目 | 说明 |
| --- | --- | --- |
| TCP 协议栈/拥塞控制 | Linux 内核 `net/ipv4/tcp*.c`（CUBIC/BBR） | CP1–3 的工业对照；`ss -ti` 观测窗口/RTT |
| 用户态 TCP 实现 | mTCP / F-Stack / lwIP | 与 CS144 自建栈思路同构（内核旁路） |
| 可靠字节流/流重组 | Seastar / ScyllaDB、TLS 记录层 | StreamReassembler 的分片管理类似实现 |
| 以太网/交换机 | Linux bridge / Open vSwitch | L05 自学习转发与 STP/流表 |
| Wi-Fi | mac80211 / hostapd | L04 关联与信道接入 |
| IP 转发与路由 | FRRouting / Linux 路由子系统 / DPDK L3 转发示例 | L06–L07、CP6 IPRouter 对照 |
| ARP/邻居发现 | Linux neigh 子系统 | CP5 NetworkInterface 的内核版 |
| NAT/中间盒 | netfilter/conntrack | L08/L17 |
| CDN/流媒体/QUIC | Nginx / quic-go / lsquic | L18 落地 |
| SDN/数据中心 | OVS-DPDK / P4 可编程交换机 / Cilium (eBPF/XDP) | L16 转发面与端侧改造 |
